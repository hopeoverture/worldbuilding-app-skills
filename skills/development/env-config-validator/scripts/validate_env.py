#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Validate environment configuration files.

Usage:
    python validate_env.py
    python validate_env.py --file .env.production
    python validate_env.py --compare .env.local .env.production
    python validate_env.py --template .env.example
"""

import os
import re
import io
import sys
import argparse
from pathlib import Path

# Configure stdout for UTF-8 encoding (prevents Windows encoding errors)
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from typing import Dict, List, Set, Tuple, Optional
from dataclasses import dataclass


@dataclass
class ValidationIssue:
    """Represents a validation issue."""
    severity: str  # 'error', 'warning', 'info'
    category: str  # 'security', 'naming', 'missing', 'weak'
    variable: str
    message: str
    suggestion: Optional[str] = None


class EnvValidator:
    """Validate environment configuration files."""

    # Required variable categories
    REQUIRED_CATEGORIES = {
        'database': ['DATABASE_URL', 'DB_URL', 'POSTGRES_URL', 'MONGODB_URI', 'MYSQL_URL'],
        'auth': ['JWT_SECRET', 'AUTH_SECRET', 'NEXTAUTH_SECRET', 'SESSION_SECRET'],
    }

    # Common secrets that should NOT be public
    SECRET_PATTERNS = [
        'SECRET', 'PASSWORD', 'KEY', 'TOKEN', 'CREDENTIAL',
        'DATABASE', 'DB_URL', 'CONNECTION', 'PRIVATE',
    ]

    # Weak or default values
    WEAK_VALUES = [
        'secret', 'password', 'test', 'example', 'changeme',
        '123456', 'admin', 'default', 'your-secret-here',
    ]

    def __init__(self, env_file: str = '.env'):
        self.env_file = Path(env_file)
        self.variables: Dict[str, str] = {}
        self.issues: List[ValidationIssue] = []

    def load_env_file(self) -> bool:
        """Load and parse environment file."""
        if not self.env_file.exists():
            self.issues.append(ValidationIssue(
                severity='error',
                category='missing',
                variable='',
                message=f'Environment file not found: {self.env_file}',
                suggestion='Create the file or check the path'
            ))
            return False

        try:
            content = self.env_file.read_text(encoding='utf-8')
        except Exception as e:
            self.issues.append(ValidationIssue(
                severity='error',
                category='parsing',
                variable='',
                message=f'Failed to read file: {e}',
            ))
            return False

        # Parse environment variables
        for line in content.split('\n'):
            line = line.strip()

            # Skip comments and empty lines
            if not line or line.startswith('#'):
                continue

            # Parse KEY=VALUE
            match = re.match(r'^([A-Z_][A-Z0-9_]*)\s*=\s*(.*)$', line)
            if match:
                key = match.group(1)
                value = match.group(2).strip()

                # Remove quotes if present
                if value.startswith('"') and value.endswith('"'):
                    value = value[1:-1]
                elif value.startswith("'") and value.endswith("'"):
                    value = value[1:-1]

                self.variables[key] = value

        return True

    def validate(self) -> List[ValidationIssue]:
        """Run all validation checks."""
        self.issues = []

        if not self.load_env_file():
            return self.issues

        # Run validation checks
        self._check_required_variables()
        self._check_naming_conventions()
        self._check_public_secrets()
        self._check_weak_values()
        self._check_secret_strength()

        return self.issues

    def _check_required_variables(self):
        """Check for required variables."""
        for category, possible_vars in self.REQUIRED_CATEGORIES.items():
            found = any(var in self.variables for var in possible_vars)

            if not found:
                self.issues.append(ValidationIssue(
                    severity='error',
                    category='missing',
                    variable=category,
                    message=f'Missing required {category} configuration',
                    suggestion=f'Add one of: {", ".join(possible_vars)}'
                ))

    def _check_naming_conventions(self):
        """Check variable naming conventions."""
        for key in self.variables.keys():
            # Check for lowercase or mixed case
            if not key.isupper():
                self.issues.append(ValidationIssue(
                    severity='warning',
                    category='naming',
                    variable=key,
                    message=f'Variable should use SCREAMING_SNAKE_CASE',
                    suggestion=f'Rename to: {key.upper()}'
                ))

            # Check for invalid characters
            if not re.match(r'^[A-Z_][A-Z0-9_]*$', key):
                self.issues.append(ValidationIssue(
                    severity='warning',
                    category='naming',
                    variable=key,
                    message='Variable name contains invalid characters',
                    suggestion='Use only uppercase letters, numbers, and underscores'
                ))

    def _check_public_secrets(self):
        """Check for secrets in public variables."""
        for key, value in self.variables.items():
            # Check if variable is public
            if not key.startswith('NEXT_PUBLIC_'):
                continue

            # Check if it looks like a secret
            for pattern in self.SECRET_PATTERNS:
                if pattern in key.upper():
                    self.issues.append(ValidationIssue(
                        severity='error',
                        category='security',
                        variable=key,
                        message='Secret exposed in public variable',
                        suggestion=f'Remove NEXT_PUBLIC_ prefix to make it private'
                    ))
                    break

            # Check for database URLs in public vars
            if any(db in key.upper() for db in ['DATABASE', 'DB_URL', 'POSTGRES', 'MONGODB', 'MYSQL']):
                self.issues.append(ValidationIssue(
                    severity='error',
                    category='security',
                    variable=key,
                    message='Database credentials exposed in public variable',
                    suggestion='Remove NEXT_PUBLIC_ prefix - database URLs must be private'
                ))

    def _check_weak_values(self):
        """Check for weak or default values."""
        for key, value in self.variables.items():
            value_lower = value.lower()

            # Check for weak values
            for weak in self.WEAK_VALUES:
                if weak in value_lower:
                    # Only error for secrets, warn for others
                    severity = 'error' if any(p in key.upper() for p in self.SECRET_PATTERNS) else 'warning'

                    self.issues.append(ValidationIssue(
                        severity=severity,
                        category='weak',
                        variable=key,
                        message=f'Weak or default value detected',
                        suggestion='Use a strong, random value'
                    ))
                    break

            # Check for empty values in required vars
            if not value:
                self.issues.append(ValidationIssue(
                    severity='warning',
                    category='missing',
                    variable=key,
                    message='Variable is defined but has no value',
                    suggestion='Provide a value or remove the variable'
                ))

    def _check_secret_strength(self):
        """Check strength of secret values."""
        secret_keys = [
            'JWT_SECRET', 'AUTH_SECRET', 'NEXTAUTH_SECRET',
            'SESSION_SECRET', 'ENCRYPTION_KEY', 'SECRET_KEY'
        ]

        for key in secret_keys:
            if key not in self.variables:
                continue

            value = self.variables[key]

            # Check minimum length (32 characters recommended)
            if len(value) < 32:
                self.issues.append(ValidationIssue(
                    severity='error',
                    category='weak',
                    variable=key,
                    message=f'Secret is too short ({len(value)} characters, minimum 32 recommended)',
                    suggestion='Generate a stronger secret with: node -e "console.log(require(\'crypto\').randomBytes(32).toString(\'hex\'))"'
                ))

            # Check for low entropy (repeating characters, patterns)
            if self._is_low_entropy(value):
                self.issues.append(ValidationIssue(
                    severity='warning',
                    category='weak',
                    variable=key,
                    message='Secret appears to have low entropy',
                    suggestion='Use a cryptographically random value'
                ))

    def _is_low_entropy(self, value: str) -> bool:
        """Check if a value has low entropy."""
        if len(value) < 10:
            return True

        # Check for repeating characters
        unique_chars = len(set(value))
        if unique_chars < len(value) / 3:
            return True

        # Check for sequential patterns
        if re.search(r'(.)\1{5,}', value):  # Same char repeated 5+ times
            return True

        if re.search(r'(abc|123|xyz|789)', value.lower()):  # Sequential patterns
            return True

        return False

    def compare_with(self, other_env_file: str) -> List[ValidationIssue]:
        """Compare with another environment file."""
        other = EnvValidator(other_env_file)
        other.load_env_file()

        comparison_issues = []

        # Variables in this file but not in other
        missing_in_other = set(self.variables.keys()) - set(other.variables.keys())
        for var in missing_in_other:
            comparison_issues.append(ValidationIssue(
                severity='warning',
                category='missing',
                variable=var,
                message=f'Variable exists in {self.env_file} but missing in {other_env_file}',
                suggestion=f'Add to {other_env_file} if required'
            ))

        # Variables in other but not in this file
        missing_in_this = set(other.variables.keys()) - set(self.variables.keys())
        for var in missing_in_this:
            comparison_issues.append(ValidationIssue(
                severity='warning',
                category='missing',
                variable=var,
                message=f'Variable exists in {other_env_file} but missing in {self.env_file}',
                suggestion=f'Add to {self.env_file} if required'
            ))

        # Check for same values (potential copy-paste error)
        for var in set(self.variables.keys()) & set(other.variables.keys()):
            # Skip checking NODE_ENV and similar environment-specific vars
            skip_vars = ['NODE_ENV', 'NEXT_PUBLIC_APP_NAME']
            if var in skip_vars:
                continue

            if self.variables[var] == other.variables[var]:
                # Only warn for secrets or URLs (should differ per environment)
                if any(p in var.upper() for p in ['SECRET', 'URL', 'KEY', 'TOKEN']):
                    if not var.startswith('NEXT_PUBLIC_'):  # Public URLs might be same
                        comparison_issues.append(ValidationIssue(
                            severity='warning',
                            category='security',
                            variable=var,
                            message=f'Same value in both {self.env_file} and {other_env_file}',
                            suggestion='Ensure environment-specific values are different'
                        ))

        return comparison_issues

    def validate_against_template(self, template_file: str) -> List[ValidationIssue]:
        """Validate against a template file (.env.example)."""
        template = EnvValidator(template_file)
        template.load_env_file()

        template_issues = []

        # Check for missing required variables
        for var in template.variables.keys():
            if var not in self.variables:
                template_issues.append(ValidationIssue(
                    severity='error',
                    category='missing',
                    variable=var,
                    message=f'Required variable (from {template_file}) is missing',
                    suggestion=f'Add {var} to {self.env_file}'
                ))

        return template_issues


def format_issues(issues: List[ValidationIssue]) -> str:
    """Format issues for display."""
    if not issues:
        return "[OK] No issues found!"

    lines = []

    # Group by severity
    errors = [i for i in issues if i.severity == 'error']
    warnings = [i for i in issues if i.severity == 'warning']
    info = [i for i in issues if i.severity == 'info']

    if errors:
        lines.append("\n=== ERRORS ===\n")
        for issue in errors:
            lines.append(f"[X] [{issue.category.upper()}] {issue.variable}")
            lines.append(f"  {issue.message}")
            if issue.suggestion:
                lines.append(f"  [TIP] {issue.suggestion}")
            lines.append("")

    if warnings:
        lines.append("\n=== WARNINGS ===\n")
        for issue in warnings:
            lines.append(f"[WARN] [{issue.category.upper()}] {issue.variable}")
            lines.append(f"  {issue.message}")
            if issue.suggestion:
                lines.append(f"  [TIP] {issue.suggestion}")
            lines.append("")

    if info:
        lines.append("\n=== INFO ===\n")
        for issue in info:
            lines.append(f"[INFO] [{issue.category.upper()}] {issue.variable}")
            lines.append(f"  {issue.message}")
            if issue.suggestion:
                lines.append(f"  [TIP] {issue.suggestion}")
            lines.append("")

    # Summary
    lines.append("\n=== SUMMARY ===")
    lines.append(f"Errors: {len(errors)}")
    lines.append(f"Warnings: {len(warnings)}")
    lines.append(f"Info: {len(info)}")

    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(
        description='Validate environment configuration files'
    )
    parser.add_argument(
        '--file',
        default='.env',
        help='Environment file to validate (default: .env)'
    )
    parser.add_argument(
        '--compare',
        nargs=2,
        metavar=('FILE1', 'FILE2'),
        help='Compare two environment files'
    )
    parser.add_argument(
        '--template',
        help='Validate against a template file (.env.example)'
    )

    args = parser.parse_args()

    # Comparison mode
    if args.compare:
        file1, file2 = args.compare
        print(f"Comparing {file1} and {file2}...\n")

        validator = EnvValidator(file1)
        validator.load_env_file()

        comparison_issues = validator.compare_with(file2)

        print(format_issues(comparison_issues))
        return 1 if any(i.severity == 'error' for i in comparison_issues) else 0

    # Template validation mode
    if args.template:
        print(f"Validating {args.file} against template {args.template}...\n")

        validator = EnvValidator(args.file)
        issues = validator.validate()

        template_issues = validator.validate_against_template(args.template)
        all_issues = issues + template_issues

        print(format_issues(all_issues))
        return 1 if any(i.severity == 'error' for i in all_issues) else 0

    # Standard validation mode
    print(f"Validating {args.file}...\n")

    validator = EnvValidator(args.file)
    issues = validator.validate()

    print(format_issues(issues))

    return 1 if any(i.severity == 'error' for i in issues) else 0


if __name__ == '__main__':
    exit(main())
