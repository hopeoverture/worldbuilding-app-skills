# Next.js Best Practices (2025)

Current best practices for Next.js 15/16 development with App Router, Server Components, and modern patterns.

## Framework Versions

### Current Versions
- **Next.js**: 15.x or 16.x (latest stable)
- **React**: 19.x (Server Components, Actions)
- **TypeScript**: 5.x
- **Node.js**: 20 LTS or higher

### Deprecated Versions to Flag
- Next.js 12.x or older (Pages Router era)
- React 17.x or older
- TypeScript 4.x or older

## App Router vs Pages Router

### [OK] Modern (App Router)

```
app/
├── layout.tsx          # Root layout
├── page.tsx            # Homepage
├── entities/
│   ├── layout.tsx      # Nested layout
│   ├── page.tsx        # Entity list
│   └── [id]/
│       └── page.tsx    # Entity detail
└── api/                # API route handlers (minimal)
    └── webhook/
        └── route.ts    # External webhooks only
```

### [ERROR] Deprecated (Pages Router)

```
pages/
├── _app.tsx            # Old pattern
├── _document.tsx       # Old pattern
├── index.tsx           # Old pattern
├── entities/
│   ├── index.tsx
│   └── [id].tsx
└── api/                # Old API routes
    └── entities.ts
```

**Migration Check**: Flag any skills using `pages/` directory or `getServerSideProps`

## Server Components vs Client Components

### Default: Server Components

```tsx
// app/entities/page.tsx
// No 'use client' directive = Server Component (default)

import { db } from '@/lib/db'

export default async function EntitiesPage() {
  // Direct database access - only in Server Components
  const entities = await db.entity.findMany()

  return (
    <div>
      <h1>Entities</h1>
      {entities.map(entity => (
        <EntityCard key={entity.id} entity={entity} />
      ))}
    </div>
  )
}
```

### Client Components (When Needed)

```tsx
// components/EntityForm.tsx
'use client'  // Required for hooks, events, browser APIs

import { useState } from 'react'
import { useForm } from 'react-hook-form'

export function EntityForm() {
  const [isSubmitting, setIsSubmitting] = useState(false)
  const form = useForm()

  return <form>...</form>
}
```

**When to use 'use client':**
- useState, useEffect, other hooks
- Event handlers (onClick, onChange)
- Browser APIs (localStorage, window)
- Third-party libraries requiring browser

**Best Practice**: Keep 'use client' boundary as low as possible in component tree

## Data Fetching

### [OK] Modern: Server Components + fetch

```tsx
// app/characters/page.tsx
export default async function CharactersPage() {
  // Fetch in Server Component
  const characters = await fetch('https://api.example.com/characters', {
    next: { revalidate: 3600 } // Cache for 1 hour
  }).then(res => res.json())

  return <CharacterList characters={characters} />
}
```

### [OK] Modern: Server Components + Database

```tsx
// app/locations/page.tsx
import { db } from '@/lib/db'

export default async function LocationsPage() {
  // Direct database access
  const locations = await db.location.findMany({
    include: { region: true }
  })

  return <LocationList locations={locations} />
}
```

### [ERROR] Deprecated: getServerSideProps

```tsx
// pages/characters.tsx - OLD PATTERN
export async function getServerSideProps() {
  const characters = await fetchCharacters()
  return { props: { characters } }
}
```

**Migration Check**: Replace `getServerSideProps`, `getStaticProps`, `getInitialProps` with Server Component async data fetching

## Server Actions

### [OK] Modern: Server Actions for Mutations

```tsx
// app/actions/character.ts
'use server'

import { db } from '@/lib/db'
import { revalidatePath } from 'next/cache'

export async function createCharacter(formData: FormData) {
  const name = formData.get('name') as string

  const character = await db.character.create({
    data: { name }
  })

  revalidatePath('/characters')
  return { success: true, character }
}
```

```tsx
// app/characters/CreateForm.tsx
'use client'

import { createCharacter } from '@/app/actions/character'

export function CreateForm() {
  return (
    <form action={createCharacter}>
      <input name="name" />
      <button type="submit">Create</button>
    </form>
  )
}
```

### [ERROR] Deprecated: API Routes for Simple Mutations

```tsx
// pages/api/characters.ts - OLD PATTERN
export default async function handler(req, res) {
  if (req.method === 'POST') {
    const character = await createCharacter(req.body)
    res.json({ character })
  }
}
```

**When to still use API Routes:**
- Webhooks from external services
- OAuth callbacks
- Third-party integrations requiring public endpoints

**Migration Check**: Replace API routes used for form submissions with Server Actions

## Metadata and SEO

### [OK] Modern: generateMetadata

```tsx
// app/characters/[id]/page.tsx
import { Metadata } from 'next'

export async function generateMetadata({ params }): Promise<Metadata> {
  const character = await db.character.findUnique({
    where: { id: params.id }
  })

  return {
    title: character.name,
    description: character.bio,
    openGraph: {
      title: character.name,
      description: character.bio,
      images: [character.image],
    },
  }
}
```

### [ERROR] Deprecated: next/head

```tsx
// OLD PATTERN
import Head from 'next/head'

<Head>
  <title>{character.name}</title>
</Head>
```

## Routing and Navigation

### [OK] Modern: Link from next/link

```tsx
import Link from 'next/link'

<Link href="/characters/123">View Character</Link>
```

### [OK] Modern: useRouter from next/navigation

```tsx
'use client'
import { useRouter } from 'next/navigation'  // Not 'next/router'!

export function BackButton() {
  const router = useRouter()
  return <button onClick={() => router.back()}>Back</button>
}
```

### [ERROR] Deprecated: useRouter from next/router

```tsx
// OLD PATTERN
import { useRouter } from 'next/router'  // Pages Router only
```

## Loading States

### [OK] Modern: loading.tsx

```tsx
// app/characters/loading.tsx
export default function Loading() {
  return <div>Loading characters...</div>
}
```

### [OK] Modern: Suspense Boundaries

```tsx
// app/characters/page.tsx
import { Suspense } from 'react'

export default function Page() {
  return (
    <Suspense fallback={<LoadingSkeleton />}>
      <CharacterList />
    </Suspense>
  )
}
```

## Error Handling

### [OK] Modern: error.tsx

```tsx
// app/characters/error.tsx
'use client'

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string }
  reset: () => void
}) {
  return (
    <div>
      <h2>Something went wrong!</h2>
      <button onClick={() => reset()}>Try again</button>
    </div>
  )
}
```

## Caching and Revalidation

### [OK] Modern: Revalidation Strategies

```tsx
// Time-based revalidation
fetch(url, { next: { revalidate: 3600 } })  // 1 hour

// On-demand revalidation
import { revalidatePath } from 'next/cache'
revalidatePath('/characters')

// Tag-based revalidation
fetch(url, { next: { tags: ['characters'] } })
import { revalidateTag } from 'next/cache'
revalidateTag('characters')

// Disable caching
fetch(url, { cache: 'no-store' })
```

## Middleware

### [OK] Modern: middleware.ts

```tsx
// middleware.ts
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export function middleware(request: NextRequest) {
  // Auth check
  const token = request.cookies.get('token')

  if (!token && request.nextUrl.pathname.startsWith('/dashboard')) {
    return NextResponse.redirect(new URL('/login', request.url))
  }

  return NextResponse.next()
}

export const config = {
  matcher: '/dashboard/:path*',
}
```

## TypeScript Patterns

### [OK] Type-Safe Server Components

```tsx
interface Character {
  id: string
  name: string
  bio: string
}

export default async function CharacterPage({
  params,
}: {
  params: { id: string }
}) {
  const character: Character = await db.character.findUnique({
    where: { id: params.id }
  })

  return <div>{character.name}</div>
}
```

### [OK] Type-Safe Server Actions

```tsx
'use server'

import { z } from 'zod'

const createCharacterSchema = z.object({
  name: z.string().min(2),
  bio: z.string().max(5000),
})

export async function createCharacter(
  data: z.infer<typeof createCharacterSchema>
) {
  const validated = createCharacterSchema.parse(data)
  // ...
}
```

## Environment Variables

### [OK] Modern: Type-Safe Env

```typescript
// env.mjs
import { createEnv } from "@t3-oss/env-nextjs"
import { z } from "zod"

export const env = createEnv({
  server: {
    DATABASE_URL: z.string().url(),
    NEXTAUTH_SECRET: z.string().min(1),
  },
  client: {
    NEXT_PUBLIC_API_URL: z.string().url(),
  },
  runtimeEnv: {
    DATABASE_URL: process.env.DATABASE_URL,
    NEXTAUTH_SECRET: process.env.NEXTAUTH_SECRET,
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL,
  },
})
```

## Configuration

### [OK] Modern: next.config.js

```javascript
/** @type {import('next').NextConfig} */
const nextConfig = {
  experimental: {
    serverActions: {
      bodySizeLimit: '2mb',
    },
  },
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 'example.com',
      },
    ],
  },
}

export default nextConfig
```

## Common Anti-Patterns to Flag

### [ERROR] Fetching in Client Components

```tsx
'use client'
import { useEffect, useState } from 'react'

// BAD: Fetch in client component
export function Characters() {
  const [data, setData] = useState([])

  useEffect(() => {
    fetch('/api/characters').then(r => r.json()).then(setData)
  }, [])

  return <div>{data.map(...)}</div>
}
```

[OK] **Fix**: Move data fetching to Server Component or use React Query for client-side data management

### [ERROR] Unnecessary 'use client'

```tsx
'use client'  // Not needed!

export function StaticCard({ title, description }) {
  return (
    <div>
      <h3>{title}</h3>
      <p>{description}</p>
    </div>
  )
}
```

[OK] **Fix**: Remove 'use client' if component doesn't use hooks, events, or browser APIs

### [ERROR] Mixing Data Fetching Methods

```tsx
// BAD: Using both old and new patterns
export async function getServerSideProps() { ... }

export default async function Page() {
  const data = await fetch(...)
}
```

[OK] **Fix**: Use only Server Component data fetching in App Router

## Performance Best Practices

### Image Optimization

```tsx
import Image from 'next/image'

<Image
  src="/character.jpg"
  alt="Character portrait"
  width={800}
  height={600}
  priority  // For LCP images
/>
```

### Font Optimization

```tsx
import { Inter } from 'next/font/google'

const inter = Inter({ subsets: ['latin'] })

export default function RootLayout({ children }) {
  return (
    <html lang="en" className={inter.className}>
      {children}
    </html>
  )
}
```

### Code Splitting

```tsx
import dynamic from 'next/dynamic'

const HeavyComponent = dynamic(() => import('@/components/HeavyComponent'), {
  loading: () => <p>Loading...</p>,
  ssr: false,  // Client-only if needed
})
```

## Validation Checklist

When reviewing Next.js skills, check for:

- [ ] Uses App Router (app/ directory), not Pages Router
- [ ] Server Components for data fetching
- [ ] Server Actions for mutations
- [ ] Proper 'use client' boundaries
- [ ] generateMetadata for SEO
- [ ] useRouter from 'next/navigation'
- [ ] Modern caching with fetch options
- [ ] loading.tsx and error.tsx files
- [ ] Type-safe environment variables
- [ ] Image and font optimization
- [ ] No deprecated APIs (getServerSideProps, etc.)
- [ ] Proper middleware usage
- [ ] Correct import paths

## Quick Reference

### Must Use (Modern)
- [OK] `app/` directory
- [OK] Server Components (default)
- [OK] Server Actions ('use server')
- [OK] `generateMetadata`
- [OK] `useRouter` from 'next/navigation'
- [OK] `revalidatePath`/`revalidateTag`

### Must Avoid (Deprecated)
- [ERROR] `pages/` directory
- [ERROR] `getServerSideProps`
- [ERROR] `getStaticProps`
- [ERROR] `getInitialProps`
- [ERROR] API routes for mutations
- [ERROR] `useRouter` from 'next/router'
- [ERROR] `next/head`
