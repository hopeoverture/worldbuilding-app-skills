import { createServerClient } from '@/lib/supabase/server';
import { redirect } from 'next/navigation';

/**
 * Get the current authenticated user
 * Returns null if not authenticated
 */
export async function getCurrentUser() {
  const supabase = await createServerClient();
  const {
    data: { user },
  } = await supabase.auth.getUser();
  return user;
}

/**
 * Get the current session
 * Returns null if not authenticated
 */
export async function getSession() {
  const supabase = await createServerClient();
  const {
    data: { session },
  } = await supabase.auth.getSession();
  return session;
}

/**
 * Require authentication - redirects to login if not authenticated
 * Use in Server Components and Server Actions that require auth
 */
export async function requireAuth() {
  const user = await getCurrentUser();

  if (!user) {
    redirect('/login');
  }

  return user;
}

/**
 * Check if user has specific role
 * Assumes roles are stored in user metadata or a profiles table
 */
export async function hasRole(role: string): Promise<boolean> {
  const user = await getCurrentUser();

  if (!user) return false;

  // Check user metadata for role
  const userRole = user.user_metadata?.role;
  return userRole === role;
}

/**
 * Require specific role - redirects to unauthorized page if role not met
 */
export async function requireRole(role: string) {
  const user = await requireAuth();

  if (!hasRole(role)) {
    redirect('/unauthorized');
  }

  return user;
}
