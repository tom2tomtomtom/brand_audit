import { NextRequest, NextResponse } from 'next/server';
import { createServerSupabase } from '@/lib/supabase-server';
import { ScraperService } from '@/services/scraper';

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

    const projectId = params.id;

    // Verify user has access to this project
    const { data: project, error: projectError } = await supabase
      .from('projects')
      .select(`
        id,
        name,
        organizations!inner (
          id,
          organization_members!inner (
            user_id
          )
        )
      `)
      .eq('id', projectId)
      .eq('organizations.organization_members.user_id', user.id)
      .single();

    if (projectError || !project) {
      return NextResponse.json({ error: 'Project not found or access denied' }, { status: 404 });
    }

    // Get all brands in this project that haven't been scraped or failed
    const { data: brands, error: brandsError } = await supabase
      .from('brands')
      .select('id, name, website_url, scraping_status')
      .eq('project_id', projectId)
      .in('scraping_status', ['pending', 'failed']);

    if (brandsError) {
      console.error('Error fetching brands:', brandsError);
      return NextResponse.json({ error: 'Failed to fetch brands' }, { status: 500 });
    }

    if (!brands || brands.length === 0) {
      return NextResponse.json({ 
        message: 'No brands available for scraping',
        scraped: 0 
      });
    }

    // Initialize scraper
    const scraper = new ScraperService();
    
    // Start scraping all brands (run in background)
    const scrapingPromises = brands.map(async (brand) => {
      try {
        // Update status to in_progress
        await supabase
          .from('brands')
          .update({ 
            scraping_status: 'in_progress',
            updated_at: new Date().toISOString(),
          })
          .eq('id', brand.id);

        // Run scraping
        await scraper.scrapeBrand(brand.id, {
          maxPages: 5,
          includeImages: true,
          includeDocuments: true,
          respectRobots: true,
          delayBetweenRequests: 2000,
        });

        // Log success
        await supabase.from('audit_logs').insert({
          user_id: user.id,
          organization_id: project.organizations.id,
          action: 'bulk_scrape_completed',
          resource_type: 'brand',
          resource_id: brand.id,
          metadata: {
            brand_name: brand.name,
            project_id: projectId,
          },
        });

        return { brandId: brand.id, success: true };
      } catch (error) {
        console.error(`Scraping failed for brand ${brand.id}:`, error);
        
        // Update status to failed
        await supabase
          .from('brands')
          .update({ 
            scraping_status: 'failed',
            updated_at: new Date().toISOString(),
          })
          .eq('id', brand.id);

        return { brandId: brand.id, success: false, error: error.message };
      }
    });

    // Don't wait for all to complete, return immediately
    Promise.all(scrapingPromises).then(async (results) => {
      const successful = results.filter(r => r.success).length;
      const failed = results.filter(r => !r.success).length;

      // Log bulk operation completion
      await supabase.from('audit_logs').insert({
        user_id: user.id,
        organization_id: project.organizations.id,
        action: 'bulk_scrape_finished',
        resource_type: 'project',
        resource_id: projectId,
        metadata: {
          total_brands: brands.length,
          successful,
          failed,
        },
      });
    });

    return NextResponse.json({ 
      message: `Started scraping ${brands.length} brands`,
      brands: brands.length,
      started: true
    });

  } catch (error) {
    console.error('Bulk scrape API error:', error);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  }
}
