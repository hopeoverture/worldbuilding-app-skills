# Environment Variable Best Practices

Comprehensive guide to managing environment variables in Next.js applications.

## Table of Contents

1. [Security Best Practices](#security-best-practices)
2. [Naming Conventions](#naming-conventions)
3. [Scoping Rules](#scoping-rules)
4. [Common Patterns](#common-patterns)
5. [Environment-Specific Configuration](#environment-specific-configuration)
6. [Secret Rotation](#secret-rotation)
7. [Testing Strategies](#testing-strategies)
8. [Deployment Checklist](#deployment-checklist)

## Security Best Practices

### 1. Never Commit Secrets

**Rule**: Never commit `.env.local` or `.env.production` files

**Setup `.gitignore`**:
```
# Environment files with secrets
.env*.local
.env.production
.env.staging

# Only commit the template
!.env.example
```

### 2. Use Strong, Random Secrets

**Requirements for secrets**:
- Minimum 32 characters
- Cryptographically random
- High entropy (mix of characters, numbers, symbols)

**Generate strong secrets**:
```bash
# Node.js (recommended for JWT/session secrets)
node -e "console.log(require('crypto').randomBytes(32).toString('hex'))"

# OpenSSL
openssl rand -hex 32

# Python
python -c "import secrets; print(secrets.token_hex(32))"
```

### 3. Scope Variables Correctly

**Public variables** (`NEXT_PUBLIC_*`):
- [OK] API endpoints
- [OK] Feature flags
- [OK] Client-side config
- [X] API keys
- [X] Database credentials
- [X] Any secrets

**Private variables** (no prefix):
- [OK] Database URLs
- [OK] API secrets
- [OK] JWT/session secrets
- [OK] Third-party service credentials

### 4. Validate on Startup

**Validate environment variables when app starts**:

```typescript
// lib/env.ts
import { z } from 'zod';

const envSchema = z.object({
  DATABASE_URL: z.string().url(),
  JWT_SECRET: z.string().min(32),
  NEXTAUTH_SECRET: z.string().min(32),
  NODE_ENV: z.enum(['development', 'staging', 'production']),
  NEXT_PUBLIC_API_URL: z.string().url(),
});

export const env = envSchema.parse(process.env);
```

**Benefits**:
- Fail fast on missing/invalid variables
- Type-safe access to env vars
- Clear documentation of required variables

### 5. Use Secret Management Tools

**For production environments**:

- **Vercel**: Use Environment Variables UI (automatic encryption)
- **AWS**: AWS Secrets Manager or Systems Manager Parameter Store
- **GCP**: Secret Manager
- **Azure**: Key Vault
- **HashiCorp Vault**: Enterprise secret management
- **Doppler**: Universal secrets manager

**Benefits**:
- Encryption at rest
- Access control and auditing
- Automatic rotation
- Version history

## Naming Conventions

### Standard Format

Use `SCREAMING_SNAKE_CASE` for all environment variables:

```bash
# [OK] CORRECT
DATABASE_URL="..."
JWT_SECRET="..."
NEXT_PUBLIC_API_URL="..."

# [X] WRONG
databaseUrl="..."
jwt-secret="..."
NextPublicApiUrl="..."
```

### Prefixes

**Next.js public variables**:
```bash
NEXT_PUBLIC_API_URL="https://api.example.com"
NEXT_PUBLIC_APP_NAME="My App"
NEXT_PUBLIC_GOOGLE_MAPS_KEY="..." # Only if client-side usage
```

**Service-specific prefixes** (optional but recommended):
```bash
# Database
DATABASE_URL="..."
DATABASE_POOL_SIZE="..."

# Stripe
STRIPE_PUBLIC_KEY="..."
STRIPE_SECRET_KEY="..."
STRIPE_WEBHOOK_SECRET="..."

# Email
SMTP_HOST="..."
SMTP_PORT="..."
SMTP_USER="..."
SMTP_PASSWORD="..."
```

### Avoid Redundancy

```bash
# [OK] GOOD - clear and concise
DATABASE_URL="..."
JWT_SECRET="..."

# [X] BAD - redundant
DATABASE_CONNECTION_URL="..."  # "CONNECTION" is redundant with "URL"
JWT_SECRET_KEY="..."           # "KEY" is redundant with "SECRET"
```

## Scoping Rules

### Public Variables (`NEXT_PUBLIC_*`)

**When to use**:
- Client-side API endpoints
- Feature flags that affect UI
- Public configuration (app name, version)
- Client-side analytics IDs
- Map API keys (if client-side only)

**Example**:
```bash
NEXT_PUBLIC_API_URL="https://api.example.com"
NEXT_PUBLIC_ANALYTICS_ID="G-XXXXXXXXXX"
NEXT_PUBLIC_FEATURE_NEW_UI="true"
```

**Access in code**:
```typescript
// Available in both server and client components
const apiUrl = process.env.NEXT_PUBLIC_API_URL;
```

### Private Variables (no prefix)

**When to use**:
- Database credentials
- API secrets
- JWT/session secrets
- Third-party service credentials
- Server-side API keys

**Example**:
```bash
DATABASE_URL="postgresql://..."
JWT_SECRET="..."
STRIPE_SECRET_KEY="sk_live_..."
OPENAI_API_KEY="sk-..."
```

**Access in code**:
```typescript
// Only available in server components and API routes
const dbUrl = process.env.DATABASE_URL; // Server-side only
```

### Mixed Scenarios

**Stripe example** (public + private keys):
```bash
# Public key - client-side checkout
NEXT_PUBLIC_STRIPE_PUBLIC_KEY="pk_live_..."

# Secret key - server-side payments
STRIPE_SECRET_KEY="sk_live_..."

# Webhook secret - server-side webhooks
STRIPE_WEBHOOK_SECRET="whsec_..."
```

**Map services example**:
```bash
# If using client-side maps
NEXT_PUBLIC_GOOGLE_MAPS_KEY="..."

# If using server-side geocoding
GOOGLE_MAPS_SERVER_KEY="..."
```

## Common Patterns

### Database Configuration

```bash
# Standard database URL
DATABASE_URL="postgresql://user:password@host:5432/dbname"

# Optional connection pool settings
DATABASE_POOL_SIZE="10"
DATABASE_POOL_TIMEOUT="30000"

# Read replicas (optional)
DATABASE_READ_URL="postgresql://user:password@read-host:5432/dbname"
```

### Authentication (NextAuth.js)

```bash
# Required for NextAuth
NEXTAUTH_URL="https://example.com"
NEXTAUTH_SECRET="..." # 32+ character random string

# OAuth providers (if using)
GOOGLE_CLIENT_ID="..."
GOOGLE_CLIENT_SECRET="..."

GITHUB_CLIENT_ID="..."
GITHUB_CLIENT_SECRET="..."
```

### JWT Authentication (Custom)

```bash
# JWT secret
JWT_SECRET="..." # 32+ character random string

# Optional: token expiration
JWT_EXPIRES_IN="7d"

# Optional: refresh token secret
JWT_REFRESH_SECRET="..." # Different from JWT_SECRET
```

### External APIs

```bash
# OpenAI
OPENAI_API_KEY="sk-..."
OPENAI_ORG_ID="org-..." # Optional

# Stripe
NEXT_PUBLIC_STRIPE_PUBLIC_KEY="pk_live_..."
STRIPE_SECRET_KEY="sk_live_..."
STRIPE_WEBHOOK_SECRET="whsec_..."

# SendGrid
SENDGRID_API_KEY="SG...."

# AWS
AWS_ACCESS_KEY_ID="..."
AWS_SECRET_ACCESS_KEY="..."
AWS_REGION="us-east-1"

# Cloudinary
CLOUDINARY_URL="cloudinary://..."
```

### Email Configuration

```bash
# SMTP
SMTP_HOST="smtp.gmail.com"
SMTP_PORT="587"
SMTP_USER="your-email@gmail.com"
SMTP_PASSWORD="app-specific-password"

# Email service API (alternative)
SENDGRID_API_KEY="SG...."
MAILGUN_API_KEY="..."
```

### Monitoring and Logging

```bash
# Sentry
SENTRY_DSN="https://...@sentry.io/..."
SENTRY_AUTH_TOKEN="..." # For source maps upload

# LogRocket
LOGROCKET_APP_ID="..."

# Custom logging
LOG_LEVEL="info" # debug, info, warn, error
```

## Environment-Specific Configuration

### Development (.env.local)

```bash
# Permissive settings for development
NODE_ENV="development"

# Local database
DATABASE_URL="postgresql://postgres:postgres@localhost:5432/myapp_dev"

# Development secrets (can be weak)
JWT_SECRET="dev-secret-change-in-production"
NEXTAUTH_SECRET="dev-nextauth-secret"

# Local URLs
NEXTAUTH_URL="http://localhost:3000"
NEXT_PUBLIC_API_URL="http://localhost:3000"

# Test API keys
STRIPE_SECRET_KEY="sk_test_..."
OPENAI_API_KEY="sk-test-..."

# Debug flags
DEBUG="true"
LOG_LEVEL="debug"
```

### Staging (.env.staging)

```bash
# Staging environment
NODE_ENV="production" # Use production mode

# Staging database
DATABASE_URL="postgresql://user:password@staging-db:5432/myapp_staging"

# Production-like secrets (but different from prod)
JWT_SECRET="staging-secret-32-chars-minimum"
NEXTAUTH_SECRET="staging-nextauth-secret"

# Staging URLs
NEXTAUTH_URL="https://staging.example.com"
NEXT_PUBLIC_API_URL="https://staging.example.com"

# Test API keys (same as dev)
STRIPE_SECRET_KEY="sk_test_..."
OPENAI_API_KEY="sk-test-..."

# Staging-specific config
SENTRY_ENVIRONMENT="staging"
LOG_LEVEL="info"
```

### Production (.env.production)

```bash
# Production environment
NODE_ENV="production"

# Production database
DATABASE_URL="postgresql://user:strong-password@prod-db:5432/myapp_prod"

# Strong, random secrets
JWT_SECRET="production-secret-use-crypto-random-32-chars-minimum"
NEXTAUTH_SECRET="production-nextauth-secret-also-32-chars-minimum"

# Production URLs
NEXTAUTH_URL="https://example.com"
NEXT_PUBLIC_API_URL="https://api.example.com"

# Production API keys
STRIPE_SECRET_KEY="sk_live_..."
OPENAI_API_KEY="sk-live-..."

# Production-specific config
SENTRY_ENVIRONMENT="production"
LOG_LEVEL="warn"

# Performance optimization
DATABASE_POOL_SIZE="20"
```

## Secret Rotation

### Why Rotate Secrets?

- **Security best practice**: Limit impact of potential leaks
- **Compliance**: Required by some standards (PCI-DSS, HIPAA)
- **Team changes**: Rotate after team member departures
- **Suspected breach**: Rotate immediately if compromise suspected

### What to Rotate

**Critical secrets** (rotate regularly):
- JWT/session secrets (every 90 days)
- Database passwords (every 90 days)
- API keys for financial services (every 90 days)

**Less critical** (rotate on schedule or as needed):
- Third-party API keys (annually or on breach)
- OAuth secrets (annually or on breach)

**Never rotate**:
- Public API keys (if they're truly public)
- Client IDs (non-secret identifiers)

### Rotation Process

**For JWT/session secrets**:

1. Generate new secret
2. Deploy with NEW_JWT_SECRET environment variable
3. Update code to validate with both old and new secrets
4. After grace period (e.g., 7 days), remove old secret
5. Rename NEW_JWT_SECRET to JWT_SECRET

**For database passwords**:

1. Create new database user/password
2. Deploy with new DATABASE_URL (no downtime)
3. Monitor for 24 hours
4. Delete old database user
5. Update password manager/secrets storage

**For API keys** (if service supports multiple keys):

1. Generate new API key (keep old active)
2. Deploy with new key
3. Monitor for 24 hours
4. Revoke old API key

## Testing Strategies

### Local Testing

**Use `.env.test` for test environment**:
```bash
# .env.test
NODE_ENV="test"
DATABASE_URL="postgresql://postgres:postgres@localhost:5432/myapp_test"
JWT_SECRET="test-secret"
```

**Load in tests**:
```typescript
// jest.config.js
module.exports = {
  setupFiles: ['<rootDir>/jest.setup.js'],
};

// jest.setup.js
import { loadEnvConfig } from '@next/env';
loadEnvConfig(process.cwd());
```

### Mock Environment Variables

```typescript
// test/utils/env.ts
export function mockEnv(vars: Record<string, string>) {
  const original = { ...process.env };

  beforeAll(() => {
    Object.assign(process.env, vars);
  });

  afterAll(() => {
    process.env = original;
  });
}

// In test file
import { mockEnv } from './utils/env';

describe('API', () => {
  mockEnv({
    JWT_SECRET: 'test-secret',
    DATABASE_URL: 'postgresql://localhost/test',
  });

  // Your tests...
});
```

### Validate Before Tests

```typescript
// test/setup.ts
import { envSchema } from '@/lib/env';

try {
  envSchema.parse(process.env);
} catch (error) {
  console.error('Invalid test environment configuration:');
  console.error(error);
  process.exit(1);
}
```

## Deployment Checklist

### Before Deploying to Production

- [ ] All required variables are set in production environment
- [ ] Secrets are strong (32+ characters, random)
- [ ] No secrets in `NEXT_PUBLIC_*` variables
- [ ] Database URL points to production database
- [ ] API keys are production keys (not test keys)
- [ ] `NODE_ENV` is set to `production`
- [ ] URLs are production URLs (no localhost)
- [ ] `.env.production` is NOT committed to git
- [ ] Secrets are stored in secure secret management system
- [ ] CI/CD has access to environment variables
- [ ] Monitoring/logging is configured (Sentry, etc.)

### Validation Script

Run before deployment:
```bash
python scripts/validate_env.py --file .env.production
```

### CI/CD Integration

**GitHub Actions example**:
```yaml
- name: Validate environment
  run: python scripts/validate_env.py --file .env.production
  env:
    DATABASE_URL: ${{ secrets.DATABASE_URL }}
    JWT_SECRET: ${{ secrets.JWT_SECRET }}
    # ... other secrets from GitHub Secrets
```

### Post-Deployment Verification

- [ ] Application starts without errors
- [ ] Database connection works
- [ ] Authentication works
- [ ] External API calls work
- [ ] No environment-related errors in logs
- [ ] Monitoring shows healthy status

## Common Mistakes to Avoid

### 1. Committing Secrets to Git

```bash
# [X] NEVER DO THIS
git add .env.production
git commit -m "Add production config" # [ERROR] Secrets in git history
```

**If you accidentally commit secrets**:
1. Rotate all exposed secrets immediately
2. Use `git filter-branch` or BFG Repo-Cleaner to remove from history
3. Force push (if safe to do so)
4. Notify team and audit access

### 2. Exposing Secrets in Public Variables

```bash
# [X] WRONG
NEXT_PUBLIC_DATABASE_URL="postgresql://..."  # [ERROR] Exposed to client
NEXT_PUBLIC_JWT_SECRET="..."                 # [ERROR] Exposed to client
```

### 3. Weak Secrets

```bash
# [X] WRONG
JWT_SECRET="secret"         # [ERROR] Too weak
JWT_SECRET="password123"    # [ERROR] Predictable
JWT_SECRET="myapp-secret"   # [ERROR] Too short
```

### 4. Copy-Pasting Between Environments

```bash
# [X] WRONG - Same secrets in dev and prod
# .env.local
JWT_SECRET="abc123..."

# .env.production
JWT_SECRET="abc123..."  # [ERROR] Should be different
```

### 5. Hardcoding in Code

```typescript
// [X] WRONG
const apiKey = 'sk_live_hardcoded_key'; // [ERROR] Never hardcode

// [OK] CORRECT
const apiKey = process.env.STRIPE_SECRET_KEY;
```

## Resources

- [Next.js Environment Variables Documentation](https://nextjs.org/docs/basic-features/environment-variables)
- [OWASP Secret Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html)
- [12-Factor App Config](https://12factor.net/config)
- [Vercel Environment Variables](https://vercel.com/docs/concepts/projects/environment-variables)
