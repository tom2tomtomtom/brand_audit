/**
 * Query Optimizer
 * Optimizes database queries with batching, caching, and intelligent fetching
 */

import { createServerSupabase } from '@/lib/supabase-server';
import { CacheManager } from '@/lib/cache';

interface QueryOptions {
  cache?: boolean;
  cacheTime?: number;
  batch?: boolean;
  batchDelay?: number;
  select?: string;
}

interface BatchedQuery {
  table: string;
  filters: Record<string, any>;
  resolve: (data: any) => void;
  reject: (error: any) => void;
  options: QueryOptions;
}

export class QueryOptimizer {
  private cache: CacheManager;
  private batchQueue: Map<string, BatchedQuery[]>;
  private batchTimers: Map<string, NodeJS.Timeout>;
  private queryMetrics: Map<string, { count: number; totalTime: number }>;

  constructor() {
    this.cache = new CacheManager();
    this.batchQueue = new Map();
    this.batchTimers = new Map();
    this.queryMetrics = new Map();
  }

  /**
   * Execute optimized query with caching and batching
   */
  async query<T>(
    table: string,
    filters: Record<string, any> = {},
    options: QueryOptions = {}
  ): Promise<T> {
    const startTime = performance.now();

    try {
      // Check cache first
      if (options.cache) {
        const cacheKey = this.getCacheKey(table, filters, options.select);
        const cached = await this.cache.get<T>(cacheKey);
        if (cached) {
          this.recordMetric(table, performance.now() - startTime);
          return cached;
        }
      }

      // Handle batching
      if (options.batch) {
        return this.batchQuery<T>(table, filters, options);
      }

      // Execute single query
      const result = await this.executeQuery<T>(table, filters, options);

      // Cache result
      if (options.cache) {
        const cacheKey = this.getCacheKey(table, filters, options.select);
        await this.cache.set(cacheKey, result, options.cacheTime || 300);
      }

      this.recordMetric(table, performance.now() - startTime);
      return result;

    } catch (error) {
      this.recordMetric(table, performance.now() - startTime);
      throw error;
    }
  }

  /**
   * Execute optimized bulk query
   */
  async bulkQuery<T>(
    table: string,
    filtersList: Record<string, any>[],
    options: QueryOptions = {}
  ): Promise<T[]> {
    const startTime = performance.now();

    try {
      // Group by common filters
      const grouped = this.groupFilters(filtersList);
      const results: T[] = [];

      // Execute grouped queries in parallel
      const promises = grouped.map(group => 
        this.executeGroupedQuery<T>(table, group, options)
      );

      const groupedResults = await Promise.all(promises);
      groupedResults.forEach(result => results.push(...result));

      this.recordMetric(`${table}_bulk`, performance.now() - startTime);
      return results;

    } catch (error) {
      this.recordMetric(`${table}_bulk`, performance.now() - startTime);
      throw error;
    }
  }

  /**
   * Preload frequently accessed data
   */
  async preload(queries: Array<{ table: string; filters?: Record<string, any>; options?: QueryOptions }>) {
    const promises = queries.map(({ table, filters = {}, options = {} }) =>
      this.query(table, filters, { ...options, cache: true })
    );

    await Promise.all(promises);
  }

  /**
   * Get query performance metrics
   */
  getMetrics() {
    const metrics: Record<string, { avgTime: number; count: number }> = {};

    this.queryMetrics.forEach((value, key) => {
      metrics[key] = {
        avgTime: value.totalTime / value.count,
        count: value.count
      };
    });

    return metrics;
  }

  /**
   * Clear all caches
   */
  async clearCache() {
    await this.cache.clear();
  }

  // Private methods

  private async batchQuery<T>(
    table: string,
    filters: Record<string, any>,
    options: QueryOptions
  ): Promise<T> {
    return new Promise((resolve, reject) => {
      // Add to batch queue
      if (!this.batchQueue.has(table)) {
        this.batchQueue.set(table, []);
      }

      this.batchQueue.get(table)!.push({
        table,
        filters,
        resolve,
        reject,
        options
      });

      // Set up batch timer
      if (!this.batchTimers.has(table)) {
        const timer = setTimeout(() => {
          this.executeBatch(table);
        }, options.batchDelay || 50);

        this.batchTimers.set(table, timer);
      }
    });
  }

  private async executeBatch(table: string) {
    const batch = this.batchQueue.get(table);
    if (!batch || batch.length === 0) return;

    // Clear queue and timer
    this.batchQueue.delete(table);
    this.batchTimers.delete(table);

    try {
      // Group similar queries
      const groups = this.groupBatchedQueries(batch);

      // Execute each group
      for (const group of groups) {
        const results = await this.executeBatchGroup(table, group);
        
        // Resolve individual promises
        group.forEach((query, index) => {
          query.resolve(results[index]);
        });
      }
    } catch (error) {
      // Reject all promises in batch
      batch.forEach(query => query.reject(error));
    }
  }

  private groupBatchedQueries(queries: BatchedQuery[]): BatchedQuery[][] {
    const groups: Map<string, BatchedQuery[]> = new Map();

    queries.forEach(query => {
      const key = JSON.stringify(query.options.select || '*');
      if (!groups.has(key)) {
        groups.set(key, []);
      }
      groups.get(key)!.push(query);
    });

    return Array.from(groups.values());
  }

  private async executeBatchGroup(table: string, group: BatchedQuery[]): Promise<any[]> {
    const supabase = createServerSupabase();
    
    // Extract all unique filter values
    const filterKeys = new Set<string>();
    group.forEach(query => {
      Object.keys(query.filters).forEach(key => filterKeys.add(key));
    });

    // Build OR query
    let query = supabase.from(table).select(group[0].options.select || '*');

    if (filterKeys.size === 1 && group.every(q => Object.keys(q.filters).length === 1)) {
      // Simple case: single filter key with multiple values
      const filterKey = Array.from(filterKeys)[0];
      const values = group.map(q => q.filters[filterKey]);
      query = query.in(filterKey, values);
    } else {
      // Complex case: build OR conditions
      const orConditions = group.map(q => {
        return Object.entries(q.filters)
          .map(([key, value]) => `${key}.eq.${value}`)
          .join(',');
      }).join(',');
      
      query = query.or(orConditions);
    }

    const { data, error } = await query;
    if (error) throw error;

    // Map results back to original queries
    return group.map(query => {
      return data?.find(item => 
        Object.entries(query.filters).every(([key, value]) => item[key] === value)
      );
    });
  }

  private async executeQuery<T>(
    table: string,
    filters: Record<string, any>,
    options: QueryOptions
  ): Promise<T> {
    const supabase = createServerSupabase();
    let query = supabase.from(table).select(options.select || '*');

    // Apply filters
    Object.entries(filters).forEach(([key, value]) => {
      if (Array.isArray(value)) {
        query = query.in(key, value);
      } else if (value === null) {
        query = query.is(key, null);
      } else {
        query = query.eq(key, value);
      }
    });

    const { data, error } = await query;
    if (error) throw error;

    return data as T;
  }

  private async executeGroupedQuery<T>(
    table: string,
    filters: Record<string, any[]>,
    options: QueryOptions
  ): Promise<T[]> {
    const supabase = createServerSupabase();
    let query = supabase.from(table).select(options.select || '*');

    // Apply grouped filters
    Object.entries(filters).forEach(([key, values]) => {
      query = query.in(key, values);
    });

    const { data, error } = await query;
    if (error) throw error;

    return data as T[];
  }

  private groupFilters(filtersList: Record<string, any>[]): Record<string, any[]>[] {
    // Group filters by common keys
    const groups: Map<string, Record<string, any[]>> = new Map();

    filtersList.forEach(filters => {
      const key = Object.keys(filters).sort().join(',');
      
      if (!groups.has(key)) {
        const grouped: Record<string, any[]> = {};
        Object.keys(filters).forEach(k => grouped[k] = []);
        groups.set(key, grouped);
      }

      const group = groups.get(key)!;
      Object.entries(filters).forEach(([k, v]) => {
        if (!group[k].includes(v)) {
          group[k].push(v);
        }
      });
    });

    return Array.from(groups.values());
  }

  private getCacheKey(table: string, filters: Record<string, any>, select?: string): string {
    return `query:${table}:${JSON.stringify(filters)}:${select || '*'}`;
  }

  private recordMetric(table: string, time: number) {
    if (!this.queryMetrics.has(table)) {
      this.queryMetrics.set(table, { count: 0, totalTime: 0 });
    }

    const metric = this.queryMetrics.get(table)!;
    metric.count++;
    metric.totalTime += time;
  }
}

// Export singleton instance
export const queryOptimizer = new QueryOptimizer();
