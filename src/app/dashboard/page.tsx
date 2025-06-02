import { redirect } from 'next/navigation';
import { createServerSupabase } from '@/lib/supabase-server';
import { DashboardContent } from '@/components/dashboard/dashboard-content';

export default async function DashboardPage() {
  const supabase = createServerSupabase();
  
  const {
    data: { session },
  } = await supabase.auth.getSession();

  if (!session) {
    redirect('/auth/login');
  }

  return <DashboardContent />;
}
