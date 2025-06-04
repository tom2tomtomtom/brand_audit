import { z } from 'zod';
import { NextRequest, NextResponse } from 'next/server';
import { ValidationError } from '@/lib/errors';

// Common validation schemas
export const commonSchemas = {
  id: z.string().uuid('Invalid ID format'),
  url: z.string().url('Invalid URL format'),
  email: z.string().email('Invalid email format'),
  name: z.string().min(1, 'Name is required').max(100, 'Name too long'),
  description: z.string().max(1000, 'Description too long').optional(),
  pagination: z.object({
    page: z.number().int().min(1).default(1),
    limit: z.number().int().min(1).max(100).default(20),
  }),
};

// Brand validation schemas
export const brandSchemas = {
  create: z.object({
    name: commonSchemas.name,
    website_url: commonSchemas.url,
    description: commonSchemas.description,
    industry: z.string().optional(),
    organization_id: commonSchemas.id,
  }),
  
  update: z.object({
    name: commonSchemas.name.optional(),
    website_url: commonSchemas.url.optional(),
    description: commonSchemas.description,
    industry: z.string().optional(),
  }),
  
  analyze: z.object({
    brand_id: commonSchemas.id,
    analysis_type: z.enum(['comprehensive', 'visual', 'content', 'competitive']),
    options: z.object({
      include_screenshots: z.boolean().default(true),
      include_assets: z.boolean().default(true),
      depth: z.enum(['shallow', 'medium', 'deep']).default('medium'),
    }).optional(),
  }),
};

// Organization validation schemas
export const organizationSchemas = {
  create: z.object({
    name: commonSchemas.name,
    description: commonSchemas.description,
    website: commonSchemas.url.optional(),
    industry: z.string().optional(),
  }),
  
  update: z.object({
    name: commonSchemas.name.optional(),
    description: commonSchemas.description,
    website: commonSchemas.url.optional(),
    industry: z.string().optional(),
  }),
  
  invite: z.object({
    email: commonSchemas.email,
    role: z.enum(['admin', 'member', 'viewer']).default('member'),
  }),
};

// Project validation schemas
export const projectSchemas = {
  create: z.object({
    name: commonSchemas.name,
    description: commonSchemas.description,
    organization_id: commonSchemas.id,
    brand_ids: z.array(commonSchemas.id).optional(),
  }),
  
  update: z.object({
    name: commonSchemas.name.optional(),
    description: commonSchemas.description,
    status: z.enum(['active', 'completed', 'archived']).optional(),
  }),
};

// Analysis validation schemas
export const analysisSchemas = {
  create: z.object({
    brand_id: commonSchemas.id,
    type: z.enum(['brand_positioning', 'visual_identity', 'content_analysis', 'competitive_analysis']),
    parameters: z.record(z.any()).optional(),
  }),
  
  feedback: z.object({
    analysis_id: commonSchemas.id,
    rating: z.number().int().min(1).max(5),
    feedback: z.string().max(1000).optional(),
    improvements: z.array(z.string()).optional(),
  }),
};

// Presentation validation schemas
export const presentationSchemas = {
  create: z.object({
    name: commonSchemas.name,
    project_id: commonSchemas.id,
    template: z.enum(['executive', 'detailed', 'visual', 'competitive']).default('executive'),
    sections: z.array(z.string()).optional(),
  }),
  
  update: z.object({
    name: commonSchemas.name.optional(),
    status: z.enum(['draft', 'generating', 'completed', 'failed']).optional(),
    content: z.record(z.any()).optional(),
  }),
};

// Request validation middleware
export function validateRequest<T>(schema: z.ZodSchema<T>) {
  return async (request: NextRequest): Promise<T> => {
    try {
      const contentType = request.headers.get('content-type');
      
      let data: any;
      
      if (contentType?.includes('application/json')) {
        data = await request.json();
      } else if (contentType?.includes('application/x-www-form-urlencoded')) {
        const formData = await request.formData();
        data = Object.fromEntries(formData.entries());
      } else {
        // For GET requests, validate query parameters
        const url = new URL(request.url);
        data = Object.fromEntries(url.searchParams.entries());
        
        // Convert string values to appropriate types for query params
        const convertedData: Record<string, any> = {};
        Object.keys(data).forEach(key => {
          const value = data[key];
          if (value === 'true') convertedData[key] = true;
          else if (value === 'false') convertedData[key] = false;
          else if (!isNaN(Number(value)) && value !== '') convertedData[key] = Number(value);
          else convertedData[key] = value;
        });
        data = convertedData;
      }
      
      return schema.parse(data);
    } catch (error) {
      if (error instanceof z.ZodError) {
        const errorMessages: Record<string, string[]> = {};
        
        error.errors.forEach(err => {
          const path = err.path.join('.');
          if (!errorMessages[path]) {
            errorMessages[path] = [];
          }
          errorMessages[path].push(err.message);
        });
        
        throw new ValidationError(
          'Request validation failed',
          errorMessages
        );
      }
      throw error;
    }
  };
}

// Query parameter validation for GET requests
export function validateQuery<T>(schema: z.ZodSchema<T>) {
  return (request: NextRequest): T => {
    try {
      const url = new URL(request.url);
      const params = Object.fromEntries(url.searchParams.entries());
      
      // Convert string values to appropriate types
      Object.keys(params).forEach(key => {
        const value = params[key];
        if (value === 'true') (params as any)[key] = true;
        else if (value === 'false') (params as any)[key] = false;
        else if (!isNaN(Number(value)) && value !== '') (params as any)[key] = Number(value);
      });
      
      return schema.parse(params);
    } catch (error) {
      if (error instanceof z.ZodError) {
        const errorMessages: Record<string, string[]> = {};
        
        error.errors.forEach(err => {
          const path = err.path.join('.');
          if (!errorMessages[path]) {
            errorMessages[path] = [];
          }
          errorMessages[path].push(err.message);
        });
        
        throw new ValidationError(
          'Query parameter validation failed',
          errorMessages
        );
      }
      throw error;
    }
  };
}

// Response validation (for development/testing)
export function validateResponse<T>(schema: z.ZodSchema<T>, data: unknown): T {
  try {
    return schema.parse(data);
  } catch (error) {
    if (error instanceof z.ZodError) {
      console.error('Response validation failed:', error.errors);
      // In development, throw error. In production, log and return data as-is
      if (process.env.NODE_ENV === 'development') {
        throw new Error(`Response validation failed: ${error.message}`);
      }
    }
    return data as T;
  }
}

// Utility to create error response
export function createValidationErrorResponse(error: ValidationError): NextResponse {
  return NextResponse.json(
    {
      error: 'Validation Error',
      message: error.message,
      details: error.errors,
    },
    { status: 400 }
  );
}

// Common response schemas for validation
export const responseSchemas = {
  success: z.object({
    success: z.boolean(),
    message: z.string().optional(),
    data: z.any().optional(),
  }),
  
  error: z.object({
    error: z.string(),
    message: z.string(),
    details: z.record(z.array(z.string())).optional(),
  }),
  
  pagination: z.object({
    data: z.array(z.any()),
    pagination: z.object({
      page: z.number(),
      limit: z.number(),
      total: z.number(),
      totalPages: z.number(),
    }),
  }),
};
