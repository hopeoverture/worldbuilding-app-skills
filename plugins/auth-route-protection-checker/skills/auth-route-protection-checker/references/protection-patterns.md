# Authentication Protection Patterns for Next.js

This reference document provides common authentication and authorization patterns for Next.js App Router applications.

## Pattern 1: Server Component Auth Check

Basic authentication check in Server Components.

```typescript
// app/dashboard/page.tsx
import { createServerClient } from '@/lib/supabase/server'
import { redirect } from 'next/navigation'

export default async function DashboardPage() {
  const supabase = createServerClient()
  const { data: { user }, error } = await supabase.auth.getUser()

  if (error || !user) {
    redirect('/login')
  }

  return (
    <div>
      <h1>Welcome, {user.email}</h1>
      {/* Protected content */}
    </div>
  )
}
```

## Pattern 2: API Route Auth Check

Protecting API routes with authentication.

```typescript
// app/api/data/route.ts
import { createServerClient } from '@/lib/supabase/server'
import { NextResponse } from 'next/server'

export async function GET(request: Request) {
  const supabase = createServerClient()
  const { data: { user }, error } = await supabase.auth.getUser()

  if (error || !user) {
    return NextResponse.json(
      { error: 'Unauthorized' },
      { status: 401 }
    )
  }

  // Fetch user-specific data
  const { data } = await supabase
    .from('items')
    .select('*')
    .eq('user_id', user.id)

  return NextResponse.json({ data })
}

export async function POST(request: Request) {
  const supabase = createServerClient()
  const { data: { user }, error } = await supabase.auth.getUser()

  if (error || !user) {
    return NextResponse.json(
      { error: 'Unauthorized' },
      { status: 401 }
    )
  }

  const body = await request.json()

  // Insert with user_id
  const { data, error: insertError } = await supabase
    .from('items')
    .insert([{ ...body, user_id: user.id }])
    .select()

  if (insertError) {
    return NextResponse.json(
      { error: insertError.message },
      { status: 400 }
    )
  }

  return NextResponse.json({ data }, { status: 201 })
}
```

## Pattern 3: Server Action Protection

Securing server actions with auth and validation.

```typescript
// lib/actions/posts.ts
'use server'

import { createServerClient } from '@/lib/supabase/server'
import { revalidatePath } from 'next/cache'
import { z } from 'zod'

const postSchema = z.object({
  title: z.string().min(1).max(200),
  content: z.string().min(1),
})

export async function createPost(formData: FormData) {
  // 1. Auth check
  const supabase = createServerClient()
  const { data: { user }, error } = await supabase.auth.getUser()

  if (error || !user) {
    return { error: 'Unauthorized' }
  }

  // 2. Input validation
  const rawData = {
    title: formData.get('title'),
    content: formData.get('content'),
  }

  const validatedData = postSchema.safeParse(rawData)

  if (!validatedData.success) {
    return { error: 'Invalid input', details: validatedData.error }
  }

  // 3. Perform action
  const { data, error: insertError } = await supabase
    .from('posts')
    .insert([{
      ...validatedData.data,
      user_id: user.id,
    }])
    .select()
    .single()

  if (insertError) {
    return { error: insertError.message }
  }

  // 4. Revalidate
  revalidatePath('/posts')

  return { data }
}

export async function updatePost(postId: string, formData: FormData) {
  const supabase = createServerClient()
  const { data: { user }, error } = await supabase.auth.getUser()

  if (error || !user) {
    return { error: 'Unauthorized' }
  }

  // Verify ownership
  const { data: post } = await supabase
    .from('posts')
    .select('user_id')
    .eq('id', postId)
    .single()

  if (!post || post.user_id !== user.id) {
    return { error: 'Forbidden' }
  }

  // Validate and update
  const rawData = {
    title: formData.get('title'),
    content: formData.get('content'),
  }

  const validatedData = postSchema.safeParse(rawData)

  if (!validatedData.success) {
    return { error: 'Invalid input' }
  }

  const { data, error: updateError } = await supabase
    .from('posts')
    .update(validatedData.data)
    .eq('id', postId)
    .select()
    .single()

  if (updateError) {
    return { error: updateError.message }
  }

  revalidatePath('/posts')
  revalidatePath(`/posts/${postId}`)

  return { data }
}
```

## Pattern 4: Role-Based Access Control (RBAC)

Check user roles for access control.

```typescript
// lib/auth/roles.ts
export type Role = 'user' | 'moderator' | 'admin'

export async function getUserRole(userId: string): Promise<Role | null> {
  const supabase = createServerClient()

  const { data } = await supabase
    .from('profiles')
    .select('role')
    .eq('id', userId)
    .single()

  return data?.role || null
}

export function canAccessRoute(userRole: Role, requiredRoles: Role[]): boolean {
  return requiredRoles.includes(userRole)
}

// Usage in server component
export default async function AdminPage() {
  const supabase = createServerClient()
  const { data: { user } } = await supabase.auth.getUser()

  if (!user) redirect('/login')

  const role = await getUserRole(user.id)

  if (!canAccessRoute(role, ['admin'])) {
    redirect('/unauthorized')
  }

  return <div>Admin Content</div>
}
```

## Pattern 5: Permission-Based Access Control

Fine-grained permission checking.

```typescript
// lib/auth/permissions.ts
export type Permission =
  | 'posts:read'
  | 'posts:create'
  | 'posts:update'
  | 'posts:delete'
  | 'users:read'
  | 'users:update'
  | 'users:delete'

export async function hasPermission(
  userId: string,
  permission: Permission
): Promise<boolean> {
  const supabase = createServerClient()

  // Check user's role-based permissions
  const { data: role } = await supabase
    .from('profiles')
    .select('role')
    .eq('id', userId)
    .single()

  // Admin has all permissions
  if (role?.role === 'admin') return true

  // Check specific permission
  const { data } = await supabase
    .from('user_permissions')
    .select('permission')
    .eq('user_id', userId)
    .eq('permission', permission)
    .single()

  return !!data
}

// Usage in server action
export async function deleteUser(targetUserId: string) {
  'use server'

  const supabase = createServerClient()
  const { data: { user } } = await supabase.auth.getUser()

  if (!user) {
    return { error: 'Unauthorized' }
  }

  const canDelete = await hasPermission(user.id, 'users:delete')

  if (!canDelete) {
    return { error: 'Insufficient permissions' }
  }

  // Perform deletion
  const { error } = await supabase
    .from('users')
    .delete()
    .eq('id', targetUserId)

  if (error) return { error: error.message }

  revalidatePath('/admin/users')
  return { success: true }
}
```

## Pattern 6: Middleware Route Protection

Protect multiple routes with middleware.

```typescript
// middleware.ts
import { createServerClient } from '@/lib/supabase/middleware'
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

const publicRoutes = ['/', '/about', '/login', '/signup']
const protectedRoutes = ['/dashboard', '/profile', '/settings']
const adminRoutes = ['/admin']

export async function middleware(request: NextRequest) {
  const response = NextResponse.next()
  const supabase = createServerClient(request, response)

  const { data: { user } } = await supabase.auth.getUser()
  const pathname = request.nextUrl.pathname

  // Allow public routes
  if (publicRoutes.includes(pathname)) {
    return response
  }

  // Check if route requires auth
  const requiresAuth = protectedRoutes.some(route =>
    pathname.startsWith(route)
  )

  if (requiresAuth && !user) {
    const redirectUrl = new URL('/login', request.url)
    redirectUrl.searchParams.set('redirect', pathname)
    return NextResponse.redirect(redirectUrl)
  }

  // Check admin routes
  const requiresAdmin = adminRoutes.some(route =>
    pathname.startsWith(route)
  )

  if (requiresAdmin) {
    if (!user) {
      return NextResponse.redirect(new URL('/login', request.url))
    }

    const { data: profile } = await supabase
      .from('profiles')
      .select('role')
      .eq('id', user.id)
      .single()

    if (profile?.role !== 'admin') {
      return NextResponse.redirect(new URL('/unauthorized', request.url))
    }
  }

  return response
}

export const config = {
  matcher: [
    '/((?!_next/static|_next/image|favicon.ico|.*\\.(?:svg|png|jpg|jpeg|gif|webp)$).*)',
  ],
}
```

## Pattern 7: Layout-Based Protection

Protect all routes within a layout.

```typescript
// app/(protected)/layout.tsx
import { createServerClient } from '@/lib/supabase/server'
import { redirect } from 'next/navigation'

export default async function ProtectedLayout({
  children,
}: {
  children: React.ReactNode
}) {
  const supabase = createServerClient()
  const { data: { user } } = await supabase.auth.getUser()

  if (!user) {
    redirect('/login')
  }

  return <>{children}</>
}

// All pages under app/(protected)/ are now protected
```

## Pattern 8: Ownership Verification

Verify user owns a resource before allowing access.

```typescript
// app/posts/[id]/edit/page.tsx
import { createServerClient } from '@/lib/supabase/server'
import { redirect, notFound } from 'next/navigation'

export default async function EditPostPage({
  params,
}: {
  params: { id: string }
}) {
  const supabase = createServerClient()
  const { data: { user } } = await supabase.auth.getUser()

  if (!user) redirect('/login')

  // Fetch post and verify ownership
  const { data: post, error } = await supabase
    .from('posts')
    .select('*')
    .eq('id', params.id)
    .single()

  if (error || !post) notFound()

  if (post.user_id !== user.id) {
    redirect('/unauthorized')
  }

  return <EditPostForm post={post} />
}
```

## Pattern 9: Multi-Tenant Isolation

Ensure users can only access their tenant's data.

```typescript
// lib/auth/tenant.ts
export async function requireTenantAccess(tenantId: string) {
  const supabase = createServerClient()
  const { data: { user } } = await supabase.auth.getUser()

  if (!user) {
    redirect('/login')
  }

  // Check tenant membership
  const { data: membership } = await supabase
    .from('tenant_members')
    .select('role')
    .eq('tenant_id', tenantId)
    .eq('user_id', user.id)
    .single()

  if (!membership) {
    redirect('/unauthorized')
  }

  return { user, role: membership.role }
}

// Usage
export default async function TenantPage({
  params,
}: {
  params: { tenantId: string }
}) {
  const { user, role } = await requireTenantAccess(params.tenantId)

  // User has access to this tenant
  return <div>Tenant Content</div>
}
```

## Pattern 10: Helper Functions

Reusable auth utilities.

```typescript
// lib/auth/helpers.ts
import { createServerClient } from '@/lib/supabase/server'
import { redirect } from 'next/navigation'
import { cache } from 'react'

// Cache the current user for the request
export const getCurrentUser = cache(async () => {
  const supabase = createServerClient()
  const { data: { user } } = await supabase.auth.getUser()
  return user
})

// Require authentication or redirect
export async function requireAuth() {
  const user = await getCurrentUser()

  if (!user) {
    redirect('/login')
  }

  return user
}

// Require specific role
export async function requireRole(allowedRoles: string[]) {
  const user = await requireAuth()
  const supabase = createServerClient()

  const { data: profile } = await supabase
    .from('profiles')
    .select('role')
    .eq('id', user.id)
    .single()

  if (!profile || !allowedRoles.includes(profile.role)) {
    redirect('/unauthorized')
  }

  return { user, role: profile.role }
}

// Get user with profile
export async function getUserWithProfile() {
  const user = await requireAuth()
  const supabase = createServerClient()

  const { data: profile } = await supabase
    .from('profiles')
    .select('*')
    .eq('id', user.id)
    .single()

  return { user, profile }
}

// Check if user can perform action
export async function canPerformAction(
  action: string,
  resourceId?: string
): Promise<boolean> {
  const user = await getCurrentUser()

  if (!user) return false

  // Check permissions logic
  const supabase = createServerClient()

  const { data } = await supabase
    .rpc('check_user_permission', {
      p_user_id: user.id,
      p_action: action,
      p_resource_id: resourceId,
    })

  return !!data
}
```

## Pattern 11: Error Handling

Proper error handling for auth failures.

```typescript
// app/api/protected/route.ts
import { createServerClient } from '@/lib/supabase/server'
import { NextResponse } from 'next/server'

export async function GET(request: Request) {
  try {
    const supabase = createServerClient()
    const { data: { user }, error } = await supabase.auth.getUser()

    if (error) {
      console.error('Auth error:', error)
      return NextResponse.json(
        { error: 'Authentication failed' },
        { status: 401 }
      )
    }

    if (!user) {
      return NextResponse.json(
        { error: 'Unauthorized - Please log in' },
        { status: 401 }
      )
    }

    // Fetch data
    const { data, error: fetchError } = await supabase
      .from('items')
      .select('*')

    if (fetchError) {
      console.error('Database error:', fetchError)
      return NextResponse.json(
        { error: 'Failed to fetch data' },
        { status: 500 }
      )
    }

    return NextResponse.json({ data })
  } catch (error) {
    console.error('Unexpected error:', error)
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    )
  }
}
```

## Pattern 12: Rate Limiting with Auth

Combine auth with rate limiting.

```typescript
// lib/rate-limit.ts
import { Ratelimit } from '@upstash/ratelimit'
import { Redis } from '@upstash/redis'

const ratelimit = new Ratelimit({
  redis: Redis.fromEnv(),
  limiter: Ratelimit.slidingWindow(10, '10 s'),
})

export async function checkRateLimit(identifier: string) {
  const { success, limit, reset, remaining } = await ratelimit.limit(
    identifier
  )

  return {
    success,
    limit,
    reset,
    remaining,
  }
}

// Usage in API route
export async function POST(request: Request) {
  const supabase = createServerClient()
  const { data: { user } } = await supabase.auth.getUser()

  if (!user) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
  }

  // Rate limit by user ID
  const rateLimitResult = await checkRateLimit(user.id)

  if (!rateLimitResult.success) {
    return NextResponse.json(
      { error: 'Rate limit exceeded' },
      {
        status: 429,
        headers: {
          'X-RateLimit-Limit': rateLimitResult.limit.toString(),
          'X-RateLimit-Remaining': rateLimitResult.remaining.toString(),
          'X-RateLimit-Reset': rateLimitResult.reset.toString(),
        },
      }
    )
  }

  // Process request
  return NextResponse.json({ success: true })
}
```

## Testing Auth Protection

Always test auth protection:

```typescript
// tests/auth.test.ts
import { describe, it, expect } from 'vitest'
import { GET } from '@/app/api/protected/route'

describe('Auth Protection', () => {
  it('rejects unauthenticated requests', async () => {
    const request = new Request('http://localhost/api/protected')
    const response = await GET(request)

    expect(response.status).toBe(401)
    const json = await response.json()
    expect(json.error).toBe('Unauthorized')
  })

  it('allows authenticated requests', async () => {
    // Mock authenticated request
    const request = new Request('http://localhost/api/protected', {
      headers: {
        Authorization: 'Bearer valid-token',
      },
    })

    const response = await GET(request)
    expect(response.status).toBe(200)
  })
})
```

## Security Best Practices

1. **Always validate on server**: Never trust client-side auth
2. **Check ownership**: Verify user owns resource before modification
3. **Use RLS**: Combine with Row-Level Security in database
4. **Rate limit**: Prevent abuse of authenticated endpoints
5. **Audit log**: Log authentication failures and privileged actions
6. **Expire sessions**: Implement session timeouts
7. **HTTPS only**: Never send auth tokens over HTTP
8. **CSRF protection**: Use CSRF tokens for state-changing operations
