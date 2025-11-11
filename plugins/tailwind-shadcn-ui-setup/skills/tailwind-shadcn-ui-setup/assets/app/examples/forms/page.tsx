'use client'

import * as React from 'react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'
import { toast } from 'sonner'

export default function FormsPage() {
  const [isSubmitting, setIsSubmitting] = React.useState(false)

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    setIsSubmitting(true)

    const formData = new FormData(event.currentTarget)
    const data = {
      name: formData.get('name'),
      email: formData.get('email'),
      message: formData.get('message'),
    }

    // Simulate API call
    await new Promise((resolve) => setTimeout(resolve, 1000))

    console.log('Form submitted:', data)
    toast.success('Form submitted successfully!')

    // Reset form
    event.currentTarget.reset()
    setIsSubmitting(false)
  }

  return (
    <div className="container max-w-4xl py-8">
      <div className="mb-8">
        <h1 className="text-4xl font-bold">Form Examples</h1>
        <p className="mt-2 text-lg text-muted-foreground">
          Accessible form components with HTML5 validation
        </p>
      </div>

      <div className="space-y-8">
        {/* Basic Form */}
        <Card>
          <CardHeader>
            <CardTitle>Contact Form</CardTitle>
            <CardDescription>
              Basic form with HTML5 validation and toast notifications
            </CardDescription>
          </CardHeader>
          <form onSubmit={handleSubmit}>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="name">
                  Name <span className="text-destructive">*</span>
                </Label>
                <Input
                  id="name"
                  name="name"
                  placeholder="John Doe"
                  required
                  aria-required="true"
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="email">
                  Email <span className="text-destructive">*</span>
                </Label>
                <Input
                  id="email"
                  name="email"
                  type="email"
                  placeholder="john@example.com"
                  required
                  aria-required="true"
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="message">
                  Message <span className="text-destructive">*</span>
                </Label>
                <textarea
                  id="message"
                  name="message"
                  className="flex min-h-[120px] w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                  placeholder="Your message here..."
                  required
                  aria-required="true"
                />
              </div>
            </CardContent>
            <CardFooter className="flex gap-2">
              <Button type="submit" disabled={isSubmitting}>
                {isSubmitting ? 'Submitting...' : 'Submit'}
              </Button>
              <Button type="reset" variant="outline" disabled={isSubmitting}>
                Reset
              </Button>
            </CardFooter>
          </form>
        </Card>

        {/* Form Validation Example */}
        <Card>
          <CardHeader>
            <CardTitle>Advanced Validation</CardTitle>
            <CardDescription>
              For production forms, consider using React Hook Form + Zod
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="rounded-lg bg-muted p-4">
              <code className="text-sm">
                <pre className="overflow-x-auto">
{`import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import * as z from 'zod'

const schema = z.object({
  email: z.string().email(),
  password: z.string().min(8)
})

export function LoginForm() {
  const form = useForm({
    resolver: zodResolver(schema)
  })

  // ... form implementation
}`}
                </pre>
              </code>
            </div>
            <div className="mt-4">
              <p className="text-sm text-muted-foreground">
                Install dependencies:{' '}
                <code className="rounded bg-muted px-1 py-0.5">
                  npm install react-hook-form @hookform/resolvers zod
                </code>
              </p>
            </div>
          </CardContent>
        </Card>

        {/* Accessibility Notes */}
        <Card>
          <CardHeader>
            <CardTitle>Accessibility Guidelines</CardTitle>
            <CardDescription>Best practices for accessible forms</CardDescription>
          </CardHeader>
          <CardContent>
            <ul className="ml-6 list-disc space-y-2 text-sm">
              <li>
                <strong>Always pair labels with inputs</strong> using{' '}
                <code className="rounded bg-muted px-1">htmlFor</code> and{' '}
                <code className="rounded bg-muted px-1">id</code>
              </li>
              <li>
                <strong>Mark required fields</strong> visually and with{' '}
                <code className="rounded bg-muted px-1">aria-required</code>
              </li>
              <li>
                <strong>Provide clear error messages</strong> linked with{' '}
                <code className="rounded bg-muted px-1">aria-describedby</code>
              </li>
              <li>
                <strong>Use appropriate input types</strong> (email, tel, url,
                etc.)
              </li>
              <li>
                <strong>Disable submit during processing</strong> with{' '}
                <code className="rounded bg-muted px-1">aria-busy</code>
              </li>
              <li>
                <strong>Don't use placeholder as label</strong> - placeholders
                disappear on focus
              </li>
            </ul>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
