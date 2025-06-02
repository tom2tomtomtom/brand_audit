-- =====================================================
-- Brand Audit Tool - Schema Verification Script
-- =====================================================

-- This script verifies that all components of the database schema
-- have been created successfully

SELECT '🔍 CHECKING DATABASE SCHEMA...' as status;

-- =====================================================
-- 1. CHECK EXTENSIONS
-- =====================================================

SELECT '📦 EXTENSIONS' as section;

SELECT 
  extname as extension_name,
  extversion as version,
  CASE WHEN extname IN ('uuid-ossp', 'pg_trgm') THEN '✅' ELSE '❌' END as status
FROM pg_extension 
WHERE extname IN ('uuid-ossp', 'pg_trgm')
ORDER BY extname;

-- =====================================================
-- 2. CHECK CUSTOM TYPES
-- =====================================================

SELECT '🏷️ CUSTOM TYPES' as section;

SELECT 
  t.typname as type_name,
  string_agg(e.enumlabel, ', ' ORDER BY e.enumsortorder) as enum_values,
  '✅' as status
FROM pg_type t 
JOIN pg_enum e ON t.oid = e.enumtypid 
WHERE t.typname IN (
  'user_role', 'member_role', 'subscription_tier', 
  'project_status', 'processing_status', 'asset_type', 
  'analysis_type', 'presentation_status'
)
GROUP BY t.typname
ORDER BY t.typname;

-- =====================================================
-- 3. CHECK TABLES
-- =====================================================

SELECT '📋 TABLES' as section;

SELECT 
  table_name,
  CASE 
    WHEN table_name IN (
      'users', 'organizations', 'organization_members', 'projects', 
      'brands', 'assets', 'campaigns', 'analyses', 'presentations', 'audit_logs'
    ) THEN '✅'
    ELSE '❓'
  END as status,
  (
    SELECT COUNT(*) 
    FROM information_schema.columns 
    WHERE table_name = t.table_name AND table_schema = 'public'
  ) as column_count
FROM information_schema.tables t
WHERE table_schema = 'public' 
AND table_type = 'BASE TABLE'
ORDER BY 
  CASE table_name
    WHEN 'users' THEN 1
    WHEN 'organizations' THEN 2
    WHEN 'organization_members' THEN 3
    WHEN 'projects' THEN 4
    WHEN 'brands' THEN 5
    WHEN 'assets' THEN 6
    WHEN 'campaigns' THEN 7
    WHEN 'analyses' THEN 8
    WHEN 'presentations' THEN 9
    WHEN 'audit_logs' THEN 10
    ELSE 99
  END;

-- =====================================================
-- 4. CHECK TABLE COLUMNS
-- =====================================================

SELECT '📊 TABLE COLUMNS DETAIL' as section;

SELECT 
  table_name,
  column_name,
  data_type,
  is_nullable,
  column_default,
  CASE WHEN is_nullable = 'NO' THEN '🔒' ELSE '🔓' END as nullable_icon
FROM information_schema.columns
WHERE table_schema = 'public' 
AND table_name IN (
  'users', 'organizations', 'organization_members', 'projects', 
  'brands', 'assets', 'campaigns', 'analyses', 'presentations', 'audit_logs'
)
ORDER BY 
  CASE table_name
    WHEN 'users' THEN 1
    WHEN 'organizations' THEN 2
    WHEN 'organization_members' THEN 3
    WHEN 'projects' THEN 4
    WHEN 'brands' THEN 5
    WHEN 'assets' THEN 6
    WHEN 'campaigns' THEN 7
    WHEN 'analyses' THEN 8
    WHEN 'presentations' THEN 9
    WHEN 'audit_logs' THEN 10
  END,
  ordinal_position;

-- =====================================================
-- 5. CHECK INDEXES
-- =====================================================

SELECT '🔍 INDEXES' as section;

SELECT 
  schemaname,
  tablename,
  indexname,
  indexdef,
  '✅' as status
FROM pg_indexes 
WHERE schemaname = 'public'
AND tablename IN (
  'users', 'organizations', 'organization_members', 'projects', 
  'brands', 'assets', 'campaigns', 'analyses', 'presentations', 'audit_logs'
)
ORDER BY tablename, indexname;

-- =====================================================
-- 6. CHECK FOREIGN KEY CONSTRAINTS
-- =====================================================

SELECT '🔗 FOREIGN KEY CONSTRAINTS' as section;

SELECT 
  tc.table_name,
  tc.constraint_name,
  tc.constraint_type,
  kcu.column_name,
  ccu.table_name AS foreign_table_name,
  ccu.column_name AS foreign_column_name,
  '✅' as status
FROM information_schema.table_constraints AS tc 
JOIN information_schema.key_column_usage AS kcu
  ON tc.constraint_name = kcu.constraint_name
  AND tc.table_schema = kcu.table_schema
JOIN information_schema.constraint_column_usage AS ccu
  ON ccu.constraint_name = tc.constraint_name
  AND ccu.table_schema = tc.table_schema
WHERE tc.constraint_type = 'FOREIGN KEY' 
AND tc.table_schema = 'public'
ORDER BY tc.table_name, tc.constraint_name;

-- =====================================================
-- 7. CHECK TRIGGERS
-- =====================================================

SELECT '⚡ TRIGGERS' as section;

SELECT 
  event_object_table as table_name,
  trigger_name,
  event_manipulation as event,
  action_timing,
  '✅' as status
FROM information_schema.triggers
WHERE trigger_schema = 'public'
ORDER BY event_object_table, trigger_name;

-- =====================================================
-- 8. CHECK RLS POLICIES
-- =====================================================

SELECT '🔐 ROW LEVEL SECURITY POLICIES' as section;

SELECT 
  schemaname,
  tablename,
  policyname,
  permissive,
  roles,
  cmd,
  '✅' as status
FROM pg_policies 
WHERE schemaname = 'public'
ORDER BY tablename, policyname;

-- =====================================================
-- 9. CHECK FUNCTIONS
-- =====================================================

SELECT '⚙️ CUSTOM FUNCTIONS' as section;

SELECT 
  routine_name as function_name,
  routine_type,
  data_type as return_type,
  '✅' as status
FROM information_schema.routines
WHERE routine_schema = 'public'
AND routine_name IN (
  'update_updated_at_column',
  'get_user_organizations',
  'is_organization_member',
  'is_organization_admin',
  'create_organization_with_owner',
  'create_project_with_brands',
  'get_user_projects_with_stats',
  'search_brands',
  'track_user_activity',
  'cleanup_temp_uploads',
  'get_organization_stats'
)
ORDER BY routine_name;

-- =====================================================
-- 10. CHECK STORAGE BUCKETS (Supabase specific)
-- =====================================================

SELECT '🗄️ STORAGE BUCKETS' as section;

SELECT 
  id as bucket_name,
  name,
  public,
  CASE WHEN public THEN '🌐 Public' ELSE '🔒 Private' END as access_type,
  created_at,
  '✅' as status
FROM storage.buckets
WHERE id IN (
  'brand-logos', 'campaign-assets', 'brand-guidelines', 
  'presentations', 'temp-uploads'
)
ORDER BY id;

-- =====================================================
-- 11. SCHEMA SUMMARY
-- =====================================================

SELECT '📈 SCHEMA SUMMARY' as section;

WITH schema_stats AS (
  SELECT 
    (SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public' AND table_type = 'BASE TABLE') as total_tables,
    (SELECT COUNT(*) FROM information_schema.columns WHERE table_schema = 'public') as total_columns,
    (SELECT COUNT(*) FROM pg_indexes WHERE schemaname = 'public') as total_indexes,
    (SELECT COUNT(*) FROM information_schema.table_constraints WHERE table_schema = 'public' AND constraint_type = 'FOREIGN KEY') as total_foreign_keys,
    (SELECT COUNT(*) FROM information_schema.triggers WHERE trigger_schema = 'public') as total_triggers,
    (SELECT COUNT(*) FROM pg_policies WHERE schemaname = 'public') as total_rls_policies,
    (SELECT COUNT(*) FROM information_schema.routines WHERE routine_schema = 'public') as total_functions,
    (SELECT COUNT(*) FROM storage.buckets) as total_storage_buckets
)
SELECT 
  '📋 Tables' as component, total_tables as count, '✅' as status FROM schema_stats
UNION ALL
SELECT '📊 Columns', total_columns, '✅' FROM schema_stats
UNION ALL
SELECT '🔍 Indexes', total_indexes, '✅' FROM schema_stats
UNION ALL
SELECT '🔗 Foreign Keys', total_foreign_keys, '✅' FROM schema_stats
UNION ALL
SELECT '⚡ Triggers', total_triggers, '✅' FROM schema_stats
UNION ALL
SELECT '🔐 RLS Policies', total_rls_policies, '✅' FROM schema_stats
UNION ALL
SELECT '⚙️ Functions', total_functions, '✅' FROM schema_stats
UNION ALL
SELECT '🗄️ Storage Buckets', total_storage_buckets, '✅' FROM schema_stats;

-- =====================================================
-- 12. VALIDATION TESTS
-- =====================================================

SELECT '🧪 VALIDATION TESTS' as section;

-- Test 1: Check if all expected tables exist
WITH expected_tables AS (
  SELECT unnest(ARRAY[
    'users', 'organizations', 'organization_members', 'projects', 
    'brands', 'assets', 'campaigns', 'analyses', 'presentations', 'audit_logs'
  ]) as table_name
),
existing_tables AS (
  SELECT table_name 
  FROM information_schema.tables 
  WHERE table_schema = 'public' AND table_type = 'BASE TABLE'
)
SELECT 
  'All Core Tables Present' as test_name,
  CASE 
    WHEN (SELECT COUNT(*) FROM expected_tables) = (SELECT COUNT(*) FROM expected_tables e JOIN existing_tables ex ON e.table_name = ex.table_name)
    THEN '✅ PASS'
    ELSE '❌ FAIL'
  END as result;

-- Test 2: Check if RLS is enabled on all tables
SELECT 
  'RLS Enabled on All Tables' as test_name,
  CASE 
    WHEN (
      SELECT COUNT(*) 
      FROM pg_class c 
      JOIN pg_namespace n ON n.oid = c.relnamespace 
      WHERE n.nspname = 'public' 
      AND c.relkind = 'r' 
      AND c.relname IN ('users', 'organizations', 'organization_members', 'projects', 'brands', 'assets', 'campaigns', 'analyses', 'presentations', 'audit_logs')
      AND c.relrowsecurity = true
    ) = 10
    THEN '✅ PASS'
    ELSE '❌ FAIL'
  END as result;

-- Test 3: Check if all custom types exist
WITH expected_types AS (
  SELECT unnest(ARRAY[
    'user_role', 'member_role', 'subscription_tier', 'project_status', 
    'processing_status', 'asset_type', 'analysis_type', 'presentation_status'
  ]) as type_name
)
SELECT 
  'All Custom Types Present' as test_name,
  CASE 
    WHEN (SELECT COUNT(*) FROM expected_types) = (SELECT COUNT(*) FROM expected_types e JOIN pg_type t ON e.type_name = t.typname)
    THEN '✅ PASS'
    ELSE '❌ FAIL'
  END as result;

SELECT '🎉 SCHEMA VERIFICATION COMPLETE!' as status;
