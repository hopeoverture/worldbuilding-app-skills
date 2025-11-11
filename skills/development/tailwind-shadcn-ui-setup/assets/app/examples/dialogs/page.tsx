'use client'

import * as React from 'react'
import { Button } from '@/components/ui/button'
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '@/components/ui/dialog'
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { toast } from 'sonner'

export default function DialogsPage() {
  const [isOpen, setIsOpen] = React.useState(false)

  const handleSave = () => {
    toast.success('Changes saved successfully!')
    setIsOpen(false)
  }

  return (
    <div className="container max-w-4xl py-8">
      <div className="mb-8">
        <h1 className="text-4xl font-bold">Dialog Examples</h1>
        <p className="mt-2 text-lg text-muted-foreground">
          Modal dialogs with focus trapping and keyboard navigation
        </p>
      </div>

      <div className="grid gap-6 md:grid-cols-2">
        {/* Basic Dialog */}
        <Card>
          <CardHeader>
            <CardTitle>Basic Dialog</CardTitle>
            <CardDescription>Simple dialog with title and content</CardDescription>
          </CardHeader>
          <CardContent>
            <Dialog>
              <DialogTrigger asChild>
                <Button>Open Dialog</Button>
              </DialogTrigger>
              <DialogContent>
                <DialogHeader>
                  <DialogTitle>Welcome!</DialogTitle>
                  <DialogDescription>
                    This is a basic dialog example. Press ESC or click outside to
                    close.
                  </DialogDescription>
                </DialogHeader>
                <div className="py-4">
                  <p className="text-sm text-muted-foreground">
                    Dialogs automatically handle:
                  </p>
                  <ul className="ml-6 mt-2 list-disc text-sm text-muted-foreground">
                    <li>Focus trapping</li>
                    <li>Keyboard navigation (ESC to close)</li>
                    <li>Backdrop click to dismiss</li>
                    <li>Return focus on close</li>
                  </ul>
                </div>
                <DialogFooter>
                  <Button onClick={() => toast.success('Action completed!')}>
                    Confirm
                  </Button>
                </DialogFooter>
              </DialogContent>
            </Dialog>
          </CardContent>
        </Card>

        {/* Dialog with Form */}
        <Card>
          <CardHeader>
            <CardTitle>Dialog with Form</CardTitle>
            <CardDescription>Dialog containing a form with inputs</CardDescription>
          </CardHeader>
          <CardContent>
            <Dialog open={isOpen} onOpenChange={setIsOpen}>
              <DialogTrigger asChild>
                <Button>Edit Profile</Button>
              </DialogTrigger>
              <DialogContent>
                <DialogHeader>
                  <DialogTitle>Edit Profile</DialogTitle>
                  <DialogDescription>
                    Make changes to your profile here. Click save when you're
                    done.
                  </DialogDescription>
                </DialogHeader>
                <div className="grid gap-4 py-4">
                  <div className="grid gap-2">
                    <Label htmlFor="name">Name</Label>
                    <Input id="name" defaultValue="John Doe" />
                  </div>
                  <div className="grid gap-2">
                    <Label htmlFor="email">Email</Label>
                    <Input
                      id="email"
                      type="email"
                      defaultValue="john@example.com"
                    />
                  </div>
                </div>
                <DialogFooter>
                  <Button variant="outline" onClick={() => setIsOpen(false)}>
                    Cancel
                  </Button>
                  <Button onClick={handleSave}>Save Changes</Button>
                </DialogFooter>
              </DialogContent>
            </Dialog>
          </CardContent>
        </Card>

        {/* Confirmation Dialog */}
        <Card>
          <CardHeader>
            <CardTitle>Confirmation Dialog</CardTitle>
            <CardDescription>Destructive action confirmation</CardDescription>
          </CardHeader>
          <CardContent>
            <Dialog>
              <DialogTrigger asChild>
                <Button variant="destructive">Delete Item</Button>
              </DialogTrigger>
              <DialogContent>
                <DialogHeader>
                  <DialogTitle>Are you absolutely sure?</DialogTitle>
                  <DialogDescription>
                    This action cannot be undone. This will permanently delete
                    your item and remove your data from our servers.
                  </DialogDescription>
                </DialogHeader>
                <DialogFooter>
                  <Button variant="outline">Cancel</Button>
                  <Button
                    variant="destructive"
                    onClick={() => {
                      toast.error('Item deleted')
                    }}
                  >
                    Delete
                  </Button>
                </DialogFooter>
              </DialogContent>
            </Dialog>
          </CardContent>
        </Card>

        {/* Info Dialog */}
        <Card>
          <CardHeader>
            <CardTitle>Information Dialog</CardTitle>
            <CardDescription>Display information without actions</CardDescription>
          </CardHeader>
          <CardContent>
            <Dialog>
              <DialogTrigger asChild>
                <Button variant="outline">Show Info</Button>
              </DialogTrigger>
              <DialogContent>
                <DialogHeader>
                  <DialogTitle>About This App</DialogTitle>
                  <DialogDescription>
                    Built with modern web technologies
                  </DialogDescription>
                </DialogHeader>
                <div className="space-y-4 py-4">
                  <div>
                    <h4 className="mb-2 text-sm font-medium">Stack</h4>
                    <ul className="space-y-1 text-sm text-muted-foreground">
                      <li>• Next.js 16 with App Router</li>
                      <li>• React 19</li>
                      <li>• Tailwind CSS v3/v4</li>
                      <li>• shadcn/ui components</li>
                      <li>• TypeScript</li>
                    </ul>
                  </div>
                  <div>
                    <h4 className="mb-2 text-sm font-medium">Features</h4>
                    <ul className="space-y-1 text-sm text-muted-foreground">
                      <li>• Dark mode support</li>
                      <li>• Fully accessible (WCAG 2.1 AA)</li>
                      <li>• Type-safe</li>
                      <li>• Production-ready</li>
                    </ul>
                  </div>
                </div>
              </DialogContent>
            </Dialog>
          </CardContent>
        </Card>
      </div>

      {/* Accessibility Info */}
      <Card className="mt-6">
        <CardHeader>
          <CardTitle>Dialog Accessibility</CardTitle>
          <CardDescription>
            shadcn/ui dialogs are built on Radix UI with full accessibility
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4 text-sm">
            <div>
              <h4 className="mb-2 font-medium">Keyboard Navigation</h4>
              <ul className="ml-6 list-disc space-y-1 text-muted-foreground">
                <li>
                  <kbd className="rounded bg-muted px-1.5 py-0.5">ESC</kbd> -
                  Close dialog
                </li>
                <li>
                  <kbd className="rounded bg-muted px-1.5 py-0.5">Tab</kbd> -
                  Move focus forward
                </li>
                <li>
                  <kbd className="rounded bg-muted px-1.5 py-0.5">
                    Shift + Tab
                  </kbd>{' '}
                  - Move focus backward
                </li>
              </ul>
            </div>

            <div>
              <h4 className="mb-2 font-medium">Screen Reader Support</h4>
              <ul className="ml-6 list-disc space-y-1 text-muted-foreground">
                <li>
                  Dialog title is announced via{' '}
                  <code className="rounded bg-muted px-1">aria-labelledby</code>
                </li>
                <li>
                  Description is read via{' '}
                  <code className="rounded bg-muted px-1">aria-describedby</code>
                </li>
                <li>Focus is trapped within dialog when open</li>
                <li>Focus returns to trigger element on close</li>
              </ul>
            </div>

            <div>
              <h4 className="mb-2 font-medium">Mouse/Touch Support</h4>
              <ul className="ml-6 list-disc space-y-1 text-muted-foreground">
                <li>Click backdrop to dismiss (optional)</li>
                <li>Close button in top-right corner</li>
                <li>Scroll content if overflowing</li>
              </ul>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
