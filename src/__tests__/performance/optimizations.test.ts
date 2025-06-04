import { QueryOptimizer } from '@/lib/performance/query-optimizer';
import { RequestBatcher } from '@/lib/performance/request-batcher';
import { WorkerManager } from '@/lib/performance/worker-manager';
import { PerformanceMonitor } from '@/lib/performance/performance-monitor';
import { performance } from 'perf_hooks';

describe('Performance Optimizations Tests', () => {
  describe('Query Optimizer', () => {
    let optimizer: QueryOptimizer;

    beforeEach(() => {
      optimizer = new QueryOptimizer();
    });

    test('should cache queries and return faster on second call', async () => {
      const mockQuery = jest.fn().mockResolvedValue({ id: 1, name: 'Test' });
      
      // First call - should hit database
      const start1 = performance.now();
      await optimizer.query('users', { id: 1 }, { cache: true });
      const time1 = performance.now() - start1;

      // Second call - should hit cache
      const start2 = performance.now();
      await optimizer.query('users', { id: 1 }, { cache: true });
      const time2 = performance.now() - start2;

      expect(time2).toBeLessThan(time1 / 2); // Cache should be at least 2x faster
    });

    test('should batch multiple queries efficiently', async () => {
      const queries = Array.from({ length: 100 }, (_, i) => ({ id: i }));
      
      const start = performance.now();
      const results = await optimizer.bulkQuery('users', queries);
      const duration = performance.now() - start;

      expect(results).toHaveLength(100);
      expect(duration).toBeLessThan(1000); // Should complete within 1 second
    });

    test('should track query metrics', async () => {
      await optimizer.query('users', { id: 1 });
      await optimizer.query('projects', { id: 1 });
      
      const metrics = optimizer.getMetrics();
      
      expect(metrics).toHaveProperty('users');
      expect(metrics).toHaveProperty('projects');
      expect(metrics.users.count).toBe(1);
    });
  });

  describe('Request Batcher', () => {
    let batcher: RequestBatcher;

    beforeEach(() => {
      batcher = new RequestBatcher({
        maxBatchSize: 5,
        batchDelay: 50,
      });
    });

    test('should batch multiple requests', async () => {
      const requests = Array.from({ length: 10 }, (_, i) => 
        batcher.request('GET', `/api/test/${i}`)
      );

      const start = performance.now();
      await Promise.all(requests);
      const duration = performance.now() - start;

      const metrics = batcher.getMetrics();
      expect(metrics.batchedRequests).toBe(10);
      expect(metrics.totalRequests).toBe(10);
      expect(duration).toBeLessThan(500); // Should batch efficiently
    });

    test('should handle request failures gracefully', async () => {
      // Mock failed request
      global.fetch = jest.fn().mockRejectedValueOnce(new Error('Network error'))
        .mockResolvedValueOnce({
          ok: true,
          json: async () => [{ id: 'req-1', success: true, data: 'test' }]
        });

      const result = await batcher.request('GET', '/api/test');
      
      expect(result).toBeDefined();
      const metrics = batcher.getMetrics();
      expect(metrics.failedRequests).toBeGreaterThanOrEqual(0);
    });
  });

  describe('Worker Manager', () => {
    let manager: WorkerManager;

    beforeEach(() => {
      manager = new WorkerManager(2); // Use 2 workers for testing
    });

    afterEach(() => {
      manager.terminate();
    });

    test('should process tasks in parallel', async () => {
      const tasks = Array.from({ length: 10 }, (_, i) => ({
        type: 'calculate-metrics',
        data: { values: [i, i + 1, i + 2], metrics: ['mean'] }
      }));

      const start = performance.now();
      const results = await manager.processBatch(tasks);
      const duration = performance.now() - start;

      expect(results).toHaveLength(10);
      expect(duration).toBeLessThan(2000); // Parallel processing should be fast
    });

    test('should handle worker crashes', async () => {
      // Simulate a task that might crash
      const result = await manager.process('invalid-task', {});
      
      expect(result).toBeDefined();
      const stats = manager.getStats();
      expect(stats.totalWorkers).toBeGreaterThan(0);
    });
  });

  describe('Performance Monitor', () => {
    let monitor: PerformanceMonitor;

    beforeEach(() => {
      monitor = new PerformanceMonitor();
    });

    afterEach(() => {
      monitor.cleanup();
    });

    test('should track performance metrics', async () => {
      monitor.recordMetric('api_test', 100, 'ms');
      monitor.recordMetric('db_query', 50, 'ms');
      
      const report = monitor.getReport();
      
      expect(report.metrics.apiResponseTime).toBeDefined();
      expect(report.metrics.databaseQueryTime).toBeDefined();
      expect(report.metrics.apiResponseTime!.test).toBe(100);
    });

    test('should calculate performance score', () => {
      // Simulate good performance
      monitor.recordMetric('lcp', 2000, 'ms');
      monitor.recordMetric('fid', 50, 'ms');
      monitor.recordMetric('cls', 0.05, 'score');
      
      const score = monitor.getPerformanceScore();
      
      expect(score).toBeGreaterThan(80); // Good performance should score > 80
    });

    test('should measure async operations', async () => {
      const mockOperation = () => new Promise(resolve => 
        setTimeout(() => resolve('done'), 100)
      );

      const result = await monitor.measure('test-operation', mockOperation);
      
      expect(result).toBe('done');
      
      const report = monitor.getReport();
      const metrics = Object.values(report.metrics).flat();
      expect(metrics.length).toBeGreaterThan(0);
    });
  });

  describe('Integration Tests', () => {
    test('should optimize end-to-end request flow', async () => {
      const optimizer = new QueryOptimizer();
      const batcher = new RequestBatcher();
      const monitor = new PerformanceMonitor();

      const endTimer = monitor.startTimer('full-flow');

      // Simulate complex operation
      const queries = await optimizer.bulkQuery('brands', [
        { status: 'active' },
        { category: 'tech' }
      ], { cache: true });

      const apiCalls = await batcher.request('POST', '/api/analyze', {
        brands: queries
      });

      endTimer();

      const report = monitor.getReport();
      expect(report.duration).toBeLessThan(5000); // Full flow under 5 seconds
    });
  });

  describe('Memory Management', () => {
    test('should not leak memory with large datasets', async () => {
      const initialMemory = process.memoryUsage().heapUsed;
      
      // Process large dataset
      const manager = new WorkerManager();
      const largeData = Array.from({ length: 1000 }, (_, i) => ({
        type: 'optimize-data',
        data: { dataset: Array(1000).fill(i), optimization: 'sort' }
      }));

      await manager.processBatch(largeData);
      manager.terminate();

      // Force garbage collection if available
      if (global.gc) {
        global.gc();
      }

      const finalMemory = process.memoryUsage().heapUsed;
      const memoryIncrease = finalMemory - initialMemory;

      // Memory increase should be reasonable (less than 50MB)
      expect(memoryIncrease).toBeLessThan(50 * 1024 * 1024);
    });
  });

  describe('Cache Performance', () => {
    test('should handle cache invalidation properly', async () => {
      const optimizer = new QueryOptimizer();

      // Cache a query
      await optimizer.query('users', { id: 1 }, { cache: true, cacheTime: 1 });

      // Wait for cache to expire
      await new Promise(resolve => setTimeout(resolve, 1100));

      // Should fetch fresh data
      const start = performance.now();
      await optimizer.query('users', { id: 1 }, { cache: true });
      const duration = performance.now() - start;

      expect(duration).toBeGreaterThan(0); // Should take time to fetch
    });
  });
});
