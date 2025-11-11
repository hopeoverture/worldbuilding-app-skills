# shadcn/ui Component Reference

## Overview

shadcn/ui provides a collection of re-usable components built with Radix UI and Tailwind CSS. Components are NOT installed as dependencies but copied into your project, giving you full control.

## Installation Command

```bash
npx shadcn-ui@latest add [component-name]
```

## Baseline Components for This Skill

The following components are installed by default:

### Core UI Elements
- **button**: Primary interactive element with variants
- **card**: Container for grouped content
- **input**: Text input field
- **label**: Form label with accessibility support
- **dialog**: Modal dialog/overlay
- **separator**: Visual or semantic separator

### Layout & Navigation
- **sheet**: Slide-over panel (mobile sidebar)
- **dropdown-menu**: Contextual menu with submenus
- **navigation-menu**: Main navigation component

### Feedback & Notifications
- **toast**: Temporary notifications (via Sonner)
- **alert**: Static notification messages
- **badge**: Status or category indicator

## Available Components by Category

### Form Components
- `checkbox` - Checkbox input with label
- `input` - Text input field
- `label` - Form label
- `textarea` - Multi-line text input
- `select` - Dropdown select
- `radio-group` - Radio button group
- `switch` - Toggle switch
- `slider` - Range slider
- `form` - Form wrapper with React Hook Form integration
- `combobox` - Searchable select (autocomplete)
- `date-picker` - Date selection with calendar
- `calendar` - Calendar component

### Layout Components
- `card` - Content card with header/footer
- `sheet` - Slide-over panel
- `dialog` - Modal dialog
- `popover` - Floating popover
- `drawer` - Bottom drawer (mobile)
- `separator` - Divider line
- `scroll-area` - Custom scrollable area
- `aspect-ratio` - Maintain aspect ratio
- `resizable` - Resizable panels

### Navigation Components
- `navigation-menu` - Main navigation
- `menubar` - Desktop menu bar
- `dropdown-menu` - Context/dropdown menu
- `context-menu` - Right-click context menu
- `tabs` - Tab navigation
- `breadcrumb` - Breadcrumb navigation
- `pagination` - Page navigation
- `command` - Command palette (⌘K)

### Feedback Components
- `toast` - Toast notifications
- `alert` - Alert messages
- `alert-dialog` - Confirmation dialog
- `badge` - Status badge
- `progress` - Progress indicator
- `skeleton` - Loading skeleton
- `spinner` - Loading spinner

### Data Display
- `table` - Data table
- `avatar` - User avatar
- `tooltip` - Hover tooltip
- `accordion` - Collapsible sections
- `collapsible` - Simple collapsible
- `hover-card` - Rich hover card
- `data-table` - Advanced data table with sorting/filtering

### Utility Components
- `toggle` - Toggle button
- `toggle-group` - Toggle button group
- `sonner` - Toast notification library integration
- `carousel` - Image/content carousel

## Usage Patterns

### Adding a Single Component

```bash
npx shadcn-ui add button
```

This creates:
- `components/ui/button.tsx`
- Updates `components.json` if needed

### Adding Multiple Components

```bash
npx shadcn-ui add button card input label
```

### Using a Component

```tsx
import { Button } from "@/components/ui/button"
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card"

export default function Example() {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Example Card</CardTitle>
      </CardHeader>
      <CardContent>
        <Button>Click me</Button>
      </CardContent>
    </Card>
  )
}
```

## Component Composition Patterns

### Form with Validation

```tsx
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import * as z from "zod"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { toast } from "sonner"

const schema = z.object({
  email: z.string().email(),
  password: z.string().min(8)
})

export function LoginForm() {
  const form = useForm({
    resolver: zodResolver(schema)
  })

  const onSubmit = (data) => {
    toast.success("Login successful!")
  }

  return (
    <form onSubmit={form.handleSubmit(onSubmit)}>
      <div>
        <Label htmlFor="email">Email</Label>
        <Input id="email" {...form.register("email")} />
      </div>
      <Button type="submit">Login</Button>
    </form>
  )
}
```

### Dialog with Form

```tsx
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"

export function CreateDialog() {
  return (
    <Dialog>
      <DialogTrigger asChild>
        <Button>Create New</Button>
      </DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Create Item</DialogTitle>
        </DialogHeader>
        <form>
          <Input placeholder="Item name" />
          <Button type="submit">Create</Button>
        </form>
      </DialogContent>
    </Dialog>
  )
}
```

### Navigation with Dropdown

```tsx
import { NavigationMenu, NavigationMenuList, NavigationMenuItem, NavigationMenuLink } from "@/components/ui/navigation-menu"
import { DropdownMenu, DropdownMenuTrigger, DropdownMenuContent, DropdownMenuItem } from "@/components/ui/dropdown-menu"
import { Button } from "@/components/ui/button"

export function AppNav() {
  return (
    <NavigationMenu>
      <NavigationMenuList>
        <NavigationMenuItem>
          <NavigationMenuLink href="/">Home</NavigationMenuLink>
        </NavigationMenuItem>
        <NavigationMenuItem>
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="ghost">Products</Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent>
              <DropdownMenuItem>Product A</DropdownMenuItem>
              <DropdownMenuItem>Product B</DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        </NavigationMenuItem>
      </NavigationMenuList>
    </NavigationMenu>
  )
}
```

## Customization

### Modifying Component Styles

Components use Tailwind classes and can be customized:

```tsx
// Customize colors via CSS variables in globals.css
:root {
  --primary: 200 100% 50%;  /* Change primary color */
}

// Or override with props
<Button className="bg-purple-600 hover:bg-purple-700">
  Custom Color
</Button>
```

### Creating Variants

Use `class-variance-authority` (CVA) for variants:

```tsx
import { cva } from "class-variance-authority"

const alertVariants = cva(
  "rounded-lg border p-4",
  {
    variants: {
      variant: {
        default: "bg-background text-foreground",
        destructive: "bg-destructive text-destructive-foreground",
        success: "bg-green-50 text-green-900"
      }
    },
    defaultVariants: {
      variant: "default"
    }
  }
)
```

## Accessibility Features

All shadcn/ui components include:
- [OK] Proper ARIA attributes
- [OK] Keyboard navigation
- [OK] Focus management
- [OK] Screen reader support
- [OK] Reduced motion support

### Example: Dialog Accessibility

```tsx
<Dialog>
  {/* Auto-handled: */}
  {/* - Focus trap */}
  {/* - ESC to close */}
  {/* - aria-labelledby */}
  {/* - Backdrop click to close */}
  <DialogContent>
    <DialogHeader>
      <DialogTitle>Title (used for aria-labelledby)</DialogTitle>
    </DialogHeader>
  </DialogContent>
</Dialog>
```

## Best Practices

### 1. Always Use Labels with Inputs

```tsx
[OK] Good
<div>
  <Label htmlFor="username">Username</Label>
  <Input id="username" />
</div>

[ERROR] Bad
<Input placeholder="Username" />  {/* Placeholder is not a label */}
```

### 2. Provide Accessible Names

```tsx
[OK] Good
<Button aria-label="Close menu">
  <X className="h-4 w-4" />
</Button>

[ERROR] Bad
<Button>
  <X className="h-4 w-4" />  {/* No text or aria-label */}
</Button>
```

### 3. Handle Loading States

```tsx
<Button disabled={isLoading}>
  {isLoading ? "Loading..." : "Submit"}
</Button>
```

### 4. Use Semantic HTML

```tsx
[OK] Good
<form onSubmit={handleSubmit}>
  <Button type="submit">Submit</Button>
</form>

[ERROR] Bad
<div onClick={handleSubmit}>
  <Button type="button">Submit</Button>
</div>
```

## Resources

- **Official Docs**: https://ui.shadcn.com
- **Component Examples**: https://ui.shadcn.com/examples
- **Radix UI Docs**: https://radix-ui.com
- **GitHub**: https://github.com/shadcn-ui/ui

## Integration with This Skill

The skill installs these baseline components automatically:
1. `button` - Primary actions
2. `card` - Content containers
3. `input` - Form inputs
4. `label` - Form labels
5. `dialog` - Modals
6. `separator` - Visual dividers

Additional components can be added as needed:
```bash
npx shadcn-ui add [component-name]
```
