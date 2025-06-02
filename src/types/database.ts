export interface Database {
  public: {
    Tables: {
      users: {
        Row: {
          id: string;
          email: string;
          full_name: string | null;
          avatar_url: string | null;
          role: 'admin' | 'editor' | 'viewer';
          created_at: string;
          updated_at: string;
        };
        Insert: {
          id: string;
          email: string;
          full_name?: string | null;
          avatar_url?: string | null;
          role?: 'admin' | 'editor' | 'viewer';
          created_at?: string;
          updated_at?: string;
        };
        Update: {
          id?: string;
          email?: string;
          full_name?: string | null;
          avatar_url?: string | null;
          role?: 'admin' | 'editor' | 'viewer';
          created_at?: string;
          updated_at?: string;
        };
      };
      organizations: {
        Row: {
          id: string;
          name: string;
          slug: string;
          logo_url: string | null;
          subscription_tier: 'free' | 'pro' | 'enterprise';
          created_at: string;
          updated_at: string;
        };
        Insert: {
          id?: string;
          name: string;
          slug: string;
          logo_url?: string | null;
          subscription_tier?: 'free' | 'pro' | 'enterprise';
          created_at?: string;
          updated_at?: string;
        };
        Update: {
          id?: string;
          name?: string;
          slug?: string;
          logo_url?: string | null;
          subscription_tier?: 'free' | 'pro' | 'enterprise';
          created_at?: string;
          updated_at?: string;
        };
      };
      organization_members: {
        Row: {
          id: string;
          organization_id: string;
          user_id: string;
          role: 'owner' | 'admin' | 'member';
          created_at: string;
        };
        Insert: {
          id?: string;
          organization_id: string;
          user_id: string;
          role?: 'owner' | 'admin' | 'member';
          created_at?: string;
        };
        Update: {
          id?: string;
          organization_id?: string;
          user_id?: string;
          role?: 'owner' | 'admin' | 'member';
          created_at?: string;
        };
      };
      projects: {
        Row: {
          id: string;
          organization_id: string;
          name: string;
          description: string | null;
          status: 'draft' | 'active' | 'completed' | 'archived';
          created_by: string;
          created_at: string;
          updated_at: string;
        };
        Insert: {
          id?: string;
          organization_id: string;
          name: string;
          description?: string | null;
          status?: 'draft' | 'active' | 'completed' | 'archived';
          created_by: string;
          created_at?: string;
          updated_at?: string;
        };
        Update: {
          id?: string;
          organization_id?: string;
          name?: string;
          description?: string | null;
          status?: 'draft' | 'active' | 'completed' | 'archived';
          created_by?: string;
          created_at?: string;
          updated_at?: string;
        };
      };
      brands: {
        Row: {
          id: string;
          project_id: string;
          name: string;
          website_url: string;
          logo_url: string | null;
          industry: string | null;
          description: string | null;
          scraping_status: 'pending' | 'in_progress' | 'completed' | 'failed';
          analysis_status: 'pending' | 'in_progress' | 'completed' | 'failed';
          created_at: string;
          updated_at: string;
        };
        Insert: {
          id?: string;
          project_id: string;
          name: string;
          website_url: string;
          logo_url?: string | null;
          industry?: string | null;
          description?: string | null;
          scraping_status?: 'pending' | 'in_progress' | 'completed' | 'failed';
          analysis_status?: 'pending' | 'in_progress' | 'completed' | 'failed';
          created_at?: string;
          updated_at?: string;
        };
        Update: {
          id?: string;
          project_id?: string;
          name?: string;
          website_url?: string;
          logo_url?: string | null;
          industry?: string | null;
          description?: string | null;
          scraping_status?: 'pending' | 'in_progress' | 'completed' | 'failed';
          analysis_status?: 'pending' | 'in_progress' | 'completed' | 'failed';
          created_at?: string;
          updated_at?: string;
        };
      };
      assets: {
        Row: {
          id: string;
          brand_id: string;
          type: 'logo' | 'image' | 'document' | 'video';
          url: string;
          filename: string;
          file_size: number;
          mime_type: string;
          width: number | null;
          height: number | null;
          alt_text: string | null;
          metadata: Record<string, any> | null;
          created_at: string;
        };
        Insert: {
          id?: string;
          brand_id: string;
          type: 'logo' | 'image' | 'document' | 'video';
          url: string;
          filename: string;
          file_size: number;
          mime_type: string;
          width?: number | null;
          height?: number | null;
          alt_text?: string | null;
          metadata?: Record<string, any> | null;
          created_at?: string;
        };
        Update: {
          id?: string;
          brand_id?: string;
          type?: 'logo' | 'image' | 'document' | 'video';
          url?: string;
          filename?: string;
          file_size?: number;
          mime_type?: string;
          width?: number | null;
          height?: number | null;
          alt_text?: string | null;
          metadata?: Record<string, any> | null;
          created_at?: string;
        };
      };
      campaigns: {
        Row: {
          id: string;
          brand_id: string;
          name: string;
          description: string | null;
          start_date: string | null;
          end_date: string | null;
          platform: string | null;
          campaign_type: string | null;
          created_at: string;
        };
        Insert: {
          id?: string;
          brand_id: string;
          name: string;
          description?: string | null;
          start_date?: string | null;
          end_date?: string | null;
          platform?: string | null;
          campaign_type?: string | null;
          created_at?: string;
        };
        Update: {
          id?: string;
          brand_id?: string;
          name?: string;
          description?: string | null;
          start_date?: string | null;
          end_date?: string | null;
          platform?: string | null;
          campaign_type?: string | null;
          created_at?: string;
        };
      };
      analyses: {
        Row: {
          id: string;
          brand_id: string;
          type: 'positioning' | 'visual' | 'competitive' | 'sentiment';
          status: 'pending' | 'in_progress' | 'completed' | 'failed';
          results: Record<string, any> | null;
          confidence_score: number | null;
          created_at: string;
          updated_at: string;
        };
        Insert: {
          id?: string;
          brand_id: string;
          type: 'positioning' | 'visual' | 'competitive' | 'sentiment';
          status?: 'pending' | 'in_progress' | 'completed' | 'failed';
          results?: Record<string, any> | null;
          confidence_score?: number | null;
          created_at?: string;
          updated_at?: string;
        };
        Update: {
          id?: string;
          brand_id?: string;
          type?: 'positioning' | 'visual' | 'competitive' | 'sentiment';
          status?: 'pending' | 'in_progress' | 'completed' | 'failed';
          results?: Record<string, any> | null;
          confidence_score?: number | null;
          created_at?: string;
          updated_at?: string;
        };
      };
      presentations: {
        Row: {
          id: string;
          project_id: string;
          name: string;
          template: string;
          status: 'draft' | 'generating' | 'completed' | 'failed';
          slides_data: Record<string, any> | null;
          export_url: string | null;
          created_by: string;
          created_at: string;
          updated_at: string;
        };
        Insert: {
          id?: string;
          project_id: string;
          name: string;
          template: string;
          status?: 'draft' | 'generating' | 'completed' | 'failed';
          slides_data?: Record<string, any> | null;
          export_url?: string | null;
          created_by: string;
          created_at?: string;
          updated_at?: string;
        };
        Update: {
          id?: string;
          project_id?: string;
          name?: string;
          template?: string;
          status?: 'draft' | 'generating' | 'completed' | 'failed';
          slides_data?: Record<string, any> | null;
          export_url?: string | null;
          created_by?: string;
          created_at?: string;
          updated_at?: string;
        };
      };
    };
  };
}
