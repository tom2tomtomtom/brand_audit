import { NextRequest, NextResponse } from 'next/server';
import { createServerSupabase } from '@/lib/supabase-server';
import { env, getSafeEnvInfo } from '@/lib/env';

interface HealthCheck {
  status: 'healthy' | 'degraded' | 'unhealthy';
  timestamp: string;
  version: string;
  environment: string;
  uptime: number;
  checks: {
    database: HealthCheckResult;
    storage: HealthCheckResult;
    ai_services: HealthCheckResult;
    external_services: HealthCheckResult;
  };
  metadata: {
    node_version: string;
    memory_usage: NodeJS.MemoryUsage;
    env_info: ReturnType<typeof getSafeEnvInfo>;
  };
}

interface HealthCheckResult {
  status: 'pass' | 'fail' | 'warn';
  response_time_ms: number;
  message?: string;
  details?: Record<string, any>;
}

const startTime = Date.now();

export async function GET(_request: NextRequest) {
  try {
    // Perform all health checks
    const [
      databaseCheck,
      storageCheck,
      aiServicesCheck,
      externalServicesCheck
    ] = await Promise.allSettled([
      checkDatabase(),
      checkStorage(),
      checkAIServices(),
      checkExternalServices()
    ]);

    // Determine overall status
    const checks = {
      database: getResultFromSettled(databaseCheck),
      storage: getResultFromSettled(storageCheck),
      ai_services: getResultFromSettled(aiServicesCheck),
      external_services: getResultFromSettled(externalServicesCheck)
    };

    const overallStatus = determineOverallStatus(checks);

    const healthCheck: HealthCheck = {
      status: overallStatus,
      timestamp: new Date().toISOString(),
      version: process.env.npm_package_version || '1.0.0',
      environment: env.NODE_ENV,
      uptime: Date.now() - startTime,
      checks,
      metadata: {
        node_version: process.version,
        memory_usage: process.memoryUsage(),
        env_info: getSafeEnvInfo()
      }
    };

    // Return appropriate HTTP status based on health
    const httpStatus = overallStatus === 'healthy' ? 200 :
                      overallStatus === 'degraded' ? 200 : 503;

    return NextResponse.json(healthCheck, { status: httpStatus });

  } catch (error) {
    const errorResponse: HealthCheck = {
      status: 'unhealthy',
      timestamp: new Date().toISOString(),
      version: process.env.npm_package_version || '1.0.0',
      environment: env.NODE_ENV,
      uptime: Date.now() - startTime,
      checks: {
        database: { status: 'fail', response_time_ms: 0, message: 'Health check failed' },
        storage: { status: 'fail', response_time_ms: 0, message: 'Health check failed' },
        ai_services: { status: 'fail', response_time_ms: 0, message: 'Health check failed' },
        external_services: { status: 'fail', response_time_ms: 0, message: 'Health check failed' }
      },
      metadata: {
        node_version: process.version,
        memory_usage: process.memoryUsage(),
        env_info: getSafeEnvInfo()
      }
    };

    return NextResponse.json(errorResponse, { status: 503 });
  }
}

async function checkDatabase(): Promise<HealthCheckResult> {
  const start = Date.now();

  try {
    const supabase = createServerSupabase();

    // Simple query to test database connectivity
    const { error } = await supabase
      .from('organizations')
      .select('id')
      .limit(1);

    const responseTime = Date.now() - start;

    if (error) {
      return {
        status: 'fail',
        response_time_ms: responseTime,
        message: `Database error: ${error.message}`,
        details: { error: error.code }
      };
    }

    return {
      status: 'pass',
      response_time_ms: responseTime,
      message: 'Database connection successful'
    };

  } catch (error) {
    return {
      status: 'fail',
      response_time_ms: Date.now() - start,
      message: `Database connection failed: ${error instanceof Error ? error.message : 'Unknown error'}`
    };
  }
}

async function checkStorage(): Promise<HealthCheckResult> {
  const start = Date.now();

  try {
    const supabase = createServerSupabase();

    // Test storage by listing buckets
    const { data, error } = await supabase.storage.listBuckets();

    const responseTime = Date.now() - start;

    if (error) {
      return {
        status: 'fail',
        response_time_ms: responseTime,
        message: `Storage error: ${error.message}`
      };
    }

    return {
      status: 'pass',
      response_time_ms: responseTime,
      message: 'Storage connection successful',
      details: { buckets_count: data?.length || 0 }
    };

  } catch (error) {
    return {
      status: 'fail',
      response_time_ms: Date.now() - start,
      message: `Storage connection failed: ${error instanceof Error ? error.message : 'Unknown error'}`
    };
  }
}

async function checkAIServices(): Promise<HealthCheckResult> {
  const start = Date.now();

  try {
    // Check if API keys are configured
    const hasOpenAI = !!env.OPENAI_API_KEY;
    const hasAnthropic = !!env.ANTHROPIC_API_KEY;

    if (!hasOpenAI && !hasAnthropic) {
      return {
        status: 'fail',
        response_time_ms: Date.now() - start,
        message: 'No AI service API keys configured'
      };
    }

    return {
      status: 'pass',
      response_time_ms: Date.now() - start,
      message: 'AI services configured',
      details: {
        openai: hasOpenAI,
        anthropic: hasAnthropic
      }
    };

  } catch (error) {
    return {
      status: 'fail',
      response_time_ms: Date.now() - start,
      message: `AI services check failed: ${error instanceof Error ? error.message : 'Unknown error'}`
    };
  }
}

async function checkExternalServices(): Promise<HealthCheckResult> {
  const start = Date.now();

  try {
    // Check if we can reach external services (basic connectivity)
    const checks = await Promise.allSettled([
      fetch('https://httpbin.org/status/200', {
        method: 'HEAD',
        signal: AbortSignal.timeout(5000)
      })
    ]);

    const responseTime = Date.now() - start;
    const failedChecks = checks.filter(check => check.status === 'rejected').length;

    if (failedChecks > 0) {
      return {
        status: 'warn',
        response_time_ms: responseTime,
        message: `${failedChecks} external service(s) unreachable`,
        details: { failed_checks: failedChecks, total_checks: checks.length }
      };
    }

    return {
      status: 'pass',
      response_time_ms: responseTime,
      message: 'External services reachable'
    };

  } catch (error) {
    return {
      status: 'fail',
      response_time_ms: Date.now() - start,
      message: `External services check failed: ${error instanceof Error ? error.message : 'Unknown error'}`
    };
  }
}

function getResultFromSettled(settled: PromiseSettledResult<HealthCheckResult>): HealthCheckResult {
  if (settled.status === 'fulfilled') {
    return settled.value;
  } else {
    return {
      status: 'fail',
      response_time_ms: 0,
      message: `Check failed: ${settled.reason instanceof Error ? settled.reason.message : 'Unknown error'}`
    };
  }
}

function determineOverallStatus(checks: HealthCheck['checks']): 'healthy' | 'degraded' | 'unhealthy' {
  const results = Object.values(checks);

  const failCount = results.filter(r => r.status === 'fail').length;
  const warnCount = results.filter(r => r.status === 'warn').length;

  if (failCount > 0) {
    // If database fails, system is unhealthy
    if (checks.database.status === 'fail') {
      return 'unhealthy';
    }
    // Other failures might be degraded
    return failCount > 1 ? 'unhealthy' : 'degraded';
  }

  if (warnCount > 0) {
    return 'degraded';
  }

  return 'healthy';
}
