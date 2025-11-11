import * as Sentry from '@sentry/nextjs';

type LogLevel = 'debug' | 'info' | 'warn' | 'error';

interface LogContext {
  [key: string]: unknown;
}

class Logger {
  private log(level: LogLevel, message: string, context?: LogContext) {
    // Add context as Sentry breadcrumb
    if (context) {
      Sentry.addBreadcrumb({
        category: 'log',
        message,
        level,
        data: context,
      });
    }

    // Also log to console in development
    if (process.env.NODE_ENV === 'development') {
      const logFn = console[level] || console.log;
      logFn(`[${level.toUpperCase()}] ${message}`, context || '');
    }
  }

  debug(message: string, context?: LogContext) {
    this.log('debug', message, context);
  }

  info(message: string, context?: LogContext) {
    this.log('info', message, context);
  }

  warn(message: string, context?: LogContext) {
    this.log('warn', message, context);
    // Set context for next error
    if (context) {
      Sentry.setContext('warning', context);
    }
  }

  error(message: string, context?: LogContext & { error?: Error }) {
    this.log('error', message, context);

    // Capture as Sentry error with context
    const error = context?.error || new Error(message);

    Sentry.captureException(error, {
      level: 'error',
      contexts: {
        custom: context,
      },
    });
  }

  // Set user context for all subsequent logs/errors
  setUser(user: { id: string; email?: string; username?: string }) {
    Sentry.setUser(user);
  }

  // Clear user context (e.g., on logout)
  clearUser() {
    Sentry.setUser(null);
  }

  // Add custom tags for filtering in Sentry
  setTag(key: string, value: string) {
    Sentry.setTag(key, value);
  }

  // Add context that persists across logs
  setContext(key: string, context: LogContext) {
    Sentry.setContext(key, context);
  }
}

export const logger = new Logger();
