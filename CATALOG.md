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

### tailwind-shadcn-ui-setup

**Location**: `skills/development/tailwind-shadcn-ui-setup/`
**Type**: Workflow-Based
**Description**: Configures production-ready Tailwind CSS (v3/v4) and shadcn/ui for Next.js 16 App Router projects. Automates dependency installation, generates base layouts with dark mode support, implements design token system with CSS variables, ensures WCAG 2.1 AA accessibility compliance, and provides example pages. Includes responsive header/sidebar navigation, theme provider, and comprehensive component library setup.

**Trigger Terms**: setup tailwind, configure shadcn/ui, add dark mode, initialize design system, setup UI framework, tailwind configuration, shadcn setup, design tokens, theme setup, UI library setup

**Resources**:
- scripts/setup_tailwind_shadcn.py - Automation script for dependency installation and configuration
- references/tailwind-v4-migration.md - Tailwind v3 vs v4 migration guide and patterns
- references/shadcn-component-list.md - Complete shadcn/ui component catalog with usage examples
- references/accessibility-checklist.md - WCAG 2.1 AA compliance guidelines and best practices
- references/theme-tokens.md - Design token system documentation and customization guide
- assets/tailwind.config.ts.template - Tailwind configuration with semantic color tokens
- assets/globals.css.template - Global styles with CSS variables and theme presets
- assets/components/* - Theme provider, mode toggle, and app shell components
- assets/app/examples/* - Example pages for forms, dialogs, and theme showcase

**Example Usage**:
> "Setup Tailwind CSS and shadcn/ui for my Next.js project"
> "Configure dark mode with design tokens"
> "Initialize a UI framework with accessible components"
> "Add Tailwind and shadcn to my Next.js app"

### supabase-rls-policy-generator

**Location**: `skills/development/supabase-rls-policy-generator/`
**Type**: Workflow-Based
**Description**: Generates comprehensive Row-Level Security (RLS) policies for Supabase databases in multi-tenant or role-based applications. Creates policies using auth.uid(), auth.jwt() claims, and role-based access patterns with helper functions, testing queries, and migration files. Includes templates for common patterns like user ownership, tenant isolation, and hierarchical permissions.

**Trigger Terms**: RLS, row level security, supabase security, generate policies, auth policies, multi-tenant security, role-based access, database security policies, supabase permissions, tenant isolation

**Resources**:
- references/rls-patterns.md - Common RLS patterns including RBAC, multi-tenant, and hierarchical permissions
- references/supabase-auth.md - Supabase auth functions and JWT structure reference
- assets/policy-templates.sql - Ready-to-use SQL templates for common RLS patterns
- assets/policy-documentation-template.md - Template for documenting generated policies

**Example Usage**:
> "Generate RLS policies for my Supabase database"
> "Create multi-tenant security policies"
> "Add row level security for role-based access"
> "Generate Supabase auth policies"

### auth-route-protection-checker

**Location**: `skills/development/auth-route-protection-checker/`
**Type**: Analysis + Code Generation
**Description**: Audits and generates authentication and authorization protection for Next.js routes, server components, API routes, and server actions. Analyzes existing routes for missing auth checks, categorizes routes by protection level, and generates protection logic based on user roles and permissions. Creates comprehensive audit reports with prioritized security gaps.

**Trigger Terms**: auth check, route protection, protect routes, secure endpoints, auth middleware, role-based routes, authorization check, api security, server action security, protect pages

**Resources**:
- references/protection-patterns.md - Authentication patterns for Next.js App Router
- references/security-best-practices.md - Security guidelines and recommendations
- assets/auth-helpers.ts - Reusable authentication utility functions
- assets/auth-tests.ts - Test templates for auth protection

**Example Usage**:
> "Check which routes need authentication"
> "Audit my Next.js app for auth protection"
> "Generate auth middleware for API routes"
> "Find unprotected endpoints in my app"

### security-hardening-checklist

**Location**: `skills/development/security-hardening-checklist/`
**Type**: Analysis + Report Generation
**Description**: Performs comprehensive security audit analyzing security headers, cookie configuration, RLS policies, input sanitization, rate limiting, environment variables, HTTPS enforcement, and CORS configuration. Generates detailed security report with prioritized issues, actionable recommendations, and fix scripts. Checks against OWASP Top 10 vulnerabilities.

**Trigger Terms**: security audit, security check, harden security, security review, vulnerability check, security headers, secure cookies, input validation, rate limiting, security best practices

**Resources**:
- references/security-headers.md - Complete security headers configuration guide
- references/rls-checklist.md - Database security checklist
- references/owasp-top-10.md - OWASP Top 10 vulnerabilities reference
- assets/security-report-template.md - Template for security audit reports

**Example Usage**:
> "Audit my app security"
> "Check for security vulnerabilities"
> "Generate security hardening report"
> "Review security headers and cookies"

### csp-config-generator

**Location**: `skills/development/csp-config-generator/`
**Type**: Analysis + Code Generation
**Description**: Generates strict Content Security Policy (CSP) headers for Next.js applications to prevent XSS attacks and control resource loading. Analyzes application to determine appropriate CSP directives, implements nonce-based or hash-based strategies, and generates configuration via next.config or middleware. Includes CSP violation reporting and testing suite.

**Trigger Terms**: CSP, Content Security Policy, security headers, XSS protection, generate CSP, configure CSP, strict CSP, nonce-based CSP, CSP directives

**Resources**:
- references/csp-directives.md - Complete CSP directive documentation
- references/csp-best-practices.md - CSP security guidelines
- assets/csp-config-template.ts - CSP configuration templates
- assets/csp-documentation-template.md - Template for CSP documentation

**Example Usage**:
> "Generate CSP configuration for Next.js"
> "Add Content Security Policy headers"
> "Configure strict CSP with nonce"
> "Setup XSS protection with CSP"

### api-contracts-and-zod-validation

**Location**: `skills/development/api-contracts-and-zod-validation/`
**Type**: Workflow-Based + Code Generation
**Description**: Generate Zod schemas and TypeScript types for forms, API routes, and Server Actions with runtime validation. Validate inputs in Server Actions or route handlers with runtime type checking. Automates TypeScript-to-Zod conversion, provides common validation patterns, and includes templates for forms, API routes, Server Actions, and entity schemas.

**Trigger Terms**: zod, schema, validation, API contract, form validation, type inference, runtime validation, parse, safeParse, input validation, request validation, Server Action validation

**Resources**:
- scripts/generate_zod_schema.py - Automated TypeScript-to-Zod schema generator
- references/zod_patterns.md - Common Zod validation patterns and best practices
- assets/schema_templates/form_schema_template.ts - Form validation template
- assets/schema_templates/server_action_schema_template.ts - Server Action validation template
- assets/schema_templates/api_route_schema_template.ts - API route validation template
- assets/schema_templates/entity_schema_template.ts - Entity validation schemas for worldbuilding

**Example Usage**:
> "Generate Zod schemas for my entity forms"
> "Add validation to Server Actions"
> "Create API contract with Zod for my routes"
> "Validate form inputs with Zod and TypeScript"

### server-actions-vs-api-optimizer

**Location**: `skills/development/server-actions-vs-api-optimizer/`
**Type**: Analysis + Recommendation
**Description**: Analyze routes and recommend whether to use Server Actions or API routes based on use case patterns including authentication, revalidation, external API calls, and client requirements. Provides automated route analysis, comprehensive decision matrix, migration plans, and real-world pattern examples.

**Trigger Terms**: Server Actions, API routes, route handler, data mutation, revalidation, authentication flow, external API, client-side fetch, route optimization, Next.js patterns

**Resources**:
- scripts/analyze_routes.py - Automated route analysis tool with recommendations
- references/decision_matrix.md - Comprehensive decision criteria for Server Actions vs API routes

**Example Usage**:
> "Should I use Server Actions or API routes for this endpoint?"
> "Analyze my routes and recommend optimizations"
> "When should I use Server Actions vs API routes?"
> "Review my Next.js routes for best practices"

### env-config-validator

**Location**: `skills/development/env-config-validator/`
**Type**: Analysis + Validation
**Description**: Validate environment configuration files across local, staging, and production environments. Ensure required secrets, database URLs, API keys, and public variables are properly scoped and set. Detects security issues, weak values, naming violations, and cross-environment inconsistencies.

**Trigger Terms**: env, environment variables, secrets, configuration, .env file, environment validation, missing variables, config check, NEXT_PUBLIC, env vars, database URL, API keys

**Resources**:
- scripts/validate_env.py - Python script to validate environment files with security checks
- references/env_best_practices.md - Comprehensive environment variable management guide
- assets/.env.example - Template for required environment variables

**Example Usage**:
> "Validate my .env file for security issues"
> "Check for missing environment variables"
> "Compare .env.local and .env.production"
> "Audit environment configuration"

---

## Data Modeling

*Skills for entity schemas, relationships, validation, and data transformation.*

(Skills will be added here as they're created)

---

## UI Components

*Skills for React components, styling patterns, and responsive design.*

### form-generator-rhf-zod

**Location**: `skills/ui-components/form-generator-rhf-zod/`
**Type**: Workflow-Based
**Description**: Generates production-ready React forms using React Hook Form, Zod validation schemas, and accessible shadcn/ui form controls. Creates forms with client-side and server-side validation, proper TypeScript types, consistent error handling, and ARIA attributes. Supports complex field types, conditional logic, array fields, and file uploads.

**Trigger Terms**: create form, generate form, build form, React Hook Form, RHF, Zod validation, form component, entity form, character form, data entry, form schema, form validation, accessible forms, form builder

**Resources**:
- scripts/generate_form.py - Generates form component, Zod schema, and server action
- scripts/generate_zod_schema.py - Converts field specifications to Zod schema
- references/rhf-patterns.md - React Hook Form patterns, hooks, and best practices
- references/zod-validation.md - Zod schema patterns, refinements, and custom validators
- references/shadcn-form-controls.md - shadcn/ui form component usage and examples
- references/server-actions.md - Server action patterns for form submission
- assets/form-template.tsx - Base form component template with RHF setup
- assets/field-templates/ - Individual field component templates
- assets/validation-schemas.ts - Common Zod validation patterns
- assets/form-utils.ts - Form utility functions

**Example Usage**:
> "Create a character creation form with React Hook Form and Zod"
> "Generate a location form with validation"
> "Build an entity form with client and server validation"

### ui-library-usage-auditor

**Location**: `skills/ui-components/ui-library-usage-auditor/`
**Type**: Task-Based
**Description**: Reviews and audits shadcn/ui component usage across the codebase to ensure accessibility, consistency, and maintainable UI patterns. Identifies accessibility violations, inconsistent patterns, component extraction opportunities, and layout issues. Generates comprehensive audit reports with prioritized recommendations and concrete fixes.

**Trigger Terms**: audit UI, review components, check shadcn, accessibility audit, component review, UI patterns, design system compliance, layout review, refactor components, extract component, consistency check, a11y review, code quality audit

**Resources**:
- references/audit-checklist.md - Comprehensive audit checklist for all categories

**Example Usage**:
> "Audit shadcn/ui usage for accessibility issues"
> "Review components for consistency and extract common patterns"
> "Check UI components for accessibility compliance"
> "Identify component extraction opportunities"

### markdown-editor-integrator

**Location**: `skills/ui-components/markdown-editor-integrator/`
**Type**: Workflow-Based
**Description**: Installs and configures @uiw/react-md-editor with theme integration, server-side sanitization, and controlled/uncontrolled modes for rich text editing in worldbuilding content. Provides editor with live preview, toolbar customization, automatic theme switching, XSS protection, and persistence patterns for drafts and auto-save.

**Trigger Terms**: markdown editor, rich text editor, text editor, add markdown, install markdown editor, markdown component, WYSIWYG, content editor, text formatting, editor preview, markdown support, rich text editing

**Resources**:
- references/theme-integration.md - Detailed theming guide for shadcn/ui integration
- references/sanitization.md - Security best practices and XSS protection
- assets/MarkdownEditor.tsx - Complete editor component with theme support
- assets/MarkdownPreview.tsx - Preview component for displaying markdown

**Example Usage**:
> "Add markdown editor to character biography form"
> "Install markdown editing with preview for location descriptions"
> "Setup rich text editor with theme support"
> "Configure markdown editor for content management"

---

## Documentation

*Skills for API documentation, user guides, and inline comments.*

(Skills will be added here as they're created)

---

## Testing

*Skills for test generation, coverage analysis, and test utilities.*

### testing-next-stack

**Location**: `skills/testing/testing-next-stack/`
**Type**: Workflow-Based
**Description**: Scaffolds comprehensive testing setup for Next.js applications including Vitest unit tests, React Testing Library component tests, and Playwright E2E flows with accessibility testing via axe-core. Generates configuration files, test utilities, example tests, and establishes testing best practices for worldbuilding app features.

**Trigger Terms**: setup testing, scaffold tests, vitest, RTL, playwright, e2e tests, component tests, unit tests, accessibility testing, a11y tests, axe-core, test configuration, testing infrastructure, test setup

**Resources**:
- scripts/generate_test_deps.py - Generate package.json dependencies for testing stack
- references/vitest-setup.md - Vitest configuration details and patterns
- references/rtl-patterns.md - React Testing Library best practices
- references/playwright-setup.md - Playwright configuration guide
- references/a11y-testing.md - Accessibility testing guidelines with axe-core
- assets/vitest.config.ts - Vitest configuration template with coverage
- assets/playwright.config.ts - Playwright configuration for multiple browsers
- assets/test-setup.ts - Test setup with mocks and global utilities
- assets/examples/unit-test.ts - Unit test example with async patterns
- assets/examples/component-test.tsx - Component test with RTL and a11y checks
- assets/examples/e2e-test.ts - E2E test with Playwright and accessibility scanning

**Example Usage**:
> "Setup testing infrastructure for my Next.js project"
> "Add Vitest and Playwright to my app with accessibility tests"
> "Configure testing with RTL and axe-core"
> "Generate test utilities and example tests"

### playwright-flow-recorder

**Location**: `skills/testing/playwright-flow-recorder/`
**Type**: Task-Based
**Description**: Creates Playwright test scripts from natural language user flow descriptions. Translates scenarios like "user signs up and creates project" into executable E2E tests with proper selectors, assertions, and error handling. Supports various input formats including simple descriptions, numbered steps, and Given/When/Then acceptance criteria.

**Trigger Terms**: playwright test, e2e flow, user scenario, test from description, record flow, user journey, test script generation, acceptance test, behavior test, user story test, scenario to test, flow to code

**Resources**:
- scripts/generate_flow_test.py - Parse natural language and generate Playwright tests
- scripts/parse_flow.py - Flow description parser with action extraction
- scripts/generate_fixtures.py - Test data generator for entities and relationships
- references/playwright-actions.md - Complete mapping of actions to Playwright code
- references/auth-patterns.md - Authentication patterns for protected flows
- references/selectors.md - Selector best practices and strategies
- assets/test-template.ts - Base Playwright test template structure
- assets/action-templates/ - Code templates for different action types

**Example Usage**:
> "Generate a Playwright test from: user signs up and creates project"
> "Create E2E test for entity creation flow"
> "Convert this acceptance criteria to Playwright tests"
> "Generate test script from user journey description"

### a11y-checker-ci

**Location**: `skills/testing/a11y-checker-ci/`
**Type**: Workflow-Based
**Description**: Adds comprehensive accessibility testing to CI/CD pipelines using axe-core Playwright integration or pa11y-ci. Automatically generates markdown reports for pull requests showing WCAG violations with severity levels, affected elements, and remediation guidance. Configures quality gates, tracks metrics over time, and enforces accessibility standards.

**Trigger Terms**: a11y ci, accessibility pipeline, wcag ci, axe-core ci, pa11y ci, accessibility reports, a11y automation, accessibility gate, compliance check, accessibility testing ci, wcag automation, a11y pr reports

**Resources**:
- scripts/generate_a11y_report.py - Generate markdown reports from axe-core results
- scripts/save_a11y_results.py - Store historical accessibility data
- scripts/generate_trend_report.py - Generate trend analysis from historical data
- references/wcag-criteria.md - WCAG standards reference guide
- references/common-violations.md - Common accessibility issues and fixes
- assets/a11y-test.spec.ts - Playwright accessibility test template
- assets/pa11y-config.json - pa11y-ci configuration template
- assets/github-actions-a11y.yml - GitHub Actions workflow with PR comments
- assets/gitlab-ci-a11y.yml - GitLab CI configuration
- assets/a11y-thresholds.json - Violation thresholds configuration
- assets/report-templates/ - Report templates for different platforms

**Example Usage**:
> "Add accessibility testing to GitHub Actions"
> "Setup a11y checks in CI with PR reports"
> "Configure WCAG compliance testing for pull requests"
> "Generate accessibility reports with axe-core"

---

## Utilities

*Skills for general-purpose tools, formatters, and development helpers.*

### skill-reviewer-and-enhancer

**Location**: `skills/utilities/skill-reviewer-and-enhancer/`
**Type**: Task-Based
**Description**: Reviews, audits, and enhances existing Claude Code skills to ensure they follow Anthropic best practices and current domain-specific patterns. Analyzes skill structure, validates frontmatter, checks instruction style for imperative form, verifies domain best practices (Next.js, testing, UI, security, etc.), identifies missing resources, and automatically applies improvements. Generates comprehensive review reports with prioritized issues and actionable recommendations.

**Trigger Terms**: review skill, audit skill, improve skill, enhance skill, update skill, check skill quality, skill best practices, fix skill, optimize skill, validate skill structure, skill compliance, modernize skill, skill analysis

**Resources**:
- scripts/analyze_skill_structure.py - Automated skill structure validation and analysis
- references/anthropic-skill-standards.md - Official Anthropic skill creation standards
- references/nextjs-best-practices.md - Next.js 15/16 patterns for skill review
- references/testing-best-practices.md - Modern testing patterns with Vitest and Playwright
- references/ui-best-practices.md - shadcn/ui and accessibility guidelines
- references/database-best-practices.md - Prisma and Supabase patterns
- references/security-best-practices.md - OWASP and security standards
- assets/review-report-template.md - Comprehensive skill review report template

**Example Usage**:
> "Review the nextjs-fullstack-scaffold skill for best practices"
> "Audit this skill and enhance it to follow Anthropic standards"
> "Check if the testing-next-stack skill uses current patterns"
> "Improve this skill and update to latest framework versions"

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

### github-actions-ci-workflow

**Location**: `skills/development/github-actions-ci-workflow/`
**Type**: Workflow-Based
**Description**: Sets up comprehensive GitHub Actions CI/CD workflows for modern web applications including automated lint, test, build, and deploy pipelines with preview URL comments on pull requests and optimized caching strategies.

**Trigger Terms**: github actions, ci/cd, continuous integration, deployment automation, workflow setup, preview deployment, ci pipeline, automated deployment

**Resources**:
- scripts/generate_ci_workflow.py - Scaffolds workflow files based on project configuration
- references/github-actions-best-practices.md - Workflow optimization and security best practices
- assets/workflow-templates/nextjs-ci.yml - Next.js CI workflow template

**Example Usage**:
> "Setup GitHub Actions CI/CD for my Next.js project"
> "Add preview deployments with URL comments on PRs"

### docs-and-changelogs

**Location**: `skills/documentation/docs-and-changelogs/`
**Type**: Workflow-Based
**Description**: Generates comprehensive changelogs from Conventional Commits, maintains CHANGELOG.md files, and scaffolds project documentation like PRD.md or ADR.md for architectural decisions and product requirements.

**Trigger Terms**: changelog, release notes, conventional commits, ADR, PRD, architectural decision, product requirements, version documentation

**Resources**:
- scripts/generate_changelog.py - Generates changelogs from git commit history
- scripts/create_adr.py - Creates architectural decision records
- scripts/create_prd.py - Scaffolds product requirement documents

**Example Usage**:
> "Generate changelog from commits since last release"
> "Create ADR for database choice"
> "Scaffold PRD for timeline feature"

### feature-flag-manager

**Location**: `skills/development/feature-flag-manager/`
**Type**: Workflow-Based
**Description**: Adds feature flag support using LaunchDarkly or JSON-based configuration to toggle features in UI components and Server Actions for progressive rollouts and A/B testing.

**Trigger Terms**: feature flags, feature toggles, launchdarkly, progressive rollout, a/b testing, canary release, feature gating

**Resources**:
- assets/feature-flag-provider.tsx - JSON-based feature flag provider implementation

**Example Usage**:
> "Add feature flags for the new timeline view"
> "Implement progressive rollout with LaunchDarkly"

### revalidation-strategy-planner

**Location**: `skills/development/revalidation-strategy-planner/`
**Type**: Task-Based
**Description**: Evaluates Next.js routes and outputs optimal revalidate settings, cache tags for ISR, SSR configurations, or streaming patterns to optimize caching strategies and data freshness.

**Trigger Terms**: revalidation, next.js caching, isr, cache tags, ssr strategy, on-demand revalidation, rendering strategy

**Resources**:
- scripts/analyze_routes.py - Analyzes routes and recommends caching strategies

**Example Usage**:
> "Analyze my routes and recommend revalidation strategies"
> "Configure ISR for entity detail pages"

### performance-budget-enforcer

**Location**: `skills/development/performance-budget-enforcer/`
**Type**: Workflow-Based
**Description**: Monitors Lighthouse scores and JavaScript bundle sizes across deployments with automated alerts when performance thresholds are exceeded to prevent performance regressions.

**Trigger Terms**: performance budget, bundle size, lighthouse ci, performance monitoring, web vitals, performance regression, lighthouse scores

**Resources**:
- (Reference and asset files to be added as needed)

**Example Usage**:
> "Setup performance budgets with Lighthouse CI"
> "Monitor bundle size and alert on increases"

### role-permission-table-builder

**Location**: `skills/development/role-permission-table-builder/`
**Type**: Task-Based
**Description**: Generates comprehensive role-based permission matrices in markdown or SQL format for pages, components, and data access patterns to design and document authorization systems.

**Trigger Terms**: rbac, role permissions, access control, authorization, permission matrix, role-based access, security policy

**Resources**:
- (Reference and asset files to be added as needed)

**Example Usage**:
> "Generate RBAC permission matrix for worldbuilding app"
> "Create SQL schema for role-based permissions"

### eslint-prettier-husky-config

**Location**: `skills/development/eslint-prettier-husky-config/`
**Type**: Workflow-Based
**Description**: Configures code quality tooling with ESLint v9 flat config, Prettier formatting, Husky git hooks, lint-staged pre-commit checks, and GitHub Actions CI lint workflow for Next.js/React projects. Automates dependency installation, creates ESLint flat config with React/TypeScript rules, sets up Prettier with ignore patterns, configures Husky pre-commit hooks, adds package.json scripts, and generates CI workflow for automated lint checks.

**Trigger Terms**: eslint, prettier, husky, lint-staged, code quality, linting setup, format code, pre-commit hooks, git hooks, lint ci, eslint v9, flat config, code formatting, quality gates

**Resources**:
- references/package-json-config.md - Complete package.json example with scripts and lint-staged configuration
- references/team-documentation.md - Template for documenting the setup for team members
- assets/eslint.config.mjs - ESLint v9 flat config template with React, TypeScript, and Next.js support
- assets/.prettierrc - Prettier configuration with recommended settings
- assets/.prettierignore - Files and directories to exclude from formatting
- assets/github-workflows-lint.yml - GitHub Actions workflow for automated lint checks

**Example Usage**:
> "Setup ESLint and Prettier for my Next.js project"
> "Add pre-commit hooks with Husky and lint-staged"
> "Configure code quality tooling with ESLint v9"
> "Setup lint checks in GitHub Actions CI"

### supabase-auth-ssr-setup

**Location**: `skills/development/supabase-auth-ssr-setup/`
**Type**: Workflow-Based
**Description**: Configures Supabase Authentication for Next.js App Router with server-side rendering, including secure cookie-based sessions, middleware protection, route guards, authentication utilities, and complete login/logout flows. Creates browser, server, and middleware Supabase client configurations, implements route protection middleware, provides auth helper functions, and includes example login page and protected dashboard.

**Trigger Terms**: supabase auth, ssr authentication, supabase ssr, next.js auth, server-side auth, auth middleware, protected routes, login flow, logout, supabase cookies, session management, route protection, auth guards

**Resources**:
- references/authentication-patterns.md - Common auth patterns and best practices for Next.js + Supabase
- references/security-considerations.md - Security best practices for session handling and cookie configuration
- assets/supabase-client.ts - Browser-side Supabase client configuration
- assets/supabase-server.ts - Server-side Supabase client for Server Components
- assets/supabase-middleware.ts - Middleware Supabase client for session refresh
- assets/middleware.ts - Next.js middleware for route protection
- assets/auth-utils.ts - Helper functions for authentication checks
- assets/auth-actions.ts - Server Actions for logout and other auth operations
- assets/login-page.tsx - Complete login page with email/password and OAuth
- assets/dashboard-page.tsx - Example protected page using requireAuth
- assets/auth-callback-route.ts - OAuth callback handler for provider authentication

**Example Usage**:
> "Setup Supabase authentication with SSR for Next.js"
> "Configure auth middleware and protected routes"
> "Add Supabase login flow with secure cookies"
> "Implement server-side authentication with Supabase"

### supabase-prisma-database-management

**Location**: `skills/development/supabase-prisma-database-management/`
**Type**: Workflow-Based
**Description**: Manages database schema, migrations, and seed data using Prisma ORM with Supabase PostgreSQL. Configures Prisma with Supabase connection strings (direct and pooled), shadow database for migration preview, provides example schema with common patterns, creates idempotent seed scripts, and adds CI workflow for schema validation and migration checks.

**Trigger Terms**: prisma, supabase database, database schema, migrations, prisma schema, database management, seed data, prisma migrate, prisma client, orm, database migrations, schema management, shadow database

**Resources**:
- references/prisma-best-practices.md - Comprehensive guide to Prisma patterns, performance optimization, and common pitfalls
- references/supabase-integration.md - Specific considerations for using Prisma with Supabase, including RLS integration
- assets/example-schema.prisma - Complete schema example with common patterns (auth, timestamps, relations, indexes)
- assets/seed.ts - Idempotent seed script template for initial data
- assets/prisma-client.ts - Singleton Prisma Client for Next.js to prevent connection exhaustion
- assets/github-workflows-schema-check.yml - CI workflow for schema validation and migration checks

**Example Usage**:
> "Setup Prisma with Supabase for my Next.js app"
> "Create database schema and migrations with Prisma"
> "Configure Prisma ORM with Supabase PostgreSQL"
> "Generate Prisma client and seed database"

### sentry-and-otel-setup

**Location**: `skills/development/sentry-and-otel-setup/`
**Type**: Workflow-Based
**Description**: Adds comprehensive error tracking and performance monitoring using Sentry with OpenTelemetry instrumentation for Next.js applications. Configures Sentry for server, client, and edge runtimes, sets up automatic error capture, implements distributed tracing, creates structured logging wrapper, adds error boundaries, and provides custom error pages.

**Trigger Terms**: sentry, error tracking, opentelemetry, otel, performance monitoring, error monitoring, tracing, logging, error boundaries, sentry setup, observability, error capture, performance tracing

**Resources**:
- references/sentry-best-practices.md - Error handling patterns, performance monitoring strategies, and quota management
- references/otel-integration.md - OpenTelemetry concepts, custom instrumentation, and distributed tracing setup
- assets/sentry-server-config.ts - Server-side Sentry configuration with tracing and sampling
- assets/sentry-client-config.ts - Client-side Sentry configuration with replay and error boundaries
- assets/instrumentation.ts - OpenTelemetry initialization and Sentry integration
- assets/logger.ts - Structured logging wrapper with Sentry integration
- assets/error-boundary.tsx - React error boundary component for client-side error handling
- assets/error-page.tsx - Custom error page for Server Component errors
- assets/global-error.tsx - Global error handler for root layout errors

**Example Usage**:
> "Setup Sentry error tracking for my Next.js app"
> "Add OpenTelemetry tracing to Server Actions"
> "Configure error monitoring with Sentry and OTel"
> "Implement performance monitoring and error capture"

