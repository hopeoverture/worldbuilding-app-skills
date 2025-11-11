import { z } from 'zod';

/**
 * Form validation schema template
 *
 * Usage:
 * 1. Customize the schema fields for your form
 * 2. Use with React Hook Form or other form libraries
 * 3. Extract TypeScript type with z.infer<typeof formSchema>
 */

export const formSchema = z.object({
  // Text input
  name: z.string()
    .min(1, 'Name is required')
    .max(100, 'Name must be 100 characters or less'),

  // Email input
  email: z.string()
    .email('Invalid email address'),

  // Optional text field
  description: z.string()
    .max(500, 'Description must be 500 characters or less')
    .optional(),

  // Number input
  age: z.coerce.number()
    .int('Age must be a whole number')
    .positive('Age must be positive')
    .optional(),

  // Select/dropdown
  category: z.enum(['option1', 'option2', 'option3'], {
    required_error: 'Please select a category',
  }),

  // Checkbox
  agreedToTerms: z.boolean()
    .refine((val) => val === true, {
      message: 'You must agree to the terms',
    }),

  // Multi-select
  tags: z.array(z.string())
    .min(1, 'At least one tag is required')
    .max(10, 'Maximum 10 tags allowed'),

  // Date input
  birthDate: z.coerce.date()
    .max(new Date(), 'Birth date cannot be in the future')
    .optional(),
});

// Infer TypeScript type from schema
export type FormData = z.infer<typeof formSchema>;

// Example: React Hook Form integration
/*
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';

function MyForm() {
  const { register, handleSubmit, formState: { errors } } = useForm<FormData>({
    resolver: zodResolver(formSchema),
  });

  const onSubmit = (data: FormData) => {
    console.log('Valid form data:', data);
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input {...register('name')} />
      {errors.name && <span>{errors.name.message}</span>}

      <button type="submit">Submit</button>
    </form>
  );
}
*/
