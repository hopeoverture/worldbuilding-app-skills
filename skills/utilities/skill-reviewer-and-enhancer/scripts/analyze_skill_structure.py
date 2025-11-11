#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Analyze skill structure and validate against Anthropic standards.

Usage:
    python analyze_skill_structure.py --skill skills/category/skill-name
"""

import sys
import io
import re
import argparse
from pathlib import Path
from typing import Dict, List, Tuple

# Configure stdout for UTF-8 encoding (prevents Windows encoding errors)
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def parse_frontmatter(content: str) -> Tuple[Dict[str, str], str]:
    """Extract and parse YAML frontmatter from SKILL.md"""
    if not content.startswith('---'):
        return {}, content

    match = re.match(r'^---\n(.*?)\n---\n(.*)$', content, re.DOTALL)
    if not match:
        return {}, content

    frontmatter_text = match.group(1)
    body = match.group(2)

    # Parse frontmatter
    frontmatter = {}
    for line in frontmatter_text.split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            frontmatter[key.strip()] = value.strip()

    return frontmatter, body

def check_name_convention(name: str) -> List[str]:
    """Check if name follows hyphen-case convention"""
    issues = []

    if not re.match(r'^[a-z0-9-]+$', name):
        issues.append(f"Name '{name}' should use only lowercase letters, digits, and hyphens")

    if name.startswith('-') or name.endswith('-'):
        issues.append(f"Name '{name}' cannot start or end with hyphen")

    if '--' in name:
        issues.append(f"Name '{name}' cannot contain consecutive hyphens")

    return issues

def check_description(description: str) -> List[str]:
    """Check description quality"""
    issues = []

    if len(description) > 1024:
        issues.append(f"Description is {len(description)} characters (max 1024)")

    if '<' in description or '>' in description:
        issues.append("Description cannot contain angle brackets")

    # Check for third-person voice
    first_person_patterns = [
        r'\bI\s+',
        r'\bwe\s+',
        r'\bour\s+',
        r'\bmy\s+',
    ]
    for pattern in first_person_patterns:
        if re.search(pattern, description, re.IGNORECASE):
            issues.append("Description should use third-person voice, not first-person")
            break

    # Check if it includes trigger terms
    if 'trigger' not in description.lower() and 'include' not in description.lower():
        issues.append("Description should explicitly mention trigger terms")

    return issues

def check_second_person_usage(body: str) -> List[Tuple[int, str]]:
    """Find second-person usage in skill body"""
    violations = []

    patterns = [
        r'\byou\s+should\b',
        r'\byou\s+can\b',
        r'\byou\s+need\s+to\b',
        r'\byou\s+have\s+to\b',
        r'\byou\s+must\b',
        r'\byou\s+will\b',
        r'\byour\b',
    ]

    lines = body.split('\n')
    for i, line in enumerate(lines, start=1):
        # Skip code blocks
        if line.strip().startswith('```') or line.strip().startswith('    '):
            continue

        for pattern in patterns:
            if re.search(pattern, line, re.IGNORECASE):
                violations.append((i, line.strip()))
                break

    return violations

def check_emoji_usage(content: str) -> List[Tuple[int, str]]:
    """Find emoji usage in skill content"""
    violations = []

    # Common emojis that should be replaced with ASCII
    # Using Unicode ranges to avoid encoding issues
    emoji_pattern = re.compile(
        r'[\U0001F300-\U0001F9FF'  # Miscellaneous Symbols and Pictographs, Supplemental
        r'\u2600-\u26FF'            # Miscellaneous Symbols
        r'\u2700-\u27BF'            # Dingbats
        r'\U0001F600-\U0001F64F'   # Emoticons
        r'\U0001F680-\U0001F6FF'   # Transport and Map
        r'\U0001F1E0-\U0001F1FF]'  # Regional Indicator Symbols
    )

    lines = content.split('\n')
    for i, line in enumerate(lines, start=1):
        if emoji_pattern.search(line):
            violations.append((i, line.strip()[:100]))  # Limit to 100 chars

    return violations

def analyze_skill(skill_path: Path) -> Dict:
    """Analyze skill structure and return findings"""
    results = {
        'valid': True,
        'critical_issues': [],
        'warnings': [],
        'suggestions': [],
    }

    # Check if SKILL.md exists
    skill_md = skill_path / 'SKILL.md'
    if not skill_md.exists():
        results['valid'] = False
        results['critical_issues'].append('SKILL.md not found')
        return results

    # Read SKILL.md
    content = skill_md.read_text(encoding='utf-8')

    # Parse frontmatter
    frontmatter, body = parse_frontmatter(content)

    if not frontmatter:
        results['valid'] = False
        results['critical_issues'].append('No YAML frontmatter found')
        return results

    # Check required fields
    if 'name' not in frontmatter:
        results['valid'] = False
        results['critical_issues'].append('Missing "name" field in frontmatter')
    else:
        name = frontmatter['name']
        name_issues = check_name_convention(name)
        if name_issues:
            results['valid'] = False
            results['critical_issues'].extend(name_issues)

    if 'description' not in frontmatter:
        results['valid'] = False
        results['critical_issues'].append('Missing "description" field in frontmatter')
    else:
        description = frontmatter['description']
        desc_issues = check_description(description)
        if desc_issues:
            for issue in desc_issues:
                if 'angle brackets' in issue or 'characters' in issue:
                    results['valid'] = False
                    results['critical_issues'].append(issue)
                else:
                    results['warnings'].append(issue)

    # Check for second-person usage
    second_person = check_second_person_usage(body)
    if second_person:
        results['warnings'].append(f"Found {len(second_person)} instances of second-person usage")
        results['second_person_violations'] = second_person[:5]  # First 5

    # Check for emoji usage (critical issue)
    emoji_violations = check_emoji_usage(content)
    if emoji_violations:
        results['valid'] = False
        results['critical_issues'].append(f"Found {len(emoji_violations)} emoji characters (must use ASCII alternatives)")
        results['emoji_violations'] = emoji_violations[:5]  # First 5

    # Check resource directories
    resources = {
        'scripts': skill_path / 'scripts',
        'references': skill_path / 'references',
        'assets': skill_path / 'assets',
    }

    mentioned_resources = {}
    for resource_type, resource_path in resources.items():
        pattern = f'{resource_type}/'
        if pattern in body:
            mentioned_resources[resource_type] = resource_path.exists()

    for resource_type, exists in mentioned_resources.items():
        if not exists:
            results['suggestions'].append(
                f"Skill mentions {resource_type}/ but directory doesn't exist"
            )

    return results

def main():
    parser = argparse.ArgumentParser(description='Analyze skill structure')
    parser.add_argument('--skill', required=True, help='Path to skill directory')
    args = parser.parse_args()

    skill_path = Path(args.skill)

    if not skill_path.exists():
        print(f"Error: Skill directory not found: {skill_path}")
        sys.exit(1)

    print(f"Analyzing skill: {skill_path}")
    print("=" * 60)

    results = analyze_skill(skill_path)

    # Print results
    if results['valid']:
        print("[PASS] Skill structure is valid!")
    else:
        print("[FAIL] Skill structure has critical issues")

    print()

    if results['critical_issues']:
        print("CRITICAL ISSUES:")
        for issue in results['critical_issues']:
            print(f"  [ERROR] {issue}")
        print()

    if results['warnings']:
        print("WARNINGS:")
        for warning in results['warnings']:
            print(f"  [WARN] {warning}")
        print()

    if 'second_person_violations' in results:
        print("SECOND-PERSON USAGE (first 5):")
        for line_num, line in results['second_person_violations']:
            print(f"  Line {line_num}: {line}")
        print()

    if 'emoji_violations' in results:
        print("EMOJI USAGE DETECTED (first 5):")
        print("  Emojis must be replaced with ASCII alternatives:")
        print("  [OK]/[PASS], [ERROR]/[FAIL], [WARN], [TIP], [INFO], [X]")
        for line_num, line in results['emoji_violations']:
            print(f"  Line {line_num}: {line}")
        print()

    if results['suggestions']:
        print("SUGGESTIONS:")
        for suggestion in results['suggestions']:
            print(f"  [TIP] {suggestion}")
        print()

    sys.exit(0 if results['valid'] else 1)

if __name__ == "__main__":
    main()
