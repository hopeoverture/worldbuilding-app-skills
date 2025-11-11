# Skill Creation Guide

Based on official Anthropic best practices from the skill-creator skill.

## Quick Start

Just tell Claude what skill you want to create! For example:

- "Create a skill to help with API documentation"
- "I need a skill for analyzing test coverage"
- "Make a skill that helps refactor React components"

Claude will follow the official Anthropic skill creation process.

## Official Skill Creation Process

### Step 1: Understanding the Skill with Concrete Examples

Before creating a skill, clearly understand concrete examples of how it will be used:

**Good questions to ask:**
- What functionality should the skill support?
- Can you give examples of how this skill would be used?
- What would a user say that should trigger this skill?

**Example:** For an image-editor skill:
- "Remove the red-eye from this image"
- "Rotate this image 90 degrees"
- "Crop this photo to 800x600"

### Step 2: Planning Reusable Resources

Analyze each example to determine what resources would be helpful:

**Example 1: PDF Editor**
- Query: "Help me rotate this PDF"
- Analysis: Rotating PDFs requires same code each time
- **Resource needed**: `scripts/rotate_pdf.py`

**Example 2: Frontend Builder**
- Query: "Build me a todo app"
- Analysis: Needs same HTML/React boilerplate each time
- **Resource needed**: `assets/hello-world/` template directory

**Example 3: BigQuery Skill**
- Query: "How many users logged in today?"
- Analysis: Needs table schemas and relationships
- **Resource needed**: `references/schema.md`

### Step 3: Initialize the Skill

Use the official init script:

```bash
python scripts/init_skill.py skill-name --path skills/category
```

This creates:
- SKILL.md with proper frontmatter and TODO markers
- Example files in scripts/, references/, and assets/
- Proper directory structure

### Step 4: Edit the Skill

#### Start with Resources

Implement the resources identified in Step 2:
- Add scripts in `scripts/`
- Add reference docs in `references/`
- Add templates/assets in `assets/`
- Delete example files you don't need

#### Update SKILL.md

Use **imperative/infinitive form** (verb-first), not second person:

**Good:**
```markdown
To generate API docs, analyze the endpoints and create OpenAPI specs.
Use scripts/generator.py when processing multiple files.
```

**Bad:**
```markdown
You should generate API docs by analyzing endpoints.
If you need to process multiple files, you can use scripts/generator.py.
```

Answer these questions in SKILL.md:
1. What is the purpose of the skill?
2. When should the skill be used?
3. How should Claude use the skill in practice?
4. What resources are available and how to use them?

### Step 5: Package the Skill

Validate and package:

```bash
python scripts/package_skill.py skills/category/skill-name ./dist
```

This automatically:
1. Validates the skill structure
2. Creates a distributable zip file
3. Reports any errors

### Step 6: Iterate

After testing, improve based on real usage:
1. Use the skill on real tasks
2. Notice struggles or inefficiencies
3. Update SKILL.md or resources
4. Test again

## Resource Types

### scripts/

Executable code for deterministic operations.

**When to include:**
- Same code is repeatedly rewritten
- Deterministic reliability needed
- Complex operations

**Examples:**
- `pdf/scripts/fill_fillable_fields.py`
- `docx/scripts/document.py`
- `data/scripts/transform_csv.py`

**Benefits:**
- Token efficient
- Deterministic execution
- Can execute without loading into context

### references/

Documentation loaded into context as needed.

**When to include:**
- Detailed documentation too long for SKILL.md
- API references
- Database schemas
- Comprehensive guides

**Examples:**
- `bigquery/references/api_docs.md`
- `finance/references/schema.md`
- `product-management/references/communication.md`

**Best practice:**
- Keep SKILL.md lean
- Claude loads only when needed
- For large files (>10k words), include grep patterns in SKILL.md

### assets/

Files used in Claude's output (not loaded into context).

**When to include:**
- Templates for Claude to copy/modify
- Images, logos, icons
- Boilerplate code directories
- Fonts, sample data

**Examples:**
- `brand/assets/logo.png`
- `frontend/assets/hello-world/` (React boilerplate)
- `typography/assets/font.ttf`
- `slides/assets/template.pptx`

**Use cases:**
- Document templates
- Project scaffolding
- Brand assets
- Starter files

## Progressive Disclosure

Skills use three-level loading:

1. **Metadata** (name + description): Always in context (~100 words)
2. **SKILL.md body**: Loaded when skill triggers (<5k words recommended)
3. **Bundled resources**: Loaded/executed as needed (unlimited)

This keeps context efficient while providing unlimited capability.

## Writing Effective Descriptions

Descriptions determine when Claude uses your skill.

**Requirements:**
- Max 1024 characters
- Use third-person (not "Use this when you...")
- Include specific trigger terms
- Explain WHAT and WHEN

**Good:**
```yaml
description: Generate OpenAPI/Swagger documentation from REST API endpoints. This skill should be used when the user asks to create API docs, document endpoints, generate Swagger files, or create API specifications.
```

**Bad:**
```yaml
description: Helps with API documentation
```

**Trigger terms by skill type:**

- **Code generation**: create, generate, scaffold, boilerplate, setup, initialize
- **Analysis**: analyze, check, review, audit, inspect, examine, evaluate
- **Refactoring**: refactor, restructure, clean up, organize, improve, optimize
- **Documentation**: document, generate docs, create README, API docs, write guide
- **Testing**: test, coverage, unit test, integration test, e2e, test suite
- **Debugging**: debug, troubleshoot, fix, resolve, diagnose, error, issue

## Validation

Before deploying, validate your skill:

```bash
python scripts/quick_validate.py skills/category/skill-name
```

**Checks:**
- SKILL.md exists
- Valid YAML frontmatter
- Required fields present (name, description)
- Name is hyphen-case (lowercase, hyphens only)
- No consecutive hyphens or leading/trailing hyphens
- Description doesn't contain angle brackets

## Tool Restrictions

For read-only skills, use `allowed-tools` to avoid permission prompts:

```yaml
---
name: code-analyzer
description: Analyze code for patterns and issues...
allowed-tools: Read, Grep, Glob, Bash
---
```

**Common combinations:**
- **Analysis only**: Read, Grep, Glob, Bash
- **File operations**: Read, Edit, Write, Bash
- **Full access**: Omit allowed-tools

## Deploying Skills

### Personal Use
```bash
cp -r skills/category/skill-name ~/.claude/skills/
```

### Project/Team Use
```bash
cp -r skills/category/skill-name .claude/skills/
git add .claude/skills/skill-name
git commit -m "Add skill-name skill"
git push
```

Team members get it on pull.

### Plugin Distribution
```bash
python scripts/package_skill.py skills/category/skill-name ./dist
```

Share the `skill-name.zip` file.

## Testing Your Skill

1. **Deploy** to skills directory
2. **Start** new Claude Code session
3. **Use trigger terms** from description
4. **Observe** if Claude invokes skill
5. **Iterate** based on results

## Troubleshooting

**Skill doesn't trigger:**
- Add more specific trigger terms to description
- Use third-person in description
- Verify skill in correct location
- Check YAML syntax (no tabs)

**Validation fails:**
- Name must be hyphen-case
- No consecutive hyphens
- No angle brackets in description
- Proper YAML frontmatter format

**Permission prompts:**
- Add `allowed-tools` for readonly skills
- Ensure scripts are executable (`chmod +x`)

## Examples

### Workflow-Based Skill

```yaml
---
name: pdf-editor
description: Edit, merge, rotate, and manipulate PDF files. This skill should be used when the user asks to modify PDFs, combine PDFs, rotate pages, extract text, or perform PDF operations.
---

# PDF Editor

## Overview
Comprehensive toolkit for PDF manipulation operations.

## Quick Start
Determine the operation needed and follow the appropriate workflow below.

## Merging PDFs
To merge multiple PDFs:
1. Use scripts/merge_pdfs.py with file paths
2. Specify output filename
3. Confirm success

## Rotating PDFs
To rotate PDF pages:
1. Use scripts/rotate_pdf.py
2. Specify rotation angle (90, 180, 270)
3. Save to new file
```

### Reference-Based Skill

```yaml
---
name: database-schema-guide
description: Guide for working with the company database schema. This skill should be used when the user asks about database structure, table relationships, queries, or database design questions.
allowed-tools: Read, Grep, Glob, Bash
---

# Database Schema Guide

## Overview
Complete reference for database schema, relationships, and query patterns.

## Usage
Consult references/schema.md for complete table definitions, relationships, and indexes.

## Common Queries
See references/query_patterns.md for examples of frequently used queries.
```

### Asset-Based Skill

```yaml
---
name: project-scaffolder
description: Scaffold new projects with proper directory structure and boilerplate code. This skill should be used when the user asks to create a new project, set up a project, initialize a codebase, or generate project structure.
---

# Project Scaffolder

## Overview
Quickly scaffold new projects with best practices and boilerplate.

## Usage
1. Determine project type (React, Python, Node, etc.)
2. Copy appropriate template from assets/
3. Customize package.json, requirements.txt, etc.
4. Initialize git repository

## Available Templates
- assets/react-template/ - React + TypeScript + Vite
- assets/python-template/ - Python project with tests
- assets/node-template/ - Node + Express API
```

## Best Practices Summary

1. **Start with concrete examples** - Understand real usage before building
2. **Plan resources first** - Identify scripts, references, assets needed
3. **Use init script** - Official template ensures correct structure
4. **Write imperatively** - Verb-first instructions, not second person
5. **Specific descriptions** - Include trigger terms users will actually say
6. **Progressive disclosure** - Use references/ and assets/ to keep SKILL.md lean
7. **Validate before deploy** - Catch errors early
8. **Iterate based on use** - Improve from real-world feedback
9. **Tool restrictions** - Use allowed-tools for readonly skills
10. **Delete unused examples** - Remove example files you don't need

## Additional Resources

- **Official Docs**: https://code.claude.com/docs/en/skills.md
- **skill-creator skill**: Available as Claude Code plugin
- **Factory Catalog**: `CATALOG.md`
- **Quick Start**: `QUICKSTART.md`
