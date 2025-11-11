# OpenTelemetry Integration

## What is OpenTelemetry?

OpenTelemetry (OTel) is an observability framework for:
- **Traces**: Track requests through distributed systems
- **Metrics**: Measure system performance
- **Logs**: Structured event logging

Sentry acts as an OTel backend, receiving and visualizing this data.

## How It Works with Sentry

1. **Instrumentation hook** (`instrumentation.ts`) initializes OTel
2. **Automatic instrumentation** tracks HTTP, database, and framework operations
3. **Custom instrumentation** adds application-specific tracing
4. **Sentry integration** sends traces to Sentry for visualization

## Automatic Instrumentation

### What Gets Traced Automatically

With Sentry + Next.js:

**Server-side:**
- HTTP requests (incoming/outgoing)
- Database queries (Prisma, PostgreSQL)
- File system operations
- Next.js Server Components
- API routes

**Client-side:**
- Navigation
- User interactions
- Fetch requests
- Component rendering (partial)

### Viewing Traces

In Sentry dashboard:
1. Go to Performance
2. Click on a transaction
3. View waterfall of spans (operations)
4. Identify bottlenecks

## Custom Instrumentation

### 1. Creating Spans

Track specific operations:

```typescript
import * as Sentry from '@sentry/nextjs';

export async function processWorldData(worldId: string) {
  return await Sentry.startSpan(
    {
      name: 'process-world-data',
      op: 'task',
      attributes: {
        worldId,
      },
    },
    async () => {
      // Your logic here
      const data = await fetchWorldData(worldId);
      const processed = await processData(data);
      return processed;
    }
  );
}
```

### 2. Nested Spans

Track sub-operations:

```typescript
export async function generateWorldContent(worldId: string) {
  return await Sentry.startSpan(
    { name: 'generate-world-content', op: 'task' },
    async (span) => {
      // Child span 1
      const entities = await Sentry.startSpan(
        { name: 'fetch-entities', op: 'db.query' },
        async () => {
          return await prisma.entity.findMany({
            where: { worldId },
          });
        }
      );

      // Child span 2
      const content = await Sentry.startSpan(
        { name: 'generate-content', op: 'ai' },
        async () => {
          return await generateContent(entities);
        }
      );

      span.setStatus('ok');
      return content;
    }
  );
}
```

### 3. Adding Attributes

Enrich spans with metadata:

```typescript
Sentry.startSpan(
  {
    name: 'export-world',
    op: 'export',
    attributes: {
      worldId: 'world-123',
      format: 'json',
      includeAssets: true,
    },
  },
  async (span) => {
    const result = await exportWorld();

    // Add result metadata
    span.setAttributes({
      'export.size': result.size,
      'export.entityCount': result.entityCount,
    });

    return result;
  }
);
```

## Distributed Tracing

### Propagating Context

Trace requests across services:

```typescript
// Service A - initiates request
export async function callServiceB() {
  return await Sentry.startSpan(
    { name: 'call-service-b', op: 'http.client' },
    async () => {
      // Context automatically propagated via headers
      const response = await fetch('https://service-b.com/api', {
        headers: {
          // Sentry automatically adds tracing headers
        },
      });

      return response.json();
    }
  );
}

// Service B - receives request
// Continues the same trace automatically if instrumented
```

### Trace Visualization

In Sentry:
- See complete request flow across services
- Identify slow external calls
- Understand service dependencies

## Common Span Operations

Use semantic operation names:

```typescript
// Database operations
{ op: 'db.query' }
{ op: 'db.insert' }
{ op: 'db.update' }

// HTTP operations
{ op: 'http.client' }
{ op: 'http.server' }

// Business logic
{ op: 'task' }
{ op: 'function' }

// External services
{ op: 'ai' }
{ op: 'cache' }
{ op: 'storage' }
```

## Performance Patterns

### 1. Identify N+1 Queries

Traces reveal repeated database queries:

```typescript
// Bad - N+1 problem shows in trace
for (const world of worlds) {
  const entities = await prisma.entity.findMany({
    where: { worldId: world.id },
  });
}
// Trace shows: db.query x N times

// Good - Single query
const entities = await prisma.entity.findMany({
  where: {
    worldId: { in: worlds.map(w => w.id) },
  },
});
// Trace shows: db.query x 1 time
```

### 2. Parallel Operations

Visualize parallel vs sequential:

```typescript
// Sequential - slow
const terrain = await generateTerrain();
const biomes = await generateBiomes();
const climate = await generateClimate();
// Trace: 3 sequential spans

// Parallel - faster
const [terrain, biomes, climate] = await Promise.all([
  generateTerrain(),
  generateBiomes(),
  generateClimate(),
]);
// Trace: 3 parallel spans
```

### 3. Caching Effectiveness

Track cache hits/misses:

```typescript
export async function getCachedData(key: string) {
  return await Sentry.startSpan(
    { name: 'get-cached-data', op: 'cache' },
    async (span) => {
      const cached = await redis.get(key);

      if (cached) {
        span.setAttributes({ 'cache.hit': true });
        return cached;
      }

      span.setAttributes({ 'cache.hit': false });
      const data = await fetchFreshData();
      await redis.set(key, data);
      return data;
    }
  );
}
```

## Sampling Strategies

### 1. Transaction-Based Sampling

Sample different operations differently:

```typescript
Sentry.init({
  tracesSampler: (samplingContext) => {
    // High-value operations - trace all
    if (samplingContext.name?.includes('checkout')) {
      return 1.0;
    }

    // Background tasks - sample less
    if (samplingContext.name?.includes('background')) {
      return 0.01;
    }

    // Default
    return 0.1;
  },
});
```

### 2. Head-Based Sampling

Decision made at trace start (Sentry default).

**Pros**: Simple, consistent per trace
**Cons**: Can't sample based on outcome

### 3. Performance Impact

- Minimal overhead (<5% typically)
- Sampling reduces overhead
- Most cost is in data transmission

## Troubleshooting

### Traces Not Appearing

1. Check `tracesSampleRate` > 0
2. Verify instrumentation.ts exports `register()`
3. Ensure Next.js experimental.instrumentationHook enabled
4. Check Sentry DSN is correct

### Missing Spans

1. Verify automatic instrumentation is enabled
2. Check custom spans use correct Sentry API
3. Ensure spans finish (call `.finish()` or use callback form)

### Incomplete Traces

1. Check trace context is propagated (especially cross-service)
2. Verify all services use compatible Sentry SDK versions
3. Review sampling - some spans may be dropped

## Best Practices

1. **Use semantic operation names** - Makes filtering/grouping easier
2. **Add relevant attributes** - Enrich spans with context
3. **Don't over-instrument** - Focus on meaningful operations
4. **Keep spans short** - Track discrete operations, not long processes
5. **Set span status** - Mark success/failure explicitly
6. **Sample appropriately** - Balance visibility with cost
7. **Review regularly** - Check for performance regressions

## Advanced: Custom Metrics

Track custom measurements:

```typescript
import * as Sentry from '@sentry/nextjs';

// Record custom metric
Sentry.metrics.distribution('world.entity.count', entityCount, {
  tags: {
    worldType: 'fantasy',
  },
});

// Track over time in Sentry dashboard
```

## Integration with Other Tools

Sentry can forward traces to:
- **DataDog** - Full observability platform
- **Jaeger** - Distributed tracing
- **Prometheus** - Metrics collection

Configure via Sentry integrations or OpenTelemetry Collector.
