import { BrandScraperService, ScrapingConfig } from '../scraper';
import puppeteer from 'puppeteer';

// Mock dependencies
jest.mock('puppeteer');
jest.mock('robots-parser');
jest.mock('@/lib/supabase-server');
jest.mock('@/lib/storage');
jest.mock('@/lib/utils');

const mockPuppeteer = puppeteer as jest.Mocked<typeof puppeteer>;

describe('BrandScraperService', () => {
  let service: BrandScraperService;
  let mockBrowser: any;
  let mockPage: any;

  const defaultConfig: ScrapingConfig = {
    maxPages: 5,
    includeImages: true,
    includeDocuments: true,
    respectRobots: true,
    delayBetweenRequests: 1000,
    maxConcurrent: 2,
  };

  beforeEach(() => {
    jest.clearAllMocks();

    // Setup mock page
    mockPage = {
      goto: jest.fn().mockResolvedValue(undefined),
      content: jest.fn().mockResolvedValue('<html><body>Test content</body></html>'),
      close: jest.fn().mockResolvedValue(undefined),
      setUserAgent: jest.fn().mockResolvedValue(undefined),
      setViewport: jest.fn().mockResolvedValue(undefined),
      waitForTimeout: jest.fn().mockResolvedValue(undefined),
      evaluate: jest.fn().mockResolvedValue({}),
      $$eval: jest.fn().mockResolvedValue([]),
    };

    // Setup mock browser
    mockBrowser = {
      newPage: jest.fn().mockResolvedValue(mockPage),
      close: jest.fn().mockResolvedValue(undefined),
    };

    mockPuppeteer.launch.mockResolvedValue(mockBrowser);

    service = new BrandScraperService(defaultConfig);
  });

  describe('initialization', () => {
    it('should initialize with default config', () => {
      const defaultService = new BrandScraperService();
      expect(defaultService).toBeInstanceOf(BrandScraperService);
    });

    it('should initialize with custom config', () => {
      const customConfig = { maxPages: 20, includeImages: false };
      const customService = new BrandScraperService(customConfig);
      expect(customService).toBeInstanceOf(BrandScraperService);
    });

    it('should launch browser on initialize', async () => {
      await service.initialize();

      expect(mockPuppeteer.launch).toHaveBeenCalledWith({
        headless: 'new',
        args: expect.arrayContaining([
          '--no-sandbox',
          '--disable-setuid-sandbox',
          '--disable-dev-shm-usage',
        ]),
      });
    });
  });

  describe('cleanup', () => {
    it('should close browser on cleanup', async () => {
      await service.initialize();
      await service.cleanup();

      expect(mockBrowser.close).toHaveBeenCalled();
    });

    it('should handle cleanup when browser is not initialized', async () => {
      await expect(service.cleanup()).resolves.not.toThrow();
    });
  });

  describe('checkRobotsTxt', () => {
    it('should check robots.txt when respectRobots is true', async () => {
      const robotsParser = require('robots-parser');
      const mockRobots = {
        isAllowed: jest.fn().mockReturnValue(true),
      };
      robotsParser.mockReturnValue(mockRobots);

      const result = await service.checkRobotsTxt('https://example.com', 'BrandAuditBot');

      expect(result).toBe(true);
      expect(robotsParser).toHaveBeenCalledWith(
        'https://example.com/robots.txt',
        'BrandAuditBot'
      );
    });

    it('should return true when respectRobots is false', async () => {
      const noRobotsService = new BrandScraperService({ ...defaultConfig, respectRobots: false });
      const result = await noRobotsService.checkRobotsTxt('https://example.com', 'BrandAuditBot');

      expect(result).toBe(true);
    });

    it('should handle robots.txt fetch errors', async () => {
      const robotsParser = require('robots-parser');
      robotsParser.mockImplementation(() => {
        throw new Error('Failed to fetch robots.txt');
      });

      const result = await service.checkRobotsTxt('https://example.com', 'BrandAuditBot');

      expect(result).toBe(true); // Should default to allowing when robots.txt fails
    });
  });

  describe('scrapeBrand', () => {
    beforeEach(() => {
      // Mock Supabase operations
      const { createServerSupabase } = require('@/lib/supabase-server');
      const mockSupabase = {
        from: jest.fn(() => ({
          select: jest.fn().mockReturnThis(),
          eq: jest.fn().mockReturnThis(),
          single: jest.fn().mockResolvedValue({
            data: {
              id: 'brand-id',
              name: 'Test Brand',
              website_url: 'https://example.com',
            },
          }),
          update: jest.fn().mockReturnThis(),
        })),
      };
      createServerSupabase.mockReturnValue(mockSupabase);

      // Mock storage operations
      const { uploadFile } = require('@/lib/storage');
      uploadFile.mockResolvedValue('uploaded-file-path');

      // Mock utils
      const utils = require('@/lib/utils');
      utils.extractDomain.mockReturnValue('example.com');
      utils.isValidUrl.mockReturnValue(true);
      utils.sanitizeFilename.mockImplementation((name) => name);
      utils.sleep.mockResolvedValue(undefined);
    });

    it('should scrape brand successfully', async () => {
      await service.initialize();

      // Mock page content with assets
      mockPage.content.mockResolvedValue(`
        <html>
          <head>
            <title>Test Brand</title>
            <meta name="description" content="Test brand description">
          </head>
          <body>
            <h1>Welcome to Test Brand</h1>
            <img src="/logo.png" alt="Test Brand Logo">
            <a href="/about">About Us</a>
          </body>
        </html>
      `);

      // Mock evaluate for extracting data
      mockPage.evaluate.mockResolvedValue({
        title: 'Test Brand',
        description: 'Test brand description',
        socialLinks: [],
      });

      // Mock $$eval for finding assets and links
      mockPage.$$eval
        .mockResolvedValueOnce([
          { src: 'https://example.com/logo.png', alt: 'Test Brand Logo' },
        ]) // Images
        .mockResolvedValueOnce([
          { href: 'https://example.com/about' },
        ]); // Links

      const result = await service.scrapeBrand('brand-id');

      expect(result.brandId).toBe('brand-id');
      expect(result.assets).toHaveLength(1);
      expect(result.assets[0]).toEqual({
        type: 'logo',
        url: 'https://example.com/logo.png',
        filename: 'logo.png',
        alt: 'Test Brand Logo',
      });
      expect(result.textContent).toContain('Welcome to Test Brand');
      expect(result.metadata.title).toBe('Test Brand');
      expect(result.errors).toHaveLength(0);
    });

    it('should handle scraping errors gracefully', async () => {
      await service.initialize();

      mockPage.goto.mockRejectedValue(new Error('Page load failed'));

      const result = await service.scrapeBrand('brand-id');

      expect(result.errors).toHaveLength(1);
      expect(result.errors[0]).toContain('Scraping failed');
    });

    it('should respect robots.txt when configured', async () => {
      const robotsParser = require('robots-parser');
      const mockRobots = {
        isAllowed: jest.fn().mockReturnValue(false),
      };
      robotsParser.mockReturnValue(mockRobots);

      await service.initialize();

      const result = await service.scrapeBrand('brand-id');

      expect(result.errors).toHaveLength(1);
      expect(result.errors[0]).toContain('robots.txt');
    });

    it('should limit pages scraped according to config', async () => {
      const limitedService = new BrandScraperService({ ...defaultConfig, maxPages: 2 });
      await limitedService.initialize();

      // Mock multiple pages being found
      mockPage.$$eval.mockResolvedValue([
        { href: 'https://example.com/page1' },
        { href: 'https://example.com/page2' },
        { href: 'https://example.com/page3' },
        { href: 'https://example.com/page4' },
      ]);

      const result = await limitedService.scrapeBrand('brand-id');

      // Should only scrape main page + 1 additional page (maxPages - 1)
      expect(mockPage.goto).toHaveBeenCalledTimes(2);
    });
  });

  describe('findAdditionalUrls', () => {
    it('should filter and prioritize URLs correctly', () => {
      const links = [
        'https://example.com/about',
        'https://example.com/products',
        'https://example.com/contact',
        'https://other-domain.com/page',
        'mailto:test@example.com',
        '#anchor',
      ];

      const additionalUrls = (service as any).findAdditionalUrls(links, 'https://example.com');

      expect(additionalUrls).toEqual([
        'https://example.com/about',
        'https://example.com/products',
        'https://example.com/contact',
      ]);
    });

    it('should prioritize important pages', () => {
      const links = [
        'https://example.com/random',
        'https://example.com/about',
        'https://example.com/products',
        'https://example.com/services',
      ];

      const additionalUrls = (service as any).findAdditionalUrls(links, 'https://example.com');

      // About and products should be prioritized
      expect(additionalUrls[0]).toBe('https://example.com/about');
      expect(additionalUrls[1]).toBe('https://example.com/products');
    });
  });

  describe('categorizeAsset', () => {
    it('should categorize assets correctly', () => {
      expect((service as any).categorizeAsset('logo.png', 'Company Logo')).toBe('logo');
      expect((service as any).categorizeAsset('image.jpg', 'Product image')).toBe('image');
      expect((service as any).categorizeAsset('document.pdf', 'Brochure')).toBe('document');
      expect((service as any).categorizeAsset('video.mp4', 'Promotional video')).toBe('video');
      expect((service as any).categorizeAsset('unknown.xyz', 'Unknown file')).toBe('image');
    });
  });
});
