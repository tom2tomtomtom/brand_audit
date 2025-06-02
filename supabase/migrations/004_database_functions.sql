-- Function to create a new organization with the user as owner
CREATE OR REPLACE FUNCTION create_organization_with_owner(
  org_name TEXT,
  org_slug TEXT,
  user_id UUID
)
RETURNS UUID AS $$
DECLARE
  new_org_id UUID;
BEGIN
  -- Insert organization
  INSERT INTO organizations (name, slug)
  VALUES (org_name, org_slug)
  RETURNING id INTO new_org_id;
  
  -- Add user as owner
  INSERT INTO organization_members (organization_id, user_id, role)
  VALUES (new_org_id, user_id, 'owner');
  
  -- Log the action
  INSERT INTO audit_logs (user_id, organization_id, action, resource_type, resource_id)
  VALUES (user_id, new_org_id, 'create', 'organization', new_org_id);
  
  RETURN new_org_id;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Function to create a project with multiple brands
CREATE OR REPLACE FUNCTION create_project_with_brands(
  project_data JSONB,
  brands_data JSONB[],
  user_id UUID,
  org_id UUID
)
RETURNS UUID AS $$
DECLARE
  new_project_id UUID;
  brand_data JSONB;
  new_brand_id UUID;
BEGIN
  -- Verify user is organization member
  IF NOT is_organization_member(user_id, org_id) THEN
    RAISE EXCEPTION 'User is not a member of this organization';
  END IF;
  
  -- Insert project
  INSERT INTO projects (
    organization_id,
    name,
    description,
    created_by
  )
  VALUES (
    org_id,
    project_data->>'name',
    project_data->>'description',
    user_id
  )
  RETURNING id INTO new_project_id;
  
  -- Insert brands
  FOREACH brand_data IN ARRAY brands_data
  LOOP
    INSERT INTO brands (
      project_id,
      name,
      website_url,
      industry,
      description
    )
    VALUES (
      new_project_id,
      brand_data->>'name',
      brand_data->>'website_url',
      brand_data->>'industry',
      brand_data->>'description'
    )
    RETURNING id INTO new_brand_id;
    
    -- Log brand creation
    INSERT INTO audit_logs (user_id, organization_id, action, resource_type, resource_id)
    VALUES (user_id, org_id, 'create', 'brand', new_brand_id);
  END LOOP;
  
  -- Log project creation
  INSERT INTO audit_logs (user_id, organization_id, action, resource_type, resource_id)
  VALUES (user_id, org_id, 'create', 'project', new_project_id);
  
  RETURN new_project_id;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Function to process asset upload
CREATE OR REPLACE FUNCTION process_asset_upload(
  brand_uuid UUID,
  asset_data JSONB,
  user_id UUID
)
RETURNS UUID AS $$
DECLARE
  new_asset_id UUID;
  org_id UUID;
BEGIN
  -- Get organization ID for the brand
  SELECT p.organization_id INTO org_id
  FROM brands b
  JOIN projects p ON b.project_id = p.id
  WHERE b.id = brand_uuid;
  
  -- Verify user access
  IF NOT is_organization_member(user_id, org_id) THEN
    RAISE EXCEPTION 'User does not have access to this brand';
  END IF;
  
  -- Insert asset
  INSERT INTO assets (
    brand_id,
    type,
    url,
    filename,
    file_size,
    mime_type,
    width,
    height,
    alt_text,
    metadata
  )
  VALUES (
    brand_uuid,
    (asset_data->>'type')::asset_type,
    asset_data->>'url',
    asset_data->>'filename',
    (asset_data->>'file_size')::INTEGER,
    asset_data->>'mime_type',
    (asset_data->>'width')::INTEGER,
    (asset_data->>'height')::INTEGER,
    asset_data->>'alt_text',
    asset_data->'metadata'
  )
  RETURNING id INTO new_asset_id;
  
  -- Log asset creation
  INSERT INTO audit_logs (user_id, organization_id, action, resource_type, resource_id)
  VALUES (user_id, org_id, 'create', 'asset', new_asset_id);
  
  RETURN new_asset_id;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Function to generate analysis report
CREATE OR REPLACE FUNCTION generate_analysis_report(
  brand_uuid UUID,
  analysis_types TEXT[],
  user_id UUID
)
RETURNS JSONB AS $$
DECLARE
  org_id UUID;
  analysis_type TEXT;
  analysis_id UUID;
  report JSONB := '{}';
BEGIN
  -- Get organization ID for the brand
  SELECT p.organization_id INTO org_id
  FROM brands b
  JOIN projects p ON b.project_id = p.id
  WHERE b.id = brand_uuid;
  
  -- Verify user access
  IF NOT is_organization_member(user_id, org_id) THEN
    RAISE EXCEPTION 'User does not have access to this brand';
  END IF;
  
  -- Create analysis records for each type
  FOREACH analysis_type IN ARRAY analysis_types
  LOOP
    INSERT INTO analyses (
      brand_id,
      type,
      status
    )
    VALUES (
      brand_uuid,
      analysis_type::analysis_type,
      'pending'
    )
    RETURNING id INTO analysis_id;
    
    -- Add to report
    report := jsonb_set(
      report,
      ARRAY[analysis_type],
      jsonb_build_object('id', analysis_id, 'status', 'pending')
    );
    
    -- Log analysis creation
    INSERT INTO audit_logs (user_id, organization_id, action, resource_type, resource_id)
    VALUES (user_id, org_id, 'create', 'analysis', analysis_id);
  END LOOP;
  
  RETURN report;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Function to track user activity
CREATE OR REPLACE FUNCTION track_user_activity(
  user_uuid UUID,
  org_uuid UUID,
  action_name TEXT,
  resource_type_name TEXT,
  resource_uuid UUID DEFAULT NULL,
  metadata_json JSONB DEFAULT NULL
)
RETURNS void AS $$
BEGIN
  INSERT INTO audit_logs (
    user_id,
    organization_id,
    action,
    resource_type,
    resource_id,
    metadata
  )
  VALUES (
    user_uuid,
    org_uuid,
    action_name,
    resource_type_name,
    resource_uuid,
    metadata_json
  );
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Function to get user's accessible projects with stats
CREATE OR REPLACE FUNCTION get_user_projects_with_stats(user_uuid UUID)
RETURNS TABLE(
  project_id UUID,
  project_name TEXT,
  project_description TEXT,
  project_status project_status,
  organization_id UUID,
  organization_name TEXT,
  brands_count BIGINT,
  completed_analyses_count BIGINT,
  total_assets_count BIGINT,
  created_at TIMESTAMPTZ,
  updated_at TIMESTAMPTZ
) AS $$
BEGIN
  RETURN QUERY
  SELECT 
    p.id,
    p.name,
    p.description,
    p.status,
    p.organization_id,
    o.name,
    COUNT(DISTINCT b.id) as brands_count,
    COUNT(DISTINCT CASE WHEN a.status = 'completed' THEN a.id END) as completed_analyses_count,
    COUNT(DISTINCT ast.id) as total_assets_count,
    p.created_at,
    p.updated_at
  FROM projects p
  JOIN organizations o ON p.organization_id = o.id
  JOIN organization_members om ON o.id = om.organization_id
  LEFT JOIN brands b ON p.id = b.project_id
  LEFT JOIN analyses a ON b.id = a.brand_id
  LEFT JOIN assets ast ON b.id = ast.brand_id
  WHERE om.user_id = user_uuid
  GROUP BY p.id, p.name, p.description, p.status, p.organization_id, o.name, p.created_at, p.updated_at
  ORDER BY p.updated_at DESC;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Function to search brands across user's organizations
CREATE OR REPLACE FUNCTION search_brands(
  user_uuid UUID,
  search_term TEXT,
  limit_count INTEGER DEFAULT 20,
  offset_count INTEGER DEFAULT 0
)
RETURNS TABLE(
  brand_id UUID,
  brand_name TEXT,
  website_url TEXT,
  industry TEXT,
  project_name TEXT,
  organization_name TEXT,
  scraping_status processing_status,
  analysis_status processing_status,
  assets_count BIGINT
) AS $$
BEGIN
  RETURN QUERY
  SELECT 
    b.id,
    b.name,
    b.website_url,
    b.industry,
    p.name,
    o.name,
    b.scraping_status,
    b.analysis_status,
    COUNT(a.id) as assets_count
  FROM brands b
  JOIN projects p ON b.project_id = p.id
  JOIN organizations o ON p.organization_id = o.id
  JOIN organization_members om ON o.id = om.organization_id
  LEFT JOIN assets a ON b.id = a.brand_id
  WHERE om.user_id = user_uuid
  AND (
    b.name ILIKE '%' || search_term || '%' OR
    b.description ILIKE '%' || search_term || '%' OR
    b.industry ILIKE '%' || search_term || '%' OR
    b.website_url ILIKE '%' || search_term || '%'
  )
  GROUP BY b.id, b.name, b.website_url, b.industry, p.name, o.name, b.scraping_status, b.analysis_status
  ORDER BY b.updated_at DESC
  LIMIT limit_count OFFSET offset_count;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;
