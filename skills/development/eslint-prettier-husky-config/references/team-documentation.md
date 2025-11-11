# Code Quality Setup - Team Documentation

## Overview

This project uses automated code quality tools to maintain consistent code style and catch errors early:

- **ESLint** - Identifies code quality issues and potential bugs
- **Prettier** - Automatically formats code to consistent style
- **Husky** - Runs quality checks before commits via git hooks
- **lint-staged** - Only checks files you're committing (fast!)
- **GitHub Actions** - Verifies code quality in CI

## For New Team Members

### First Time Setup

After cloning the repository, run:

```bash
npm install
```

This automatically sets up Husky git hooks via the `prepare` script.

### Daily Workflow

When you make changes and commit:

1. Stage your files: `git add .`
2. Commit: `git commit -m "your message"`
3. **Pre-commit hook automatically runs** and checks your staged files
4. If checks pass, commit succeeds
5. If checks fail, fix the issues and try again

### Manual Quality Checks

Run these commands any time:

```bash
# Check for linting errors
npm run lint

# Auto-fix linting issues
npm run lint:fix

# Format all files
npm run format

# Check formatting (doesn't modify files)
npm run format:check
```

### IDE Integration

**Recommended**: Install ESLint and Prettier extensions in your editor:

- **VS Code**: Install "ESLint" and "Prettier - Code formatter" extensions
- **WebStorm/IntelliJ**: Enable ESLint and Prettier in Settings > Languages & Frameworks

Configure format on save in your editor for the best experience.

## Common Scenarios

### Pre-commit Hook Fails

**Linting errors**: Review the errors shown. Run `npm run lint:fix` to auto-fix many issues.

**Formatting issues**: Run `npm run format` to format all files, then try committing again.

**Type errors**: Fix TypeScript errors shown in the output. The hook prevents commits with type errors.

### Bypassing Hooks (Emergency Only)

In rare cases where you need to commit despite failing checks:

```bash
git commit --no-verify -m "your message"
```

**Warning**: Only use this for emergencies. The CI will still fail if code quality checks don't pass.

### Updating ESLint Rules

If you encounter a rule that doesn't make sense for your use case:

1. Discuss with the team first
2. Update `eslint.config.mjs` with the agreed change
3. Run `npm run lint` to verify the change works
4. Commit the configuration change

## Troubleshooting

### Hooks Not Running

If pre-commit hooks don't run when you commit:

```bash
# Reinstall Husky
rm -rf .husky
npm run prepare
```

Verify `.husky/pre-commit` exists and is executable.

### ESLint Configuration Errors

If ESLint fails to run with configuration errors:

```bash
# Check your Node version (should be 18+)
node --version

# Reinstall dependencies
rm -rf node_modules package-lock.json
npm install
```

### Conflicts Between Tools

If ESLint and Prettier report conflicting issues:

- Prettier should always win for formatting issues
- Check that `eslint-config-prettier` is installed
- Verify it's last in the config chain to disable conflicting ESLint rules

### CI Passing Locally But Failing in GitHub Actions

- Ensure you've committed all configuration files
- Verify Node.js version matches between local and CI
- Check that all devDependencies are in package.json
- Run `npm run lint` and `npm run format:check` locally before pushing

## Configuration Files

- `eslint.config.mjs` - ESLint rules and configuration
- `.prettierrc` - Prettier formatting rules
- `.prettierignore` - Files Prettier should skip
- `.husky/pre-commit` - Pre-commit hook that runs lint-staged
- `package.json` - Contains lint-staged configuration and scripts
- `.github/workflows/lint.yml` - CI workflow for automated checks

## Additional Resources

- [ESLint Documentation](https://eslint.org/docs/latest/)
- [Prettier Documentation](https://prettier.io/docs/en/)
- [Husky Documentation](https://typicode.github.io/husky/)
- [lint-staged Documentation](https://github.com/lint-staged/lint-staged)
