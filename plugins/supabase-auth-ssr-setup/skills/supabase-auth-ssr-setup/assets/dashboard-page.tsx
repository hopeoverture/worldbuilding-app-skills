import { requireAuth } from '@/lib/auth/utils';
import { logout } from '@/app/actions/auth';

export default async function DashboardPage() {
  const user = await requireAuth();

  return (
    <div className="min-h-screen p-8">
      <div className="mx-auto max-w-4xl">
        <div className="mb-8 flex items-center justify-between">
          <h1 className="text-3xl font-bold">Dashboard</h1>

          <form action={logout}>
            <button
              type="submit"
              className="rounded-md border border-gray-300 px-4 py-2 hover:bg-gray-50"
            >
              Sign out
            </button>
          </form>
        </div>

        <div className="rounded-lg border p-6">
          <h2 className="mb-4 text-xl font-semibold">User Information</h2>

          <dl className="space-y-2">
            <div>
              <dt className="text-sm font-medium text-gray-500">Email</dt>
              <dd className="text-base">{user.email}</dd>
            </div>

            <div>
              <dt className="text-sm font-medium text-gray-500">User ID</dt>
              <dd className="font-mono text-sm">{user.id}</dd>
            </div>

            <div>
              <dt className="text-sm font-medium text-gray-500">
                Email Verified
              </dt>
              <dd className="text-base">
                {user.email_confirmed_at ? 'Yes' : 'No'}
              </dd>
            </div>

            <div>
              <dt className="text-sm font-medium text-gray-500">
                Last Sign In
              </dt>
              <dd className="text-base">
                {user.last_sign_in_at
                  ? new Date(user.last_sign_in_at).toLocaleString()
                  : 'N/A'}
              </dd>
            </div>
          </dl>
        </div>

        <div className="mt-6 rounded-lg bg-blue-50 p-4">
          <p className="text-sm text-blue-900">
            This is a protected page. You can only access it when authenticated.
          </p>
        </div>
      </div>
    </div>
  );
}
