'use server';

import { z } from 'zod';

/**
 * Server Action validation schema template
 *
 * Usage:
 * 1. Define input schema for Server Action parameters
 * 2. Validate with safeParse at the beginning of the action
 * 3. Return validation errors to the client
 */

// Input schema
const actionInputSchema = z.object({
  id: z.string().uuid('Invalid ID format'),
  name: z.string().min(1, 'Name is required').max(100),
  type: z.enum(['type1', 'type2', 'type3']),
  metadata: z.record(z.string(), z.any()).optional(),
});

// Output schema (optional, for type safety)
const actionOutputSchema = z.object({
  success: z.boolean(),
  data: z.any().optional(),
  errors: z.record(z.array(z.string())).optional(),
});

// Types
type ActionInput = z.infer<typeof actionInputSchema>;
type ActionOutput = z.infer<typeof actionOutputSchema>;

/**
 * Example Server Action with validation
 */
export async function myServerAction(input: unknown): Promise<ActionOutput> {
  // Validate input
  const result = actionInputSchema.safeParse(input);

  if (!result.success) {
    return {
      success: false,
      errors: result.error.flatten().fieldErrors,
    };
  }

  // Type-safe validated data
  const { id, name, type, metadata } = result.data;

  try {
    // Perform server-side logic
    // Example: database operation, API call, etc.
    const data = await performAction(id, name, type, metadata);

    return {
      success: true,
      data,
    };
  } catch (error) {
    return {
      success: false,
      errors: {
        _general: ['An unexpected error occurred'],
      },
    };
  }
}

async function performAction(
  id: string,
  name: string,
  type: string,
  metadata?: Record<string, any>
) {
  // Implement your server-side logic here
  return { id, name, type, metadata };
}

// Example: FormData-based Server Action
export async function formDataAction(formData: FormData): Promise<ActionOutput> {
  const rawData = {
    id: formData.get('id'),
    name: formData.get('name'),
    type: formData.get('type'),
  };

  const result = actionInputSchema.safeParse(rawData);

  if (!result.success) {
    return {
      success: false,
      errors: result.error.flatten().fieldErrors,
    };
  }

  // Process validated data
  const { id, name, type } = result.data;

  // ... rest of implementation

  return { success: true, data: { id, name, type } };
}

// Example: Client-side usage
/*
'use client';

import { myServerAction } from './actions';
import { useState } from 'react';

function MyComponent() {
  const [errors, setErrors] = useState<Record<string, string[]>>({});

  async function handleSubmit(data: any) {
    const result = await myServerAction(data);

    if (!result.success) {
      setErrors(result.errors || {});
    } else {
      console.log('Success:', result.data);
      setErrors({});
    }
  }

  return (
    <div>
      {errors.name && <span>{errors.name[0]}</span>}
    </div>
  );
}
*/
