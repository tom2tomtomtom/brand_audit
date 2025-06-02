import { NextRequest, NextResponse } from 'next/server';
import { createServerSupabase } from '@/lib/supabase-server';
import { AIAnalyzerService } from '@/services/ai-analyzer';
import { z } from 'zod';

const analysisRequestSchema = z.object({
  brandId: z.string().uuid(),
  types: z.array(z.enum(['positioning', 'visual', 'competitive', 'sentiment'])).optional(),
});

export async function POST(request: NextRequest) {
  try {
    const supabase = createServerSupabase();
    
    const { data: { user }, error: authError } = await supabase.auth.getUser();
    if (authError || !user) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }

    const body = await request.json();
    const { brandId, types } = analysisRequestSchema.parse(body);

    // Verify user has access to this brand
    const { data: brand, error: brandError } = await supabase
      .from('brands')
      .select(`
        *,
        projects!inner (
          organization_id,
          organization_members!inner (
            user_id
          )
        )
      `)
      .eq('id', brandId)
      .eq('projects.organization_members.user_id', user.id)
      .single();

    if (brandError || !brand) {
      return NextResponse.json({ error: 'Brand not found or access denied' }, { status: 404 });
    }

    // Check if analysis is already in progress
    if (brand.analysis_status === 'in_progress') {
      return NextResponse.json({ error: 'Analysis already in progress' }, { status: 409 });
    }

    // Initialize analyzer with user ID
    const analyzer = new AIAnalyzerService(user.id);

    // Start analysis (run in background)
    if (types && types.length > 0) {
      // Run specific analyses
      Promise.all(
        types.map(async (type) => {
          try {
            const input = await analyzer['prepareBrandData'](brandId);
            
            switch (type) {
              case 'positioning':
                return await analyzer.analyzePositioning(input);
              case 'visual':
                return await analyzer.analyzeVisualIdentity(input);
              case 'competitive':
                return await analyzer.analyzeCompetitive(input);
              case 'sentiment':
                return await analyzer.analyzeSentiment(input);
            }
          } catch (error) {
            console.error(`${type} analysis failed:`, error);
            throw error;
          }
        })
      ).then(async (results) => {
        // Log completion
        await supabase.from('audit_logs').insert({
          user_id: user.id,
          organization_id: brand.projects.organization_id,
          action: 'analysis_completed',
          resource_type: 'brand',
          resource_id: brandId,
          metadata: {
            types,
            results_count: results.length,
          },
        });
      }).catch(async (error) => {
        console.error('Analysis failed:', error);
        
        // Log failure
        await supabase.from('audit_logs').insert({
          user_id: user.id,
          organization_id: brand.projects.organization_id,
          action: 'analysis_failed',
          resource_type: 'brand',
          resource_id: brandId,
          metadata: {
            error: error.message,
            types,
          },
        });
      });
    } else {
      // Run full analysis
      analyzer.runFullAnalysis(brandId)
        .then(async (result) => {
          // Log completion
          await supabase.from('audit_logs').insert({
            user_id: user.id,
            organization_id: brand.projects.organization_id,
            action: 'full_analysis_completed',
            resource_type: 'brand',
            resource_id: brandId,
            metadata: {
              errors: result.errors,
              completed_analyses: Object.keys(result).filter(k => k !== 'errors').length,
            },
          });
        })
        .catch(async (error) => {
          console.error('Full analysis failed:', error);
          
          // Log failure
          await supabase.from('audit_logs').insert({
            user_id: user.id,
            organization_id: brand.projects.organization_id,
            action: 'full_analysis_failed',
            resource_type: 'brand',
            resource_id: brandId,
            metadata: {
              error: error.message,
            },
          });
        });
    }

    return NextResponse.json({ 
      message: 'Analysis started',
      brandId,
      types: types || ['positioning', 'visual', 'competitive', 'sentiment'],
      status: 'in_progress'
    });

  } catch (error) {
    if (error instanceof z.ZodError) {
      return NextResponse.json({ 
        error: 'Validation error', 
        details: error.errors 
      }, { status: 400 });
    }

    console.error('Analysis API error:', error);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  }
}

export async function GET(request: NextRequest) {
  try {
    const supabase = createServerSupabase();
    
    const { data: { user }, error: authError } = await supabase.auth.getUser();
    if (authError || !user) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }

    const { searchParams } = new URL(request.url);
    const brandId = searchParams.get('brandId');

    if (!brandId) {
      return NextResponse.json({ error: 'Brand ID required' }, { status: 400 });
    }

    // Get analysis results
    const { data: brand, error: brandError } = await supabase
      .from('brands')
      .select(`
        id,
        name,
        analysis_status,
        updated_at,
        analyses (
          id,
          type,
          status,
          results,
          confidence_score,
          created_at
        ),
        projects!inner (
          organization_id,
          organization_members!inner (
            user_id
          )
        )
      `)
      .eq('id', brandId)
      .eq('projects.organization_members.user_id', user.id)
      .single();

    if (brandError || !brand) {
      return NextResponse.json({ error: 'Brand not found or access denied' }, { status: 404 });
    }

    // Group analyses by type
    const analysesByType = brand.analyses.reduce((acc: any, analysis: any) => {
      acc[analysis.type] = analysis;
      return acc;
    }, {});

    return NextResponse.json({
      brandId: brand.id,
      name: brand.name,
      status: brand.analysis_status,
      lastUpdated: brand.updated_at,
      analyses: analysesByType,
    });

  } catch (error) {
    console.error('Analysis status API error:', error);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  }
}
