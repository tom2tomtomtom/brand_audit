import { SupabaseClient } from '@supabase/supabase-js';
import { createServerSupabase } from './supabase-server';

/**
 * Optimized database query utilities for the Brand Audit Tool
 * 
 * Provides efficient query patterns to prevent N+1 queries and optimize
 * data fetching with proper joins and selective field selection.
 * 
 * @module DatabaseOptimizations
 */

/**
 * Options for project queries
 */
export interface ProjectQueryOptions {
  /** Include brand details */
  includeBrands?: boolean;
  /** Include analysis results */
  includeAnalyses?: boolean;
  /** Include asset counts */
  includeAssetCounts?: boolean;
  /** Limit number of results */
  limit?: number;
  /** Offset for pagination */
  offset?: number;
  /** Filter by status */
  status?: 'draft' | 'active' | 'completed' | 'archived';
}

/**
 * Options for brand queries
 */
export interface BrandQueryOptions {
  /** Include visual data */
  includeVisualData?: boolean;
  /** Include latest analyses */
  includeAnalyses?: boolean;
  /** Include asset details */
  includeAssets?: boolean;
  /** Maximum number of assets to include */
  assetLimit?: number;
}

/**
 * Fetch projects with optimized queries
 * 
 * Uses single query with nested selects to avoid N+1 problems
 * 
 * @param {string} organizationId - Organization ID to filter by
 * @param {ProjectQueryOptions} options - Query options
 * @returns {Promise<any[]>} Array of projects with related data
 * 
 * @example
 * ```typescript
 * const projects = await getProjectsOptimized(orgId, {
 *   includeBrands: true,
 *   includeAnalyses: true,
 *   limit: 20
 * });
 * ```
 */
export async function getProjectsOptimized(
  organizationId: string,
  options: ProjectQueryOptions = {}
): Promise<any[]> {
  const supabase = createServerSupabase();
  
  let query = supabase
    .from('projects')
    .select(`
      id,
      name,
      description,
      status,
      created_at,
      updated_at,
      created_by
    `)
    .eq('organization_id', organizationId);

  // Add brand data with counts
  if (options.includeBrands) {
    query = query.select(`
      *,
      brands!inner (
        id,
        name,
        website_url,
        industry,
        scraping_status,
        analysis_status,
        ${options.includeAssetCounts ? '_asset_count:assets(count)' : ''},
        ${options.includeAnalyses ? `analyses (
          id,
          type,
          status,
          confidence_score,
          created_at
        )` : ''}
      )
    `);
  }

  // Apply filters
  if (options.status) {
    query = query.eq('status', options.status);
  }

  // Apply pagination
  if (options.limit) {
    query = query.limit(options.limit);
  }
  if (options.offset) {
    query = query.range(options.offset, options.offset + (options.limit || 10) - 1);
  }

  // Order by most recently updated
  query = query.order('updated_at', { ascending: false });

  const { data, error } = await query;

  if (error) throw error;
  return data || [];
}

/**
 * Fetch a single brand with all related data in one query
 * 
 * @param {string} brandId - Brand ID
 * @param {BrandQueryOptions} options - Query options
 * @returns {Promise<any>} Brand with related data
 */
export async function getBrandWithDataOptimized(
  brandId: string,
  options: BrandQueryOptions = {}
): Promise<any> {
  const supabase = createServerSupabase();
  
  let selectQuery = `
    id,
    name,
    website_url,
    logo_url,
    industry,
    description,
    scraping_status,
    analysis_status,
    created_at,
    updated_at
  `;

  // Include visual data if requested
  if (options.includeVisualData) {
    selectQuery += `,
    visual_data
    `;
  }

  // Include analyses if requested
  if (options.includeAnalyses) {
    selectQuery += `,
    analyses!brand_id (
      id,
      type,
      status,
      results,
      confidence_score,
      created_at
    )
    `;
  }

  // Include assets if requested
  if (options.includeAssets) {
    selectQuery += `,
    assets!brand_id (
      id,
      type,
      url,
      filename,
      file_size,
      mime_type,
      alt_text,
      created_at
    )
    `;
    
    if (options.assetLimit) {
      selectQuery += `.limit(${options.assetLimit})`;
    }
  }

  const { data, error } = await supabase
    .from('brands')
    .select(selectQuery)
    .eq('id', brandId)
    .single();

  if (error) throw error;
  return data;
}

/**
 * Batch fetch multiple brands efficiently
 * 
 * @param {string[]} brandIds - Array of brand IDs
 * @param {BrandQueryOptions} options - Query options
 * @returns {Promise<any[]>} Array of brands with related data
 */
export async function getBrandsBatchOptimized(
  brandIds: string[],
  options: BrandQueryOptions = {}
): Promise<any[]> {
  const supabase = createServerSupabase();
  
  let query = supabase
    .from('brands')
    .select(`
      id,
      name,
      website_url,
      industry,
      scraping_status,
      analysis_status,
      ${options.includeAnalyses ? `analyses (
        type,
        status,
        confidence_score
      )` : ''},
      ${options.includeAssets ? `_asset_count:assets(count)` : ''}
    `)
    .in('id', brandIds);

  const { data, error } = await query;

  if (error) throw error;
  return data || [];
}

/**
 * Get project statistics with optimized aggregation
 * 
 * @param {string} projectId - Project ID
 * @returns {Promise<any>} Project statistics
 */
export async function getProjectStatsOptimized(projectId: string): Promise<{
  totalBrands: number;
  completedAnalyses: number;
  totalAssets: number;
  averageConfidence: number;
}> {
  const supabase = createServerSupabase();

  // Use RPC function for complex aggregation
  const { data, error } = await supabase.rpc('get_project_stats', {
    project_id: projectId
  });

  if (error) throw error;

  return data || {
    totalBrands: 0,
    completedAnalyses: 0,
    totalAssets: 0,
    averageConfidence: 0
  };
}

/**
 * Search brands across organization with full-text search
 * 
 * @param {string} organizationId - Organization ID
 * @param {string} searchTerm - Search term
 * @param {number} limit - Maximum results
 * @returns {Promise<any[]>} Search results
 */
export async function searchBrandsOptimized(
  organizationId: string,
  searchTerm: string,
  limit = 20
): Promise<any[]> {
  const supabase = createServerSupabase();

  const { data, error } = await supabase.rpc('search_brands_fts', {
    org_id: organizationId,
    search_query: searchTerm,
    result_limit: limit
  });

  if (error) throw error;
  return data || [];
}

/**
 * Get organization dashboard data in single query
 * 
 * @param {string} organizationId - Organization ID
 * @returns {Promise<any>} Dashboard data
 */
export async function getOrganizationDashboardData(
  organizationId: string
): Promise<{
  recentProjects: any[];
  brandStats: any;
  activityLog: any[];
}> {
  const supabase = createServerSupabase();

  // Parallel queries for dashboard data
  const [projectsResult, statsResult, activityResult] = await Promise.all([
    // Recent projects with brand counts
    supabase
      .from('projects')
      .select(`
        id,
        name,
        status,
        updated_at,
        _brand_count:brands(count)
      `)
      .eq('organization_id', organizationId)
      .order('updated_at', { ascending: false })
      .limit(5),

    // Organization statistics
    supabase.rpc('get_organization_stats', {
      org_uuid: organizationId
    }),

    // Recent activity
    supabase
      .from('audit_logs')
      .select(`
        id,
        action,
        resource_type,
        created_at,
        user:users!user_id(full_name, email)
      `)
      .eq('organization_id', organizationId)
      .order('created_at', { ascending: false })
      .limit(10)
  ]);

  if (projectsResult.error) throw projectsResult.error;
  if (statsResult.error) throw statsResult.error;
  if (activityResult.error) throw activityResult.error;

  return {
    recentProjects: projectsResult.data || [],
    brandStats: statsResult.data || {},
    activityLog: activityResult.data || []
  };
}

/**
 * Batch update brand statuses efficiently
 * 
 * @param {string[]} brandIds - Array of brand IDs
 * @param {string} status - New status
 * @returns {Promise<void>}
 */
export async function updateBrandStatusesBatch(
  brandIds: string[],
  status: 'pending' | 'in_progress' | 'completed' | 'failed'
): Promise<void> {
  const supabase = createServerSupabase();

  const { error } = await supabase
    .from('brands')
    .update({ 
      analysis_status: status,
      updated_at: new Date().toISOString()
    })
    .in('id', brandIds);

  if (error) throw error;
}

/**
 * Create SQL functions for complex queries
 * These should be run once during database setup
 */
export const optimizedSQLFunctions = `
-- Function to get project statistics
CREATE OR REPLACE FUNCTION get_project_stats(project_id UUID)
RETURNS TABLE(
  total_brands BIGINT,
  completed_analyses BIGINT,
  total_assets BIGINT,
  average_confidence NUMERIC
) AS $$
BEGIN
  RETURN QUERY
  SELECT
    COUNT(DISTINCT b.id) as total_brands,
    COUNT(DISTINCT CASE WHEN a.status = 'completed' THEN a.id END) as completed_analyses,
    COUNT(DISTINCT ast.id) as total_assets,
    AVG(a.confidence_score)::NUMERIC as average_confidence
  FROM brands b
  LEFT JOIN analyses a ON b.id = a.brand_id
  LEFT JOIN assets ast ON b.id = ast.brand_id
  WHERE b.project_id = get_project_stats.project_id;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Function for full-text search on brands
CREATE OR REPLACE FUNCTION search_brands_fts(
  org_id UUID,
  search_query TEXT,
  result_limit INTEGER DEFAULT 20
)
RETURNS TABLE(
  brand_id UUID,
  brand_name TEXT,
  website_url TEXT,
  industry TEXT,
  project_name TEXT,
  rank REAL
) AS $$
BEGIN
  RETURN QUERY
  SELECT
    b.id as brand_id,
    b.name as brand_name,
    b.website_url,
    b.industry,
    p.name as project_name,
    ts_rank(
      to_tsvector('english', b.name || ' ' || COALESCE(b.description, '') || ' ' || COALESCE(b.industry, '')),
      plainto_tsquery('english', search_query)
    ) as rank
  FROM brands b
  JOIN projects p ON b.project_id = p.id
  WHERE p.organization_id = org_id
  AND to_tsvector('english', b.name || ' ' || COALESCE(b.description, '') || ' ' || COALESCE(b.industry, ''))
    @@ plainto_tsquery('english', search_query)
  ORDER BY rank DESC
  LIMIT result_limit;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;
`;
