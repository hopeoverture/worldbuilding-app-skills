'use client'

import * as React from 'react'
import { Button } from '@/components/ui/button'
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'
import { Separator } from '@/components/ui/separator'
import { useTheme } from 'next-themes'

export default function ThemePage() {
  const { theme, setTheme } = useTheme()
  const [mounted, setMounted] = React.useState(false)

  // Prevent hydration mismatch
  React.useEffect(() => {
    setMounted(true)
  }, [])

  if (!mounted) {
    return null
  }

  return (
    <div className="container max-w-6xl py-8">
      <div className="mb-8">
        <h1 className="text-4xl font-bold">Theme & Design Tokens</h1>
        <p className="mt-2 text-lg text-muted-foreground">
          Explore the color system and design tokens
        </p>
      </div>

      {/* Theme Switcher */}
      <Card className="mb-8">
        <CardHeader>
          <CardTitle>Theme Switcher</CardTitle>
          <CardDescription>
            Current theme: <strong className="capitalize">{theme}</strong>
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="flex gap-2">
            <Button
              variant={theme === 'light' ? 'default' : 'outline'}
              onClick={() => setTheme('light')}
            >
              Light
            </Button>
            <Button
              variant={theme === 'dark' ? 'default' : 'outline'}
              onClick={() => setTheme('dark')}
            >
              Dark
            </Button>
            <Button
              variant={theme === 'system' ? 'default' : 'outline'}
              onClick={() => setTheme('system')}
            >
              System
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Color Tokens */}
      <div className="space-y-8">
        <Card>
          <CardHeader>
            <CardTitle>Semantic Colors</CardTitle>
            <CardDescription>
              Colors that describe purpose, not appearance
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid gap-4 sm:grid-cols-2">
              <ColorSwatch
                label="Background"
                description="Main background color"
                className="bg-background text-foreground"
              />
              <ColorSwatch
                label="Foreground"
                description="Main text color"
                className="bg-foreground text-background"
              />
              <ColorSwatch
                label="Primary"
                description="Brand color for main actions"
                className="bg-primary text-primary-foreground"
              />
              <ColorSwatch
                label="Secondary"
                description="Less prominent actions"
                className="bg-secondary text-secondary-foreground"
              />
              <ColorSwatch
                label="Muted"
                description="Disabled states, subtle backgrounds"
                className="bg-muted text-muted-foreground"
              />
              <ColorSwatch
                label="Accent"
                description="Highlights, hover states"
                className="bg-accent text-accent-foreground"
              />
              <ColorSwatch
                label="Destructive"
                description="Errors, delete actions"
                className="bg-destructive text-destructive-foreground"
              />
              <ColorSwatch
                label="Card"
                description="Elevated surfaces"
                className="border bg-card text-card-foreground"
              />
            </div>
          </CardContent>
        </Card>

        {/* Component Variants */}
        <Card>
          <CardHeader>
            <CardTitle>Button Variants</CardTitle>
            <CardDescription>
              Different button styles using semantic colors
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="flex flex-wrap gap-2">
              <Button>Default</Button>
              <Button variant="secondary">Secondary</Button>
              <Button variant="destructive">Destructive</Button>
              <Button variant="outline">Outline</Button>
              <Button variant="ghost">Ghost</Button>
              <Button variant="link">Link</Button>
            </div>
            <Separator className="my-4" />
            <div className="flex flex-wrap gap-2">
              <Button size="sm">Small</Button>
              <Button size="default">Default</Button>
              <Button size="lg">Large</Button>
              <Button size="icon">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  width="16"
                  height="16"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                >
                  <path d="M5 12h14" />
                  <path d="m12 5 7 7-7 7" />
                </svg>
              </Button>
            </div>
          </CardContent>
        </Card>

        {/* Typography */}
        <Card>
          <CardHeader>
            <CardTitle>Typography Scale</CardTitle>
            <CardDescription>Text styles with proper hierarchy</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div>
                <h1 className="text-4xl font-bold">Heading 1 (4xl)</h1>
                <p className="text-sm text-muted-foreground">
                  text-4xl font-bold
                </p>
              </div>
              <div>
                <h2 className="text-3xl font-bold">Heading 2 (3xl)</h2>
                <p className="text-sm text-muted-foreground">
                  text-3xl font-bold
                </p>
              </div>
              <div>
                <h3 className="text-2xl font-semibold">Heading 3 (2xl)</h3>
                <p className="text-sm text-muted-foreground">
                  text-2xl font-semibold
                </p>
              </div>
              <div>
                <h4 className="text-xl font-semibold">Heading 4 (xl)</h4>
                <p className="text-sm text-muted-foreground">
                  text-xl font-semibold
                </p>
              </div>
              <div>
                <p className="text-base">Body text (base)</p>
                <p className="text-sm text-muted-foreground">text-base</p>
              </div>
              <div>
                <p className="text-sm">Small text (sm)</p>
                <p className="text-sm text-muted-foreground">text-sm</p>
              </div>
              <div>
                <p className="text-xs text-muted-foreground">
                  Extra small (xs)
                </p>
                <p className="text-sm text-muted-foreground">text-xs</p>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Customization Guide */}
        <Card>
          <CardHeader>
            <CardTitle>Customization</CardTitle>
            <CardDescription>How to customize your theme</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div>
                <h4 className="mb-2 font-medium">1. Update CSS Variables</h4>
                <p className="mb-2 text-sm text-muted-foreground">
                  Edit <code className="rounded bg-muted px-1">app/globals.css</code>:
                </p>
                <pre className="overflow-x-auto rounded-lg bg-muted p-4 text-sm">
                  <code>{`:root {
  --primary: 270 80% 45%;  /* Change to your brand color */
  --radius: 0.75rem;        /* Adjust border radius */
}`}</code>
                </pre>
              </div>

              <div>
                <h4 className="mb-2 font-medium">2. Use HSL Color Picker</h4>
                <p className="text-sm text-muted-foreground">
                  Find HSL values using:{' '}
                  <a
                    href="https://hslpicker.com"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-primary underline"
                  >
                    HSL Color Picker
                  </a>
                </p>
              </div>

              <div>
                <h4 className="mb-2 font-medium">3. Test Contrast</h4>
                <p className="text-sm text-muted-foreground">
                  Ensure WCAG compliance using:{' '}
                  <a
                    href="https://webaim.org/resources/contrastchecker/"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-primary underline"
                  >
                    WebAIM Contrast Checker
                  </a>
                </p>
              </div>

              <div>
                <h4 className="mb-2 font-medium">4. Test Both Themes</h4>
                <p className="text-sm text-muted-foreground">
                  Always verify colors look good in both light and dark mode
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}

function ColorSwatch({
  label,
  description,
  className,
}: {
  label: string
  description: string
  className: string
}) {
  return (
    <div className="space-y-2">
      <div
        className={`flex h-20 items-center justify-center rounded-lg border ${className}`}
      >
        <span className="font-medium">{label}</span>
      </div>
      <div>
        <p className="text-sm font-medium">{label}</p>
        <p className="text-xs text-muted-foreground">{description}</p>
      </div>
    </div>
  )
}
