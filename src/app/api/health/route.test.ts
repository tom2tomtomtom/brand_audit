import { GET } from './route';
import { NextRequest } from 'next/server';

// Mock the environment and dependencies
jest.mock('@/lib/env', () => ({
  env: {
    NODE_ENV: 'test',
    OPENAI_API_KEY: 'test-key',
    ANTHROPIC_API_KEY: 'test-key'
  },
  getSafeEnvInfo: () => ({
    nodeEnv: 'test',
    hasOpenAI: true,
    hasAnthropic: true,
    hasRedis: false,
    hasSentry: false,
    features: {
      enableAnalytics: false,
      enableDebugLogs: true,
      enableRateLimiting: false,
      enableEncryption: false,
      enableMonitoring: false,
    }
  })
}));

jest.mock('@/lib/supabase-server', () => ({
  createServerSupabase: () => ({
    from: () => ({
      select: () => ({
        limit: () => ({
          then: (callback: any) => callback({ data: [], error: null })
        })
      })
    }),
    storage: {
      listBuckets: () => Promise.resolve({ data: [], error: null })
    }
  })
}));

// Mock fetch for external services check
global.fetch = jest.fn(() =>
  Promise.resolve({
    ok: true,
    status: 200,
  })
) as jest.Mock;

describe('/api/health', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('should return healthy status when all checks pass', async () => {
    const request = new NextRequest('http://localhost:3000/api/health');
    const response = await GET(request);
    const data = await response.json();

    expect(response.status).toBe(200);
    expect(data.status).toBe('healthy');
    expect(data).toHaveProperty('timestamp');
    expect(data).toHaveProperty('version');
    expect(data).toHaveProperty('environment', 'test');
    expect(data).toHaveProperty('uptime');
    expect(data).toHaveProperty('checks');
    expect(data).toHaveProperty('metadata');

    // Check that all health checks are present
    expect(data.checks).toHaveProperty('database');
    expect(data.checks).toHaveProperty('storage');
    expect(data.checks).toHaveProperty('ai_services');
    expect(data.checks).toHaveProperty('external_services');

    // Check metadata structure
    expect(data.metadata).toHaveProperty('node_version');
    expect(data.metadata).toHaveProperty('memory_usage');
    expect(data.metadata).toHaveProperty('env_info');
  });

  it('should return degraded status when some checks fail', async () => {
    // Mock a failing external service
    (global.fetch as jest.Mock).mockRejectedValueOnce(new Error('Network error'));

    const request = new NextRequest('http://localhost:3000/api/health');
    const response = await GET(request);
    const data = await response.json();

    expect(response.status).toBe(200); // Still 200 for degraded
    expect(data.status).toBe('degraded');
  });

  it('should return unhealthy status when database fails', async () => {
    // Mock database failure
    jest.doMock('@/lib/supabase-server', () => ({
      createServerSupabase: () => ({
        from: () => ({
          select: () => ({
            limit: () => Promise.resolve({ 
              data: null, 
              error: { message: 'Connection failed', code: 'CONNECTION_ERROR' } 
            })
          })
        }),
        storage: {
          listBuckets: () => Promise.resolve({ data: [], error: null })
        }
      })
    }));

    const request = new NextRequest('http://localhost:3000/api/health');
    const response = await GET(request);
    const data = await response.json();

    expect(response.status).toBe(503);
    expect(data.status).toBe('unhealthy');
  });

  it('should handle errors gracefully', async () => {
    // Mock a complete failure
    jest.doMock('@/lib/supabase-server', () => {
      throw new Error('Complete failure');
    });

    const request = new NextRequest('http://localhost:3000/api/health');
    const response = await GET(request);
    const data = await response.json();

    expect(response.status).toBe(503);
    expect(data.status).toBe('unhealthy');
  });

  it('should include performance metrics', async () => {
    const request = new NextRequest('http://localhost:3000/api/health');
    const response = await GET(request);
    const data = await response.json();

    // Check that response times are included
    expect(data.checks.database).toHaveProperty('response_time_ms');
    expect(data.checks.storage).toHaveProperty('response_time_ms');
    expect(data.checks.ai_services).toHaveProperty('response_time_ms');
    expect(data.checks.external_services).toHaveProperty('response_time_ms');

    // Response times should be numbers
    expect(typeof data.checks.database.response_time_ms).toBe('number');
    expect(typeof data.checks.storage.response_time_ms).toBe('number');
  });

  it('should validate AI services configuration', async () => {
    const request = new NextRequest('http://localhost:3000/api/health');
    const response = await GET(request);
    const data = await response.json();

    expect(data.checks.ai_services.status).toBe('pass');
    expect(data.checks.ai_services.details).toHaveProperty('openai', true);
    expect(data.checks.ai_services.details).toHaveProperty('anthropic', true);
  });
});
