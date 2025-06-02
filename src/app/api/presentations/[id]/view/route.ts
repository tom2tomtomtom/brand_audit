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

    const presentationId = params.id;

    // Get presentation with access check
    const { data: presentation, error: presentationError } = await supabase
      .from('presentations')
      .select(`
        *,
        projects!inner (
          id,
          name,
          organizations!inner (
            id,
            organization_members!inner (
              user_id
            )
          )
        )
      `)
      .eq('id', presentationId)
      .eq('projects.organizations.organization_members.user_id', user.id)
      .single();

    if (presentationError || !presentation) {
      return NextResponse.json({ error: 'Presentation not found or access denied' }, { status: 404 });
    }

    if (presentation.status !== 'completed' || !presentation.export_url) {
      return NextResponse.json({ error: 'Presentation not ready for viewing' }, { status: 400 });
    }

    // Get file from storage
    const { data: fileData, error: fileError } = await supabase.storage
      .from('presentations')
      .download(presentation.export_url.replace('presentations/', ''));

    if (fileError || !fileData) {
      console.error('File download error:', fileError);
      return NextResponse.json({ error: 'Failed to load presentation file' }, { status: 500 });
    }

    // Convert blob to text
    const htmlContent = await fileData.text();

    // Return HTML content directly
    return new NextResponse(htmlContent, {
      headers: {
        'Content-Type': 'text/html',
        'Cache-Control': 'no-cache, no-store, must-revalidate',
      },
    });

  } catch (error) {
    console.error('View API error:', error);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  }
}
