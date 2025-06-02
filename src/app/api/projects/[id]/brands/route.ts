import { NextRequest, NextResponse } from 'next/server';
import { createServerSupabase } from '@/lib/supabase-server';

export async function GET(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
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
        organization_members!inner (
          user_id
        )
      `)
      .eq('id', projectId)
      .eq('organization_members.user_id', user.id)
      .single();

    if (projectError || !project) {
      return NextResponse.json({ error: 'Project not found or access denied' }, { status: 404 });
    }

    // Get brands for this project
    const { data: brands, error: brandsError } = await supabase
      .from('brands')
      .select(`
        *,
        assets (
          id,
          type,
          filename,
          file_size
        ),
        analyses (
          id,
          type,
          status,
          confidence_score
        )
      `)
      .eq('project_id', projectId)
      .order('created_at', { ascending: false });

    if (brandsError) {
      return NextResponse.json({ error: 'Failed to fetch brands' }, { status: 500 });
    }

    return NextResponse.json({ 
      brands: brands || [],
      project: {
        id: project.id,
        name: project.name,
      }
    });

  } catch (error) {
    console.error('Brands API error:', error);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  }
}

export async function POST(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  try {
    const supabase = createServerSupabase();
    
    const { data: { user }, error: authError } = await supabase.auth.getUser();
    if (authError || !user) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }

    const projectId = params.id;
    const body = await request.json();

    // Verify user has access to this project
    const { data: project, error: projectError } = await supabase
      .from('projects')
      .select(`
        id,
        organization_id,
        organization_members!inner (
          user_id
        )
      `)
      .eq('id', projectId)
      .eq('organization_members.user_id', user.id)
      .single();

    if (projectError || !project) {
      return NextResponse.json({ error: 'Project not found or access denied' }, { status: 404 });
    }

    // Create new brand
    const { data: brand, error: brandError } = await supabase
      .from('brands')
      .insert({
        project_id: projectId,
        name: body.name,
        website_url: body.websiteUrl,
        industry: body.industry,
        description: body.description,
      })
      .select()
      .single();

    if (brandError) {
      return NextResponse.json({ error: 'Failed to create brand' }, { status: 500 });
    }

    // Log the action
    await supabase.from('audit_logs').insert({
      user_id: user.id,
      organization_id: project.organization_id,
      action: 'brand_created',
      resource_type: 'brand',
      resource_id: brand.id,
      metadata: {
        project_id: projectId,
        brand_name: body.name,
      },
    });

    return NextResponse.json({ brand }, { status: 201 });

  } catch (error) {
    console.error('Create brand API error:', error);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  }
}
