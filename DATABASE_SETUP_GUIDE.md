# 🗄️ Database Setup Guide

This guide will help you set up the complete database schema for the Brand Audit Tool using Supabase.

## 📋 Prerequisites

- Supabase account ([sign up here](https://supabase.com))
- Basic understanding of SQL
- Access to Supabase SQL Editor

## 🚀 Quick Setup

### Step 1: Create Supabase Project

1. Go to [Supabase Dashboard](https://supabase.com/dashboard)
2. Click "New Project"
3. Choose your organization
4. Enter project details:
   - **Name**: `brand-audit-tool`
   - **Database Password**: Generate a strong password
   - **Region**: Choose closest to your users
5. Click "Create new project"
6. Wait for project to be ready (2-3 minutes)

### Step 2: Run Database Schema

1. In your Supabase project dashboard, go to **SQL Editor**
2. Click "New Query"
3. Copy the entire contents of `database_setup.sql`
4. Paste into the SQL editor
5. Click "Run" to execute the schema

### Step 3: Get Environment Variables

1. Go to **Settings** → **API**
2. Copy the following values:
   - **Project URL** → `NEXT_PUBLIC_SUPABASE_URL`
   - **Project API Keys** → **anon/public** → `NEXT_PUBLIC_SUPABASE_ANON_KEY`
   - **Project API Keys** → **service_role** → `SUPABASE_SERVICE_ROLE_KEY`

### Step 4: Configure Application

1. Create `.env.local` in your project root:
   ```env
   NEXT_PUBLIC_SUPABASE_URL=your_project_url_here
   NEXT_PUBLIC_SUPABASE_ANON_KEY=your_anon_key_here
   SUPABASE_SERVICE_ROLE_KEY=your_service_role_key_here
   ```

2. Restart your development server:
   ```bash
   npm run dev
   ```

## 📊 Database Schema Overview

### Core Tables

| Table | Purpose | Key Features |
|-------|---------|--------------|
| `users` | User profiles | Extends Supabase auth.users |
| `organizations` | Multi-tenant structure | Subscription tiers, slugs |
| `organization_members` | User-org relationships | Role-based access |
| `projects` | Brand analysis projects | Status tracking |
| `brands` | Companies being analyzed | Scraping/analysis status |
| `assets` | Collected brand assets | File metadata, categorization |
| `campaigns` | Marketing campaigns | Platform tracking |
| `analyses` | AI-generated insights | Confidence scoring |
| `presentations` | Generated slide decks | Template system |
| `audit_logs` | Activity tracking | Full audit trail |

### Key Features

- ✅ **Row Level Security (RLS)** - Multi-tenant data isolation
- ✅ **Full-text Search** - Search brands and assets
- ✅ **Audit Logging** - Track all user activities
- ✅ **Business Logic Functions** - Complex operations in database
- ✅ **Storage Integration** - File upload buckets
- ✅ **Performance Indexes** - Optimized queries

## 🔐 Security Features

### Row Level Security Policies

- Users can only access data from their organizations
- Role-based permissions (owner, admin, member)
- Secure multi-tenancy
- Audit trail for all actions

### Storage Security

- Public bucket for brand logos
- Private buckets for sensitive assets
- Automatic cleanup of temporary uploads
- Organization-based access control

## 🛠️ Useful Functions

### Business Logic Functions

```sql
-- Create organization with owner
SELECT create_organization_with_owner('Company Name', 'company-slug', user_id);

-- Create project with brands
SELECT create_project_with_brands(project_data, brands_array, user_id, org_id);

-- Get user's projects with statistics
SELECT * FROM get_user_projects_with_stats(user_id);

-- Search brands across organizations
SELECT * FROM search_brands(user_id, 'search term');

-- Track user activity
SELECT track_user_activity(user_id, org_id, 'action', 'resource_type');
```

### Utility Functions

```sql
-- Get organization statistics
SELECT * FROM get_organization_stats(org_id);

-- Clean up old temporary uploads
SELECT cleanup_temp_uploads();
```

## 🧪 Testing the Setup

### Verify Tables Created

```sql
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public' 
AND table_name IN (
  'users', 'organizations', 'projects', 'brands', 
  'assets', 'campaigns', 'analyses', 'presentations'
);
```

### Check RLS Policies

```sql
SELECT schemaname, tablename, policyname, permissive, roles, cmd, qual 
FROM pg_policies 
WHERE schemaname = 'public';
```

### Test Functions

```sql
-- Test helper functions
SELECT is_organization_member('user-id', 'org-id');
SELECT * FROM get_user_organizations('user-id');
```

## 🔧 Troubleshooting

### Common Issues

1. **"relation does not exist" errors**
   - Make sure you're running the SQL in the correct database
   - Check that all tables were created successfully

2. **RLS policy errors**
   - Ensure you're authenticated when testing
   - Check that user exists in the users table

3. **Function errors**
   - Verify all custom types were created
   - Check function syntax for any typos

### Getting Help

- Check Supabase documentation: https://supabase.com/docs
- Join Supabase Discord: https://discord.supabase.com
- Review the application logs for specific errors

## 🎯 Next Steps

After setting up the database:

1. **Test Authentication** - Try registering a new user
2. **Create Sample Data** - Add a test organization and project
3. **Verify API Routes** - Test the `/api/projects` endpoint
4. **Set up Storage** - Configure file upload functionality
5. **Add LLM Integration** - Connect OpenAI/Claude APIs

## 📚 Additional Resources

- [Supabase Documentation](https://supabase.com/docs)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Row Level Security Guide](https://supabase.com/docs/guides/auth/row-level-security)
- [Supabase Storage Guide](https://supabase.com/docs/guides/storage)

---

🎉 **Congratulations!** Your Brand Audit Tool database is now ready for development!
