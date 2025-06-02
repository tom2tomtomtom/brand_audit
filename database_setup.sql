-- =====================================================
-- Brand Audit Tool - Complete Database Schema
-- =====================================================

-- Enable necessary extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Create custom types
CREATE TYPE user_role AS ENUM ('admin', 'editor', 'viewer');
CREATE TYPE member_role AS ENUM ('owner', 'admin', 'member');
CREATE TYPE subscription_tier AS ENUM ('free', 'pro', 'enterprise');
CREATE TYPE project_status AS ENUM ('draft', 'active', 'completed', 'archived');
CREATE TYPE processing_status AS ENUM ('pending', 'in_progress', 'completed', 'failed');
CREATE TYPE asset_type AS ENUM ('logo', 'image', 'document', 'video');
CREATE TYPE analysis_type AS ENUM ('positioning', 'visual', 'competitive', 'sentiment');
CREATE TYPE presentation_status AS ENUM ('draft', 'generating', 'completed', 'failed');

-- =====================================================
-- TABLES
-- =====================================================

-- Users table (extends Supabase auth.users)
CREATE TABLE users (
  id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  email TEXT UNIQUE NOT NULL,
  full_name TEXT,
  avatar_url TEXT,
  role user_role DEFAULT 'viewer',
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Organizations table
CREATE TABLE organizations (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  name TEXT NOT NULL,
  slug TEXT UNIQUE NOT NULL,
  logo_url TEXT,
  subscription_tier subscription_tier DEFAULT 'free',
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Organization members table
CREATE TABLE organization_members (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  role member_role DEFAULT 'member',
  created_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(organization_id, user_id)
);

-- Projects table
CREATE TABLE projects (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
  name TEXT NOT NULL,
  description TEXT,
  status project_status DEFAULT 'draft',
  created_by UUID NOT NULL REFERENCES users(id),
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Brands table
CREATE TABLE brands (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
  name TEXT NOT NULL,
  website_url TEXT NOT NULL,
  logo_url TEXT,
  industry TEXT,
  description TEXT,
  scraping_status processing_status DEFAULT 'pending',
  analysis_status processing_status DEFAULT 'pending',
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Assets table
CREATE TABLE assets (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  brand_id UUID NOT NULL REFERENCES brands(id) ON DELETE CASCADE,
  type asset_type NOT NULL,
  url TEXT NOT NULL,
  filename TEXT NOT NULL,
  file_size INTEGER NOT NULL,
  mime_type TEXT NOT NULL,
  width INTEGER,
  height INTEGER,
  alt_text TEXT,
  metadata JSONB,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Campaigns table
CREATE TABLE campaigns (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  brand_id UUID NOT NULL REFERENCES brands(id) ON DELETE CASCADE,
  name TEXT NOT NULL,
  description TEXT,
  start_date DATE,
  end_date DATE,
  platform TEXT,
  campaign_type TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Analyses table
CREATE TABLE analyses (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  brand_id UUID NOT NULL REFERENCES brands(id) ON DELETE CASCADE,
  type analysis_type NOT NULL,
  status processing_status DEFAULT 'pending',
  results JSONB,
  confidence_score DECIMAL(3,2),
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Presentations table
CREATE TABLE presentations (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
  name TEXT NOT NULL,
  template TEXT NOT NULL,
  status presentation_status DEFAULT 'draft',
  slides_data JSONB,
  export_url TEXT,
  created_by UUID NOT NULL REFERENCES users(id),
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Audit logs table
CREATE TABLE audit_logs (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES users(id),
  organization_id UUID REFERENCES organizations(id),
  action TEXT NOT NULL,
  resource_type TEXT NOT NULL,
  resource_id UUID,
  metadata JSONB,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- =====================================================
-- INDEXES
-- =====================================================

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_organizations_slug ON organizations(slug);
CREATE INDEX idx_organization_members_org_id ON organization_members(organization_id);
CREATE INDEX idx_organization_members_user_id ON organization_members(user_id);
CREATE INDEX idx_projects_org_id ON projects(organization_id);
CREATE INDEX idx_projects_created_by ON projects(created_by);
CREATE INDEX idx_brands_project_id ON brands(project_id);
CREATE INDEX idx_brands_website_url ON brands(website_url);
CREATE INDEX idx_assets_brand_id ON assets(brand_id);
CREATE INDEX idx_assets_type ON assets(type);
CREATE INDEX idx_campaigns_brand_id ON campaigns(brand_id);
CREATE INDEX idx_analyses_brand_id ON analyses(brand_id);
CREATE INDEX idx_analyses_type ON analyses(type);
CREATE INDEX idx_presentations_project_id ON presentations(project_id);
CREATE INDEX idx_audit_logs_user_id ON audit_logs(user_id);
CREATE INDEX idx_audit_logs_org_id ON audit_logs(organization_id);
CREATE INDEX idx_audit_logs_created_at ON audit_logs(created_at);

-- Full-text search indexes
CREATE INDEX idx_brands_search ON brands USING gin(to_tsvector('english', name || ' ' || COALESCE(description, '')));
CREATE INDEX idx_assets_search ON assets USING gin(to_tsvector('english', filename || ' ' || COALESCE(alt_text, '')));

-- =====================================================
-- TRIGGERS
-- =====================================================

-- Create updated_at trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ language 'plpgsql';

-- Apply updated_at triggers
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_organizations_updated_at BEFORE UPDATE ON organizations FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_projects_updated_at BEFORE UPDATE ON projects FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_brands_updated_at BEFORE UPDATE ON brands FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_analyses_updated_at BEFORE UPDATE ON analyses FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_presentations_updated_at BEFORE UPDATE ON presentations FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- =====================================================
-- ROW LEVEL SECURITY (RLS)
-- =====================================================

-- Enable RLS on all tables
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE organizations ENABLE ROW LEVEL SECURITY;
ALTER TABLE organization_members ENABLE ROW LEVEL SECURITY;
ALTER TABLE projects ENABLE ROW LEVEL SECURITY;
ALTER TABLE brands ENABLE ROW LEVEL SECURITY;
ALTER TABLE assets ENABLE ROW LEVEL SECURITY;
ALTER TABLE campaigns ENABLE ROW LEVEL SECURITY;
ALTER TABLE analyses ENABLE ROW LEVEL SECURITY;
ALTER TABLE presentations ENABLE ROW LEVEL SECURITY;
ALTER TABLE audit_logs ENABLE ROW LEVEL SECURITY;

-- =====================================================
-- HELPER FUNCTIONS
-- =====================================================

-- Helper function to get user's organizations
CREATE OR REPLACE FUNCTION get_user_organizations(user_uuid UUID)
RETURNS TABLE(organization_id UUID, role member_role) AS $$
BEGIN
  RETURN QUERY
  SELECT om.organization_id, om.role
  FROM organization_members om
  WHERE om.user_id = user_uuid;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Helper function to check if user is organization member
CREATE OR REPLACE FUNCTION is_organization_member(user_uuid UUID, org_uuid UUID)
RETURNS BOOLEAN AS $$
BEGIN
  RETURN EXISTS (
    SELECT 1 FROM organization_members
    WHERE user_id = user_uuid AND organization_id = org_uuid
  );
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Helper function to check if user is organization admin/owner
CREATE OR REPLACE FUNCTION is_organization_admin(user_uuid UUID, org_uuid UUID)
RETURNS BOOLEAN AS $$
BEGIN
  RETURN EXISTS (
    SELECT 1 FROM organization_members
    WHERE user_id = user_uuid
    AND organization_id = org_uuid
    AND role IN ('owner', 'admin')
  );
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- =====================================================
-- RLS POLICIES
-- =====================================================

-- Users policies
CREATE POLICY "Users can view their own profile" ON users
  FOR SELECT USING (auth.uid() = id);

CREATE POLICY "Users can update their own profile" ON users
  FOR UPDATE USING (auth.uid() = id);

-- Organizations policies
CREATE POLICY "Users can view organizations they belong to" ON organizations
  FOR SELECT USING (
    id IN (SELECT organization_id FROM get_user_organizations(auth.uid()))
  );

CREATE POLICY "Organization admins can update organization" ON organizations
  FOR UPDATE USING (
    is_organization_admin(auth.uid(), id)
  );

CREATE POLICY "Users can create organizations" ON organizations
  FOR INSERT WITH CHECK (true);

-- Organization members policies
CREATE POLICY "Users can view organization members of their organizations" ON organization_members
  FOR SELECT USING (
    organization_id IN (SELECT organization_id FROM get_user_organizations(auth.uid()))
  );

CREATE POLICY "Organization admins can manage members" ON organization_members
  FOR ALL USING (
    is_organization_admin(auth.uid(), organization_id)
  );

CREATE POLICY "Users can join organizations" ON organization_members
  FOR INSERT WITH CHECK (
    user_id = auth.uid() OR
    is_organization_admin(auth.uid(), organization_id)
  );

-- Projects policies
CREATE POLICY "Users can view projects in their organizations" ON projects
  FOR SELECT USING (
    is_organization_member(auth.uid(), organization_id)
  );

CREATE POLICY "Organization members can create projects" ON projects
  FOR INSERT WITH CHECK (
    is_organization_member(auth.uid(), organization_id) AND
    created_by = auth.uid()
  );

CREATE POLICY "Project creators and org admins can update projects" ON projects
  FOR UPDATE USING (
    created_by = auth.uid() OR
    is_organization_admin(auth.uid(), organization_id)
  );

CREATE POLICY "Project creators and org admins can delete projects" ON projects
  FOR DELETE USING (
    created_by = auth.uid() OR
    is_organization_admin(auth.uid(), organization_id)
  );

-- Brands policies
CREATE POLICY "Users can view brands in accessible projects" ON brands
  FOR SELECT USING (
    project_id IN (
      SELECT p.id FROM projects p
      WHERE is_organization_member(auth.uid(), p.organization_id)
    )
  );

CREATE POLICY "Users can manage brands in accessible projects" ON brands
  FOR ALL USING (
    project_id IN (
      SELECT p.id FROM projects p
      WHERE is_organization_member(auth.uid(), p.organization_id)
    )
  );

-- Assets policies
CREATE POLICY "Users can view assets of accessible brands" ON assets
  FOR SELECT USING (
    brand_id IN (
      SELECT b.id FROM brands b
      JOIN projects p ON b.project_id = p.id
      WHERE is_organization_member(auth.uid(), p.organization_id)
    )
  );

CREATE POLICY "Users can manage assets of accessible brands" ON assets
  FOR ALL USING (
    brand_id IN (
      SELECT b.id FROM brands b
      JOIN projects p ON b.project_id = p.id
      WHERE is_organization_member(auth.uid(), p.organization_id)
    )
  );

-- Campaigns policies
CREATE POLICY "Users can view campaigns of accessible brands" ON campaigns
  FOR SELECT USING (
    brand_id IN (
      SELECT b.id FROM brands b
      JOIN projects p ON b.project_id = p.id
      WHERE is_organization_member(auth.uid(), p.organization_id)
    )
  );

CREATE POLICY "Users can manage campaigns of accessible brands" ON campaigns
  FOR ALL USING (
    brand_id IN (
      SELECT b.id FROM brands b
      JOIN projects p ON b.project_id = p.id
      WHERE is_organization_member(auth.uid(), p.organization_id)
    )
  );

-- Analyses policies
CREATE POLICY "Users can view analyses of accessible brands" ON analyses
  FOR SELECT USING (
    brand_id IN (
      SELECT b.id FROM brands b
      JOIN projects p ON b.project_id = p.id
      WHERE is_organization_member(auth.uid(), p.organization_id)
    )
  );

CREATE POLICY "Users can manage analyses of accessible brands" ON analyses
  FOR ALL USING (
    brand_id IN (
      SELECT b.id FROM brands b
      JOIN projects p ON b.project_id = p.id
      WHERE is_organization_member(auth.uid(), p.organization_id)
    )
  );

-- Presentations policies
CREATE POLICY "Users can view presentations in accessible projects" ON presentations
  FOR SELECT USING (
    project_id IN (
      SELECT p.id FROM projects p
      WHERE is_organization_member(auth.uid(), p.organization_id)
    )
  );

CREATE POLICY "Users can create presentations in accessible projects" ON presentations
  FOR INSERT WITH CHECK (
    project_id IN (
      SELECT p.id FROM projects p
      WHERE is_organization_member(auth.uid(), p.organization_id)
    ) AND created_by = auth.uid()
  );

CREATE POLICY "Presentation creators can update their presentations" ON presentations
  FOR UPDATE USING (
    created_by = auth.uid() OR
    project_id IN (
      SELECT p.id FROM projects p
      WHERE is_organization_admin(auth.uid(), p.organization_id)
    )
  );

CREATE POLICY "Presentation creators can delete their presentations" ON presentations
  FOR DELETE USING (
    created_by = auth.uid() OR
    project_id IN (
      SELECT p.id FROM projects p
      WHERE is_organization_admin(auth.uid(), p.organization_id)
    )
  );

-- Audit logs policies
CREATE POLICY "Users can view audit logs of their organizations" ON audit_logs
  FOR SELECT USING (
    organization_id IN (SELECT organization_id FROM get_user_organizations(auth.uid()))
  );

CREATE POLICY "System can insert audit logs" ON audit_logs
  FOR INSERT WITH CHECK (true);

-- =====================================================
-- BUSINESS LOGIC FUNCTIONS
-- =====================================================

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
  brands_data JSONB,
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

  -- Insert brands from JSONB array
  FOR brand_data IN SELECT * FROM jsonb_array_elements(brands_data)
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

-- =====================================================
-- STORAGE BUCKETS (For Supabase)
-- =====================================================

-- Create storage buckets
INSERT INTO storage.buckets (id, name, public) VALUES
  ('brand-logos', 'brand-logos', true),
  ('campaign-assets', 'campaign-assets', false),
  ('brand-guidelines', 'brand-guidelines', false),
  ('presentations', 'presentations', false),
  ('temp-uploads', 'temp-uploads', false)
ON CONFLICT (id) DO NOTHING;

-- =====================================================
-- SAMPLE DATA (Optional - for development/testing)
-- =====================================================

-- Sample user (will be created by Supabase Auth)
-- INSERT INTO users (id, email, full_name, role) VALUES
--   ('00000000-0000-0000-0000-000000000001', 'demo@example.com', 'Demo User', 'admin')
-- ON CONFLICT (id) DO NOTHING;

-- Sample organization
-- INSERT INTO organizations (id, name, slug, subscription_tier) VALUES
--   ('00000000-0000-0000-0000-000000000001', 'Demo Company', 'demo-company', 'pro')
-- ON CONFLICT (id) DO NOTHING;

-- Sample organization membership
-- INSERT INTO organization_members (organization_id, user_id, role) VALUES
--   ('00000000-0000-0000-0000-000000000001', '00000000-0000-0000-0000-000000000001', 'owner')
-- ON CONFLICT (organization_id, user_id) DO NOTHING;

-- =====================================================
-- UTILITY FUNCTIONS
-- =====================================================

-- Function to clean up old temp uploads
CREATE OR REPLACE FUNCTION cleanup_temp_uploads()
RETURNS void AS $$
BEGIN
  DELETE FROM storage.objects
  WHERE bucket_id = 'temp-uploads'
  AND created_at < NOW() - INTERVAL '24 hours';
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Function to get organization stats
CREATE OR REPLACE FUNCTION get_organization_stats(org_uuid UUID)
RETURNS TABLE(
  total_projects BIGINT,
  total_brands BIGINT,
  total_assets BIGINT,
  completed_analyses BIGINT,
  active_members BIGINT
) AS $$
BEGIN
  RETURN QUERY
  SELECT
    COUNT(DISTINCT p.id) as total_projects,
    COUNT(DISTINCT b.id) as total_brands,
    COUNT(DISTINCT a.id) as total_assets,
    COUNT(DISTINCT CASE WHEN an.status = 'completed' THEN an.id END) as completed_analyses,
    COUNT(DISTINCT om.user_id) as active_members
  FROM organizations o
  LEFT JOIN projects p ON o.id = p.organization_id
  LEFT JOIN brands b ON p.id = b.project_id
  LEFT JOIN assets a ON b.id = a.brand_id
  LEFT JOIN analyses an ON b.id = an.brand_id
  LEFT JOIN organization_members om ON o.id = om.organization_id
  WHERE o.id = org_uuid;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- =====================================================
-- COMPLETION MESSAGE
-- =====================================================

DO $$
BEGIN
  RAISE NOTICE '✅ Brand Audit Tool database schema setup completed successfully!';
  RAISE NOTICE '';
  RAISE NOTICE '📋 Summary:';
  RAISE NOTICE '   - Tables: 10 core tables created';
  RAISE NOTICE '   - Indexes: Performance indexes added';
  RAISE NOTICE '   - RLS: Row Level Security enabled';
  RAISE NOTICE '   - Functions: Business logic functions created';
  RAISE NOTICE '   - Storage: Buckets configured';
  RAISE NOTICE '';
  RAISE NOTICE '🚀 Next steps:';
  RAISE NOTICE '   1. Set up Supabase project';
  RAISE NOTICE '   2. Run this SQL in your Supabase SQL editor';
  RAISE NOTICE '   3. Configure environment variables';
  RAISE NOTICE '   4. Start building your application!';
  RAISE NOTICE '';
END $$;
