# Markdown Sanitization Security Guide

## Why Sanitization is Critical

Markdown editors can be exploited for XSS attacks through:
- Malicious JavaScript in HTML tags
- Script injection via event handlers
- Data exfiltration through image sources
- Link-based phishing attacks
- Iframe injection

## Client-Side Sanitization

### Using rehype-sanitize

```bash
npm install rehype-sanitize
```

```tsx
import MDEditor from '@uiw/react-md-editor'
import rehypeSanitize from 'rehype-sanitize'

<MDEditor
  value={value}
  onChange={onChange}
  previewOptions={{
    rehypePlugins: [[rehypeSanitize]],
  }}
/>
```

### Custom Sanitization Schema

```tsx
import rehypeSanitize, { defaultSchema } from 'rehype-sanitize'
import { deepmerge } from 'deepmerge-ts'

const customSchema = deepmerge(defaultSchema, {
  attributes: {
    '*': ['className'], // Allow className on all elements
    a: ['href', 'title', 'target', 'rel'],
    img: ['src', 'alt', 'title', 'width', 'height'],
    code: ['className'], // For syntax highlighting
  },
  tagNames: [
    // Standard markdown
    'p', 'br', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
    'strong', 'em', 'u', 's', 'del', 'ins',
    'ul', 'ol', 'li',
    'blockquote', 'code', 'pre',
    'a', 'img',
    'table', 'thead', 'tbody', 'tr', 'th', 'td',
    'hr', 'div', 'span',
    // Additional if needed
    'kbd', 'mark', 'abbr',
  ],
  protocols: {
    href: ['http', 'https', 'mailto'],
    src: ['http', 'https'],
  },
})

<MDEditor
  previewOptions={{
    rehypePlugins: [[rehypeSanitize, customSchema]],
  }}
/>
```

### Strict Sanitization (No HTML)

```tsx
import rehypeSanitize from 'rehype-sanitize'

const strictSchema = {
  tagNames: [
    'p', 'br', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
    'strong', 'em', 'code', 'pre',
    'ul', 'ol', 'li',
    'blockquote',
    'a',
    'hr',
  ],
  attributes: {
    a: ['href'],
    code: ['className'],
  },
  protocols: {
    href: ['https'], // Only HTTPS links
  },
}

<MDEditor
  previewOptions={{
    rehypePlugins: [[rehypeSanitize, strictSchema]],
  }}
/>
```

## Server-Side Sanitization

### Using DOMPurify

```bash
npm install isomorphic-dompurify
```

```typescript
// lib/sanitize-markdown.ts
import DOMPurify from 'isomorphic-dompurify'

export function sanitizeMarkdown(markdown: string): string {
  return DOMPurify.sanitize(markdown, {
    ALLOWED_TAGS: [
      'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
      'p', 'br', 'strong', 'em', 'u', 's',
      'ul', 'ol', 'li',
      'blockquote', 'code', 'pre',
      'a', 'img',
      'table', 'thead', 'tbody', 'tr', 'th', 'td',
      'hr', 'div', 'span',
    ],
    ALLOWED_ATTR: [
      'href', 'src', 'alt', 'title',
      'class', 'id',
      'width', 'height',
    ],
    ALLOWED_URI_REGEXP: /^(?:https?:|mailto:)/i,
    KEEP_CONTENT: true,
    RETURN_DOM: false,
    RETURN_DOM_FRAGMENT: false,
    RETURN_DOM_IMPORT: false,
  })
}
```

### Server Action with Sanitization

```typescript
'use server'

import { sanitizeMarkdown } from '@/lib/sanitize-markdown'
import { db } from '@/lib/db'
import { auth } from '@/lib/auth'

export async function saveCharacterBio(
  characterId: string,
  biography: string
) {
  const session = await auth()

  if (!session?.user) {
    return { success: false, message: 'Unauthorized' }
  }

  // Sanitize before saving
  const sanitizedBio = sanitizeMarkdown(biography)

  try {
    await db.character.update({
      where: { id: characterId },
      data: { biography: sanitizedBio },
    })

    return { success: true }
  } catch (error) {
    console.error('Failed to save biography:', error)
    return { success: false, message: 'Failed to save' }
  }
}
```

### API Route with Sanitization

```typescript
// app/api/entities/[id]/description/route.ts
import { NextRequest, NextResponse } from 'next/server'
import { sanitizeMarkdown } from '@/lib/sanitize-markdown'
import { db } from '@/lib/db'
import { getServerSession } from 'next-auth'

export async function PATCH(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  const session = await getServerSession()

  if (!session?.user) {
    return NextResponse.json(
      { error: 'Unauthorized' },
      { status: 401 }
    )
  }

  const { description } = await request.json()

  // Validate input
  if (!description || typeof description !== 'string') {
    return NextResponse.json(
      { error: 'Invalid description' },
      { status: 400 }
    )
  }

  // Sanitize
  const sanitized = sanitizeMarkdown(description)

  // Save to database
  await db.entity.update({
    where: { id: params.id },
    data: { description: sanitized },
  })

  return NextResponse.json({ success: true })
}
```

## Advanced Sanitization Patterns

### Markdown-to-HTML with Sanitization

```typescript
import { remark } from 'remark'
import remarkHtml from 'remark-html'
import DOMPurify from 'isomorphic-dompurify'

export async function markdownToSafeHtml(markdown: string): Promise<string> {
  // Convert markdown to HTML
  const result = await remark()
    .use(remarkHtml, { sanitize: false }) // Don't double-sanitize
    .process(markdown)

  const html = result.toString()

  // Sanitize HTML
  const sanitized = DOMPurify.sanitize(html, {
    ALLOWED_TAGS: [
      'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
      'p', 'br', 'strong', 'em', 'code', 'pre',
      'ul', 'ol', 'li',
      'blockquote', 'a', 'img',
      'table', 'thead', 'tbody', 'tr', 'th', 'td',
      'hr',
    ],
    ALLOWED_ATTR: ['href', 'src', 'alt', 'title'],
  })

  return sanitized
}

// Usage in server action
export async function saveDescription(id: string, markdown: string) {
  const html = await markdownToSafeHtml(markdown)

  await db.entity.update({
    where: { id },
    data: {
      descriptionMarkdown: markdown, // Store original
      descriptionHtml: html,         // Store sanitized HTML
    },
  })

  return { success: true }
}
```

### Link Validation

```typescript
import DOMPurify from 'isomorphic-dompurify'

export function sanitizeWithLinkValidation(markdown: string): string {
  return DOMPurify.sanitize(markdown, {
    ALLOWED_TAGS: ['a', 'p', 'h1', 'h2', 'h3', 'strong', 'em', 'code'],
    ALLOWED_ATTR: ['href'],
    ALLOWED_URI_REGEXP: /^https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)$/,
    // Block certain domains
    FORBID_ATTR: [],
    HOOKS: {
      afterSanitizeAttributes: (node) => {
        if (node.tagName === 'A') {
          const href = node.getAttribute('href')
          if (href) {
            // Block suspicious links
            const suspiciousDomains = ['malicious.com', 'phishing.com']
            const url = new URL(href)
            if (suspiciousDomains.some(domain => url.hostname.includes(domain))) {
              node.removeAttribute('href')
            }
            // Force external links to open in new tab
            node.setAttribute('target', '_blank')
            node.setAttribute('rel', 'noopener noreferrer')
          }
        }
      },
    },
  })
}
```

### Image Source Validation

```typescript
import DOMPurify from 'isomorphic-dompurify'

export function sanitizeWithImageValidation(markdown: string): string {
  return DOMPurify.sanitize(markdown, {
    ALLOWED_TAGS: ['img', 'p', 'h1', 'h2', 'strong', 'em'],
    ALLOWED_ATTR: ['src', 'alt', 'title', 'width', 'height'],
    HOOKS: {
      afterSanitizeAttributes: (node) => {
        if (node.tagName === 'IMG') {
          const src = node.getAttribute('src')
          if (src) {
            try {
              const url = new URL(src)
              // Only allow images from trusted domains
              const trustedDomains = [
                'images.example.com',
                'cdn.example.com',
                'storage.googleapis.com',
              ]
              if (!trustedDomains.some(domain => url.hostname === domain)) {
                node.removeAttribute('src')
                node.setAttribute('alt', 'Image blocked: untrusted source')
              }
            } catch (error) {
              // Invalid URL, remove src
              node.removeAttribute('src')
            }
          }
        }
      },
    },
  })
}
```

## Security Best Practices

### 1. Always Sanitize on Server

Never trust client-side sanitization alone:

```typescript
// [ERROR] BAD: Only client-side sanitization
function onSubmit(data: FormValues) {
  await saveDescription(data.description) // Raw user input
}

// [OK] GOOD: Server-side sanitization
'use server'
export async function saveDescription(description: string) {
  const sanitized = sanitizeMarkdown(description)
  await db.save(sanitized)
}
```

### 2. Validate Input Length

```typescript
const MAX_MARKDOWN_LENGTH = 50000 // 50KB

export async function saveDescription(description: string) {
  if (description.length > MAX_MARKDOWN_LENGTH) {
    throw new Error('Description too long')
  }

  const sanitized = sanitizeMarkdown(description)
  await db.save(sanitized)
}
```

### 3. Store Both Raw and Sanitized

```typescript
export async function saveDescription(
  entityId: string,
  description: string
) {
  const sanitized = sanitizeMarkdown(description)

  await db.entity.update({
    where: { id: entityId },
    data: {
      descriptionRaw: description,     // Original for editing
      description: sanitized,           // Sanitized for display
      descriptionUpdatedAt: new Date(),
    },
  })
}
```

### 4. Implement Rate Limiting

```typescript
import { Ratelimit } from '@upstash/ratelimit'
import { Redis } from '@upstash/redis'

const ratelimit = new Ratelimit({
  redis: Redis.fromEnv(),
  limiter: Ratelimit.slidingWindow(10, '1 m'), // 10 requests per minute
})

export async function saveDescription(
  userId: string,
  description: string
) {
  const { success } = await ratelimit.limit(userId)

  if (!success) {
    throw new Error('Rate limit exceeded')
  }

  const sanitized = sanitizeMarkdown(description)
  await db.save(sanitized)
}
```

### 5. Log Suspicious Content

```typescript
export function sanitizeAndLog(
  markdown: string,
  userId: string
): string {
  const original = markdown
  const sanitized = DOMPurify.sanitize(markdown)

  // If content was modified, it contained potentially malicious code
  if (original !== sanitized) {
    console.warn('Suspicious content detected:', {
      userId,
      timestamp: new Date(),
      removed: original.length - sanitized.length,
    })

    // Optionally store for security review
    logSecurityEvent({
      type: 'SUSPICIOUS_CONTENT',
      userId,
      original: original.substring(0, 1000), // First 1KB
      sanitized: sanitized.substring(0, 1000),
    })
  }

  return sanitized
}
```

## Testing Sanitization

### Unit Tests

```typescript
import { describe, it, expect } from 'vitest'
import { sanitizeMarkdown } from './sanitize-markdown'

describe('sanitizeMarkdown', () => {
  it('removes script tags', () => {
    const input = '<script>alert("XSS")</script>Hello'
    const output = sanitizeMarkdown(input)
    expect(output).not.toContain('<script>')
    expect(output).toContain('Hello')
  })

  it('removes event handlers', () => {
    const input = '<img src="x" onerror="alert(1)">'
    const output = sanitizeMarkdown(input)
    expect(output).not.toContain('onerror')
  })

  it('allows safe HTML', () => {
    const input = '<p><strong>Bold</strong> and <em>italic</em></p>'
    const output = sanitizeMarkdown(input)
    expect(output).toContain('<strong>')
    expect(output).toContain('<em>')
  })

  it('sanitizes links', () => {
    const input = '<a href="javascript:alert(1)">Click</a>'
    const output = sanitizeMarkdown(input)
    expect(output).not.toContain('javascript:')
  })

  it('handles nested tags', () => {
    const input = '<div><script>alert(1)</script><p>Safe</p></div>'
    const output = sanitizeMarkdown(input)
    expect(output).not.toContain('<script>')
    expect(output).toContain('Safe')
  })
})
```

### Integration Tests

```typescript
import { test, expect } from '@playwright/test'

test.describe('Markdown Editor Security', () => {
  test('prevents XSS through markdown', async ({ page }) => {
    await page.goto('/editor')

    const xssPayload = '<script>window.xssExecuted = true</script>Hello'

    await page.fill('[role="textbox"]', xssPayload)
    await page.click('button:has-text("Save")')

    await page.waitForTimeout(1000)

    // Check that script did not execute
    const xssExecuted = await page.evaluate(() => {
      return (window as any).xssExecuted
    })
    expect(xssExecuted).toBeUndefined()

    // Check that content was sanitized
    const preview = await page.locator('.preview').textContent()
    expect(preview).toContain('Hello')
    expect(preview).not.toContain('<script>')
  })
})
```

## Common Attack Vectors

### Script Injection
```html
<!-- Attack -->
<script>alert('XSS')</script>
<img src=x onerror="alert('XSS')">
<svg onload="alert('XSS')">

<!-- Sanitized -->
<!-- Scripts and event handlers removed -->
```

### Link-based Attacks
```html
<!-- Attack -->
<a href="javascript:alert('XSS')">Click</a>
<a href="data:text/html,<script>alert('XSS')</script>">Click</a>

<!-- Sanitized -->
<a>Click</a> <!-- href removed -->
```

### Iframe Injection
```html
<!-- Attack -->
<iframe src="https://malicious.com"></iframe>

<!-- Sanitized -->
<!-- iframe tag removed completely -->
```

## Sanitization Checklist

- [ ] Client-side sanitization with rehype-sanitize configured
- [ ] Server-side sanitization with DOMPurify
- [ ] Whitelist approach (allowed tags/attributes)
- [ ] Protocol restrictions (https only)
- [ ] Input length validation
- [ ] Rate limiting on save endpoints
- [ ] Logging of sanitized content
- [ ] Both raw and sanitized versions stored
- [ ] External links open in new tab with rel="noopener noreferrer"
- [ ] Image sources validated against trusted domains
- [ ] Unit tests for XSS prevention
- [ ] Integration tests with malicious payloads
- [ ] Security headers configured (CSP)
- [ ] Regular dependency updates for security patches
