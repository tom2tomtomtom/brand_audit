/**
 * In-memory caching layer for the Brand Audit Tool
 * 
 * Provides LRU (Least Recently Used) caching for expensive operations
 * like AI analyses, visual brand data, and database queries.
 * 
 * In production, this should be replaced with Redis for distributed caching.
 * 
 * @module CacheLayer
 */

import { LRUCache } from 'lru-cache';
import crypto from 'crypto';

/**
 * Cache configuration options
 */
export interface CacheConfig {
  /** Maximum number of items in cache */
  max: number;
  /** Maximum age in milliseconds */
  ttl: number;
  /** Update age on get */
  updateAgeOnGet?: boolean;
  /** Update age on has */
  updateAgeOnHas?: boolean;
}

/**
 * Cache statistics for monitoring
 */
export interface CacheStats {
  hits: number;
  misses: number;
  sets: number;
  deletes: number;
  hitRate: number;
  size: number;
  maxSize: number;
}

/**
 * Generic cache wrapper with TTL and LRU eviction
 * 
 * @class CacheManager
 * @template T - Type of cached values
 */
export class CacheManager<T = any> {
  private cache: LRUCache<string, T>;
  private stats = {
    hits: 0,
    misses: 0,
    sets: 0,
    deletes: 0,
  };

  constructor(config: CacheConfig) {
    this.cache = new LRUCache<string, T>({
      max: config.max,
      ttl: config.ttl,
      updateAgeOnGet: config.updateAgeOnGet ?? true,
      updateAgeOnHas: config.updateAgeOnHas ?? false,
    });
  }

  /**
   * Get value from cache
   * @param {string} key - Cache key
   * @returns {T | undefined} Cached value or undefined
   */
  get(key: string): T | undefined {
    const value = this.cache.get(key);
    if (value !== undefined) {
      this.stats.hits++;
    } else {
      this.stats.misses++;
    }
    return value;
  }

  /**
   * Set value in cache
   * @param {string} key - Cache key
   * @param {T} value - Value to cache
   * @param {number} [ttl] - Optional TTL override in milliseconds
   */
  set(key: string, value: T, ttl?: number): void {
    const options = ttl ? { ttl } : undefined;
    this.cache.set(key, value, options);
    this.stats.sets++;
  }

  /**
   * Check if key exists in cache
   * @param {string} key - Cache key
   * @returns {boolean} True if key exists
   */
  has(key: string): boolean {
    return this.cache.has(key);
  }

  /**
   * Delete key from cache
   * @param {string} key - Cache key
   * @returns {boolean} True if key was deleted
   */
  delete(key: string): boolean {
    const result = this.cache.delete(key);
    if (result) {
      this.stats.deletes++;
    }
    return result;
  }

  /**
   * Clear all cached values
   */
  clear(): void {
    this.cache.clear();
  }

  /**
   * Get cache statistics
   * @returns {CacheStats} Cache statistics
   */
  getStats(): CacheStats {
    const hitRate = this.stats.hits / (this.stats.hits + this.stats.misses) || 0;
    return {
      ...this.stats,
      hitRate: Math.round(hitRate * 100) / 100,
      size: this.cache.size,
      maxSize: this.cache.max,
    };
  }

  /**
   * Get or set value with async factory function
   * @param {string} key - Cache key
   * @param {() => Promise<T>} factory - Factory function to create value if not cached
   * @param {number} [ttl] - Optional TTL override
   * @returns {Promise<T>} Cached or newly created value
   */
  async getOrSet(key: string, factory: () => Promise<T>, ttl?: number): Promise<T> {
    const cached = this.get(key);
    if (cached !== undefined) {
      return cached;
    }

    const value = await factory();
    this.set(key, value, ttl);
    return value;
  }
}

/**
 * Create cache key from multiple parts
 * @param {...string} parts - Key parts
 * @returns {string} Combined cache key
 */
export function createCacheKey(...parts: string[]): string {
  return parts.join(':');
}

/**
 * Create hash-based cache key for complex objects
 * @param {any} obj - Object to hash
 * @returns {string} Hash-based cache key
 */
export function createHashKey(obj: any): string {
  const str = JSON.stringify(obj, Object.keys(obj).sort());
  return crypto.createHash('sha256').update(str).digest('hex').substring(0, 16);
}

// Singleton cache instances
let analysisCache: CacheManager | null = null;
let visualDataCache: CacheManager | null = null;
let queryCache: CacheManager | null = null;
let presentationCache: CacheManager | null = null;

/**
 * Get or create analysis cache instance
 * @returns {CacheManager} Analysis cache
 */
export function getAnalysisCache(): CacheManager {
  if (!analysisCache) {
    analysisCache = new CacheManager({
      max: 100,
      ttl: 1000 * 60 * 60, // 1 hour
    });
  }
  return analysisCache;
}

/**
 * Get or create visual data cache instance
 * @returns {CacheManager} Visual data cache
 */
export function getVisualDataCache(): CacheManager {
  if (!visualDataCache) {
    visualDataCache = new CacheManager({
      max: 200,
      ttl: 1000 * 60 * 60 * 24, // 24 hours
    });
  }
  return visualDataCache;
}

/**
 * Get or create query cache instance
 * @returns {CacheManager} Query cache
 */
export function getQueryCache(): CacheManager {
  if (!queryCache) {
    queryCache = new CacheManager({
      max: 500,
      ttl: 1000 * 60 * 5, // 5 minutes
    });
  }
  return queryCache;
}

/**
 * Get or create presentation cache instance
 * @returns {CacheManager} Presentation cache
 */
export function getPresentationCache(): CacheManager {
  if (!presentationCache) {
    presentationCache = new CacheManager({
      max: 50,
      ttl: 1000 * 60 * 30, // 30 minutes
    });
  }
  return presentationCache;
}

/**
 * Decorator for caching method results
 * 
 * @example
 * ```typescript
 * class MyService {
 *   @Cacheable({ ttl: 60000 })
 *   async expensiveOperation(param: string): Promise<Result> {
 *     // ... expensive computation
 *   }
 * }
 * ```
 */
export function Cacheable(options: { ttl?: number; keyPrefix?: string } = {}) {
  return function (
    target: any,
    propertyName: string,
    descriptor: PropertyDescriptor
  ) {
    const originalMethod = descriptor.value;
    const cache = new CacheManager({
      max: 100,
      ttl: options.ttl || 1000 * 60 * 5, // Default 5 minutes
    });

    descriptor.value = async function (...args: any[]) {
      const keyPrefix = options.keyPrefix || `${target.constructor.name}:${propertyName}`;
      const key = createCacheKey(keyPrefix, createHashKey(args));

      return cache.getOrSet(key, () => originalMethod.apply(this, args));
    };

    return descriptor;
  };
}

/**
 * Cache invalidation patterns
 */
export class CacheInvalidator {
  /**
   * Invalidate all caches for a specific brand
   * @param {string} brandId - Brand ID
   */
  static invalidateBrand(brandId: string): void {
    const patterns = [
      `brand:${brandId}`,
      `analysis:${brandId}`,
      `visual:${brandId}`,
    ];

    this.invalidatePatterns(patterns);
  }

  /**
   * Invalidate all caches for a specific project
   * @param {string} projectId - Project ID
   */
  static invalidateProject(projectId: string): void {
    const patterns = [
      `project:${projectId}`,
      `presentation:${projectId}`,
    ];

    this.invalidatePatterns(patterns);
  }

  /**
   * Invalidate caches matching patterns
   * @private
   * @param {string[]} patterns - Cache key patterns
   */
  private static invalidatePatterns(patterns: string[]): void {
    const caches = [
      getAnalysisCache(),
      getVisualDataCache(),
      getQueryCache(),
      getPresentationCache(),
    ];

    caches.forEach(cache => {
      // In a real implementation with Redis, we'd use pattern matching
      // For now, we'll clear the entire cache (not ideal for production)
      cache.clear();
    });
  }
}

/**
 * Cache warming utilities
 */
export class CacheWarmer {
  /**
   * Pre-warm caches for a project
   * @param {string} projectId - Project ID
   * @param {Function} dataLoader - Function to load project data
   */
  static async warmProjectCache(
    projectId: string,
    dataLoader: (projectId: string) => Promise<any>
  ): Promise<void> {
    const cache = getQueryCache();
    const key = createCacheKey('project', projectId);

    try {
      const data = await dataLoader(projectId);
      cache.set(key, data);
    } catch (error) {
      console.error('Cache warming failed:', error);
    }
  }

  /**
   * Pre-warm visual data caches for multiple brands
   * @param {string[]} brandIds - Array of brand IDs
   * @param {Function} dataLoader - Function to load visual data
   */
  static async warmVisualDataCache(
    brandIds: string[],
    dataLoader: (brandId: string) => Promise<any>
  ): Promise<void> {
    const cache = getVisualDataCache();

    await Promise.all(
      brandIds.map(async (brandId) => {
        const key = createCacheKey('visual', brandId);
        try {
          const data = await dataLoader(brandId);
          cache.set(key, data);
        } catch (error) {
          console.error(`Visual cache warming failed for ${brandId}:`, error);
        }
      })
    );
  }
}

/**
 * Export all cache statistics for monitoring
 * @returns {Record<string, CacheStats>} All cache statistics
 */
export function getAllCacheStats(): Record<string, CacheStats> {
  return {
    analysis: getAnalysisCache().getStats(),
    visualData: getVisualDataCache().getStats(),
    query: getQueryCache().getStats(),
    presentation: getPresentationCache().getStats(),
  };
}

// Future Redis implementation placeholder
export interface RedisConfig {
  url: string;
  password?: string;
  db?: number;
}

/**
 * Future Redis-based cache implementation
 * @todo Implement when Redis is added to infrastructure
 */
export class RedisCacheManager<T = any> {
  constructor(config: RedisConfig) {
    // TODO: Implement Redis-based caching
    console.warn('Redis caching not yet implemented, using in-memory cache');
  }
}
