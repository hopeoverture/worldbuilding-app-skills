# Zod Validation Reference

## Basic Types

### Strings

```typescript
// Basic string
z.string()

// With constraints
z.string().min(3, "Minimum 3 characters")
z.string().max(100, "Maximum 100 characters")
z.string().length(10, "Must be exactly 10 characters")

// Email
z.string().email("Invalid email address")

// URL
z.string().url("Invalid URL")

// UUID
z.string().uuid("Invalid UUID")

// CUID
z.string().cuid("Invalid CUID")

// Regex pattern
z.string().regex(/^[a-zA-Z]+$/, "Letters only")

// DateTime ISO
z.string().datetime("Invalid datetime")

// IP Address
z.string().ip("Invalid IP address")
z.string().ip({ version: 'v4' }) // IPv4 only
z.string().ip({ version: 'v6' }) // IPv6 only

// Trim whitespace
z.string().trim()

// Transform to lowercase
z.string().toLowerCase()

// Transform to uppercase
z.string().toUpperCase()

// Empty strings as null
z.string().nullable()

// Starts with
z.string().startsWith("prefix", "Must start with 'prefix'")

// Ends with
z.string().endsWith("suffix", "Must end with 'suffix'")

// Includes
z.string().includes("substring", "Must contain 'substring'")
```

### Numbers

```typescript
// Basic number
z.number()

// Integer only
z.number().int("Must be an integer")

// Positive numbers
z.number().positive("Must be positive")

// Non-negative (includes 0)
z.number().nonnegative("Must be 0 or greater")

// Negative numbers
z.number().negative("Must be negative")

// Non-positive (includes 0)
z.number().nonpositive("Must be 0 or less")

// Range
z.number().min(0, "Minimum is 0")
z.number().max(100, "Maximum is 100")
z.number().gte(0).lte(100) // Greater/less than or equal

// Multiple of
z.number().multipleOf(5, "Must be multiple of 5")

// Finite (not Infinity or NaN)
z.number().finite("Must be finite")

// Safe integer
z.number().safe("Must be safe integer")
```

### Booleans

```typescript
// Basic boolean
z.boolean()

// Coerce from string
z.coerce.boolean() // "true", "false", "1", "0" → boolean
```

### Dates

```typescript
// Date object
z.date()

// Min/max dates
z.date().min(new Date("2020-01-01"), "Too early")
z.date().max(new Date("2030-12-31"), "Too late")

// Coerce from string or number
z.coerce.date()
```

### Enums

```typescript
// String enum
z.enum(['character', 'location', 'item'])

// With error message
z.enum(['character', 'location', 'item'], {
  errorMap: () => ({ message: "Invalid entity type" })
})

// Native enum
enum Role {
  Admin = 'ADMIN',
  User = 'USER'
}
z.nativeEnum(Role)
```

### Literals

```typescript
// Single literal value
z.literal('admin')
z.literal(42)
z.literal(true)

// Union of literals
z.union([
  z.literal('small'),
  z.literal('medium'),
  z.literal('large')
])
```

## Complex Types

### Objects

```typescript
// Basic object
z.object({
  name: z.string(),
  age: z.number()
})

// Nested objects
z.object({
  user: z.object({
    name: z.string(),
    email: z.string().email()
  }),
  address: z.object({
    street: z.string(),
    city: z.string()
  })
})

// Optional properties
z.object({
  name: z.string(),
  nickname: z.string().optional()
})

// Partial (all properties optional)
const schema = z.object({ name: z.string(), age: z.number() })
const partialSchema = schema.partial()

// Pick specific keys
schema.pick({ name: true })

// Omit specific keys
schema.omit({ age: true })

// Extend object
const baseSchema = z.object({ name: z.string() })
const extendedSchema = baseSchema.extend({
  age: z.number()
})

// Merge objects
const merged = schema1.merge(schema2)

// Passthrough (allow unknown keys)
z.object({ name: z.string() }).passthrough()

// Strict (reject unknown keys)
z.object({ name: z.string() }).strict()

// Catchall (type for unknown keys)
z.object({ name: z.string() }).catchall(z.string())
```

### Arrays

```typescript
// Basic array
z.array(z.string())

// Array with min/max length
z.array(z.string()).min(1, "At least one item required")
z.array(z.string()).max(10, "Maximum 10 items")
z.array(z.string()).length(5, "Must have exactly 5 items")

// Non-empty array
z.array(z.string()).nonempty("Cannot be empty")

// Array of objects
z.array(z.object({
  id: z.string(),
  name: z.string()
}))
```

### Tuples

```typescript
// Fixed-length array with specific types
z.tuple([z.string(), z.number(), z.boolean()])

// With rest parameter
z.tuple([z.string(), z.number()]).rest(z.string())
```

### Records

```typescript
// Object with string keys and specific value type
z.record(z.string()) // Record<string, string>
z.record(z.number()) // Record<string, number>

// With specific key type
z.record(z.enum(['a', 'b', 'c']), z.number())
```

### Maps & Sets

```typescript
// Map
z.map(z.string(), z.number()) // Map<string, number>

// Set
z.set(z.string()) // Set<string>
z.set(z.number()).min(3, "At least 3 items")
```

### Unions

```typescript
// Union of types
z.union([z.string(), z.number()])

// Discriminated union
z.discriminatedUnion('type', [
  z.object({ type: z.literal('character'), race: z.string() }),
  z.object({ type: z.literal('location'), region: z.string() })
])
```

### Intersections

```typescript
// Combine multiple schemas
const Name = z.object({ name: z.string() })
const Age = z.object({ age: z.number() })
const Person = z.intersection(Name, Age)
// or
const Person = Name.and(Age)
```

## Optional and Nullable

```typescript
// Optional (can be undefined)
z.string().optional() // string | undefined

// Nullable (can be null)
z.string().nullable() // string | null

// Both
z.string().nullish() // string | null | undefined

// With default value
z.string().default("default value")
z.number().default(0)

// Default from function
z.date().default(() => new Date())
```

## Refinements

### Basic Refinement

```typescript
// Custom validation
z.string().refine(
  (val) => val.length > 5,
  { message: "Must be more than 5 characters" }
)

// Multiple refinements
z.string()
  .refine((val) => val.includes('@'), "Must include @")
  .refine((val) => val.endsWith('.com'), "Must end with .com")
```

### Async Refinement

```typescript
z.string().refine(
  async (username) => {
    const exists = await checkUsername(username)
    return !exists
  },
  { message: "Username already taken" }
)
```

### Cross-Field Validation

```typescript
z.object({
  password: z.string().min(8),
  confirmPassword: z.string()
}).refine(
  (data) => data.password === data.confirmPassword,
  {
    message: "Passwords must match",
    path: ["confirmPassword"] // Error shown on this field
  }
)

// Multiple cross-field validations
z.object({
  startDate: z.date(),
  endDate: z.date(),
  type: z.enum(['event', 'period'])
}).refine(
  (data) => data.startDate < data.endDate,
  {
    message: "End date must be after start date",
    path: ["endDate"]
  }
).refine(
  (data) => {
    if (data.type === 'event') {
      return data.startDate.getTime() === data.endDate.getTime()
    }
    return true
  },
  {
    message: "Events must have same start and end date",
    path: ["endDate"]
  }
)
```

### Superrefine (Advanced)

```typescript
z.object({
  age: z.number(),
  faction: z.string()
}).superrefine((data, ctx) => {
  if (data.age < 18 && data.faction === 'military') {
    ctx.addIssue({
      code: z.ZodIssueCode.custom,
      message: "Must be 18+ to join military",
      path: ["age"]
    })
  }

  if (data.age > 1000 && !data.faction.startsWith('ancient')) {
    ctx.addIssue({
      code: z.ZodIssueCode.custom,
      message: "Ancient beings must join ancient factions",
      path: ["faction"]
    })
  }
})
```

## Transformations

```typescript
// Transform string to number
z.string().transform((val) => parseInt(val))

// Transform and validate
z.string()
  .transform((val) => val.trim())
  .pipe(z.string().min(1))

// Transform dates
z.string().transform((val) => new Date(val))

// Coerce types
z.coerce.number() // "123" → 123
z.coerce.boolean() // "true" → true
z.coerce.date() // "2023-01-01" → Date

// Chain transformations
z.string()
  .transform((val) => val.trim())
  .transform((val) => val.toLowerCase())
  .transform((val) => val.split(','))
```

## Preprocess

```typescript
// Transform before validation
z.preprocess(
  (val) => {
    if (typeof val === 'string') {
      return val.trim()
    }
    return val
  },
  z.string().min(1)
)

// Normalize dates
z.preprocess(
  (val) => {
    if (val instanceof Date) return val
    if (typeof val === 'string') return new Date(val)
    return val
  },
  z.date()
)
```

## Custom Error Messages

```typescript
// Field-level messages
z.string({
  required_error: "Name is required",
  invalid_type_error: "Name must be a string"
})

// Constraint messages
z.string()
  .min(3, { message: "Minimum 3 characters" })
  .max(100, { message: "Maximum 100 characters" })

// Error map for entire schema
const schema = z.object({
  name: z.string(),
  age: z.number()
}, {
  errorMap: (issue, ctx) => {
    if (issue.code === z.ZodIssueCode.invalid_type) {
      return { message: "Please provide a valid value" }
    }
    return { message: ctx.defaultError }
  }
})
```

## Parsing and Validation

```typescript
// Parse (throws on error)
try {
  const result = schema.parse(data)
  // result is typed
} catch (error) {
  if (error instanceof z.ZodError) {
    console.log(error.errors)
  }
}

// Safe parse (returns result object)
const result = schema.safeParse(data)

if (result.success) {
  console.log(result.data) // typed data
} else {
  console.log(result.error) // ZodError
}

// Parse async
const result = await schema.parseAsync(data)

// Safe parse async
const result = await schema.safeParseAsync(data)
```

## Error Handling

```typescript
// Get all errors
const result = schema.safeParse(data)
if (!result.success) {
  result.error.issues.forEach(issue => {
    console.log(issue.path) // ['field', 'name']
    console.log(issue.message) // "Invalid value"
    console.log(issue.code) // ZodIssueCode
  })
}

// Flatten errors for forms
const result = schema.safeParse(data)
if (!result.success) {
  const flattened = result.error.flatten()
  console.log(flattened.fieldErrors) // { name: ["error"], age: ["error"] }
  console.log(flattened.formErrors) // ["general error"]
}

// Format errors for React Hook Form
const result = schema.safeParse(data)
if (!result.success) {
  const errors = result.error.flatten().fieldErrors
  Object.entries(errors).forEach(([field, messages]) => {
    form.setError(field as any, {
      type: 'validation',
      message: messages?.[0] || 'Invalid value'
    })
  })
}
```

## Common Patterns for Worldbuilding

### Character Schema

```typescript
const characterSchema = z.object({
  name: z.string()
    .min(2, "Name too short")
    .max(100, "Name too long")
    .regex(/^[a-zA-Z\s'-]+$/, "Invalid characters in name"),

  race: z.string().min(1, "Race required"),

  age: z.number()
    .int("Age must be whole number")
    .min(0, "Age cannot be negative")
    .max(10000, "Age unrealistic"),

  faction: z.string().optional(),

  attributes: z.object({
    strength: z.number().min(0).max(100),
    intelligence: z.number().min(0).max(100),
    charisma: z.number().min(0).max(100)
  }).optional(),

  biography: z.string()
    .max(5000, "Biography too long")
    .optional(),

  relationships: z.array(z.object({
    characterId: z.string().uuid(),
    type: z.enum(['ally', 'enemy', 'neutral', 'family']),
    description: z.string().optional()
  })).optional()
})
```

### Location Schema

```typescript
const locationSchema = z.object({
  name: z.string().min(2).max(200),

  type: z.enum([
    'city', 'town', 'village', 'dungeon', 'forest',
    'mountain', 'ocean', 'desert', 'ruins', 'landmark'
  ]),

  region: z.string().optional(),

  coordinates: z.object({
    x: z.number(),
    y: z.number(),
    z: z.number().optional()
  }).optional(),

  climate: z.enum([
    'tropical', 'temperate', 'arctic', 'desert', 'varied'
  ]).optional(),

  population: z.number()
    .int()
    .nonnegative()
    .optional(),

  government: z.string().optional(),

  description: z.string().max(10000).optional(),

  pointsOfInterest: z.array(z.object({
    name: z.string(),
    description: z.string(),
    type: z.string()
  })).optional()
}).refine(
  (data) => {
    // Cities should have population
    if (data.type === 'city' && !data.population) {
      return false
    }
    return true
  },
  {
    message: "Cities must have population defined",
    path: ["population"]
  }
)
```

### Timeline Event Schema

```typescript
const eventSchema = z.object({
  title: z.string().min(1).max(200),

  date: z.union([
    z.date(),
    z.object({
      year: z.number(),
      month: z.number().min(1).max(12).optional(),
      day: z.number().min(1).max(31).optional()
    })
  ]),

  endDate: z.union([
    z.date(),
    z.object({
      year: z.number(),
      month: z.number().min(1).max(12).optional(),
      day: z.number().min(1).max(31).optional()
    })
  ]).optional(),

  location: z.string().optional(),

  participants: z.array(z.string()).optional(),

  description: z.string().max(5000).optional(),

  consequences: z.string().max(5000).optional(),

  relatedEvents: z.array(z.string()).optional(),

  tags: z.array(z.string()).optional()
}).refine(
  (data) => {
    // If endDate exists, validate it's after startDate
    if (data.endDate) {
      // Compare dates/objects appropriately
      return true // Implement comparison logic
    }
    return true
  },
  {
    message: "End date must be after start date",
    path: ["endDate"]
  }
)
```

### Item/Artifact Schema

```typescript
const itemSchema = z.object({
  name: z.string().min(1).max(200),

  type: z.enum([
    'weapon', 'armor', 'artifact', 'consumable',
    'tool', 'treasure', 'document', 'other'
  ]),

  rarity: z.enum([
    'common', 'uncommon', 'rare', 'epic', 'legendary', 'unique'
  ]),

  owner: z.string().uuid().optional(),

  location: z.string().uuid().optional(),

  properties: z.record(z.string(), z.any()).optional(),

  magicalEffects: z.array(z.object({
    name: z.string(),
    description: z.string(),
    potency: z.number().min(1).max(10).optional()
  })).optional(),

  value: z.number().nonnegative().optional(),

  weight: z.number().nonnegative().optional(),

  history: z.string().max(5000).optional(),

  requiresAttunement: z.boolean().default(false)
}).refine(
  (data) => {
    // Magical items should have magical effects
    if (data.requiresAttunement && (!data.magicalEffects || data.magicalEffects.length === 0)) {
      return false
    }
    return true
  },
  {
    message: "Items requiring attunement must have magical effects",
    path: ["magicalEffects"]
  }
)
```

## Type Inference

```typescript
// Infer TypeScript type from schema
type Character = z.infer<typeof characterSchema>

// Infer input type (before transformations)
type CharacterInput = z.input<typeof characterSchema>

// Infer output type (after transformations)
type CharacterOutput = z.output<typeof characterSchema>

// Use in React Hook Form
const form = useForm<Character>({
  resolver: zodResolver(characterSchema)
})
```

## Schema Composition

```typescript
// Base entity schema
const baseEntitySchema = z.object({
  id: z.string().uuid(),
  name: z.string().min(1).max(200),
  description: z.string().max(5000).optional(),
  tags: z.array(z.string()).optional(),
  createdAt: z.date(),
  updatedAt: z.date()
})

// Extend for specific entities
const characterSchema = baseEntitySchema.extend({
  type: z.literal('character'),
  race: z.string(),
  age: z.number().optional()
})

const locationSchema = baseEntitySchema.extend({
  type: z.literal('location'),
  coordinates: z.object({ x: z.number(), y: z.number() }).optional()
})

// Union of all entity types
const entitySchema = z.discriminatedUnion('type', [
  characterSchema,
  locationSchema
])
```
