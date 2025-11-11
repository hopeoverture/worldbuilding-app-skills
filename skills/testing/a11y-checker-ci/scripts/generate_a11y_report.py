#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate accessibility test reports from axe-core results."""

import argparse
import io
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any

# Configure stdout for UTF-8 encoding (prevents Windows encoding errors)
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


class A11yReportGenerator:
    """Generate markdown reports from accessibility test results."""

    SEVERITY_ICONS = {
        'critical': '[CRITICAL]',
        'serious': '[SERIOUS]',
        'moderate': '[MODERATE]',
        'minor': '[MINOR]'
    }

    SEVERITY_ORDER = ['critical', 'serious', 'moderate', 'minor']

    def __init__(self, results_file: str):
        """Initialize with results file."""
        with open(results_file, 'r') as f:
            self.results = json.load(f)

    def generate_report(self, format_type: str = 'github') -> str:
        """Generate report in specified format."""
        if format_type == 'github':
            return self._generate_github_report()
        elif format_type == 'gitlab':
            return self._generate_gitlab_report()
        elif format_type == 'slack':
            return self._generate_slack_report()
        else:
            return self._generate_github_report()

    def _generate_github_report(self) -> str:
        """Generate report formatted for GitHub PR comments."""
        violations = self._extract_violations()
        summary = self._generate_summary(violations)

        report = "# Accessibility Test Report\n\n"
        report += summary + "\n\n"

        if violations:
            report += "## Violations\n\n"
            report += self._generate_violations_section(violations)
        else:
            report += "**[PASS] No accessibility violations found!**\n\n"
            report += "All tested pages meet WCAG 2.1 Level AA standards.\n"

        report += "\n---\n"
        report += f"*Report generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n"

        return report

    def _generate_gitlab_report(self) -> str:
        """Generate report formatted for GitLab MR comments."""
        # Similar to GitHub but with GitLab-specific formatting
        return self._generate_github_report()

    def _generate_slack_report(self) -> str:
        """Generate report formatted for Slack."""
        violations = self._extract_violations()
        total = sum(len(v) for v in violations.values())

        if total == 0:
            return "[PASS] Accessibility tests passed! No violations found."

        report = f"[WARN] Accessibility Report: {total} violations found\n\n"

        for severity in self.SEVERITY_ORDER:
            if violations.get(severity):
                count = len(violations[severity])
                icon = self.SEVERITY_ICONS[severity]
                report += f"{icon} *{severity.title()}*: {count}\n"

        return report

    def _extract_violations(self) -> Dict[str, List[Dict]]:
        """Extract and organize violations by severity."""
        violations = {
            'critical': [],
            'serious': [],
            'moderate': [],
            'minor': []
        }

        # Handle different result formats
        if isinstance(self.results, list):
            # Playwright format
            for result in self.results:
                if 'violations' in result:
                    for violation in result['violations']:
                        impact = violation.get('impact', 'minor')
                        violations[impact].append(violation)
        elif isinstance(self.results, dict):
            # Single result format
            if 'violations' in self.results:
                for violation in self.results['violations']:
                    impact = violation.get('impact', 'minor')
                    violations[impact].append(violation)

        return violations

    def _generate_summary(self, violations: Dict[str, List[Dict]]) -> str:
        """Generate executive summary."""
        total = sum(len(v) for v in violations.values())
        status = "[FAIL] Failed" if total > 0 else "[PASS] Passed"

        summary = f"**Status:** {status}\n"
        summary += f"**Total Violations:** {total}\n"
        summary += f"**WCAG Level:** AA\n\n"

        summary += "## Summary by Severity\n\n"

        for severity in self.SEVERITY_ORDER:
            count = len(violations.get(severity, []))
            icon = self.SEVERITY_ICONS[severity]
            summary += f"- {icon} **{severity.title()}:** {count}\n"

        return summary

    def _generate_violations_section(self, violations: Dict[str, List[Dict]]) -> str:
        """Generate detailed violations section."""
        section = ""

        for severity in self.SEVERITY_ORDER:
            severity_violations = violations.get(severity, [])
            if not severity_violations:
                continue

            icon = self.SEVERITY_ICONS[severity]
            count = len(severity_violations)
            section += f"### {icon} {severity.title()} ({count})\n\n"

            for i, violation in enumerate(severity_violations, 1):
                section += self._format_violation(i, violation, severity)
                section += "\n---\n\n"

        return section

    def _format_violation(self, index: int, violation: Dict, severity: str) -> str:
        """Format a single violation."""
        rule_id = violation.get('id', 'unknown')
        description = violation.get('description', 'No description')
        help_text = violation.get('help', '')
        help_url = violation.get('helpUrl', '')

        output = f"#### {index}. {description}\n\n"
        output += f"**Rule ID:** `{rule_id}`\n"
        output += f"**Impact:** {severity.title()}\n"

        # WCAG tags
        tags = [tag for tag in violation.get('tags', []) if 'wcag' in tag.lower()]
        if tags:
            output += f"**WCAG:** {', '.join(tags)}\n"

        output += "\n"

        if help_text:
            output += f"**Description:**\n{help_text}\n\n"

        # Affected elements
        nodes = violation.get('nodes', [])
        if nodes:
            output += f"**Affected Elements:** {len(nodes)}\n\n"
            output += "<details>\n<summary>Show affected elements</summary>\n\n"
            output += "```html\n"

            for node in nodes[:5]:  # Limit to first 5
                html = node.get('html', '')
                if html:
                    output += f"{html}\n"

            if len(nodes) > 5:
                output += f"\n... and {len(nodes) - 5} more\n"

            output += "```\n"
            output += "</details>\n\n"

        # Remediation
        if help_url:
            output += f"**More Information:** [{help_url}]({help_url})\n\n"

        return output


def main():
    parser = argparse.ArgumentParser(
        description="Generate accessibility test reports"
    )
    parser.add_argument(
        '--input',
        required=True,
        help='Input JSON file with test results'
    )
    parser.add_argument(
        '--output',
        default='accessibility-report.md',
        help='Output markdown file'
    )
    parser.add_argument(
        '--format',
        choices=['github', 'gitlab', 'slack'],
        default='github',
        help='Report format'
    )

    args = parser.parse_args()

    # Check input file exists
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input file not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    # Generate report
    try:
        generator = A11yReportGenerator(args.input)
        report = generator.generate_report(args.format)

        # Write output
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w') as f:
            f.write(report)

        print(f"Report generated: {output_path}")

    except Exception as e:
        print(f"Error generating report: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
