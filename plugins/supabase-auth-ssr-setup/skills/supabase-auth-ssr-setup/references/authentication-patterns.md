# Authentication Patterns for Next.js + Supabase

## Common Authentication Patterns

### Pattern 1: Protected Route Groups

Use Next.js route groups to protect multiple routes with a single layout:

```
app/
├── (public)/
│   ├── layout.tsx          # Public layout
│   ├── page.tsx            # Home page
│   └── about/
│       └── page.tsx        # About page
└── (protected)/
    ├── layout.tsx          # Protected layout with requireAuth()
    ├── dashboard/
    │   └── page.tsx
    └── settings/
        └── page.tsx
```

**Protected layout example:**
```typescript
// app/(protected)/layout.tsx
import { requireAuth } from '@/lib/auth/utils';

export default async function ProtectedLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  await requireAuth();
  return <>{children}</>;
}
```

All routes inside `(protected)` automatically require authentication.

### Pattern 2: Conditional UI Based on Auth State

Show different content based on whether user is authenticated:

```typescript
import { getCurrentUser } from '@/lib/auth/utils';

export default async function HomePage() {
  const user = await getCurrentUser();

  return (
    <div>
      {user ? (
        <div>
          <h1>Welcome back, {user.email}!</h1>
          <a href="/dashboard">Go to Dashboard</a>
        </div>
      ) : (
        <div>
          <h1>Welcome to our app</h1>
          <a href="/login">Sign in</a>
        </div>
      )}
    </div>
  );
}
```

### Pattern 3: Role-Based Access Control

Protect routes based on user roles:

```typescript
// lib/auth/utils.ts - Add role checking
export async function requireRole(allowedRoles: string[]) {
  const user = await requireAuth();
  const supabase = await createServerClient();

  const { data: profile } = await supabase
    .from('profiles')
    .select('role')
    .eq('id', user.id)
    .single();

  if (!profile || !allowedRoles.includes(profile.role)) {
    redirect('/unauthorized');
  }

  return { user, profile };
}
```

**Usage in admin page:**
```typescript
export default async function AdminPage() {
  await requireRole(['admin', 'moderator']);

  return <div>Admin Dashboard</div>;
}
```

### Pattern 4: Server Action Authentication

Protect Server Actions that modify data:

```typescript
'use server';

import { requireAuth } from '@/lib/auth/utils';
import { createServerClient } from '@/lib/supabase/server';
import { revalidatePath } from 'next/cache';

export async function createPost(formData: FormData) {
  const user = await requireAuth();
  const supabase = await createServerClient();

  const title = formData.get('title') as string;
  const content = formData.get('content') as string;

  const { error } = await supabase.from('posts').insert({
    title,
    content,
    author_id: user.id,
  });

  if (error) throw error;

  revalidatePath('/posts');
}
```

### Pattern 5: API Route Authentication

Protect API routes for external access:

```typescript
// app/api/protected/route.ts
import { createServerClient } from '@/lib/supabase/server';
import { NextResponse } from 'next/server';

export async function GET() {
  const supabase = await createServerClient();
  const {
    data: { user },
  } = await supabase.auth.getUser();

  if (!user) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  // Return protected data
  return NextResponse.json({ data: 'Protected data' });
}
```

### Pattern 6: Parallel Data Fetching with Auth

Fetch user and their data in parallel:

```typescript
export default async function ProfilePage() {
  const user = await requireAuth();

  const supabase = await createServerClient();

  // Fetch user profile and posts in parallel
  const [{ data: profile }, { data: posts }] = await Promise.all([
    supabase.from('profiles').select('*').eq('id', user.id).single(),
    supabase.from('posts').select('*').eq('author_id', user.id),
  ]);

  return (
    <div>
      <h1>{profile?.name}</h1>
      <h2>Posts</h2>
      {posts?.map((post) => (
        <div key={post.id}>{post.title}</div>
      ))}
    </div>
  );
}
```

### Pattern 7: Redirect After Login

Preserve intended destination after login:

**Middleware:**
```typescript
export async function middleware(request: NextRequest) {
  const { supabaseResponse, user } = await updateSession(request);

  if (!user && request.nextUrl.pathname.startsWith('/dashboard')) {
    const redirectUrl = new URL('/login', request.url);
    // Save the intended destination
    redirectUrl.searchParams.set('redirect', request.nextUrl.pathname);
    return Response.redirect(redirectUrl);
  }

  return supabaseResponse;
}
```

**Login page:**
```typescript
export default async function LoginPage({
  searchParams,
}: {
  searchParams: { redirect?: string };
}) {
  // After successful login, redirect to intended page
  const redirectTo = searchParams.redirect || '/dashboard';

  // Use redirectTo in form action or success handler
}
```

### Pattern 8: Email Verification Check

Require email verification before accessing certain features:

```typescript
export async function requireVerifiedEmail() {
  const user = await requireAuth();

  if (!user.email_confirmed_at) {
    redirect('/verify-email');
  }

  return user;
}
```

## Best Practices

1. **Use Server Components for Auth Checks**: Leverage Server Components for initial auth checks to avoid client-side flashing
2. **Middleware for Session Refresh**: Always refresh sessions in middleware to keep auth state fresh
3. **Revalidate After Auth Changes**: Use `revalidatePath()` after login/logout to clear cached content
4. **Secure Cookie Configuration**: Ensure cookies use secure, httpOnly, and sameSite settings
5. **Handle Auth Errors Gracefully**: Provide clear error messages and recovery paths
6. **Use TypeScript**: Type your user objects and auth functions for better DX
7. **Test Protected Routes**: Verify both authenticated and unauthenticated access
8. **Implement Proper Redirects**: Always redirect after authentication changes to prevent stale UI

## Anti-Patterns to Avoid

1. **Client-Side Only Auth**: Don't rely solely on client-side auth checks
2. **Checking Auth on Every Component**: Use layouts and route groups instead
3. **Exposing Sensitive Data**: Never send sensitive data to client without auth check
4. **Hardcoded Redirects**: Use dynamic redirects based on user intent
5. **Ignoring Middleware**: Always use middleware for session refresh
6. **Not Handling Loading States**: Show appropriate loading states during auth checks
