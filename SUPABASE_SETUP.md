# Supabase Setup Guide for Brand Audit Tool

This guide will help you set up Supabase to enable persistent job tracking and eliminate "Job not found" errors on Railway.

## 🎯 Benefits of Supabase Integration

✅ **Persistent job tracking** - Jobs survive Railway restarts  
✅ **No more "Job not found" errors**  
✅ **Job history** - See past analyses  
✅ **Resume capability** - Resume interrupted jobs  
✅ **Multiple concurrent users**  
✅ **Better scalability**

## 🚀 Quick Setup (5 minutes)

### Step 1: Create Supabase Project

1. Go to [supabase.com](https://supabase.com)
2. Click "Start your project" 
3. Sign up with GitHub (recommended)
4. Click "New Project"
5. Choose organization and enter:
   - **Name:** `brand-audit-tool`
   - **Database Password:** (generate secure password)
   - **Region:** Choose closest to your users
6. Click "Create new project"

### Step 2: Set Up Database Schema

1. Go to your Supabase project dashboard
2. Click "SQL Editor" in the sidebar
3. Click "New query"
4. Copy and paste the entire contents of `supabase_schema.sql`
5. Click "Run" to create all tables and indexes

### Step 3: Get Your Credentials

1. Go to "Settings" → "API" in your Supabase dashboard
2. Copy these values:
   - **Project URL:** `https://xxxxx.supabase.co`
   - **Anon public key:** `eyJhbGciOiJIUzI1NiIsIn...`

### Step 4: Add to Railway

1. Go to your Railway project dashboard
2. Click "Variables" tab
3. Add these variables:
   ```
   SUPABASE_URL=https://your-project.supabase.co
   SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsIn...
   ```
4. Railway will automatically restart your app

## ✅ Verification

After Railway restarts:

1. Visit your app: https://web-production-3788.up.railway.app/
2. Start a new analysis
3. **No more timeout/job not found errors!**
4. Jobs will persist through Railway restarts
5. You can check job status in Supabase dashboard

## 📊 Database Tables Created

- **`analysis_jobs`** - Job tracking and progress
- **`scraped_brands`** - Brand data storage (future use)
- **`brand_analyses`** - Analysis results (future use)

## 🎉 What This Fixes

**Before Supabase:**
- ❌ Jobs lost on Railway restart
- ❌ "Job not found" errors
- ❌ No job history
- ❌ Memory limitations

**After Supabase:**
- ✅ Jobs persist through restarts
- ✅ Reliable progress tracking
- ✅ Job history in database
- ✅ Unlimited concurrent users

## 💰 Cost

**Supabase Free Tier:**
- 500MB database storage
- 2GB bandwidth per month
- **Perfect for this application!**

## 🔧 Advanced Features (Future)

Once basic setup works, you can enable:
- Real-time progress updates (no polling needed)
- User accounts and job ownership
- Analysis history and templates
- Collaborative features

## 🆘 Troubleshooting

**App still uses in-memory storage:**
- Check Railway logs for Supabase connection errors
- Verify SUPABASE_URL and SUPABASE_ANON_KEY are correct
- App will fallback to in-memory if Supabase fails

**Connection errors:**
- Check Supabase project is not paused
- Verify API key permissions in Supabase dashboard

The app is designed to work with or without Supabase - it gracefully falls back to in-memory storage if needed.