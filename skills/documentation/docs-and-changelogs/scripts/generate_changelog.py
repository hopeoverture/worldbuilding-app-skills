#!/usr/bin/env python3
"""
Generate CHANGELOG.md from Conventional Commits in git history.
"""

import argparse
import re
import subprocess
from collections import defaultdict
from datetime import datetime
from pathlib import Path


COMMIT_PATTERN = re.compile(
    r'^(?P<type>\w+)(?:\((?P<scope>[\w-]+)\))?(?P<breaking>!)?: (?P<description>.+)$'
)

TYPE_HEADERS = {
    'feat': 'Added',
    'fix': 'Fixed',
    'docs': 'Documentation',
    'style': 'Style',
    'refactor': 'Changed',
    'perf': 'Performance',
    'test': 'Tests',
    'chore': 'Maintenance',
    'ci': 'CI/CD',
    'build': 'Build',
    'revert': 'Reverted',
}


def get_commits(since=None, until='HEAD'):
    """Get git commits in range."""
    cmd = ['git', 'log', '--pretty=format:%H|%s|%b|%an|%ae|%ad', '--date=short']

    if since:
        cmd.append(f'{since}..{until}')
    else:
        cmd.append(until)

    result = subprocess.run(cmd, capture_output=True, text=True)

    commits = []
    for line in result.stdout.strip().split('\n'):
        if not line:
            continue
        parts = line.split('|')
        if len(parts) >= 6:
            commits.append({
                'hash': parts[0],
                'subject': parts[1],
                'body': parts[2],
                'author': parts[3],
                'email': parts[4],
                'date': parts[5],
            })

    return commits


def parse_commit(commit):
    """Parse conventional commit message."""
    match = COMMIT_PATTERN.match(commit['subject'])

    if not match:
        return None

    parsed = {
        'type': match.group('type'),
        'scope': match.group('scope'),
        'breaking': bool(match.group('breaking')),
        'description': match.group('description'),
        'hash': commit['hash'][:7],
        'full_hash': commit['hash'],
        'body': commit['body'],
    }

    # Check for BREAKING CHANGE in body
    if 'BREAKING CHANGE' in commit['body']:
        parsed['breaking'] = True
        # Extract breaking change description
        breaking_match = re.search(r'BREAKING CHANGE:\s*(.+)', commit['body'])
        if breaking_match:
            parsed['breaking_description'] = breaking_match.group(1)

    return parsed


def group_commits(commits):
    """Group commits by type and breaking changes."""
    groups = defaultdict(list)
    breaking = []

    for commit in commits:
        parsed = parse_commit(commit)
        if not parsed:
            continue

        if parsed['breaking']:
            breaking.append(parsed)

        commit_type = parsed['type']
        groups[commit_type].append(parsed)

    return groups, breaking


def format_commit(commit):
    """Format a single commit for changelog."""
    scope = f"**{commit['scope']}**: " if commit['scope'] else ""
    return f"- {scope}{commit['description']} ([{commit['hash']}](../../commit/{commit['full_hash']}))"


def generate_changelog_section(version, date, groups, breaking):
    """Generate a changelog section for a version."""
    lines = [
        f"## [{version}] - {date}",
        ""
    ]

    # Breaking changes first
    if breaking:
        lines.append("### BREAKING CHANGES")
        lines.append("")
        for commit in breaking:
            if 'breaking_description' in commit:
                lines.append(f"- {commit['breaking_description']}")
            else:
                lines.append(format_commit(commit))
        lines.append("")

    # Regular changes by type
    for commit_type, header in TYPE_HEADERS.items():
        if commit_type in groups and groups[commit_type]:
            lines.append(f"### {header}")
            lines.append("")
            for commit in groups[commit_type]:
                lines.append(format_commit(commit))
            lines.append("")

    return '\n'.join(lines)


def get_current_version():
    """Get current version from package.json."""
    try:
        import json
        with open('package.json') as f:
            data = json.load(f)
            return data.get('version', '0.0.0')
    except:
        return '0.0.0'


def get_last_tag():
    """Get the most recent git tag."""
    result = subprocess.run(
        ['git', 'describe', '--tags', '--abbrev=0'],
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        return result.stdout.strip()
    return None


def update_changelog(content, output_path):
    """Update or create CHANGELOG.md file."""
    changelog_path = Path(output_path)

    if changelog_path.exists():
        with open(changelog_path) as f:
            existing = f.read()

        # Insert new content after header
        if '## [' in existing:
            parts = existing.split('## [', 1)
            updated = parts[0] + content + '\n## [' + parts[1]
        else:
            updated = existing + '\n\n' + content
    else:
        # Create new changelog with header
        header = """# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

"""
        updated = header + content

    with open(changelog_path, 'w') as f:
        f.write(updated)

    print(f"Updated: {changelog_path}")


def main():
    parser = argparse.ArgumentParser(description='Generate changelog from git commits')
    parser.add_argument('--since', help='Start from this tag/commit')
    parser.add_argument('--until', default='HEAD', help='End at this tag/commit')
    parser.add_argument('--version', help='Version number for this release')
    parser.add_argument('--output', default='CHANGELOG.md', help='Output file path')
    parser.add_argument('--date', help='Release date (YYYY-MM-DD)')

    args = parser.parse_args()

    # Determine version and since
    version = args.version or get_current_version()
    since = args.since or get_last_tag()

    if not since:
        print("Warning: No previous tag found. Generating changelog for all commits.")

    # Get and parse commits
    commits = get_commits(since=since, until=args.until)

    if not commits:
        print("No commits found in range.")
        return

    groups, breaking = group_commits(commits)

    # Generate changelog section
    date = args.date or datetime.now().strftime('%Y-%m-%d')
    changelog_content = generate_changelog_section(version, date, groups, breaking)

    # Update changelog file
    update_changelog(changelog_content, args.output)

    # Print summary
    print(f"\nGenerated changelog for version {version}")
    print(f"  Commits processed: {len(commits)}")
    print(f"  Breaking changes: {len(breaking)}")
    print(f"  Features: {len(groups.get('feat', []))}")
    print(f"  Bug fixes: {len(groups.get('fix', []))}")


if __name__ == '__main__':
    main()
