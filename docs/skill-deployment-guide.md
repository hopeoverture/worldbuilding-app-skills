# Skill Deployment Guide

Complete guide for importing and deploying Claude Code skills from this repository into your projects.

## Table of Contents

- [Understanding Skill Types](#understanding-skill-types)
- [Pre-Deployment Checklist](#pre-deployment-checklist)
- [Deployment Methods](#deployment-methods)
- [Verification and Testing](#verification-and-testing)
- [Troubleshooting](#troubleshooting)
- [Best Practices](#best-practices)

## Understanding Skill Types

### Personal Skills

**Location:** `~/.claude/skills/`

**Scope:** Available across all projects on your machine

**Use Cases:**
- Individual workflow automation
- Personal productivity tools
- Experimental capabilities you want to try
- Skills you use frequently across multiple projects

**Pros:**
- One-time setup works everywhere
- No git commits required
- Private to your machine

**Cons:**
- Not shared with team
- Must be installed on each machine separately
- Can't be version controlled with project

### Project Skills

**Location:** `.claude/skills/` (in project root)

**Scope:** Available only within the specific project

**Use Cases:**
- Team-wide workflows
- Project-specific expertise
- Shared utilities and conventions
- Tools tied to project tech stack

**Pros:**
- Automatically shared via git
- Version controlled with project
- Team members get updates automatically
- Project-specific context

**Cons:**
- Must be added to each project
- Takes up space in project repository

## Pre-Deployment Checklist

Before deploying skills, verify they are ready:

### 1. Validate Skill Structure

```bash
python scripts/quick_validate.py skills/category/skill-name
```

Expected output: `[OK] Skill is valid!`

### 2. Check File Requirements

Verify each skill has:
- `SKILL.md` file in skill directory
- Valid YAML frontmatter (name and description)
- Lowercase hyphenated name (max 64 characters)
- Description under 1,024 characters
- No emoji characters (ASCII only)

### 3. Review Skill Description

Ensure description includes:
- Clear explanation of WHAT the skill does
- Specific WHEN to use it (trigger terms)
- Concrete examples of activation phrases
- Third-person voice ("This skill..." not "You...")

Example of good description:
```yaml
description: Generate Zod validation schemas and TypeScript types from entity definitions.
  Use when creating API contracts, form validation, or data models. Trigger terms include
  "generate schema", "create validation", "Zod types", or "API contract".
```

### 4. Test File Integrity

Check packaged skills:
```bash
# Verify zip file exists and is not corrupted
unzip -t dist/skill-name.zip

# Preview contents
unzip -l dist/skill-name.zip
```

## Deployment Methods

### Method 1: Deploy Single Skill to Project (Recommended for Teams)

**Use when:** Sharing specific skills with your team via git

```bash
# From this repository root
cd worldbuilding-app-skills

# Create target directory in your project
mkdir -p /path/to/your-project/.claude/skills

# Copy skill directory
cp -r skills/category/skill-name /path/to/your-project/.claude/skills/

# Navigate to your project
cd /path/to/your-project

# Commit to version control
git add .claude/skills/skill-name
git commit -m "Add skill-name skill for [purpose]"
git push
```

**Team members:** Pull changes and skills are automatically available

### Method 2: Deploy from Packaged Zip

**Use when:** Receiving skills from distribution or downloading from releases

```bash
# Option A: Deploy to project
cd /path/to/your-project
mkdir -p .claude/skills
cd .claude/skills
unzip /path/to/skill-name.zip

# Option B: Deploy to personal skills
cd ~/.claude/skills
unzip /path/to/skill-name.zip

# Verify extraction
ls -la skill-name/SKILL.md
```

### Method 3: Deploy Multiple Skills at Once

**Use when:** Setting up a new project with multiple required skills

```bash
# Deploy specific category
cp -r skills/development/* /path/to/your-project/.claude/skills/

# Deploy selected skills
for skill in api-contracts-and-zod-validation \
             supabase-auth-ssr-setup \
             tailwind-shadcn-ui-setup; do
  cp -r skills/development/$skill /path/to/your-project/.claude/skills/
done

# Deploy all skills (careful - 26 skills)
mkdir -p /path/to/your-project/.claude/skills
find skills -name "SKILL.md" -exec dirname {} \; | while read skill_path; do
  skill_name=$(basename "$skill_path")
  cp -r "$skill_path" /path/to/your-project/.claude/skills/
done
```

### Method 4: Deploy to Personal Skills (Cross-Project)

**Use when:** Want skills available in all your projects

```bash
# Create personal skills directory if needed
mkdir -p ~/.claude/skills

# Copy skill
cp -r skills/category/skill-name ~/.claude/skills/

# Or from packaged zip
cd ~/.claude/skills
unzip /path/to/worldbuilding-app-skills/dist/skill-name.zip

# Verify
ls ~/.claude/skills/skill-name/SKILL.md
```

### Method 5: Selective Project Setup

**Use when:** Starting a new worldbuilding project and want core skills

Example setup for Next.js worldbuilding app:

```bash
PROJECT_DIR="/path/to/new-worldbuilding-app"
SKILLS_SOURCE="./skills"

mkdir -p "$PROJECT_DIR/.claude/skills"

# Core development setup
cp -r "$SKILLS_SOURCE/development/nextjs-fullstack-scaffold" \
      "$PROJECT_DIR/.claude/skills/"
cp -r "$SKILLS_SOURCE/development/tailwind-shadcn-ui-setup" \
      "$PROJECT_DIR/.claude/skills/"
cp -r "$SKILLS_SOURCE/development/eslint-prettier-husky-config" \
      "$PROJECT_DIR/.claude/skills/"

# Authentication & database
cp -r "$SKILLS_SOURCE/development/supabase-auth-ssr-setup" \
      "$PROJECT_DIR/.claude/skills/"
cp -r "$SKILLS_SOURCE/development/supabase-prisma-database-management" \
      "$PROJECT_DIR/.claude/skills/"
cp -r "$SKILLS_SOURCE/development/supabase-rls-policy-generator" \
      "$PROJECT_DIR/.claude/skills/"

# Data validation
cp -r "$SKILLS_SOURCE/development/api-contracts-and-zod-validation" \
      "$PROJECT_DIR/.claude/skills/"
cp -r "$SKILLS_SOURCE/ui-components/form-generator-rhf-zod" \
      "$PROJECT_DIR/.claude/skills/"

# Testing
cp -r "$SKILLS_SOURCE/testing/testing-next-stack" \
      "$PROJECT_DIR/.claude/skills/"

# Security
cp -r "$SKILLS_SOURCE/development/security-hardening-checklist" \
      "$PROJECT_DIR/.claude/skills/"
cp -r "$SKILLS_SOURCE/development/env-config-validator" \
      "$PROJECT_DIR/.claude/skills/"

echo "Core skills deployed to $PROJECT_DIR"
```

## Verification and Testing

### Step 1: Verify File Structure

```bash
# Check skill exists in correct location
# For project skills:
ls .claude/skills/skill-name/SKILL.md

# For personal skills:
ls ~/.claude/skills/skill-name/SKILL.md
```

Expected: Path should exist and display the SKILL.md file

### Step 2: Validate YAML Frontmatter

```bash
# Check first 10 lines for proper YAML
head -n 10 .claude/skills/skill-name/SKILL.md
```

Verify:
- Line 1: `---` (opening delimiter)
- Line 2+: `name:` and `description:` fields
- Closing `---` before Markdown content starts
- Proper indentation (spaces, not tabs)
- No emoji characters

### Step 3: Test Skill Discovery

Start Claude Code and ask:

```
What skills are available?
```

or

```
List all skills in this project.
```

Expected: Your skill should appear in the list with its name and description

### Step 4: Test Skill Activation

Ask a question that matches the skill's description trigger terms.

Example for `api-contracts-and-zod-validation`:
```
Can you help me generate a Zod schema for a user entity?
```

Expected: Claude should recognize and activate the skill automatically

### Step 5: Verify Tool Restrictions (if applicable)

For skills with `allowed-tools` configuration:

```bash
# Check frontmatter includes allowed-tools
grep -A 5 "allowed-tools:" .claude/skills/skill-name/SKILL.md
```

Test that restricted skills only use specified tools without permission prompts.

## Troubleshooting

### Issue: Claude Doesn't See the Skill

**Symptoms:** Skill doesn't appear in skill list, never gets activated

**Solutions:**

1. **Check file path**
   ```bash
   # Verify exact location
   ls -la .claude/skills/skill-name/SKILL.md
   # or
   ls -la ~/.claude/skills/skill-name/SKILL.md
   ```

2. **Verify directory name**
   - Must be lowercase letters, numbers, and hyphens only
   - No spaces, underscores, or special characters
   - Max 64 characters

3. **Check SKILL.md exists**
   - File must be named exactly `SKILL.md` (case-sensitive)
   - Must be in the skill directory root

4. **Restart Claude Code**
   - Skills are loaded at startup
   - Exit and restart Claude Code after adding skills

### Issue: Skill Never Activates

**Symptoms:** Skill appears in list but Claude doesn't use it

**Solutions:**

1. **Improve description specificity**

   Bad:
   ```yaml
   description: Helps with data validation
   ```

   Good:
   ```yaml
   description: Generate Zod validation schemas from TypeScript types and entity
     definitions. Use when creating form validation, API request/response contracts,
     or data models. Trigger terms include "Zod schema", "validation", "type safety",
     "API contract", "form schema".
   ```

2. **Add concrete trigger terms**
   - Include exact phrases users would say
   - Add technology names (Zod, Prisma, React, etc.)
   - Include action verbs (generate, create, validate, check)
   - Mention file types or contexts (API, form, database)

3. **Test with exact trigger terms**
   - Use phrases from your description
   - Be explicit: "Use the [skill-name] skill to..."

### Issue: YAML Parsing Errors

**Symptoms:** Skill doesn't load, Claude reports syntax errors

**Solutions:**

1. **Check delimiters**
   ```yaml
   ---
   name: skill-name
   description: Description text here
   ---

   # Rest of content
   ```

2. **Validate indentation**
   - Use spaces, not tabs
   - Consistent indentation (2 or 4 spaces)
   - No trailing spaces

3. **Check for special characters**
   - No emoji characters (use ASCII alternatives)
   - Quote strings with special characters:
     ```yaml
     description: "Text with: colons or other special chars"
     ```

4. **Use online YAML validator**
   - Copy frontmatter to https://www.yamllint.com/
   - Fix any reported errors

### Issue: Scripts Don't Execute

**Symptoms:** Skill activates but scripts fail to run

**Solutions:**

1. **Check execute permissions**
   ```bash
   chmod +x .claude/skills/skill-name/scripts/*.py
   chmod +x .claude/skills/skill-name/scripts/*.sh
   ```

2. **Verify Python shebang**
   ```python
   #!/usr/bin/env python3
   # -*- coding: utf-8 -*-
   ```

3. **Check script paths**
   - Use forward slashes: `scripts/helper.py`
   - Reference from skill root directory

4. **Test scripts independently**
   ```bash
   cd .claude/skills/skill-name
   python scripts/script_name.py --test
   ```

### Issue: Multiple Similar Skills Conflict

**Symptoms:** Wrong skill activates for a task

**Solutions:**

1. **Use distinct terminology**
   - Differentiate trigger terms between skills
   - Example: "Excel spreadsheets" vs "CSV data files"

2. **Make descriptions more specific**
   - Narrow the scope of each skill
   - Include explicit exclusions if needed

3. **Manually specify skill**
   ```
   Use the [exact-skill-name] skill to [task]
   ```

### Issue: Skill Works Locally But Not for Team

**Symptoms:** Skill works on your machine but teammates can't use it

**Solutions:**

1. **Verify committed to git**
   ```bash
   git status .claude/skills/
   git log --oneline -- .claude/skills/skill-name
   ```

2. **Check .gitignore**
   ```bash
   # Ensure .claude/skills/ is not ignored
   grep -r "\.claude" .gitignore
   ```

3. **Confirm teammates pulled changes**
   ```bash
   git pull origin main
   ls .claude/skills/skill-name/SKILL.md
   ```

4. **Check for local dependencies**
   - Document required tools in skill description
   - Include installation instructions in SKILL.md

### Issue: Windows Encoding Errors

**Symptoms:** Errors about character encoding, especially with packaged skills

**Solutions:**

1. **Avoid emoji characters**
   - Use ASCII alternatives: `[OK]`, `[ERROR]`, `[INFO]`
   - No Unicode decorative characters

2. **Use UTF-8 encoding**
   - Ensure text editors save as UTF-8
   - Add UTF-8 BOM if needed on Windows

3. **Check Python scripts**
   - Include encoding header:
     ```python
     # -*- coding: utf-8 -*-
     ```
   - Configure stdout for Windows:
     ```python
     import io
     import sys
     if sys.platform == 'win32':
         sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
     ```

## Best Practices

### Project Setup Strategy

**1. Start Minimal**
- Deploy only skills you'll immediately use
- Add more skills as needs arise
- Avoid deploying all 26 skills unless necessary

**2. Organize by Project Phase**

*Phase 1 - Initial Setup (3-5 skills):*
- nextjs-fullstack-scaffold
- tailwind-shadcn-ui-setup
- eslint-prettier-husky-config

*Phase 2 - Core Features (5-7 skills):*
- supabase-auth-ssr-setup
- supabase-prisma-database-management
- api-contracts-and-zod-validation
- form-generator-rhf-zod

*Phase 3 - Production Ready (3-5 skills):*
- security-hardening-checklist
- sentry-and-otel-setup
- testing-next-stack
- github-actions-ci-workflow

**3. Team Coordination**
- Communicate when adding new skills
- Document which skills are used in project README
- Review skills during onboarding

### Maintenance

**Keep Skills Updated**
```bash
# In your project
cd /path/to/your-project

# Update from source repository
cp -r /path/to/worldbuilding-app-skills/skills/category/skill-name \
      .claude/skills/

# Commit changes
git add .claude/skills/skill-name
git commit -m "Update skill-name to latest version"
```

**Remove Unused Skills**
```bash
# Clean up skills you don't use
rm -rf .claude/skills/unused-skill-name

git rm -r .claude/skills/unused-skill-name
git commit -m "Remove unused skill"
```

**Document Your Skills**

Create `.claude/skills/README.md` in your project:
```markdown
# Project Skills

This project uses the following Claude Code skills:

## Core Development
- **nextjs-fullstack-scaffold**: Initialize Next.js app structure
- **tailwind-shadcn-ui-setup**: UI framework configuration

## Authentication
- **supabase-auth-ssr-setup**: Supabase SSR authentication

## Documentation
See: https://github.com/your-org/worldbuilding-app-skills
```

### Security Considerations

**Review Before Deploying**
- Read SKILL.md content
- Check scripts for security issues
- Verify allowed-tools restrictions
- Review file access patterns

**Use Tool Restrictions**
- For analysis-only skills, use `allowed-tools: Read, Grep, Glob, Bash`
- Prevent unintended modifications
- Reduce permission prompts

**Avoid Sensitive Data**
- Don't include API keys in skills
- Don't hardcode credentials
- Use environment variables instead
- Document required ENV vars in SKILL.md

### Performance Tips

**Reduce Context Size**
- Use `references/` for large documentation
- Move templates to `assets/` directory
- Keep SKILL.md under 5,000 words
- Include grep patterns for large reference files

**Optimize Descriptions**
- Front-load important trigger terms
- Keep descriptions under 512 characters when possible
- Use specific, unique terminology

**Script Efficiency**
- Cache results when possible
- Use helper scripts for repeated operations
- Include progress indicators for long operations

## Quick Reference

### File Structure Template

```
.claude/skills/skill-name/
├── SKILL.md              # Required: Instructions and frontmatter
├── scripts/              # Optional: Executable Python/Bash code
│   └── helper.py
├── references/           # Optional: Documentation loaded as needed
│   └── api_guide.md
└── assets/               # Optional: Templates and output files
    └── template.tsx
```

### YAML Frontmatter Template

```yaml
---
name: skill-name
description: Brief explanation of functionality and when to use. Include specific
  trigger terms like "generate", "create", "validate", technology names, and
  file types. Max 1024 characters.
allowed-tools: Read, Grep, Glob, Edit, Write, Bash
---
```

### Deployment Commands Cheatsheet

```bash
# Validate before deployment
python scripts/quick_validate.py skills/category/skill-name

# Deploy to project (team sharing)
cp -r skills/category/skill-name /path/to/project/.claude/skills/

# Deploy to personal (all projects)
cp -r skills/category/skill-name ~/.claude/skills/

# Deploy from zip
unzip dist/skill-name.zip -d /path/to/project/.claude/skills/

# Verify deployment
ls -la .claude/skills/skill-name/SKILL.md

# Test in Claude Code
# Ask: "What skills are available?"
# Then: Use trigger terms from description
```

### Common Locations

| Type | Path | Scope |
|------|------|-------|
| Project skills | `.claude/skills/` | Current project only |
| Personal skills | `~/.claude/skills/` | All projects on machine |
| Source repository | `skills/category/` | Development/distribution |
| Packaged skills | `dist/*.zip` | Distribution format |

## Next Steps

After deploying skills:

1. **Verify Installation**
   - Check file structure
   - Test skill discovery
   - Validate activation

2. **Integrate with Workflow**
   - Document in project README
   - Add to onboarding materials
   - Create example usage patterns

3. **Customize if Needed**
   - Adapt descriptions for your context
   - Add project-specific references
   - Modify scripts for your stack

4. **Monitor Usage**
   - Note which skills are helpful
   - Identify gaps or improvements
   - Share feedback with team

5. **Stay Updated**
   - Check source repository for updates
   - Review changelog for improvements
   - Update deployed skills periodically

## Additional Resources

- **Source Repository**: https://github.com/your-org/worldbuilding-app-skills
- **Skill Catalog**: [CATALOG.md](../CATALOG.md)
- **Creation Guide**: [skill-creation-guide.md](skill-creation-guide.md)
- **Quick Start**: [../QUICKSTART.md](../QUICKSTART.md)
- **Official Docs**: https://code.claude.com/docs/en/skills.md

## Support

For issues or questions:
1. Check [Troubleshooting](#troubleshooting) section above
2. Review official Claude Code documentation
3. Validate skill structure with `quick_validate.py`
4. Open issue in source repository
