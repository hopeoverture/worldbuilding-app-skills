'use client'

import { useTheme } from 'next-themes'
import dynamic from 'next/dynamic'
import { ComponentProps } from 'react'
import rehypeSanitize from 'rehype-sanitize'
import '@uiw/react-markdown-preview/markdown.css'

const MDPreview = dynamic(
  () => import('@uiw/react-markdown-preview'),
  { ssr: false }
)

type MDPreviewProps = ComponentProps<typeof MDPreview>

interface MarkdownPreviewProps extends Omit<MDPreviewProps, 'source' | 'data-color-mode'> {
  content: string
  className?: string
}

/**
 * Markdown Preview component for displaying formatted markdown
 *
 * Features:
 * - Automatic theme switching
 * - XSS protection with rehype-sanitize
 * - GitHub-flavored markdown support
 * - Syntax highlighting for code blocks
 * - Next.js SSR compatible
 *
 * @example
 * ```tsx
 * <MarkdownPreview
 *   content={character.biography}
 *   className="max-w-3xl"
 * />
 * ```
 */
export function MarkdownPreview({
  content,
  className = '',
  ...props
}: MarkdownPreviewProps) {
  const { theme } = useTheme()

  return (
    <div
      data-color-mode={theme === 'dark' ? 'dark' : 'light'}
      className={`markdown-preview-wrapper ${className}`}
    >
      <MDPreview
        source={content}
        rehypePlugins={[[rehypeSanitize]]}
        {...props}
      />
    </div>
  )
}

// CSS for preview theme integration (add to globals.css)
const previewStyles = `
/* Markdown Preview Theme Integration */

.markdown-preview-wrapper {
  @apply rounded-md;
}

.markdown-preview-wrapper .wmde-markdown {
  @apply bg-transparent text-foreground;
  font-family: inherit;
}

/* Typography */
.markdown-preview-wrapper .wmde-markdown h1,
.markdown-preview-wrapper .wmde-markdown h2,
.markdown-preview-wrapper .wmde-markdown h3,
.markdown-preview-wrapper .wmde-markdown h4,
.markdown-preview-wrapper .wmde-markdown h5,
.markdown-preview-wrapper .wmde-markdown h6 {
  @apply text-foreground font-semibold;
  border-bottom: none;
}

.markdown-preview-wrapper .wmde-markdown p {
  @apply text-foreground leading-7;
}

/* Links */
.markdown-preview-wrapper .wmde-markdown a {
  @apply text-primary hover:underline;
}

/* Lists */
.markdown-preview-wrapper .wmde-markdown ul,
.markdown-preview-wrapper .wmde-markdown ol {
  @apply text-foreground;
}

/* Blockquotes */
.markdown-preview-wrapper .wmde-markdown blockquote {
  @apply border-l-4 border-primary/50 bg-muted/50 text-muted-foreground italic;
}

/* Code */
.markdown-preview-wrapper .wmde-markdown code {
  @apply bg-muted text-primary px-1.5 py-0.5 rounded text-sm;
}

.markdown-preview-wrapper .wmde-markdown pre {
  @apply bg-muted rounded-md p-4 overflow-x-auto;
}

.markdown-preview-wrapper .wmde-markdown pre code {
  @apply bg-transparent p-0;
}

/* Tables */
.markdown-preview-wrapper .wmde-markdown table {
  @apply border-collapse w-full border border-border;
}

.markdown-preview-wrapper .wmde-markdown th {
  @apply bg-muted font-semibold text-left p-2 border border-border;
}

.markdown-preview-wrapper .wmde-markdown td {
  @apply p-2 border border-border;
}

.markdown-preview-wrapper .wmde-markdown tr:nth-child(even) {
  @apply bg-muted/30;
}

/* Horizontal Rule */
.markdown-preview-wrapper .wmde-markdown hr {
  @apply border-border my-4;
}

/* Images */
.markdown-preview-wrapper .wmde-markdown img {
  @apply rounded-md max-w-full h-auto;
}

/* Task Lists */
.markdown-preview-wrapper .wmde-markdown input[type="checkbox"] {
  @apply mr-2;
}
`

// Export styles constant for documentation
export { previewStyles }
