-- Enable Row Level Security on all tables
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
