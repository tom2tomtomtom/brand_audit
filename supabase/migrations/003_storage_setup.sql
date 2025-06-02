-- Create storage buckets
INSERT INTO storage.buckets (id, name, public) VALUES 
  ('brand-logos', 'brand-logos', true),
  ('campaign-assets', 'campaign-assets', false),
  ('brand-guidelines', 'brand-guidelines', false),
  ('presentations', 'presentations', false),
  ('temp-uploads', 'temp-uploads', false);

-- Storage policies for brand-logos bucket (public)
CREATE POLICY "Public can view brand logos" ON storage.objects
  FOR SELECT USING (bucket_id = 'brand-logos');

CREATE POLICY "Authenticated users can upload brand logos" ON storage.objects
  FOR INSERT WITH CHECK (
    bucket_id = 'brand-logos' AND
    auth.role() = 'authenticated'
  );

CREATE POLICY "Users can update their organization's brand logos" ON storage.objects
  FOR UPDATE USING (
    bucket_id = 'brand-logos' AND
    auth.role() = 'authenticated'
  );

CREATE POLICY "Users can delete their organization's brand logos" ON storage.objects
  FOR DELETE USING (
    bucket_id = 'brand-logos' AND
    auth.role() = 'authenticated'
  );

-- Storage policies for campaign-assets bucket (private)
CREATE POLICY "Users can view campaign assets of accessible brands" ON storage.objects
  FOR SELECT USING (
    bucket_id = 'campaign-assets' AND
    auth.role() = 'authenticated' AND
    (storage.foldername(name))[1] IN (
      SELECT b.id::text FROM brands b
      JOIN projects p ON b.project_id = p.id
      WHERE EXISTS (
        SELECT 1 FROM organization_members om
        WHERE om.user_id = auth.uid() AND om.organization_id = p.organization_id
      )
    )
  );

CREATE POLICY "Users can upload campaign assets for accessible brands" ON storage.objects
  FOR INSERT WITH CHECK (
    bucket_id = 'campaign-assets' AND
    auth.role() = 'authenticated' AND
    (storage.foldername(name))[1] IN (
      SELECT b.id::text FROM brands b
      JOIN projects p ON b.project_id = p.id
      WHERE EXISTS (
        SELECT 1 FROM organization_members om
        WHERE om.user_id = auth.uid() AND om.organization_id = p.organization_id
      )
    )
  );

CREATE POLICY "Users can update campaign assets for accessible brands" ON storage.objects
  FOR UPDATE USING (
    bucket_id = 'campaign-assets' AND
    auth.role() = 'authenticated' AND
    (storage.foldername(name))[1] IN (
      SELECT b.id::text FROM brands b
      JOIN projects p ON b.project_id = p.id
      WHERE EXISTS (
        SELECT 1 FROM organization_members om
        WHERE om.user_id = auth.uid() AND om.organization_id = p.organization_id
      )
    )
  );

CREATE POLICY "Users can delete campaign assets for accessible brands" ON storage.objects
  FOR DELETE USING (
    bucket_id = 'campaign-assets' AND
    auth.role() = 'authenticated' AND
    (storage.foldername(name))[1] IN (
      SELECT b.id::text FROM brands b
      JOIN projects p ON b.project_id = p.id
      WHERE EXISTS (
        SELECT 1 FROM organization_members om
        WHERE om.user_id = auth.uid() AND om.organization_id = p.organization_id
      )
    )
  );

-- Storage policies for brand-guidelines bucket (private)
CREATE POLICY "Users can view brand guidelines of accessible brands" ON storage.objects
  FOR SELECT USING (
    bucket_id = 'brand-guidelines' AND
    auth.role() = 'authenticated' AND
    (storage.foldername(name))[1] IN (
      SELECT b.id::text FROM brands b
      JOIN projects p ON b.project_id = p.id
      WHERE EXISTS (
        SELECT 1 FROM organization_members om
        WHERE om.user_id = auth.uid() AND om.organization_id = p.organization_id
      )
    )
  );

CREATE POLICY "Users can upload brand guidelines for accessible brands" ON storage.objects
  FOR INSERT WITH CHECK (
    bucket_id = 'brand-guidelines' AND
    auth.role() = 'authenticated' AND
    (storage.foldername(name))[1] IN (
      SELECT b.id::text FROM brands b
      JOIN projects p ON b.project_id = p.id
      WHERE EXISTS (
        SELECT 1 FROM organization_members om
        WHERE om.user_id = auth.uid() AND om.organization_id = p.organization_id
      )
    )
  );

-- Storage policies for presentations bucket (private)
CREATE POLICY "Users can view presentations of accessible projects" ON storage.objects
  FOR SELECT USING (
    bucket_id = 'presentations' AND
    auth.role() = 'authenticated' AND
    (storage.foldername(name))[1] IN (
      SELECT p.id::text FROM projects p
      WHERE EXISTS (
        SELECT 1 FROM organization_members om
        WHERE om.user_id = auth.uid() AND om.organization_id = p.organization_id
      )
    )
  );

CREATE POLICY "Users can upload presentations for accessible projects" ON storage.objects
  FOR INSERT WITH CHECK (
    bucket_id = 'presentations' AND
    auth.role() = 'authenticated' AND
    (storage.foldername(name))[1] IN (
      SELECT p.id::text FROM projects p
      WHERE EXISTS (
        SELECT 1 FROM organization_members om
        WHERE om.user_id = auth.uid() AND om.organization_id = p.organization_id
      )
    )
  );

-- Storage policies for temp-uploads bucket (private)
CREATE POLICY "Users can manage their own temp uploads" ON storage.objects
  FOR ALL USING (
    bucket_id = 'temp-uploads' AND
    auth.role() = 'authenticated' AND
    (storage.foldername(name))[1] = auth.uid()::text
  );

-- Function to clean up old temp uploads
CREATE OR REPLACE FUNCTION cleanup_temp_uploads()
RETURNS void AS $$
BEGIN
  DELETE FROM storage.objects
  WHERE bucket_id = 'temp-uploads'
  AND created_at < NOW() - INTERVAL '24 hours';
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Schedule cleanup function (requires pg_cron extension)
-- SELECT cron.schedule('cleanup-temp-uploads', '0 2 * * *', 'SELECT cleanup_temp_uploads();');
