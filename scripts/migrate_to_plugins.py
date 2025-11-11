#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Migrate skills to plugin marketplace format.

This script:
1. Preserves existing skills/ directory structure
2. Creates new plugins/ directory with plugin format
3. Generates plugin.json for each skill
4. Generates marketplace.json manifest
5. Maintains all existing resources
"""

import io
import sys
import os
import json
import shutil
import re
from pathlib import Path
from typing import Dict, List, Optional

# Configure stdout for UTF-8 encoding (prevents Windows encoding errors)
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def extract_frontmatter(skill_md_path: Path) -> Optional[Dict]:
    """Extract YAML frontmatter from SKILL.md file."""
    try:
        with open(skill_md_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract frontmatter between --- delimiters
        match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
        if not match:
            return None

        frontmatter_text = match.group(1)

        # Parse simple YAML (name and description)
        result = {}
        for line in frontmatter_text.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip()
                value = value.strip()

                # Handle multiline descriptions
                if key == 'description':
                    # Continue reading if line ends without quote
                    result[key] = value
                else:
                    result[key] = value

        return result
    except Exception as e:
        print(f"[WARNING] Failed to parse frontmatter from {skill_md_path}: {e}")
        return None

def find_all_skills(skills_dir: Path) -> List[Dict]:
    """Find all skills in the skills/ directory."""
    skills = []

    for category_dir in skills_dir.iterdir():
        if not category_dir.is_dir():
            continue

        for skill_dir in category_dir.iterdir():
            if not skill_dir.is_dir():
                continue

            skill_md = skill_dir / 'SKILL.md'
            if not skill_md.exists():
                continue

            frontmatter = extract_frontmatter(skill_md)
            if not frontmatter:
                print(f"[WARNING] Skipping {skill_dir.name} - invalid frontmatter")
                continue

            skills.append({
                'name': frontmatter.get('name', skill_dir.name),
                'description': frontmatter.get('description', ''),
                'category': category_dir.name,
                'source_path': skill_dir,
                'relative_path': skill_dir.relative_to(skills_dir.parent)
            })

    return skills

def create_plugin_structure(skill: Dict, plugins_dir: Path, author_info: Dict) -> bool:
    """Create plugin structure for a single skill."""
    plugin_name = skill['name']
    plugin_dir = plugins_dir / plugin_name

    print(f"Creating plugin: {plugin_name}")

    # Create plugin directories
    plugin_config_dir = plugin_dir / '.claude-plugin'
    plugin_skills_dir = plugin_dir / 'skills' / plugin_name

    plugin_config_dir.mkdir(parents=True, exist_ok=True)
    plugin_skills_dir.mkdir(parents=True, exist_ok=True)

    # Copy skill contents to plugin
    source_skill_dir = skill['source_path']

    # Copy all files and directories from skill to plugin/skills/skill-name/
    for item in source_skill_dir.iterdir():
        dest = plugin_skills_dir / item.name
        if item.is_dir():
            if dest.exists():
                shutil.rmtree(dest)
            shutil.copytree(item, dest)
        else:
            shutil.copy2(item, dest)

    # Generate plugin.json
    plugin_json = {
        "name": plugin_name,
        "description": skill['description'][:500] if len(skill['description']) > 500 else skill['description'],
        "version": "1.0.0",
        "author": author_info
    }

    plugin_json_path = plugin_config_dir / 'plugin.json'
    with open(plugin_json_path, 'w', encoding='utf-8') as f:
        json.dump(plugin_json, f, indent=2, ensure_ascii=False)

    print(f"  [OK] Created {plugin_name}")
    return True

def generate_marketplace_json(skills: List[Dict], marketplace_dir: Path, marketplace_info: Dict) -> bool:
    """Generate marketplace.json manifest."""
    plugins_list = []

    for skill in skills:
        plugin_entry = {
            "name": skill['name'],
            "source": f"./plugins/{skill['name']}",
            "description": skill['description'][:500] if len(skill['description']) > 500 else skill['description'],
            "version": "1.0.0",
            "author": marketplace_info['author'],
            "category": skill['category']
        }
        plugins_list.append(plugin_entry)

    marketplace_json = {
        "name": marketplace_info['name'],
        "owner": marketplace_info['owner'],
        "plugins": plugins_list
    }

    marketplace_config_dir = marketplace_dir / '.claude-plugin'
    marketplace_config_dir.mkdir(parents=True, exist_ok=True)

    marketplace_json_path = marketplace_config_dir / 'marketplace.json'
    with open(marketplace_json_path, 'w', encoding='utf-8') as f:
        json.dump(marketplace_json, f, indent=2, ensure_ascii=False)

    print(f"\n[OK] Generated marketplace.json with {len(plugins_list)} plugins")
    return True

def main():
    """Main migration function."""
    print("=" * 60)
    print("Claude Code Plugin Marketplace Migration")
    print("=" * 60)
    print()

    # Get repository root
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent
    skills_dir = repo_root / 'skills'
    plugins_dir = repo_root / 'plugins'

    if not skills_dir.exists():
        print("[ERROR] skills/ directory not found")
        sys.exit(1)

    # Configuration
    marketplace_info = {
        "name": "worldbuilding-app-skills",
        "owner": {
            "name": "Hope Overture",
            "email": "support@worldbuilding-app-skills.dev"
        },
        "author": {
            "name": "Hope Overture",
            "email": "support@worldbuilding-app-skills.dev"
        }
    }

    # Find all skills
    print("Scanning for skills...")
    skills = find_all_skills(skills_dir)
    print(f"Found {len(skills)} skills across categories\n")

    if len(skills) == 0:
        print("[ERROR] No skills found")
        sys.exit(1)

    # Create plugins directory
    if plugins_dir.exists():
        print(f"[INFO] plugins/ directory exists, contents will be overwritten")
        response = input("Continue? (y/n): ").lower()
        if response != 'y':
            print("Migration cancelled")
            sys.exit(0)

    plugins_dir.mkdir(exist_ok=True)

    # Create plugin for each skill
    print("\nCreating plugins...")
    print("-" * 60)
    successful = 0
    failed = 0

    for skill in skills:
        try:
            if create_plugin_structure(skill, plugins_dir, marketplace_info['author']):
                successful += 1
            else:
                failed += 1
        except Exception as e:
            print(f"  [ERROR] Failed to create plugin for {skill['name']}: {e}")
            failed += 1

    print("-" * 60)
    print(f"Plugins created: {successful} successful, {failed} failed\n")

    # Generate marketplace.json
    print("Generating marketplace.json...")
    if generate_marketplace_json(skills, repo_root, marketplace_info):
        print("[OK] Marketplace manifest created")
    else:
        print("[ERROR] Failed to create marketplace manifest")
        sys.exit(1)

    # Summary
    print("\n" + "=" * 60)
    print("Migration Complete!")
    print("=" * 60)
    print()
    print("Structure created:")
    print(f"  - plugins/ directory with {successful} plugins")
    print(f"  - .claude-plugin/marketplace.json manifest")
    print()
    print("Original skills/ directory preserved unchanged")
    print()
    print("Next steps:")
    print("  1. Review generated files")
    print("  2. Customize marketplace.json owner info if needed")
    print("  3. Commit and push to GitHub")
    print("  4. Users can add marketplace:")
    print("     /plugin marketplace add hopeoverture/worldbuilding-app-skills")
    print()
    print("Plugin installation example:")
    print("  /plugin install nextjs-fullstack-scaffold@worldbuilding-app-skills")
    print()

if __name__ == '__main__':
    main()
