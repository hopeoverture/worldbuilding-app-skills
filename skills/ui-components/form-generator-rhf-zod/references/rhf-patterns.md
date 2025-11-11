# React Hook Form Patterns Reference

## Core Hooks

### useForm

Main hook for form management:

```tsx
const form = useForm<FormValues>({
  resolver: zodResolver(schema),
  defaultValues: { name: '', email: '' },
  mode: 'onBlur', // 'onChange' | 'onBlur' | 'onSubmit' | 'onTouched' | 'all'
  reValidateMode: 'onChange', // When to re-validate after first error
  criteriaMode: 'firstError', // 'firstError' | 'all'
  shouldFocusError: true,
  shouldUnregister: false,
  shouldUseNativeValidation: false,
  delayError: 500 // Delay error display (ms)
})
```

### useFieldArray

Manage dynamic field arrays:

```tsx
const { fields, append, prepend, remove, swap, move, insert } = useFieldArray({
  control: form.control,
  name: 'items',
  keyName: 'id' // Custom key name (default: 'id')
})
```

### useWatch

Watch field values without re-rendering entire form:

```tsx
const watchedValue = useWatch({
  control: form.control,
  name: 'fieldName',
  defaultValue: 'default'
})

// Watch multiple fields
const [field1, field2] = useWatch({
  control: form.control,
  name: ['field1', 'field2']
})

// Watch all fields
const allValues = useWatch({ control: form.control })
```

### useFormState

Access form state without subscribing to all changes:

```tsx
const { isDirty, isValid, errors, isSubmitting } = useFormState({
  control: form.control
})
```

### useController

Lower-level field control:

```tsx
const { field, fieldState, formState } = useController({
  name: 'fieldName',
  control: form.control,
  rules: { required: true },
  defaultValue: ''
})
```

## Form Validation Modes

### onSubmit (Default)
- Validates on form submission
- Best for simple forms
- Minimal re-renders
- Delayed feedback

```tsx
const form = useForm({ mode: 'onSubmit' })
```

### onBlur
- Validates when field loses focus
- Good balance of UX and performance
- Recommended for most forms

```tsx
const form = useForm({ mode: 'onBlur' })
```

### onChange
- Validates on every keystroke
- Real-time feedback
- More re-renders
- Good for complex validation

```tsx
const form = useForm({ mode: 'onChange' })
```

### onTouched
- Validates after field is touched then on every change
- Progressive enhancement approach

```tsx
const form = useForm({ mode: 'onTouched' })
```

### all
- Validates on all events
- Most feedback but most re-renders

```tsx
const form = useForm({ mode: 'all' })
```

## Form Methods

### Form State Access

```tsx
// Check if form is dirty
form.formState.isDirty

// Check if form is valid
form.formState.isValid

// Check if submitting
form.formState.isSubmitting

// Get all errors
form.formState.errors

// Check if field is touched
form.formState.touchedFields.fieldName

// Get dirty fields
form.formState.dirtyFields

// Submit count
form.formState.submitCount
```

### Form Actions

```tsx
// Submit form
form.handleSubmit(onSubmit, onError)

// Reset form
form.reset() // to default values
form.reset({ name: 'New Name' }) // to specific values

// Set value
form.setValue('fieldName', 'value', {
  shouldValidate: true,
  shouldDirty: true,
  shouldTouch: true
})

// Get value
const value = form.getValues('fieldName')
const allValues = form.getValues()

// Clear errors
form.clearErrors() // all errors
form.clearErrors('fieldName') // specific field

// Set error
form.setError('fieldName', {
  type: 'manual',
  message: 'Error message'
})

// Trigger validation
form.trigger() // all fields
form.trigger('fieldName') // specific field
form.trigger(['field1', 'field2']) // multiple fields

// Set focus
form.setFocus('fieldName')
```

## Advanced Patterns

### Dependent Fields

```tsx
const faction = form.watch('faction')

<FormField
  control={form.control}
  name="rank"
  render={({ field }) => (
    <FormItem>
      <FormLabel>Rank</FormLabel>
      <Select onValueChange={field.onChange} defaultValue={field.value}>
        <FormControl>
          <SelectTrigger>
            <SelectValue placeholder="Select rank" />
          </SelectTrigger>
        </FormControl>
        <SelectContent>
          {getRanksForFaction(faction).map(rank => (
            <SelectItem key={rank.id} value={rank.id}>
              {rank.name}
            </SelectItem>
          ))}
        </SelectContent>
      </Select>
      <FormMessage />
    </FormItem>
  )}
/>
```

### Async Validation

```tsx
const schema = z.object({
  username: z.string()
    .min(3)
    .refine(async (username) => {
      const available = await checkUsernameAvailability(username)
      return available
    }, {
      message: 'Username already taken'
    })
})

// Use mode: 'onBlur' for better UX with async validation
const form = useForm({
  resolver: zodResolver(schema),
  mode: 'onBlur'
})
```

### Form Context

Share form between multiple components:

```tsx
// Parent component
import { FormProvider } from 'react-hook-form'

const form = useForm()

<FormProvider {...form}>
  <ChildComponent1 />
  <ChildComponent2 />
</FormProvider>

// Child component
import { useFormContext } from 'react-hook-form'

function ChildComponent() {
  const form = useFormContext()
  // Use form methods
}
```

### Controlled Components

```tsx
import { Controller } from 'react-hook-form'

<Controller
  name="customField"
  control={form.control}
  render={({ field, fieldState, formState }) => (
    <CustomComponent
      value={field.value}
      onChange={field.onChange}
      onBlur={field.onBlur}
      error={fieldState.error?.message}
    />
  )}
/>
```

### Transform Values on Submit

```tsx
const onSubmit = form.handleSubmit((data) => {
  const transformed = {
    ...data,
    age: parseInt(data.age),
    tags: data.tags.map(t => t.toLowerCase()),
    createdAt: new Date()
  }
  // Submit transformed data
})
```

### Dirty Field Tracking

```tsx
const dirtyFields = form.formState.dirtyFields

function onSubmit(data: FormValues) {
  // Only submit changed fields
  const changedData = Object.keys(dirtyFields).reduce((acc, key) => {
    acc[key] = data[key]
    return acc
  }, {} as Partial<FormValues>)

  await updateEntity(id, changedData)
}
```

### Multi-Step Form

```tsx
const [step, setStep] = useState(1)

function onSubmit(data: FormValues) {
  if (step < 3) {
    setStep(step + 1)
  } else {
    // Final submission
    submitData(data)
  }
}

<Form {...form}>
  <form onSubmit={form.handleSubmit(onSubmit)}>
    {step === 1 && <Step1Fields control={form.control} />}
    {step === 2 && <Step2Fields control={form.control} />}
    {step === 3 && <Step3Fields control={form.control} />}

    <div className="flex gap-2">
      {step > 1 && (
        <Button type="button" onClick={() => setStep(step - 1)}>
          Previous
        </Button>
      )}
      <Button type="submit">
        {step < 3 ? 'Next' : 'Submit'}
      </Button>
    </div>
  </form>
</Form>
```

### Reset with Default Values

```tsx
// Reset to specific values after successful submission
async function onSubmit(data: FormValues) {
  const result = await createEntity(data)

  if (result.success) {
    form.reset({
      name: '',
      type: 'default',
      // Keep some values
      category: data.category
    })
  }
}
```

### Error Handling

```tsx
async function onSubmit(data: FormValues) {
  try {
    const result = await submitAction(data)

    if (!result.success) {
      // Set server errors
      if (result.errors) {
        Object.entries(result.errors).forEach(([field, message]) => {
          form.setError(field as any, {
            type: 'server',
            message: message as string
          })
        })
      }

      // Set root error for general issues
      if (result.message) {
        form.setError('root', {
          type: 'server',
          message: result.message
        })
      }
    } else {
      toast.success('Saved successfully')
      form.reset()
    }
  } catch (error) {
    form.setError('root', {
      type: 'server',
      message: 'An unexpected error occurred'
    })
  }
}

// Display root error
{form.formState.errors.root && (
  <Alert variant="destructive">
    <AlertDescription>
      {form.formState.errors.root.message}
    </AlertDescription>
  </Alert>
)}
```

### Optimistic Updates

```tsx
const [optimisticData, setOptimisticData] = useState<Entity | null>(null)

async function onSubmit(data: FormValues) {
  // Show optimistic state
  setOptimisticData(data as Entity)
  toast.success('Saving...')

  try {
    const result = await saveEntity(data)

    if (result.success) {
      // Confirm success
      setOptimisticData(result.data)
      toast.success('Saved successfully')
    } else {
      // Revert optimistic state
      setOptimisticData(null)
      toast.error('Save failed')
    }
  } catch (error) {
    setOptimisticData(null)
    toast.error('An error occurred')
  }
}
```

### Auto-Save Draft

```tsx
import { useEffect } from 'react'
import { useDebouncedCallback } from 'use-debounce'

const saveDraft = useDebouncedCallback(async (data: FormValues) => {
  await saveDraftToStorage(data)
}, 1000)

useEffect(() => {
  const subscription = form.watch((data) => {
    if (form.formState.isDirty) {
      saveDraft(data as FormValues)
    }
  })
  return () => subscription.unsubscribe()
}, [form.watch, form.formState.isDirty])

// Load draft on mount
useEffect(() => {
  const draft = loadDraftFromStorage()
  if (draft) {
    form.reset(draft)
  }
}, [])
```

### Conditional Required Fields

```tsx
const schema = z.object({
  type: z.enum(['character', 'location']),
  characterRace: z.string().optional(),
  locationType: z.string().optional()
}).refine(
  (data) => {
    if (data.type === 'character') {
      return data.characterRace !== undefined && data.characterRace.length > 0
    }
    return true
  },
  {
    message: 'Race is required for characters',
    path: ['characterRace']
  }
).refine(
  (data) => {
    if (data.type === 'location') {
      return data.locationType !== undefined && data.locationType.length > 0
    }
    return true
  },
  {
    message: 'Location type is required',
    path: ['locationType']
  }
)
```

### Field Masking/Formatting

```tsx
<FormField
  control={form.control}
  name="phone"
  render={({ field }) => (
    <FormItem>
      <FormLabel>Phone</FormLabel>
      <FormControl>
        <Input
          {...field}
          onChange={(e) => {
            const formatted = formatPhoneNumber(e.target.value)
            field.onChange(formatted)
          }}
          placeholder="(123) 456-7890"
        />
      </FormControl>
      <FormMessage />
    </FormItem>
  )}
/>

function formatPhoneNumber(value: string): string {
  const numbers = value.replace(/\D/g, '')
  const match = numbers.match(/^(\d{0,3})(\d{0,3})(\d{0,4})$/)
  if (!match) return value

  const formatted = [match[1], match[2], match[3]]
    .filter(Boolean)
    .join('-')

  return formatted
}
```

## Performance Optimization

### Isolate Re-renders

```tsx
// Bad: Entire form re-renders on field change
const value = form.watch('field')

// Good: Only component re-renders
function WatchedField() {
  const value = useWatch({ control: form.control, name: 'field' })
  return <div>{value}</div>
}
```

### Use FormField for Each Field

```tsx
// FormField isolates re-renders to individual fields
<FormField
  control={form.control}
  name="field"
  render={({ field }) => (
    <FormItem>
      <FormControl>
        <Input {...field} />
      </FormControl>
    </FormItem>
  )}
/>
```

### Memoize Expensive Computations

```tsx
import { useMemo } from 'react'

const options = useMemo(() => {
  return computeExpensiveOptions()
}, [dependencies])
```

## Testing Patterns

```tsx
import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { MyForm } from './MyForm'

describe('MyForm', () => {
  it('submits form with valid data', async () => {
    const onSubmit = vi.fn()
    render(<MyForm onSubmit={onSubmit} />)

    await userEvent.type(screen.getByLabelText(/name/i), 'Test Name')
    await userEvent.click(screen.getByRole('button', { name: /submit/i }))

    await waitFor(() => {
      expect(onSubmit).toHaveBeenCalledWith({
        name: 'Test Name'
      })
    })
  })

  it('shows validation errors', async () => {
    render(<MyForm />)

    await userEvent.click(screen.getByRole('button', { name: /submit/i }))

    expect(await screen.findByText(/name is required/i)).toBeInTheDocument()
  })

  it('clears errors on valid input', async () => {
    render(<MyForm />)

    const input = screen.getByLabelText(/name/i)

    await userEvent.click(screen.getByRole('button', { name: /submit/i }))
    expect(await screen.findByText(/name is required/i)).toBeInTheDocument()

    await userEvent.type(input, 'Valid Name')
    await waitFor(() => {
      expect(screen.queryByText(/name is required/i)).not.toBeInTheDocument()
    })
  })
})
```
