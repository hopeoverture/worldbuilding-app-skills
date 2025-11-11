# Anthropic Skill Standards

Official standards for creating Claude Code skills based on Anthropic's skill-creator best practices.

## Core Principles

Skills should follow these fundamental principles:
1. **Progressive Disclosure**: Metadata → SKILL.md → Resources (load only what's needed)
2. **Imperative Voice**: Use verb-first instructions, not second-person
3. **Third-Person Descriptions**: Describe what the skill does, not what "you" do
4. **Resource Bundling**: Scripts, references, and assets organized in standard directories

## Skill Structure

### Required Files

```
skill-name/
├── SKILL.md (required)
└── Optional bundled resources:
    ├── scripts/      - Executable code
    ├── references/   - Documentation loaded as needed
    └── assets/       - Templates and output files
```

### SKILL.md Format

```markdown
---
name: skill-name-in-hyphen-case
description: Third-person description with trigger terms. Max 1024 chars.
allowed-tools: Read, Grep, Glob  # Optional, for read-only skills
---

# Skill Title

Brief overview paragraph.

## Overview

To accomplish [goal], this skill [explains approach].

## When to Use

Use this skill when:
- [Specific scenario 1]
- [Specific scenario 2]

## Implementation Steps

### Step 1: [Action]

To [accomplish substep], do:

1. [Specific instruction]
2. [Specific instruction]

[Code example if applicable]

...

## Resources

- `scripts/[name].py` - Description
- `references/[name].md` - Description
- `assets/[name]` - Description
```

## Frontmatter Standards

### Name Field

**Format**: `hyphen-case` (lowercase letters, digits, hyphens only)

**Valid:**
- `nextjs-fullstack-scaffold`
- `api-contracts-and-zod-validation`
- `form-generator-rhf-zod`

**Invalid:**
- `NextjsScaffold` (PascalCase)
- `nextjs_scaffold` (snake_case)
- `nextjsScaffold` (camelCase)
- `-nextjs-scaffold` (starts with hyphen)
- `nextjs--scaffold` (consecutive hyphens)

### Description Field

**Requirements:**
- Use third-person voice
- Include WHAT the skill does
- Include WHEN to use it
- Include specific trigger terms users would search
- Maximum 1024 characters
- No angle brackets (< or >)

**Format:**
```yaml
description: This skill should be used when [scenarios]. Apply when [cases]. Trigger terms include [keywords, phrases, terms].
```

**Example:**
```yaml
description: This skill should be used when generating React forms with React Hook Form, Zod validation, and shadcn/ui components. Applies when creating entity forms, character editors, location forms, or any form requiring client and server validation. Trigger terms include create form, generate form, React Hook Form, RHF, Zod validation, form component.
```

### allowed-tools Field (Optional)

**When to use**: For read-only or analysis skills that don't modify code

**Format:**
```yaml
allowed-tools: Read, Grep, Glob, Bash
```

**Common combinations:**
- Analysis only: `Read, Grep, Glob, Bash`
- File operations: `Read, Edit, Write, Bash`
- Full access: Omit field entirely

## Instruction Voice Standards

### Imperative/Infinitive Form

**Always use verb-first instructions:**

[OK] **Correct Examples:**
- "To create a form, use the generator script"
- "Generate schemas using Zod"
- "Install dependencies with npm"
- "Configure the database connection"
- "Use the template from assets/form.tsx"
- "Consult references/api-patterns.md for details"

[ERROR] **Incorrect Examples:**
- "You should create forms using the generator"
- "You can generate schemas with Zod"
- "You need to install dependencies"
- "You have to configure the database"
- "You will use the template"
- "You should consult the reference"

### Description Voice

**Use third-person for descriptions:**

[OK] **Correct:**
- "This skill should be used when..."
- "Apply this skill when creating..."
- "Use for generating..."

[ERROR] **Incorrect:**
- "Use this skill when you need to..."
- "You should use this when..."
- "This helps you create..."

## Resource Organization

### scripts/ Directory

**Purpose**: Executable code for deterministic operations

**When to include:**
- Code is repeatedly rewritten in skill usage
- Deterministic operations needed
- Complex logic that benefits from separate execution

**Format:**
- Python: `script_name.py` (executable, #!/usr/bin/env python3)
- Bash: `script_name.sh` (executable, #!/bin/bash)

**Documentation in SKILL.md:**
```markdown
### scripts/generate_form.py

Generates form component from field specification.

Usage:
\`\`\`bash
python scripts/generate_form.py --fields fields.json --output components/forms
\`\`\`
```

### references/ Directory

**Purpose**: Documentation loaded into context as needed

**When to include:**
- Detailed information too long for SKILL.md (>5k words)
- API reference documentation
- Pattern catalogs
- Specification documents

**Format**: Markdown files with descriptive names

**For large files (>10k words):**
Include grep patterns in SKILL.md:
```markdown
Consult `references/api-reference.md` for API details.

To find specific endpoints:
\`\`\`bash
Grep: pattern="GET /api/entities" path="references/api-reference.md"
\`\`\`
```

### assets/ Directory

**Purpose**: Files used in output (not loaded into context)

**When to include:**
- Templates
- Boilerplate code
- Starter files
- Configuration examples

**Format**: Any file type appropriate for the skill

**Reference in SKILL.md:**
```markdown
Use template from `assets/form-template.tsx` as starting point.
```

## Trigger Terms

Include specific terms users would search for:

### Technical Terms
- Framework names: Next.js, React, Vitest, Playwright
- Library names: Zod, React Hook Form, Prisma
- Tool names: ESLint, Prettier, Husky
- Pattern names: Server Actions, RLS, CSP

### Action Terms
- create, generate, build, scaffold, initialize
- setup, configure, install, integrate
- test, validate, check, audit, review
- optimize, improve, refactor, enhance

### Domain Terms (for worldbuilding)
- entity, character, location, item, faction
- relationship, timeline, event, lore
- world, map, narrative, description

### Problem Terms
- error, issue, bug, vulnerability
- performance, slow, bottleneck
- inconsistent, duplicate, broken

## Skill Categories

### development
Code generation, refactoring, debugging, setup, configuration, frameworks, libraries, tooling

### data-modeling
Schemas, types, validation, database design, entity relationships, migrations

### ui-components
React components, styling, responsive design, accessibility, user interface

### documentation
API docs, guides, comments, changelogs, ADRs, PRDs

### testing
Unit tests, integration tests, E2E tests, accessibility tests, coverage, mocks

### utilities
Helpers, formatters, converters, validators, analyzers, auditors

## Quality Checklist

Before finalizing a skill, verify:

- [ ] Name is hyphen-case (lowercase, hyphens only)
- [ ] Description is third-person voice
- [ ] Description includes trigger terms
- [ ] Description explains WHAT and WHEN
- [ ] Description is under 1024 characters
- [ ] Instructions use imperative form (no "you")
- [ ] Section structure is logical
- [ ] Resources are properly referenced
- [ ] Scripts have usage examples
- [ ] Large references include grep patterns
- [ ] Assets are described in context
- [ ] Examples are clear and complete
- [ ] Code follows current best practices
- [ ] Validation passes: `python scripts/quick_validate.py`

## Common Mistakes

### Mistake 1: Second-Person Voice

[ERROR] "You should install the dependencies"
[OK] "Install the dependencies"

[ERROR] "You can use the template"
[OK] "Use the template" or "To use the template"

### Mistake 2: Wrong Name Format

[ERROR] `FormGenerator` (PascalCase)
[OK] `form-generator`

[ERROR] `form_generator` (snake_case)
[OK] `form-generator`

### Mistake 3: Vague Description

[ERROR] "This skill helps with forms and validation stuff."
[OK] "This skill should be used when generating React forms with React Hook Form and Zod validation. Use for creating entity forms, data entry interfaces, or any form requiring validation."

### Mistake 4: Missing Trigger Terms

[ERROR] "This skill generates forms." (no searchable terms)
[OK] "This skill generates React Hook Form components with Zod validation. Trigger terms include create form, generate form, RHF, React Hook Form, Zod validation, form component."

### Mistake 5: Incomplete Resource References

[ERROR] "Use the script to generate forms." (which script?)
[OK] "Use `scripts/generate_form.py` to generate form components."

## Version Guidelines

Keep skills current with latest versions:

### Framework Versions
- Next.js: 15/16 (App Router, Server Components)
- React: 19 (Server Components, Actions)
- TypeScript: 5.x
- Node.js: 20+

### Testing Tools
- Vitest (not Jest)
- React Testing Library
- Playwright
- axe-core for a11y

### Build Tools
- Vite (for fast builds)
- ESM (not CommonJS)
- Modern bundlers

### Deprecated Patterns to Avoid
- Next.js Pages Router (use App Router)
- Jest (use Vitest)
- getServerSideProps (use Server Components)
- API routes for mutations (use Server Actions)
- Class components (use function components)

## Maintenance

### Regular Updates
- Review skills quarterly for outdated patterns
- Update framework versions
- Replace deprecated APIs
- Add new best practices
- Improve trigger terms based on usage

### Validation
Run validation regularly:
```bash
python scripts/quick_validate.py skills/[category]/[skill-name]
```

### Quality Audits
Use skill-reviewer-and-enhancer to audit:
```bash
# Trigger the skill
"Review and enhance the [skill-name] skill"
```

## References

- Official Anthropic skill-creator skill
- Claude Code documentation
- Community best practices
- Framework official documentation
