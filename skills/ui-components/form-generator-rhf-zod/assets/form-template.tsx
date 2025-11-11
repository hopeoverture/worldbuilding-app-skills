'use client'

import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { Button } from '@/components/ui/button'
import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from '@/components/ui/form'
import { Input } from '@/components/ui/input'
import { toast } from 'sonner'

// Define your schema
const formSchema = z.object({
  name: z.string().min(2, 'Name must be at least 2 characters').max(100),
  email: z.string().email('Invalid email address'),
  // Add more fields as needed
})

// Infer TypeScript type from schema
type FormValues = z.infer<typeof formSchema>

interface ExampleFormProps {
  defaultValues?: Partial<FormValues>
  onSuccess?: (data: FormValues) => void
}

export function ExampleForm({ defaultValues, onSuccess }: ExampleFormProps) {
  // Initialize form with React Hook Form
  const form = useForm<FormValues>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      name: '',
      email: '',
      ...defaultValues,
    },
    mode: 'onBlur', // Validate on blur for better UX
  })

  // Form submission handler
  async function onSubmit(values: FormValues) {
    try {
      // Call your server action or API endpoint
      const result = await submitFormAction(values)

      if (result.success) {
        toast.success('Form submitted successfully')
        form.reset()
        onSuccess?.(values)
      } else {
        // Handle server-side validation errors
        if (result.errors) {
          Object.entries(result.errors).forEach(([field, message]) => {
            form.setError(field as keyof FormValues, {
              type: 'server',
              message: message as string,
            })
          })
        }
        toast.error(result.message || 'Failed to submit form')
      }
    } catch (error) {
      console.error('Form submission error:', error)
      toast.error('An unexpected error occurred')
    }
  }

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
        {/* Name Field */}
        <FormField
          control={form.control}
          name="name"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Name</FormLabel>
              <FormControl>
                <Input placeholder="Enter your name" {...field} />
              </FormControl>
              <FormDescription>
                This is your display name.
              </FormDescription>
              <FormMessage />
            </FormItem>
          )}
        />

        {/* Email Field */}
        <FormField
          control={form.control}
          name="email"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Email</FormLabel>
              <FormControl>
                <Input type="email" placeholder="you@example.com" {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        {/* Add more FormField components as needed */}

        {/* Root Error Display */}
        {form.formState.errors.root && (
          <div className="rounded-md bg-destructive/15 p-3 text-sm text-destructive">
            {form.formState.errors.root.message}
          </div>
        )}

        {/* Submit Button */}
        <div className="flex gap-3">
          <Button type="submit" disabled={form.formState.isSubmitting}>
            {form.formState.isSubmitting ? 'Submitting...' : 'Submit'}
          </Button>
          <Button
            type="button"
            variant="outline"
            onClick={() => form.reset()}
            disabled={form.formState.isSubmitting}
          >
            Reset
          </Button>
        </div>
      </form>
    </Form>
  )
}

// Placeholder server action - replace with actual implementation
async function submitFormAction(data: FormValues) {
  // Simulate API call
  await new Promise((resolve) => setTimeout(resolve, 1000))

  // Example server-side validation
  const validated = formSchema.safeParse(data)
  if (!validated.success) {
    return {
      success: false,
      errors: validated.error.flatten().fieldErrors,
    }
  }

  // Perform database operation
  // const result = await db.insert(...)

  return {
    success: true,
    data: validated.data,
  }
}
