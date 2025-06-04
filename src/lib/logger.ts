import { env } from '@/lib/env';
import { APP_CONSTANTS } from '@/lib/constants';

// Log levels
export enum LogLevel {
  ERROR = 'error',
  WARN = 'warn',
  INFO = 'info',
  DEBUG = 'debug',
}

// Log context interface
export interface LogContext {
  userId?: string;
  organizationId?: string;
  requestId?: string;
  sessionId?: string;
  userAgent?: string;
  ip?: string;
  method?: string;
  url?: string;
  statusCode?: number;
  duration?: number;
  [key: string]: any;
}

// Log entry interface
export interface LogEntry {
  timestamp: string;
  level: LogLevel;
  message: string;
  context?: LogContext;
  error?: {
    name: string;
    message: string;
    stack?: string;
    code?: string;
  };
  service: string;
  environment: string;
  version: string;
}

// Logger class
class Logger {
  private service: string;
  private environment: string;
  private version: string;

  constructor(service: string = 'brand-audit-api') {
    this.service = service;
    this.environment = env.NODE_ENV;
    this.version = APP_CONSTANTS.APP_VERSION;
  }

  private createLogEntry(
    level: LogLevel,
    message: string,
    context?: LogContext,
    error?: Error
  ): LogEntry {
    const entry: LogEntry = {
      timestamp: new Date().toISOString(),
      level,
      message,
      service: this.service,
      environment: this.environment,
      version: this.version,
    };

    if (context) {
      entry.context = context;
    }

    if (error) {
      entry.error = {
        name: error.name,
        message: error.message,
        ...(error.stack && { stack: error.stack }),
        ...((error as any).code && { code: (error as any).code }),
      };
    }

    return entry;
  }

  private shouldLog(level: LogLevel): boolean {
    const logLevels = [LogLevel.ERROR, LogLevel.WARN, LogLevel.INFO, LogLevel.DEBUG];
    const currentLevelIndex = logLevels.indexOf(this.getLogLevel());
    const messageLevelIndex = logLevels.indexOf(level);
    
    return messageLevelIndex <= currentLevelIndex;
  }

  private getLogLevel(): LogLevel {
    if (this.environment === 'production') {
      return LogLevel.INFO;
    } else if (this.environment === 'test') {
      return LogLevel.WARN;
    } else {
      return LogLevel.DEBUG;
    }
  }

  private output(entry: LogEntry): void {
    if (!this.shouldLog(entry.level)) {
      return;
    }

    const logString = JSON.stringify(entry, null, this.environment === 'development' ? 2 : 0);

    // In development, use console methods for better formatting
    if (this.environment === 'development') {
      switch (entry.level) {
        case LogLevel.ERROR:
          console.error(logString);
          break;
        case LogLevel.WARN:
          console.warn(logString);
          break;
        case LogLevel.INFO:
          console.info(logString);
          break;
        case LogLevel.DEBUG:
          console.debug(logString);
          break;
      }
    } else {
      // In production, use console.log for structured logging
      console.log(logString);
    }

    // Send to external logging service in production
    if (this.environment === 'production') {
      this.sendToExternalService(entry);
    }
  }

  private async sendToExternalService(entry: LogEntry): Promise<void> {
    // In a real implementation, you would send to services like:
    // - Datadog
    // - New Relic
    // - Elasticsearch
    // - CloudWatch
    // - Sentry (for errors)
    
    try {
      // Example: Send errors to Sentry
      if (entry.level === LogLevel.ERROR && env.SENTRY_DSN) {
        // Sentry.captureException would be called here
        // This is just a placeholder
      }

      // Example: Send to custom logging endpoint
      // await fetch('/api/internal/logs', {
      //   method: 'POST',
      //   headers: { 'Content-Type': 'application/json' },
      //   body: JSON.stringify(entry)
      // });
    } catch (error) {
      // Fallback to console if external service fails
      console.error('Failed to send log to external service:', error);
    }
  }

  // Public logging methods
  error(message: string, context?: LogContext, error?: Error): void {
    const entry = this.createLogEntry(LogLevel.ERROR, message, context, error);
    this.output(entry);
  }

  warn(message: string, context?: LogContext): void {
    const entry = this.createLogEntry(LogLevel.WARN, message, context);
    this.output(entry);
  }

  info(message: string, context?: LogContext): void {
    const entry = this.createLogEntry(LogLevel.INFO, message, context);
    this.output(entry);
  }

  debug(message: string, context?: LogContext): void {
    const entry = this.createLogEntry(LogLevel.DEBUG, message, context);
    this.output(entry);
  }

  // Specialized logging methods
  apiRequest(method: string, url: string, context?: LogContext): void {
    this.info(`API Request: ${method} ${url}`, {
      ...context,
      method,
      url,
      type: 'api_request',
    });
  }

  apiResponse(method: string, url: string, statusCode: number, duration: number, context?: LogContext): void {
    const level = statusCode >= 400 ? LogLevel.WARN : LogLevel.INFO;
    const entry = this.createLogEntry(
      level,
      `API Response: ${method} ${url} - ${statusCode} (${duration}ms)`,
      {
        ...context,
        method,
        url,
        statusCode,
        duration,
        type: 'api_response',
      }
    );
    this.output(entry);
  }

  databaseQuery(query: string, duration: number, context?: LogContext): void {
    this.debug(`Database Query: ${query} (${duration}ms)`, {
      ...context,
      query,
      duration,
      type: 'database_query',
    });
  }

  externalService(service: string, operation: string, duration: number, success: boolean, context?: LogContext): void {
    const level = success ? LogLevel.INFO : LogLevel.WARN;
    this.output(this.createLogEntry(
      level,
      `External Service: ${service}.${operation} - ${success ? 'SUCCESS' : 'FAILED'} (${duration}ms)`,
      {
        ...context,
        service,
        operation,
        duration,
        success,
        type: 'external_service',
      }
    ));
  }

  userAction(action: string, userId: string, context?: LogContext): void {
    this.info(`User Action: ${action}`, {
      ...context,
      userId,
      action,
      type: 'user_action',
    });
  }

  securityEvent(event: string, severity: 'low' | 'medium' | 'high' | 'critical', context?: LogContext): void {
    const level = severity === 'critical' || severity === 'high' ? LogLevel.ERROR : LogLevel.WARN;
    this.output(this.createLogEntry(
      level,
      `Security Event: ${event}`,
      {
        ...context,
        event,
        severity,
        type: 'security_event',
      }
    ));
  }

  performance(operation: string, duration: number, context?: LogContext): void {
    const level = duration > APP_CONSTANTS.MONITORING.ALERT_THRESHOLDS.RESPONSE_TIME_P95 
      ? LogLevel.WARN 
      : LogLevel.INFO;
    
    this.output(this.createLogEntry(
      level,
      `Performance: ${operation} took ${duration}ms`,
      {
        ...context,
        operation,
        duration,
        type: 'performance',
      }
    ));
  }

  // Create child logger with additional context
  child(additionalContext: LogContext): Logger {
    const childLogger = new Logger(this.service);
    
    // Override output method to include additional context
    const originalOutput = childLogger.output.bind(childLogger);
    childLogger.output = (entry: LogEntry) => {
      entry.context = { ...additionalContext, ...entry.context };
      originalOutput(entry);
    };
    
    return childLogger;
  }
}

// Create default logger instance
export const logger = new Logger();

// Create specialized loggers for different services
export const createLogger = (service: string) => new Logger(service);

// Utility functions for common logging patterns
export const logApiCall = async <T>(
  operation: string,
  fn: () => Promise<T>,
  context?: LogContext
): Promise<T> => {
  const start = Date.now();
  logger.info(`Starting ${operation}`, context);
  
  try {
    const result = await fn();
    const duration = Date.now() - start;
    logger.info(`Completed ${operation}`, { ...context, duration, success: true });
    return result;
  } catch (error) {
    const duration = Date.now() - start;
    logger.error(`Failed ${operation}`, { ...context, duration, success: false }, error as Error);
    throw error;
  }
};

export const logDatabaseOperation = async <T>(
  operation: string,
  query: string,
  fn: () => Promise<T>,
  context?: LogContext
): Promise<T> => {
  const start = Date.now();
  
  try {
    const result = await fn();
    const duration = Date.now() - start;
    logger.databaseQuery(query, duration, { ...context, operation });
    return result;
  } catch (error) {
    const duration = Date.now() - start;
    logger.error(`Database operation failed: ${operation}`, 
      { ...context, query, duration }, error as Error);
    throw error;
  }
};

// Export types
export type { LogContext as LoggerContext, LogEntry as LoggerEntry };
