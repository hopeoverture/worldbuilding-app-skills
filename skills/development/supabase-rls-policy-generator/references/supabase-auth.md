# Supabase Auth Reference

This document provides reference information for Supabase authentication functions and JWT structure.

## Core Auth Functions

### auth.uid()

Returns the UUID of the currently authenticated user.

```sql
-- Usage in RLS policy
CREATE POLICY "User access own records"
  ON table_name FOR SELECT
  USING (auth.uid() = user_id);
```

**Returns**: UUID or NULL if unauthenticated

**Common Uses**:
- User ownership checks
- Filtering user-specific data
- Inserting records with current user ID

### auth.jwt()

Returns the full JSON Web Token for the authenticated user.

```sql
-- Access top-level claims
auth.jwt() ->> 'role'  -- Returns: 'authenticated', 'anon', custom role

-- Access nested app_metadata
auth.jwt() -> 'app_metadata' ->> 'subscription_tier'
auth.jwt() -> 'app_metadata' ->> 'organization_id'

-- Access user_metadata
auth.jwt() -> 'user_metadata' ->> 'display_name'
```

**Returns**: JSONB object or NULL if unauthenticated

## JWT Structure

Standard Supabase JWT contains:

```json
{
  "aud": "authenticated",
  "exp": 1234567890,
  "sub": "user-uuid",
  "email": "user@example.com",
  "phone": "",
  "app_metadata": {
    "provider": "email",
    "providers": ["email"]
  },
  "user_metadata": {
    "display_name": "John Doe",
    "avatar_url": "https://..."
  },
  "role": "authenticated",
  "aal": "aal1",
  "amr": [
    {
      "method": "password",
      "timestamp": 1234567890
    }
  ],
  "session_id": "session-uuid"
}
```

### Custom Claims

Add custom claims via database functions or auth hooks:

```sql
-- Example: Add custom role from database
CREATE OR REPLACE FUNCTION auth.custom_access_token_hook(event jsonb)
RETURNS jsonb
LANGUAGE plpgsql
AS $$
DECLARE
  user_role TEXT;
  org_id UUID;
BEGIN
  -- Get user's role and organization
  SELECT role, organization_id INTO user_role, org_id
  FROM user_profiles
  WHERE id = (event->>'user_id')::uuid;

  -- Add custom claims
  event := jsonb_set(event, '{claims,role}', to_jsonb(user_role));
  event := jsonb_set(event, '{claims,organization_id}', to_jsonb(org_id::text));

  RETURN event;
END;
$$;
```

Access custom claims in policies:

```sql
-- Check custom role
CREATE POLICY "Admin access"
  ON table_name FOR ALL
  USING (auth.jwt() ->> 'role' = 'admin');

-- Check custom organization
CREATE POLICY "Organization access"
  ON table_name FOR SELECT
  USING (
    organization_id = (auth.jwt() ->> 'organization_id')::uuid
  );
```

## Common Patterns

### Check Authentication Status

```sql
-- Require authenticated user
USING (auth.uid() IS NOT NULL)

-- Allow both authenticated and anonymous
USING (true)

-- Authenticated users only
USING (auth.jwt() ->> 'role' = 'authenticated')
```

### Role-Based Access

```sql
-- Simple role check
USING (auth.jwt() ->> 'role' = 'admin')

-- Multiple roles
USING (
  auth.jwt() ->> 'role' IN ('admin', 'moderator')
)

-- Custom role from app_metadata
USING (
  auth.jwt() -> 'app_metadata' ->> 'custom_role' = 'premium_user'
)
```

### Email Verification

```sql
-- Require verified email
USING (
  (auth.jwt() -> 'email_confirmed_at') IS NOT NULL
)
```

### Multi-Factor Authentication

```sql
-- Require MFA
USING (
  auth.jwt() ->> 'aal' = 'aal2'
)
```

## Session Management

### Session ID

Access current session:

```sql
-- Filter by session
USING (
  session_id = (auth.jwt() ->> 'session_id')::uuid
)
```

### Authentication Method

Check how user authenticated:

```sql
-- Check for password authentication
USING (
  EXISTS (
    SELECT 1 FROM jsonb_array_elements(auth.jwt() -> 'amr') AS method
    WHERE method ->> 'method' = 'password'
  )
)

-- Check for OAuth
USING (
  EXISTS (
    SELECT 1 FROM jsonb_array_elements(auth.jwt() -> 'amr') AS method
    WHERE method ->> 'method' = 'oauth'
  )
)
```

## User Metadata vs App Metadata

### User Metadata
- User-controlled data
- Can be updated by user
- Store preferences, profile info
- Access: `auth.jwt() -> 'user_metadata'`

### App Metadata
- Admin-controlled data
- Cannot be updated by user
- Store roles, permissions, org IDs
- Access: `auth.jwt() -> 'app_metadata'`

## Security Considerations

### Always Validate User ID

```sql
-- GOOD: Enforce user ID on insert
CREATE POLICY "Insert own records"
  ON table_name FOR INSERT
  WITH CHECK (auth.uid() = user_id);

-- BAD: Allow any user_id
CREATE POLICY "Insert records"
  ON table_name FOR INSERT
  WITH CHECK (true);
```

### Don't Trust Client-Provided IDs

```sql
-- GOOD: Use auth.uid() directly
INSERT INTO posts (user_id, content)
VALUES (auth.uid(), 'content');

-- BAD: Trust client-provided user_id
INSERT INTO posts (user_id, content)
VALUES ($1, $2);  -- Client could pass any user_id
```

### Use SECURITY DEFINER Carefully

```sql
-- Mark function as SECURITY DEFINER only when necessary
CREATE FUNCTION check_permission()
RETURNS BOOLEAN
SECURITY DEFINER  -- Runs with function owner's privileges
AS $$
  -- Be very careful here - this bypasses RLS
$$;
```

## Testing Auth Context

Test policies with different auth states:

```sql
-- Set user ID
SET request.jwt.claim.sub = 'user-uuid';

-- Set role
SET request.jwt.claim.role = 'admin';

-- Set custom claims
SET request.jwt.claims = '{"role": "admin", "organization_id": "org-uuid"}';

-- Reset
RESET request.jwt.claim.sub;
RESET request.jwt.claim.role;
RESET request.jwt.claims;
```

## Common Errors

### "function auth.uid() does not exist"
- RLS is not enabled on the database
- Not using Supabase's auth schema

### NULL when expecting user ID
- User is not authenticated
- Token has expired
- Policy executed outside auth context

### "permission denied for relation"
- RLS is enabled but no policies match
- User doesn't have base GRANT permissions

## Performance Tips

1. **Cache JWT lookups**: Use helper functions to avoid repeated JWT parsing
2. **Index foreign keys**: Always index user_id, tenant_id, etc.
3. **Avoid complex JWT parsing**: Move complex logic to helper functions
4. **Use materialized views**: For complex role hierarchies

## Additional Resources

- Supabase Auth Documentation: https://supabase.com/docs/guides/auth
- Row Level Security Guide: https://supabase.com/docs/guides/auth/row-level-security
- JWT Customization: https://supabase.com/docs/guides/auth/custom-claims-and-role-based-access-control-rbac
