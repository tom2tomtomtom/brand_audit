import { NextRequest, NextResponse } from 'next/server';
import { createServerSupabase } from '@/lib/supabase-server';
import { PresentationGeneratorService } from '@/services/presentation-generator';
import { z } from 'zod';

const createPresentationSchema = z.object({
  projectId: z.string().uuid(),
  templateId: z.string(),
  name: z.string().optional(),
});

export async function POST(request: NextRequest) {
  try {
    const supabase = createServerSupabase();
    
    const { data: { user }, error: authError } = await supabase.auth.getUser();
    if (authError || !user) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }

    const body = await request.json();
    const { projectId, templateId, name } = createPresentationSchema.parse(body);

    // Verify user has access to this project
    const { data: project, error: projectError } = await supabase
      .from('projects')
      .select(`
        *,
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

    // Initialize presentation generator
    const generator = new PresentationGeneratorService();

    // Generate presentation
    const presentationId = await generator.generatePresentation(
      projectId,
      templateId,
      user.id
    );

    // Log the action
    await supabase.from('audit_logs').insert({
      user_id: user.id,
      organization_id: project.organization_id,
      action: 'presentation_generated',
      resource_type: 'presentation',
      resource_id: presentationId,
      metadata: {
        project_id: projectId,
        template_id: templateId,
      },
    });

    return NextResponse.json({ 
      presentationId,
      message: 'Presentation generated successfully'
    }, { status: 201 });

  } catch (error) {
    if (error instanceof z.ZodError) {
      return NextResponse.json({ 
        error: 'Validation error', 
        details: error.errors 
      }, { status: 400 });
    }

    console.error('Presentation generation API error:', error);
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
    const projectId = searchParams.get('projectId');

    if (projectId) {
      // Get presentations for a specific project
      const { data: presentations, error } = await supabase
        .from('presentations')
        .select(`
          *,
          projects!inner (
            name,
            organization_members!inner (
              user_id
            )
          )
        `)
        .eq('project_id', projectId)
        .eq('projects.organization_members.user_id', user.id)
        .order('created_at', { ascending: false });

      if (error) {
        return NextResponse.json({ error: 'Failed to fetch presentations' }, { status: 500 });
      }

      return NextResponse.json({ presentations });
    } else {
      // Get all presentations for user's organizations
      const { data: presentations, error } = await supabase
        .from('presentations')
        .select(`
          *,
          projects!inner (
            name,
            organization_members!inner (
              user_id
            )
          )
        `)
        .eq('projects.organization_members.user_id', user.id)
        .order('created_at', { ascending: false })
        .limit(50);

      if (error) {
        return NextResponse.json({ error: 'Failed to fetch presentations' }, { status: 500 });
      }

      return NextResponse.json({ presentations });
    }

  } catch (error) {
    console.error('Presentations API error:', error);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  }
}
