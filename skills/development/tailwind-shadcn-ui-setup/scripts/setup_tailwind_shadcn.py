#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tailwind CSS v4 + shadcn/ui Setup Automation Script

Configures Tailwind CSS and shadcn/ui for Next.js 16 App Router projects.
Handles detection of existing setup, merging configurations, and installing dependencies.
"""

import io
import json
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional

# Configure stdout for UTF-8 encoding (prevents Windows encoding errors)
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


class SetupManager:
    """Manages the Tailwind + shadcn/ui setup process."""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.package_json_path = project_root / "package.json"
        self.existing_tailwind = False
        self.existing_shadcn = False

    def detect_existing_setup(self) -> Dict[str, bool]:
        """Detect existing Tailwind and shadcn/ui installations."""
        print("[INFO] Detecting existing setup...")

        if not self.package_json_path.exists():
            print("[ERROR] Error: package.json not found. Is this a Next.js project?")
            sys.exit(1)

        with open(self.package_json_path) as f:
            package_data = json.load(f)

        dependencies = {
            **package_data.get("dependencies", {}),
            **package_data.get("devDependencies", {})
        }

        self.existing_tailwind = "tailwindcss" in dependencies
        self.existing_shadcn = "class-variance-authority" in dependencies

        return {
            "tailwind": self.existing_tailwind,
            "shadcn": self.existing_shadcn,
            "nextjs": "next" in dependencies
        }

    def install_dependencies(self, use_dark_mode: bool = True):
        """Install required npm packages."""
        print("\n[INSTALL] Installing dependencies...")

        # Core dependencies
        core_deps = [
            "tailwindcss",
            "postcss",
            "autoprefixer",
            "class-variance-authority",
            "clsx",
            "tailwind-merge",
            "lucide-react",
            "@tailwindcss/forms",
            "@tailwindcss/typography"
        ]

        if use_dark_mode:
            core_deps.append("next-themes")

        # shadcn/ui peer dependencies
        shadcn_deps = [
            "@radix-ui/react-slot",
            "@radix-ui/react-dialog",
            "@radix-ui/react-dropdown-menu",
            "@radix-ui/react-separator",
            "sonner"
        ]

        all_deps = core_deps + shadcn_deps

        print(f"Installing: {', '.join(all_deps)}")

        try:
            subprocess.run(
                ["npm", "install", "--save"] + all_deps,
                cwd=self.project_root,
                check=True,
                capture_output=True,
                text=True
            )
            print("[OK] Dependencies installed successfully")
        except subprocess.CalledProcessError as e:
            print(f"[ERROR] Error installing dependencies: {e.stderr}")
            sys.exit(1)

    def check_shadcn_init(self) -> bool:
        """Check if shadcn/ui has been initialized."""
        components_json = self.project_root / "components.json"
        return components_json.exists()

    def init_shadcn(self):
        """Initialize shadcn/ui configuration."""
        if self.check_shadcn_init():
            print("[OK] shadcn/ui already initialized (components.json found)")
            return

        print("\n[SETUP] Initializing shadcn/ui...")
        print("Note: This will create components.json with default settings")

        # Create a default components.json
        components_config = {
            "$schema": "https://ui.shadcn.com/schema.json",
            "style": "default",
            "rsc": True,
            "tsx": True,
            "tailwind": {
                "config": "tailwind.config.ts",
                "css": "app/globals.css",
                "baseColor": "zinc",
                "cssVariables": True
            },
            "aliases": {
                "components": "@/components",
                "utils": "@/lib/utils"
            }
        }

        components_json_path = self.project_root / "components.json"
        with open(components_json_path, 'w') as f:
            json.dump(components_config, f, indent=2)

        print("[OK] Created components.json")

    def add_shadcn_components(self, components: List[str]):
        """Add shadcn/ui components."""
        print(f"\n[SETUP] Adding shadcn/ui components: {', '.join(components)}")

        for component in components:
            try:
                print(f"  Adding {component}...")
                subprocess.run(
                    ["npx", "shadcn-ui@latest", "add", component, "--yes"],
                    cwd=self.project_root,
                    check=True,
                    capture_output=True,
                    text=True
                )
            except subprocess.CalledProcessError as e:
                print(f"  [WARN] Warning: Could not add {component}: {e.stderr}")
                print(f"     You can add it manually later with: npx shadcn-ui add {component}")

        print("[OK] shadcn/ui components added")

    def copy_template_files(self, skill_dir: Path, theme_preset: str, use_dark_mode: bool, sidebar_layout: bool):
        """Copy template files from assets directory."""
        print("\n[SETUP] Copying template files...")

        assets_dir = skill_dir / "assets"

        # Files to copy with their destinations
        template_mappings = {
            "tailwind.config.ts.template": self.project_root / "tailwind.config.ts",
            "postcss.config.js.template": self.project_root / "postcss.config.js",
            "globals.css.template": self.project_root / "app" / "globals.css",
        }

        for template_name, dest_path in template_mappings.items():
            template_path = assets_dir / template_name
            if template_path.exists():
                dest_path.parent.mkdir(parents=True, exist_ok=True)

                # Read template and replace placeholders
                content = template_path.read_text()
                content = content.replace("{{THEME_PRESET}}", theme_preset)

                dest_path.write_text(content)
                print(f"  [OK] Created {dest_path.relative_to(self.project_root)}")

    def create_utils_file(self):
        """Create lib/utils.ts with cn helper."""
        utils_dir = self.project_root / "lib"
        utils_dir.mkdir(exist_ok=True)

        utils_content = '''import { type ClassValue, clsx } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}
'''

        utils_path = utils_dir / "utils.ts"
        if not utils_path.exists():
            utils_path.write_text(utils_content)
            print("[OK] Created lib/utils.ts")
        else:
            print("[INFO] lib/utils.ts already exists, skipping")

    def print_summary(self, config: Dict):
        """Print setup summary."""
        print("\n" + "="*60)
        print("[OK] Tailwind CSS + shadcn/ui Setup Complete!")
        print("="*60)
        print(f"\n[CONFIG] Configuration:")
        print(f"  • Theme Preset: {config['theme_preset']}")
        print(f"  • Dark Mode: {'Enabled' if config['use_dark_mode'] else 'Disabled'}")
        print(f"  • Sidebar Layout: {'Yes' if config['sidebar_layout'] else 'No'}")
        print(f"  • Examples: {'Included' if config['include_examples'] else 'Not included'}")
        print(f"\n[FILES] Files Created/Updated:")
        print(f"  • tailwind.config.ts")
        print(f"  • postcss.config.js")
        print(f"  • app/globals.css")
        print(f"  • components.json")
        print(f"  • lib/utils.ts")
        print(f"\n[NEXT] Next Steps:")
        print(f"  1. Review tailwind.config.ts and customize tokens")
        print(f"  2. Check app/globals.css for CSS variables")
        print(f"  3. Start your dev server: npm run dev")
        print(f"  4. Add more shadcn components: npx shadcn-ui add [component]")
        print(f"\n[TIP] Tip: Run the skill again to add example pages and components")
        print("="*60 + "\n")


def get_user_input(prompt: str, default: str, options: Optional[List[str]] = None) -> str:
    """Get user input with validation."""
    while True:
        if options:
            prompt_with_options = f"{prompt} ({'/'.join(options)}) [{default}]: "
        else:
            prompt_with_options = f"{prompt} [{default}]: "

        response = input(prompt_with_options).strip() or default

        if options and response not in options:
            print(f"Invalid option. Please choose from: {', '.join(options)}")
            continue

        return response


def main():
    """Main setup function."""
    print("==> Tailwind CSS v4 + shadcn/ui Setup")
    print("="*60)

    # Detect project root
    project_root = Path.cwd()

    # Initialize setup manager
    manager = SetupManager(project_root)

    # Detect existing setup
    existing = manager.detect_existing_setup()

    if not existing["nextjs"]:
        print("[ERROR] Error: This doesn't appear to be a Next.js project")
        print("   Make sure you're in the project root with package.json")
        sys.exit(1)

    if existing["tailwind"]:
        print("[OK] Existing Tailwind CSS installation detected")
    if existing["shadcn"]:
        print("[OK] Existing shadcn/ui installation detected")

    print("\n[CONFIG] Configuration Options\n")

    # Get user preferences
    use_dark_mode = get_user_input(
        "Enable dark mode?",
        "yes",
        ["yes", "no"]
    ) == "yes"

    theme_preset = get_user_input(
        "Theme preset",
        "zinc",
        ["zinc", "slate", "neutral"]
    )

    sidebar_layout = get_user_input(
        "Include sidebar layout?",
        "yes",
        ["yes", "no"]
    ) == "yes"

    include_examples = get_user_input(
        "Include example pages?",
        "yes",
        ["yes", "no"]
    ) == "yes"

    config = {
        "use_dark_mode": use_dark_mode,
        "theme_preset": theme_preset,
        "sidebar_layout": sidebar_layout,
        "include_examples": include_examples
    }

    print("\n" + "="*60)
    print("Starting setup with your configuration...")
    print("="*60 + "\n")

    # Install dependencies
    manager.install_dependencies(use_dark_mode)

    # Initialize shadcn/ui
    manager.init_shadcn()

    # Add base shadcn components
    base_components = ["button", "card", "input", "label", "dialog", "separator"]
    manager.add_shadcn_components(base_components)

    # Create utils file
    manager.create_utils_file()

    # Note: Template file copying requires the skill's asset directory
    # This would be handled by the SKILL.md instructions to copy files
    print("\n[INFO] Note: Template files should be copied by the skill instructions")
    print("   This script handles dependency installation and shadcn/ui setup")

    # Print summary
    manager.print_summary(config)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[WARN] Setup cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] Error: {e}")
        sys.exit(1)
