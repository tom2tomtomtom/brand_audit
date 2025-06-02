import { NextRequest, NextResponse } from 'next/server';
import { createServerSupabase } from '@/lib/supabase-server';
import { AIAnalyzerService } from '@/services/ai-analyzer';

interface RouteParams {
  params: {
    id: string;
  };
}

export async function POST(request: NextRequest, { params }: RouteParams) {
  try {
    const supabase = createServerSupabase();
    
    const { data: { user }, error: authError } = await supabase.auth.getUser();
    if (authError || !user) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }

    const projectId = params.id;

    // Verify user has access to this project
    const { data: project, error: projectError } = await supabase
      .from('projects')
      .select(`
        id,
        name,
        organizations!inner (
          id,
          organization_members!inner (
            user_id
          )
        )
      `)
      .eq('id', projectId)
      .eq('organizations.organization_members.user_id', user.id)
      .single();

    if (projectError || !project) {
      return NextResponse.json({ error: 'Project not found or access denied' }, { status: 404 });
    }

    // Get all brands that are ready for analysis (scraping completed)
    const { data: brands, error: brandsError } = await supabase
      .from('brands')
      .select('id, name, website_url, scraping_status, analysis_status')
      .eq('project_id', projectId)
      .eq('scraping_status', 'completed')
      .in('analysis_status', ['pending', 'failed']);

    if (brandsError) {
      console.error('Error fetching brands:', brandsError);
      return NextResponse.json({ error: 'Failed to fetch brands' }, { status: 500 });
    }

    if (!brands || brands.length === 0) {
      return NextResponse.json({ 
        message: 'No brands ready for analysis. Complete scraping first.',
        analyzed: 0 
      });
    }

    // Initialize AI analyzer
    const analyzer = new AIAnalyzerService();
    
    // Start analyzing all brands (run in background)
    const analysisPromises = brands.map(async (brand) => {
      try {
        // Update status to in_progress
        await supabase
          .from('brands')
          .update({ 
            analysis_status: 'in_progress',
            updated_at: new Date().toISOString(),
          })
          .eq('id', brand.id);

        // Run full analysis
        const result = await analyzer.runFullAnalysis(brand.id);

        // Log success
        await supabase.from('audit_logs').insert({
          user_id: user.id,
          organization_id: project.organizations.id,
          action: 'bulk_analysis_completed',
          resource_type: 'brand',
          resource_id: brand.id,
          metadata: {
            brand_name: brand.name,
            project_id: projectId,
            analyses_completed: Object.keys(result).filter(k => k !== 'errors').length,
            errors: result.errors,
          },
        });

        return { brandId: brand.id, success: true, result };
      } catch (error) {
        console.error(`Analysis failed for brand ${brand.id}:`, error);
        
        // Update status to failed
        await supabase
          .from('brands')
          .update({ 
            analysis_status: 'failed',
            updated_at: new Date().toISOString(),
          })
          .eq('id', brand.id);

        return { brandId: brand.id, success: false, error: error.message };
      }
    });

    // Don't wait for all to complete, return immediately
    Promise.all(analysisPromises).then(async (results) => {
      const successful = results.filter(r => r.success).length;
      const failed = results.filter(r => !r.success).length;

      // Log bulk operation completion
      await supabase.from('audit_logs').insert({
        user_id: user.id,
        organization_id: project.organizations.id,
        action: 'bulk_analysis_finished',
        resource_type: 'project',
        resource_id: projectId,
        metadata: {
          total_brands: brands.length,
          successful,
          failed,
        },
      });
    });

    return NextResponse.json({ 
      message: `Started analyzing ${brands.length} brands`,
      brands: brands.length,
      started: true
    });

  } catch (error) {
    console.error('Bulk analysis API error:', error);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  }
}
