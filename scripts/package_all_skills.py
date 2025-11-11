#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Package All Skills - Batch packages all skills in the repository

Usage:
    python scripts/package_all_skills.py [output-directory]

Example:
    python scripts/package_all_skills.py
    python scripts/package_all_skills.py ./dist
"""

import sys
from pathlib import Path
from package_skill import package_skill


def find_all_skills(skills_dir="skills"):
    """Find all skill directories containing SKILL.md files."""
    skills_path = Path(skills_dir)
    if not skills_path.exists():
        return []

    skill_folders = []
    for skill_md in skills_path.rglob("SKILL.md"):
        skill_folders.append(skill_md.parent)

    return sorted(skill_folders)


def main():
    output_dir = sys.argv[1] if len(sys.argv) > 1 else "./dist"

    print("=" * 60)
    print("PACKAGING ALL SKILLS")
    print("=" * 60)
    print(f"Output directory: {output_dir}\n")

    skills = find_all_skills()

    if not skills:
        print("[ERROR] No skills found in the repository")
        sys.exit(1)

    print(f"Found {len(skills)} skills to package\n")

    successful = []
    failed = []

    for i, skill_path in enumerate(skills, 1):
        category = skill_path.parent.name
        skill_name = skill_path.name

        print(f"\n[{i}/{len(skills)}] Packaging {category}/{skill_name}")
        print("-" * 60)

        result = package_skill(skill_path, output_dir)

        if result:
            successful.append(f"{category}/{skill_name}")
        else:
            failed.append(f"{category}/{skill_name}")

    # Summary
    print("\n" + "=" * 60)
    print("PACKAGING SUMMARY")
    print("=" * 60)
    print(f"Total skills: {len(skills)}")
    print(f"Successful: {len(successful)}")
    print(f"Failed: {len(failed)}")

    if failed:
        print("\n[WARN] Failed to package:")
        for skill in failed:
            print(f"  - {skill}")
        sys.exit(1)
    else:
        print("\n[OK] All skills packaged successfully!")
        sys.exit(0)


if __name__ == "__main__":
    main()
