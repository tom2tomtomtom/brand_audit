import { NextRequest } from 'next/server';
import { GET } from '@/app/api/health/route';
import { createServerSupabase } from '@/lib/supabase-server';
import { env } from '@/lib/env';

// Mock dependencies
jest.mock('@/lib/supabase-server');
jest.mock('@/lib/env', () => ({
  env: {
    NODE_ENV: 'test',
    OPENAI_API_KEY: 'test-key',
    ANTHROPIC_API_KEY: 'test-key',
  },
  getSafeEnvInfo: jest.fn(() => ({
    nodeEnv: 'test',
    hasOpenAI: true,
    hasAnthropic: true,
    hasRedis: false,
    hasSentry: false,
    features: {
      enableAnalytics: false,
      enableDebugLogs: false,
      enableRateLimiting: false,
      enableEncryption: false,
      enableMonitoring: false,
    },
  })),
}));

// Mock fetch for external service checks
global.fetch = jest.fn();

describe('/api/health', () => {
  let mockSupabase: any;

  beforeEach(() => {
    jest.clearAllMocks();
    
    // Setup mock Supabase
    mockSupabase = {
      from: jest.fn().mockReturnThis(),
      select: jest.fn().mockReturnThis(),
      limit: jest.fn().mockResolvedValue({ error: null }),
      storage: {
        listBuckets: jest.fn().mockResolvedValue({ 
          data: [{ id: 'test-bucket' }], 
          error: null 
        }),
      },
    };
    
    (createServerSupabase as jest.Mock).mockReturnValue(mockSupabase);
    (global.fetch as jest.Mock).mockResolvedValue({ ok: true });
  });

  describe('Successful health check', () => {
    it('should return healthy status when all checks pass', async () => {
      const request = new NextRequest('http://localhost:3000/api/health');
      const response = await GET(request);
      const data = await response.json();

      expect(response.status).toBe(200);
      expect(data.status).toBe('healthy');
      expect(data.checks).toMatchObject({
        database: { status: 'pass' },
        storage: { status: 'pass' },
        ai_services: { status: 'pass' },
        external_services: { status: 'pass' },
      });
      expect(data.metadata).toMatchObject({
        node_version: process.version,
        env_info: {
          nodeEnv: 'test',
          hasOpenAI: true,
          hasAnthropic: true,
        },
      });
    });

    it('should include response times for each check', async () => {
      const request = new NextRequest('http://localhost:3000/api/health');
      const response = await GET(request);
      const data = await response.json();

      expect(data.checks.database.response_time_ms).toBeGreaterThan(0);
      expect(data.checks.storage.response_time_ms).toBeGreaterThan(0);
      expect(data.checks.ai_services.response_time_ms).toBeGreaterThan(0);
      expect(data.checks.external_services.response_time_ms).toBeGreaterThan(0);
    });
  });

  describe('Degraded health check', () => {
    it('should return degraded status when database is healthy but other services fail', async () => {
      mockSupabase.storage.listBuckets.mockResolvedValue({ 
        error: { message: 'Storage error' } 
      });
      (global.fetch as jest.Mock).mockRejectedValue(new Error('Network error'));

      const request = new NextRequest('http://localhost:3000/api/health');
      const response = await GET(request);
      const data = await response.json();

      expect(response.status).toBe(200);
      expect(data.status).toBe('degraded');
      expect(data.checks.database.status).toBe('pass');
      expect(data.checks.storage.status).toBe('fail');
      expect(data.checks.external_services.status).toBe('fail');
    });

    it('should return degraded for warnings in external services', async () => {
      (global.fetch as jest.Mock).mockRejectedValueOnce(new Error('Timeout'));

      const request = new NextRequest('http://localhost:3000/api/health');
      const response = await GET(request);
      const data = await response.json();

      expect(response.status).toBe(200);
      expect(data.status).toBe('degraded');
      expect(data.checks.external_services.status).toBe('warn');
    });
  });

  describe('Unhealthy status', () => {
    it('should return unhealthy when database fails', async () => {
      mockSupabase.limit.mockResolvedValue({ 
        error: { message: 'Database connection failed' } 
      });

      const request = new NextRequest('http://localhost:3000/api/health');
      const response = await GET(request);
      const data = await response.json();

      expect(response.status).toBe(503);
      expect(data.status).toBe('unhealthy');
      expect(data.checks.database.status).toBe('fail');
      expect(data.checks.database.message).toContain('Database error');
    });

    it('should return unhealthy when multiple critical services fail', async () => {
      mockSupabase.limit.mockResolvedValue({ 
        error: { message: 'Database error' } 
      });
      mockSupabase.storage.listBuckets.mockResolvedValue({ 
        error: { message: 'Storage error' } 
      });

      const request = new NextRequest('http://localhost:3000/api/health');
      const response = await GET(request);
      const data = await response.json();

      expect(response.status).toBe(503);
      expect(data.status).toBe('unhealthy');
    });
  });

  describe('Individual check failures', () => {
    it('should handle database check timeout', async () => {
      mockSupabase.limit.mockRejectedValue(new Error('Timeout'));

      const request = new NextRequest('http://localhost:3000/api/health');
      const response = await GET(request);
      const data = await response.json();

      expect(data.checks.database.status).toBe('fail');
      expect(data.checks.database.message).toContain('Database connection failed');
    });

    it('should handle storage check failure', async () => {
      mockSupabase.storage.listBuckets.mockRejectedValue(new Error('Storage unavailable'));

      const request = new NextRequest('http://localhost:3000/api/health');
      const response = await GET(request);
      const data = await response.json();

      expect(data.checks.storage.status).toBe('fail');
      expect(data.checks.storage.message).toContain('Storage connection failed');
    });

    it('should detect missing AI service configurations', async () => {
      // Mock env without API keys
      jest.doMock('@/lib/env', () => ({
        env: {
          NODE_ENV: 'test',
          OPENAI_API_KEY: '',
          ANTHROPIC_API_KEY: '',
        },
        getSafeEnvInfo: jest.fn(() => ({
          hasOpenAI: false,
          hasAnthropic: false,
        })),
      }));

      const request = new NextRequest('http://localhost:3000/api/health');
      const response = await GET(request);
      const data = await response.json();

      expect(data.checks.ai_services.status).toBe('fail');
      expect(data.checks.ai_services.message).toBe('No AI service API keys configured');
    });
  });

  describe('Metadata and system info', () => {
    it('should include memory usage information', async () => {
      const request = new NextRequest('http://localhost:3000/api/health');
      const response = await GET(request);
      const data = await response.json();

      expect(data.metadata.memory_usage).toHaveProperty('rss');
      expect(data.metadata.memory_usage).toHaveProperty('heapTotal');
      expect(data.metadata.memory_usage).toHaveProperty('heapUsed');
      expect(data.metadata.memory_usage).toHaveProperty('external');
    });

    it('should include uptime information', async () => {
      const request = new NextRequest('http://localhost:3000/api/health');
      const response = await GET(request);
      const data = await response.json();

      expect(data.uptime).toBeGreaterThan(0);
      expect(typeof data.uptime).toBe('number');
    });

    it('should include version and environment info', async () => {
      const request = new NextRequest('http://localhost:3000/api/health');
      const response = await GET(request);
      const data = await response.json();

      expect(data.version).toBeTruthy();
      expect(data.environment).toBe('test');
      expect(data.timestamp).toBeTruthy();
    });
  });

  describe('Error handling', () => {
    it('should handle complete health check failure gracefully', async () => {
      // Mock all checks to throw errors
      (createServerSupabase as jest.Mock).mockImplementation(() => {
        throw new Error('Supabase initialization failed');
      });

      const request = new NextRequest('http://localhost:3000/api/health');
      const response = await GET(request);
      const data = await response.json();

      expect(response.status).toBe(503);
      expect(data.status).toBe('unhealthy');
      expect(data.checks).toMatchObject({
        database: { status: 'fail' },
        storage: { status: 'fail' },
        ai_services: { status: 'fail' },
        external_services: { status: 'fail' },
      });
    });

    it('should handle promise rejection in allSettled', async () => {
      // Make one check reject unexpectedly
      mockSupabase.from.mockImplementation(() => {
        throw new Error('Unexpected error');
      });

      const request = new NextRequest('http://localhost:3000/api/health');
      const response = await GET(request);
      const data = await response.json();

      expect(response.status).toBe(503);
      expect(data.checks.database.status).toBe('fail');
      expect(data.checks.database.message).toContain('Check failed');
    });
  });

  describe('Performance', () => {
    it('should complete health check within reasonable time', async () => {
      const start = Date.now();
      const request = new NextRequest('http://localhost:3000/api/health');
      await GET(request);
      const duration = Date.now() - start;

      expect(duration).toBeLessThan(1000); // Should complete within 1 second
    });

    it('should run checks in parallel', async () => {
      // Add delays to simulate slower checks
      mockSupabase.limit.mockImplementation(() => 
        new Promise(resolve => setTimeout(() => resolve({ error: null }), 100))
      );
      mockSupabase.storage.listBuckets.mockImplementation(() => 
        new Promise(resolve => setTimeout(() => resolve({ data: [], error: null }), 100))
      );

      const start = Date.now();
      const request = new NextRequest('http://localhost:3000/api/health');
      await GET(request);
      const duration = Date.now() - start;

      // If running in parallel, should be ~100ms, not 200ms+
      expect(duration).toBeLessThan(150);
    });
  });
});
