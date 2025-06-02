import { redirect } from 'next/navigation';
import { createServerSupabase } from '@/lib/supabase-server';
import { AnalysisResults } from '@/components/analysis/analysis-results';

interface AnalysisPageProps {
  params: {
    id: string;
  };
}

export default async function AnalysisPage({ params }: AnalysisPageProps) {
  const supabase = createServerSupabase();
  
  const {
    data: { session },
  } = await supabase.auth.getSession();

  if (!session) {
    redirect('/auth/login');
  }

  // Verify user has access to this brand
  const { data: brand, error } = await supabase
    .from('brands')
    .select(`
      id,
      name,
      projects!inner (
        id,
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

  if (error || !brand) {
    redirect('/dashboard');
  }

  return (
    <div className="container mx-auto py-6">
      <AnalysisResults brandId={params.id} />
    </div>
  );
}
