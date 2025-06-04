import { NextRequest, NextResponse } from 'next/server';
import { createServerSupabase } from '@/lib/supabase-server';

export async function GET(request: NextRequest) {
  try {
    const supabase = createServerSupabase();
    
    const { data: { user }, error: authError } = await supabase.auth.getUser();
    if (authError || !user) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }

    // Get user's organization
    const { data: membership } = await supabase
      .from('organization_members')
      .select('organization_id')
      .eq('user_id', user.id)
      .eq('status', 'active')
      .single();

    if (!membership) {
      return NextResponse.json({ error: 'No organization found' }, { status: 404 });
    }

    // Get brands for the organization with visual data
    const { data: brands, error } = await supabase
      .from('brands')
      .select(`
        id,
        name,
        website_url,
        industry,
        visual_data,
        scraping_status,
        created_at,
        updated_at,
        projects!inner(
          organization_id
        )
      `)
      .eq('projects.organization_id', membership.organization_id)
      .order('created_at', { ascending: false });

    if (error) {
      console.error('Error fetching brands:', error);
      return NextResponse.json(
        { error: 'Failed to fetch brands' },
        { status: 500 }
      );
    }

    // Transform the data to match our interface
    const transformedBrands = brands?.map(brand => ({
      id: brand.id,
      name: brand.name,
      websiteUrl: brand.website_url,
      industry: brand.industry,
      visualData: brand.visual_data,
      scrapingStatus: brand.scraping_status,
      createdAt: brand.created_at,
      updatedAt: brand.updated_at,
    })) || [];

    return NextResponse.json({
      brands: transformedBrands,
      total: transformedBrands.length,
    });
  } catch (error) {
    console.error('API error:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}

export async function POST(request: NextRequest) {
  try {
    const supabase = createServerSupabase();
    
    const { data: { user }, error: authError } = await supabase.auth.getUser();
    if (authError || !user) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }

    const body = await request.json();
    const { name, websiteUrl, industry, projectId } = body;

    if (!name || !websiteUrl || !projectId) {
      return NextResponse.json(
        { error: 'Name, website URL, and project ID are required' },
        { status: 400 }
      );
    }

    // Verify the project belongs to the user's organization
    const { data: project } = await supabase
      .from('projects')
      .select(`
        id,
        organization_id,
        organization_members!inner(
          user_id
        )
      `)
      .eq('id', projectId)
      .eq('organization_members.user_id', user.id)
      .eq('organization_members.status', 'active')
      .single();

    if (!project) {
      return NextResponse.json(
        { error: 'Project not found or access denied' },
        { status: 404 }
      );
    }

    // Create the brand
    const { data: brand, error } = await supabase
      .from('brands')
      .insert({
        name,
        website_url: websiteUrl,
        industry,
        project_id: projectId,
        scraping_status: 'pending',
      })
      .select()
      .single();

    if (error) {
      console.error('Error creating brand:', error);
      return NextResponse.json(
        { error: 'Failed to create brand' },
        { status: 500 }
      );
    }

    return NextResponse.json({
      brand: {
        id: brand.id,
        name: brand.name,
        websiteUrl: brand.website_url,
        industry: brand.industry,
        scrapingStatus: brand.scraping_status,
        createdAt: brand.created_at,
      },
    });
  } catch (error) {
    console.error('API error:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}
