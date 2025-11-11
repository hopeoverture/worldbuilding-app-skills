#!/usr/bin/env python3
"""
Generate GitHub Actions CI/CD workflow files based on project configuration.
"""

import json
import os
import sys
from pathlib import Path


def detect_package_manager(project_root):
    """Detect package manager from lock files."""
    if (project_root / "pnpm-lock.yaml").exists():
        return "pnpm"
    elif (project_root / "yarn.lock").exists():
        return "yarn"
    elif (project_root / "package-lock.json").exists():
        return "npm"
    return "npm"


def detect_framework(package_json):
    """Detect framework from package.json dependencies."""
    deps = {**package_json.get("dependencies", {}), **package_json.get("devDependencies", {})}

    if "next" in deps:
        return "nextjs"
    elif "vite" in deps:
        return "vite"
    elif "react-scripts" in deps:
        return "cra"
    elif "vue" in deps:
        return "vue"
    return "generic"


def detect_test_runner(package_json):
    """Detect test runner from package.json."""
    deps = {**package_json.get("dependencies", {}), **package_json.get("devDependencies", {})}

    if "vitest" in deps:
        return "vitest"
    elif "@playwright/test" in deps:
        return "playwright"
    elif "jest" in deps:
        return "jest"
    return None


def generate_ci_workflow(config):
    """Generate CI workflow YAML content."""
    pm = config["package_manager"]
    install_cmd = {
        "npm": "npm ci",
        "yarn": "yarn install --frozen-lockfile",
        "pnpm": "pnpm install --frozen-lockfile"
    }[pm]

    cache_path = {
        "npm": "~/.npm",
        "yarn": "~/.yarn/cache",
        "pnpm": "~/.pnpm-store"
    }[pm]

    lock_file = {
        "npm": "package-lock.json",
        "yarn": "yarn.lock",
        "pnpm": "pnpm-lock.yaml"
    }[pm]

    test_cmd = config.get("test_command", "npm test")
    build_cmd = config.get("build_command", "npm run build")

    workflow = f"""name: CI

on:
  push:
    branches: [main, master]
  pull_request:
    branches: [main, master]

jobs:
  lint:
    name: Lint
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: '{pm}'

      - name: Install dependencies
        run: {install_cmd}

      - name: Run linter
        run: npm run lint

      - name: Check formatting
        run: npm run format:check
        continue-on-error: true

      - name: Type check
        run: npm run type-check
        continue-on-error: true

  test:
    name: Test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: '{pm}'

      - name: Install dependencies
        run: {install_cmd}

      - name: Run tests
        run: {test_cmd}

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        if: always()
        with:
          files: ./coverage/coverage-final.json
          fail_ci_if_error: false

  build:
    name: Build
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: '{pm}'

      - name: Install dependencies
        run: {install_cmd}

      - name: Cache Next.js build
        uses: actions/cache@v3
        if: contains('{config["framework"]}', 'next')
        with:
          path: |
            .next/cache
          key: ${{{{ runner.os }}}}-nextjs-${{{{ hashFiles('{lock_file}') }}}}-${{{{ hashFiles('**/*.js', '**/*.jsx', '**/*.ts', '**/*.tsx') }}}}
          restore-keys: |
            ${{{{ runner.os }}}}-nextjs-${{{{ hashFiles('{lock_file}') }}}}-

      - name: Build application
        run: {build_cmd}
        env:
          NEXT_TELEMETRY_DISABLED: 1

      - name: Upload build artifacts
        uses: actions/upload-artifact@v3
        with:
          name: build
          path: |
            .next
            out
            dist
            build
          retention-days: 7
"""

    return workflow


def generate_preview_workflow(config):
    """Generate preview deployment workflow."""
    pm = config["package_manager"]
    install_cmd = {
        "npm": "npm ci",
        "yarn": "yarn install --frozen-lockfile",
        "pnpm": "pnpm install --frozen-lockfile"
    }[pm]

    workflow = f"""name: Preview Deployment

on:
  pull_request:
    types: [opened, synchronize, reopened, closed]

jobs:
  preview:
    name: Deploy Preview
    runs-on: ubuntu-latest
    if: github.event.action != 'closed'
    permissions:
      pull-requests: write
      contents: read
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: '{pm}'

      - name: Install dependencies
        run: {install_cmd}

      - name: Build for preview
        run: npm run build
        env:
          NEXT_TELEMETRY_DISABLED: 1

      - name: Deploy to Vercel
        id: deploy
        run: |
          npx vercel --token ${{{{ secrets.VERCEL_TOKEN }}}} --yes --env ENVIRONMENT=preview > deployment-url.txt
          echo "url=$(cat deployment-url.txt)" >> $GITHUB_OUTPUT

      - name: Comment preview URL
        uses: actions/github-script@v7
        with:
          script: |
            const url = '${{{{ steps.deploy.outputs.url }}}}';
            const comment = `## Preview Deployment

            :rocket: Your preview deployment is ready!

            **URL**: ${{url}}

            Built from commit: ${{{{ github.event.pull_request.head.sha }}}}`;

            github.rest.issues.createComment({{
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: comment
            }});

  cleanup:
    name: Cleanup Preview
    runs-on: ubuntu-latest
    if: github.event.action == 'closed'
    steps:
      - name: Delete preview deployment
        run: |
          echo "Cleaning up preview deployment for PR #${{{{ github.event.pull_request.number }}}}"
          # Add cleanup logic for your deployment provider
"""

    return workflow


def generate_deploy_workflow(config):
    """Generate production deployment workflow."""
    workflow = """name: Deploy Production

on:
  push:
    branches: [main, master]

jobs:
  deploy:
    name: Deploy to Production
    runs-on: ubuntu-latest
    environment:
      name: production
      url: https://your-app-url.com
    steps:
      - uses: actions/checkout@v4

      - name: Download build artifacts
        uses: actions/download-artifact@v3
        with:
          name: build

      - name: Deploy to production
        run: |
          echo "Add your deployment commands here"
          # Example: npx vercel --prod --token ${{ secrets.VERCEL_TOKEN }}

      - name: Notify on success
        if: success()
        run: |
          echo "Deployment successful"
          # Add notification logic (Slack, Discord, etc.)

      - name: Notify on failure
        if: failure()
        run: |
          echo "Deployment failed"
          # Add failure notification logic
"""

    return workflow


def main():
    if len(sys.argv) < 2:
        print("Usage: generate_ci_workflow.py <project_root>")
        sys.exit(1)

    project_root = Path(sys.argv[1]).resolve()

    if not project_root.exists():
        print(f"Error: Project root not found: {project_root}")
        sys.exit(1)

    # Read package.json
    package_json_path = project_root / "package.json"
    if not package_json_path.exists():
        print("Error: package.json not found")
        sys.exit(1)

    with open(package_json_path) as f:
        package_json = json.load(f)

    # Detect configuration
    config = {
        "package_manager": detect_package_manager(project_root),
        "framework": detect_framework(package_json),
        "test_runner": detect_test_runner(package_json),
        "test_command": package_json.get("scripts", {}).get("test", "npm test"),
        "build_command": package_json.get("scripts", {}).get("build", "npm run build"),
    }

    print(f"Detected configuration:")
    print(f"  Package manager: {config['package_manager']}")
    print(f"  Framework: {config['framework']}")
    print(f"  Test runner: {config['test_runner']}")
    print()

    # Create workflows directory
    workflows_dir = project_root / ".github" / "workflows"
    workflows_dir.mkdir(parents=True, exist_ok=True)

    # Generate workflow files
    workflows = {
        "ci.yml": generate_ci_workflow(config),
        "preview.yml": generate_preview_workflow(config),
        "deploy.yml": generate_deploy_workflow(config),
    }

    for filename, content in workflows.items():
        filepath = workflows_dir / filename
        with open(filepath, "w") as f:
            f.write(content)
        print(f"Created: {filepath}")

    print()
    print("GitHub Actions workflows generated successfully!")
    print()
    print("Next steps:")
    print("1. Review and customize the generated workflow files")
    print("2. Add required secrets to your GitHub repository settings")
    print("3. Commit and push the workflows to trigger CI/CD")


if __name__ == "__main__":
    main()
