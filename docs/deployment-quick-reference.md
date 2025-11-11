# Skill Deployment Quick Reference

One-page reference for common deployment tasks.

## Before Deploying

```bash
# Validate skill structure
python scripts/quick_validate.py skills/category/skill-name

# Check packaged skill integrity
unzip -t dist/skill-name.zip
```

## Deployment Methods

### Deploy to Project (Team Sharing)

```bash
# Single skill
cp -r skills/category/skill-name /path/to/project/.claude/skills/

# From packaged zip
cd /path/to/project/.claude/skills
unzip /path/to/dist/skill-name.zip

# Commit to git
git add .claude/skills/skill-name
git commit -m "Add skill-name skill"
git push
```

### Deploy to Personal (All Projects)

```bash
# Single skill
cp -r skills/category/skill-name ~/.claude/skills/

# From packaged zip
cd ~/.claude/skills
unzip /path/to/dist/skill-name.zip
```

### Deploy Multiple Skills

```bash
# Specific skills
for skill in skill-one skill-two skill-three; do
  cp -r skills/category/$skill /path/to/project/.claude/skills/
done

# Entire category
cp -r skills/development/* /path/to/project/.claude/skills/
```

## Verification Steps

```bash
# 1. Check file exists
ls .claude/skills/skill-name/SKILL.md

# 2. Validate YAML frontmatter
head -n 10 .claude/skills/skill-name/SKILL.md

# 3. Set script permissions (if applicable)
chmod +x .claude/skills/skill-name/scripts/*.py
```

## In Claude Code

```
# Test discovery
What skills are available?

# Test activation
[Use trigger terms from skill description]
```

## Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| Skill not found | Check path: `.claude/skills/skill-name/SKILL.md` |
| Never activates | Add specific trigger terms to description |
| YAML errors | Verify `---` delimiters, no tabs, no emoji |
| Script fails | Check permissions: `chmod +x scripts/*.py` |
| Team can't see | Verify committed: `git log -- .claude/skills/` |

## Common Setups

### New Next.js Project

```bash
PROJECT=".claude/skills"
mkdir -p $PROJECT

cp -r skills/development/nextjs-fullstack-scaffold $PROJECT/
cp -r skills/development/tailwind-shadcn-ui-setup $PROJECT/
cp -r skills/development/supabase-auth-ssr-setup $PROJECT/
cp -r skills/development/api-contracts-and-zod-validation $PROJECT/
```

### Testing Setup

```bash
PROJECT=".claude/skills"

cp -r skills/testing/testing-next-stack $PROJECT/
cp -r skills/testing/playwright-flow-recorder $PROJECT/
cp -r skills/testing/a11y-checker-ci $PROJECT/
```

### Security Setup

```bash
PROJECT=".claude/skills"

cp -r skills/development/security-hardening-checklist $PROJECT/
cp -r skills/development/env-config-validator $PROJECT/
cp -r skills/development/supabase-rls-policy-generator $PROJECT/
cp -r skills/development/csp-config-generator $PROJECT/
```

## File Structure

```
your-project/
└── .claude/
    └── skills/
        └── skill-name/
            ├── SKILL.md          (required)
            ├── scripts/          (optional)
            ├── references/       (optional)
            └── assets/           (optional)
```

## YAML Template

```yaml
---
name: skill-name
description: What it does and when to use. Include trigger terms.
allowed-tools: Read, Grep, Glob, Edit, Write, Bash
---
```

## Updating Skills

```bash
# Pull latest from source
cp -r /path/to/worldbuilding-app-skills/skills/category/skill-name \
      .claude/skills/

# Commit update
git add .claude/skills/skill-name
git commit -m "Update skill-name to latest version"
```

## Removing Skills

```bash
# Remove from project
git rm -r .claude/skills/skill-name
git commit -m "Remove unused skill"

# Remove from personal
rm -rf ~/.claude/skills/skill-name
```

## Available Skills by Category

### Development (18)
- api-contracts-and-zod-validation
- auth-route-protection-checker
- csp-config-generator
- env-config-validator
- eslint-prettier-husky-config
- feature-flag-manager
- github-actions-ci-workflow
- nextjs-fullstack-scaffold
- performance-budget-enforcer
- revalidation-strategy-planner
- role-permission-table-builder
- security-hardening-checklist
- sentry-and-otel-setup
- server-actions-vs-api-optimizer
- supabase-auth-ssr-setup
- supabase-prisma-database-management
- supabase-rls-policy-generator
- tailwind-shadcn-ui-setup

### Documentation (1)
- docs-and-changelogs

### Testing (3)
- a11y-checker-ci
- playwright-flow-recorder
- testing-next-stack

### UI Components (3)
- form-generator-rhf-zod
- markdown-editor-integrator
- ui-library-usage-auditor

### Utilities (1)
- skill-reviewer-and-enhancer

## More Information

Full guide: [skill-deployment-guide.md](skill-deployment-guide.md)
