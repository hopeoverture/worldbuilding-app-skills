# Package.json Configuration Reference

## Complete Scripts and Lint-Staged Configuration

Add these sections to your `package.json`:

```json
{
  "name": "your-project",
  "version": "0.1.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "eslint . --max-warnings 0",
    "lint:fix": "eslint . --fix",
    "format": "prettier --write .",
    "format:check": "prettier --check .",
    "prepare": "husky"
  },
  "lint-staged": {
    "*.{js,jsx,ts,tsx}": [
      "eslint --fix",
      "prettier --write"
    ],
    "*.{json,md,yml,yaml,css,scss}": [
      "prettier --write"
    ]
  },
  "devDependencies": {
    "eslint": "^9.0.0",
    "@eslint/js": "^9.0.0",
    "eslint-config-prettier": "^9.1.0",
    "eslint-plugin-react": "^7.35.0",
    "eslint-plugin-react-hooks": "^4.6.0",
    "eslint-plugin-jsx-a11y": "^6.9.0",
    "@typescript-eslint/parser": "^7.0.0",
    "@typescript-eslint/eslint-plugin": "^7.0.0",
    "typescript-eslint": "^7.0.0",
    "prettier": "^3.3.0",
    "husky": "^9.0.0",
    "lint-staged": "^15.2.0"
  }
}
```

## Script Descriptions

- **lint**: Runs ESLint on entire codebase with zero warning tolerance (fails CI on warnings)
- **lint:fix**: Automatically fixes ESLint issues where possible
- **format**: Formats all files in project with Prettier
- **format:check**: Checks formatting without modifying files (good for CI)
- **prepare**: npm lifecycle hook that runs after `npm install` to set up Husky

## Lint-Staged Configuration

The `lint-staged` object defines which commands run on which file types during pre-commit:

- JavaScript/TypeScript files: Run ESLint with auto-fix, then Prettier
- Other files (JSON, Markdown, YAML, CSS): Run only Prettier

### Adding Type Checking

For stricter pre-commit checks, add TypeScript type checking:

```json
{
  "lint-staged": {
    "*.{ts,tsx}": [
      "eslint --fix",
      "prettier --write",
      "bash -c 'tsc --noEmit'"
    ],
    "*.{js,jsx}": [
      "eslint --fix",
      "prettier --write"
    ]
  }
}
```

Note: Type checking all staged files can slow down commits. Consider using it selectively.

### Adding Tests

To run tests on staged files:

```json
{
  "lint-staged": {
    "*.{ts,tsx,js,jsx}": [
      "eslint --fix",
      "prettier --write",
      "jest --bail --findRelatedTests"
    ]
  }
}
```

The `--findRelatedTests` flag runs only tests related to changed files.
