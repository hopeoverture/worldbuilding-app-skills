# Prisma Best Practices

## Schema Design

### Naming Conventions

**Models**: PascalCase, singular
```prisma
model User { }  // [OK] Good
model users { } // [ERROR] Bad
```

**Fields**: camelCase
```prisma
model User {
  createdAt DateTime  // [OK] Good
  created_at DateTime // [ERROR] Bad (unless mapping to existing DB)
}
```

**Database names**: snake_case with `@@map` and `@map`
```prisma
model Profile {
  avatarUrl String @map("avatar_url")
  @@map("profiles")
}
```

### ID Fields

**Prefer UUIDs for distributed systems:**
```prisma
id String @id @default(uuid()) @db.Uuid
```

**Use auto-increment for simple cases:**
```prisma
id Int @id @default(autoincrement())
```

### Timestamps

Always include creation and update timestamps:
```prisma
createdAt DateTime @default(now()) @map("created_at")
updatedAt DateTime @updatedAt @map("updated_at")
```

### Indexes

Add indexes on:
- Foreign keys (automatically indexed)
- Frequently queried fields
- Unique constraints
- Compound queries

```prisma
model Post {
  authorId String @db.Uuid
  published Boolean
  publishedAt DateTime?

  @@index([authorId])
  @@index([published, publishedAt])
}
```

### Relations

**One-to-many:**
```prisma
model User {
  posts Post[]
}

model Post {
  authorId String @db.Uuid
  author   User   @relation(fields: [authorId], references: [id])

  @@index([authorId])
}
```

**Many-to-many:**
```prisma
model Post {
  tags PostTag[]
}

model Tag {
  posts PostTag[]
}

model PostTag {
  postId String @db.Uuid
  post   Post   @relation(fields: [postId], references: [id])

  tagId  String @db.Uuid
  tag    Tag    @relation(fields: [tagId], references: [id])

  @@id([postId, tagId])
}
```

**Cascade deletes:**
```prisma
author User @relation(fields: [authorId], references: [id], onDelete: Cascade)
```

## Query Optimization

### Select Only Needed Fields

```typescript
// [ERROR] Bad - fetches all fields
const users = await prisma.user.findMany();

// [OK] Good - only fetch what you need
const users = await prisma.user.findMany({
  select: {
    id: true,
    name: true,
    email: true,
  },
});
```

### Use Include Wisely

```typescript
// [ERROR] Bad - deep nesting can be slow
const posts = await prisma.post.findMany({
  include: {
    author: {
      include: {
        profile: {
          include: {
            settings: true,
          },
        },
      },
    },
  },
});

// [OK] Good - only include what you display
const posts = await prisma.post.findMany({
  include: {
    author: {
      select: {
        id: true,
        name: true,
      },
    },
  },
});
```

### Pagination

Always paginate large result sets:

```typescript
// Offset pagination
const posts = await prisma.post.findMany({
  skip: 20,
  take: 10,
});

// Cursor-based pagination (better for large datasets)
const posts = await prisma.post.findMany({
  take: 10,
  cursor: {
    id: lastPostId,
  },
});
```

### Batch Operations

Use batch operations for bulk inserts/updates:

```typescript
// [OK] Single query instead of N queries
await prisma.user.createMany({
  data: [
    { email: 'user1@example.com', name: 'User 1' },
    { email: 'user2@example.com', name: 'User 2' },
  ],
  skipDuplicates: true,
});
```

## Connection Management

### Singleton Pattern (Next.js)

Prevent connection exhaustion in development:

```typescript
// lib/prisma.ts
import { PrismaClient } from '@prisma/client';

const globalForPrisma = globalThis as unknown as {
  prisma: PrismaClient | undefined;
};

export const prisma = globalForPrisma.prisma ?? new PrismaClient();

if (process.env.NODE_ENV !== 'production') {
  globalForPrisma.prisma = prisma;
}
```

### Connection Pooling

Use Supabase connection pooler for better performance:

```prisma
datasource db {
  provider  = "postgresql"
  url       = env("DIRECT_URL")       // Pooled connection
  directUrl = env("DATABASE_URL")     // Direct for migrations
}
```

## Migration Best Practices

### 1. Review Generated SQL

Always check `migration.sql` before applying:
```bash
npx prisma migrate dev --name add_users --create-only
# Review prisma/migrations/.../migration.sql
npx prisma migrate dev
```

### 2. Atomic Migrations

One logical change per migration:
- [OK] Good: "add_user_roles"
- [ERROR] Bad: "add_users_and_posts_and_comments"

### 3. Production Migrations

Use `migrate deploy` in production:
```bash
npx prisma migrate deploy
```

Never use `migrate dev` or `migrate reset` in production.

### 4. Handle Data Migrations

For complex data transformations, use multi-step migrations:

```sql
-- Step 1: Add new column with default
ALTER TABLE "User" ADD COLUMN "full_name" TEXT;

-- Step 2: Populate from existing data
UPDATE "User" SET "full_name" = "first_name" || ' ' || "last_name";

-- Step 3: Make non-nullable
ALTER TABLE "User" ALTER COLUMN "full_name" SET NOT NULL;
```

### 5. Rollback Strategy

Migrations can't be rolled back automatically. Plan for:
- Backup before major migrations
- Keep old columns temporarily
- Deploy in stages

## Error Handling

### Handle Unique Constraint Violations

```typescript
try {
  await prisma.user.create({
    data: { email: 'test@example.com' },
  });
} catch (error) {
  if (error.code === 'P2002') {
    // Unique constraint violation
    throw new Error('Email already exists');
  }
  throw error;
}
```

### Use Transactions

For operations that must succeed or fail together:

```typescript
await prisma.$transaction(async (tx) => {
  const user = await tx.user.create({
    data: { email: 'test@example.com' },
  });

  await tx.profile.create({
    data: {
      userId: user.id,
      bio: 'New user',
    },
  });
});
```

## TypeScript Integration

### Leverage Generated Types

```typescript
import { Prisma } from '@prisma/client';

// Use generated types for input
type UserCreateInput = Prisma.UserCreateInput;

// Type-safe queries
const where: Prisma.UserWhereInput = {
  email: {
    contains: '@example.com',
  },
};
```

### Type Query Results

```typescript
// Get inferred type from query
const user = await prisma.user.findUnique({
  where: { id: '1' },
  include: { posts: true },
});

type UserWithPosts = typeof user;
```

## Common Pitfalls

### 1. N+1 Query Problem

```typescript
// [ERROR] Bad - N+1 queries
const posts = await prisma.post.findMany();
for (const post of posts) {
  const author = await prisma.user.findUnique({
    where: { id: post.authorId },
  });
}

// [OK] Good - single query with include
const posts = await prisma.post.findMany({
  include: { author: true },
});
```

### 2. Not Using Transactions

```typescript
// [ERROR] Bad - can leave inconsistent state
await prisma.user.create({ data: userData });
await prisma.profile.create({ data: profileData }); // If this fails, user exists without profile

// [OK] Good - atomic operation
await prisma.$transaction([
  prisma.user.create({ data: userData }),
  prisma.profile.create({ data: profileData }),
]);
```

### 3. Exposing Prisma Client to Frontend

```typescript
// [ERROR] Bad - never import Prisma in client components
'use client';
import { prisma } from '@/lib/prisma'; // Security risk!

// [OK] Good - use Server Actions or API routes
'use server';
import { prisma } from '@/lib/prisma';
export async function getUsers() {
  return await prisma.user.findMany();
}
```

### 4. Ignoring Soft Deletes

```prisma
model User {
  deletedAt DateTime? @map("deleted_at")
}

// Query only non-deleted
const activeUsers = await prisma.user.findMany({
  where: { deletedAt: null },
});
```

## Performance Tips

1. **Use indexes** on filtered/sorted fields
2. **Limit result sets** with take/skip
3. **Select only needed fields** to reduce data transfer
4. **Use connection pooling** for serverless environments
5. **Batch operations** instead of loops
6. **Cache frequent queries** at application level
7. **Monitor slow queries** in Supabase dashboard
8. **Use database views** for complex, repeated queries
