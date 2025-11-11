# Supabase Integration with Prisma

## Connection Configuration

### Database URLs

Supabase provides two types of connection strings:

**Direct Connection (Port 5432)** - For migrations:
```env
DATABASE_URL="postgresql://postgres:[PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres"
```

**Pooled Connection (Port 6543)** - For queries via pgBouncer:
```env
DIRECT_URL="postgresql://postgres:[PASSWORD]@db.[PROJECT-REF].supabase.co:6543/postgres?pgbouncer=true"
```

**Schema configuration:**
```prisma
datasource db {
  provider  = "postgresql"
  url       = env("DIRECT_URL")       // Pooled for app queries
  directUrl = env("DATABASE_URL")     // Direct for migrations
}
```

### Why Two Connections?

- **Direct (5432)**: Supports all PostgreSQL features, required for migrations
- **Pooled (6543)**: Better performance, connection pooling, but limited features
- Prisma uses direct for migrations, pooled for queries

## Row Level Security (RLS) Considerations

### Prisma vs Supabase Auth

**Key concept**: Prisma connects as the `postgres` user, which **bypasses RLS policies**.

This means:
- Prisma can read/write all data regardless of RLS
- Use Prisma in Server Components/Actions where you control access
- RLS still protects data accessed via Supabase client

### Using Prisma with RLS

For RLS to work with Prisma, you need to set the user context:

```typescript
import { prisma } from '@/lib/prisma';
import { getCurrentUser } from '@/lib/auth/utils';

export async function getUserPosts() {
  const user = await getCurrentUser();

  // Set RLS context (requires custom configuration)
  await prisma.$executeRaw`SET LOCAL rls.user_id = ${user.id}`;

  // Now RLS policies can use current_setting('rls.user_id')
  const posts = await prisma.post.findMany();

  return posts;
}
```

**Better approach**: Use Prisma for admin operations, Supabase client for user operations:

```typescript
// Admin operation - bypasses RLS
import { prisma } from '@/lib/prisma';
await prisma.post.findMany(); // Gets all posts

// User operation - respects RLS
import { createServerClient } from '@/lib/supabase/server';
const supabase = await createServerClient();
const { data } = await supabase.from('posts').select('*'); // Only user's posts
```

## Schema Management

### Prisma Manages Schema

Use Prisma as source of truth for schema:

```bash
# 1. Update schema.prisma
# 2. Generate migration
npx prisma migrate dev --name add_posts

# 3. Migration is applied to Supabase database
```

### Supabase Features

Some Supabase features are managed outside Prisma:

**RLS Policies** - Define in Supabase dashboard or SQL:
```sql
CREATE POLICY "Users can view own posts"
ON posts FOR SELECT
USING (auth.uid() = author_id);
```

**Storage Buckets** - Use Supabase dashboard/API

**Realtime** - Configure in Supabase dashboard

**Edge Functions** - Deploy separately

### Hybrid Approach

1. Use Prisma for schema, migrations, and admin operations
2. Use Supabase client for user-facing operations with RLS
3. Define RLS policies separately from Prisma

## Working with Supabase Auth

### Linking to auth.users

Don't create foreign key to `auth.users` (different schema):

```prisma
model Profile {
  id    String @id @db.Uuid  // Same as auth.users.id
  email String @unique

  // No foreign key to auth.users - different schema
}
```

**Create profile on signup** via database trigger:

```sql
-- Create profile when user signs up
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
  INSERT INTO public.profiles (id, email)
  VALUES (NEW.id, NEW.email);
  RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW
  EXECUTE FUNCTION public.handle_new_user();
```

### Syncing Profile Data

Keep profiles in sync with auth.users:

```sql
-- Update profile when email changes
CREATE OR REPLACE FUNCTION public.handle_user_update()
RETURNS TRIGGER AS $$
BEGIN
  UPDATE public.profiles
  SET email = NEW.email
  WHERE id = NEW.id;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE TRIGGER on_auth_user_updated
  AFTER UPDATE ON auth.users
  FOR EACH ROW
  WHEN (OLD.email IS DISTINCT FROM NEW.email)
  EXECUTE FUNCTION public.handle_user_update();
```

## Migrations in Supabase

### Local Development

1. Pull current schema from Supabase:
```bash
npx prisma db pull
```

2. Make changes to schema.prisma

3. Create migration:
```bash
npx prisma migrate dev --name my_changes
```

### Production Deployment

Apply migrations during deployment:

```bash
npx prisma migrate deploy
```

**GitHub Actions example:**
```yaml
- name: Run Prisma migrations
  run: npx prisma migrate deploy
  env:
    DATABASE_URL: ${{ secrets.SUPABASE_DATABASE_URL }}
```

### Migration History

Prisma creates `_prisma_migrations` table to track applied migrations. Don't modify this table.

## Realtime with Prisma

Supabase Realtime works with Prisma-managed tables:

1. Create table via Prisma migration
2. Enable realtime in Supabase dashboard for specific tables
3. Subscribe to changes via Supabase client

```typescript
// Enable realtime on a table (in SQL editor or dashboard)
ALTER PUBLICATION supabase_realtime ADD TABLE posts;

// Subscribe to changes
const supabase = createClient();
const channel = supabase
  .channel('posts')
  .on('postgres_changes', { event: '*', schema: 'public', table: 'posts' },
    (payload) => {
      console.log('Change received!', payload);
    }
  )
  .subscribe();
```

## Environment Setup

### Development

```env
# .env.local
DATABASE_URL="postgresql://postgres:postgres@localhost:54322/postgres"
DIRECT_URL="postgresql://postgres:postgres@localhost:54322/postgres"
```

### Staging/Production

```env
# .env.production
DATABASE_URL="postgresql://postgres:[PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres"
DIRECT_URL="postgresql://postgres:[PASSWORD]@db.[PROJECT-REF].supabase.co:6543/postgres?pgbouncer=true"
```

## Best Practices

1. **Use Prisma for schema management** - Single source of truth
2. **Use Supabase client for RLS-protected queries** - User-facing operations
3. **Use Prisma for admin operations** - Bulk updates, analytics
4. **Define RLS policies separately** - Not managed by Prisma
5. **Use triggers for auth.users integration** - Auto-create profiles
6. **Enable realtime selectively** - Only on tables that need it
7. **Test migrations locally first** - Use Supabase CLI for local dev
8. **Monitor connection pool** - Use pooled connection for queries

## Troubleshooting

**Migration fails with permission error**: Ensure DATABASE_URL uses postgres user with sufficient privileges.

**RLS blocks Prisma queries**: This is expected. Use Supabase client for RLS-protected data.

**Connection pool exhausted**: Use pooled connection (DIRECT_URL) for application queries.

**Realtime not working**: Check table is published (`ALTER PUBLICATION supabase_realtime ADD TABLE tablename`).

**Auth user ID doesn't match profile**: Ensure trigger exists and is executed on user creation.

## Supabase CLI Integration

Use Supabase CLI for local development:

```bash
# Start local Supabase
npx supabase start

# Link to remote project
npx supabase link --project-ref your-project-ref

# Pull remote schema
npx supabase db pull

# Generate types for Supabase client
npx supabase gen types typescript --local > types/database.ts
```

Prisma and Supabase CLI can coexist:
- Prisma for schema management and migrations
- Supabase CLI for local development and type generation
