import {
  AppError,
  AuthenticationError,
  AuthorizationError,
  ValidationError,
  NotFoundError,
  RateLimitError,
  ExternalServiceError,
  ScrapingError,
  TimeoutError,
  NetworkError,
  RobotsBlockedError,
  AIServiceError,
  AIQuotaExceededError,
  AIInvalidResponseError,
  DatabaseError,
  StorageError,
  FileTooLargeError,
  ConfigurationError,
  BusinessLogicError,
  InsufficientCreditsError,
  SubscriptionRequiredError,
  isAppError,
  isOperationalError,
  createScrapingError,
  createAIError,
  logError
} from '../errors';

describe('Error Classes', () => {
  describe('AppError Base Class', () => {
    class TestError extends AppError {
      readonly statusCode = 500;
      readonly code = 'TEST_ERROR';
      readonly isOperational = true;
    }

    it('should create error with message and context', () => {
      const error = new TestError('Test error message', { key: 'value' });
      expect(error.message).toBe('Test error message');
      expect(error.context).toEqual({ key: 'value' });
      expect(error.name).toBe('TestError');
    });

    it('should serialize to JSON correctly', () => {
      const error = new TestError('Test error');
      const json = error.toJSON();
      expect(json).toMatchObject({
        name: 'TestError',
        message: 'Test error',
        code: 'TEST_ERROR',
        statusCode: 500
      });
    });
  });

  describe('Authentication Errors', () => {
    it('should create AuthenticationError with correct properties', () => {
      const error = new AuthenticationError();
      expect(error.statusCode).toBe(401);
      expect(error.code).toBe('AUTH_REQUIRED');
      expect(error.isOperational).toBe(true);
      expect(error.message).toBe('Authentication required');
    });

    it('should create AuthorizationError with correct properties', () => {
      const error = new AuthorizationError();
      expect(error.statusCode).toBe(403);
      expect(error.code).toBe('INSUFFICIENT_PERMISSIONS');
      expect(error.message).toBe('Insufficient permissions');
    });
  });

  describe('Validation Errors', () => {
    it('should create ValidationError with field errors', () => {
      const fieldErrors = {
        email: ['Invalid email format'],
        password: ['Too short', 'Must contain numbers']
      };
      const error = new ValidationError('Validation failed', fieldErrors);
      expect(error.statusCode).toBe(400);
      expect(error.errors).toEqual(fieldErrors);
    });

    it('should create NotFoundError with resource info', () => {
      const error = new NotFoundError('User', '123');
      expect(error.statusCode).toBe(404);
      expect(error.message).toBe("User with identifier '123' not found");
    });

    it('should create NotFoundError without identifier', () => {
      const error = new NotFoundError('Resource');
      expect(error.message).toBe('Resource not found');
    });
  });

  describe('Rate Limiting Errors', () => {
    it('should create RateLimitError with retry after', () => {
      const error = new RateLimitError('Too many requests', 60);
      expect(error.statusCode).toBe(429);
      expect(error.retryAfter).toBe(60);
    });
  });

  describe('Scraping Errors', () => {
    it('should create ScrapingError with URL and reason', () => {
      const originalError = new Error('Connection failed');
      const error = new ScrapingError('https://example.com', 'Network issue', originalError);
      expect(error.statusCode).toBe(422);
      expect(error.code).toBe('SCRAPING_ERROR');
      expect(error.message).toBe('Failed to scrape https://example.com: Network issue');
      expect(error.originalError).toBe(originalError);
    });

    it('should create TimeoutError', () => {
      const error = new TimeoutError('https://example.com', 30000);
      expect(error.message).toBe('Scraping timeout: Operation timed out after 30000ms for https://example.com');
    });

    it('should create NetworkError', () => {
      const error = new NetworkError('https://example.com', 'DNS lookup failed');
      expect(error.message).toBe('Network error for https://example.com: DNS lookup failed');
    });

    it('should create RobotsBlockedError', () => {
      const error = new RobotsBlockedError('https://example.com');
      expect(error.message).toBe('Scraping blocked by robots.txt for https://example.com');
    });
  });

  describe('AI Service Errors', () => {
    it('should create AIServiceError', () => {
      const originalError = new Error('API Error');
      const error = new AIServiceError('OpenAI', 'Rate limit exceeded', originalError);
      expect(error.statusCode).toBe(502);
      expect(error.message).toBe('OpenAI AI service error: Rate limit exceeded');
    });

    it('should create AIQuotaExceededError', () => {
      const error = new AIQuotaExceededError('Anthropic');
      expect(error.statusCode).toBe(429);
      expect(error.message).toBe('Anthropic API quota exceeded');
    });

    it('should create AIInvalidResponseError', () => {
      const error = new AIInvalidResponseError('OpenAI', { invalid: 'response' });
      expect(error.message).toBe('OpenAI returned invalid response format');
      expect(error.context).toEqual({ response: { invalid: 'response' } });
    });
  });

  describe('Storage Errors', () => {
    it('should create StorageError', () => {
      const error = new StorageError('upload', 'File not found');
      expect(error.message).toBe('Storage upload failed: File not found');
    });

    it('should create FileTooLargeError', () => {
      const error = new FileTooLargeError(1048576, 2097152);
      expect(error.statusCode).toBe(413);
      expect(error.message).toBe('File size 2097152 bytes exceeds maximum allowed size of 1048576 bytes');
    });
  });

  describe('Business Logic Errors', () => {
    it('should create InsufficientCreditsError', () => {
      const error = new InsufficientCreditsError(100, 50);
      expect(error.statusCode).toBe(402);
      expect(error.message).toBe('Insufficient credits: 100 required, 50 available');
    });

    it('should create SubscriptionRequiredError', () => {
      const error = new SubscriptionRequiredError('Advanced Analysis');
      expect(error.statusCode).toBe(402);
      expect(error.message).toBe('Advanced Analysis requires an active subscription');
    });
  });
});

describe('Error Type Guards', () => {
  it('should identify AppError instances', () => {
    const appError = new AuthenticationError();
    const regularError = new Error('Regular error');
    
    expect(isAppError(appError)).toBe(true);
    expect(isAppError(regularError)).toBe(false);
    expect(isAppError('string error')).toBe(false);
  });

  it('should identify operational errors', () => {
    const operationalError = new ValidationError('Test');
    const configError = new ConfigurationError('test', 'missing');
    
    expect(isOperationalError(operationalError)).toBe(true);
    expect(isOperationalError(configError)).toBe(false);
  });
});

describe('Error Factory Functions', () => {
  describe('createScrapingError', () => {
    it('should create TimeoutError for timeout messages', () => {
      const error = createScrapingError('https://example.com', new Error('Request timeout'));
      expect(error).toBeInstanceOf(TimeoutError);
    });

    it('should create NetworkError for network messages', () => {
      const error = createScrapingError('https://example.com', new Error('ENOTFOUND'));
      expect(error).toBeInstanceOf(NetworkError);
    });

    it('should create generic ScrapingError for other errors', () => {
      const error = createScrapingError('https://example.com', new Error('Unknown error'));
      expect(error).toBeInstanceOf(ScrapingError);
    });

    it('should handle non-Error inputs', () => {
      const error = createScrapingError('https://example.com', 'String error');
      expect(error).toBeInstanceOf(ScrapingError);
      expect(error.message).toContain('String error');
    });
  });

  describe('createAIError', () => {
    it('should create AIQuotaExceededError for quota messages', () => {
      const error = createAIError('OpenAI', new Error('Rate limit exceeded'));
      expect(error).toBeInstanceOf(AIQuotaExceededError);
    });

    it('should create AIInvalidResponseError for format errors', () => {
      const error = createAIError('Claude', new Error('Invalid response format'));
      expect(error).toBeInstanceOf(AIInvalidResponseError);
    });

    it('should create generic AIServiceError for other errors', () => {
      const error = createAIError('OpenAI', new Error('Service unavailable'));
      expect(error).toBeInstanceOf(AIServiceError);
    });
  });
});

describe('Error Logging', () => {
  let consoleWarnSpy: jest.SpyInstance;
  let consoleErrorSpy: jest.SpyInstance;

  beforeEach(() => {
    consoleWarnSpy = jest.spyOn(console, 'warn').mockImplementation();
    consoleErrorSpy = jest.spyOn(console, 'error').mockImplementation();
  });

  afterEach(() => {
    consoleWarnSpy.mockRestore();
    consoleErrorSpy.mockRestore();
  });

  it('should log operational errors as warnings', () => {
    const error = new ValidationError('Test error');
    logError(error, { extra: 'context' });
    
    expect(consoleWarnSpy).toHaveBeenCalledWith(
      'Operational error:',
      expect.objectContaining({
        error: expect.objectContaining({
          message: 'Test error',
          code: 'VALIDATION_ERROR'
        }),
        context: { extra: 'context' }
      })
    );
  });

  it('should log non-operational errors as errors', () => {
    const error = new ConfigurationError('database', 'Missing connection string');
    logError(error);
    
    expect(consoleErrorSpy).toHaveBeenCalledWith(
      'System error:',
      expect.objectContaining({
        error: expect.objectContaining({
          message: 'Configuration error for database: Missing connection string'
        })
      })
    );
  });

  it('should handle non-AppError instances', () => {
    const error = new Error('Regular error');
    logError(error);
    
    expect(consoleErrorSpy).toHaveBeenCalledWith(
      'System error:',
      expect.objectContaining({
        error: expect.objectContaining({
          name: 'Error',
          message: 'Regular error'
        })
      })
    );
  });
});
