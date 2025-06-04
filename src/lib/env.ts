import { z } from 'zod';

// Define the schema for environment variables
const envSchema = z.object({
  // Next.js
  NODE_ENV: z.enum(['development', 'production', 'test']).default('development'),
  
  // Supabase
  NEXT_PUBLIC_SUPABASE_URL: z.string().url('Invalid Supabase URL'),
  NEXT_PUBLIC_SUPABASE_ANON_KEY: z.string().min(1, 'Supabase anon key is required'),
  SUPABASE_SERVICE_ROLE_KEY: z.string().min(1, 'Supabase service role key is required'),
  
  // AI Services
  OPENAI_API_KEY: z.string().min(1, 'OpenAI API key is required'),
  ANTHROPIC_API_KEY: z.string().min(1, 'Anthropic API key is required').optional(),
  
  // Storage
  STORAGE_BUCKET: z.string().default('brand-assets'),
  
  // Security
  NEXTAUTH_SECRET: z.string().min(32, 'NextAuth secret must be at least 32 characters').optional(),
  ENCRYPTION_KEY: z.string().min(32, 'Encryption key must be at least 32 characters').optional(),
  
  // Rate Limiting
  REDIS_URL: z.string().url('Invalid Redis URL').optional(),
  
  // Monitoring
  SENTRY_DSN: z.string().url('Invalid Sentry DSN').optional(),
  
  // Application
  NEXT_PUBLIC_APP_URL: z.string().url('Invalid app URL').default('http://localhost:3000'),
  
  // Database
  DATABASE_URL: z.string().url('Invalid database URL').optional(),
  
  // External Services
  WEBHOOK_SECRET: z.string().min(1, 'Webhook secret is required').optional(),
  
  // Development
  SKIP_ENV_VALIDATION: z.string().optional(),
});

// Type for validated environment variables
export type Env = z.infer<typeof envSchema>;

// Validate environment variables
function validateEnv(): Env {
  // Skip validation in certain scenarios
  if (process.env.SKIP_ENV_VALIDATION === 'true') {
    console.warn('⚠️ Environment validation skipped');
    return process.env as any;
  }

  try {
    const parsed = envSchema.parse(process.env);
    
    // Additional validation for production
    if (parsed.NODE_ENV === 'production') {
      if (!parsed.NEXTAUTH_SECRET) {
        throw new Error('NEXTAUTH_SECRET is required in production');
      }
      if (!parsed.ENCRYPTION_KEY) {
        throw new Error('ENCRYPTION_KEY is required in production');
      }
      if (!parsed.SENTRY_DSN) {
        console.warn('⚠️ SENTRY_DSN not configured for production monitoring');
      }
    }

    // Log successful validation in development
    if (parsed.NODE_ENV === 'development') {
      console.log('✅ Environment variables validated successfully');
    }

    return parsed;
  } catch (error) {
    if (error instanceof z.ZodError) {
      const errorMessages = error.errors.map(err => 
        `${err.path.join('.')}: ${err.message}`
      ).join('\n');
      
      throw new Error(
        `❌ Invalid environment variables:\n${errorMessages}\n\n` +
        'Please check your .env file and ensure all required variables are set correctly.'
      );
    }
    throw error;
  }
}

// Export validated environment variables
export const env = validateEnv();

// Helper functions for environment checks
export const isDevelopment = env.NODE_ENV === 'development';
export const isProduction = env.NODE_ENV === 'production';
export const isTest = env.NODE_ENV === 'test';

// Feature flags based on environment
export const features = {
  enableAnalytics: isProduction,
  enableDebugLogs: isDevelopment,
  enableRateLimiting: isProduction || env.REDIS_URL !== undefined,
  enableEncryption: env.ENCRYPTION_KEY !== undefined,
  enableMonitoring: env.SENTRY_DSN !== undefined,
} as const;

// Utility to get safe environment info (without secrets)
export function getSafeEnvInfo() {
  return {
    nodeEnv: env.NODE_ENV,
    hasOpenAI: !!env.OPENAI_API_KEY,
    hasAnthropic: !!env.ANTHROPIC_API_KEY,
    hasRedis: !!env.REDIS_URL,
    hasSentry: !!env.SENTRY_DSN,
    features,
  };
}
