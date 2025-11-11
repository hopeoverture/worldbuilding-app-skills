# Plugin Marketplace Guide

Complete guide for using the Worldbuilding App Skills plugin marketplace to easily install and manage skills.

## Table of Contents

- [What is the Plugin Marketplace?](#what-is-the-plugin-marketplace)
- [Quick Start](#quick-start)
- [Installing Plugins](#installing-plugins)
- [Managing Plugins](#managing-plugins)
- [Available Plugins](#available-plugins)
- [Troubleshooting](#troubleshooting)

## What is the Plugin Marketplace?

The Worldbuilding App Skills plugin marketplace provides an easy way to install and manage all 26 Claude Code skills through Claude's built-in plugin system. Instead of manually copying skill directories, you can install plugins with a single command.

### Benefits of Plugin Format

- **One-command installation**: Install any skill instantly
- **Automatic updates**: Update plugins with simple commands
- **Easy discovery**: Browse available plugins via `/plugin`
- **Version management**: Track and manage plugin versions
- **Team sharing**: Share marketplace configuration across teams

## Quick Start

### Step 1: Add the Marketplace

Open Claude Code and add the Worldbuilding App Skills marketplace:

```
/plugin marketplace add hopeoverture/worldbuilding-app-skills
```

This connects Claude Code to the plugin marketplace hosted on GitHub.

### Step 2: Browse Available Plugins

List all available plugins:

```
/plugin
```

This shows all 26 skills available in the marketplace, organized by category.

### Step 3: Install a Plugin

Install any plugin by name:

```
/plugin install nextjs-fullstack-scaffold@worldbuilding-app-skills
```

The plugin is now available for use across your Claude Code projects!

## Installing Plugins

### Install Single Plugin

Install a specific plugin:

```
/plugin install plugin-name@worldbuilding-app-skills
```

Examples:

```
/plugin install tailwind-shadcn-ui-setup@worldbuilding-app-skills
/plugin install supabase-auth-ssr-setup@worldbuilding-app-skills
/plugin install form-generator-rhf-zod@worldbuilding-app-skills
```

### Install Multiple Plugins

Install several plugins for a new project:

```
/plugin install nextjs-fullstack-scaffold@worldbuilding-app-skills
/plugin install tailwind-shadcn-ui-setup@worldbuilding-app-skills
/plugin install api-contracts-and-zod-validation@worldbuilding-app-skills
/plugin install testing-next-stack@worldbuilding-app-skills
```

### Starter Bundles

**Full Stack Setup (Core Development)**

```
/plugin install nextjs-fullstack-scaffold@worldbuilding-app-skills
/plugin install tailwind-shadcn-ui-setup@worldbuilding-app-skills
/plugin install eslint-prettier-husky-config@worldbuilding-app-skills
/plugin install api-contracts-and-zod-validation@worldbuilding-app-skills
/plugin install env-config-validator@worldbuilding-app-skills
```

**Authentication & Database**

```
/plugin install supabase-auth-ssr-setup@worldbuilding-app-skills
/plugin install supabase-prisma-database-management@worldbuilding-app-skills
/plugin install supabase-rls-policy-generator@worldbuilding-app-skills
/plugin install auth-route-protection-checker@worldbuilding-app-skills
```

**UI Components**

```
/plugin install form-generator-rhf-zod@worldbuilding-app-skills
/plugin install markdown-editor-integrator@worldbuilding-app-skills
/plugin install ui-library-usage-auditor@worldbuilding-app-skills
```

**Testing & Quality**

```
/plugin install testing-next-stack@worldbuilding-app-skills
/plugin install playwright-flow-recorder@worldbuilding-app-skills
/plugin install a11y-checker-ci@worldbuilding-app-skills
```

**Security**

```
/plugin install security-hardening-checklist@worldbuilding-app-skills
/plugin install csp-config-generator@worldbuilding-app-skills
/plugin install env-config-validator@worldbuilding-app-skills
```

## Managing Plugins

### List Installed Plugins

See all your installed plugins:

```
/plugin list
```

### Update Plugin

Update a plugin to the latest version:

```
/plugin update plugin-name
```

### Uninstall Plugin

Remove a plugin you no longer need:

```
/plugin uninstall plugin-name
```

### View Plugin Details

Get information about a specific plugin:

```
/plugin info plugin-name@worldbuilding-app-skills
```

## Available Plugins

### Development (18 plugins)

| Plugin Name | Description |
|-------------|-------------|
| `nextjs-fullstack-scaffold` | Scaffold production-ready Next.js apps |
| `tailwind-shadcn-ui-setup` | Configure Tailwind CSS and shadcn/ui |
| `supabase-auth-ssr-setup` | Setup Supabase SSR authentication |
| `supabase-prisma-database-management` | Manage Prisma database schema |
| `supabase-rls-policy-generator` | Generate RLS security policies |
| `auth-route-protection-checker` | Audit and protect routes |
| `security-hardening-checklist` | Comprehensive security audit |
| `csp-config-generator` | Generate CSP headers |
| `api-contracts-and-zod-validation` | Create Zod validation schemas |
| `server-actions-vs-api-optimizer` | Optimize route patterns |
| `env-config-validator` | Validate environment configs |
| `eslint-prettier-husky-config` | Setup code quality tools |
| `github-actions-ci-workflow` | Configure CI/CD pipelines |
| `feature-flag-manager` | Implement feature flags |
| `sentry-and-otel-setup` | Add error tracking |
| `revalidation-strategy-planner` | Optimize caching strategies |
| `performance-budget-enforcer` | Monitor performance budgets |
| `role-permission-table-builder` | Generate RBAC matrices |

### Testing (3 plugins)

| Plugin Name | Description |
|-------------|-------------|
| `testing-next-stack` | Complete testing infrastructure |
| `playwright-flow-recorder` | Generate E2E tests from flows |
| `a11y-checker-ci` | CI accessibility testing |

### UI Components (3 plugins)

| Plugin Name | Description |
|-------------|-------------|
| `form-generator-rhf-zod` | Generate React Hook Form components |
| `ui-library-usage-auditor` | Audit component usage |
| `markdown-editor-integrator` | Add markdown editing |

### Documentation (1 plugin)

| Plugin Name | Description |
|-------------|-------------|
| `docs-and-changelogs` | Generate changelogs and docs |

### Utilities (1 plugin)

| Plugin Name | Description |
|-------------|-------------|
| `skill-reviewer-and-enhancer` | Review and improve skills |

## Troubleshooting

### Marketplace Not Found

**Problem**: `/plugin marketplace add` fails

**Solution**:
1. Verify GitHub repository is public
2. Check repository URL: `hopeoverture/worldbuilding-app-skills`
3. Ensure `.claude-plugin/marketplace.json` exists in repo

### Plugin Installation Fails

**Problem**: `/plugin install` returns error

**Solution**:
1. Verify plugin name is correct (use `/plugin` to list)
2. Check marketplace is added: `/plugin marketplace list`
3. Try reinstalling marketplace:
   ```
   /plugin marketplace remove worldbuilding-app-skills
   /plugin marketplace add hopeoverture/worldbuilding-app-skills
   ```

### Plugin Not Activating

**Problem**: Plugin installed but skill doesn't trigger

**Solution**:
1. Check plugin is installed: `/plugin list`
2. Restart Claude Code
3. Use explicit trigger terms from skill description
4. Ask: "What skills are available?" to verify

### Multiple Marketplace Conflicts

**Problem**: Same plugin name in different marketplaces

**Solution**:
Always specify marketplace: `plugin-name@worldbuilding-app-skills`

### Update Not Working

**Problem**: `/plugin update` doesn't get latest changes

**Solution**:
1. Uninstall and reinstall:
   ```
   /plugin uninstall plugin-name
   /plugin install plugin-name@worldbuilding-app-skills
   ```
2. Clear plugin cache (if available)
3. Check if marketplace has been updated on GitHub

## Comparison: Plugins vs Direct Copy

### Use Plugins When:

- Want easy installation and updates
- Working across multiple projects
- Need centralized management
- Want version tracking
- Prefer official distribution method

### Use Direct Copy When:

- Customizing skills for specific project
- Working offline or without GitHub access
- Testing skill modifications
- Need version control with project code
- Working with team via project repository

Both methods work well - choose based on your workflow!

## Advanced Usage

### Project-Level Marketplace Configuration

Add marketplace to project's `.claude/settings.json`:

```json
{
  "pluginMarketplaces": [
    {
      "name": "worldbuilding-app-skills",
      "url": "https://github.com/hopeoverture/worldbuilding-app-skills"
    }
  ],
  "plugins": [
    "nextjs-fullstack-scaffold@worldbuilding-app-skills",
    "tailwind-shadcn-ui-setup@worldbuilding-app-skills"
  ]
}
```

Team members automatically get access when they trust the folder.

### Custom Marketplace URL

If forking or hosting elsewhere:

```
/plugin marketplace add https://github.com/your-org/your-fork
```

### Verify Plugin Integrity

Check plugin contents after installation:

```
ls ~/.claude/plugins/plugin-name/
```

## Next Steps

After installing plugins:

1. **Test activation**: Use trigger terms to verify skills work
2. **Install dependencies**: Check SKILL.md for required packages
3. **Customize if needed**: Modify installed plugins in `~/.claude/plugins/`
4. **Share with team**: Configure project-level marketplace settings
5. **Stay updated**: Periodically check for plugin updates

## Additional Resources

- **Skill Catalog**: [CATALOG.md](../CATALOG.md) - Detailed descriptions of all skills
- **Direct Installation**: [skill-deployment-guide.md](skill-deployment-guide.md) - Manual installation methods
- **Quick Reference**: [deployment-quick-reference.md](deployment-quick-reference.md) - Common commands
- **Official Docs**: https://code.claude.com/docs/en/plugin-marketplaces

## Support

For issues or questions:

1. Check [Troubleshooting](#troubleshooting) section above
2. Review plugin description: `/plugin info plugin-name@worldbuilding-app-skills`
3. Check GitHub repository issues
4. Open issue at: https://github.com/hopeoverture/worldbuilding-app-skills/issues

---

**Happy building!** The plugin marketplace makes it easy to get started with worldbuilding app development using best practices and proven patterns.
