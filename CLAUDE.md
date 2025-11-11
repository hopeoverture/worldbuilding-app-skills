# CLAUDE.md

This file provides guidance to Claude Code when working with skills in this repository.

## Repository Purpose

This is a **skills repository for worldbuilding application development** - a collection of Claude Code skills designed to streamline web development work on worldbuilding apps using **official Anthropic best practices**.

## Project Context

**Application Type**: Web-based worldbuilding application
**Tech Stack**: Modern web technologies (React, Node.js, databases, etc.)
**Focus Areas**: Entity management, relationship mapping, timeline tools, world consistency, data visualization

## Official Skill Creation Process

When the user requests a skill, follow the official 6-step process from Anthropic's skill-creator:

### 1. Understand with Concrete Examples

Ask clarifying questions before creating:
- What functionality should the skill support?
- Can you give examples of how this would be used?
- What would a user say that should trigger this skill?
- How does this relate to worldbuilding app features?

**Don't skip this** - understanding concrete usage is critical for effective skills.

### 2. Plan Reusable Resources

Analyze examples to determine needed resources:
- **scripts/**: Is the same code repeatedly rewritten? Deterministic operations needed?
- **references/**: Does Claude need reference docs, schemas, API guides, or specifications?
- **assets/**: Are there templates, boilerplate code, or files needed for output?

### 3. Initialize with Official Script

```bash
python scripts/init_skill.py skill-name --path skills/category
```

Categories: `development`, `data-modeling`, `ui-components`, `documentation`, `testing`, `utilities`

### 4. Edit the Skill

**A. Implement Resources First**
- Add scripts to `scripts/` directory
- Add reference docs to `references/` directory
- Add templates/assets to `assets/` directory
- Delete example files that aren't needed

**B. Update SKILL.md**

**Critical: Use imperative/infinitive form (verb-first), NOT second person**

Good: "To generate entity schemas, analyze the requirements and create TypeScript interfaces."
Bad: "You should generate entity schemas by analyzing requirements."

**Frontmatter structure:**
```yaml
---
name: skill-name  # hyphen-case only
description: Complete explanation with trigger terms. Use third-person. Max 1024 chars.
allowed-tools: Read, Grep, Glob, Bash  # Optional - for readonly skills
---
```

**Description requirements:**
- Use third-person ("This skill should be used when...")
- Include WHAT it does and WHEN to use it
- Include specific trigger terms users would actually say
- Max 1024 characters

### 5. Update Catalog

Add entry to `CATALOG.md` under appropriate category with location, type, description, trigger terms, and resources.

### 6. Offer Deployment

Ask user about deployment:
- Project: `cp -r skills/category/skill-name /path/to/worldbuilding-app/.claude/skills/`
- Personal: `cp -r skills/category/skill-name ~/.claude/skills/`
- Package: `python scripts/package_skill.py skills/category/skill-name ./dist`

## Skill Structure

Official Anthropic structure:

```
skill-name/
├── SKILL.md (required - YAML frontmatter + instructions)
└── Bundled Resources (optional)
    ├── scripts/      - Executable Python/Bash code
    ├── references/   - Documentation loaded as needed
    └── assets/       - Templates/files for output
```

## Progressive Disclosure

Three-level loading system:
1. **Metadata** (name + description): Always in context (~100 words)
2. **SKILL.md body**: When skill triggers (<5k words recommended)
3. **Bundled resources**: As needed (unlimited)

Keep SKILL.md lean. Move detailed info to references/. Put output files in assets/.

## Writing Style

**Always use imperative/infinitive form:**
- "To accomplish X, do Y"
- "Use scripts/helper.py when..."
- "Consult references/api.md for details"

**Never use second person:**
- ~~"You should do X"~~
- ~~"If you need Y, you can..."~~

## Resource Guidelines

### scripts/
Executable code for deterministic operations. Include when same code is repeatedly rewritten.
- Examples: `generate_entity_schema.py`, `validate_relationships.py`, `export_timeline.py`
- Can execute without loading into context

### references/
Documentation loaded into context as needed. Include for detailed info too long for SKILL.md.
- Examples: `api_endpoints.md`, `entity_schema.md`, `database_structure.md`
- For large files (>10k words), include grep patterns in SKILL.md

### assets/
Files used in output (not loaded into context). Include templates, boilerplate, starter code.
- Examples: `entity_template.ts`, `component_boilerplate/`, `test_fixtures/`

## Worldbuilding-Specific Trigger Terms

Include these in descriptions for better discoverability:

**Entity & Data:**
- entity, character, location, item, faction, organization
- relationship, connection, link, association
- attribute, property, field, metadata
- schema, model, type, interface

**Worldbuilding Features:**
- timeline, chronology, event, history
- map, geography, region, territory
- lore, backstory, description, narrative
- consistency, validation, conflict detection

**Development:**
- generate, create, scaffold, initialize
- analyze, check, review, audit
- refactor, optimize, improve
- document, explain, annotate
- test, coverage, mock data

## Tool Restrictions

For readonly/analysis skills, use `allowed-tools` to avoid permission prompts:

```yaml
allowed-tools: Read, Grep, Glob, Bash
```

Common combinations:
- Analysis only: Read, Grep, Glob, Bash
- File operations: Read, Edit, Write, Bash
- Full access: Omit allowed-tools

## Quality Checklist

Before finishing, verify:
- [ ] Name is hyphen-case (lowercase, hyphens only, no consecutive hyphens)
- [ ] Description uses third-person voice
- [ ] Description includes specific trigger terms
- [ ] Description explains WHAT and WHEN (max 1024 chars)
- [ ] Instructions use imperative form (verb-first)
- [ ] Resources referenced in SKILL.md
- [ ] Example files deleted if not needed
- [ ] `allowed-tools` set if readonly
- [ ] CATALOG.md updated
- [ ] Validated: `python scripts/quick_validate.py skills/category/skill-name`

## Skill Categories for This Project

- **development**: Code generation, refactoring, debugging, patterns for worldbuilding features
- **data-modeling**: Entity schemas, relationships, validation, data transformation
- **ui-components**: React components, styling, responsive design for worldbuilding UI
- **documentation**: API docs, user guides, inline comments, architecture documentation
- **testing**: Test generation, coverage, mock data, test utilities
- **utilities**: Formatters, converters, helpers, development tools

## Template Patterns

Choose based on skill structure:
- **Workflow-Based**: Sequential processes with clear steps
- **Task-Based**: Different operations/capabilities
- **Reference/Guidelines**: Standards, specifications, policies
- **Capabilities-Based**: Interrelated features

Mix patterns as needed for your specific skill.

## Key Files

- `CLAUDE.md`: This file - instructions for Claude Code
- `README.md`: User-facing documentation
- `CATALOG.md`: Inventory of all created skills
- `QUICKSTART.md`: Quick start guide
- `scripts/`: Official Anthropic skill creation tools
- `docs/skill-creation-guide.md`: Comprehensive creation guide

## Remember

This repository uses **official Anthropic best practices** from the skill-creator skill:

1. Start with concrete examples (don't skip Step 1)
2. Plan resources before coding (Step 2)
3. Use init script for structure (Step 3)
4. Write imperatively, third-person descriptions (Step 4)
5. Include specific trigger terms (Step 4)
6. Update catalog (Step 5)
7. Validate before deploying (Step 6)
8. Iterate based on real usage

These practices ensure skills follow Anthropic's official standards and work reliably in worldbuilding app development contexts.
