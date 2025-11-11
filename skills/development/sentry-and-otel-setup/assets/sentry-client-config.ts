import * as Sentry from '@sentry/nextjs';

Sentry.init({
  dsn: process.env.NEXT_PUBLIC_SENTRY_DSN,

  // Set environment
  environment: process.env.NODE_ENV,

  // Adjust sample rate for production
  tracesSampleRate: process.env.NODE_ENV === 'production' ? 0.1 : 1.0,

  // Capture 100% of errors
  sampleRate: 1.0,

  // Disable in development
  enabled: process.env.NODE_ENV !== 'development',

  // Session Replay - captures user interactions for debugging
  replaysSessionSampleRate: 0.1, // 10% of sessions
  replaysOnErrorSampleRate: 1.0, // 100% of sessions with errors

  integrations: [
    Sentry.replayIntegration({
      maskAllText: true,
      blockAllMedia: true,
    }),
  ],

  // Filter out noise
  beforeSend(event, hint) {
    // Don't send in development
    if (process.env.NODE_ENV === 'development') {
      return null;
    }

    // Filter out specific client errors
    const error = hint.originalException;
    if (error && typeof error === 'object' && 'message' in error) {
      const message = String(error.message);

      // Common browser errors to ignore
      if (
        message.includes('ResizeObserver') ||
        message.includes('Non-Error promise rejection') ||
        message.includes('ChunkLoadError')
      ) {
        return null;
      }
    }

    return event;
  },

  // Add custom tags
  initialScope: {
    tags: {
      runtime: 'client',
    },
  },
});
