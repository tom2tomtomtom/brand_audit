import { NextRequest } from 'next/server';
import { GET, POST } from '../projects/route';

// Mock Supabase
const mockSupabase = {
  auth: {
    getUser: jest.fn(),
  },
  from: jest.fn(() => ({
    select: jest.fn().mockReturnThis(),
    insert: jest.fn().mockReturnThis(),
    eq: jest.fn().mockReturnThis(),
    single: jest.fn(),
  })),
  rpc: jest.fn(),
};

jest.mock('@/lib/supabase-server', () => ({
  createServerSupabase: () => mockSupabase,
}));

describe('/api/projects', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('GET /api/projects', () => {
    it('should return projects for authenticated user', async () => {
      // Mock authenticated user
      mockSupabase.auth.getUser.mockResolvedValue({
        data: { user: { id: 'user-123' } },
        error: null,
      });

      // Mock projects data
      const mockProjects = [
        {
          id: 'project-1',
          name: 'Test Project',
          description: 'Test description',
          brand_count: 2,
          completed_analyses: 1,
        },
      ];

      mockSupabase.rpc.mockResolvedValue({
        data: mockProjects,
        error: null,
      });

      const request = new NextRequest('http://localhost:3000/api/projects');
      const response = await GET(request);
      const data = await response.json();

      expect(response.status).toBe(200);
      expect(data.projects).toEqual(mockProjects);
      expect(mockSupabase.rpc).toHaveBeenCalledWith('get_user_projects_with_stats', {
        user_uuid: 'user-123',
      });
    });

    it('should return 401 for unauthenticated user', async () => {
      mockSupabase.auth.getUser.mockResolvedValue({
        data: { user: null },
        error: new Error('Not authenticated'),
      });

      const request = new NextRequest('http://localhost:3000/api/projects');
      const response = await GET(request);
      const data = await response.json();

      expect(response.status).toBe(401);
      expect(data.error).toBe('Unauthorized');
    });

    it('should handle database errors', async () => {
      mockSupabase.auth.getUser.mockResolvedValue({
        data: { user: { id: 'user-123' } },
        error: null,
      });

      mockSupabase.rpc.mockResolvedValue({
        data: null,
        error: new Error('Database error'),
      });

      const request = new NextRequest('http://localhost:3000/api/projects');
      const response = await GET(request);
      const data = await response.json();

      expect(response.status).toBe(500);
      expect(data.error).toBe('Failed to fetch projects');
    });
  });

  describe('POST /api/projects', () => {
    const validProjectData = {
      name: 'New Project',
      description: 'Project description',
      brands: [
        {
          name: 'Brand 1',
          websiteUrl: 'https://brand1.com',
          industry: 'Technology',
          description: 'Tech brand',
        },
        {
          name: 'Brand 2',
          websiteUrl: 'https://brand2.com',
        },
      ],
    };

    beforeEach(() => {
      // Mock authenticated user
      mockSupabase.auth.getUser.mockResolvedValue({
        data: { user: { id: 'user-123' } },
        error: null,
      });

      // Mock organization membership
      mockSupabase.from.mockReturnValue({
        select: jest.fn().mockReturnThis(),
        eq: jest.fn().mockReturnThis(),
        single: jest.fn().mockResolvedValue({
          data: { organization_id: 'org-123' },
          error: null,
        }),
      });
    });

    it('should create project with brands successfully', async () => {
      // Mock project creation
      mockSupabase.rpc.mockResolvedValue({
        data: 'project-123',
        error: null,
      });

      // Mock project fetch
      const mockProject = {
        id: 'project-123',
        name: 'New Project',
        description: 'Project description',
        brands: [
          { id: 'brand-1', name: 'Brand 1' },
          { id: 'brand-2', name: 'Brand 2' },
        ],
      };

      mockSupabase.from.mockReturnValueOnce({
        select: jest.fn().mockReturnThis(),
        eq: jest.fn().mockReturnThis(),
        single: jest.fn().mockResolvedValue({
          data: mockProject,
          error: null,
        }),
      });

      const request = new NextRequest('http://localhost:3000/api/projects', {
        method: 'POST',
        body: JSON.stringify(validProjectData),
      });

      const response = await POST(request);
      const data = await response.json();

      expect(response.status).toBe(201);
      expect(data.project).toEqual(mockProject);
      expect(mockSupabase.rpc).toHaveBeenCalledWith('create_project_with_brands', {
        project_data: {
          name: 'New Project',
          description: 'Project description',
        },
        brands_data: [
          {
            name: 'Brand 1',
            website_url: 'https://brand1.com',
            industry: 'Technology',
            description: 'Tech brand',
          },
          {
            name: 'Brand 2',
            website_url: 'https://brand2.com',
            industry: undefined,
            description: undefined,
          },
        ],
        user_id: 'user-123',
        org_id: 'org-123',
      });
    });

    it('should validate request data', async () => {
      const invalidData = {
        name: '', // Empty name should fail validation
        brands: [], // Empty brands array should fail validation
      };

      const request = new NextRequest('http://localhost:3000/api/projects', {
        method: 'POST',
        body: JSON.stringify(invalidData),
      });

      const response = await POST(request);
      const data = await response.json();

      expect(response.status).toBe(400);
      expect(data.error).toBe('Validation error');
      expect(data.details).toBeDefined();
    });

    it('should require valid URLs for brands', async () => {
      const invalidData = {
        name: 'Test Project',
        brands: [
          {
            name: 'Brand 1',
            websiteUrl: 'invalid-url', // Invalid URL
          },
        ],
      };

      const request = new NextRequest('http://localhost:3000/api/projects', {
        method: 'POST',
        body: JSON.stringify(invalidData),
      });

      const response = await POST(request);
      const data = await response.json();

      expect(response.status).toBe(400);
      expect(data.error).toBe('Validation error');
    });

    it('should return 401 for unauthenticated user', async () => {
      mockSupabase.auth.getUser.mockResolvedValue({
        data: { user: null },
        error: new Error('Not authenticated'),
      });

      const request = new NextRequest('http://localhost:3000/api/projects', {
        method: 'POST',
        body: JSON.stringify(validProjectData),
      });

      const response = await POST(request);
      const data = await response.json();

      expect(response.status).toBe(401);
      expect(data.error).toBe('Unauthorized');
    });

    it('should return 400 when user has no organization', async () => {
      mockSupabase.from.mockReturnValue({
        select: jest.fn().mockReturnThis(),
        eq: jest.fn().mockReturnThis(),
        single: jest.fn().mockResolvedValue({
          data: null,
          error: new Error('No organization found'),
        }),
      });

      const request = new NextRequest('http://localhost:3000/api/projects', {
        method: 'POST',
        body: JSON.stringify(validProjectData),
      });

      const response = await POST(request);
      const data = await response.json();

      expect(response.status).toBe(400);
      expect(data.error).toBe('No organization found');
    });

    it('should handle project creation errors', async () => {
      mockSupabase.rpc.mockResolvedValue({
        data: null,
        error: new Error('Database error'),
      });

      const request = new NextRequest('http://localhost:3000/api/projects', {
        method: 'POST',
        body: JSON.stringify(validProjectData),
      });

      const response = await POST(request);
      const data = await response.json();

      expect(response.status).toBe(500);
      expect(data.error).toBe('Failed to create project');
    });
  });
});
