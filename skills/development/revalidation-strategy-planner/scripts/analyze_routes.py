#!/usr/bin/env python3
"""
Analyze Next.js routes and recommend revalidation strategies.
"""

import json
import os
import re
from pathlib import Path
from typing import Dict, List, Optional


class RouteAnalyzer:
    def __init__(self, app_dir: Path):
        self.app_dir = app_dir
        self.routes = []

    def analyze(self):
        """Analyze all routes in the app directory."""
        self.routes = []
        self._scan_directory(self.app_dir)
        return self.routes

    def _scan_directory(self, directory: Path, route_path: str = ""):
        """Recursively scan directory for routes."""
        if not directory.exists():
            print(f"Warning: Directory not found: {directory}")
            return

        for item in directory.iterdir():
            if item.name.startswith('_') or item.name.startswith('.'):
                continue

            if item.is_dir():
                # Handle route groups (groupName) and dynamic routes [param]
                if item.name.startswith('(') and item.name.endswith(')'):
                    # Route group - doesn't affect URL
                    self._scan_directory(item, route_path)
                elif item.name.startswith('[') and item.name.endswith(']'):
                    # Dynamic route segment
                    param = item.name
                    self._scan_directory(item, f"{route_path}/{param}")
                else:
                    # Regular route segment
                    self._scan_directory(item, f"{route_path}/{item.name}")

            elif item.name == 'page.tsx' or item.name == 'page.js':
                # Found a page route
                route = self._analyze_route_file(item, route_path or '/')
                if route:
                    self.routes.append(route)

    def _analyze_route_file(self, file_path: Path, route_path: str) -> Optional[Dict]:
        """Analyze a page file and determine recommendations."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Detect existing configuration
            has_revalidate = 'export const revalidate' in content
            has_dynamic = 'export const dynamic' in content
            has_fetch = 'fetch(' in content or 'await' in content
            has_suspense = 'Suspense' in content
            has_params = '[' in route_path and ']' in route_path
            has_searchparams = 'searchParams' in content

            # Determine route characteristics
            is_dynamic_route = has_params
            is_personalized = any(
                keyword in content.lower()
                for keyword in ['session', 'user', 'auth', 'dashboard']
            )
            is_list = any(
                keyword in route_path.lower()
                for keyword in ['/entities', '/timeline', '/characters', '/locations']
            )
            is_detail = is_dynamic_route and not is_list

            # Make recommendations
            recommendation = self._recommend_strategy(
                is_personalized=is_personalized,
                is_list=is_list,
                is_detail=is_detail,
                has_fetch=has_fetch,
                route_path=route_path,
            )

            return {
                'path': route_path,
                'file': str(file_path.relative_to(self.app_dir.parent)),
                'characteristics': {
                    'dynamic_route': is_dynamic_route,
                    'personalized': is_personalized,
                    'list_page': is_list,
                    'detail_page': is_detail,
                    'has_data_fetching': has_fetch,
                    'has_suspense': has_suspense,
                },
                'current_config': {
                    'has_revalidate': has_revalidate,
                    'has_dynamic': has_dynamic,
                },
                'recommendation': recommendation,
            }
        except Exception as e:
            print(f"Error analyzing {file_path}: {e}")
            return None

    def _recommend_strategy(
        self, is_personalized: bool, is_list: bool, is_detail: bool, has_fetch: bool, route_path: str
    ) -> Dict:
        """Recommend rendering and caching strategy."""

        # Personalized content needs SSR
        if is_personalized:
            return {
                'strategy': 'SSR',
                'config': "export const dynamic = 'force-dynamic';",
                'revalidate': None,
                'cache_tags': [],
                'reasoning': 'Personalized content requires server-side rendering for each request',
                'priority': 'high',
            }

        # Detail pages benefit from ISR
        if is_detail:
            return {
                'strategy': 'ISR',
                'config': 'export const revalidate = 1800; // 30 minutes',
                'revalidate': 1800,
                'cache_tags': [self._extract_entity_tag(route_path), 'entities'],
                'reasoning': 'Detail pages can use ISR with moderate revalidation for balance of performance and freshness',
                'priority': 'medium',
            }

        # List pages with frequent updates
        if is_list:
            return {
                'strategy': 'ISR',
                'config': 'export const revalidate = 300; // 5 minutes',
                'revalidate': 300,
                'cache_tags': ['entities', 'timeline', 'characters'],
                'reasoning': 'List pages benefit from shorter revalidation to show recent updates',
                'priority': 'medium',
            }

        # Static pages
        if not has_fetch:
            return {
                'strategy': 'SSG',
                'config': '// Static page, no revalidation needed',
                'revalidate': None,
                'cache_tags': [],
                'reasoning': 'No data fetching detected, suitable for static generation',
                'priority': 'low',
            }

        # Default to ISR with moderate interval
        return {
            'strategy': 'ISR',
            'config': 'export const revalidate = 600; // 10 minutes',
            'revalidate': 600,
            'cache_tags': [],
            'reasoning': 'Default ISR strategy provides good balance for most pages',
            'priority': 'low',
        }

    def _extract_entity_tag(self, route_path: str) -> str:
        """Extract entity name from route for cache tagging."""
        parts = route_path.split('/')
        for i, part in enumerate(parts):
            if part.startswith('[') and part.endswith(']'):
                if i > 0:
                    entity_type = parts[i - 1].rstrip('s')  # Remove plural 's'
                    return f"{entity_type}-{{id}}"
        return 'entity-{id}'

    def print_report(self):
        """Print analysis report."""
        print(f"\n{'=' * 80}")
        print(f"Next.js Revalidation Strategy Analysis")
        print(f"{'=' * 80}\n")

        print(f"Analyzed {len(self.routes)} routes\n")

        # Group by strategy
        strategies = {}
        for route in self.routes:
            strategy = route['recommendation']['strategy']
            if strategy not in strategies:
                strategies[strategy] = []
            strategies[strategy].append(route)

        for strategy, routes in strategies.items():
            print(f"\n{strategy} Routes ({len(routes)}):")
            print("-" * 80)
            for route in routes:
                rec = route['recommendation']
                print(f"\nRoute: {route['path']}")
                print(f"  File: {route['file']}")
                print(f"  Strategy: {rec['strategy']}")
                print(f"  Config: {rec['config']}")
                if rec['cache_tags']:
                    print(f"  Cache Tags: {', '.join(rec['cache_tags'])}")
                print(f"  Reasoning: {rec['reasoning']}")

    def export_json(self, output_path: Path):
        """Export analysis to JSON file."""
        with open(output_path, 'w') as f:
            json.dump(self.routes, f, indent=2)
        print(f"\nExported analysis to: {output_path}")


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Analyze Next.js routes for revalidation strategies')
    parser.add_argument('app_dir', help='Path to Next.js app directory')
    parser.add_argument('--output', '-o', help='Output JSON file path')

    args = parser.parse_args()

    app_dir = Path(args.app_dir)
    if not app_dir.exists():
        print(f"Error: Directory not found: {app_dir}")
        return 1

    analyzer = RouteAnalyzer(app_dir)
    analyzer.analyze()
    analyzer.print_report()

    if args.output:
        analyzer.export_json(Path(args.output))

    return 0


if __name__ == '__main__':
    exit(main())
