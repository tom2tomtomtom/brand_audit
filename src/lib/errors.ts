// Base error class for application errors
export abstract class AppError extends Error {
  abstract readonly statusCode: number;
  abstract readonly code: string;
  abstract readonly isOperational: boolean;

  constructor(message: string, public readonly context?: Record<string, any>) {
    super(message);
    this.name = this.constructor.name;
    Error.captureStackTrace(this, this.constructor);
  }

  toJSON() {
    return {
      name: this.name,
      message: this.message,
      code: this.code,
      statusCode: this.statusCode,
      context: this.context,
      stack: this.stack,
    };
  }
}

// Authentication & Authorization Errors
export class AuthenticationError extends AppError {
  readonly statusCode = 401;
  readonly code = 'AUTH_REQUIRED';
  readonly isOperational = true;

  constructor(message = 'Authentication required') {
    super(message);
  }
}

export class AuthorizationError extends AppError {
  readonly statusCode = 403;
  readonly code = 'INSUFFICIENT_PERMISSIONS';
  readonly isOperational = true;

  constructor(message = 'Insufficient permissions') {
    super(message);
  }
}

// Validation Errors
export class ValidationError extends AppError {
  readonly statusCode = 400;
  readonly code = 'VALIDATION_ERROR';
  readonly isOperational = true;

  constructor(message: string, public readonly errors?: Record<string, string[]>) {
    super(message);
  }
}

export class NotFoundError extends AppError {
  readonly statusCode = 404;
  readonly code = 'RESOURCE_NOT_FOUND';
  readonly isOperational = true;

  constructor(resource: string, identifier?: string) {
    const message = identifier 
      ? `${resource} with identifier '${identifier}' not found`
      : `${resource} not found`;
    super(message);
  }
}

// Rate Limiting Errors
export class RateLimitError extends AppError {
  readonly statusCode = 429;
  readonly code = 'RATE_LIMIT_EXCEEDED';
  readonly isOperational = true;

  constructor(
    message = 'Rate limit exceeded',
    public readonly retryAfter?: number
  ) {
    super(message);
  }
}

// External Service Errors
export class ExternalServiceError extends AppError {
  readonly statusCode = 502;
  readonly code = 'EXTERNAL_SERVICE_ERROR';
  readonly isOperational = true;

  constructor(
    service: string,
    message: string,
    public readonly originalError?: Error
  ) {
    super(`${service} error: ${message}`);
  }
}

// Scraping Specific Errors
export class ScrapingError extends AppError {
  readonly statusCode = 422;
  readonly code = 'SCRAPING_ERROR';
  readonly isOperational = true;

  constructor(url: string, reason: string, public readonly originalError?: Error) {
    super(`Failed to scrape ${url}: ${reason}`);
  }
}

export class TimeoutError extends ScrapingError {
  readonly code = 'SCRAPING_TIMEOUT';

  constructor(url: string, timeout: number) {
    super(url, `Operation timed out after ${timeout}ms`);
  }
}

export class NetworkError extends ScrapingError {
  readonly code = 'NETWORK_ERROR';

  constructor(url: string, message: string) {
    super(url, `Network error: ${message}`);
  }
}

export class RobotsBlockedError extends ScrapingError {
  readonly code = 'ROBOTS_BLOCKED';

  constructor(url: string) {
    super(url, 'Scraping blocked by robots.txt');
  }
}

// AI Service Errors
export class AIServiceError extends ExternalServiceError {
  readonly code = 'AI_SERVICE_ERROR';

  constructor(provider: string, message: string, originalError?: Error) {
    super(provider, message, originalError);
  }
}

export class AIQuotaExceededError extends AIServiceError {
  readonly code = 'AI_QUOTA_EXCEEDED';

  constructor(provider: string) {
    super(provider, 'API quota exceeded');
  }
}

export class AIInvalidResponseError extends AIServiceError {
  readonly code = 'AI_INVALID_RESPONSE';

  constructor(provider: string, response: any) {
    super(provider, 'Invalid response format', new Error(JSON.stringify(response)));
  }
}

// Database Errors
export class DatabaseError extends AppError {
  readonly statusCode = 500;
  readonly code = 'DATABASE_ERROR';
  readonly isOperational = true;

  constructor(operation: string, message: string, originalError?: Error) {
    super(`Database ${operation} failed: ${message}`);
    this.context = { operation, originalError: originalError?.message };
  }
}

// File/Storage Errors
export class StorageError extends AppError {
  readonly statusCode = 500;
  readonly code = 'STORAGE_ERROR';
  readonly isOperational = true;

  constructor(operation: string, message: string) {
    super(`Storage ${operation} failed: ${message}`);
  }
}

export class FileTooLargeError extends AppError {
  readonly statusCode = 413;
  readonly code = 'FILE_TOO_LARGE';
  readonly isOperational = true;

  constructor(maxSize: number, actualSize: number) {
    super(`File size ${actualSize} bytes exceeds maximum allowed size of ${maxSize} bytes`);
  }
}

// Configuration Errors
export class ConfigurationError extends AppError {
  readonly statusCode = 500;
  readonly code = 'CONFIGURATION_ERROR';
  readonly isOperational = false;

  constructor(setting: string, message: string) {
    super(`Configuration error for ${setting}: ${message}`);
  }
}

// Business Logic Errors
export class BusinessLogicError extends AppError {
  readonly statusCode = 422;
  readonly code = 'BUSINESS_LOGIC_ERROR';
  readonly isOperational = true;

  constructor(message: string) {
    super(message);
  }
}

export class InsufficientCreditsError extends BusinessLogicError {
  readonly code = 'INSUFFICIENT_CREDITS';

  constructor(required: number, available: number) {
    super(`Insufficient credits: ${required} required, ${available} available`);
  }
}

export class SubscriptionRequiredError extends BusinessLogicError {
  readonly code = 'SUBSCRIPTION_REQUIRED';

  constructor(feature: string) {
    super(`${feature} requires an active subscription`);
  }
}

// Error type guards
export function isAppError(error: unknown): error is AppError {
  return error instanceof AppError;
}

export function isOperationalError(error: unknown): boolean {
  return isAppError(error) && error.isOperational;
}

// Error factory functions
export function createScrapingError(url: string, error: unknown): ScrapingError {
  if (error instanceof Error) {
    if (error.message.includes('timeout')) {
      return new TimeoutError(url, 30000);
    }
    if (error.message.includes('network') || error.message.includes('ENOTFOUND')) {
      return new NetworkError(url, error.message);
    }
    return new ScrapingError(url, error.message, error);
  }
  return new ScrapingError(url, String(error));
}

export function createAIError(provider: string, error: unknown): AIServiceError {
  if (error instanceof Error) {
    if (error.message.includes('quota') || error.message.includes('rate limit')) {
      return new AIQuotaExceededError(provider);
    }
    if (error.message.includes('invalid') || error.message.includes('format')) {
      return new AIInvalidResponseError(provider, error.message);
    }
    return new AIServiceError(provider, error.message, error);
  }
  return new AIServiceError(provider, String(error));
}

// Error logging utility
export function logError(error: unknown, context?: Record<string, any>) {
  const errorInfo = {
    timestamp: new Date().toISOString(),
    error: isAppError(error) ? error.toJSON() : {
      name: error instanceof Error ? error.name : 'Unknown',
      message: error instanceof Error ? error.message : String(error),
      stack: error instanceof Error ? error.stack : undefined,
    },
    context,
  };

  if (isOperationalError(error)) {
    console.warn('Operational error:', errorInfo);
  } else {
    console.error('System error:', errorInfo);
  }

  // In production, send to monitoring service
  if (process.env.NODE_ENV === 'production' && typeof window === 'undefined') {
    // Send to Sentry or other monitoring service
    // Sentry.captureException(error, { extra: context });
  }
}
