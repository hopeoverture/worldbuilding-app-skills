# Tailwind CSS v4 Migration Guide

## Overview

Tailwind CSS v4 introduces significant changes to configuration and usage patterns. This document outlines the differences and provides migration guidance.

## Current Status (as of January 2025)

- **Tailwind CSS v3.x**: Stable, widely adopted
- **Tailwind CSS v4**: In development, alpha/beta releases available
- **Recommendation**: Use v3 with forward-compatible patterns for production projects

## Key Differences: v3 vs v4

### Configuration Format

**v3 (Current)**
```ts
// tailwind.config.ts
import type { Config } from 'tailwindcss'

export default {
  darkMode: 'class',
  content: ['./app/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: { /* ... */ }
    }
  },
  plugins: []
} satisfies Config
```

**v4 (Future)**
```css
/* @config directive in CSS */
@config "./tailwind.config.js";

@theme {
  --color-brand: #3b82f6;
  --font-sans: system-ui, sans-serif;
}
```

### CSS Variables & Tokens

**v3 Pattern (Forward-Compatible)**
```css
:root {
  --background: 0 0% 100%;
  --foreground: 222.2 84% 4.9%;
}

.dark {
  --background: 222.2 84% 4.9%;
  --foreground: 210 40% 98%;
}
```

```ts
// tailwind.config.ts
colors: {
  background: 'hsl(var(--background))',
  foreground: 'hsl(var(--foreground))'
}
```

**v4 Expected Pattern**
```css
@theme {
  --color-background: oklch(100% 0 0);
  --color-foreground: oklch(20% 0.02 270);
}
```

### Plugin System

**v3**: JavaScript-based plugins in config file
**v4**: CSS-based plugins with `@plugin` directive

## Migration Strategy

### Phase 1: v3 with Forward-Compatible Patterns (Current)

Use CSS variables extensively:
- Define semantic tokens (--primary, --background, etc.)
- Use HSL/OKLCH color space for easier manipulation
- Structure CSS variables to match expected v4 patterns

### Phase 2: v4 Alpha/Beta Testing (When Available)

Test v4 alphas in non-production projects:
```bash
npm install tailwindcss@next
```

Update configuration:
- Move color tokens to `@theme` directive
- Convert plugins to CSS-based format
- Test build performance and output

### Phase 3: v4 Stable Migration (Future)

When v4 is stable:
1. Update package: `npm install tailwindcss@latest`
2. Migrate config format (may have migration tool)
3. Test thoroughly across all components
4. Update documentation

## Recommended Patterns for This Skill

### Use CSS Custom Properties

[OK] **Good (Forward-Compatible)**
```css
:root {
  --radius: 0.5rem;
  --primary: 222.2 47.4% 11.2%;
}

.card {
  border-radius: var(--radius);
  background: hsl(var(--primary));
}
```

[ERROR] **Avoid (Hard-Coded)**
```css
.card {
  border-radius: 0.5rem;
  background: #1e293b;
}
```

### Semantic Color Naming

Use semantic names that describe purpose, not appearance:
- [OK] `--primary`, `--destructive`, `--muted`
- [ERROR] `--blue-500`, `--red-600`, `--gray-200`

### HSL Color Space

Use HSL (or OKLCH when v4 is available) for better color manipulation:
```css
/* HSL: Hue Saturation Lightness */
--primary: 222.2 47.4% 11.2%;

/* Usage in CSS */
background: hsl(var(--primary));
background: hsl(var(--primary) / 0.8); /* With alpha */
```

## Checking for v4 Availability

```bash
# Check installed version
npm list tailwindcss

# Check latest available version
npm view tailwindcss versions --json

# Install specific version
npm install tailwindcss@4.0.0  # When available
```

## V4-Specific Features to Watch For

### CSS-First Configuration
- `@theme` directive for token definition
- `@plugin` for extending functionality
- Native CSS nesting support

### Improved Color System
- OKLCH color space support
- Better color mixing
- Improved dark mode handling

### Performance Improvements
- Faster build times
- Smaller CSS output
- Better JIT performance

### New Utilities
- Container queries (better support)
- Cascade layers
- View transitions

## Resources

- **Tailwind CSS Docs**: https://tailwindcss.com/docs
- **V4 Alpha Docs**: https://tailwindcss.com/docs/v4-alpha
- **GitHub Discussions**: https://github.com/tailwindlabs/tailwindcss/discussions
- **Upgrade Guide**: https://tailwindcss.com/docs/upgrade-guide (when v4 is stable)

## Notes for Skill Usage

When this skill runs:
1. Check Tailwind version: `npm view tailwindcss version`
2. If v4 stable is available: Use v4 configuration patterns
3. If v4 is not available: Use v3 with forward-compatible CSS variables
4. Add comments in generated files indicating v4 migration points:
   ```ts
   // TODO: When upgrading to Tailwind v4, move these tokens to @theme directive
   ```

This approach ensures the skill produces production-ready code today while being ready for v4 when it arrives.
