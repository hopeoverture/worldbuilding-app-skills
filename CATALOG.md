# Skills Catalog

Inventory of Claude Code skills for worldbuilding application development.

## Development

*Skills for code generation, refactoring, debugging, and architectural patterns.*

### nextjs-fullstack-scaffold

**Location**: `skills/development/nextjs-fullstack-scaffold/`
**Type**: Workflow-Based
**Description**: Scaffolds a production-ready full-stack Next.js application with Next.js 16 (App Router), React 19, TypeScript, Tailwind CSS v4, shadcn/ui, Supabase authentication, Prisma ORM, comprehensive testing (Vitest + Playwright), and CI/CD setup. Generates complete folder structure, configuration files, authentication flow, protected routes, example components, database schema, and tests.

**Trigger Terms**: scaffold, create nextjs app, initialize fullstack, starter template, boilerplate, setup nextjs, production template, full-stack setup, nextjs supabase, nextjs prisma

**Resources**:
- scripts/scaffold.py - Python scaffolding script for generating project files
- references/stack-architecture.md - Complete architecture patterns and best practices
- references/implementation-checklist.md - Step-by-step checklist for all features
- assets/folder-structure.txt - Visual representation of project structure
- assets/templates/package.template.json - package.json template with all dependencies

**Example Usage**:
> "Create a new Next.js app with Supabase authentication and Prisma"
> "Scaffold a full-stack Next.js application with TypeScript and Tailwind"
> "Initialize a production-ready Next.js starter template"

---

## Data Modeling

*Skills for entity schemas, relationships, validation, and data transformation.*

(Skills will be added here as they're created)

---

## UI Components

*Skills for React components, styling patterns, and responsive design.*

(Skills will be added here as they're created)

---

## Documentation

*Skills for API documentation, user guides, and inline comments.*

(Skills will be added here as they're created)

---

## Testing

*Skills for test generation, coverage analysis, and test utilities.*

(Skills will be added here as they're created)

---

## Utilities

*Skills for general-purpose tools, formatters, and development helpers.*

(Skills will be added here as they're created)

---

## How to Add Skills

When creating a new skill, add an entry here following this format:

```markdown
### skill-name

**Location**: `skills/category/skill-name/`
**Type**: [Workflow-Based | Task-Based | Reference | Capabilities]
**Description**: Brief description of what the skill does and when to use it.

**Trigger Terms**: keyword1, keyword2, keyword3
**Resources**:
- scripts/script_name.py - What it does
- references/doc_name.md - What it contains
- assets/template_name.ext - What it's for

**Example Usage**:
> "Generate an entity schema for locations"
```
