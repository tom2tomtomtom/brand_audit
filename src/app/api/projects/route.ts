import { NextRequest, NextResponse } from 'next/server';
import { createServerSupabase } from '@/lib/supabase-server';
import { z } from 'zod';

const createProjectSchema = z.object({
  name: z.string().min(1, 'Project name is required'),
  description: z.string().optional(),
  brands: z.array(z.object({
    name: z.string().min(1, 'Brand name is required'),
    websiteUrl: z.string().url('Valid URL is required'),
    industry: z.string().optional(),
    description: z.string().optional(),
  })).min(1, 'At least one brand is required'),
});

export async function GET(request: NextRequest) {
  try {
    const supabase = createServerSupabase();
    
    const { data: { user }, error: authError } = await supabase.auth.getUser();
    if (authError || !user) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }

    // Get user's projects with stats
    const { data: projects, error } = await supabase
      .rpc('get_user_projects_with_stats', { user_uuid: user.id });

    if (error) {
      console.error('Error fetching projects:', error);
      return NextResponse.json({ error: 'Failed to fetch projects' }, { status: 500 });
    }

    return NextResponse.json({ projects });
  } catch (error) {
    console.error('API error:', error);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
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
    const validatedData = createProjectSchema.parse(body);

    // Get user's current organization
    const { data: orgMember, error: orgError } = await supabase
      .from('organization_members')
      .select('organization_id')
      .eq('user_id', user.id)
      .single();

    if (orgError || !orgMember) {
      return NextResponse.json({ error: 'No organization found' }, { status: 400 });
    }

    // Create project with brands using the database function
    const { data: projectId, error: createError } = await supabase
      .rpc('create_project_with_brands', {
        project_data: {
          name: validatedData.name,
          description: validatedData.description,
        },
        brands_data: validatedData.brands.map(brand => ({
          name: brand.name,
          website_url: brand.websiteUrl,
          industry: brand.industry,
          description: brand.description,
        })),
        user_id: user.id,
        org_id: orgMember.organization_id,
      });

    if (createError) {
      console.error('Error creating project:', createError);
      return NextResponse.json({ error: 'Failed to create project' }, { status: 500 });
    }

    // Fetch the created project
    const { data: project, error: fetchError } = await supabase
      .from('projects')
      .select(`
        *,
        brands (*)
      `)
      .eq('id', projectId)
      .single();

    if (fetchError) {
      console.error('Error fetching created project:', fetchError);
      return NextResponse.json({ error: 'Project created but failed to fetch' }, { status: 500 });
    }

    return NextResponse.json({ project }, { status: 201 });
  } catch (error) {
    if (error instanceof z.ZodError) {
      return NextResponse.json({ 
        error: 'Validation error', 
        details: error.errors 
      }, { status: 400 });
    }

    console.error('API error:', error);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  }
}
