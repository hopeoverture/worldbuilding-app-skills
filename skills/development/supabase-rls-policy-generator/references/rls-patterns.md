# RLS Policy Patterns

This reference document provides common Row-Level Security patterns for Supabase applications.

## Pattern 1: User Ownership

Simple pattern where users can only access their own records.

```sql
-- Enable RLS
ALTER TABLE posts ENABLE ROW LEVEL SECURITY;

-- User can view own posts
CREATE POLICY "Users view own posts"
  ON posts FOR SELECT
  USING (auth.uid() = user_id);

-- User can insert posts with their ID
CREATE POLICY "Users create own posts"
  ON posts FOR INSERT
  WITH CHECK (auth.uid() = user_id);

-- User can update own posts
CREATE POLICY "Users update own posts"
  ON posts FOR UPDATE
  USING (auth.uid() = user_id)
  WITH CHECK (auth.uid() = user_id);

-- User can delete own posts
CREATE POLICY "Users delete own posts"
  ON posts FOR DELETE
  USING (auth.uid() = user_id);
```

## Pattern 2: Multi-Tenant Isolation

Users can access all records within their tenant.

```sql
-- Enable RLS
ALTER TABLE documents ENABLE ROW LEVEL SECURITY;

-- Users can only see documents in their tenant
CREATE POLICY "Tenant isolation"
  ON documents FOR ALL
  USING (
    tenant_id IN (
      SELECT tenant_id FROM user_tenants
      WHERE user_id = auth.uid()
    )
  );
```

## Pattern 3: Role-Based Access Control (RBAC)

Different access levels based on user roles.

```sql
-- Enable RLS
ALTER TABLE sensitive_data ENABLE ROW LEVEL SECURITY;

-- Admins can view all records
CREATE POLICY "Admins view all"
  ON sensitive_data FOR SELECT
  USING (auth.jwt() ->> 'role' = 'admin');

-- Managers can view team records
CREATE POLICY "Managers view team"
  ON sensitive_data FOR SELECT
  USING (
    auth.jwt() ->> 'role' = 'manager' AND
    team_id IN (
      SELECT team_id FROM user_teams
      WHERE user_id = auth.uid() AND role = 'manager'
    )
  );

-- Regular users can view own records
CREATE POLICY "Users view own"
  ON sensitive_data FOR SELECT
  USING (auth.uid() = user_id);
```

## Pattern 4: Public/Private Resources

Some records are public, others are private.

```sql
-- Enable RLS
ALTER TABLE articles ENABLE ROW LEVEL SECURITY;

-- Everyone can view public articles
CREATE POLICY "Public articles readable"
  ON articles FOR SELECT
  USING (is_public = true);

-- Authenticated users can view their private articles
CREATE POLICY "Private articles owner only"
  ON articles FOR SELECT
  USING (is_public = false AND auth.uid() = user_id);

-- Only author can update
CREATE POLICY "Author can update"
  ON articles FOR UPDATE
  USING (auth.uid() = user_id);
```

## Pattern 5: Hierarchical Permissions

Organization > Team > User hierarchy.

```sql
-- Enable RLS
ALTER TABLE projects ENABLE ROW LEVEL SECURITY;

-- Organization admins see all organization projects
CREATE POLICY "Org admins view all"
  ON projects FOR SELECT
  USING (
    organization_id IN (
      SELECT organization_id FROM user_organizations
      WHERE user_id = auth.uid() AND role = 'admin'
    )
  );

-- Team members see team projects
CREATE POLICY "Team members view team projects"
  ON projects FOR SELECT
  USING (
    team_id IN (
      SELECT team_id FROM user_teams
      WHERE user_id = auth.uid()
    )
  );

-- Project owner can always view
CREATE POLICY "Owner can view"
  ON projects FOR SELECT
  USING (auth.uid() = owner_id);
```

## Pattern 6: Shared Resources

Resources shared with specific users.

```sql
-- Enable RLS
ALTER TABLE files ENABLE ROW LEVEL SECURITY;

-- Owner can view
CREATE POLICY "Owner can view files"
  ON files FOR SELECT
  USING (auth.uid() = owner_id);

-- Shared users can view
CREATE POLICY "Shared users can view"
  ON files FOR SELECT
  USING (
    EXISTS (
      SELECT 1 FROM file_shares
      WHERE file_id = files.id
      AND user_id = auth.uid()
      AND (expires_at IS NULL OR expires_at > NOW())
    )
  );

-- Public files viewable by all authenticated
CREATE POLICY "Public files viewable"
  ON files FOR SELECT
  USING (is_public = true);
```

## Pattern 7: JWT Claims-Based Access

Access based on custom JWT claims.

```sql
-- Enable RLS
ALTER TABLE premium_content ENABLE ROW LEVEL SECURITY;

-- Premium users can view premium content
CREATE POLICY "Premium users access"
  ON premium_content FOR SELECT
  USING (
    (auth.jwt() -> 'app_metadata' ->> 'subscription_tier') IN ('premium', 'enterprise')
  );

-- Organization-scoped access
CREATE POLICY "Organization scoped"
  ON premium_content FOR SELECT
  USING (
    organization_id = (auth.jwt() -> 'app_metadata' ->> 'organization_id')::uuid
  );
```

## Pattern 8: Time-Based Access

Access that expires or becomes available at certain times.

```sql
-- Enable RLS
ALTER TABLE scheduled_content ENABLE ROW LEVEL SECURITY;

-- Content available after publish date
CREATE POLICY "Published content viewable"
  ON scheduled_content FOR SELECT
  USING (
    published_at IS NOT NULL AND
    published_at <= NOW() AND
    (expires_at IS NULL OR expires_at > NOW())
  );

-- Authors can always view
CREATE POLICY "Authors view all states"
  ON scheduled_content FOR SELECT
  USING (auth.uid() = author_id);
```

## Pattern 9: Cascading Permissions

Permissions inherited from parent resources.

```sql
-- Enable RLS on both tables
ALTER TABLE folders ENABLE ROW LEVEL SECURITY;
ALTER TABLE folder_items ENABLE ROW LEVEL SECURITY;

-- Folder access based on ownership or sharing
CREATE POLICY "Folder access"
  ON folders FOR SELECT
  USING (
    auth.uid() = owner_id OR
    EXISTS (
      SELECT 1 FROM folder_permissions
      WHERE folder_id = folders.id AND user_id = auth.uid()
    )
  );

-- Item access inherits from folder
CREATE POLICY "Item access via folder"
  ON folder_items FOR SELECT
  USING (
    folder_id IN (
      SELECT id FROM folders
      WHERE auth.uid() = owner_id OR
      EXISTS (
        SELECT 1 FROM folder_permissions
        WHERE folder_id = folders.id AND user_id = auth.uid()
      )
    )
  );
```

## Pattern 10: Conditional Write Restrictions

Different rules for reading vs writing.

```sql
-- Enable RLS
ALTER TABLE moderated_content ENABLE ROW LEVEL SECURITY;

-- Anyone authenticated can view approved content
CREATE POLICY "View approved content"
  ON moderated_content FOR SELECT
  USING (status = 'approved');

-- Users can insert content (starts as pending)
CREATE POLICY "Users can create content"
  ON moderated_content FOR INSERT
  WITH CHECK (
    auth.uid() = author_id AND
    status = 'pending'
  );

-- Only moderators can approve
CREATE POLICY "Moderators can approve"
  ON moderated_content FOR UPDATE
  USING (auth.jwt() ->> 'role' = 'moderator')
  WITH CHECK (
    status IN ('approved', 'rejected') AND
    (OLD.status != 'approved' OR auth.jwt() ->> 'role' = 'admin')
  );
```

## Helper Functions

Reusable functions for complex RLS logic.

```sql
-- Check if user has specific role
CREATE OR REPLACE FUNCTION auth.user_has_role(required_role TEXT)
RETURNS BOOLEAN AS $$
BEGIN
  RETURN (auth.jwt() ->> 'role') = required_role;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Check tenant membership
CREATE OR REPLACE FUNCTION auth.user_in_tenant(target_tenant_id UUID)
RETURNS BOOLEAN AS $$
BEGIN
  RETURN EXISTS (
    SELECT 1 FROM user_tenants
    WHERE user_id = auth.uid() AND tenant_id = target_tenant_id
  );
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Check organization permission
CREATE OR REPLACE FUNCTION auth.user_can_access_org(org_id UUID, min_role TEXT DEFAULT 'member')
RETURNS BOOLEAN AS $$
DECLARE
  user_role TEXT;
  role_hierarchy TEXT[] := ARRAY['member', 'manager', 'admin', 'owner'];
  min_role_level INT;
  user_role_level INT;
BEGIN
  SELECT role INTO user_role
  FROM user_organizations
  WHERE user_id = auth.uid() AND organization_id = org_id;

  IF user_role IS NULL THEN
    RETURN FALSE;
  END IF;

  min_role_level := array_position(role_hierarchy, min_role);
  user_role_level := array_position(role_hierarchy, user_role);

  RETURN user_role_level >= min_role_level;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;
```

## Performance Tips

1. **Index Policy Columns**: Add indexes on columns used in policies
```sql
CREATE INDEX idx_posts_user_id ON posts(user_id);
CREATE INDEX idx_documents_tenant_id ON documents(tenant_id);
CREATE INDEX idx_files_owner_id ON files(owner_id);
```

2. **Avoid Subqueries**: Use helper functions for complex logic
```sql
-- Slow
USING (
  user_id IN (
    SELECT user_id FROM complex_query WHERE ...
  )
)

-- Faster
USING (auth.check_user_access(user_id))
```

3. **Materialized Views**: For complex hierarchical permissions
```sql
CREATE MATERIALIZED VIEW user_accessible_resources AS
SELECT user_id, resource_id, access_level
FROM ... -- complex joins

-- Refresh periodically
REFRESH MATERIALIZED VIEW user_accessible_resources;
```

## Testing RLS Policies

Always test policies with different user contexts:

```sql
-- Test as specific user
SET request.jwt.claim.sub = 'user-uuid-here';
SELECT * FROM table_name;

-- Test as specific role
SET request.jwt.claim.role = 'admin';
SELECT * FROM table_name;

-- Test insert
INSERT INTO table_name (user_id, content) VALUES (auth.uid(), 'test');

-- Reset
RESET ALL;
```

## Common Pitfalls

1. **Forgetting WITH CHECK**: INSERT/UPDATE policies need WITH CHECK clause
2. **Not enabling RLS**: ALTER TABLE ... ENABLE ROW LEVEL SECURITY is required
3. **Overly complex policies**: Keep policies simple, use helper functions
4. **Missing indexes**: Policy columns need indexes for performance
5. **Testing as superuser**: Superusers bypass RLS, test as regular users
6. **Not considering anon vs authenticated**: Different policies for public access
