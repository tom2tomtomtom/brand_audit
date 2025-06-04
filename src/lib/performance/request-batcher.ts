/**
 * Request Batcher
 * Batches multiple API requests to reduce network overhead
 */

interface BatchRequest {
  id: string;
  method: string;
  url: string;
  data?: any;
  headers?: Record<string, string>;
  resolve: (data: any) => void;
  reject: (error: any) => void;
  timestamp: number;
  retries: number;
}

interface BatchConfig {
  maxBatchSize: number;
  batchDelay: number;
  maxRetries: number;
  retryDelay: number;
  enableCompression: boolean;
}

export class RequestBatcher {
  private queue: Map<string, BatchRequest[]> = new Map();
  private timers: Map<string, NodeJS.Timeout> = new Map();
  private config: BatchConfig;
  private metrics: {
    totalRequests: number;
    batchedRequests: number;
    failedRequests: number;
    averageBatchSize: number;
  } = {
    totalRequests: 0,
    batchedRequests: 0,
    failedRequests: 0,
    averageBatchSize: 0,
  };

  constructor(config: Partial<BatchConfig> = {}) {
    this.config = {
      maxBatchSize: 50,
      batchDelay: 50,
      maxRetries: 3,
      retryDelay: 1000,
      enableCompression: true,
      ...config,
    };
  }

  /**
   * Add a request to the batch queue
   */
  async request<T>(
    method: string,
    url: string,
    data?: any,
    headers?: Record<string, string>
  ): Promise<T> {
    return new Promise((resolve, reject) => {
      const request: BatchRequest = {
        id: this.generateId(),
        method,
        url,
        data,
        headers: headers || {},
        resolve,
        reject,
        timestamp: Date.now(),
        retries: 0,
      };

      this.enqueueRequest(request);
      this.metrics.totalRequests++;
    });
  }

  /**
   * Execute a batch of requests immediately
   */
  async flush(endpoint?: string) {
    if (endpoint) {
      const batch = this.queue.get(endpoint);
      if (batch && batch.length > 0) {
        clearTimeout(this.timers.get(endpoint));
        this.timers.delete(endpoint);
        await this.executeBatch(endpoint, batch);
      }
    } else {
      // Flush all endpoints
      const promises: Promise<void>[] = [];
      this.queue.forEach((batch, endpoint) => {
        if (batch.length > 0) {
          clearTimeout(this.timers.get(endpoint));
          this.timers.delete(endpoint);
          promises.push(this.executeBatch(endpoint, batch));
        }
      });
      await Promise.all(promises);
    }
  }

  /**
   * Get batching metrics
   */
  getMetrics() {
    return {
      ...this.metrics,
      currentQueueSize: Array.from(this.queue.values()).reduce(
        (sum, batch) => sum + batch.length,
        0
      ),
      endpoints: Array.from(this.queue.keys()),
    };
  }

  /**
   * Clear all pending requests
   */
  clear() {
    this.timers.forEach(timer => clearTimeout(timer));
    this.queue.clear();
    this.timers.clear();
  }

  // Private methods

  private enqueueRequest(request: BatchRequest) {
    const endpoint = this.getEndpoint(request.url);
    
    if (!this.queue.has(endpoint)) {
      this.queue.set(endpoint, []);
    }

    const batch = this.queue.get(endpoint)!;
    batch.push(request);

    // Execute immediately if batch is full
    if (batch.length >= this.config.maxBatchSize) {
      clearTimeout(this.timers.get(endpoint));
      this.timers.delete(endpoint);
      this.executeBatch(endpoint, batch);
      return;
    }

    // Set up batch timer if not exists
    if (!this.timers.has(endpoint)) {
      const timer = setTimeout(() => {
        const currentBatch = this.queue.get(endpoint);
        if (currentBatch && currentBatch.length > 0) {
          this.executeBatch(endpoint, currentBatch);
        }
      }, this.config.batchDelay);

      this.timers.set(endpoint, timer);
    }
  }

  private async executeBatch(endpoint: string, batch: BatchRequest[]) {
    this.queue.set(endpoint, []);
    this.timers.delete(endpoint);

    try {
      // Update metrics
      this.metrics.batchedRequests += batch.length;
      this.metrics.averageBatchSize =
        (this.metrics.averageBatchSize * (this.metrics.batchedRequests - batch.length) +
          batch.length * batch.length) /
        this.metrics.batchedRequests;

      // Prepare batch request
      const batchPayload = {
        requests: batch.map(req => ({
          id: req.id,
          method: req.method,
          path: this.getPath(req.url),
          data: req.data,
          headers: req.headers,
        })),
      };

      // Send batch request
      const response = await fetch(`${endpoint}/batch`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-Batch-Count': batch.length.toString(),
          ...(this.config.enableCompression && {
            'Accept-Encoding': 'gzip, deflate, br',
            'Content-Encoding': 'gzip',
          }),
        },
        body: JSON.stringify(batchPayload),
      });

      if (!response.ok) {
        throw new Error(`Batch request failed: ${response.statusText}`);
      }

      const results = await response.json();

      // Process results
      batch.forEach(request => {
        const result = results.find((r: any) => r.id === request.id);
        if (result) {
          if (result.success) {
            request.resolve(result.data);
          } else {
            request.reject(new Error(result.error || 'Request failed'));
            this.metrics.failedRequests++;
          }
        } else {
          request.reject(new Error('No result found for request'));
          this.metrics.failedRequests++;
        }
      });
    } catch (error) {
      // Handle batch failure
      this.handleBatchError(batch, error as Error);
    }
  }

  private handleBatchError(batch: BatchRequest[], error: Error) {
    batch.forEach(request => {
      if (request.retries < this.config.maxRetries) {
        // Retry individual requests
        request.retries++;
        setTimeout(() => {
          this.enqueueRequest(request);
        }, this.config.retryDelay * request.retries);
      } else {
        // Final failure
        request.reject(error);
        this.metrics.failedRequests++;
      }
    });
  }

  private getEndpoint(url: string): string {
    const urlObj = new URL(url);
    return `${urlObj.protocol}//${urlObj.host}`;
  }

  private getPath(url: string): string {
    const urlObj = new URL(url);
    return urlObj.pathname + urlObj.search;
  }

  private generateId(): string {
    return `req-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
  }
}

// API-specific batchers
export class APIBatcher {
  private batchers: Map<string, RequestBatcher> = new Map();
  private defaultConfig: Partial<BatchConfig> = {
    maxBatchSize: 25,
    batchDelay: 50,
    maxRetries: 3,
    retryDelay: 1000,
  };

  /**
   * Get or create a batcher for a specific API
   */
  getBatcher(apiName: string, config?: Partial<BatchConfig>): RequestBatcher {
    if (!this.batchers.has(apiName)) {
      this.batchers.set(
        apiName,
        new RequestBatcher({ ...this.defaultConfig, ...config })
      );
    }
    return this.batchers.get(apiName)!;
  }

  /**
   * Batch Supabase queries
   */
  async batchSupabase<T>(
    queries: Array<{
      table: string;
      method: 'select' | 'insert' | 'update' | 'delete';
      params?: any;
    }>
  ): Promise<T[]> {
    const batcher = this.getBatcher('supabase');
    
    const promises = queries.map(query => {
      const url = `/api/supabase/${query.table}`;
      return batcher.request<T>(query.method, url, query.params);
    });

    return Promise.all(promises);
  }

  /**
   * Batch OpenAI requests
   */
  async batchOpenAI<T>(
    requests: Array<{
      model: string;
      messages: any[];
      options?: any;
    }>
  ): Promise<T[]> {
    const batcher = this.getBatcher('openai', {
      maxBatchSize: 10, // OpenAI has stricter limits
      batchDelay: 100,
    });

    const promises = requests.map(request => {
      return batcher.request<T>('POST', '/api/openai/chat', request);
    });

    return Promise.all(promises);
  }

  /**
   * Batch scraping requests
   */
  async batchScrape<T>(
    urls: string[],
    options: any = {}
  ): Promise<T[]> {
    const batcher = this.getBatcher('scraper', {
      maxBatchSize: 5, // Scraping is resource-intensive
      batchDelay: 200,
    });

    const promises = urls.map(url => {
      return batcher.request<T>('POST', '/api/scraper/batch', { url, ...options });
    });

    return Promise.all(promises);
  }

  /**
   * Get metrics for all batchers
   */
  getAllMetrics() {
    const metrics: Record<string, any> = {};
    this.batchers.forEach((batcher, name) => {
      metrics[name] = batcher.getMetrics();
    });
    return metrics;
  }

  /**
   * Flush all batchers
   */
  async flushAll() {
    const promises = Array.from(this.batchers.values()).map(batcher =>
      batcher.flush()
    );
    await Promise.all(promises);
  }
}

// Singleton instance
export const apiBatcher = new APIBatcher();

// React hook for batched requests
import { useCallback } from 'react';

export function useBatchedRequest(apiName: string, config?: Partial<BatchConfig>) {
  const batcher = apiBatcher.getBatcher(apiName, config);

  const request = useCallback(
    async <T>(
      method: string,
      url: string,
      data?: any,
      headers?: Record<string, string>
    ): Promise<T> => {
      return batcher.request<T>(method, url, data, headers);
    },
    [batcher]
  );

  const flush = useCallback(async () => {
    await batcher.flush();
  }, [batcher]);

  const getMetrics = useCallback(() => {
    return batcher.getMetrics();
  }, [batcher]);

  return { request, flush, getMetrics };
}

// Utility function for batch operations
export async function batchOperation<T, R>(
  items: T[],
  operation: (batch: T[]) => Promise<R[]>,
  batchSize = 10
): Promise<R[]> {
  const results: R[] = [];
  
  for (let i = 0; i < items.length; i += batchSize) {
    const batch = items.slice(i, i + batchSize);
    const batchResults = await operation(batch);
    results.push(...batchResults);
  }
  
  return results;
}
