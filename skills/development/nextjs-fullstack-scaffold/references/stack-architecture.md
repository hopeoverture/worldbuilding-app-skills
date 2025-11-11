# Stack Architecture Reference

## Technology Stack

### Core Framework
- **Next.js 16** (App Router) - React framework with built-in routing, server components, and API routes
- **React 19** - UI library with Server Components support
- **TypeScript** - Type safety across the entire stack

### Styling
- **Tailwind CSS v4** - Utility-first CSS framework
- **shadcn/ui** - Accessible component system built on Radix UI
- **CSS Variables** - For theming and dark mode support

### Backend & Database
- **Supabase** - Auth provider + PostgreSQL hosting
- **Prisma ORM** - Type-safe database client
- **Server Actions** - Next.js server-side mutations

### Forms & Validation
- **React Hook Form** - Performant form management
- **Zod** - Runtime type validation and schema definition
- **@hookform/resolvers** - Bridge between RHF and Zod

### Developer Experience
- **ESLint v9** - Code linting with flat config
- **Prettier** - Code formatting
- **Husky** - Git hooks for pre-commit checks
- **lint-staged** - Run linters on staged files only

### Testing
- **Vitest** - Unit test runner
- **React Testing Library** - Component testing
- **Playwright** - E2E browser testing

### Utilities
- **Sonner** - Toast notifications
- **lucide-react** - Icon library
- **clsx + tailwind-merge** - Conditional CSS class utilities

## Architecture Patterns

### App Router Structure

#### Route Groups
Use route groups to organize routes without affecting URL structure:

```
app/
  (auth)/          # Public authentication routes
    login/
    signup/
  (protected)/     # Protected routes requiring authentication
    dashboard/
    profile/
    settings/
```

#### Layouts
- Root layout (`app/layout.tsx`) - Wraps entire app
- Group layouts - Shared UI for route groups
- Nested layouts - Inherited down the tree

### Server vs Client Components

#### Server Components (Default)
- Data fetching
- Database queries
- Server-side logic
- No interactivity needed

#### Client Components (`"use client"`)
- Interactivity (onClick, onChange, etc.)
- React hooks (useState, useEffect, etc.)
- Browser APIs
- Third-party libraries requiring client-side code

### Data Fetching Patterns

#### Server Components
```typescript
async function getData() {
  const data = await prisma.table.findMany()
  return data
}

export default async function Page() {
  const data = await getData()
  return <div>{/* render */}</div>
}
```

#### Server Actions
```typescript
'use server'

export async function createItem(formData: FormData) {
  const validated = schema.parse(formData)
  await prisma.item.create({ data: validated })
  revalidatePath('/items')
}
```

### Authentication Flow

#### Supabase SSR Setup
1. Create Supabase client for server (cookies-based)
2. Create Supabase client for client (storage-based)
3. Middleware to refresh tokens
4. Protected route groups

#### Auth Flow
1. User submits login form
2. Server Action validates credentials
3. Supabase sets secure cookies
4. Middleware verifies on subsequent requests
5. Redirect to dashboard

### Database Layer

#### Prisma Schema
- Define models matching Supabase tables
- Use `@db.Uuid` for UUID types
- Add indexes for performance
- Include relations

#### Migrations
```bash
npx prisma migrate dev --name init
npx prisma generate
npx prisma db push
```

### Form Handling Pattern

```typescript
const form = useForm<FormData>({
  resolver: zodResolver(schema),
  defaultValues: {...}
})

async function onSubmit(data: FormData) {
  const result = await serverAction(data)
  if (result.success) {
    toast.success('Success!')
  }
}
```

### Testing Strategy

#### Unit Tests
- Utility functions
- Validation schemas
- Helper functions

#### Integration Tests
- Component behavior
- Form submissions
- User interactions

#### E2E Tests
- Critical user flows
- Authentication
- Data mutations

## File Naming Conventions

- **Components**: PascalCase (`UserProfile.tsx`)
- **Utilities**: camelCase (`formatDate.ts`)
- **Server Actions**: camelCase (`createUser.ts`)
- **Route Segments**: lowercase (`dashboard`, `profile`)
- **API Routes**: lowercase (`route.ts`)

## Configuration Files

### TypeScript (`tsconfig.json`)
- Strict mode enabled
- Path aliases (`@/*`)
- Next.js plugin

### ESLint (`eslint.config.mjs`)
- Flat config format (v9)
- Next.js rules
- TypeScript rules
- Custom rules for unused vars

### Tailwind (`tailwind.config.ts`)
- CSS variables for theming
- Dark mode support
- Custom color palette
- shadcn/ui compatible

### Prisma (`prisma/schema.prisma`)
- PostgreSQL datasource
- Shadow database for migrations
- Supabase connection pooling

## Environment Variables

Required variables:
```
NEXT_PUBLIC_SUPABASE_URL
NEXT_PUBLIC_SUPABASE_ANON_KEY
DATABASE_URL (connection pooling)
DIRECT_URL (direct connection)
```

## Deployment

### Vercel Setup
1. Connect GitHub repository
2. Set environment variables
3. Configure build settings (auto-detected)
4. Deploy

### Build Command
```bash
npm run build
```
- Runs Prisma generate
- Builds Next.js app
- Type checks
- Lint checks

## Best Practices

### Performance
- Use Server Components by default
- Minimize client-side JavaScript
- Implement proper caching strategies
- Use React Suspense for loading states

### Security
- Validate all inputs with Zod
- Use Server Actions for mutations
- Implement Row Level Security in Supabase
- Never expose secrets to client

### Accessibility
- Use shadcn/ui components (built on Radix)
- Include ARIA labels
- Ensure keyboard navigation
- Test with screen readers

### Type Safety
- Define Zod schemas for all forms
- Use Prisma for database queries
- Type all API responses
- Avoid `any` types
