import { NextRequest, NextResponse } from 'next/server';
import { createServerSupabase } from '@/lib/supabase-server';
import { costTracker } from '@/lib/rate-limiter';

export async function GET(request: NextRequest) {
  try {
    const supabase = createServerSupabase();
    
    const { data: { user }, error: authError } = await supabase.auth.getUser();
    if (authError || !user) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }

    // Check if user is admin (you can implement your own admin check)
    const { data: userData, error: userError } = await supabase
      .from('users')
      .select('role')
      .eq('id', user.id)
      .single();

    if (userError || userData?.role !== 'admin') {
      return NextResponse.json({ error: 'Admin access required' }, { status: 403 });
    }

    // Get system statistics
    const stats = await getSystemStats(supabase);
    
    return NextResponse.json(stats);

  } catch (error) {
    console.error('Admin stats API error:', error);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  }
}

async function getSystemStats(supabase: any) {
  const now = new Date();
  const last24Hours = new Date(now.getTime() - 24 * 60 * 60 * 1000);
  const last7Days = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000);
  const thisMonth = new Date(now.getFullYear(), now.getMonth(), 1);

  // User statistics
  const { data: totalUsers } = await supabase
    .from('users')
    .select('id', { count: 'exact' });

  const { data: activeUsers24h } = await supabase
    .from('audit_logs')
    .select('user_id', { count: 'exact' })
    .gte('created_at', last24Hours.toISOString())
    .not('user_id', 'is', null);

  const { data: newUsers7d } = await supabase
    .from('users')
    .select('id', { count: 'exact' })
    .gte('created_at', last7Days.toISOString());

  // Project statistics
  const { data: totalProjects } = await supabase
    .from('projects')
    .select('id', { count: 'exact' });

  const { data: activeProjects } = await supabase
    .from('projects')
    .select('id', { count: 'exact' })
    .eq('status', 'active');

  const { data: projectsThisMonth } = await supabase
    .from('projects')
    .select('id', { count: 'exact' })
    .gte('created_at', thisMonth.toISOString());

  // Brand statistics
  const { data: totalBrands } = await supabase
    .from('brands')
    .select('id', { count: 'exact' });

  const { data: scrapedBrands } = await supabase
    .from('brands')
    .select('id', { count: 'exact' })
    .eq('scraping_status', 'completed');

  const { data: analyzedBrands } = await supabase
    .from('brands')
    .select('id', { count: 'exact' })
    .eq('analysis_status', 'completed');

  // Analysis statistics
  const { data: totalAnalyses } = await supabase
    .from('analyses')
    .select('id', { count: 'exact' });

  const { data: analysesThisMonth } = await supabase
    .from('analyses')
    .select('id', { count: 'exact' })
    .gte('created_at', thisMonth.toISOString());

  const { data: analysesByType } = await supabase
    .from('analyses')
    .select('type')
    .gte('created_at', thisMonth.toISOString());

  // Presentation statistics
  const { data: totalPresentations } = await supabase
    .from('presentations')
    .select('id', { count: 'exact' });

  const { data: presentationsThisMonth } = await supabase
    .from('presentations')
    .select('id', { count: 'exact' })
    .gte('created_at', thisMonth.toISOString());

  // Error statistics
  const { data: errors24h } = await supabase
    .from('audit_logs')
    .select('id', { count: 'exact' })
    .gte('created_at', last24Hours.toISOString())
    .like('action', '%failed%');

  // Storage statistics
  const { data: totalAssets } = await supabase
    .from('assets')
    .select('id, file_size', { count: 'exact' });

  const totalStorageBytes = totalAssets?.reduce((sum: number, asset: any) => 
    sum + (asset.file_size || 0), 0) || 0;

  // Analysis type breakdown
  const analysisTypeBreakdown = analysesByType?.reduce((acc: any, analysis: any) => {
    acc[analysis.type] = (acc[analysis.type] || 0) + 1;
    return acc;
  }, {}) || {};

  return {
    users: {
      total: totalUsers?.length || 0,
      active24h: activeUsers24h?.length || 0,
      new7d: newUsers7d?.length || 0,
    },
    projects: {
      total: totalProjects?.length || 0,
      active: activeProjects?.length || 0,
      thisMonth: projectsThisMonth?.length || 0,
    },
    brands: {
      total: totalBrands?.length || 0,
      scraped: scrapedBrands?.length || 0,
      analyzed: analyzedBrands?.length || 0,
      scrapingRate: totalBrands?.length ? 
        Math.round((scrapedBrands?.length || 0) / totalBrands.length * 100) : 0,
      analysisRate: totalBrands?.length ? 
        Math.round((analyzedBrands?.length || 0) / totalBrands.length * 100) : 0,
    },
    analyses: {
      total: totalAnalyses?.length || 0,
      thisMonth: analysesThisMonth?.length || 0,
      byType: analysisTypeBreakdown,
    },
    presentations: {
      total: totalPresentations?.length || 0,
      thisMonth: presentationsThisMonth?.length || 0,
    },
    system: {
      errors24h: errors24h?.length || 0,
      totalStorageGB: Math.round(totalStorageBytes / (1024 * 1024 * 1024) * 100) / 100,
      totalAssets: totalAssets?.length || 0,
    },
    timestamp: now.toISOString(),
  };
}
