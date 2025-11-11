# Worldbuilding App Skills

Claude Code skills for developing and maintaining worldbuilding applications, built using official Anthropic best practices.

## About This Project

This repository contains custom Claude Code skills designed specifically for web development work on worldbuilding applications. These skills help automate common tasks, enforce best practices, and streamline development workflows.

## Structure

```
worldbuilding-app-skills/
├── README.md (this file)
├── QUICKSTART.md (quick start guide)
├── CLAUDE.md (guidance for Claude Code)
├── CATALOG.md (inventory of skills)
├── .claude-plugin/
│   └── marketplace.json   - Plugin marketplace manifest
├── plugins/ (plugin format for marketplace)
│   ├── nextjs-fullstack-scaffold/
│   ├── tailwind-shadcn-ui-setup/
│   └── ... (26 total plugins)
├── skills/ (organized by purpose)
│   ├── development/      - Code generation, refactoring, patterns
│   ├── data-modeling/    - Entity schemas, relationships, validation
│   ├── ui-components/    - Component generation, styling
│   ├── documentation/    - API docs, user guides, comments
│   ├── testing/          - Unit tests, integration tests, e2e tests
│   └── utilities/        - Helpers, formatters, tools
├── scripts/ (skill management tools)
│   ├── init_skill.py      - Initialize new skill structure
│   ├── quick_validate.py  - Validate skill structure
│   ├── package_skill.py   - Package for distribution
│   └── migrate_to_plugins.py - Convert skills to plugin format
├── dist/ (packaged skills as .zip files)
└── docs/ (additional documentation)
```

## Quick Start

### Create a New Skill

Ask Claude Code:
```
Create a skill for [what you want to automate]
```

Claude will follow the official 6-step process:
1. Ask clarifying questions with concrete examples
2. Plan reusable resources (scripts, references, assets)
3. Initialize with proper structure
4. Implement the skill with resources
5. Update the catalog
6. Offer deployment options

### Or Use the Init Script

```bash
python scripts/init_skill.py my-skill-name --path skills/development
```

Then edit the generated SKILL.md and supporting files.

## Installing Skills

### Option 1: Plugin Marketplace (Recommended)

The easiest way to use these skills is through the Claude Code plugin marketplace:

**Step 1: Add the marketplace**
```
/plugin marketplace add hopeoverture/worldbuilding-app-skills
```

**Step 2: Install plugins**
```
/plugin install nextjs-fullstack-scaffold@worldbuilding-app-skills
/plugin install tailwind-shadcn-ui-setup@worldbuilding-app-skills
/plugin install form-generator-rhf-zod@worldbuilding-app-skills
```

**Benefits:**
- One-command installation and updates
- Easy discovery and version management
- Works across all your projects
- Official distribution method

See [docs/plugin-marketplace-guide.md](docs/plugin-marketplace-guide.md) for complete plugin marketplace documentation.

### Option 2: Direct Copy

**Quick Deploy to Project:**
```bash
# Copy to your worldbuilding app's .claude/skills directory
cp -r skills/category/skill-name /path/to/worldbuilding-app/.claude/skills/
```

**Deploy to Personal Use (All Projects):**
```bash
cp -r skills/category/skill-name ~/.claude/skills/
```

**Deploy from Packaged Zip:**
```bash
# All skills are pre-packaged in dist/
unzip dist/skill-name.zip -d /path/to/project/.claude/skills/
```

**For Complete Deployment Guide:**
See [docs/skill-deployment-guide.md](docs/skill-deployment-guide.md) for detailed instructions,
troubleshooting, and best practices.

## Skill Categories

### Development
Code generation, refactoring, architecture patterns, debugging tools for worldbuilding features.

### Data Modeling
Entity schemas, relationship definitions, validation rules, data transformation utilities.

### UI Components
React component generation, styling patterns, responsive design helpers.

### Documentation
API documentation, user guides, inline comments, architecture docs.

### Testing
Test generation, coverage analysis, mock data generation, test utilities.

### Utilities
General-purpose tools, formatters, converters, development helpers.

## Worldbuilding-Specific Use Cases

Skills in this repository might help with:
- Generating entity types (characters, locations, items, factions)
- Creating relationship schemas between entities
- Building timeline and chronology tools
- Managing world attributes and settings
- Generating map data structures
- Creating content templates
- Validating world consistency
- Export/import utilities

## Skill Structure

Each skill follows official Anthropic structure:

```
skill-name/
├── SKILL.md (required - YAML frontmatter + instructions)
└── Bundled Resources (optional)
    ├── scripts/      - Executable Python/Bash code
    ├── references/   - Documentation loaded as needed
    └── assets/       - Templates/files for output
```

## Best Practices

1. **Clear Names**: lowercase-with-hyphens (e.g., `entity-schema-generator`)
2. **Specific Triggers**: Include terms users actually say in descriptions
3. **Stay Focused**: One clear capability per skill
4. **Use Resources**: Put code in scripts/, docs in references/, templates in assets/
5. **Imperative Form**: Write "To do X, use Y" not "You should do X"
6. **Validate First**: Run `quick_validate.py` before deploying

## Official Scripts

### init_skill.py
```bash
python scripts/init_skill.py skill-name --path skills/category
```

### quick_validate.py
```bash
python scripts/quick_validate.py skills/category/skill-name
```

### package_skill.py
```bash
python scripts/package_skill.py skills/category/skill-name ./dist
```

## Available Skills

See [CATALOG.md](CATALOG.md) for the complete inventory of skills.

## Resources

- **Plugin Marketplace Guide**: [docs/plugin-marketplace-guide.md](docs/plugin-marketplace-guide.md) - Easy installation via Claude Code plugins (recommended)
- **Deployment Guide**: [docs/skill-deployment-guide.md](docs/skill-deployment-guide.md) - Complete guide for importing skills into projects
- **Quick Reference**: [docs/deployment-quick-reference.md](docs/deployment-quick-reference.md) - Common deployment commands
- **Creation Guide**: [docs/skill-creation-guide.md](docs/skill-creation-guide.md) - How to create new skills
- **Quick Start**: [QUICKSTART.md](QUICKSTART.md) - Get started quickly
- **Catalog**: [CATALOG.md](CATALOG.md) - Full inventory of available skills
- **Claude Instructions**: [CLAUDE.md](CLAUDE.md) - Guidance for Claude Code

## Contributing

When creating new skills for this project:
1. Follow the official 6-step process
2. Update CATALOG.md
3. Validate before committing
4. Document trigger terms clearly
5. Include concrete examples in descriptions
