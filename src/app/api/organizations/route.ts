import { NextRequest, NextResponse } from 'next/server';
import { createServerSupabase } from '@/lib/supabase-server';
import { z } from 'zod';

const createOrganizationSchema = z.object({
  name: z.string().min(1, 'Organization name is required'),
  description: z.string().optional(),
  website: z.string().url().optional().or(z.literal('')),
  industry: z.string().optional(),
});

export async function POST(request: NextRequest) {
  try {
    const supabase = createServerSupabase();
    
    const { data: { user }, error: authError } = await supabase.auth.getUser();
    if (authError || !user) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }

    const body = await request.json();
    const validatedData = createOrganizationSchema.parse(body);

    // Check if user already has an organization
    const { data: existingMembership } = await supabase
      .from('organization_members')
      .select('organization_id')
      .eq('user_id', user.id)
      .single();

    if (existingMembership) {
      return NextResponse.json(
        { error: 'User already belongs to an organization' },
        { status: 400 }
      );
    }

    // Create organization
    const { data: organization, error: orgError } = await supabase
      .from('organizations')
      .insert({
        name: validatedData.name,
        description: validatedData.description,
        website: validatedData.website || null,
        industry: validatedData.industry,
        subscription_tier: 'free',
        created_by: user.id,
      })
      .select()
      .single();

    if (orgError) {
      console.error('Error creating organization:', orgError);
      return NextResponse.json(
        { error: 'Failed to create organization' },
        { status: 500 }
      );
    }

    // Add user as admin member
    const { error: memberError } = await supabase
      .from('organization_members')
      .insert({
        organization_id: organization.id,
        user_id: user.id,
        role: 'admin',
        status: 'active',
      });

    if (memberError) {
      console.error('Error adding user to organization:', memberError);
      // Try to clean up the organization
      await supabase.from('organizations').delete().eq('id', organization.id);
      return NextResponse.json(
        { error: 'Failed to add user to organization' },
        { status: 500 }
      );
    }

    return NextResponse.json({
      organization: {
        id: organization.id,
        name: organization.name,
        description: organization.description,
        website: organization.website,
        industry: organization.industry,
        subscriptionTier: organization.subscription_tier,
        createdAt: organization.created_at,
      },
    });
  } catch (error) {
    if (error instanceof z.ZodError) {
      return NextResponse.json(
        { error: 'Invalid input', details: error.errors },
        { status: 400 }
      );
    }

    console.error('API error:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}

export async function GET(request: NextRequest) {
  try {
    const supabase = createServerSupabase();
    
    const { data: { user }, error: authError } = await supabase.auth.getUser();
    if (authError || !user) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }

    // Get user's organizations
    const { data: memberships, error } = await supabase
      .from('organization_members')
      .select(`
        role,
        status,
        organizations (
          id,
          name,
          description,
          website,
          industry,
          subscription_tier,
          logo_url,
          created_at,
          updated_at
        )
      `)
      .eq('user_id', user.id)
      .eq('status', 'active');

    if (error) {
      console.error('Error fetching organizations:', error);
      return NextResponse.json(
        { error: 'Failed to fetch organizations' },
        { status: 500 }
      );
    }

    const organizations = memberships?.map(membership => ({
      id: (membership.organizations as any).id,
      name: (membership.organizations as any).name,
      description: (membership.organizations as any).description,
      website: (membership.organizations as any).website,
      industry: (membership.organizations as any).industry,
      subscriptionTier: (membership.organizations as any).subscription_tier,
      logoUrl: (membership.organizations as any).logo_url,
      role: membership.role,
      createdAt: (membership.organizations as any).created_at,
      updatedAt: (membership.organizations as any).updated_at,
    })) || [];

    return NextResponse.json({ organizations });
  } catch (error) {
    console.error('API error:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}
