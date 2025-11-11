# Plugins Directory

This directory contains all skills packaged in Claude Code plugin format for easy installation via the plugin marketplace.

## Structure

Each plugin follows this structure:

```
plugin-name/
├── .claude-plugin/
│   └── plugin.json          # Plugin manifest
└── skills/
    └── plugin-name/         # Skill directory
        ├── SKILL.md         # Required: Skill instructions
        ├── scripts/         # Optional: Executable code
        ├── references/      # Optional: Documentation
        └── assets/          # Optional: Templates
```

## Installation

These plugins are automatically available through the Claude Code plugin marketplace.

### Add Marketplace

```
/plugin marketplace add hopeoverture/worldbuilding-app-skills
```

### Install Plugin

```
/plugin install plugin-name@worldbuilding-app-skills
```

## Available Plugins

See the marketplace.json manifest at `.claude-plugin/marketplace.json` for the complete list of 26 available plugins.

### Categories

- **Development** (18 plugins): Next.js scaffolding, Supabase setup, security, validation, CI/CD
- **Testing** (3 plugins): Vitest, Playwright, accessibility testing
- **UI Components** (3 plugins): Forms, markdown editor, component auditing
- **Documentation** (1 plugin): Changelogs and ADRs
- **Utilities** (1 plugin): Skill review and enhancement

## Relationship to skills/ Directory

The `skills/` directory at the repository root contains the source skills.

This `plugins/` directory is generated from the source skills using:

```bash
python scripts/migrate_to_plugins.py
```

Both formats are maintained:
- **skills/**: Source format for development and direct installation
- **plugins/**: Distribution format for Claude Code plugin marketplace

## Documentation

- **Plugin Marketplace Guide**: [../docs/plugin-marketplace-guide.md](../docs/plugin-marketplace-guide.md)
- **Deployment Guide**: [../docs/skill-deployment-guide.md](../docs/skill-deployment-guide.md)
- **Catalog**: [../CATALOG.md](../CATALOG.md)

## Support

For issues or questions about plugins:

1. Check plugin marketplace guide
2. Review marketplace.json manifest
3. Open issue on GitHub repository

---

Generated plugins are ready for use with Claude Code plugin marketplace system.
