/**
 * Performance Monitor
 * Comprehensive performance tracking and reporting system
 */

interface PerformanceMetric {
  name: string;
  value: number;
  unit: string;
  timestamp: number;
  tags?: Record<string, string>;
}

interface PerformanceReport {
  timestamp: number;
  duration: number;
  metrics: {
    // Core Web Vitals
    lcp?: number; // Largest Contentful Paint
    fid?: number; // First Input Delay
    cls?: number; // Cumulative Layout Shift
    fcp?: number; // First Contentful Paint
    ttfb?: number; // Time to First Byte
    
    // Custom metrics
    apiResponseTime?: Record<string, number>;
    databaseQueryTime?: Record<string, number>;
    cacheHitRate?: number;
    memoryUsage?: number;
    cpuUsage?: number;
    bundleSize?: number;
    renderTime?: Record<string, number>;
  };
  errors: Array<{
    type: string;
    message: string;
    stack?: string;
    timestamp: number;
  }>;
}

export class PerformanceMonitor {
  private metrics: Map<string, PerformanceMetric[]> = new Map();
  private observers: Map<string, PerformanceObserver> = new Map();
  private startTime: number;
  private errorCount = 0;
  private slowQueries: Array<{ query: string; duration: number; timestamp: number }> = [];

  constructor() {
    this.startTime = performance.now();
    this.initializeObservers();
    this.setupErrorTracking();
  }

  /**
   * Initialize performance observers
   */
  private initializeObservers() {
    // Navigation timing
    if (typeof window !== 'undefined' && 'PerformanceObserver' in window) {
      // LCP Observer
      const lcpObserver = new PerformanceObserver((list) => {
        const entries = list.getEntries();
        const lastEntry = entries[entries.length - 1] as any;
        this.recordMetric('lcp', lastEntry.renderTime || lastEntry.loadTime, 'ms');
      });
      lcpObserver.observe({ entryTypes: ['largest-contentful-paint'] });
      this.observers.set('lcp', lcpObserver);

      // FID Observer
      const fidObserver = new PerformanceObserver((list) => {
        list.getEntries().forEach((entry: any) => {
          this.recordMetric('fid', entry.processingStart - entry.startTime, 'ms');
        });
      });
      fidObserver.observe({ entryTypes: ['first-input'] });
      this.observers.set('fid', fidObserver);

      // CLS Observer
      let clsValue = 0;
      const clsObserver = new PerformanceObserver((list) => {
        list.getEntries().forEach((entry: any) => {
          if (!entry.hadRecentInput) {
            clsValue += entry.value;
            this.recordMetric('cls', clsValue, 'score');
          }
        });
      });
      clsObserver.observe({ entryTypes: ['layout-shift'] });
      this.observers.set('cls', clsObserver);
    }
  }

  /**
   * Setup error tracking
   */
  private setupErrorTracking() {
    if (typeof window !== 'undefined') {
      window.addEventListener('error', (event) => {
        this.errorCount++;
        this.recordError({
          type: 'javascript',
          message: event.message,
          stack: event.error?.stack,
          timestamp: Date.now(),
        });
      });

      window.addEventListener('unhandledrejection', (event) => {
        this.errorCount++;
        this.recordError({
          type: 'promise',
          message: event.reason?.message || String(event.reason),
          stack: event.reason?.stack,
          timestamp: Date.now(),
        });
      });
    }
  }

  /**
   * Record a performance metric
   */
  recordMetric(name: string, value: number, unit = 'ms', tags?: Record<string, string>) {
    const metric: PerformanceMetric = {
      name,
      value,
      unit,
      timestamp: Date.now(),
      tags: tags || {},
    };

    if (!this.metrics.has(name)) {
      this.metrics.set(name, []);
    }
    this.metrics.get(name)!.push(metric);

    // Track slow operations
    if (unit === 'ms' && value > 1000) {
      this.slowQueries.push({
        query: name,
        duration: value,
        timestamp: Date.now(),
      });
    }
  }

  /**
   * Record an error
   */
  private recordError(error: any) {
    if (!this.metrics.has('errors')) {
      this.metrics.set('errors', []);
    }
    this.metrics.get('errors')!.push(error);
  }

  /**
   * Start timing an operation
   */
  startTimer(name: string): () => void {
    const startTime = performance.now();
    return () => {
      const duration = performance.now() - startTime;
      this.recordMetric(name, duration, 'ms');
      return duration;
    };
  }

  /**
   * Measure async operation
   */
  async measure<T>(name: string, operation: () => Promise<T>): Promise<T> {
    const endTimer = this.startTimer(name);
    try {
      const result = await operation();
      endTimer();
      return result;
    } catch (error) {
      endTimer();
      throw error;
    }
  }

  /**
   * Get performance report
   */
  getReport(): PerformanceReport {
    const duration = performance.now() - this.startTime;
    const report: PerformanceReport = {
      timestamp: Date.now(),
      duration,
      metrics: {},
      errors: [],
    };

    // Calculate averages for metrics
    this.metrics.forEach((values, name) => {
      if (name === 'errors') {
        report.errors = values as any;
      } else {
        const avg = values.reduce((sum, m) => sum + m.value, 0) / values.length;
        
        // Map to appropriate metric category
        if (['lcp', 'fid', 'cls', 'fcp', 'ttfb'].includes(name)) {
          (report.metrics as any)[name] = avg;
        } else if (name.startsWith('api_')) {
          if (!report.metrics.apiResponseTime) {
            report.metrics.apiResponseTime = {};
          }
          report.metrics.apiResponseTime[name.replace('api_', '')] = avg;
        } else if (name.startsWith('db_')) {
          if (!report.metrics.databaseQueryTime) {
            report.metrics.databaseQueryTime = {};
          }
          report.metrics.databaseQueryTime[name.replace('db_', '')] = avg;
        } else if (name.startsWith('render_')) {
          if (!report.metrics.renderTime) {
            report.metrics.renderTime = {};
          }
          report.metrics.renderTime[name.replace('render_', '')] = avg;
        }
      }
    });

    // Add system metrics
    if (typeof window !== 'undefined' && 'performance' in window) {
      const memory = (performance as any).memory;
      if (memory) {
        report.metrics.memoryUsage = memory.usedJSHeapSize / 1048576; // MB
      }
    }

    return report;
  }

  /**
   * Get performance score (0-100)
   */
  getPerformanceScore(): number {
    const report = this.getReport();
    let score = 100;

    // Core Web Vitals scoring
    if (report.metrics.lcp) {
      if (report.metrics.lcp > 4000) score -= 30;
      else if (report.metrics.lcp > 2500) score -= 15;
    }

    if (report.metrics.fid) {
      if (report.metrics.fid > 300) score -= 20;
      else if (report.metrics.fid > 100) score -= 10;
    }

    if (report.metrics.cls) {
      if (report.metrics.cls > 0.25) score -= 20;
      else if (report.metrics.cls > 0.1) score -= 10;
    }

    // Error rate
    const errorRate = this.errorCount / (report.duration / 1000); // errors per second
    if (errorRate > 1) score -= 20;
    else if (errorRate > 0.1) score -= 10;

    // Slow queries
    if (this.slowQueries.length > 10) score -= 10;
    else if (this.slowQueries.length > 5) score -= 5;

    return Math.max(0, score);
  }

  /**
   * Send metrics to analytics
   */
  async sendMetrics(endpoint: string) {
    const report = this.getReport();
    
    try {
      await fetch(endpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(report),
      });
    } catch (error) {
      console.error('Failed to send metrics:', error);
    }
  }

  /**
   * Reset all metrics
   */
  reset() {
    this.metrics.clear();
    this.errorCount = 0;
    this.slowQueries = [];
    this.startTime = performance.now();
  }

  /**
   * Cleanup observers
   */
  cleanup() {
    this.observers.forEach(observer => observer.disconnect());
    this.observers.clear();
  }
}

// Singleton instance
export const performanceMonitor = new PerformanceMonitor();

// React hooks for performance monitoring
import { useEffect, useCallback } from 'react';

export function usePerformanceMonitor() {
  useEffect(() => {
    return () => {
      performanceMonitor.cleanup();
    };
  }, []);

  const recordMetric = useCallback((name: string, value: number, unit?: string) => {
    performanceMonitor.recordMetric(name, value, unit);
  }, []);

  const startTimer = useCallback((name: string) => {
    return performanceMonitor.startTimer(name);
  }, []);

  const measure = useCallback(async <T,>(name: string, operation: () => Promise<T>) => {
    return performanceMonitor.measure(name, operation);
  }, []);

  const getReport = useCallback(() => {
    return performanceMonitor.getReport();
  }, []);

  const getScore = useCallback(() => {
    return performanceMonitor.getPerformanceScore();
  }, []);

  return {
    recordMetric,
    startTimer,
    measure,
    getReport,
    getScore,
  };
}

// Component render time tracking
export function useRenderTime(componentName: string) {
  useEffect(() => {
    const endTimer = performanceMonitor.startTimer(`render_${componentName}`);
    return () => {
      endTimer();
    };
  }, [componentName]);
}

// API call tracking
export function trackAPICall(endpoint: string) {
  return async <T,>(operation: () => Promise<T>): Promise<T> => {
    return performanceMonitor.measure(`api_${endpoint}`, operation);
  };
}

// Database query tracking
export function trackDatabaseQuery(queryName: string) {
  return async <T,>(operation: () => Promise<T>): Promise<T> => {
    return performanceMonitor.measure(`db_${queryName}`, operation);
  };
}

// Performance context provider
import React, { createContext, useContext } from 'react';

const PerformanceContext = createContext<PerformanceMonitor | null>(null);

export function PerformanceProvider({ children }: { children: React.ReactNode }) {
  return (
    <PerformanceContext.Provider value={performanceMonitor}>
      {children}
    </PerformanceContext.Provider>
  );
}

export function usePerformanceContext() {
  const context = useContext(PerformanceContext);
  if (!context) {
    throw new Error('usePerformanceContext must be used within PerformanceProvider');
  }
  return context;
}
