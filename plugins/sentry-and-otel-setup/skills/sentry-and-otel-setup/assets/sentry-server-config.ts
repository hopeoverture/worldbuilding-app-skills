import * as Sentry from '@sentry/nextjs';

Sentry.init({
  dsn: process.env.SENTRY_DSN,

  // Set environment
  environment: process.env.NODE_ENV,

  // Adjust sample rate for production in production
  tracesSampleRate: process.env.NODE_ENV === 'production' ? 0.1 : 1.0,

  // Capture 100% of errors
  sampleRate: 1.0,

  // Disable in development to reduce noise
  enabled: process.env.NODE_ENV !== 'development',

  // Capture Server Actions and API routes
  integrations: [
    Sentry.rewriteFramesIntegration({
      root: process.cwd(),
    }),
  ],

  // Filter out noise
  beforeSend(event, hint) {
    // Don't send errors from development
    if (process.env.NODE_ENV === 'development') {
      return null;
    }

    // Filter out specific errors
    const error = hint.originalException;
    if (error && typeof error === 'object' && 'message' in error) {
      const message = String(error.message);

      // Ignore known non-critical errors
      if (
        message.includes('ResizeObserver') ||
        message.includes('NotFoundError') ||
        message.includes('AbortError')
      ) {
        return null;
      }
    }

    return event;
  },

  // Add custom tags
  initialScope: {
    tags: {
      runtime: 'server',
    },
  },
});
