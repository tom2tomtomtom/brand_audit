import { createServerSupabase } from '@/lib/supabase-server';
import { ProjectDashboard } from '@/components/dashboard/project-dashboard';
import { redirect } from 'next/navigation';

interface ProjectPageProps {
  params: {
    id: string;
  };
}

export default async function ProjectPage({ params }: ProjectPageProps) {
  const supabase = createServerSupabase();

  // Get current user
  const { data: { user }, error: authError } = await supabase.auth.getUser();
  
  if (authError || !user) {
    redirect('/auth/login');
  }

  // Get project with access check
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
    .eq('id', params.id)
    .eq('organizations.organization_members.user_id', user.id)
    .single();

  if (projectError || !project) {
    redirect('/dashboard');
  }

  return (
    <div className="container mx-auto py-6">
      <ProjectDashboard project={project} />
    </div>
  );
}
