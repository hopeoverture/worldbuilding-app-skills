'use client'

import { useTheme } from 'next-themes'
import dynamic from 'next/dynamic'
import { ComponentProps } from 'react'
import rehypeSanitize from 'rehype-sanitize'
import '@uiw/react-md-editor/markdown-editor.css'
import '@uiw/react-markdown-preview/markdown.css'

const MDEditor = dynamic(
  () => import('@uiw/react-md-editor'),
  { ssr: false }
)

type MDEditorProps = ComponentProps<typeof MDEditor>

interface MarkdownEditorProps extends Omit<MDEditorProps, 'data-color-mode'> {
  value: string
  onChange?: (value?: string) => void
  height?: number | string
  hideToolbar?: boolean
  enablePreview?: boolean
  preview?: 'edit' | 'live' | 'preview'
}

/**
 * Markdown Editor component with theme integration and sanitization
 *
 * Features:
 * - Automatic theme switching (light/dark)
 * - XSS protection with rehype-sanitize
 * - Controlled component for forms
 * - Customizable toolbar and preview
 * - Next.js SSR compatible
 *
 * @example
 * ```tsx
 * const [content, setContent] = useState('')
 *
 * <MarkdownEditor
 *   value={content}
 *   onChange={setContent}
 *   height={400}
 * />
 * ```
 */
export function MarkdownEditor({
  value,
  onChange,
  height = 400,
  hideToolbar = false,
  enablePreview = true,
  preview = 'live',
  ...props
}: MarkdownEditorProps) {
  const { theme } = useTheme()

  return (
    <div
      data-color-mode={theme === 'dark' ? 'dark' : 'light'}
      className="markdown-editor-wrapper"
    >
      <MDEditor
        value={value}
        onChange={onChange}
        height={height}
        hideToolbar={hideToolbar}
        enablePreview={enablePreview}
        preview={preview}
        previewOptions={{
          rehypePlugins: [[rehypeSanitize]],
        }}
        {...props}
      />
    </div>
  )
}

// CSS for theme integration (add to globals.css)
const editorStyles = `
/* Markdown Editor Theme Integration */

.markdown-editor-wrapper {
  @apply rounded-md border border-input;
}

.w-md-editor {
  @apply bg-background text-foreground shadow-none;
  border: none !important;
}

.w-md-editor-toolbar {
  @apply border-b border-border bg-muted/30;
}

.w-md-editor-toolbar button,
.w-md-editor-toolbar li button {
  @apply text-foreground hover:bg-accent hover:text-accent-foreground;
}

.w-md-editor-toolbar li.active button {
  @apply bg-accent text-accent-foreground;
}

.w-md-editor-content {
  @apply text-foreground;
}

.w-md-editor-preview {
  @apply prose prose-sm dark:prose-invert max-w-none p-4;
}

.w-md-editor-text-pre,
.w-md-editor-text-input {
  @apply text-foreground;
}

.w-md-editor-text-pre > code,
.w-md-editor-text-input > code {
  @apply text-foreground;
}

/* Code blocks in preview */
.wmde-markdown {
  @apply bg-transparent text-foreground;
}

.wmde-markdown pre {
  @apply bg-muted;
}

.wmde-markdown code {
  @apply text-primary;
}

.wmde-markdown blockquote {
  @apply border-l-primary/50;
}

.wmde-markdown a {
  @apply text-primary hover:underline;
}

/* Tables in preview */
.wmde-markdown table {
  @apply border-border;
}

.wmde-markdown th,
.wmde-markdown td {
  @apply border-border;
}

.wmde-markdown th {
  @apply bg-muted;
}
`

// Export styles constant for documentation
export { editorStyles }
