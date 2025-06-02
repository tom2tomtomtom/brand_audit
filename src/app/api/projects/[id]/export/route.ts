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

    const projectId = params.id;
    const { searchParams } = new URL(request.url);
    const format = searchParams.get('format') || 'json';

    // Verify user has access to this project
    const { data: project, error: projectError } = await supabase
      .from('projects')
      .select(`
        *,
        organizations!inner (
          id,
          name,
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

    // Get complete project data
    const { data: brands, error: brandsError } = await supabase
      .from('brands')
      .select(`
        *,
        assets (*),
        analyses (*)
      `)
      .eq('project_id', projectId)
      .order('created_at', { ascending: true });

    if (brandsError) {
      console.error('Error fetching brands:', brandsError);
      return NextResponse.json({ error: 'Failed to fetch project data' }, { status: 500 });
    }

    // Prepare export data
    const exportData = {
      project: {
        id: project.id,
        name: project.name,
        description: project.description,
        status: project.status,
        created_at: project.created_at,
        updated_at: project.updated_at,
        organization: {
          id: project.organizations.id,
          name: project.organizations.name,
        },
      },
      brands: brands?.map(brand => ({
        id: brand.id,
        name: brand.name,
        website_url: brand.website_url,
        industry: brand.industry,
        description: brand.description,
        scraping_status: brand.scraping_status,
        analysis_status: brand.analysis_status,
        created_at: brand.created_at,
        updated_at: brand.updated_at,
        assets: brand.assets?.map((asset: any) => ({
          id: asset.id,
          type: asset.type,
          url: asset.url,
          filename: asset.filename,
          file_size: asset.file_size,
          alt_text: asset.alt_text,
          created_at: asset.created_at,
        })) || [],
        analyses: brand.analyses?.map((analysis: any) => ({
          id: analysis.id,
          type: analysis.type,
          status: analysis.status,
          results: analysis.results,
          confidence_score: analysis.confidence_score,
          created_at: analysis.created_at,
        })) || [],
      })) || [],
      exported_at: new Date().toISOString(),
      exported_by: user.email,
    };

    // Log export action
    await supabase.from('audit_logs').insert({
      user_id: user.id,
      organization_id: project.organizations.id,
      action: 'data_exported',
      resource_type: 'project',
      resource_id: projectId,
      metadata: {
        format,
        brands_count: brands?.length || 0,
      },
    });

    if (format === 'csv') {
      // Generate CSV format
      const csvData = generateCSV(exportData);
      
      return new NextResponse(csvData, {
        headers: {
          'Content-Type': 'text/csv',
          'Content-Disposition': `attachment; filename="${project.name}_export.csv"`,
        },
      });
    } else {
      // Return JSON format
      return new NextResponse(JSON.stringify(exportData, null, 2), {
        headers: {
          'Content-Type': 'application/json',
          'Content-Disposition': `attachment; filename="${project.name}_export.json"`,
        },
      });
    }

  } catch (error) {
    console.error('Export API error:', error);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  }
}

function generateCSV(data: any): string {
  const rows = [];
  
  // Header row
  rows.push([
    'Brand Name',
    'Website URL',
    'Industry',
    'Scraping Status',
    'Analysis Status',
    'Assets Count',
    'Analyses Count',
    'Positioning Analysis',
    'Visual Analysis',
    'Competitive Analysis',
    'Sentiment Analysis',
    'Created At',
    'Updated At'
  ].join(','));

  // Data rows
  data.brands.forEach((brand: any) => {
    const positioningAnalysis = brand.analyses.find((a: any) => a.type === 'positioning');
    const visualAnalysis = brand.analyses.find((a: any) => a.type === 'visual');
    const competitiveAnalysis = brand.analyses.find((a: any) => a.type === 'competitive');
    const sentimentAnalysis = brand.analyses.find((a: any) => a.type === 'sentiment');

    rows.push([
      `"${brand.name}"`,
      `"${brand.website_url}"`,
      `"${brand.industry || ''}"`,
      `"${brand.scraping_status}"`,
      `"${brand.analysis_status}"`,
      brand.assets.length,
      brand.analyses.length,
      positioningAnalysis ? `"${positioningAnalysis.status}"` : '""',
      visualAnalysis ? `"${visualAnalysis.status}"` : '""',
      competitiveAnalysis ? `"${competitiveAnalysis.status}"` : '""',
      sentimentAnalysis ? `"${sentimentAnalysis.status}"` : '""',
      `"${brand.created_at}"`,
      `"${brand.updated_at}"`
    ].join(','));
  });

  return rows.join('\n');
}
