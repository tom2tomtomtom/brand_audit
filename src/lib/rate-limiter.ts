interface RateLimitConfig {
  maxRequests: number;
  windowMs: number;
  keyGenerator?: (identifier: string) => string;
}

interface RateLimitEntry {
  count: number;
  resetTime: number;
}

class RateLimiter {
  private store = new Map<string, RateLimitEntry>();
  private config: RateLimitConfig;

  constructor(config: RateLimitConfig) {
    this.config = config;
    
    // Clean up expired entries every minute
    setInterval(() => {
      this.cleanup();
    }, 60000);
  }

  async checkLimit(identifier: string): Promise<{
    allowed: boolean;
    remaining: number;
    resetTime: number;
  }> {
    const key = this.config.keyGenerator ? this.config.keyGenerator(identifier) : identifier;
    const now = Date.now();
    
    let entry = this.store.get(key);
    
    if (!entry || now >= entry.resetTime) {
      // Create new entry or reset expired entry
      entry = {
        count: 0,
        resetTime: now + this.config.windowMs,
      };
    }
    
    entry.count++;
    this.store.set(key, entry);
    
    const allowed = entry.count <= this.config.maxRequests;
    const remaining = Math.max(0, this.config.maxRequests - entry.count);
    
    return {
      allowed,
      remaining,
      resetTime: entry.resetTime,
    };
  }

  private cleanup(): void {
    const now = Date.now();
    for (const [key, entry] of this.store.entries()) {
      if (now >= entry.resetTime) {
        this.store.delete(key);
      }
    }
  }
}

// Rate limiters for different services
export const openaiRateLimiter = new RateLimiter({
  maxRequests: 50, // 50 requests per hour per user
  windowMs: 60 * 60 * 1000, // 1 hour
});

export const anthropicRateLimiter = new RateLimiter({
  maxRequests: 30, // 30 requests per hour per user
  windowMs: 60 * 60 * 1000, // 1 hour
});

export const scrapingRateLimiter = new RateLimiter({
  maxRequests: 20, // 20 scraping jobs per hour per user
  windowMs: 60 * 60 * 1000, // 1 hour
});

export const presentationRateLimiter = new RateLimiter({
  maxRequests: 10, // 10 presentations per hour per user
  windowMs: 60 * 60 * 1000, // 1 hour
});

// Helper function to check rate limit and throw error if exceeded
export async function checkRateLimit(
  limiter: RateLimiter, 
  identifier: string, 
  action: string
): Promise<void> {
  const result = await limiter.checkLimit(identifier);
  
  if (!result.allowed) {
    const resetDate = new Date(result.resetTime);
    throw new Error(
      `Rate limit exceeded for ${action}. Try again after ${resetDate.toLocaleTimeString()}`
    );
  }
}

// Cost tracking for API usage
interface CostTracker {
  openaiTokens: number;
  anthropicTokens: number;
  estimatedCost: number;
  lastReset: number;
}

class CostTrackingService {
  private store = new Map<string, CostTracker>();
  
  // Estimated costs per 1K tokens (approximate)
  private readonly OPENAI_COST_PER_1K = 0.002; // $0.002 per 1K tokens for GPT-4
  private readonly ANTHROPIC_COST_PER_1K = 0.008; // $0.008 per 1K tokens for Claude

  trackOpenAIUsage(userId: string, tokens: number): void {
    this.updateUsage(userId, tokens, 0);
  }

  trackAnthropicUsage(userId: string, tokens: number): void {
    this.updateUsage(userId, 0, tokens);
  }

  private updateUsage(userId: string, openaiTokens: number, anthropicTokens: number): void {
    const now = Date.now();
    const monthStart = new Date(new Date().getFullYear(), new Date().getMonth(), 1).getTime();
    
    let tracker = this.store.get(userId);
    
    if (!tracker || tracker.lastReset < monthStart) {
      // Reset monthly usage
      tracker = {
        openaiTokens: 0,
        anthropicTokens: 0,
        estimatedCost: 0,
        lastReset: now,
      };
    }
    
    tracker.openaiTokens += openaiTokens;
    tracker.anthropicTokens += anthropicTokens;
    tracker.estimatedCost = 
      (tracker.openaiTokens / 1000) * this.OPENAI_COST_PER_1K +
      (tracker.anthropicTokens / 1000) * this.ANTHROPIC_COST_PER_1K;
    
    this.store.set(userId, tracker);
  }

  getUsage(userId: string): CostTracker | null {
    return this.store.get(userId) || null;
  }

  checkCostLimit(userId: string, maxMonthlyCost: number = 50): boolean {
    const usage = this.getUsage(userId);
    return !usage || usage.estimatedCost < maxMonthlyCost;
  }
}

export const costTracker = new CostTrackingService();

// Error handling utilities
export class APIError extends Error {
  constructor(
    message: string,
    public statusCode: number = 500,
    public code?: string
  ) {
    super(message);
    this.name = 'APIError';
  }
}

export function handleAPIError(error: any): APIError {
  if (error instanceof APIError) {
    return error;
  }

  // OpenAI errors
  if (error.status) {
    switch (error.status) {
      case 401:
        return new APIError('Invalid API key', 401, 'INVALID_API_KEY');
      case 429:
        return new APIError('Rate limit exceeded', 429, 'RATE_LIMIT_EXCEEDED');
      case 500:
        return new APIError('OpenAI service error', 500, 'SERVICE_ERROR');
      default:
        return new APIError(`API error: ${error.message}`, error.status);
    }
  }

  // Anthropic errors
  if (error.error?.type) {
    switch (error.error.type) {
      case 'authentication_error':
        return new APIError('Invalid Anthropic API key', 401, 'INVALID_API_KEY');
      case 'rate_limit_error':
        return new APIError('Anthropic rate limit exceeded', 429, 'RATE_LIMIT_EXCEEDED');
      case 'api_error':
        return new APIError('Anthropic service error', 500, 'SERVICE_ERROR');
      default:
        return new APIError(`Anthropic error: ${error.error.message}`, 500);
    }
  }

  // Generic errors
  return new APIError(error.message || 'Unknown error occurred', 500);
}

// Retry logic with exponential backoff
export async function retryWithBackoff<T>(
  fn: () => Promise<T>,
  maxRetries: number = 3,
  baseDelay: number = 1000
): Promise<T> {
  let lastError: Error;

  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    try {
      return await fn();
    } catch (error) {
      lastError = error as Error;
      
      // Don't retry on authentication errors or client errors
      if (error instanceof APIError && error.statusCode < 500) {
        throw error;
      }
      
      if (attempt === maxRetries) {
        break;
      }
      
      // Exponential backoff with jitter
      const delay = baseDelay * Math.pow(2, attempt) + Math.random() * 1000;
      await new Promise(resolve => setTimeout(resolve, delay));
    }
  }

  throw lastError!;
}
