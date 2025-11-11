import { signInWithPassword, signInWithMagicLink } from '@/app/actions/auth';
import { createServerClient } from '@/lib/supabase/server';
import { redirect } from 'next/navigation';

export default async function LoginPage({
  searchParams,
}: {
  searchParams: { redirect?: string; error?: string };
}) {
  // Check if user is already logged in
  const supabase = await createServerClient();
  const {
    data: { user },
  } = await supabase.auth.getUser();

  if (user) {
    redirect(searchParams.redirect || '/dashboard');
  }

  return (
    <div className="flex min-h-screen items-center justify-center">
      <div className="w-full max-w-md space-y-8 rounded-lg border p-8">
        <div>
          <h2 className="text-center text-3xl font-bold">Sign in</h2>
          <p className="mt-2 text-center text-sm text-gray-600">
            Access your account
          </p>
        </div>

        {searchParams.error && (
          <div className="rounded-md bg-red-50 p-4">
            <p className="text-sm text-red-800">{searchParams.error}</p>
          </div>
        )}

        {/* Email/Password Form */}
        <form action={signInWithPassword} className="space-y-6">
          <div>
            <label htmlFor="email" className="block text-sm font-medium">
              Email address
            </label>
            <input
              id="email"
              name="email"
              type="email"
              autoComplete="email"
              required
              className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2"
            />
          </div>

          <div>
            <label htmlFor="password" className="block text-sm font-medium">
              Password
            </label>
            <input
              id="password"
              name="password"
              type="password"
              autoComplete="current-password"
              required
              className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2"
            />
          </div>

          <button
            type="submit"
            className="w-full rounded-md bg-blue-600 px-4 py-2 text-white hover:bg-blue-700"
          >
            Sign in with email
          </button>
        </form>

        <div className="relative">
          <div className="absolute inset-0 flex items-center">
            <div className="w-full border-t border-gray-300" />
          </div>
          <div className="relative flex justify-center text-sm">
            <span className="bg-white px-2 text-gray-500">Or</span>
          </div>
        </div>

        {/* Magic Link Form */}
        <form action={signInWithMagicLink} className="space-y-4">
          <div>
            <label htmlFor="magic-email" className="block text-sm font-medium">
              Email for magic link
            </label>
            <input
              id="magic-email"
              name="email"
              type="email"
              autoComplete="email"
              required
              className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2"
            />
          </div>

          <button
            type="submit"
            className="w-full rounded-md border border-gray-300 bg-white px-4 py-2 hover:bg-gray-50"
          >
            Send magic link
          </button>
        </form>

        {/* OAuth Providers - Uncomment to enable */}
        {/*
        <div className="space-y-2">
          <button
            onClick={() => signInWithOAuth('google')}
            className="w-full rounded-md border border-gray-300 bg-white px-4 py-2 hover:bg-gray-50"
          >
            Continue with Google
          </button>

          <button
            onClick={() => signInWithOAuth('github')}
            className="w-full rounded-md border border-gray-300 bg-white px-4 py-2 hover:bg-gray-50"
          >
            Continue with GitHub
          </button>
        </div>
        */}

        <div className="text-center text-sm">
          <a href="/signup" className="text-blue-600 hover:underline">
            Don't have an account? Sign up
          </a>
        </div>
      </div>
    </div>
  );
}
