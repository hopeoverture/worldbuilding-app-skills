-- Supabase RLS Policy Templates
-- Copy and adapt these templates for your tables

-- ============================================================================
-- TEMPLATE 1: User Ownership (Basic)
-- ============================================================================
-- Use when: Users can only access their own records
-- Tables: user_profiles, user_settings, user_preferences

ALTER TABLE table_name ENABLE ROW LEVEL SECURITY;

CREATE POLICY "users_select_own"
  ON table_name FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "users_insert_own"
  ON table_name FOR INSERT
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "users_update_own"
  ON table_name FOR UPDATE
  USING (auth.uid() = user_id)
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "users_delete_own"
  ON table_name FOR DELETE
  USING (auth.uid() = user_id);

-- ============================================================================
-- TEMPLATE 2: Multi-Tenant Isolation
-- ============================================================================
-- Use when: Multiple tenants/organizations sharing the database
-- Tables: documents, projects, team_data

ALTER TABLE table_name ENABLE ROW LEVEL SECURITY;

-- Assumes a user_tenants junction table
CREATE POLICY "tenant_isolation"
  ON table_name FOR ALL
  USING (
    tenant_id IN (
      SELECT tenant_id FROM user_tenants
      WHERE user_id = auth.uid()
    )
  );

-- Alternative: Using JWT claim for tenant ID
CREATE POLICY "tenant_isolation_jwt"
  ON table_name FOR ALL
  USING (
    tenant_id = (auth.jwt() -> 'app_metadata' ->> 'tenant_id')::uuid
  );

-- ============================================================================
-- TEMPLATE 3: Role-Based Access Control (Simple)
-- ============================================================================
-- Use when: Different access based on user roles
-- Tables: admin_settings, moderation_queue

ALTER TABLE table_name ENABLE ROW LEVEL SECURITY;

-- Admins can do everything
CREATE POLICY "admins_all_access"
  ON table_name FOR ALL
  USING (auth.jwt() ->> 'role' = 'admin');

-- Regular users can only read
CREATE POLICY "users_read_only"
  ON table_name FOR SELECT
  USING (auth.jwt() ->> 'role' = 'authenticated');

-- ============================================================================
-- TEMPLATE 4: Role-Based with Ownership Fallback
-- ============================================================================
-- Use when: Users can access own records, admins can access all
-- Tables: posts, comments, submissions

ALTER TABLE table_name ENABLE ROW LEVEL SECURITY;

CREATE POLICY "select_own_or_admin"
  ON table_name FOR SELECT
  USING (
    auth.uid() = user_id OR
    auth.jwt() ->> 'role' = 'admin'
  );

CREATE POLICY "insert_own"
  ON table_name FOR INSERT
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "update_own_or_admin"
  ON table_name FOR UPDATE
  USING (
    auth.uid() = user_id OR
    auth.jwt() ->> 'role' = 'admin'
  );

CREATE POLICY "delete_own_or_admin"
  ON table_name FOR DELETE
  USING (
    auth.uid() = user_id OR
    auth.jwt() ->> 'role' = 'admin'
  );

-- ============================================================================
-- TEMPLATE 5: Public/Private Resources
-- ============================================================================
-- Use when: Some records are public, others are private
-- Tables: articles, galleries, portfolios

ALTER TABLE table_name ENABLE ROW LEVEL SECURITY;

-- Everyone (including anon) can view public records
CREATE POLICY "public_records_viewable"
  ON table_name FOR SELECT
  USING (is_public = true);

-- Authenticated users can view own private records
CREATE POLICY "private_records_owner"
  ON table_name FOR SELECT
  USING (
    is_public = false AND
    auth.uid() = user_id
  );

-- Only owner can modify
CREATE POLICY "owner_can_modify"
  ON table_name FOR UPDATE
  USING (auth.uid() = user_id);

CREATE POLICY "owner_can_delete"
  ON table_name FOR DELETE
  USING (auth.uid() = user_id);

-- ============================================================================
-- TEMPLATE 6: Hierarchical Permissions (Organization/Team)
-- ============================================================================
-- Use when: Organization > Team > User hierarchy
-- Tables: projects, resources, team_documents

ALTER TABLE table_name ENABLE ROW LEVEL SECURITY;

-- Organization admins see all
CREATE POLICY "org_admin_all"
  ON table_name FOR ALL
  USING (
    organization_id IN (
      SELECT organization_id FROM user_organizations
      WHERE user_id = auth.uid() AND role = 'admin'
    )
  );

-- Team members see team records
CREATE POLICY "team_member_access"
  ON table_name FOR SELECT
  USING (
    team_id IN (
      SELECT team_id FROM user_teams
      WHERE user_id = auth.uid()
    )
  );

-- Owner always has access
CREATE POLICY "owner_access"
  ON table_name FOR ALL
  USING (auth.uid() = owner_id);

-- ============================================================================
-- TEMPLATE 7: Shared Resources
-- ============================================================================
-- Use when: Resources can be shared with specific users
-- Tables: files, documents, notes

ALTER TABLE table_name ENABLE ROW LEVEL SECURITY;

-- Owner can do everything
CREATE POLICY "owner_full_access"
  ON table_name FOR ALL
  USING (auth.uid() = owner_id);

-- Shared users can read (and maybe write)
CREATE POLICY "shared_users_read"
  ON table_name FOR SELECT
  USING (
    EXISTS (
      SELECT 1 FROM table_name_shares
      WHERE resource_id = table_name.id
      AND user_id = auth.uid()
      AND (expires_at IS NULL OR expires_at > NOW())
    )
  );

-- Shared users with write permission can update
CREATE POLICY "shared_users_write"
  ON table_name FOR UPDATE
  USING (
    EXISTS (
      SELECT 1 FROM table_name_shares
      WHERE resource_id = table_name.id
      AND user_id = auth.uid()
      AND can_write = true
      AND (expires_at IS NULL OR expires_at > NOW())
    )
  );

-- ============================================================================
-- TEMPLATE 8: Time-Based Access
-- ============================================================================
-- Use when: Content has publish/expire dates
-- Tables: scheduled_posts, campaigns, events

ALTER TABLE table_name ENABLE ROW LEVEL SECURITY;

-- Published content is viewable
CREATE POLICY "view_published"
  ON table_name FOR SELECT
  USING (
    status = 'published' AND
    (published_at IS NULL OR published_at <= NOW()) AND
    (expires_at IS NULL OR expires_at > NOW())
  );

-- Authors can view all states
CREATE POLICY "author_view_all"
  ON table_name FOR SELECT
  USING (auth.uid() = author_id);

-- Authors can update before published
CREATE POLICY "author_update_unpublished"
  ON table_name FOR UPDATE
  USING (
    auth.uid() = author_id AND
    (status = 'draft' OR published_at > NOW())
  );

-- ============================================================================
-- TEMPLATE 9: Cascading Permissions (Parent/Child)
-- ============================================================================
-- Use when: Child records inherit permissions from parent
-- Tables: comments (child of posts), task_items (child of tasks)

-- Parent table
ALTER TABLE parent_table ENABLE ROW LEVEL SECURITY;

CREATE POLICY "parent_access"
  ON parent_table FOR SELECT
  USING (
    auth.uid() = owner_id OR
    is_public = true
  );

-- Child table inherits from parent
ALTER TABLE child_table ENABLE ROW LEVEL SECURITY;

CREATE POLICY "child_inherit_from_parent"
  ON child_table FOR SELECT
  USING (
    parent_id IN (
      SELECT id FROM parent_table
      WHERE auth.uid() = owner_id OR is_public = true
    )
  );

-- ============================================================================
-- TEMPLATE 10: Moderation/Approval Workflow
-- ============================================================================
-- Use when: Content needs approval before being visible
-- Tables: user_submissions, comments, reviews

ALTER TABLE table_name ENABLE ROW LEVEL SECURITY;

-- Users can view approved content
CREATE POLICY "view_approved"
  ON table_name FOR SELECT
  USING (status = 'approved');

-- Users can view own content in any state
CREATE POLICY "view_own"
  ON table_name FOR SELECT
  USING (auth.uid() = author_id);

-- Users can create content (starts as pending)
CREATE POLICY "create_as_pending"
  ON table_name FOR INSERT
  WITH CHECK (
    auth.uid() = author_id AND
    status = 'pending'
  );

-- Users can edit own pending content
CREATE POLICY "update_own_pending"
  ON table_name FOR UPDATE
  USING (
    auth.uid() = author_id AND
    status = 'pending'
  );

-- Moderators can update status
CREATE POLICY "moderators_approve"
  ON table_name FOR UPDATE
  USING (auth.jwt() ->> 'role' IN ('moderator', 'admin'))
  WITH CHECK (status IN ('approved', 'rejected'));

-- ============================================================================
-- HELPER FUNCTIONS
-- ============================================================================

-- Check if user has specific role
CREATE OR REPLACE FUNCTION auth.user_has_role(required_role TEXT)
RETURNS BOOLEAN AS $$
BEGIN
  RETURN (auth.jwt() ->> 'role') = required_role;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Check if user is in tenant
CREATE OR REPLACE FUNCTION auth.user_in_tenant(target_tenant_id UUID)
RETURNS BOOLEAN AS $$
BEGIN
  RETURN EXISTS (
    SELECT 1 FROM user_tenants
    WHERE user_id = auth.uid() AND tenant_id = target_tenant_id
  );
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Check team membership
CREATE OR REPLACE FUNCTION auth.user_in_team(target_team_id UUID)
RETURNS BOOLEAN AS $$
BEGIN
  RETURN EXISTS (
    SELECT 1 FROM user_teams
    WHERE user_id = auth.uid() AND team_id = target_team_id
  );
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Check organization role
CREATE OR REPLACE FUNCTION auth.user_org_role(org_id UUID)
RETURNS TEXT AS $$
DECLARE
  user_role TEXT;
BEGIN
  SELECT role INTO user_role
  FROM user_organizations
  WHERE user_id = auth.uid() AND organization_id = org_id;

  RETURN user_role;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Check if user can access resource
CREATE OR REPLACE FUNCTION auth.can_access_resource(
  resource_owner_id UUID,
  resource_is_public BOOLEAN DEFAULT false
)
RETURNS BOOLEAN AS $$
BEGIN
  RETURN (
    auth.uid() = resource_owner_id OR
    resource_is_public = true OR
    auth.jwt() ->> 'role' = 'admin'
  );
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- ============================================================================
-- INDEXES FOR PERFORMANCE
-- ============================================================================

-- Always index columns used in RLS policies
CREATE INDEX IF NOT EXISTS idx_table_user_id ON table_name(user_id);
CREATE INDEX IF NOT EXISTS idx_table_tenant_id ON table_name(tenant_id);
CREATE INDEX IF NOT EXISTS idx_table_owner_id ON table_name(owner_id);
CREATE INDEX IF NOT EXISTS idx_table_is_public ON table_name(is_public);
CREATE INDEX IF NOT EXISTS idx_table_status ON table_name(status);
CREATE INDEX IF NOT EXISTS idx_table_published_at ON table_name(published_at);

-- Composite indexes for common queries
CREATE INDEX IF NOT EXISTS idx_table_user_status
  ON table_name(user_id, status);
CREATE INDEX IF NOT EXISTS idx_table_tenant_created
  ON table_name(tenant_id, created_at DESC);

-- ============================================================================
-- GRANT PERMISSIONS
-- ============================================================================

-- Grant table access to authenticated users
GRANT SELECT, INSERT, UPDATE, DELETE ON table_name TO authenticated;

-- Grant read-only to anonymous for public content
GRANT SELECT ON table_name TO anon;

-- Grant usage on sequences
GRANT USAGE, SELECT ON SEQUENCE table_name_id_seq TO authenticated;
