# Accessibility Checklist for Tailwind + shadcn/ui Setup

## Overview

This checklist ensures the Tailwind + shadcn/ui setup meets WCAG 2.1 Level AA standards and provides an inclusive user experience.

## Color & Contrast

### Requirements
- [OK] Normal text (< 18pt): Contrast ratio ≥ 4.5:1
- [OK] Large text (≥ 18pt or bold 14pt): Contrast ratio ≥ 3:1
- [OK] UI components: Contrast ratio ≥ 3:1
- [OK] Focus indicators: Contrast ratio ≥ 3:1

### Implementation

```css
/* Light mode - High contrast */
:root {
  --background: 0 0% 100%;        /* White */
  --foreground: 222.2 84% 4.9%;   /* Near black - 16.7:1 ratio */
  --muted: 210 40% 96.1%;         /* Light gray background */
  --muted-foreground: 215.4 16.3% 46.9%; /* Medium gray text - 4.6:1 ratio */
  --border: 214.3 31.8% 91.4%;    /* Light border */
}

/* Dark mode - High contrast */
.dark {
  --background: 222.2 84% 4.9%;   /* Near black */
  --foreground: 210 40% 98%;      /* Near white - 16.5:1 ratio */
  --muted: 217.2 32.6% 17.5%;     /* Dark gray background */
  --muted-foreground: 215 20.2% 65.1%; /* Light gray text - 6.8:1 ratio */
  --border: 217.2 32.6% 17.5%;    /* Dark border */
}
```

### Testing Contrast

```bash
# Use online tools:
# - https://webaim.org/resources/contrastchecker/
# - https://contrast-ratio.com/
# - Chrome DevTools (Lighthouse audit)

# Or programmatically:
npm install --save-dev axe-core @axe-core/playwright
```

## Focus Management

### Visible Focus Indicators

```css
/* Global focus styles */
@layer base {
  *:focus-visible {
    @apply outline-none ring-2 ring-ring ring-offset-2 ring-offset-background;
  }

  /* Respect reduced motion */
  @media (prefers-reduced-motion: reduce) {
    *:focus-visible {
      @apply transition-none;
    }
  }
}
```

### Focus Order
- [OK] Logical tab order (follows visual order)
- [OK] No keyboard traps
- [OK] Skip links for navigation
- [OK] Focus moves appropriately in modals/dialogs

### Implementation

```tsx
// Skip link (in layout)
<a
  href="#main-content"
  className="sr-only focus:not-sr-only focus:absolute focus:top-4 focus:left-4 focus:z-50"
>
  Skip to main content
</a>

{/* Rest of layout */}
<main id="main-content">
  {children}
</main>
```

## Keyboard Navigation

### Requirements
- [OK] All interactive elements keyboard accessible
- [OK] Logical tab order
- [OK] Keyboard shortcuts don't conflict
- [OK] Escape closes modals/dropdowns
- [OK] Arrow keys for menus/lists
- [OK] Enter/Space activates buttons

### shadcn/ui Components

All shadcn/ui components support keyboard navigation out of the box:

```tsx
// Dialog - auto-handles:
// - ESC to close
// - Focus trap
// - Return focus on close
<Dialog>
  <DialogContent>
    <DialogTitle>Title</DialogTitle>
    {/* Content */}
  </DialogContent>
</Dialog>

// Dropdown - auto-handles:
// - Arrow keys for navigation
// - Enter to select
// - ESC to close
<DropdownMenu>
  <DropdownMenuTrigger>Menu</DropdownMenuTrigger>
  <DropdownMenuContent>
    <DropdownMenuItem>Item 1</DropdownMenuItem>
  </DropdownMenuContent>
</DropdownMenu>
```

## Semantic HTML

### Use Proper Elements

```tsx
[OK] Good - Semantic
<nav aria-label="Main navigation">
  <ul>
    <li><a href="/">Home</a></li>
  </ul>
</nav>

<main>
  <article>
    <h1>Article Title</h1>
    <p>Content...</p>
  </article>
</main>

<footer>
  <p>&copy; 2025 Company</p>
</footer>

[ERROR] Bad - Non-semantic
<div className="nav">
  <div className="link" onClick={goHome}>Home</div>
</div>

<div className="main">
  <div className="article">
    <div className="title">Article Title</div>
    <div>Content...</div>
  </div>
</div>
```

### Heading Hierarchy

```tsx
[OK] Good - Logical hierarchy
<h1>Page Title</h1>
  <h2>Section</h2>
    <h3>Subsection</h3>
  <h2>Another Section</h2>

[ERROR] Bad - Skips levels
<h1>Page Title</h1>
  <h3>Section</h3>  {/* Skipped h2 */}
  <h2>Another Section</h2>  {/* Out of order */}
```

## Form Accessibility

### Always Pair Labels with Inputs

```tsx
[OK] Good
<div className="space-y-2">
  <Label htmlFor="email">Email address</Label>
  <Input id="email" type="email" required aria-required="true" />
</div>

[ERROR] Bad
<Input placeholder="Email address" />  {/* Placeholder is not a label */}
```

### Error Messages

```tsx
<div className="space-y-2">
  <Label htmlFor="password">Password</Label>
  <Input
    id="password"
    type="password"
    aria-invalid={!!errors.password}
    aria-describedby={errors.password ? "password-error" : undefined}
  />
  {errors.password && (
    <p id="password-error" className="text-sm text-destructive" role="alert">
      {errors.password.message}
    </p>
  )}
</div>
```

### Required Fields

```tsx
<Label htmlFor="username">
  Username
  <span className="text-destructive" aria-label="required">*</span>
</Label>
<Input id="username" required aria-required="true" />
```

## ARIA Attributes

### When to Use ARIA

**First Rule**: Don't use ARIA unless necessary. Use semantic HTML first.

```tsx
[OK] Good - Semantic HTML (no ARIA needed)
<button>Click me</button>

[ERROR] Unnecessary ARIA
<div role="button" tabIndex={0} onClick={...}>Click me</div>
```

### Common ARIA Patterns

```tsx
// Live regions for dynamic content
<div role="status" aria-live="polite" aria-atomic="true">
  {statusMessage}
</div>

// Loading state
<Button disabled={isLoading} aria-busy={isLoading}>
  {isLoading ? "Loading..." : "Submit"}
</Button>

// Icon buttons need labels
<Button size="icon" aria-label="Close menu">
  <X className="h-4 w-4" />
</Button>

// Expanded/collapsed state
<Button
  aria-expanded={isOpen}
  aria-controls="content-id"
  onClick={() => setIsOpen(!isOpen)}
>
  Toggle
</Button>
<div id="content-id" hidden={!isOpen}>
  Content
</div>
```

## Screen Reader Support

### Visually Hidden Content

Use `.sr-only` for screen-reader-only text:

```tsx
<Button>
  <span className="sr-only">Delete item</span>
  <Trash className="h-4 w-4" aria-hidden="true" />
</Button>
```

### Skip Links

```tsx
<a
  href="#main-content"
  className="sr-only focus:not-sr-only focus:absolute focus:top-4 focus:left-4 focus:z-50 focus:px-4 focus:py-2 focus:bg-background focus:ring-2"
>
  Skip to main content
</a>
```

### Icon-Only Buttons

```tsx
// Always provide text alternative
<Button variant="ghost" size="icon" aria-label="Search">
  <Search className="h-4 w-4" />
</Button>

// Or use tooltip with title
<Button variant="ghost" size="icon" title="Search">
  <Search className="h-4 w-4" />
  <span className="sr-only">Search</span>
</Button>
```

## Motion & Animation

### Respect User Preferences

```css
/* Disable animations for users who prefer reduced motion */
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

### Implementation in Components

```tsx
// Add to globals.css
@layer base {
  @media (prefers-reduced-motion: reduce) {
    * {
      animation-duration: 0.01ms !important;
      animation-iteration-count: 1 !important;
      transition-duration: 0.01ms !important;
      scroll-behavior: auto !important;
    }
  }
}
```

## Dark Mode Accessibility

### Proper Contrast in Both Modes

```css
/* Test both themes */
:root {
  /* Light mode */
  --primary: 222.2 47.4% 11.2%;
  --primary-foreground: 210 40% 98%;
  /* Ensure ≥ 4.5:1 ratio */
}

.dark {
  /* Dark mode */
  --primary: 217.2 91.2% 59.8%;
  --primary-foreground: 222.2 47.4% 11.2%;
  /* Ensure ≥ 4.5:1 ratio */
}
```

### Flash Prevention

```tsx
// In app/layout.tsx
<html lang="en" suppressHydrationWarning>
  <body>
    <ThemeProvider
      attribute="class"
      defaultTheme="system"
      enableSystem
      disableTransitionOnChange  {/* Prevent flash */}
    >
      {children}
    </ThemeProvider>
  </body>
</html>
```

## Testing Checklist

### Manual Testing

- [ ] Navigate entire app with keyboard only (no mouse)
- [ ] Test with screen reader (NVDA, JAWS, VoiceOver)
- [ ] Zoom to 200% and ensure layout doesn't break
- [ ] Test in high contrast mode
- [ ] Verify dark mode contrast
- [ ] Check focus indicators on all interactive elements
- [ ] Test form validation with screen reader

### Automated Testing

```bash
# Install axe-core
npm install --save-dev @axe-core/playwright

# Use in tests
import { test, expect } from '@playwright/test'
import { injectAxe, checkA11y } from 'axe-playwright'

test('homepage is accessible', async ({ page }) => {
  await page.goto('http://localhost:3000')
  await injectAxe(page)
  await checkA11y(page)
})
```

### Browser DevTools

- Chrome Lighthouse (Accessibility audit)
- Firefox Accessibility Inspector
- Edge Accessibility Insights
- axe DevTools Extension

## Common Issues & Fixes

### Issue: Missing Form Labels

```tsx
[ERROR] Problem
<Input placeholder="Email" />

[OK] Fix
<div>
  <Label htmlFor="email">Email</Label>
  <Input id="email" placeholder="you@example.com" />
</div>
```

### Issue: Non-Accessible Custom Components

```tsx
[ERROR] Problem
<div onClick={handleClick} className="cursor-pointer">
  Click me
</div>

[OK] Fix
<button onClick={handleClick} type="button">
  Click me
</button>
```

### Issue: Low Color Contrast

```tsx
[ERROR] Problem
<p className="text-gray-400">Important text</p>  {/* 2.8:1 ratio */}

[OK] Fix
<p className="text-gray-700 dark:text-gray-300">Important text</p>  {/* 5.2:1 ratio */}
```

### Issue: Missing Focus Indicators

```tsx
[ERROR] Problem
<Button className="focus:outline-none">Click</Button>

[OK] Fix
<Button className="focus-visible:ring-2 focus-visible:ring-ring">Click</Button>
```

## Resources

- **WCAG Guidelines**: https://www.w3.org/WAI/WCAG21/quickref/
- **WebAIM**: https://webaim.org/
- **a11y Project**: https://www.a11yproject.com/
- **Radix UI (shadcn base)**: https://radix-ui.com (includes A11y)
- **MDN Accessibility**: https://developer.mozilla.org/en-US/docs/Web/Accessibility

## Skill Implementation

This skill ensures:
- [OK] High contrast color tokens (≥ 4.5:1 for text)
- [OK] Visible focus styles with ring utilities
- [OK] Skip link in base layout
- [OK] Semantic HTML landmarks (header, nav, main, footer)
- [OK] Proper label/input associations
- [OK] Dark mode with accessible contrast
- [OK] Reduced motion support
- [OK] All shadcn components use Radix (accessible primitives)
