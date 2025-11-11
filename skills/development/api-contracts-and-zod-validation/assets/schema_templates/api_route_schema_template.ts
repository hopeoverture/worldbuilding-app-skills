import { NextRequest, NextResponse } from 'next/server';
import { z } from 'zod';

/**
 * API Route validation schema template
 *
 * Usage:
 * 1. Define request and response schemas
 * 2. Validate incoming requests with safeParse
 * 3. Return typed errors for invalid requests
 */

// Request schema
const requestSchema = z.object({
  query: z.string().min(1, 'Query is required'),
  filters: z.object({
    type: z.array(z.string()).optional(),
    tags: z.array(z.string()).optional(),
    dateRange: z.object({
      start: z.string().datetime().optional(),
      end: z.string().datetime().optional(),
    }).optional(),
  }).optional(),
  pagination: z.object({
    page: z.number().int().positive().default(1),
    limit: z.number().int().min(1).max(100).default(10),
  }).optional(),
});

// Response schema
const responseSchema = z.object({
  success: z.boolean(),
  data: z.any().optional(),
  error: z.string().optional(),
  details: z.any().optional(),
});

// Types
type RequestBody = z.infer<typeof requestSchema>;
type ResponseBody = z.infer<typeof responseSchema>;

/**
 * POST endpoint with validation
 */
export async function POST(request: NextRequest): Promise<NextResponse<ResponseBody>> {
  try {
    // Parse request body
    const body = await request.json();

    // Validate request
    const result = requestSchema.safeParse(body);

    if (!result.success) {
      return NextResponse.json(
        {
          success: false,
          error: 'Invalid request body',
          details: result.error.format(),
        },
        { status: 400 }
      );
    }

    // Type-safe validated data
    const { query, filters, pagination } = result.data;

    // Perform business logic
    const data = await processRequest(query, filters, pagination);

    return NextResponse.json({
      success: true,
      data,
    });
  } catch (error) {
    return NextResponse.json(
      {
        success: false,
        error: 'Internal server error',
      },
      { status: 500 }
    );
  }
}

async function processRequest(
  query: string,
  filters?: RequestBody['filters'],
  pagination?: RequestBody['pagination']
) {
  // Implement your business logic here
  return { results: [], total: 0 };
}

/**
 * GET endpoint with query parameter validation
 */
const queryParamsSchema = z.object({
  id: z.string().uuid('Invalid ID format'),
  includeRelated: z.coerce.boolean().optional(),
});

export async function GET(request: NextRequest): Promise<NextResponse<ResponseBody>> {
  // Parse query parameters
  const searchParams = request.nextUrl.searchParams;
  const queryParams = {
    id: searchParams.get('id'),
    includeRelated: searchParams.get('includeRelated'),
  };

  // Validate query parameters
  const result = queryParamsSchema.safeParse(queryParams);

  if (!result.success) {
    return NextResponse.json(
      {
        success: false,
        error: 'Invalid query parameters',
        details: result.error.format(),
      },
      { status: 400 }
    );
  }

  const { id, includeRelated } = result.data;

  // Fetch data
  const data = await fetchData(id, includeRelated);

  return NextResponse.json({
    success: true,
    data,
  });
}

async function fetchData(id: string, includeRelated?: boolean) {
  // Implement your data fetching logic here
  return { id, includeRelated };
}

/**
 * PATCH endpoint with partial update validation
 */
const updateSchema = z.object({
  name: z.string().min(1).max(100).optional(),
  description: z.string().max(500).optional(),
  tags: z.array(z.string()).max(10).optional(),
  status: z.enum(['active', 'inactive', 'archived']).optional(),
}).refine(
  (data) => Object.keys(data).length > 0,
  { message: 'At least one field must be provided for update' }
);

export async function PATCH(
  request: NextRequest,
  { params }: { params: { id: string } }
): Promise<NextResponse<ResponseBody>> {
  // Validate ID from route params
  const idResult = z.string().uuid().safeParse(params.id);

  if (!idResult.success) {
    return NextResponse.json(
      {
        success: false,
        error: 'Invalid ID format',
      },
      { status: 400 }
    );
  }

  // Parse and validate request body
  const body = await request.json();
  const result = updateSchema.safeParse(body);

  if (!result.success) {
    return NextResponse.json(
      {
        success: false,
        error: 'Invalid update data',
        details: result.error.format(),
      },
      { status: 400 }
    );
  }

  const id = idResult.data;
  const updates = result.data;

  // Perform update
  const data = await updateData(id, updates);

  return NextResponse.json({
    success: true,
    data,
  });
}

async function updateData(id: string, updates: z.infer<typeof updateSchema>) {
  // Implement your update logic here
  return { id, ...updates };
}

// Example: Middleware with validation
export function validateRequest<T>(schema: z.ZodSchema<T>) {
  return async (request: NextRequest): Promise<{ data?: T; error?: ResponseBody }> => {
    try {
      const body = await request.json();
      const result = schema.safeParse(body);

      if (!result.success) {
        return {
          error: {
            success: false,
            error: 'Validation failed',
            details: result.error.format(),
          },
        };
      }

      return { data: result.data };
    } catch {
      return {
        error: {
          success: false,
          error: 'Invalid JSON body',
        },
      };
    }
  };
}

// Usage of middleware:
/*
export async function POST(request: NextRequest) {
  const { data, error } = await validateRequest(requestSchema)(request);

  if (error) {
    return NextResponse.json(error, { status: 400 });
  }

  // Use validated data
  console.log(data);

  return NextResponse.json({ success: true });
}
*/
