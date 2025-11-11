# RLS Policies Documentation: [Table Name]

**Generated**: [Date]
**Database**: [Database Name]
**Schema**: public

## Overview

This document describes the Row-Level Security (RLS) policies implemented for the `[table_name]` table.

**Security Model**: [Multi-tenant / Role-based / Hybrid / etc.]

## Table Schema

```sql
CREATE TABLE [table_name] (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES auth.users(id),
  tenant_id UUID REFERENCES tenants(id),
  [other columns...]
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);
```

**Security-relevant columns**:
- `user_id`: Owner of the record
- `tenant_id`: Tenant/organization identifier
- [other relevant columns...]

## RLS Status

```sql
-- RLS is ENABLED on this table
ALTER TABLE [table_name] ENABLE ROW LEVEL SECURITY;
```

## Policies

### Policy 1: [Policy Name]

**Operation**: SELECT | INSERT | UPDATE | DELETE | ALL
**Policy Name**: `[policy_name]`

**Purpose**: [What this policy does]

**SQL**:
```sql
CREATE POLICY "[policy_name]"
  ON [table_name] FOR [OPERATION]
  USING ([condition])
  WITH CHECK ([condition]);
```

**Access Rules**:
- [Who] can [do what] when [condition]
- Example: "Users can view records where they are the owner"
- Example: "Admins can view all records"

**Testing**:
```sql
-- Test as user [user_id]
SET request.jwt.claim.sub = '[user-uuid]';
SELECT * FROM [table_name]; -- Expected: [description]

-- Test as admin
SET request.jwt.claim.role = 'admin';
SELECT * FROM [table_name]; -- Expected: [description]
```

---

### Policy 2: [Policy Name]

[Repeat structure for each policy...]

## Access Matrix

| Role / Context | SELECT | INSERT | UPDATE | DELETE |
|---------------|--------|--------|--------|--------|
| Anonymous | No | No | No | No |
| Authenticated User | Own records | Own records | Own records | Own records |
| Team Member | Team records | Team records | Team records | No |
| Admin | All records | All records | All records | All records |

## Helper Functions

### Function: [function_name]

**Purpose**: [What this function does]

**SQL**:
```sql
CREATE OR REPLACE FUNCTION [function_name]([params])
RETURNS [type] AS $$
BEGIN
  [implementation]
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;
```

**Usage in Policies**:
```sql
USING ([function_name](param))
```

## Indexes

The following indexes support RLS policy performance:

```sql
CREATE INDEX idx_[table]_user_id ON [table_name](user_id);
CREATE INDEX idx_[table]_tenant_id ON [table_name](tenant_id);
-- [other indexes...]
```

## Permissions

```sql
-- Authenticated users can perform CRUD operations (filtered by RLS)
GRANT SELECT, INSERT, UPDATE, DELETE ON [table_name] TO authenticated;

-- Anonymous users can read public records (filtered by RLS)
GRANT SELECT ON [table_name] TO anon;

-- Sequence usage
GRANT USAGE, SELECT ON SEQUENCE [table_name]_id_seq TO authenticated;
```

## Testing Scenarios

### Scenario 1: User Access Own Records

**Setup**:
```sql
-- Create test user
INSERT INTO auth.users (id, email) VALUES
  ('user-1-uuid', 'user1@example.com');

-- Create test records
INSERT INTO [table_name] (user_id, [data])
VALUES ('user-1-uuid', 'data1');
```

**Test**:
```sql
-- Set auth context
SET request.jwt.claim.sub = 'user-1-uuid';

-- User should see own record
SELECT * FROM [table_name];
-- Expected: 1 row

-- User should not see other users' records
SELECT * FROM [table_name] WHERE user_id != 'user-1-uuid';
-- Expected: 0 rows
```

### Scenario 2: [Other scenarios...]

[Add more test scenarios as needed]

## Security Considerations

### Enforced Restrictions
- [x] Users cannot access other users' private data
- [x] Users cannot modify tenant_id after creation
- [x] Anonymous users have read-only access to public data
- [x] [Other restrictions...]

### Known Limitations
- [Any limitations or edge cases]
- [Performance considerations]
- [Future improvements needed]

## Common Issues and Troubleshooting

### Issue 1: "Permission denied for relation [table_name]"

**Cause**: RLS is enabled but no policies match the user's context.

**Solution**:
1. Verify user is authenticated: `SELECT auth.uid();`
2. Check user's role: `SELECT auth.jwt() ->> 'role';`
3. Verify policy conditions match user context

### Issue 2: Policies not applying correctly

**Cause**: Testing as superuser, which bypasses RLS.

**Solution**:
```sql
-- Test as non-superuser
SET ROLE non_superuser_role;
-- Or use Supabase client with actual auth token
```

### Issue 3: Performance degradation

**Cause**: Missing indexes on columns used in policies.

**Solution**:
```sql
-- Add indexes
CREATE INDEX idx_[table]_[column] ON [table_name]([column]);
-- Analyze table
ANALYZE [table_name];
```

## Migration History

### Initial RLS Setup
- **Date**: [Date]
- **Migration**: `[timestamp]_add_rls_policies.sql`
- **Changes**: Enabled RLS and created initial policies

### [Future updates...]

## Maintenance

### Regular Tasks
- [ ] Review policy effectiveness quarterly
- [ ] Monitor query performance
- [ ] Audit access logs for anomalies
- [ ] Update policies when roles/permissions change

### Performance Monitoring
```sql
-- Check policy execution time
EXPLAIN ANALYZE
SELECT * FROM [table_name]
WHERE [typical_condition];

-- Check index usage
SELECT schemaname, tablename, indexname, idx_scan
FROM pg_stat_user_indexes
WHERE tablename = '[table_name]';
```

## References

- Supabase RLS Documentation: https://supabase.com/docs/guides/auth/row-level-security
- PostgreSQL RLS Policies: https://www.postgresql.org/docs/current/ddl-rowsecurity.html
- Auth Functions: https://supabase.com/docs/guides/database/postgres/row-level-security

## Change Log

| Date | Author | Change |
|------|--------|--------|
| [Date] | [Name] | Initial policies created |
| [Date] | [Name] | Added admin access policy |
| ... | ... | ... |
