import { redirect } from 'next/navigation';
import { createServerSupabase } from '@/lib/supabase-server';
import { LandingPage } from '@/components/landing-page';

export default async function HomePage() {
  const supabase = createServerSupabase();
  
  const {
    data: { session },
  } = await supabase.auth.getSession();

  if (session) {
    redirect('/dashboard');
  }

  return <LandingPage />;
}
