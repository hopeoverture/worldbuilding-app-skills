# Sentry Best Practices

## Error Handling Patterns

### 1. Structured Error Handling

Use consistent error handling across the application:

```typescript
import { logger } from '@/lib/logger';
import * as Sentry from '@sentry/nextjs';

export async function performOperation() {
  try {
    // Operation logic
    const result = await someOperation();
    logger.info('Operation succeeded', { result });
    return result;

  } catch (error) {
    // Log with context
    logger.error('Operation failed', {
      error: error as Error,
      operation: 'performOperation',
      timestamp: new Date().toISOString(),
    });

    // Re-throw for caller to handle
    throw error;
  }
}
```

### 2. User-Facing vs Internal Errors

Distinguish between errors shown to users and internal errors:

```typescript
class UserFacingError extends Error {
  constructor(
    message: string,
    public userMessage: string,
    public statusCode: number = 400
  ) {
    super(message);
    this.name = 'UserFacingError';
  }
}

// Usage
try {
  await createEntity(data);
} catch (error) {
  if (error instanceof UserFacingError) {
    // Show to user
    return { error: error.userMessage };
  }

  // Internal error - log to Sentry, show generic message
  logger.error('Entity creation failed', { error });
  return { error: 'An unexpected error occurred' };
}
```

### 3. Add Context to Errors

Enrich errors with relevant context:

```typescript
export async function updateEntity(entityId: string, data: unknown) {
  // Set context for all errors in this scope
  Sentry.setContext('entity', {
    id: entityId,
    type: 'character',
    data,
  });

  try {
    const result = await prisma.entity.update({
      where: { id: entityId },
      data,
    });
    return result;

  } catch (error) {
    // Error automatically includes entity context
    logger.error('Entity update failed', { error, entityId });
    throw error;
  }
}
```

## Performance Monitoring

### 1. Custom Transactions

Track important operations:

```typescript
import * as Sentry from '@sentry/nextjs';

export async function generateWorld(params: WorldParams) {
  const transaction = Sentry.startTransaction({
    name: 'generate-world',
    op: 'task',
    tags: {
      worldType: params.type,
      complexity: params.complexity,
    },
  });

  try {
    // Track each step
    const terrainSpan = transaction.startChild({
      op: 'generate-terrain',
      description: 'Generate terrain data',
    });
    const terrain = await generateTerrain(params);
    terrainSpan.finish();

    const biomesSpan = transaction.startChild({
      op: 'generate-biomes',
      description: 'Generate biome data',
    });
    const biomes = await generateBiomes(terrain);
    biomesSpan.finish();

    transaction.setStatus('ok');
    return { terrain, biomes };

  } catch (error) {
    transaction.setStatus('internal_error');
    throw error;

  } finally {
    transaction.finish();
  }
}
```

### 2. Database Query Monitoring

Track slow queries:

```typescript
import { prisma } from '@/lib/prisma';

// Prisma automatically creates spans for queries when OTel is configured
const users = await prisma.user.findMany({
  where: { active: true },
  include: { profile: true },
});

// Shows up in Sentry as:
// - db.query
// - duration
// - query details
```

### 3. API Call Monitoring

Track external API calls:

```typescript
export async function fetchExternalData(url: string) {
  return await Sentry.startSpan(
    {
      name: 'external-api-call',
      op: 'http.client',
      attributes: {
        'http.url': url,
      },
    },
    async () => {
      const response = await fetch(url);

      // Add response details to span
      Sentry.getCurrentScope().setContext('http', {
        status: response.status,
        statusText: response.statusText,
      });

      return response.json();
    }
  );
}
```

## Quota Management

### 1. Sample Rates

Adjust sampling to control quota usage:

```typescript
Sentry.init({
  // Errors
  sampleRate: 1.0, // 100% of errors

  // Performance monitoring
  tracesSampleRate: process.env.NODE_ENV === 'production' ? 0.1 : 1.0,

  // Session replay
  replaysSessionSampleRate: 0.05, // 5% of normal sessions
  replaysOnErrorSampleRate: 1.0,  // 100% of error sessions
});
```

### 2. Filter Out Noise

Prevent known non-issues from consuming quota:

```typescript
Sentry.init({
  beforeSend(event, hint) {
    const error = hint.originalException;

    // Filter by error message
    if (error && typeof error === 'object' && 'message' in error) {
      const message = String(error.message);

      const ignoredPatterns = [
        'ResizeObserver loop',
        'Non-Error promise rejection',
        'Loading chunk',
        'Script error.',
      ];

      if (ignoredPatterns.some((pattern) => message.includes(pattern))) {
        return null;
      }
    }

    // Filter by URL
    if (event.request?.url?.includes('localhost')) {
      return null;
    }

    return event;
  },
});
```

### 3. Inbound Filters

Configure in Sentry dashboard:
- Settings > Inbound Filters
- Filter by:
  - Browser version
  - Error message
  - Release version
  - IP address

## User Context

### 1. Set User on Authentication

```typescript
// In middleware or auth utility
import * as Sentry from '@sentry/nextjs';
import { getCurrentUser } from '@/lib/auth/utils';

export async function setUserContext() {
  const user = await getCurrentUser();

  if (user) {
    Sentry.setUser({
      id: user.id,
      email: user.email,
      username: user.name,
    });
  }
}
```

### 2. Clear User on Logout

```typescript
export async function logout() {
  // Clear Sentry context
  Sentry.setUser(null);
  logger.clearUser();

  // Logout logic
  await supabase.auth.signOut();
}
```

## Breadcrumbs

Track user journey:

```typescript
// Navigation
Sentry.addBreadcrumb({
  category: 'navigation',
  message: 'User navigated to world editor',
  level: 'info',
  data: { worldId: 'world-123' },
});

// User actions
Sentry.addBreadcrumb({
  category: 'user.action',
  message: 'Created new character',
  level: 'info',
  data: {
    characterName: 'Hero',
    worldId: 'world-123',
  },
});

// Data changes
Sentry.addBreadcrumb({
  category: 'data',
  message: 'Updated world settings',
  level: 'info',
  data: {
    worldId: 'world-123',
    settings: { theme: 'dark' },
  },
});
```

## Source Maps

### 1. Verify Upload

Check source maps are uploaded:

```bash
# Build with source maps
npm run build

# Verify in Sentry dashboard
# Settings > Source Maps > [Release]
```

### 2. Configure Properly

```typescript
// next.config.js
const { withSentryConfig } = require('@sentry/nextjs');

module.exports = withSentryConfig(
  nextConfig,
  {
    // Sentry webpack plugin options
    silent: true,
    org: process.env.SENTRY_ORG,
    project: process.env.SENTRY_PROJECT,
    authToken: process.env.SENTRY_AUTH_TOKEN,
  },
  {
    // Sentry SDK options
    hideSourceMaps: true, // Don't expose source maps to public
    widenClientFileUpload: true, // Upload more files for better stack traces
    disableLogger: true, // Reduce noise in build logs
  }
);
```

### 3. Troubleshooting

**Source maps not working:**
- Verify `SENTRY_AUTH_TOKEN` is set
- Check build logs for upload errors
- Ensure release version matches between app and Sentry

## Alerting

### 1. Configure Alert Rules

In Sentry dashboard:
- Alerts > Create Alert Rule
- Set conditions (frequency, affected users)
- Choose notification channels (email, Slack, PagerDuty)

**Recommended alerts:**
- High error rate (>10 errors/minute)
- New error type
- Regression (error in new release)
- Performance degradation

### 2. Alert Fatigue

Avoid alert fatigue:
- Use appropriate thresholds
- Filter out noisy errors
- Set up different alerts for different severity
- Use digest emails instead of immediate notifications

## Release Tracking

Associate errors with releases:

```typescript
Sentry.init({
  release: process.env.NEXT_PUBLIC_VERCEL_GIT_COMMIT_SHA || 'dev',
  environment: process.env.NODE_ENV,
});
```

**Benefits:**
- Track which release introduced errors
- Compare error rates between releases
- Verify if deploy fixed issues

## Testing

### 1. Test Error Capture

```typescript
// Test error handling
export async function testSentry() {
  try {
    throw new Error('Test error from Sentry setup');
  } catch (error) {
    logger.error('Testing Sentry integration', { error });
  }
}
```

### 2. Verify in Dashboard

After testing:
1. Go to Sentry dashboard
2. Check Issues for test error
3. Verify context, breadcrumbs, and user info
4. Check source maps resolve correctly

## Common Pitfalls

1. **Not filtering development errors** - Always disable Sentry in development or filter out
2. **Missing source maps** - Stack traces are unreadable without them
3. **Not setting user context** - Makes debugging user-specific issues hard
4. **Over-sampling in production** - Wastes quota and money
5. **Ignoring performance monitoring** - Only tracking errors misses slow operations
6. **Not reviewing regularly** - Set aside time weekly to review Sentry issues
