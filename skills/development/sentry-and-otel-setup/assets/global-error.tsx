'use client';

import * as Sentry from '@sentry/nextjs';
import { useEffect } from 'react';

export default function GlobalError({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    Sentry.captureException(error);
  }, [error]);

  return (
    <html>
      <body>
        <div className="flex min-h-screen items-center justify-center p-4">
          <div className="max-w-md rounded-lg border p-6">
            <h2 className="mb-2 text-2xl font-semibold">Application Error</h2>

            <p className="mb-4 text-gray-600">
              A critical error occurred. Please refresh the page.
            </p>

            <div className="flex gap-2">
              <button
                onClick={reset}
                className="rounded bg-blue-600 px-4 py-2 text-white hover:bg-blue-700"
              >
                Reload page
              </button>
            </div>
          </div>
        </div>
      </body>
    </html>
  );
}
