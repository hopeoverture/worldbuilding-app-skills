/**
 * Feature Flag Provider - JSON-based implementation
 */

import { createContext, useContext, ReactNode } from 'react';

// Feature flag configuration type
export interface FeatureFlagConfig {
  enabled: boolean;
  description?: string;
  rolloutPercentage?: number;
  allowedUsers?: string[];
  environments?: Record<string, boolean>;
}

export interface FeatureFlags {
  [key: string]: FeatureFlagConfig;
}

// Context for feature flags
const FeatureFlagContext = createContext<FeatureFlags>({});

interface FeatureFlagProviderProps {
  children: ReactNode;
  flags: FeatureFlags;
  userId?: string;
  environment?: string;
}

/**
 * Provider component that makes feature flags available to the app
 */
export function FeatureFlagProvider({
  children,
  flags,
  userId,
  environment = process.env.NODE_ENV,
}: FeatureFlagProviderProps) {
  // Evaluate flags based on environment and user
  const evaluatedFlags = evaluateFlags(flags, { userId, environment });

  return (
    <FeatureFlagContext.Provider value={evaluatedFlags}>
      {children}
    </FeatureFlagContext.Provider>
  );
}

/**
 * Hook to access feature flags
 */
export function useFeatureFlags() {
  const context = useContext(FeatureFlagContext);
  if (!context) {
    throw new Error('useFeatureFlags must be used within FeatureFlagProvider');
  }
  return context;
}

/**
 * Hook to check if a specific feature flag is enabled
 */
export function useFeatureFlag(flagName: string): boolean {
  const flags = useFeatureFlags();
  const flag = flags[flagName];

  if (!flag) {
    console.warn(`Feature flag "${flagName}" not found, defaulting to false`);
    return false;
  }

  return flag.enabled;
}

/**
 * Hook for multivariate flags (A/B testing)
 */
export function useFeatureFlagVariant<T extends string>(
  flagName: string,
  variants: Record<string, T>,
  defaultVariant: T
): T {
  const flags = useFeatureFlags();
  const flag = flags[flagName];

  if (!flag || !flag.enabled) {
    return defaultVariant;
  }

  // Simple hash-based variant assignment
  const variantKeys = Object.keys(variants);
  const hash = hashString(flagName + (flag.allowedUsers?.[0] || ''));
  const index = hash % variantKeys.length;

  return variants[variantKeys[index]] || defaultVariant;
}

/**
 * Evaluate flags based on context
 */
function evaluateFlags(
  flags: FeatureFlags,
  context: { userId?: string; environment?: string }
): FeatureFlags {
  const evaluated: FeatureFlags = {};

  for (const [key, config] of Object.entries(flags)) {
    evaluated[key] = {
      ...config,
      enabled: evaluateFlag(config, context),
    };
  }

  return evaluated;
}

/**
 * Evaluate a single flag
 */
function evaluateFlag(
  config: FeatureFlagConfig,
  context: { userId?: string; environment?: string }
): boolean {
  // Check environment-specific override
  if (config.environments && context.environment) {
    const envEnabled = config.environments[context.environment];
    if (envEnabled !== undefined) {
      return envEnabled;
    }
  }

  // Check user allowlist
  if (config.allowedUsers && config.allowedUsers.length > 0 && context.userId) {
    if (config.allowedUsers.includes(context.userId)) {
      return config.enabled;
    }
    return false;
  }

  // Check rollout percentage
  if (config.rolloutPercentage !== undefined && context.userId) {
    const hash = hashString(context.userId);
    const bucket = hash % 100;
    if (bucket >= config.rolloutPercentage) {
      return false;
    }
  }

  return config.enabled;
}

/**
 * Simple string hash function
 */
function hashString(str: string): number {
  let hash = 0;
  for (let i = 0; i < str.length; i++) {
    const char = str.charCodeAt(i);
    hash = (hash << 5) - hash + char;
    hash = hash & hash; // Convert to 32-bit integer
  }
  return Math.abs(hash);
}
