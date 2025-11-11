# Quick Start Guide

Get started creating Claude Code skills for your worldbuilding application in minutes.

## Prerequisites

- Claude Code installed and configured
- Python 3.7+ (for skill management scripts)
- Your worldbuilding app repository

## Create Your First Skill

### Option 1: Ask Claude (Recommended)

Just describe what you want to automate:

```
Create a skill for generating TypeScript entity schemas
```

Claude will:
1. Ask clarifying questions
2. Plan the skill structure
3. Generate SKILL.md with proper frontmatter
4. Create any needed scripts, references, or assets
5. Update the catalog
6. Offer deployment options

### Option 2: Use the Init Script

```bash
# Navigate to this directory
cd /path/to/worldbuilding-app-skills

# Initialize a new skill
python scripts/init_skill.py entity-generator --path skills/data-modeling

# Edit the generated SKILL.md
# Add any scripts, references, or assets
```

## Deploy Your Skill

### To Your Worldbuilding App

```bash
cp -r skills/data-modeling/entity-generator /path/to/worldbuilding-app/.claude/skills/
```

Now when you work in your worldbuilding app, Claude will automatically use this skill when appropriate.

### To All Your Projects

```bash
cp -r skills/data-modeling/entity-generator ~/.claude/skills/
```

## Validate Your Skill

Before deploying, validate the structure:

```bash
python scripts/quick_validate.py skills/data-modeling/entity-generator
```

## Example: Entity Schema Generator

Let's create a skill that generates TypeScript entity schemas.

### 1. Ask Claude

```
Create a skill that generates TypeScript entity schemas for worldbuilding entities like characters, locations, and items.
```

### 2. Claude Asks Questions

- What properties should be included?
- What TypeScript types should be used?
- Should it include validation rules?
- What naming conventions?

### 3. Claude Creates the Skill

```
skills/data-modeling/entity-schema-generator/
├── SKILL.md
├── scripts/
│   └── generate_schema.py
├── references/
│   └── typescript_patterns.md
└── assets/
    └── entity_template.ts
```

### 4. Deploy to Your App

```bash
cp -r skills/data-modeling/entity-schema-generator \
  /path/to/worldbuilding-app/.claude/skills/
```

### 5. Use It

In your worldbuilding app:
```
Generate a schema for a Location entity with name, description, coordinates, and climate
```

Claude will automatically activate the skill and generate the TypeScript schema.

## Common Skill Ideas

### For Worldbuilding Apps

**Data Modeling:**
- Entity schema generator
- Relationship validator
- Migration generator
- Type definition creator

**UI Components:**
- Entity form generator
- Card component creator
- Timeline component builder
- Map visualization helper

**Development:**
- API endpoint generator
- CRUD operation scaffolder
- State management setup
- Route configuration tool

**Testing:**
- Mock entity generator
- Test fixture creator
- E2E test scaffolder
- Validation test builder

**Documentation:**
- API documentation generator
- Entity documentation writer
- Inline comment generator
- User guide creator

## Skill Structure

Every skill follows this structure:

```
skill-name/
├── SKILL.md (required)
│   ├── YAML frontmatter (name, description, allowed-tools)
│   └── Instructions (imperative form)
└── Bundled Resources (optional)
    ├── scripts/      - Executable code
    ├── references/   - Documentation
    └── assets/       - Templates/files
```

## Best Practices

1. **Start Simple**: Create focused skills that do one thing well
2. **Use Resources**: Put reusable code in scripts/, docs in references/
3. **Clear Triggers**: Include specific terms users would actually say
4. **Imperative Form**: Write "To do X, use Y" not "You should do X"
5. **Validate First**: Run `quick_validate.py` before deploying
6. **Update Catalog**: Add your skill to CATALOG.md

## SKILL.md Template

```yaml
---
name: my-skill-name
description: This skill should be used when [trigger scenario]. It [what it does]. Use it for [specific use cases]. Trigger terms: keyword1, keyword2, keyword3.
allowed-tools: Read, Grep, Glob, Bash  # Optional - for readonly
---

# Skill Instructions

To accomplish [goal], follow these steps:

1. Analyze the [input/context]
2. Generate the [output] using [method]
3. Validate the [result]

## Using Scripts

Execute `scripts/helper.py` to [purpose].

## References

Consult `references/guide.md` for [information].

## Assets

Use templates in `assets/` for [purpose].
```

## Next Steps

1. **Browse Examples**: Check CATALOG.md for existing skills
2. **Read Docs**: See docs/skill-creation-guide.md for details
3. **Create Skills**: Start automating your common tasks
4. **Iterate**: Refine skills based on actual usage

## Getting Help

- **Documentation**: Read CLAUDE.md for Claude's instructions
- **Examples**: Browse the skills/ directory
- **Validation**: Use quick_validate.py to check structure
- **Official Guide**: See docs/skill-creation-guide.md

## Useful Commands

```bash
# Create a skill
python scripts/init_skill.py skill-name --path skills/category

# Validate a skill
python scripts/quick_validate.py skills/category/skill-name

# Package for distribution
python scripts/package_skill.py skills/category/skill-name ./dist

# Deploy to project
cp -r skills/category/skill-name /path/to/project/.claude/skills/

# Deploy globally
cp -r skills/category/skill-name ~/.claude/skills/
```

Now start creating skills that streamline your worldbuilding app development!
