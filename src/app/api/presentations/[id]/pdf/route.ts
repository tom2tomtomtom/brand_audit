import { NextRequest, NextResponse } from 'next/server';
import { createServerSupabase } from '@/lib/supabase-server';
import { PDFGeneratorService } from '@/services/pdf-generator';

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

    const presentationId = params.id;

    // Verify user has access to this presentation
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

    if (presentation.status !== 'completed') {
      return NextResponse.json({ error: 'Presentation not ready for PDF generation' }, { status: 400 });
    }

    // Generate PDF
    const pdfGenerator = new PDFGeneratorService();
    const pdfPath = await pdfGenerator.generatePresentationPDF(presentationId);

    // Log the action
    await supabase.from('audit_logs').insert({
      user_id: user.id,
      organization_id: presentation.projects.organizations.id,
      action: 'pdf_generated',
      resource_type: 'presentation',
      resource_id: presentationId,
      metadata: {
        pdf_path: pdfPath,
      },
    });

    return NextResponse.json({ 
      message: 'PDF generated successfully',
      pdfPath 
    });

  } catch (error) {
    console.error('PDF generation API error:', error);
    return NextResponse.json({ error: 'Failed to generate PDF' }, { status: 500 });
  }
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

    if (!presentation.pdf_url) {
      return NextResponse.json({ error: 'PDF not available' }, { status: 404 });
    }

    // Get PDF file from storage
    const { data: pdfData, error: fileError } = await supabase.storage
      .from('presentations')
      .download(presentation.pdf_url.replace('presentations/', ''));

    if (fileError || !pdfData) {
      console.error('PDF download error:', fileError);
      return NextResponse.json({ error: 'Failed to download PDF' }, { status: 500 });
    }

    // Convert blob to buffer
    const buffer = await pdfData.arrayBuffer();

    // Return PDF with appropriate headers
    return new NextResponse(buffer, {
      headers: {
        'Content-Type': 'application/pdf',
        'Content-Disposition': `attachment; filename="${presentation.name}.pdf"`,
        'Content-Length': buffer.byteLength.toString(),
      },
    });

  } catch (error) {
    console.error('PDF download API error:', error);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  }
}
