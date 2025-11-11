# Zod Validation Patterns

Common Zod validation patterns for API contracts, forms, and Server Actions.

## String Validation

### Basic String Constraints

```typescript
import { z } from 'zod';

// Required string
const requiredString = z.string();

// Optional string
const optionalString = z.string().optional();

// String with length constraints
const username = z.string().min(3).max(20);

// Non-empty string
const nonEmpty = z.string().min(1);

// String with default value
const withDefault = z.string().default('default value');
```

### Common String Formats

```typescript
// Email validation
const email = z.string().email();

// URL validation
const url = z.string().url();

// UUID validation
const uuid = z.string().uuid();

// Custom regex pattern
const phoneNumber = z.string().regex(/^\+?[1-9]\d{1,14}$/);

// Alphanumeric only
const alphanumeric = z.string().regex(/^[a-zA-Z0-9]+$/);

// Trim whitespace
const trimmed = z.string().trim();

// Lowercase transformation
const lowercase = z.string().toLowerCase();
```

### Advanced String Validation

```typescript
// Custom refinement
const strongPassword = z.string()
  .min(8)
  .refine(
    (val) => /[A-Z]/.test(val) && /[a-z]/.test(val) && /[0-9]/.test(val),
    { message: 'Password must contain uppercase, lowercase, and number' }
  );

// Multiple validations with custom messages
const entityName = z.string()
  .min(1, 'Name is required')
  .max(100, 'Name must be 100 characters or less')
  .regex(/^[a-zA-Z0-9\s-]+$/, 'Name can only contain letters, numbers, spaces, and hyphens');
```

## Number Validation

```typescript
// Basic number
const age = z.number();

// Integer only
const count = z.number().int();

// Positive number
const positive = z.number().positive();

// Non-negative (>= 0)
const nonNegative = z.number().nonnegative();

// Min/max constraints
const percentage = z.number().min(0).max(100);

// Multiple of
const evenNumber = z.number().multipleOf(2);

// Finite number (not Infinity or NaN)
const finite = z.number().finite();

// Convert string to number
const stringToNumber = z.coerce.number();
```

## Boolean Validation

```typescript
// Basic boolean
const isActive = z.boolean();

// Optional boolean with default
const isPublic = z.boolean().default(false);

// Coerce to boolean (accepts "true", "false", 1, 0)
const coercedBoolean = z.coerce.boolean();
```

## Date Validation

```typescript
// Basic date
const createdAt = z.date();

// Date with min/max constraints
const futureDate = z.date().min(new Date());
const pastDate = z.date().max(new Date());

// Date range
const dateInRange = z.date()
  .min(new Date('2020-01-01'))
  .max(new Date('2030-12-31'));

// Convert string to date
const stringToDate = z.coerce.date();

// ISO date string
const isoDate = z.string().datetime();
```

## Array Validation

```typescript
// Array of strings
const tags = z.array(z.string());

// Array with length constraints
const limitedTags = z.array(z.string()).min(1).max(10);

// Non-empty array
const nonEmptyArray = z.array(z.string()).nonempty();

// Array with unique items
const uniqueTags = z.array(z.string())
  .refine((items) => new Set(items).size === items.length, {
    message: 'Tags must be unique'
  });

// Tuple (fixed-length array with different types)
const coordinate = z.tuple([z.number(), z.number()]);
```

## Object Validation

```typescript
// Basic object shape
const user = z.object({
  id: z.string().uuid(),
  name: z.string(),
  email: z.string().email(),
  age: z.number().int().positive().optional(),
});

// Nested objects
const entity = z.object({
  id: z.string(),
  name: z.string(),
  metadata: z.object({
    createdBy: z.string(),
    tags: z.array(z.string()),
  }),
});

// Partial object (all fields optional)
const partialUser = user.partial();

// Pick specific fields
const userCredentials = user.pick({ email: true, password: true });

// Omit specific fields
const publicUser = user.omit({ password: true });

// Extend object
const extendedUser = user.extend({
  role: z.string(),
});

// Merge objects
const merged = user.merge(z.object({ role: z.string() }));
```

## Union and Intersection Types

```typescript
// Union (one of multiple types)
const stringOrNumber = z.union([z.string(), z.number()]);

// Discriminated union
const result = z.discriminatedUnion('status', [
  z.object({ status: z.literal('success'), data: z.any() }),
  z.object({ status: z.literal('error'), error: z.string() }),
]);

// Intersection (combines multiple types)
const timestamped = z.object({
  createdAt: z.date(),
  updatedAt: z.date(),
});
const userWithTimestamps = z.intersection(user, timestamped);
```

## Enum and Literal Types

```typescript
// Enum
const roleEnum = z.enum(['admin', 'user', 'guest']);

// Literal
const statusLiteral = z.literal('active');

// Multiple literals (union)
const status = z.union([
  z.literal('active'),
  z.literal('inactive'),
  z.literal('pending'),
]);

// Native enum support
enum Role {
  Admin = 'admin',
  User = 'user',
  Guest = 'guest',
}
const nativeEnum = z.nativeEnum(Role);
```

## Optional and Nullable

```typescript
// Optional (can be undefined)
const optional = z.string().optional();

// Nullable (can be null)
const nullable = z.string().nullable();

// Both optional and nullable
const optionalNullable = z.string().optional().nullable();

// Nullish (undefined or null)
const nullish = z.string().nullish();
```

## Custom Error Messages

```typescript
// Field-level messages
const username = z.string({
  required_error: 'Username is required',
  invalid_type_error: 'Username must be a string',
});

// Validation-level messages
const password = z.string()
  .min(8, { message: 'Password must be at least 8 characters' })
  .max(100, { message: 'Password is too long' });

// Custom refinement with message
const ageValidation = z.number()
  .refine((val) => val >= 18, {
    message: 'Must be 18 or older',
  });
```

## Transformations

```typescript
// Transform to different type
const numberFromString = z.string().transform((val) => parseInt(val, 10));

// Preprocessing
const trimmedString = z.preprocess(
  (val) => typeof val === 'string' ? val.trim() : val,
  z.string()
);

// Chain transforms
const normalized = z.string()
  .trim()
  .toLowerCase()
  .transform((val) => val.replace(/\s+/g, '-'));
```

## Advanced Patterns

### Conditional Validation

```typescript
// Dependent fields
const formSchema = z.object({
  hasAddress: z.boolean(),
  address: z.string().optional(),
}).refine(
  (data) => !data.hasAddress || (data.hasAddress && data.address),
  { message: 'Address is required when hasAddress is true', path: ['address'] }
);
```

### Record/Map Validation

```typescript
// Record with string keys
const metadata = z.record(z.string(), z.any());

// Record with specific value type
const scores = z.record(z.string(), z.number());

// Map
const map = z.map(z.string(), z.number());
```

### Recursive Types

```typescript
// Self-referencing type (tree structure)
interface Category {
  id: string;
  name: string;
  children?: Category[];
}

const categorySchema: z.ZodType<Category> = z.lazy(() =>
  z.object({
    id: z.string(),
    name: z.string(),
    children: z.array(categorySchema).optional(),
  })
);
```

## Form Integration Patterns

### React Hook Form

```typescript
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';

const formSchema = z.object({
  name: z.string().min(1, 'Name is required'),
  email: z.string().email('Invalid email address'),
  age: z.number().int().positive().optional(),
});

type FormData = z.infer<typeof formSchema>;

function MyForm() {
  const { register, handleSubmit, formState: { errors } } = useForm<FormData>({
    resolver: zodResolver(formSchema),
  });

  const onSubmit = (data: FormData) => {
    console.log(data);
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      {/* Form fields */}
    </form>
  );
}
```

## API Validation Patterns

### Server Action with Validation

```typescript
'use server';

import { z } from 'zod';

const createEntitySchema = z.object({
  name: z.string().min(1).max(100),
  type: z.enum(['character', 'location', 'item']),
  description: z.string().optional(),
});

export async function createEntity(formData: FormData) {
  const rawData = {
    name: formData.get('name'),
    type: formData.get('type'),
    description: formData.get('description'),
  };

  // Validate with safeParse
  const result = createEntitySchema.safeParse(rawData);

  if (!result.success) {
    return {
      success: false,
      errors: result.error.flatten().fieldErrors,
    };
  }

  // Type-safe data
  const { name, type, description } = result.data;

  // Process validated data
  // ...

  return { success: true, data: { id: '123' } };
}
```

### API Route with Validation

```typescript
import { NextRequest, NextResponse } from 'next/server';
import { z } from 'zod';

const requestSchema = z.object({
  query: z.string(),
  filters: z.object({
    type: z.array(z.string()).optional(),
    tags: z.array(z.string()).optional(),
  }).optional(),
});

export async function POST(request: NextRequest) {
  const body = await request.json();

  const result = requestSchema.safeParse(body);

  if (!result.success) {
    return NextResponse.json(
      { error: 'Invalid request', details: result.error.format() },
      { status: 400 }
    );
  }

  const { query, filters } = result.data;

  // Process validated data
  // ...

  return NextResponse.json({ results: [] });
}
```

## Worldbuilding-Specific Patterns

### Entity Validation

```typescript
const entitySchema = z.object({
  id: z.string().uuid(),
  type: z.enum(['character', 'location', 'item', 'faction', 'event']),
  name: z.string().min(1).max(200),
  description: z.string().max(5000).optional(),
  tags: z.array(z.string()).max(20),
  attributes: z.record(z.string(), z.any()),
  metadata: z.object({
    createdAt: z.date(),
    updatedAt: z.date(),
    createdBy: z.string(),
  }),
});
```

### Relationship Validation

```typescript
const relationshipSchema = z.object({
  id: z.string().uuid(),
  sourceId: z.string().uuid(),
  targetId: z.string().uuid(),
  type: z.string().min(1).max(50),
  strength: z.number().min(0).max(1).optional(),
  metadata: z.record(z.string(), z.any()).optional(),
}).refine(
  (data) => data.sourceId !== data.targetId,
  { message: 'Source and target must be different entities', path: ['targetId'] }
);
```

### Timeline Event Validation

```typescript
const timelineEventSchema = z.object({
  id: z.string().uuid(),
  name: z.string().min(1).max(200),
  date: z.object({
    year: z.number().int(),
    month: z.number().int().min(1).max(12).optional(),
    day: z.number().int().min(1).max(31).optional(),
  }),
  description: z.string().max(5000).optional(),
  entityIds: z.array(z.string().uuid()),
}).refine(
  (data) => {
    if (data.date.day && !data.date.month) {
      return false;
    }
    return true;
  },
  { message: 'Month is required when day is specified', path: ['date', 'month'] }
);
```

## Best Practices

1. **Use `.safeParse()` over `.parse()`**: Prevents throwing exceptions
2. **Provide clear error messages**: Help users understand what went wrong
3. **Validate early**: At API boundaries and form submissions
4. **Use type inference**: `z.infer<typeof schema>` for TypeScript types
5. **Keep schemas colocated**: Near the code that uses them
6. **Document complex validations**: Add comments explaining business rules
7. **Test edge cases**: Empty values, boundary conditions, invalid formats
8. **Use refinements for complex logic**: When built-in validators aren't enough
9. **Consider performance**: Complex validations on large datasets may be slow
10. **Version your schemas**: When APIs evolve, maintain backward compatibility
