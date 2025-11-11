# Security Considerations for Supabase Auth

## Cookie Security

### Secure Cookie Configuration

The `@supabase/ssr` package automatically configures secure cookies with these settings:

- **httpOnly**: Prevents client-side JavaScript from accessing cookies
- **secure**: Cookies only sent over HTTPS (except localhost)
- **sameSite**: Prevents CSRF attacks by restricting cross-site cookie sending
- **path**: Limits cookie scope to specific paths

**Do not modify** cookie settings unless you understand the security implications.

### Session Duration

Configure session timeout in Supabase dashboard:

1. Go to Authentication > Settings
2. Adjust "JWT expiry limit" (default: 1 hour)
3. Set "Refresh token expiry" (default: 30 days)

**Recommendations:**
- Short JWT expiry (1 hour) for better security
- Longer refresh token expiry (30 days) for better UX
- Use middleware to automatically refresh sessions

## Row Level Security (RLS)

### Enable RLS on All Tables

Always enable Row Level Security on tables containing user data:

```sql
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;
```

### Create Restrictive Policies

**Read own data:**
```sql
CREATE POLICY "Users can view own profile"
ON profiles FOR SELECT
USING (auth.uid() = id);
```

**Update own data:**
```sql
CREATE POLICY "Users can update own profile"
ON profiles FOR UPDATE
USING (auth.uid() = id);
```

**Insert on signup:**
```sql
CREATE POLICY "Users can insert own profile"
ON profiles FOR INSERT
WITH CHECK (auth.uid() = id);
```

### Test RLS Policies

Always test policies with different user contexts:

```sql
-- Test as specific user
SET LOCAL ROLE authenticated;
SET LOCAL request.jwt.claims.sub = 'user-uuid-here';

-- Run queries to verify access
SELECT * FROM profiles;
```

## Authentication Best Practices

### 1. Never Trust Client Input

Always validate on server-side:

```typescript
export async function updateProfile(formData: FormData) {
  const user = await requireAuth();

  // Validate input
  const name = formData.get('name') as string;
  if (!name || name.length < 2) {
    throw new Error('Invalid name');
  }

  // Only update own profile
  const supabase = await createServerClient();
  await supabase
    .from('profiles')
    .update({ name })
    .eq('id', user.id); // Ensure user can only update their own data
}
```

### 2. Use Server Components for Sensitive Data

Fetch sensitive data in Server Components, not Client Components:

```typescript
// [OK] Good - Server Component
export default async function ProfilePage() {
  const user = await requireAuth();
  const supabase = await createServerClient();

  const { data: privateData } = await supabase
    .from('private_table')
    .select('*')
    .eq('user_id', user.id);

  return <div>{/* Use privateData */}</div>;
}
```

```typescript
// [ERROR] Bad - Client Component exposes API
'use client';

export default function ProfilePage() {
  const [data, setData] = useState(null);

  useEffect(() => {
    // Fetching sensitive data on client
    fetch('/api/private-data').then(/* ... */);
  }, []);
}
```

### 3. Implement Rate Limiting

Protect authentication endpoints from brute force:

```typescript
// Example using Upstash Rate Limit
import { Ratelimit } from '@upstash/ratelimit';
import { Redis } from '@upstash/redis';

const ratelimit = new Ratelimit({
  redis: Redis.fromEnv(),
  limiter: Ratelimit.slidingWindow(5, '15 m'), // 5 attempts per 15 minutes
});

export async function signInWithPassword(formData: FormData) {
  const email = formData.get('email') as string;

  const { success } = await ratelimit.limit(email);
  if (!success) {
    return { error: 'Too many attempts. Please try again later.' };
  }

  // Proceed with sign in
}
```

### 4. Validate Email Addresses

Require email verification before granting full access:

```typescript
export async function requireVerifiedEmail() {
  const user = await requireAuth();

  if (!user.email_confirmed_at) {
    redirect('/verify-email');
  }

  return user;
}
```

Configure in Supabase:
- Authentication > Settings > Enable "Confirm email"
- Customize email templates in Authentication > Email Templates

### 5. Use Environment Variables Correctly

**Public variables** (safe to expose):
- `NEXT_PUBLIC_SUPABASE_URL`
- `NEXT_PUBLIC_SUPABASE_ANON_KEY`

**Private variables** (server-side only):
- `SUPABASE_SERVICE_ROLE_KEY` (never expose to client!)

```typescript
// [OK] Good - Service role only on server
'use server';

import { createClient } from '@supabase/supabase-js';

export async function adminFunction() {
  const supabase = createClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.SUPABASE_SERVICE_ROLE_KEY! // Only accessible server-side
  );

  // Bypasses RLS - use carefully
}
```

## Common Security Mistakes

### 1. Exposing Service Role Key

[ERROR] **Never** use service role key in client-side code:

```typescript
// [ERROR] DANGEROUS - Exposes admin access
const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL,
  process.env.SUPABASE_SERVICE_ROLE_KEY // Exposed to client!
);
```

### 2. Skipping RLS

[ERROR] **Never** disable RLS or use service role to bypass it unnecessarily:

```sql
-- [ERROR] DANGEROUS - Allows anyone to read all data
ALTER TABLE profiles DISABLE ROW LEVEL SECURITY;
```

### 3. Client-Side Authorization

[ERROR] **Never** rely only on client-side checks:

```typescript
// [ERROR] BAD - Can be bypassed
'use client';

export default function AdminPanel() {
  const [user, setUser] = useState(null);

  if (user?.role !== 'admin') {
    return <div>Unauthorized</div>;
  }

  return <div>Admin content</div>; // Still rendered in HTML!
}
```

[OK] **Always** enforce on server:

```typescript
// [OK] GOOD - Server-side enforcement
export default async function AdminPanel() {
  await requireRole('admin'); // Redirects if not admin

  return <div>Admin content</div>;
}
```

### 4. Not Revalidating After Auth Changes

[ERROR] **Never** forget to revalidate after login/logout:

```typescript
// [ERROR] BAD - Stale cached content may show
export async function logout() {
  const supabase = await createServerClient();
  await supabase.auth.signOut();
  redirect('/'); // Missing revalidation!
}
```

[OK] **Always** revalidate:

```typescript
// [OK] GOOD
export async function logout() {
  const supabase = await createServerClient();
  await supabase.auth.signOut();
  revalidatePath('/', 'layout'); // Clears all cached pages
  redirect('/');
}
```

## Audit Checklist

Use this checklist when implementing authentication:

- [ ] RLS enabled on all tables with user data
- [ ] RLS policies tested with different user contexts
- [ ] Service role key never exposed to client
- [ ] Email verification required for sensitive actions
- [ ] Rate limiting on authentication endpoints
- [ ] Input validation on all Server Actions
- [ ] Secure cookies configured (httpOnly, secure, sameSite)
- [ ] Middleware refreshes sessions on all requests
- [ ] Sensitive data only fetched in Server Components
- [ ] Authorization checks on server-side, not client-side
- [ ] Proper revalidation after auth state changes
- [ ] Error messages don't leak sensitive information
- [ ] OAuth redirect URLs configured correctly
- [ ] Session timeout appropriate for use case
- [ ] Logout clears all auth state and cookies
