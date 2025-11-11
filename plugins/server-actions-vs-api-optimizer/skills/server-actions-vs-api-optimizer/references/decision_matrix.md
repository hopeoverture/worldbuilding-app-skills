# Server Actions vs API Routes Decision Matrix

Comprehensive guide for choosing between Server Actions and API routes in Next.js applications.

## Quick Decision Tree

```
Is it a form submission?
├─ YES → Use Server Action (unless external API involved)
└─ NO
   ├─ Is it a webhook or external callback?
   │  └─ YES → Use API Route
   └─ NO
      ├─ Does it need non-POST methods (GET, PUT, DELETE)?
      │  └─ YES → Use API Route
      └─ NO
         ├─ Does it proxy an external API?
         │  └─ YES → Use API Route
         └─ NO
            ├─ Does it need revalidatePath/revalidateTag?
            │  └─ YES → Use Server Action
            └─ NO → Either works (prefer Server Action for simplicity)
```

## Detailed Decision Matrix

| Criterion | Server Action | API Route | Notes |
|-----------|--------------|-----------|-------|
| **Form submission** | [OK] Strongly recommended | - | Progressive enhancement, CSRF protection |
| **Data mutation** | [OK] Recommended | ○ Works | Server Actions simpler for mutations |
| **Revalidation needed** | [OK] Built-in | - Requires manual | `revalidatePath()`, `revalidateTag()` |
| **External API proxy** | - Not ideal | [OK] Recommended | Hide API keys, rate limiting |
| **Webhooks** | - Cannot use | [OK] Required | Needs public URL endpoint |
| **OAuth callbacks** | - Cannot use | [OK] Required | Third-party redirects |
| **GET requests** | - POST only | [OK] Required | Server Actions are POST-only |
| **Multiple HTTP methods** | - POST only | [OK] Required | REST API with GET/POST/PUT/DELETE |
| **External client access** | - Internal only | [OK] Required | Mobile apps, third-party integrations |
| **Custom response headers** | - Limited | [OK] Full control | CORS, caching, content-type |
| **Streaming responses** | ○ Possible | [OK] Easier | SSE, custom streams |
| **File uploads** | [OK] FormData | ○ Works | Server Actions handle FormData natively |
| **Type safety** | [OK] Full | ○ Manual | Server Actions fully type-safe |
| **CSRF protection** | [OK] Automatic | - Manual | Server Actions have built-in protection |
| **Progressive enhancement** | [OK] Works without JS | - Requires JS | Forms work even if JS fails |
| **Authentication in RSC** | [OK] Direct access | - Via middleware | Server Actions can access auth directly |

**Legend**: [OK] = Strongly recommended, ○ = Works but not ideal, - = Not suitable/possible

## Use Case Patterns

### 1. Form Submissions

**Scenario**: User submits a form to create/update data

**Recommended**: Server Action

**Reasoning**:
- Built-in form handling with `action` attribute
- Automatic CSRF protection
- Progressive enhancement (works without JavaScript)
- Simpler code than fetch + API route
- Type-safe with TypeScript

**Example**:
```typescript
// Server Action (recommended)
'use server';
export async function createEntity(formData: FormData) {
  const name = formData.get('name') as string;
  await db.entity.create({ name });
  revalidatePath('/entities');
  return { success: true };
}

// Usage in component
<form action={createEntity}>
  <input name="name" required />
  <button type="submit">Create</button>
</form>
```

### 2. External API Proxying

**Scenario**: Client needs to call external API, but API keys must be hidden

**Recommended**: API Route

**Reasoning**:
- Hides API keys on server
- Enables rate limiting
- Allows response transformation
- Can cache responses
- Standard REST pattern

**Example**:
```typescript
// API Route (recommended)
export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const query = searchParams.get('query');

  const response = await fetch(
    `https://api.external.com?key=${process.env.API_KEY}&q=${query}`,
    { next: { revalidate: 3600 } } // Cache for 1 hour
  );

  return Response.json(await response.json());
}
```

### 3. Webhooks

**Scenario**: External service (Stripe, GitHub, etc.) sends POST requests

**Recommended**: API Route

**Reasoning**:
- Needs public, stable URL
- External service cannot call Server Actions
- Requires signature verification
- May need custom response codes/headers

**Example**:
```typescript
// API Route (required)
export async function POST(request: Request) {
  const signature = request.headers.get('stripe-signature');
  const body = await request.text();

  // Verify webhook signature
  const event = stripe.webhooks.constructEvent(
    body,
    signature,
    process.env.WEBHOOK_SECRET
  );

  // Process event
  await handleWebhookEvent(event);

  return Response.json({ received: true });
}
```

### 4. Data Mutations with Revalidation

**Scenario**: Update data and refresh cache

**Recommended**: Server Action

**Reasoning**:
- Built-in `revalidatePath()` and `revalidateTag()`
- Simpler than manual cache invalidation
- Type-safe
- Direct server access

**Example**:
```typescript
// Server Action (recommended)
'use server';
export async function updateEntity(id: string, data: any) {
  await db.entity.update({ where: { id }, data });
  revalidatePath('/entities');
  revalidateTag(`entity-${id}`);
  return { success: true };
}
```

### 5. OAuth Callbacks

**Scenario**: Third-party service redirects back to your app

**Recommended**: API Route

**Reasoning**:
- Needs stable public URL
- External redirect target
- May need to set cookies/headers
- Standard OAuth flow pattern

**Example**:
```typescript
// API Route (required)
export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const code = searchParams.get('code');

  // Exchange code for token
  const token = await exchangeCodeForToken(code);

  // Set cookie and redirect
  const response = NextResponse.redirect('/dashboard');
  response.cookies.set('auth_token', token, { httpOnly: true });

  return response;
}
```

### 6. Public REST API

**Scenario**: Expose API endpoints for mobile apps or third-party integrations

**Recommended**: API Route

**Reasoning**:
- External client access
- Standard REST conventions
- Multiple HTTP methods (GET, POST, PUT, DELETE)
- Custom authentication (API keys, tokens)
- Can document with OpenAPI/Swagger

**Example**:
```typescript
// API Route (required)
export async function GET(request: Request) {
  const token = request.headers.get('authorization');
  if (!validateApiKey(token)) {
    return Response.json({ error: 'Unauthorized' }, { status: 401 });
  }

  const entities = await db.entity.findMany();
  return Response.json({ entities });
}
```

### 7. File Uploads

**Scenario**: User uploads files

**Recommended**: Server Action

**Reasoning**:
- Native FormData handling
- Simpler than API route with multipart parsing
- Can stream large files
- Progressive enhancement

**Example**:
```typescript
// Server Action (recommended)
'use server';
export async function uploadFile(formData: FormData) {
  const file = formData.get('file') as File;

  // Process file
  const buffer = Buffer.from(await file.arrayBuffer());
  await saveFile(buffer, file.name);

  revalidatePath('/files');
  return { success: true, filename: file.name };
}
```

### 8. Optimistic Updates

**Scenario**: Update UI immediately, validate on server

**Recommended**: Server Action

**Reasoning**:
- Works with `useOptimistic` hook
- Automatic rollback on error
- Type-safe
- Simpler state management

**Example**:
```typescript
'use client';
import { useOptimistic } from 'react';

function Component() {
  const [optimisticData, addOptimistic] = useOptimistic(data);

  async function handleUpdate(newData) {
    addOptimistic(newData); // Update UI immediately
    await serverAction(newData); // Validate on server
  }

  return <UI data={optimisticData} onUpdate={handleUpdate} />;
}
```

### 9. Server-Sent Events (SSE)

**Scenario**: Push real-time updates to client

**Recommended**: API Route

**Reasoning**:
- Needs streaming response
- Custom headers (Content-Type: text/event-stream)
- Long-lived connection
- Standard SSE protocol

**Example**:
```typescript
// API Route (recommended)
export async function GET() {
  const stream = new ReadableStream({
    start(controller) {
      const interval = setInterval(() => {
        controller.enqueue(`data: ${JSON.stringify({ time: Date.now() })}\n\n`);
      }, 1000);

      return () => clearInterval(interval);
    },
  });

  return new Response(stream, {
    headers: {
      'Content-Type': 'text/event-stream',
      'Cache-Control': 'no-cache',
      'Connection': 'keep-alive',
    },
  });
}
```

### 10. Complex Authentication Flows

**Scenario**: Multi-step authentication with redirects

**Recommended**: API Route

**Reasoning**:
- Full control over response
- Custom headers and cookies
- Complex redirect logic
- Standard auth patterns

**Example**:
```typescript
// API Route (recommended)
export async function POST(request: Request) {
  const { email, password } = await request.json();

  const user = await authenticateUser(email, password);

  if (!user) {
    return Response.json({ error: 'Invalid credentials' }, { status: 401 });
  }

  const response = NextResponse.json({ user });
  response.cookies.set('session', user.sessionToken, {
    httpOnly: true,
    secure: true,
    sameSite: 'lax',
    maxAge: 60 * 60 * 24 * 7, // 7 days
  });

  return response;
}
```

## Performance Considerations

### Server Actions

**Pros**:
- Automatic request deduplication
- Built-in caching with React
- No additional route handler overhead
- Smaller client bundle (no fetch logic)

**Cons**:
- POST-only (cannot use GET with browser caching)
- No HTTP-level caching (no Cache-Control headers)

### API Routes

**Pros**:
- Full HTTP caching support (Cache-Control, ETag)
- GET requests can leverage browser cache
- Can use CDN caching
- Standard HTTP optimizations

**Cons**:
- Additional route handler overhead
- Requires client-side fetch logic
- No automatic deduplication

## Security Considerations

### Server Actions

**Pros**:
- Built-in CSRF protection
- No CORS issues (same-origin)
- Automatic request validation
- Type-safe by default

**Cons**:
- Cannot restrict by IP or API key
- Limited rate limiting options

### API Routes

**Pros**:
- Full control over authentication
- API key/token validation
- IP-based restrictions
- Custom rate limiting
- CORS configuration

**Cons**:
- Must implement CSRF protection manually
- More attack surface (public endpoints)

## Developer Experience

### Server Actions

**Pros**:
- Simpler code (no fetch boilerplate)
- Fully type-safe
- Better error handling with React
- Progressive enhancement
- Automatic form reset

**Cons**:
- Less familiar to backend developers
- Debugging can be harder (no network tab)
- Limited to Next.js ecosystem

### API Routes

**Pros**:
- Standard REST patterns
- Familiar to all developers
- Easy to test (curl, Postman)
- Visible in network tab
- Framework-agnostic clients

**Cons**:
- More boilerplate code
- Manual type safety
- Requires client-side error handling
- CSRF protection needed

## Migration Strategies

### API Route → Server Action

**When to migrate**:
- POST-only endpoint
- Used for form submissions
- Needs revalidation
- Only called from your app

**Steps**:
1. Create Server Action with same logic
2. Remove fetch call from client
3. Update form to use `action` prop
4. Add revalidation if needed
5. Remove API route
6. Test thoroughly

**Complexity**: Low to Medium

### Server Action → API Route

**When to migrate**:
- Need external client access
- Require GET/PUT/DELETE methods
- Need custom headers/cookies
- Webhook target

**Steps**:
1. Create API route with same logic
2. Add authentication/authorization
3. Remove revalidation (use cache instead)
4. Update clients to use fetch
5. Remove Server Action
6. Test with external clients

**Complexity**: Medium to High

## Worldbuilding App Examples

### Entity Management

| Operation | Recommended | Reason |
|-----------|------------|--------|
| Create entity form | Server Action | Form submission, revalidation |
| Update entity form | Server Action | Form submission, revalidation |
| Delete entity | Server Action | Simple mutation, revalidation |
| Get entity list | API Route (GET) | External dashboard, caching |
| Bulk import | Server Action | FormData, file upload |
| Export entities | API Route (GET) | Streaming, custom headers |

### Relationships

| Operation | Recommended | Reason |
|-----------|------------|--------|
| Add relationship | Server Action | Simple mutation, revalidation |
| Remove relationship | Server Action | Simple mutation, revalidation |
| Get relationship graph | API Route (GET) | Complex data, caching |
| Bulk relationship update | Server Action | Transaction, revalidation |

### Timeline Events

| Operation | Recommended | Reason |
|-----------|------------|--------|
| Create event | Server Action | Form submission, revalidation |
| Update event | Server Action | Form submission, revalidation |
| Timeline feed | API Route (GET) | Caching, pagination |
| Event search | API Route (GET) | Complex query, caching |

### Search and Filtering

| Operation | Recommended | Reason |
|-----------|------------|--------|
| Search within app | Server Action | With revalidation, type-safe |
| Public search API | API Route (GET) | External access, rate limiting |
| Save search filter | Server Action | Form submission, revalidation |

## Best Practices Summary

1. **Default to Server Actions for forms** - Simpler, more secure, better UX
2. **Use API Routes for external integration** - Webhooks, proxies, third-party APIs
3. **Consider HTTP methods** - Non-POST operations need API routes
4. **Think about clients** - External clients require API routes
5. **Evaluate caching needs** - Complex caching may favor API routes
6. **Prioritize type safety** - Server Actions provide better type safety
7. **Plan for scale** - API routes better for public APIs with rate limiting
8. **Progressive enhancement** - Forms with Server Actions work without JS
9. **Monitor performance** - Both have trade-offs, measure and optimize
10. **Be consistent** - Choose patterns and stick to them across your codebase
