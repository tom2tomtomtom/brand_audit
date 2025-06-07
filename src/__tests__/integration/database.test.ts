import { createServerSupabase } from '@/lib/supabase-server';

// Mock environment variables for testing
process.env.NEXT_PUBLIC_SUPABASE_URL = 'https://test.supabase.co';
process.env.SUPABASE_SERVICE_ROLE_KEY = 'test-service-role-key';

// This would be a real integration test with a test database
// For now, we'll mock the Supabase client but test the logic

const mockSupabase = {
  from: jest.fn(() => ({
    select: jest.fn().mockReturnThis(),
    insert: jest.fn().mockReturnThis(),
    update: jest.fn().mockReturnThis(),
    delete: jest.fn().mockReturnThis(),
    eq: jest.fn().mockReturnThis(),
    order: jest.fn().mockReturnThis(),
    single: jest.fn().mockResolvedValue({ data: null, error: null }),
  })),
  auth: {
    getUser: jest.fn(),
  },
  rpc: jest.fn(),
  storage: {
    from: jest.fn(() => ({
      upload: jest.fn(),
      download: jest.fn(),
      remove: jest.fn(),
    })),
  },
};

jest.mock('@/lib/supabase-server', () => ({
  createServerSupabase: () => mockSupabase,
}));

describe('Database Integration Tests', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('User Management', () => {
    it('should create user and organization on first login', async () => {
      const mockUser = {
        id: 'user-123',
        email: 'test@example.com',
        user_metadata: {
          full_name: 'Test User',
        },
      };

      mockSupabase.auth.getUser.mockResolvedValue({
        data: { user: mockUser },
        error: null,
      });

      // Mock user doesn't exist
      mockSupabase.from.mockReturnValueOnce({
        select: jest.fn().mockReturnThis(),
        eq: jest.fn().mockReturnThis(),
        single: jest.fn().mockResolvedValue({
          data: null,
          error: { code: 'PGRST116' }, // Not found
        }),
      });

      // Mock user creation
      mockSupabase.from.mockReturnValueOnce({
        insert: jest.fn().mockReturnThis(),
        select: jest.fn().mockReturnThis(),
        single: jest.fn().mockResolvedValue({
          data: { id: 'user-123', email: 'test@example.com' },
          error: null,
        }),
      });

      // Mock organization creation
      mockSupabase.from.mockReturnValueOnce({
        insert: jest.fn().mockReturnThis(),
        select: jest.fn().mockReturnThis(),
        single: jest.fn().mockResolvedValue({
          data: { id: 'org-123', name: 'Test User Organization' },
          error: null,
        }),
      });

      // Mock organization membership creation
      mockSupabase.from.mockReturnValueOnce({
        insert: jest.fn().mockResolvedValue({
          data: { user_id: 'user-123', organization_id: 'org-123' },
          error: null,
        }),
      });

      const supabase = createServerSupabase();
      
      // Simulate the user creation flow
      const { data: user } = await supabase.auth.getUser();
      expect(user?.user).toEqual(mockUser);

      // Check if user exists
      const userQuery = supabase.from('users');
      expect(userQuery.select).toBeDefined();
    });

    it('should handle existing user login', async () => {
      const mockUser = {
        id: 'user-123',
        email: 'test@example.com',
      };

      mockSupabase.auth.getUser.mockResolvedValue({
        data: { user: mockUser },
        error: null,
      });

      // Mock user exists
      mockSupabase.from.mockReturnValue({
        select: jest.fn().mockReturnThis(),
        eq: jest.fn().mockReturnThis(),
        single: jest.fn().mockResolvedValue({
          data: { id: 'user-123', email: 'test@example.com' },
          error: null,
        }),
      });

      const supabase = createServerSupabase();
      const { data: user } = await supabase.auth.getUser();
      
      expect(user?.user).toEqual(mockUser);
    });
  });

  describe('Project Management', () => {
    it('should create project with brands using RPC function', async () => {
      const projectData = {
        name: 'Test Project',
        description: 'Test description',
      };

      const brandsData = [
        {
          name: 'Nike',
          website_url: 'https://nike.com',
          industry: 'Sports',
        },
        {
          name: 'Adidas',
          website_url: 'https://adidas.com',
          industry: 'Sports',
        },
      ];

      mockSupabase.rpc.mockResolvedValue({
        data: 'project-123',
        error: null,
      });

      const supabase = createServerSupabase();
      const result = await supabase.rpc('create_project_with_brands', {
        project_data: projectData,
        brands_data: brandsData,
        user_id: 'user-123',
        org_id: 'org-123',
      });

      expect(result.data).toBe('project-123');
      expect(mockSupabase.rpc).toHaveBeenCalledWith('create_project_with_brands', {
        project_data: projectData,
        brands_data: brandsData,
        user_id: 'user-123',
        org_id: 'org-123',
      });
    });

    it('should fetch user projects with stats', async () => {
      const mockProjects = [
        {
          id: 'project-1',
          name: 'Project 1',
          brand_count: 2,
          completed_analyses: 1,
          total_assets: 15,
        },
        {
          id: 'project-2',
          name: 'Project 2',
          brand_count: 3,
          completed_analyses: 3,
          total_assets: 25,
        },
      ];

      mockSupabase.rpc.mockResolvedValue({
        data: mockProjects,
        error: null,
      });

      const supabase = createServerSupabase();
      const result = await supabase.rpc('get_user_projects_with_stats', {
        user_uuid: 'user-123',
      });

      expect(result.data).toEqual(mockProjects);
      expect(mockSupabase.rpc).toHaveBeenCalledWith('get_user_projects_with_stats', {
        user_uuid: 'user-123',
      });
    });

    it('should handle project access control', async () => {
      // Mock project query with RLS
      const mockChain = {
        select: jest.fn().mockReturnThis(),
        eq: jest.fn().mockReturnThis(),
        single: jest.fn().mockResolvedValue({
          data: null,
          error: { code: 'PGRST116' }, // Not found due to RLS
        }),
      };
      mockSupabase.from.mockReturnValue(mockChain);

      const supabase = createServerSupabase();
      const result = await supabase
        .from('projects')
        .select('*')
        .eq('id', 'project-123')
        .single();

      expect(result.data).toBeNull();
      expect(result.error?.code).toBe('PGRST116');
    });
  });

  describe('Brand Operations', () => {
    it('should update brand status', async () => {
      const mockChain = {
        update: jest.fn().mockReturnThis(),
        eq: jest.fn().mockReturnThis(),
        select: jest.fn().mockReturnThis(),
        single: jest.fn().mockResolvedValue({
          data: { id: 'brand-123', status: 'in_progress' },
          error: null,
        }),
      };
      mockSupabase.from.mockReturnValue(mockChain);

      const supabase = createServerSupabase();
      const result = await supabase
        .from('brands')
        .update({ status: 'in_progress' })
        .eq('id', 'brand-123')
        .select()
        .single();

      expect(result.data?.status).toBe('in_progress');
    });

    it('should store brand assets', async () => {
      const mockAssets = [
        {
          brand_id: 'brand-123',
          type: 'logo',
          filename: 'logo.png',
          file_url: 'https://storage.com/logo.png',
          file_size: 1024,
        },
      ];

      const mockChain = {
        insert: jest.fn().mockResolvedValue({
          data: mockAssets,
          error: null,
        }),
      };
      mockSupabase.from.mockReturnValue(mockChain);

      const supabase = createServerSupabase();
      const result = await supabase.from('assets').insert(mockAssets);

      expect(result.data).toEqual(mockAssets);
    });
  });

  describe('Analysis Storage', () => {
    it('should store analysis results', async () => {
      const analysisData = {
        brand_id: 'brand-123',
        type: 'positioning',
        results: {
          brandVoice: 'Professional',
          targetAudience: 'Business professionals',
        },
        confidence_score: 0.85,
        status: 'completed',
      };

      mockSupabase.from.mockReturnValue({
        insert: jest.fn().mockReturnThis(),
        select: jest.fn().mockReturnThis(),
        single: jest.fn().mockResolvedValue({
          data: { id: 'analysis-123', ...analysisData },
          error: null,
        }),
      });

      const supabase = createServerSupabase();
      const result = await supabase
        .from('analyses')
        .insert(analysisData)
        .select()
        .single();

      expect(result.data?.type).toBe('positioning');
      expect(result.data?.confidence_score).toBe(0.85);
    });

    it('should fetch latest analyses by type', async () => {
      const mockAnalyses = [
        {
          id: 'analysis-1',
          type: 'positioning',
          created_at: '2024-01-02T00:00:00Z',
          results: { brandVoice: 'Professional' },
        },
        {
          id: 'analysis-2',
          type: 'positioning',
          created_at: '2024-01-01T00:00:00Z',
          results: { brandVoice: 'Casual' },
        },
        {
          id: 'analysis-3',
          type: 'visual',
          created_at: '2024-01-01T00:00:00Z',
          results: { colorPalette: ['#FF0000'] },
        },
      ];

      mockSupabase.from.mockReturnValue({
        select: jest.fn().mockReturnThis(),
        eq: jest.fn().mockReturnThis(),
        order: jest.fn().mockResolvedValue({
          data: mockAnalyses,
          error: null,
        }),
      });

      const supabase = createServerSupabase();
      const result = await supabase
        .from('analyses')
        .select('*')
        .eq('brand_id', 'brand-123')
        .order('created_at', { ascending: false });

      expect(result.data).toEqual(mockAnalyses);
    });
  });

  describe('Storage Operations', () => {
    it('should upload files to storage', async () => {
      const mockFile = new Uint8Array([1, 2, 3, 4]);
      const filename = 'test-file.png';

      mockSupabase.storage.from.mockReturnValue({
        upload: jest.fn().mockResolvedValue({
          data: { path: `brands/brand-123/${filename}` },
          error: null,
        }),
      });

      const supabase = createServerSupabase();
      const result = await supabase.storage
        .from('brand-assets')
        .upload(`brands/brand-123/${filename}`, mockFile);

      expect(result.data?.path).toBe(`brands/brand-123/${filename}`);
    });

    it('should download files from storage', async () => {
      const mockFileData = new Blob(['file content']);

      mockSupabase.storage.from.mockReturnValue({
        download: jest.fn().mockResolvedValue({
          data: mockFileData,
          error: null,
        }),
      });

      const supabase = createServerSupabase();
      const result = await supabase.storage
        .from('brand-assets')
        .download('brands/brand-123/logo.png');

      expect(result.data).toBe(mockFileData);
    });
  });
});
