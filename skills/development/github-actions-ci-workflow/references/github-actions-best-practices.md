# GitHub Actions Best Practices

## Workflow Optimization

### Caching Strategies

1. **Dependency Caching**
   - Always cache package manager dependencies
   - Use lock file hashes as cache keys
   - Include fallback restoration keys for partial matches
   - Example: `${{ runner.os }}-npm-${{ hashFiles('**/package-lock.json') }}`

2. **Build Artifact Caching**
   - Cache framework-specific build directories (.next/cache, .nuxt, etc.)
   - Include source file hashes in cache key for invalidation
   - Use separate caches for different build targets

3. **Cache Size Management**
   - Keep cache sizes under 10GB per repository
   - Regularly clean up unused caches
   - Split large caches into multiple smaller caches

### Job Parallelization

1. **Matrix Builds**
   - Test across multiple Node.js versions
   - Run tests in parallel across different OS
   - Split test suites into separate jobs

2. **Job Dependencies**
   - Use `needs` to create job dependency chains
   - Run independent jobs in parallel
   - Share artifacts between dependent jobs

### Performance Tips

1. **Reduce Checkout Time**
   - Use shallow clones: `fetch-depth: 1`
   - Only checkout when necessary
   - Skip submodules if not needed

2. **Optimize Installation**
   - Use frozen lockfiles to skip dependency resolution
   - Enable package manager caching
   - Consider using pnpm for faster installs

3. **Conditional Execution**
   - Skip jobs based on file changes using `paths` filter
   - Use `if` conditions to skip unnecessary steps
   - Exit early when possible

## Security Best Practices

### Secrets Management

1. **Store Sensitive Data Securely**
   - Use GitHub Secrets for credentials
   - Never log secrets or expose in URLs
   - Use environment-specific secrets

2. **Token Permissions**
   - Use minimal required permissions
   - Prefer `GITHUB_TOKEN` over personal access tokens
   - Set explicit permissions in workflow file

3. **Dependency Security**
   - Pin action versions to specific commits
   - Enable Dependabot for action updates
   - Review third-party action code

### Access Control

1. **Environment Protection**
   - Use environment protection rules for production
   - Require manual approval for critical deployments
   - Limit who can approve deployments

2. **Branch Protection**
   - Require status checks before merge
   - Enable branch protection rules
   - Prevent force pushes to main branch

## Deployment Strategies

### Preview Deployments

1. **Per-PR Previews**
   - Deploy each PR to unique preview URL
   - Comment URL on PR for easy access
   - Clean up when PR is closed

2. **Preview Environment Configuration**
   - Use separate environment variables
   - Connect to preview database/services
   - Enable debug logging

### Production Deployments

1. **Blue-Green Deployment**
   - Deploy to new environment
   - Run smoke tests
   - Switch traffic when verified

2. **Rollback Strategy**
   - Keep previous deployment available
   - Tag successful deployments
   - Automate rollback on failure

3. **Deployment Gates**
   - Manual approval for production
   - Require successful CI before deploy
   - Schedule deployments during maintenance windows

## Monitoring and Debugging

### Workflow Monitoring

1. **Status Badges**
   - Add status badges to README
   - Monitor workflow success rates
   - Track deployment frequency

2. **Notifications**
   - Set up Slack/Discord notifications
   - Alert on deployment failures
   - Send deployment summaries

### Debugging Workflows

1. **Enable Debug Logging**
   - Set `ACTIONS_STEP_DEBUG` secret to `true`
   - Use `::debug::` commands in scripts
   - Review workflow run logs

2. **Test Locally**
   - Use `act` to run workflows locally
   - Test workflow changes in fork
   - Validate YAML syntax before commit

## Common Patterns

### Monorepo Support

```yaml
on:
  push:
    paths:
      - 'packages/frontend/**'
      - 'packages/shared/**'
```

### Conditional Steps

```yaml
- name: Deploy to production
  if: github.ref == 'refs/heads/main' && github.event_name == 'push'
  run: npm run deploy
```

### Reusable Workflows

```yaml
jobs:
  call-reusable:
    uses: org/repo/.github/workflows/reusable.yml@main
    with:
      environment: production
```

### Composite Actions

Create reusable composite actions for common tasks:

```yaml
# .github/actions/setup-node/action.yml
name: Setup Node.js
runs:
  using: composite
  steps:
    - uses: actions/setup-node@v4
      with:
        node-version: '20'
        cache: 'npm'
    - run: npm ci
      shell: bash
```

## Cost Optimization

1. **Reduce Workflow Minutes**
   - Cache aggressively
   - Skip unnecessary jobs
   - Use self-hosted runners for high-volume repos

2. **Efficient Runners**
   - Use smallest runner size that meets requirements
   - Self-host runners for private repos
   - Schedule resource-intensive jobs during off-peak

3. **Artifact Management**
   - Set appropriate retention days
   - Clean up old artifacts
   - Compress artifacts before upload

## Framework-Specific Tips

### Next.js

- Cache `.next/cache` directory
- Set `NEXT_TELEMETRY_DISABLED=1`
- Use `next build` output for deployment
- Configure ISR revalidation appropriately

### Vite

- Cache `node_modules/.vite` directory
- Enable build caching
- Use `vite build` for production builds

### Testing

- Run unit and integration tests in parallel
- Upload test results and coverage
- Use matrix builds for cross-browser testing
- Consider Playwright for E2E tests

## Troubleshooting

### Common Issues

1. **Cache Not Restoring**
   - Verify cache key matches
   - Check cache size limits
   - Ensure paths are correct

2. **Permission Errors**
   - Check GITHUB_TOKEN permissions
   - Verify repository settings
   - Review branch protection rules

3. **Timeout Errors**
   - Increase job timeout
   - Split into smaller jobs
   - Optimize dependencies

4. **Build Failures**
   - Check environment variables
   - Verify Node.js version
   - Review dependency compatibility
