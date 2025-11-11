# Implementation Checklist

Complete checklist for scaffolding a Next.js full-stack application.

## Phase 1: Project Setup

### Configuration Files
- [ ] `package.json` - Dependencies and scripts
- [ ] `tsconfig.json` - TypeScript configuration
- [ ] `next.config.ts` - Next.js configuration
- [ ] `tailwind.config.ts` - Tailwind CSS + shadcn/ui
- [ ] `postcss.config.mjs` - PostCSS configuration
- [ ] `eslint.config.mjs` - ESLint v9 flat config
- [ ] `prettier.config.js` - Prettier configuration
- [ ] `.gitignore` - Git ignore patterns
- [ ] `.env.example` - Environment variables template
- [ ] `README.md` - Setup instructions

### Testing Configuration
- [ ] `vitest.config.ts` - Vitest configuration
- [ ] `playwright.config.ts` - Playwright configuration
- [ ] Set up test directories (`tests/unit`, `tests/integration`, `tests/e2e`)

### Git Hooks
- [ ] Initialize Husky (`npx husky init`)
- [ ] Add pre-commit hook for lint-staged
- [ ] Configure lint-staged in package.json

## Phase 2: Folder Structure

### App Router Structure
- [ ] `app/layout.tsx` - Root layout
- [ ] `app/page.tsx` - Home page
- [ ] `app/globals.css` - Global styles with Tailwind
- [ ] `app/(auth)/login/page.tsx` - Login page
- [ ] `app/(auth)/layout.tsx` - Auth layout
- [ ] `app/(protected)/dashboard/page.tsx` - Dashboard
- [ ] `app/(protected)/profile/page.tsx` - User profile
- [ ] `app/(protected)/data/page.tsx` - Data table page
- [ ] `app/(protected)/layout.tsx` - Protected layout
- [ ] `app/api/data/route.ts` - Example API route
- [ ] `middleware.ts` - Auth middleware

### Components
- [ ] `components/providers.tsx` - App providers (Toaster, etc.)
- [ ] `components/layout/header.tsx` - Header component
- [ ] `components/layout/sidebar.tsx` - Sidebar component
- [ ] `components/layout/nav.tsx` - Navigation component
- [ ] `components/auth/login-form.tsx` - Login form with RHF + Zod
- [ ] `components/auth/auth-button.tsx` - Login/logout button
- [ ] `components/dashboard/stats-card.tsx` - Stats card component
- [ ] `components/dashboard/data-table.tsx` - Data table component

### shadcn/ui Components
- [ ] `components/ui/button.tsx`
- [ ] `components/ui/card.tsx`
- [ ] `components/ui/input.tsx`
- [ ] `components/ui/label.tsx`
- [ ] `components/ui/form.tsx`
- [ ] `components/ui/table.tsx`
- [ ] `components/ui/dropdown-menu.tsx`
- [ ] `components/ui/avatar.tsx`

### Lib Files
- [ ] `lib/utils.ts` - Utility functions (cn, etc.)
- [ ] `lib/prisma.ts` - Prisma client singleton
- [ ] `lib/supabase/client.ts` - Supabase client for client components
- [ ] `lib/supabase/server.ts` - Supabase client for server components
- [ ] `lib/supabase/middleware.ts` - Supabase middleware helper
- [ ] `lib/actions/auth.ts` - Auth server actions
- [ ] `lib/actions/user.ts` - User server actions
- [ ] `lib/actions/data.ts` - Data server actions
- [ ] `lib/validations/auth.ts` - Auth validation schemas
- [ ] `lib/validations/user.ts` - User validation schemas
- [ ] `lib/validations/data.ts` - Data validation schemas

### Database
- [ ] `prisma/schema.prisma` - Prisma schema
- [ ] `prisma/seed.ts` - Database seed script

## Phase 3: Core Features

### Authentication
- [ ] Supabase auth setup (server + client)
- [ ] Login form with email/password
- [ ] Server action for sign in
- [ ] Server action for sign out
- [ ] Middleware for protected routes
- [ ] Auth state management
- [ ] Redirect logic after login/logout

### Protected Routes
- [ ] Dashboard page with data fetching
- [ ] Profile page with user info
- [ ] Data table page with CRUD operations
- [ ] Server actions for mutations
- [ ] Form validation with Zod
- [ ] Toast notifications on success/error

### UI Components
- [ ] Responsive layout with header/sidebar
- [ ] Dark mode toggle (optional)
- [ ] Loading states with Suspense
- [ ] Error boundaries
- [ ] Accessible forms with shadcn/ui

### Database Integration
- [ ] Prisma schema with User model
- [ ] Prisma schema with example data model
- [ ] Database migrations
- [ ] Seed script with sample data
- [ ] Prisma client queries in server components
- [ ] Server actions with database mutations

## Phase 4: Testing

### Unit Tests
- [ ] `tests/unit/utils.test.ts` - Test utility functions
- [ ] Test Zod validation schemas
- [ ] Test helper functions

### Integration Tests
- [ ] `tests/integration/auth.test.tsx` - Test auth components
- [ ] Test form submissions
- [ ] Test server actions

### E2E Tests
- [ ] `tests/e2e/login.spec.ts` - Test login flow
- [ ] Test protected route access
- [ ] Test form submission flows
- [ ] Test navigation

## Phase 5: CI/CD

### GitHub Actions
- [ ] `.github/workflows/ci.yml` - CI workflow
- [ ] Run linting
- [ ] Run type checking
- [ ] Run tests
- [ ] Run build
- [ ] Set up Vercel deployment (optional)

## Phase 6: Documentation

### README Sections
- [ ] Project overview
- [ ] Tech stack list
- [ ] Prerequisites
- [ ] Installation steps
- [ ] Environment variable setup
- [ ] Database setup (Prisma)
- [ ] Supabase setup instructions
- [ ] Running locally
- [ ] Testing commands
- [ ] Deployment instructions
- [ ] Folder structure explanation
- [ ] Contributing guidelines (optional)

## Verification Steps

After scaffolding, verify:

1. **Dependencies Install**: `npm install` completes without errors
2. **Type Checking**: `npx tsc --noEmit` passes
3. **Linting**: `npm run lint` passes
4. **Formatting**: `npm run format:check` passes
5. **Build**: `npm run build` succeeds
6. **Tests**: `npm test` passes
7. **E2E Tests**: `npm run test:e2e` passes (with test environment)
8. **Dev Server**: `npm run dev` starts successfully
9. **Prisma**: `npx prisma generate` works
10. **Git Hooks**: Commit triggers lint-staged

## Common Issues & Solutions

### Issue: Prisma client not generated
**Solution**: Run `npx prisma generate` after schema changes

### Issue: Supabase auth not working
**Solution**: Check environment variables and cookie configuration

### Issue: ESLint errors
**Solution**: Run `npm run lint -- --fix` to auto-fix

### Issue: Type errors
**Solution**: Ensure all dependencies are installed and Prisma is generated

### Issue: Build fails
**Solution**: Check for missing environment variables and type errors

### Issue: Tests fail
**Solution**: Ensure test environment is properly configured in vitest.config.ts

## Post-Scaffold Tasks

After completing the scaffold:

1. **Environment Setup**: Copy `.env.example` to `.env` and fill in values
2. **Supabase Project**: Create Supabase project and get credentials
3. **Database Schema**: Run `npx prisma db push` to sync schema
4. **Seed Data**: Run `npm run db:seed` to populate sample data
5. **Install shadcn/ui**: Run initialization commands for components
6. **Git Init**: Initialize git repository and make first commit
7. **Deploy**: Connect to Vercel and deploy
8. **Test**: Verify all features work in production

## Optional Enhancements

Consider adding these after the base scaffold:

- [ ] Email verification flow
- [ ] Password reset flow
- [ ] User roles and permissions
- [ ] Multi-factor authentication
- [ ] File upload with Supabase Storage
- [ ] Real-time subscriptions
- [ ] Advanced data table features (export, filters)
- [ ] User preferences/settings page
- [ ] Activity logs/audit trail
- [ ] API documentation
- [ ] Storybook for components
- [ ] Performance monitoring
- [ ] Error tracking (Sentry)
- [ ] Analytics integration
