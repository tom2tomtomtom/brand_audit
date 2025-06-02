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
      return NextResponse.json({ error: 'Presentation not ready for download' }, { status: 400 });
    }

    // Get file from storage
    const { data: fileData, error: fileError } = await supabase.storage
      .from('presentations')
      .download(presentation.export_url.replace('presentations/', ''));

    if (fileError || !fileData) {
      console.error('File download error:', fileError);
      return NextResponse.json({ error: 'Failed to download presentation file' }, { status: 500 });
    }

    // Convert blob to buffer
    const buffer = await fileData.arrayBuffer();

    // Return file with appropriate headers
    return new NextResponse(buffer, {
      headers: {
        'Content-Type': 'text/html',
        'Content-Disposition': `attachment; filename="${presentation.name}.html"`,
        'Content-Length': buffer.byteLength.toString(),
      },
    });

  } catch (error) {
    console.error('Download API error:', error);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  }
}
