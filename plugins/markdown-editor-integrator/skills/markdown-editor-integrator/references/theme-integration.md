# Markdown Editor Theme Integration Guide

## Overview

Integrate @uiw/react-md-editor with shadcn/ui theming system for consistent light/dark mode support.

## Theme Switching

### Using next-themes

```tsx
'use client'

import { useTheme } from 'next-themes'
import MDEditor from '@uiw/react-md-editor'

export function ThemedMarkdownEditor({ value, onChange }) {
  const { theme } = useTheme()

  return (
    <div data-color-mode={theme === 'dark' ? 'dark' : 'light'}>
      <MDEditor
        value={value}
        onChange={onChange}
        height={400}
      />
    </div>
  )
}
```

### data-color-mode Attribute

The `data-color-mode` attribute controls the editor's theme:
- `light` - Light mode
- `dark` - Dark mode
- `auto` - System preference (default)

## CSS Variable Mapping

Map shadcn/ui CSS variables to editor styles:

```css
/* globals.css */

/* Editor Container */
.w-md-editor {
  --md-editor-bg: hsl(var(--background));
  --md-editor-color: hsl(var(--foreground));
  --md-editor-border: hsl(var(--border));
}

/* Toolbar */
.w-md-editor-toolbar {
  background-color: hsl(var(--muted) / 0.3);
  border-bottom-color: hsl(var(--border));
}

.w-md-editor-toolbar button {
  color: hsl(var(--foreground));
}

.w-md-editor-toolbar button:hover {
  background-color: hsl(var(--accent));
  color: hsl(var(--accent-foreground));
}

.w-md-editor-toolbar li.active button {
  background-color: hsl(var(--accent));
  color: hsl(var(--accent-foreground));
}

/* Editor Content */
.w-md-editor-content {
  color: hsl(var(--foreground));
}

.w-md-editor-text-pre,
.w-md-editor-text-input {
  color: hsl(var(--foreground));
  caret-color: hsl(var(--foreground));
}

/* Preview */
.w-md-editor-preview {
  background-color: hsl(var(--background));
  color: hsl(var(--foreground));
}

.wmde-markdown {
  background-color: transparent;
  color: hsl(var(--foreground));
}

/* Code Blocks */
.wmde-markdown pre {
  background-color: hsl(var(--muted));
}

.wmde-markdown code {
  background-color: hsl(var(--muted));
  color: hsl(var(--primary));
}

/* Inline Code */
.wmde-markdown :not(pre) > code {
  background-color: hsl(var(--muted));
  color: hsl(var(--primary));
  padding: 0.2em 0.4em;
  border-radius: 0.25rem;
  font-size: 0.875em;
}

/* Blockquotes */
.wmde-markdown blockquote {
  border-left-color: hsl(var(--primary) / 0.5);
  background-color: hsl(var(--muted) / 0.5);
  color: hsl(var(--muted-foreground));
}

/* Links */
.wmde-markdown a {
  color: hsl(var(--primary));
  text-decoration: underline;
}

.wmde-markdown a:hover {
  color: hsl(var(--primary) / 0.8);
}

/* Tables */
.wmde-markdown table {
  border-color: hsl(var(--border));
}

.wmde-markdown th,
.wmde-markdown td {
  border-color: hsl(var(--border));
}

.wmde-markdown th {
  background-color: hsl(var(--muted));
}

.wmde-markdown tr:nth-child(even) {
  background-color: hsl(var(--muted) / 0.3);
}

/* Horizontal Rule */
.wmde-markdown hr {
  border-color: hsl(var(--border));
}

/* Headings */
.wmde-markdown h1,
.wmde-markdown h2,
.wmde-markdown h3,
.wmde-markdown h4,
.wmde-markdown h5,
.wmde-markdown h6 {
  color: hsl(var(--foreground));
  border-bottom: none;
}
```

## Tailwind Class Approach

Use Tailwind utility classes for theming:

```tsx
'use client'

import { useTheme } from 'next-themes'
import MDEditor from '@uiw/react-md-editor'
import { cn } from '@/lib/utils'

export function MarkdownEditor({ value, onChange, className }) {
  const { theme } = useTheme()

  return (
    <div
      data-color-mode={theme === 'dark' ? 'dark' : 'light'}
      className={cn(
        'rounded-md border border-input overflow-hidden',
        className
      )}
    >
      <MDEditor
        value={value}
        onChange={onChange}
        height={400}
        className="shadow-none"
      />
    </div>
  )
}
```

## Typography Integration

Integrate with Tailwind Typography (prose):

```css
/* Preview with prose styling */
.w-md-editor-preview {
  @apply prose prose-sm dark:prose-invert max-w-none p-4;
}

/* Override prose defaults with theme colors */
.w-md-editor-preview.prose {
  --tw-prose-body: hsl(var(--foreground));
  --tw-prose-headings: hsl(var(--foreground));
  --tw-prose-links: hsl(var(--primary));
  --tw-prose-bold: hsl(var(--foreground));
  --tw-prose-code: hsl(var(--primary));
  --tw-prose-pre-bg: hsl(var(--muted));
  --tw-prose-quotes: hsl(var(--muted-foreground));
  --tw-prose-quote-borders: hsl(var(--primary) / 0.5);
}

.w-md-editor-preview.prose.dark {
  --tw-prose-body: hsl(var(--foreground));
  --tw-prose-headings: hsl(var(--foreground));
  --tw-prose-links: hsl(var(--primary));
  --tw-prose-bold: hsl(var(--foreground));
  --tw-prose-code: hsl(var(--primary));
  --tw-prose-pre-bg: hsl(var(--muted));
  --tw-prose-quotes: hsl(var(--muted-foreground));
  --tw-prose-quote-borders: hsl(var(--primary) / 0.5);
}
```

## Complete Component with Theme

```tsx
'use client'

import { useTheme } from 'next-themes'
import dynamic from 'next/dynamic'
import { ComponentProps, useEffect, useState } from 'react'
import rehypeSanitize from 'rehype-sanitize'
import { cn } from '@/lib/utils'

const MDEditor = dynamic(
  () => import('@uiw/react-md-editor'),
  { ssr: false }
)

type MDEditorProps = ComponentProps<typeof MDEditor>

interface MarkdownEditorProps extends Omit<MDEditorProps, 'data-color-mode'> {
  value: string
  onChange?: (value?: string) => void
  height?: number | string
  className?: string
}

export function MarkdownEditor({
  value,
  onChange,
  height = 400,
  className,
  ...props
}: MarkdownEditorProps) {
  const { theme, resolvedTheme } = useTheme()
  const [mounted, setMounted] = useState(false)

  useEffect(() => {
    setMounted(true)
  }, [])

  if (!mounted) {
    return (
      <div
        className={cn(
          'rounded-md border border-input bg-background',
          className
        )}
        style={{ height }}
      >
        <div className="flex items-center justify-center h-full text-muted-foreground">
          Loading editor...
        </div>
      </div>
    )
  }

  const colorMode = (resolvedTheme || theme) === 'dark' ? 'dark' : 'light'

  return (
    <div
      data-color-mode={colorMode}
      className={cn('markdown-editor-wrapper', className)}
    >
      <MDEditor
        value={value}
        onChange={onChange}
        height={height}
        previewOptions={{
          rehypePlugins: [[rehypeSanitize]],
        }}
        {...props}
      />
    </div>
  )
}
```

## Dark Mode Specifics

### Handle System Preference

```tsx
import { useTheme } from 'next-themes'
import { useEffect, useState } from 'react'

export function useEditorTheme() {
  const { theme, systemTheme } = useTheme()
  const [colorMode, setColorMode] = useState<'light' | 'dark'>('light')

  useEffect(() => {
    const effectiveTheme = theme === 'system' ? systemTheme : theme
    setColorMode(effectiveTheme === 'dark' ? 'dark' : 'light')
  }, [theme, systemTheme])

  return colorMode
}

// Usage
const colorMode = useEditorTheme()

<div data-color-mode={colorMode}>
  <MDEditor {...props} />
</div>
```

### Handle Theme Transitions

```css
/* Smooth theme transitions */
.w-md-editor,
.w-md-editor-toolbar,
.w-md-editor-content,
.w-md-editor-preview,
.wmde-markdown,
.wmde-markdown * {
  transition: background-color 0.2s ease, color 0.2s ease, border-color 0.2s ease;
}
```

## Custom Syntax Highlighting

Integrate with shadcn/ui color scheme:

```tsx
import { useTheme } from 'next-themes'
import MDEditor from '@uiw/react-md-editor'

export function MarkdownEditor({ value, onChange }) {
  const { theme } = useTheme()

  return (
    <div data-color-mode={theme === 'dark' ? 'dark' : 'light'}>
      <MDEditor
        value={value}
        onChange={onChange}
        previewOptions={{
          components: {
            code: ({ node, inline, className, children, ...props }) => {
              return inline ? (
                <code className="bg-muted text-primary px-1.5 py-0.5 rounded text-sm" {...props}>
                  {children}
                </code>
              ) : (
                <code className={className} {...props}>
                  {children}
                </code>
              )
            },
          },
        }}
      />
    </div>
  )
}
```

## Testing Theme Integration

```tsx
import { render, screen } from '@testing-library/react'
import { ThemeProvider } from 'next-themes'
import { MarkdownEditor } from './MarkdownEditor'

describe('MarkdownEditor Theme', () => {
  it('applies light theme', () => {
    render(
      <ThemeProvider defaultTheme="light">
        <MarkdownEditor value="Test" onChange={() => {}} />
      </ThemeProvider>
    )

    const wrapper = screen.getByRole('textbox').closest('[data-color-mode]')
    expect(wrapper).toHaveAttribute('data-color-mode', 'light')
  })

  it('applies dark theme', () => {
    render(
      <ThemeProvider defaultTheme="dark">
        <MarkdownEditor value="Test" onChange={() => {}} />
      </ThemeProvider>
    )

    const wrapper = screen.getByRole('textbox').closest('[data-color-mode]')
    expect(wrapper).toHaveAttribute('data-color-mode', 'dark')
  })
})
```

## Troubleshooting

**Issue:** Theme not applying immediately
**Solution:** Ensure editor is mounted after theme is resolved

**Issue:** Flash of wrong theme
**Solution:** Add loading state while theme resolves

**Issue:** CSS variables not working
**Solution:** Verify CSS is imported in correct order (globals.css before editor CSS)

**Issue:** Dark mode colors not matching shadcn/ui
**Solution:** Use HSL values from CSS variables, not hardcoded colors
