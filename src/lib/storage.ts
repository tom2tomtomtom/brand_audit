import { createServerSupabase } from '@/lib/supabase-server';

export interface UploadOptions {
  cacheControl?: string;
  contentType?: string;
  upsert?: boolean;
}

export const getPublicUrl = (bucket: string, path: string) => {
  const supabase = createServerSupabase();
  const { data } = supabase.storage.from(bucket).getPublicUrl(path);
  return data.publicUrl;
};

export const uploadFile = async (
  bucket: string,
  path: string,
  file: File | Buffer | Uint8Array,
  options?: UploadOptions
) => {
  const supabase = createServerSupabase();
  
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
  const supabase = createServerSupabase();
  
  const { error } = await supabase.storage.from(bucket).remove(paths);
  
  if (error) {
    throw new Error(`Delete failed: ${error.message}`);
  }
};

export const downloadFile = async (bucket: string, path: string) => {
  const supabase = createServerSupabase();
  
  const { data, error } = await supabase.storage.from(bucket).download(path);
  
  if (error) {
    throw new Error(`Download failed: ${error.message}`);
  }
  
  return data;
};

export const listFiles = async (bucket: string, folder?: string) => {
  const supabase = createServerSupabase();
  
  const { data, error } = await supabase.storage
    .from(bucket)
    .list(folder, {
      limit: 100,
      offset: 0,
    });

  if (error) {
    throw new Error(`List failed: ${error.message}`);
  }

  return data;
};

export const getSignedUrl = async (
  bucket: string,
  path: string,
  expiresIn: number = 3600
) => {
  const supabase = createServerSupabase();
  
  const { data, error } = await supabase.storage
    .from(bucket)
    .createSignedUrl(path, expiresIn);

  if (error) {
    throw new Error(`Signed URL creation failed: ${error.message}`);
  }

  return data.signedUrl;
};
