# Theme Token System

## Overview

This document describes the CSS custom property-based design token system used for Tailwind + shadcn/ui theming.

## Token Philosophy

### Semantic Naming
Tokens describe **purpose**, not appearance:
- [OK] `--primary` (describes role)
- [ERROR] `--blue-600` (describes appearance)

### Benefits
- Easy theme switching
- Consistent design system
- Automatic dark mode support
- Forward-compatible with Tailwind v4

## Color Token Structure

### HSL Format

All colors use HSL (Hue, Saturation, Lightness) format without the `hsl()` wrapper:

```css
/* Define as space-separated values */
--primary: 222.2 47.4% 11.2%;

/* Use with hsl() wrapper */
background-color: hsl(var(--primary));

/* With alpha transparency */
background-color: hsl(var(--primary) / 0.5);
```

### Why HSL?
- **Intuitive**: Easier to adjust than RGB
- **Lightness control**: Simple to create shades
- **Alpha transparency**: Works with modern CSS syntax
- **Tooling**: Better design tool support

## Core Color Tokens

### Base Colors

```css
:root {
  /* Background & Foreground */
  --background: 0 0% 100%;           /* Pure white */
  --foreground: 222.2 84% 4.9%;      /* Near black text */

  /* Card (elevated surfaces) */
  --card: 0 0% 100%;                 /* White card background */
  --card-foreground: 222.2 84% 4.9%; /* Card text */

  /* Popover (floating UI) */
  --popover: 0 0% 100%;              /* White popover */
  --popover-foreground: 222.2 84% 4.9%; /* Popover text */
}
```

### Semantic Colors

```css
:root {
  /* Primary (brand color, main actions) */
  --primary: 222.2 47.4% 11.2%;
  --primary-foreground: 210 40% 98%;

  /* Secondary (less prominent actions) */
  --secondary: 210 40% 96.1%;
  --secondary-foreground: 222.2 47.4% 11.2%;

  /* Muted (disabled states, subtle backgrounds) */
  --muted: 210 40% 96.1%;
  --muted-foreground: 215.4 16.3% 46.9%;

  /* Accent (highlights, hover states) */
  --accent: 210 40% 96.1%;
  --accent-foreground: 222.2 47.4% 11.2%;

  /* Destructive (errors, delete actions) */
  --destructive: 0 84.2% 60.2%;
  --destructive-foreground: 210 40% 98%;
}
```

### UI Element Colors

```css
:root {
  /* Borders */
  --border: 214.3 31.8% 91.4%;       /* Subtle border */
  --input: 214.3 31.8% 91.4%;        /* Input border */

  /* Focus & Selection */
  --ring: 222.2 84% 4.9%;            /* Focus ring */

  /* Status Colors (optional) */
  --success: 142 76% 36%;
  --success-foreground: 0 0% 100%;
  --warning: 38 92% 50%;
  --warning-foreground: 0 0% 100%;
  --info: 199 89% 48%;
  --info-foreground: 0 0% 100%;
}
```

## Dark Mode Tokens

### Dark Mode Strategy

Use `.dark` class to override tokens:

```css
.dark {
  /* Base */
  --background: 222.2 84% 4.9%;      /* Near black */
  --foreground: 210 40% 98%;         /* Near white */

  /* Card */
  --card: 222.2 84% 4.9%;
  --card-foreground: 210 40% 98%;

  /* Primary */
  --primary: 210 40% 98%;
  --primary-foreground: 222.2 47.4% 11.2%;

  /* Secondary */
  --secondary: 217.2 32.6% 17.5%;
  --secondary-foreground: 210 40% 98%;

  /* Muted */
  --muted: 217.2 32.6% 17.5%;
  --muted-foreground: 215 20.2% 65.1%;

  /* Accent */
  --accent: 217.2 32.6% 17.5%;
  --accent-foreground: 210 40% 98%;

  /* Destructive */
  --destructive: 0 62.8% 30.6%;
  --destructive-foreground: 210 40% 98%;

  /* Borders */
  --border: 217.2 32.6% 17.5%;
  --input: 217.2 32.6% 17.5%;

  /* Focus */
  --ring: 212.7 26.8% 83.9%;
}
```

## Theme Presets

### Zinc (Default)

Cool, neutral gray tones. Professional and versatile.

```css
:root {
  --background: 0 0% 100%;
  --foreground: 240 10% 3.9%;
  --primary: 240 5.9% 10%;
  --primary-foreground: 0 0% 98%;
  --muted: 240 4.8% 95.9%;
  --muted-foreground: 240 3.8% 46.1%;
  --border: 240 5.9% 90%;
}

.dark {
  --background: 240 10% 3.9%;
  --foreground: 0 0% 98%;
  --primary: 0 0% 98%;
  --primary-foreground: 240 5.9% 10%;
  --muted: 240 3.7% 15.9%;
  --muted-foreground: 240 5% 64.9%;
  --border: 240 3.7% 15.9%;
}
```

### Slate

Slightly cooler than Zinc. Tech-focused feel.

```css
:root {
  --background: 0 0% 100%;
  --foreground: 222.2 84% 4.9%;
  --primary: 222.2 47.4% 11.2%;
  --primary-foreground: 210 40% 98%;
  --muted: 210 40% 96.1%;
  --muted-foreground: 215.4 16.3% 46.9%;
  --border: 214.3 31.8% 91.4%;
}

.dark {
  --background: 222.2 84% 4.9%;
  --foreground: 210 40% 98%;
  --primary: 210 40% 98%;
  --primary-foreground: 222.2 47.4% 11.2%;
  --muted: 217.2 32.6% 17.5%;
  --muted-foreground: 215 20.2% 65.1%;
  --border: 217.2 32.6% 17.5%;
}
```

### Neutral

True neutral grays. Clean and minimal.

```css
:root {
  --background: 0 0% 100%;
  --foreground: 0 0% 3.9%;
  --primary: 0 0% 9%;
  --primary-foreground: 0 0% 98%;
  --muted: 0 0% 96.1%;
  --muted-foreground: 0 0% 45.1%;
  --border: 0 0% 89.8%;
}

.dark {
  --background: 0 0% 3.9%;
  --foreground: 0 0% 98%;
  --primary: 0 0% 98%;
  --primary-foreground: 0 0% 9%;
  --muted: 0 0% 14.9%;
  --muted-foreground: 0 0% 63.9%;
  --border: 0 0% 14.9%;
}
```

## Spacing & Sizing Tokens

### Border Radius

```css
:root {
  --radius: 0.5rem;  /* Base radius: 8px */
}

/* Usage in Tailwind config */
borderRadius: {
  lg: 'var(--radius)',
  md: 'calc(var(--radius) - 2px)',
  sm: 'calc(var(--radius) - 4px)',
}
```

### Font Family (Optional)

```css
:root {
  --font-sans: ui-sans-serif, system-ui, sans-serif;
  --font-mono: ui-monospace, 'Cascadia Code', monospace;
}
```

## Usage in Tailwind Config

### Extending Theme

```ts
// tailwind.config.ts
export default {
  theme: {
    extend: {
      colors: {
        border: 'hsl(var(--border))',
        input: 'hsl(var(--input))',
        ring: 'hsl(var(--ring))',
        background: 'hsl(var(--background))',
        foreground: 'hsl(var(--foreground))',
        primary: {
          DEFAULT: 'hsl(var(--primary))',
          foreground: 'hsl(var(--primary-foreground))'
        },
        secondary: {
          DEFAULT: 'hsl(var(--secondary))',
          foreground: 'hsl(var(--secondary-foreground))'
        },
        destructive: {
          DEFAULT: 'hsl(var(--destructive))',
          foreground: 'hsl(var(--destructive-foreground))'
        },
        muted: {
          DEFAULT: 'hsl(var(--muted))',
          foreground: 'hsl(var(--muted-foreground))'
        },
        accent: {
          DEFAULT: 'hsl(var(--accent))',
          foreground: 'hsl(var(--accent-foreground))'
        },
        popover: {
          DEFAULT: 'hsl(var(--popover))',
          foreground: 'hsl(var(--popover-foreground))'
        },
        card: {
          DEFAULT: 'hsl(var(--card))',
          foreground: 'hsl(var(--card-foreground))'
        }
      },
      borderRadius: {
        lg: 'var(--radius)',
        md: 'calc(var(--radius) - 2px)',
        sm: 'calc(var(--radius) - 4px)'
      }
    }
  }
}
```

## Using Tokens in Components

### In CSS

```css
.custom-component {
  background-color: hsl(var(--background));
  color: hsl(var(--foreground));
  border: 1px solid hsl(var(--border));
  border-radius: var(--radius);
}

/* With alpha */
.overlay {
  background-color: hsl(var(--background) / 0.8);
}
```

### With Tailwind Utilities

```tsx
<div className="bg-background text-foreground border-border">
  <h1 className="text-primary">Heading</h1>
  <p className="text-muted-foreground">Subtitle</p>
  <Button variant="destructive">Delete</Button>
</div>
```

## Customization Guide

### Changing Primary Color

1. **Find your HSL values**: Use a color picker that shows HSL
2. **Update light mode**:
   ```css
   :root {
     --primary: 270 80% 45%;  /* Purple example */
     --primary-foreground: 0 0% 100%;  /* White text */
   }
   ```
3. **Update dark mode**:
   ```css
   .dark {
     --primary: 270 80% 65%;  /* Lighter purple */
     --primary-foreground: 240 10% 10%;  /* Dark text */
   }
   ```
4. **Test contrast**: Use WebAIM contrast checker

### Creating Custom Tokens

```css
/* Add to globals.css */
:root {
  /* Custom tokens */
  --sidebar-width: 16rem;
  --header-height: 4rem;
  --brand-gradient: linear-gradient(135deg, hsl(var(--primary)), hsl(var(--accent)));
}

/* Use in components */
.sidebar {
  width: var(--sidebar-width);
}
```

### Adding More Semantic Colors

```css
:root {
  --success: 142 76% 36%;
  --success-foreground: 0 0% 100%;
  --warning: 38 92% 50%;
  --warning-foreground: 0 0% 100%;
}

.dark {
  --success: 142 71% 45%;
  --warning: 38 92% 60%;
}
```

```ts
// Add to tailwind.config.ts
colors: {
  success: {
    DEFAULT: 'hsl(var(--success))',
    foreground: 'hsl(var(--success-foreground))'
  },
  warning: {
    DEFAULT: 'hsl(var(--warning))',
    foreground: 'hsl(var(--warning-foreground))'
  }
}
```

## Best Practices

### 1. Always Pair Background/Foreground

```tsx
[OK] Good
<div className="bg-primary text-primary-foreground">
  Readable text
</div>

[ERROR] Bad
<div className="bg-primary text-foreground">
  Low contrast
</div>
```

### 2. Test Both Themes

Always verify colors in both light and dark mode:
```bash
# Use browser DevTools to toggle:
document.documentElement.classList.toggle('dark')
```

### 3. Use Semantic Tokens

```tsx
[OK] Good (semantic)
<p className="text-muted-foreground">Helper text</p>
<Button variant="destructive">Delete</Button>

[ERROR] Bad (hard-coded)
<p className="text-gray-500 dark:text-gray-400">Helper text</p>
<Button className="bg-red-600">Delete</Button>
```

### 4. Maintain Contrast Ratios

- Normal text: ≥ 4.5:1
- Large text: ≥ 3:1
- UI components: ≥ 3:1

## Tools for Theme Development

### Color Pickers with HSL
- [HSL Color Picker](https://hslpicker.com/)
- [Coolors](https://coolors.co/)
- [Palettte App](https://palettte.app/)

### Contrast Checkers
- [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/)
- [Contrast Ratio](https://contrast-ratio.com/)
- Chrome DevTools (Lighthouse)

### Theme Generators
- [Realtime Colors](https://realtimecolors.com/)
- [shadcn/ui Themes](https://ui.shadcn.com/themes)
- [Tailwind Color Generator](https://uicolors.app/create)

## Example: Complete Theme

```css
/* globals.css */
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  :root {
    /* Base */
    --background: 0 0% 100%;
    --foreground: 240 10% 3.9%;

    /* UI Elements */
    --card: 0 0% 100%;
    --card-foreground: 240 10% 3.9%;
    --popover: 0 0% 100%;
    --popover-foreground: 240 10% 3.9%;

    /* Primary Brand */
    --primary: 240 5.9% 10%;
    --primary-foreground: 0 0% 98%;

    /* Secondary Actions */
    --secondary: 240 4.8% 95.9%;
    --secondary-foreground: 240 5.9% 10%;

    /* Muted Elements */
    --muted: 240 4.8% 95.9%;
    --muted-foreground: 240 3.8% 46.1%;

    /* Accents */
    --accent: 240 4.8% 95.9%;
    --accent-foreground: 240 5.9% 10%;

    /* Destructive */
    --destructive: 0 84.2% 60.2%;
    --destructive-foreground: 0 0% 98%;

    /* Borders & Inputs */
    --border: 240 5.9% 90%;
    --input: 240 5.9% 90%;
    --ring: 240 5.9% 10%;

    /* Radius */
    --radius: 0.5rem;
  }

  .dark {
    --background: 240 10% 3.9%;
    --foreground: 0 0% 98%;
    --card: 240 10% 3.9%;
    --card-foreground: 0 0% 98%;
    --popover: 240 10% 3.9%;
    --popover-foreground: 0 0% 98%;
    --primary: 0 0% 98%;
    --primary-foreground: 240 5.9% 10%;
    --secondary: 240 3.7% 15.9%;
    --secondary-foreground: 0 0% 98%;
    --muted: 240 3.7% 15.9%;
    --muted-foreground: 240 5% 64.9%;
    --accent: 240 3.7% 15.9%;
    --accent-foreground: 0 0% 98%;
    --destructive: 0 62.8% 30.6%;
    --destructive-foreground: 0 0% 98%;
    --border: 240 3.7% 15.9%;
    --input: 240 3.7% 15.9%;
    --ring: 240 4.9% 83.9%;
  }
}
```

## Resources

- **HSL Color Space**: https://developer.mozilla.org/en-US/docs/Web/CSS/color_value/hsl
- **shadcn/ui Theming**: https://ui.shadcn.com/docs/theming
- **Tailwind CSS Customization**: https://tailwindcss.com/docs/customizing-colors
- **Design Tokens**: https://www.w3.org/community/design-tokens/
