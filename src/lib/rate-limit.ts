import { NextRequest, NextResponse } from 'next/server';
import { RateLimitError } from '@/lib/errors';
import { logger } from '@/lib/logger';
import { APP_CONSTANTS } from '@/lib/constants';

// Rate limit configuration interface
export interface RateLimitConfig {
  windowMs: number; // Time window in milliseconds
  maxRequests: number; // Maximum requests per window
  keyGenerator?: (request: NextRequest) => string;
  skipSuccessfulRequests?: boolean;
  skipFailedRequests?: boolean;
  message?: string;
  headers?: boolean; // Include rate limit headers in response
}

// Rate limit store interface
interface RateLimitStore {
  get(key: string): Promise<number | null>;
  set(key: string, value: number, ttl: number): Promise<void>;
  increment(key: string, ttl: number): Promise<number>;
  reset(key: string): Promise<void>;
}

// In-memory store implementation (for development)
class MemoryStore implements RateLimitStore {
  private store = new Map<string, { count: number; resetTime: number }>();

  async get(key: string): Promise<number | null> {
    const entry = this.store.get(key);
    if (!entry || Date.now() > entry.resetTime) {
      this.store.delete(key);
      return null;
    }
    return entry.count;
  }

  async set(key: string, value: number, ttl: number): Promise<void> {
    this.store.set(key, {
      count: value,
      resetTime: Date.now() + ttl,
    });
  }

  async increment(key: string, ttl: number): Promise<number> {
    const entry = this.store.get(key);
    const now = Date.now();
    
    if (!entry || now > entry.resetTime) {
      const newEntry = { count: 1, resetTime: now + ttl };
      this.store.set(key, newEntry);
      return 1;
    }
    
    entry.count++;
    return entry.count;
  }

  async reset(key: string): Promise<void> {
    this.store.delete(key);
  }

  // Cleanup expired entries periodically
  cleanup(): void {
    const now = Date.now();
    const entries = Array.from(this.store.entries());
    for (const [key, entry] of entries) {
      if (now > entry.resetTime) {
        this.store.delete(key);
      }
    }
  }
}

// Redis store implementation (for production)
class RedisStore implements RateLimitStore {
  private redis: any; // Redis client would be injected

  constructor(redisClient?: any) {
    this.redis = redisClient;
  }

  async get(key: string): Promise<number | null> {
    if (!this.redis) return null;
    
    try {
      const value = await this.redis.get(key);
      return value ? parseInt(value, 10) : null;
    } catch (error) {
      logger.error('Redis get error in rate limiter', { key }, error as Error);
      return null;
    }
  }

  async set(key: string, value: number, ttl: number): Promise<void> {
    if (!this.redis) return;
    
    try {
      await this.redis.setex(key, Math.ceil(ttl / 1000), value);
    } catch (error) {
      logger.error('Redis set error in rate limiter', { key, value, ttl }, error as Error);
    }
  }

  async increment(key: string, ttl: number): Promise<number> {
    if (!this.redis) return 1;
    
    try {
      const multi = this.redis.multi();
      multi.incr(key);
      multi.expire(key, Math.ceil(ttl / 1000));
      const results = await multi.exec();
      return results[0][1];
    } catch (error) {
      logger.error('Redis increment error in rate limiter', { key, ttl }, error as Error);
      return 1;
    }
  }

  async reset(key: string): Promise<void> {
    if (!this.redis) return;
    
    try {
      await this.redis.del(key);
    } catch (error) {
      logger.error('Redis reset error in rate limiter', { key }, error as Error);
    }
  }
}

// Rate limiter class
export class RateLimiter {
  private store: RateLimitStore;
  private config: Required<RateLimitConfig>;

  constructor(config: RateLimitConfig, store?: RateLimitStore) {
    this.config = {
      keyGenerator: this.defaultKeyGenerator,
      skipSuccessfulRequests: false,
      skipFailedRequests: false,
      message: 'Too many requests, please try again later',
      headers: true,
      ...config,
    };

    this.store = store || new MemoryStore();

    // Setup cleanup for memory store
    if (this.store instanceof MemoryStore) {
      setInterval(() => {
        (this.store as MemoryStore).cleanup();
      }, 60000); // Cleanup every minute
    }
  }

  private defaultKeyGenerator(request: NextRequest): string {
    // Use IP address as default key
    const forwarded = request.headers.get('x-forwarded-for');
    const ip = forwarded ? forwarded.split(',')[0] : 
               request.headers.get('x-real-ip') || 
               'unknown';
    return `rate_limit:${ip}`;
  }

  private getUserId(request: NextRequest): string | null {
    // Extract user ID from JWT token or session
    try {
      const authHeader = request.headers.get('authorization');
      if (authHeader?.startsWith('Bearer ')) {
        // In a real implementation, you would decode the JWT
        // const token = authHeader.substring(7);
        // const decoded = jwt.decode(token);
        // return decoded.sub;
        return null; // Placeholder
      }
      return null;
    } catch {
      return null;
    }
  }

  async checkLimit(request: NextRequest): Promise<{
    allowed: boolean;
    limit: number;
    remaining: number;
    resetTime: number;
    retryAfter?: number;
  }> {
    const key = this.config.keyGenerator(request);
    const now = Date.now();
    const resetTime = now + this.config.windowMs;

    try {
      const currentCount = await this.store.increment(key, this.config.windowMs);
      
      const remaining = Math.max(0, this.config.maxRequests - currentCount);
      const allowed = currentCount <= this.config.maxRequests;

      const result = {
        allowed,
        limit: this.config.maxRequests,
        remaining,
        resetTime,
      };

      if (!allowed) {
        const retryAfter = Math.ceil(this.config.windowMs / 1000);
        return { ...result, retryAfter };
      }

      return result;
    } catch (error) {
      logger.error('Rate limit check failed', { key }, error as Error);
      // Fail open - allow request if rate limiting fails
      return {
        allowed: true,
        limit: this.config.maxRequests,
        remaining: this.config.maxRequests,
        resetTime,
      };
    }
  }

  async middleware(request: NextRequest): Promise<NextResponse | null> {
    const result = await this.checkLimit(request);

    // Add rate limit headers if enabled
    const headers: Record<string, string> = {};
    if (this.config.headers) {
      headers['X-RateLimit-Limit'] = result.limit.toString();
      headers['X-RateLimit-Remaining'] = result.remaining.toString();
      headers['X-RateLimit-Reset'] = new Date(result.resetTime).toISOString();
    }

    if (!result.allowed) {
      if (result.retryAfter) {
        headers['Retry-After'] = result.retryAfter.toString();
      }

      logger.warn('Rate limit exceeded', {
        key: this.config.keyGenerator(request),
        limit: result.limit,
        ip: request.headers.get('x-forwarded-for') || request.headers.get('x-real-ip') || 'unknown',
        userAgent: request.headers.get('user-agent') || 'unknown',
        url: request.url,
      });

      return NextResponse.json(
        {
          error: 'Rate Limit Exceeded',
          message: this.config.message,
          retryAfter: result.retryAfter,
        },
        {
          status: 429,
          headers,
        }
      );
    }

    // Return null to continue processing, but add headers to response later
    return null;
  }
}

// Predefined rate limiters for different use cases
export const rateLimiters = {
  // General API rate limiter
  api: new RateLimiter({
    windowMs: 60 * 1000, // 1 minute
    maxRequests: APP_CONSTANTS.RATE_LIMITS.API_REQUESTS_PER_MINUTE,
    message: 'Too many API requests, please try again later',
  }),

  // Strict rate limiter for authentication endpoints
  auth: new RateLimiter({
    windowMs: 15 * 60 * 1000, // 15 minutes
    maxRequests: 5,
    message: 'Too many authentication attempts, please try again later',
  }),

  // Rate limiter for AI analysis requests
  aiAnalysis: new RateLimiter({
    windowMs: 60 * 60 * 1000, // 1 hour
    maxRequests: APP_CONSTANTS.RATE_LIMITS.ANALYSIS_REQUESTS_PER_DAY / 24,
    message: 'AI analysis rate limit exceeded, please try again later',
    keyGenerator: (request) => {
      // Use user ID for authenticated requests
      const userId = request.headers.get('x-user-id');
      const ip = request.headers.get('x-forwarded-for') || 'unknown';
      return `ai_analysis:${userId || ip}`;
    },
  }),

  // Rate limiter for scraping requests
  scraping: new RateLimiter({
    windowMs: 60 * 60 * 1000, // 1 hour
    maxRequests: APP_CONSTANTS.RATE_LIMITS.SCRAPING_REQUESTS_PER_HOUR,
    message: 'Scraping rate limit exceeded, please try again later',
  }),

  // Rate limiter for file uploads
  upload: new RateLimiter({
    windowMs: 60 * 1000, // 1 minute
    maxRequests: 10,
    message: 'Upload rate limit exceeded, please try again later',
  }),
};

// Utility function to create custom rate limiter
export function createRateLimiter(config: RateLimitConfig): RateLimiter {
  return new RateLimiter(config);
}

// Utility function to apply rate limiting to API routes
export function withRateLimit(rateLimiter: RateLimiter) {
  return async (request: NextRequest, handler: () => Promise<NextResponse>): Promise<NextResponse> => {
    const rateLimitResponse = await rateLimiter.middleware(request);
    
    if (rateLimitResponse) {
      return rateLimitResponse;
    }

    try {
      const response = await handler();
      
      // Add rate limit headers to successful responses
      if (rateLimiter['config'].headers) {
        const result = await rateLimiter.checkLimit(request);
        response.headers.set('X-RateLimit-Limit', result.limit.toString());
        response.headers.set('X-RateLimit-Remaining', result.remaining.toString());
        response.headers.set('X-RateLimit-Reset', new Date(result.resetTime).toISOString());
      }
      
      return response;
    } catch (error) {
      logger.error('API handler error', {
        url: request.url,
        method: request.method,
      }, error as Error);
      throw error;
    }
  };
}

// Export types
export type { RateLimitConfig as RateLimiterConfig, RateLimitStore as RateLimiterStore };
