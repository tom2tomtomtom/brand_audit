import { NextRequest, NextResponse } from 'next/server';
import { createServerSupabase } from '@/lib/supabase-server';

export async function POST(request: NextRequest) {
  try {
    const supabase = createServerSupabase();
    
    const { data: { user }, error: authError } = await supabase.auth.getUser();
    if (authError || !user) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }

    // Check if user already exists in our users table
    const { data: existingUser, error: checkError } = await supabase
      .from('users')
      .select('id')
      .eq('id', user.id)
      .single();

    if (checkError && checkError.code !== 'PGRST116') { // PGRST116 = no rows returned
      console.error('Error checking user:', checkError);
      return NextResponse.json({ error: 'Database error' }, { status: 500 });
    }

    if (existingUser) {
      return NextResponse.json({ message: 'User already exists' });
    }

    // Create user in our users table
    const { error: createUserError } = await supabase
      .from('users')
      .insert({
        id: user.id,
        email: user.email!,
        full_name: user.user_metadata?.full_name || user.user_metadata?.name || null,
        avatar_url: user.user_metadata?.avatar_url || null,
        role: 'viewer',
      });

    if (createUserError) {
      console.error('Error creating user:', createUserError);
      return NextResponse.json({ error: 'Failed to create user' }, { status: 500 });
    }

    // Create a default organization for the user
    const orgSlug = `${user.email?.split('@')[0]}-org-${Date.now()}`;
    const orgName = `${user.user_metadata?.full_name || user.email?.split('@')[0]}'s Organization`;

    const { data: orgId, error: orgError } = await supabase
      .rpc('create_organization_with_owner', {
        org_name: orgName,
        org_slug: orgSlug,
        user_id: user.id,
      });

    if (orgError) {
      console.error('Error creating organization:', orgError);
      // Don't fail the request if org creation fails, user can create one later
    }

    return NextResponse.json({ 
      message: 'User created successfully',
      organizationId: orgId 
    });

  } catch (error) {
    console.error('API error:', error);
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

    // Get user data with organizations
    const { data: userData, error: userError } = await supabase
      .from('users')
      .select('*')
      .eq('id', user.id)
      .single();

    if (userError) {
      console.error('Error fetching user:', userError);
      return NextResponse.json({ error: 'User not found' }, { status: 404 });
    }

    // Get user's organizations
    const { data: orgData, error: orgError } = await supabase
      .from('organization_members')
      .select(`
        role,
        organizations (
          id,
          name,
          slug,
          logo_url,
          subscription_tier,
          created_at,
          updated_at
        )
      `)
      .eq('user_id', user.id);

    if (orgError) {
      console.error('Error fetching organizations:', orgError);
      return NextResponse.json({ error: 'Failed to fetch organizations' }, { status: 500 });
    }

    const organizations = orgData?.map(item => ({
      ...item.organizations,
      logoUrl: (item.organizations as any).logo_url,
      subscriptionTier: (item.organizations as any).subscription_tier,
      createdAt: (item.organizations as any).created_at,
      updatedAt: (item.organizations as any).updated_at,
      memberRole: item.role,
    })) || [];

    return NextResponse.json({
      user: {
        id: userData.id,
        email: userData.email,
        fullName: userData.full_name,
        avatarUrl: userData.avatar_url,
        role: userData.role,
        createdAt: userData.created_at,
        updatedAt: userData.updated_at,
      },
      organizations,
    });

  } catch (error) {
    console.error('API error:', error);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  }
}
