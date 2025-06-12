-- Supabase Database Schema for Brand Audit Tool
-- Run this in your Supabase SQL editor

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Analysis Jobs Table
CREATE TABLE IF NOT EXISTS analysis_jobs (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    job_id TEXT UNIQUE NOT NULL,
    status TEXT NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'started', 'running', 'completed', 'failed')),
    progress DECIMAL(5,2) DEFAULT 0.0 CHECK (progress >= 0 AND progress <= 100),
    current_task TEXT,
    total_brands INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    completed_at TIMESTAMP WITH TIME ZONE,
    error_message TEXT,
    estimated_completion INTEGER, -- seconds
    result_file_path TEXT
);

-- Scraped Brands Table (for future enhancement)
CREATE TABLE IF NOT EXISTS scraped_brands (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    job_id TEXT REFERENCES analysis_jobs(job_id) ON DELETE CASCADE,
    brand_name TEXT NOT NULL,
    brand_url TEXT NOT NULL,
    scraped_data JSONB,
    scraped_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Brand Analyses Table (for future enhancement)
CREATE TABLE IF NOT EXISTS brand_analyses (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    job_id TEXT REFERENCES analysis_jobs(job_id) ON DELETE CASCADE,
    brand_name TEXT NOT NULL,
    analysis_data JSONB,
    analyzed_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_analysis_jobs_job_id ON analysis_jobs(job_id);
CREATE INDEX IF NOT EXISTS idx_analysis_jobs_status ON analysis_jobs(status);
CREATE INDEX IF NOT EXISTS idx_analysis_jobs_created_at ON analysis_jobs(created_at);
CREATE INDEX IF NOT EXISTS idx_scraped_brands_job_id ON scraped_brands(job_id);
CREATE INDEX IF NOT EXISTS idx_brand_analyses_job_id ON brand_analyses(job_id);

-- Function to automatically update the updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Trigger to automatically update updated_at
CREATE TRIGGER update_analysis_jobs_updated_at 
    BEFORE UPDATE ON analysis_jobs 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

-- RLS (Row Level Security) policies - Enable if you want user-based access control
-- ALTER TABLE analysis_jobs ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE scraped_brands ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE brand_analyses ENABLE ROW LEVEL SECURITY;

-- For now, allow all operations (you can restrict this later)
-- CREATE POLICY "Allow all operations on analysis_jobs" ON analysis_jobs FOR ALL USING (true);
-- CREATE POLICY "Allow all operations on scraped_brands" ON scraped_brands FOR ALL USING (true);
-- CREATE POLICY "Allow all operations on brand_analyses" ON brand_analyses FOR ALL USING (true);

-- Clean up function for old jobs (optional)
CREATE OR REPLACE FUNCTION cleanup_old_jobs(days_old INTEGER DEFAULT 7)
RETURNS INTEGER AS $$
DECLARE
    deleted_count INTEGER;
BEGIN
    DELETE FROM analysis_jobs 
    WHERE created_at < NOW() - (days_old || ' days')::INTERVAL
    AND status IN ('completed', 'failed');
    
    GET DIAGNOSTICS deleted_count = ROW_COUNT;
    RETURN deleted_count;
END;
$$ LANGUAGE plpgsql;

-- Optional: Create a scheduled function to cleanup old jobs automatically
-- This would need to be set up in Supabase Edge Functions or via pg_cron extension