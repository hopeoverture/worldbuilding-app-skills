#!/usr/bin/env python3
"""
Analyze Next.js routes and Server Actions to provide optimization recommendations.

Usage:
    python analyze_routes.py --path /path/to/app --output analysis-report.md
    python analyze_routes.py --path ./app --format json
"""

import os
import re
import json
import argparse
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple
from dataclasses import dataclass, asdict


@dataclass
class RouteInfo:
    """Information about a route or Server Action."""
    path: str
    type: str  # 'api_route' or 'server_action'
    methods: List[str]  # HTTP methods for API routes
    has_auth: bool
    has_revalidation: bool
    has_external_api: bool
    has_form_data: bool
    has_streaming: bool
    has_cookies: bool
    has_headers: bool
    recommendation: str
    reason: str
    migration_complexity: str  # 'low', 'medium', 'high'


class RouteAnalyzer:
    """Analyze Next.js routes and Server Actions."""

    def __init__(self, app_path: str):
        self.app_path = Path(app_path)
        self.routes: List[RouteInfo] = []

    def analyze(self) -> List[RouteInfo]:
        """Analyze all routes in the app directory."""
        # Find all route.ts/js files (API routes)
        for route_file in self.app_path.rglob('route.*'):
            if route_file.suffix in ['.ts', '.tsx', '.js', '.jsx']:
                self._analyze_api_route(route_file)

        # Find Server Actions (files with 'use server')
        for file in self.app_path.rglob('*.*'):
            if file.suffix in ['.ts', '.tsx', '.js', '.jsx']:
                if self._has_server_directive(file):
                    self._analyze_server_actions(file)

        return self.routes

    def _has_server_directive(self, file_path: Path) -> bool:
        """Check if file has 'use server' directive."""
        try:
            content = file_path.read_text(encoding='utf-8')
            return "'use server'" in content or '"use server"' in content
        except:
            return False

    def _analyze_api_route(self, file_path: Path):
        """Analyze an API route file."""
        try:
            content = file_path.read_text(encoding='utf-8')
        except:
            return

        # Detect HTTP methods
        methods = []
        for method in ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']:
            if re.search(rf'export\s+async\s+function\s+{method}', content):
                methods.append(method)

        if not methods:
            return

        # Analyze patterns
        has_auth = self._detect_auth(content)
        has_revalidation = self._detect_revalidation(content)
        has_external_api = self._detect_external_api(content)
        has_form_data = self._detect_form_data(content)
        has_streaming = self._detect_streaming(content)
        has_cookies = self._detect_cookies(content)
        has_headers = self._detect_custom_headers(content)

        # Generate recommendation
        recommendation, reason, complexity = self._recommend_for_api_route(
            methods=methods,
            has_auth=has_auth,
            has_revalidation=has_revalidation,
            has_external_api=has_external_api,
            has_form_data=has_form_data,
            has_streaming=has_streaming,
            has_cookies=has_cookies,
            has_headers=has_headers,
        )

        route_info = RouteInfo(
            path=str(file_path.relative_to(self.app_path)),
            type='api_route',
            methods=methods,
            has_auth=has_auth,
            has_revalidation=has_revalidation,
            has_external_api=has_external_api,
            has_form_data=has_form_data,
            has_streaming=has_streaming,
            has_cookies=has_cookies,
            has_headers=has_headers,
            recommendation=recommendation,
            reason=reason,
            migration_complexity=complexity,
        )

        self.routes.append(route_info)

    def _analyze_server_actions(self, file_path: Path):
        """Analyze Server Actions in a file."""
        try:
            content = file_path.read_text(encoding='utf-8')
        except:
            return

        # Find exported async functions
        function_pattern = re.compile(
            r'export\s+(?:async\s+)?function\s+(\w+)',
            re.MULTILINE
        )

        for match in function_pattern.finditer(content):
            function_name = match.group(1)

            # Try to extract function body (basic approach)
            start = match.start()
            # Find the opening brace
            brace_pos = content.find('{', start)
            if brace_pos == -1:
                continue

            # Simple brace matching (not perfect but works for most cases)
            brace_count = 1
            pos = brace_pos + 1
            while pos < len(content) and brace_count > 0:
                if content[pos] == '{':
                    brace_count += 1
                elif content[pos] == '}':
                    brace_count -= 1
                pos += 1

            function_body = content[brace_pos:pos]

            # Analyze patterns in function body
            has_auth = self._detect_auth(function_body)
            has_revalidation = self._detect_revalidation(function_body)
            has_external_api = self._detect_external_api(function_body)
            has_form_data = 'FormData' in function_body

            # Generate recommendation
            recommendation, reason, complexity = self._recommend_for_server_action(
                function_name=function_name,
                has_auth=has_auth,
                has_revalidation=has_revalidation,
                has_external_api=has_external_api,
                has_form_data=has_form_data,
            )

            route_info = RouteInfo(
                path=f"{file_path.relative_to(self.app_path)}::{function_name}",
                type='server_action',
                methods=['POST'],  # Server Actions are POST-only
                has_auth=has_auth,
                has_revalidation=has_revalidation,
                has_external_api=has_external_api,
                has_form_data=has_form_data,
                has_streaming=False,
                has_cookies=False,
                has_headers=False,
                recommendation=recommendation,
                reason=reason,
                migration_complexity=complexity,
            )

            self.routes.append(route_info)

    def _detect_auth(self, content: str) -> bool:
        """Detect authentication patterns."""
        patterns = [
            r'auth\(',
            r'getServerSession',
            r'getSession',
            r'session',
            r'currentUser',
            r'verifyToken',
            r'authorization',
            r'Authorization',
        ]
        return any(re.search(pattern, content, re.IGNORECASE) for pattern in patterns)

    def _detect_revalidation(self, content: str) -> bool:
        """Detect revalidation calls."""
        return 'revalidatePath' in content or 'revalidateTag' in content

    def _detect_external_api(self, content: str) -> bool:
        """Detect external API calls."""
        patterns = [
            r'fetch\([\'"]https?://',
            r'axios\.',
            r'\.get\([\'"]https?://',
            r'\.post\([\'"]https?://',
        ]
        return any(re.search(pattern, content) for pattern in patterns)

    def _detect_form_data(self, content: str) -> bool:
        """Detect FormData handling."""
        return 'FormData' in content or 'formData' in content

    def _detect_streaming(self, content: str) -> bool:
        """Detect streaming responses."""
        return 'ReadableStream' in content or 'TransformStream' in content or 'stream' in content.lower()

    def _detect_cookies(self, content: str) -> bool:
        """Detect cookie operations."""
        return 'cookies()' in content or 'setCookie' in content

    def _detect_custom_headers(self, content: str) -> bool:
        """Detect custom header operations."""
        patterns = [
            r'headers\(\)',
            r'\.headers\.',
            r'setHeader',
            r'Response\.json\([^,]+,\s*\{[^}]*headers',
        ]
        return any(re.search(pattern, content) for pattern in patterns)

    def _recommend_for_api_route(
        self,
        methods: List[str],
        has_auth: bool,
        has_revalidation: bool,
        has_external_api: bool,
        has_form_data: bool,
        has_streaming: bool,
        has_cookies: bool,
        has_headers: bool,
    ) -> Tuple[str, str, str]:
        """Generate recommendation for an API route."""
        reasons = []

        # Strong indicators to keep as API route
        if has_external_api:
            reasons.append("proxies external API")
        if has_streaming:
            reasons.append("uses streaming responses")
        if has_custom_headers or has_cookies:
            reasons.append("requires custom headers/cookies")
        if 'GET' in methods or len(methods) > 1:
            reasons.append(f"uses multiple HTTP methods ({', '.join(methods)})")

        # Strong indicators to convert to Server Action
        if methods == ['POST'] and has_revalidation and not has_external_api:
            if has_form_data:
                return (
                    'Convert to Server Action',
                    'Simple POST with form data and revalidation - ideal for Server Action',
                    'low'
                )
            else:
                return (
                    'Convert to Server Action',
                    'POST-only mutation with revalidation - better as Server Action',
                    'low'
                )

        # Keep as API route
        if reasons:
            return (
                'Keep as API Route',
                'Better as API route: ' + ', '.join(reasons),
                'n/a'
            )

        # Neutral case - could go either way
        if methods == ['POST']:
            return (
                'Consider Server Action',
                'Simple POST endpoint could be simplified as Server Action',
                'low'
            )

        return (
            'Keep as API Route',
            'Current implementation is appropriate',
            'n/a'
        )

    def _recommend_for_server_action(
        self,
        function_name: str,
        has_auth: bool,
        has_revalidation: bool,
        has_external_api: bool,
        has_form_data: bool,
    ) -> Tuple[str, str, str]:
        """Generate recommendation for a Server Action."""
        # Check if Server Action might be better as API route
        if has_external_api and not has_revalidation:
            return (
                'Consider API Route',
                'External API calls without revalidation might be better as API route for reusability',
                'medium'
            )

        # Good use of Server Action
        if has_revalidation or has_form_data:
            return (
                'Keep as Server Action',
                'Good use of Server Action - leverages revalidation and/or form handling',
                'n/a'
            )

        # Neutral
        return (
            'Keep as Server Action',
            'Current implementation is appropriate',
            'n/a'
        )

    def generate_report(self, format: str = 'markdown') -> str:
        """Generate analysis report."""
        if format == 'json':
            return json.dumps([asdict(route) for route in self.routes], indent=2)

        # Markdown report
        lines = [
            '# Next.js Route Analysis Report',
            '',
            f'Analyzed {len(self.routes)} routes/actions',
            '',
        ]

        # Summary statistics
        api_routes = [r for r in self.routes if r.type == 'api_route']
        server_actions = [r for r in self.routes if r.type == 'server_action']
        needs_migration = [r for r in self.routes if 'Convert' in r.recommendation or 'Consider' in r.recommendation]

        lines.extend([
            '## Summary',
            '',
            f'- **API Routes**: {len(api_routes)}',
            f'- **Server Actions**: {len(server_actions)}',
            f'- **Recommended Migrations**: {len(needs_migration)}',
            '',
        ])

        # Recommendations for migration
        if needs_migration:
            lines.extend([
                '## Recommended Migrations',
                '',
            ])

            for route in needs_migration:
                lines.extend([
                    f'### {route.path}',
                    '',
                    f'**Current**: {route.type.replace("_", " ").title()}',
                    f'**Recommendation**: {route.recommendation}',
                    f'**Reason**: {route.reason}',
                    f'**Complexity**: {route.migration_complexity}',
                    '',
                ])

        # Detailed analysis
        lines.extend([
            '## Detailed Analysis',
            '',
        ])

        for route in self.routes:
            lines.extend([
                f'### {route.path}',
                '',
                f'- **Type**: {route.type.replace("_", " ").title()}',
                f'- **Methods**: {", ".join(route.methods)}',
                f'- **Authentication**: {"Yes" if route.has_auth else "No"}',
                f'- **Revalidation**: {"Yes" if route.has_revalidation else "No"}',
                f'- **External API**: {"Yes" if route.has_external_api else "No"}',
                f'- **Form Data**: {"Yes" if route.has_form_data else "No"}',
            ])

            if route.type == 'api_route':
                lines.extend([
                    f'- **Streaming**: {"Yes" if route.has_streaming else "No"}',
                    f'- **Custom Headers/Cookies**: {"Yes" if (route.has_cookies or route.has_headers) else "No"}',
                ])

            lines.extend([
                '',
                f'**Recommendation**: {route.recommendation}',
                f'**Reason**: {route.reason}',
                '',
            ])

        return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(
        description='Analyze Next.js routes and provide optimization recommendations'
    )
    parser.add_argument(
        '--path',
        required=True,
        help='Path to the Next.js app directory'
    )
    parser.add_argument(
        '--output',
        help='Output file path for the report'
    )
    parser.add_argument(
        '--format',
        choices=['markdown', 'json'],
        default='markdown',
        help='Output format (default: markdown)'
    )

    args = parser.parse_args()

    # Validate path
    app_path = Path(args.path)
    if not app_path.exists():
        print(f"Error: Path does not exist: {args.path}")
        return 1

    # Analyze routes
    analyzer = RouteAnalyzer(args.path)
    routes = analyzer.analyze()

    if not routes:
        print("No routes or Server Actions found.")
        return 0

    # Generate report
    report = analyzer.generate_report(format=args.format)

    # Write output
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(report, encoding='utf-8')
        print(f"Report written to: {args.output}")
    else:
        print(report)

    return 0


if __name__ == '__main__':
    exit(main())
