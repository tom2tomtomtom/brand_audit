import { createClient } from '@supabase/supabase-js';
import { createBrowserClient } from '@supabase/ssr';
import type { Database } from '@/types/database';

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL!;
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!;

if (!supabaseUrl || !supabaseAnonKey) {
  throw new Error('Missing Supabase environment variables');
}

// Client-side Supabase client
export const supabase = createClient<Database>(supabaseUrl, supabaseAnonKey, {
  auth: {
    persistSession: true,
    autoRefreshToken: true,
  },
});

// Client component client (for use in client components)
export const createClientSupabase = () =>
  createBrowserClient<Database>(supabaseUrl, supabaseAnonKey);

// Storage helpers
export const getPublicUrl = (bucket: string, path: string) => {
  const { data } = supabase.storage.from(bucket).getPublicUrl(path);
  return data.publicUrl;
};

export const uploadFile = async (
  bucket: string,
  path: string,
  file: File | Buffer,
  options?: {
    cacheControl?: string;
    contentType?: string;
    upsert?: boolean;
  }
) => {
  const { data, error } = await supabase.storage
    .from(bucket)
    .upload(path, file, {
      cacheControl: options?.cacheControl || '3600',
      contentType: options?.contentType,
      upsert: options?.upsert || false,
    });

  if (error) {
    throw new Error(`Upload failed: ${error.message}`);
  }

  return data;
};

export const deleteFile = async (bucket: string, paths: string[]) => {
  const { error } = await supabase.storage.from(bucket).remove(paths);
  
  if (error) {
    throw new Error(`Delete failed: ${error.message}`);
  }
};

// Database helpers
export const withErrorHandling = async <T>(
  operation: () => Promise<{ data: T; error: any }>
): Promise<T> => {
  const { data, error } = await operation();
  
  if (error) {
    console.error('Database operation failed:', error);
    throw new Error(error.message || 'Database operation failed');
  }
  
  return data;
};

// Real-time subscriptions
export const subscribeToTable = <T>(
  table: string,
  callback: (payload: any) => void,
  filter?: string
) => {
  const channel = supabase
    .channel(`${table}_changes`)
    .on(
      'postgres_changes',
      {
        event: '*',
        schema: 'public',
        table,
        filter,
      },
      callback
    )
    .subscribe();

  return () => {
    supabase.removeChannel(channel);
  };
};

// Auth helpers
export const getCurrentUser = async () => {
  const { data: { user }, error } = await supabase.auth.getUser();
  
  if (error) {
    throw new Error(`Auth error: ${error.message}`);
  }
  
  return user;
};

export const signOut = async () => {
  const { error } = await supabase.auth.signOut();
  
  if (error) {
    throw new Error(`Sign out error: ${error.message}`);
  }
};

// Type-safe query builders
export const createTypedQuery = () => ({
  users: () => supabase.from('users'),
  organizations: () => supabase.from('organizations'),
  organization_members: () => supabase.from('organization_members'),
  projects: () => supabase.from('projects'),
  brands: () => supabase.from('brands'),
  assets: () => supabase.from('assets'),
  campaigns: () => supabase.from('campaigns'),
  analyses: () => supabase.from('analyses'),
  presentations: () => supabase.from('presentations'),
});

export const db = createTypedQuery();
