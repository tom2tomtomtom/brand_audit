import { NextRequest, NextResponse } from 'next/server';
import { createServerSupabase } from '@/lib/supabase-server';

interface RouteParams {
  params: {
    id: string;
  };
}

export async function GET(request: NextRequest, { params }: RouteParams) {
  try {
    const supabase = createServerSupabase();
    
    const { data: { user }, error: authError } = await supabase.auth.getUser();
    if (authError || !user) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }

    const brandId = params.id;

    // Verify user has access to this brand
    const { data: brand, error: brandError } = await supabase
      .from('brands')
      .select(`
        *,
        projects!inner (
          id,
          name,
          organization_id,
          organizations!inner (
            id,
            organization_members!inner (
              user_id
            )
          )
        )
      `)
      .eq('id', brandId)
      .eq('projects.organizations.organization_members.user_id', user.id)
      .single();

    if (brandError || !brand) {
      return NextResponse.json({ error: 'Brand not found or access denied' }, { status: 404 });
    }

    // Get all analyses for this brand
    const { data: analyses, error: analysesError } = await supabase
      .from('analyses')
      .select('*')
      .eq('brand_id', brandId)
      .order('created_at', { ascending: false });

    if (analysesError) {
      console.error('Error fetching analyses:', analysesError);
      return NextResponse.json({ error: 'Failed to fetch analyses' }, { status: 500 });
    }

    // Group analyses by type (get the latest of each type)
    const latestAnalyses: Record<string, any> = {};
    analyses?.forEach(analysis => {
      if (!latestAnalyses[analysis.type] || 
          new Date(analysis.created_at) > new Date(latestAnalyses[analysis.type].created_at)) {
        latestAnalyses[analysis.type] = analysis;
      }
    });

    return NextResponse.json({
      brand: {
        id: brand.id,
        name: brand.name,
        websiteUrl: brand.website_url,
        industry: brand.industry,
        project: {
          id: brand.projects.id,
          name: brand.projects.name,
        },
      },
      analyses: latestAnalyses,
      history: analyses || [],
    });

  } catch (error) {
    console.error('API error:', error);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  }
}
