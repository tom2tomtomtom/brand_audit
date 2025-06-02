import { redirect } from 'next/navigation';
import { createServerSupabase } from '@/lib/supabase-server';
import { PresentationViewer } from '@/components/presentations/presentation-viewer';

interface PresentationPageProps {
  params: {
    id: string;
  };
}

export default async function PresentationPage({ params }: PresentationPageProps) {
  const supabase = createServerSupabase();
  
  const {
    data: { session },
  } = await supabase.auth.getSession();

  if (!session) {
    redirect('/auth/login');
  }

  // Get presentation with access check
  const { data: presentation, error } = await supabase
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
    .eq('id', params.id)
    .eq('projects.organizations.organization_members.user_id', session.user.id)
    .single();

  if (error || !presentation) {
    redirect('/dashboard');
  }

  return <PresentationViewer presentation={presentation} />;
}
