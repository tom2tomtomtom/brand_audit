import { NextRequest, NextResponse } from 'next/server';
import { createServerSupabase } from '@/lib/supabase-server';
import { validateRequest, validateQuery, brandSchemas, commonSchemas, createValidationErrorResponse } from '@/lib/validation';
import { logger, logApiCall } from '@/lib/logger';
import { rateLimiters, withRateLimit } from '@/lib/rate-limit';
import { AuthenticationError, ValidationError, NotFoundError, DatabaseError } from '@/lib/errors';
import { APP_CONSTANTS } from '@/lib/constants';

export async function GET(request: NextRequest) {
  return withRateLimit(rateLimiters.api)(request, async () => {
    return logApiCall('GET /api/brands', async () => {
      try {
        // Validate query parameters
        const querySchema = commonSchemas.pagination.extend({
          search: commonSchemas.name.optional(),
          industry: commonSchemas.name.optional(),
        });

        const query = validateQuery(querySchema)(request);

        const supabase = createServerSupabase();

        const { data: { user }, error: authError } = await supabase.auth.getUser();
        if (authError || !user) {
          throw new AuthenticationError('Authentication required');
        }

        logger.info('Fetching brands for user', { userId: user.id });

        // Get user's organization
        const { data: membership } = await supabase
          .from('organization_members')
          .select('organization_id')
          .eq('user_id', user.id)
          .eq('status', 'active')
          .single();

        if (!membership) {
          throw new NotFoundError('Organization membership');
        }

        // Build query with filters
        let brandsQuery = supabase
          .from('brands')
          .select(`
            id,
            name,
            website_url,
            industry,
            visual_data,
            scraping_status,
            created_at,
            updated_at,
            projects!inner(
              organization_id
            )
          `)
          .eq('projects.organization_id', membership.organization_id);

        // Apply search filter if provided
        if (query.search) {
          brandsQuery = brandsQuery.ilike('name', `%${query.search}%`);
        }

        // Apply industry filter if provided
        if (query.industry) {
          brandsQuery = brandsQuery.eq('industry', query.industry);
        }

        // Apply pagination
        const page = query.page || 1;
        const limit = query.limit || APP_CONSTANTS.DATABASE.DEFAULT_PAGE_SIZE;
        const offset = (page - 1) * limit;

        brandsQuery = brandsQuery
          .range(offset, offset + limit - 1)
          .order('created_at', { ascending: false });

        const { data: brands, error, count } = await brandsQuery;

        if (error) {
          logger.error('Error fetching brands', {
            userId: user.id,
            organizationId: membership.organization_id
          }, error);
          throw new DatabaseError('fetch', error.message);
        }

        // Transform the data to match our interface
        const transformedBrands = brands?.map(brand => ({
          id: brand.id,
          name: brand.name,
          websiteUrl: brand.website_url,
          industry: brand.industry,
          visualData: brand.visual_data,
          scrapingStatus: brand.scraping_status,
          createdAt: brand.created_at,
          updatedAt: brand.updated_at,
        })) || [];

        const totalCount = count || transformedBrands.length;
        const totalPages = Math.ceil(totalCount / limit);

        logger.info('Successfully fetched brands', {
          userId: user.id,
          organizationId: membership.organization_id,
          count: transformedBrands.length,
          page,
          limit
        });

        return NextResponse.json({
          data: transformedBrands,
          pagination: {
            page,
            limit,
            total: totalCount,
            totalPages,
          },
        });
      } catch (error) {
        if (error instanceof AuthenticationError) {
          return NextResponse.json({ error: error.message }, { status: 401 });
        }
        if (error instanceof NotFoundError) {
          return NextResponse.json({ error: error.message }, { status: 404 });
        }
        if (error instanceof ValidationError) {
          return createValidationErrorResponse(error);
        }
        if (error instanceof DatabaseError) {
          return NextResponse.json({ error: 'Database error occurred' }, { status: 500 });
        }

        logger.error('Unexpected error in GET /api/brands', {}, error as Error);
        return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
      }
    });
  });
}

export async function POST(request: NextRequest) {
  return withRateLimit(rateLimiters.api)(request, async () => {
    return logApiCall('POST /api/brands', async () => {
      try {
        // Validate request body
        const brandData = await validateRequest(brandSchemas.create)(request);

        const supabase = createServerSupabase();

        const { data: { user }, error: authError } = await supabase.auth.getUser();
        if (authError || !user) {
          throw new AuthenticationError('Authentication required');
        }

        logger.info('Creating new brand', {
          userId: user.id,
          brandName: brandData.name,
          websiteUrl: brandData.website_url
        });

        // Verify the project belongs to the user's organization
        const { data: project } = await supabase
          .from('projects')
          .select(`
            id,
            organization_id,
            organization_members!inner(
              user_id
            )
          `)
          .eq('id', brandData.organization_id)
          .eq('organization_members.user_id', user.id)
          .eq('organization_members.status', 'active')
          .single();

        if (!project) {
          throw new NotFoundError('Project', brandData.organization_id);
        }

        // Create the brand
        const { data: brand, error } = await supabase
          .from('brands')
          .insert({
            name: brandData.name,
            website_url: brandData.website_url,
            industry: brandData.industry,
            project_id: brandData.organization_id,
            scraping_status: 'pending',
          })
          .select()
          .single();

        if (error) {
          logger.error('Error creating brand', {
            userId: user.id,
            brandName: brandData.name
          }, error);
          throw new DatabaseError('create', error.message);
        }

        logger.info('Successfully created brand', {
          userId: user.id,
          brandId: brand.id,
          brandName: brand.name
        });

        return NextResponse.json({
          brand: {
            id: brand.id,
            name: brand.name,
            websiteUrl: brand.website_url,
            industry: brand.industry,
            scrapingStatus: brand.scraping_status,
            createdAt: brand.created_at,
          },
        });
      } catch (error) {
        if (error instanceof AuthenticationError) {
          return NextResponse.json({ error: error.message }, { status: 401 });
        }
        if (error instanceof NotFoundError) {
          return NextResponse.json({ error: error.message }, { status: 404 });
        }
        if (error instanceof ValidationError) {
          return createValidationErrorResponse(error);
        }
        if (error instanceof DatabaseError) {
          return NextResponse.json({ error: 'Database error occurred' }, { status: 500 });
        }

        logger.error('Unexpected error in POST /api/brands', {}, error as Error);
        return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
      }
    });
  });
}
