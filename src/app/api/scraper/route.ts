import { NextRequest, NextResponse } from 'next/server';
import { createServerSupabase } from '@/lib/supabase-server';
import { BrandScraperService } from '@/services/scraper';
import { z } from 'zod';

const scrapeRequestSchema = z.object({
  brandId: z.string().uuid(),
  config: z.object({
    maxPages: z.number().min(1).max(50).default(10),
    includeImages: z.boolean().default(true),
    includeDocuments: z.boolean().default(true),
    respectRobots: z.boolean().default(true),
    delayBetweenRequests: z.number().min(1000).max(10000).default(2000),
  }).optional(),
});

export async function POST(request: NextRequest) {
  try {
    const supabase = createServerSupabase();
    
    const { data: { user }, error: authError } = await supabase.auth.getUser();
    if (authError || !user) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }

    const body = await request.json();
    const { brandId, config } = scrapeRequestSchema.parse(body);

    // Verify user has access to this brand
    const { data: brand, error: brandError } = await supabase
      .from('brands')
      .select(`
        *,
        projects!inner (
          organization_id,
          organization_members!inner (
            user_id
          )
        )
      `)
      .eq('id', brandId)
      .eq('projects.organization_members.user_id', user.id)
      .single();

    if (brandError || !brand) {
      return NextResponse.json({ error: 'Brand not found or access denied' }, { status: 404 });
    }

    // Check if scraping is already in progress
    if (brand.scraping_status === 'in_progress') {
      return NextResponse.json({ error: 'Scraping already in progress' }, { status: 409 });
    }

    // Initialize scraper
    const scraper = new BrandScraperService(config);

    // Start scraping (run in background)
    scraper.scrapeBrand(brandId, brand.website_url)
      .then(async (result) => {
        // Log completion
        await supabase.from('audit_logs').insert({
          user_id: user.id,
          organization_id: brand.projects.organization_id,
          action: 'scrape_completed',
          resource_type: 'brand',
          resource_id: brandId,
          metadata: {
            assets_found: result.assets.length,
            errors: result.errors,
          },
        });
      })
      .catch(async (error) => {
        console.error('Scraping failed:', error);
        
        // Log failure
        await supabase.from('audit_logs').insert({
          user_id: user.id,
          organization_id: brand.projects.organization_id,
          action: 'scrape_failed',
          resource_type: 'brand',
          resource_id: brandId,
          metadata: {
            error: error.message,
          },
        });
      })
      .finally(() => {
        scraper.cleanup();
      });

    return NextResponse.json({ 
      message: 'Scraping started',
      brandId,
      status: 'in_progress'
    });

  } catch (error) {
    if (error instanceof z.ZodError) {
      return NextResponse.json({ 
        error: 'Validation error', 
        details: error.errors 
      }, { status: 400 });
    }

    console.error('Scraping API error:', error);
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

    const { searchParams } = new URL(request.url);
    const brandId = searchParams.get('brandId');

    if (!brandId) {
      return NextResponse.json({ error: 'Brand ID required' }, { status: 400 });
    }

    // Get scraping status and assets
    const { data: brand, error: brandError } = await supabase
      .from('brands')
      .select(`
        id,
        name,
        scraping_status,
        updated_at,
        assets (
          id,
          type,
          url,
          filename,
          file_size,
          created_at
        ),
        projects!inner (
          organization_id,
          organization_members!inner (
            user_id
          )
        )
      `)
      .eq('id', brandId)
      .eq('projects.organization_members.user_id', user.id)
      .single();

    if (brandError || !brand) {
      return NextResponse.json({ error: 'Brand not found or access denied' }, { status: 404 });
    }

    return NextResponse.json({
      brandId: brand.id,
      name: brand.name,
      status: brand.scraping_status,
      lastUpdated: brand.updated_at,
      assets: brand.assets,
    });

  } catch (error) {
    console.error('Scraping status API error:', error);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  }
}
