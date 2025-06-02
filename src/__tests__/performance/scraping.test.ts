import { BrandScraperService } from '@/services/scraper';
import { performance } from 'perf_hooks';

// Mock dependencies for performance testing
jest.mock('puppeteer');
jest.mock('@/lib/supabase-server');
jest.mock('@/lib/storage');

describe('Scraping Performance Tests', () => {
  let service: BrandScraperService;

  beforeEach(() => {
    service = new BrandScraperService({
      maxPages: 5,
      includeImages: true,
      includeDocuments: true,
      respectRobots: true,
      delayBetweenRequests: 100, // Reduced for testing
      maxConcurrent: 3,
    });

    // Mock Puppeteer for performance testing
    const puppeteer = require('puppeteer');
    const mockBrowser = {
      newPage: jest.fn().mockResolvedValue({
        goto: jest.fn().mockResolvedValue(undefined),
        content: jest.fn().mockResolvedValue('<html><body>Test</body></html>'),
        close: jest.fn().mockResolvedValue(undefined),
        setUserAgent: jest.fn().mockResolvedValue(undefined),
        setViewport: jest.fn().mockResolvedValue(undefined),
        waitForTimeout: jest.fn().mockResolvedValue(undefined),
        evaluate: jest.fn().mockResolvedValue({}),
        $$eval: jest.fn().mockResolvedValue([]),
      }),
      close: jest.fn().mockResolvedValue(undefined),
    };
    puppeteer.launch.mockResolvedValue(mockBrowser);

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

    // Mock storage
    const { uploadFile } = require('@/lib/storage');
    uploadFile.mockResolvedValue('uploaded-file-path');

    // Mock utils
    const utils = require('@/lib/utils');
    utils.extractDomain.mockReturnValue('example.com');
    utils.isValidUrl.mockReturnValue(true);
    utils.sanitizeFilename.mockImplementation((name) => name);
    utils.sleep.mockImplementation((ms) => new Promise(resolve => setTimeout(resolve, ms / 10))); // Speed up for testing
  });

  test('should complete single brand scraping within time limit', async () => {
    const startTime = performance.now();
    
    await service.initialize();
    const result = await service.scrapeBrand('brand-id');
    await service.cleanup();
    
    const endTime = performance.now();
    const duration = endTime - startTime;

    expect(duration).toBeLessThan(10000); // Should complete within 10 seconds
    expect(result.brandId).toBe('brand-id');
    expect(result.errors).toHaveLength(0);
  });

  test('should handle concurrent brand scraping efficiently', async () => {
    const brandIds = ['brand-1', 'brand-2', 'brand-3', 'brand-4', 'brand-5'];
    
    const startTime = performance.now();
    
    await service.initialize();
    
    // Run concurrent scraping
    const promises = brandIds.map(brandId => service.scrapeBrand(brandId));
    const results = await Promise.all(promises);
    
    await service.cleanup();
    
    const endTime = performance.now();
    const duration = endTime - startTime;

    // Should complete all 5 brands faster than sequential processing
    expect(duration).toBeLessThan(30000); // Should complete within 30 seconds
    expect(results).toHaveLength(5);
    results.forEach((result, index) => {
      expect(result.brandId).toBe(brandIds[index]);
    });
  });

  test('should respect rate limiting delays', async () => {
    const serviceWithDelay = new BrandScraperService({
      maxPages: 2,
      delayBetweenRequests: 1000, // 1 second delay
      maxConcurrent: 1,
    });

    const startTime = performance.now();
    
    await serviceWithDelay.initialize();
    await serviceWithDelay.scrapeBrand('brand-id');
    await serviceWithDelay.cleanup();
    
    const endTime = performance.now();
    const duration = endTime - startTime;

    // Should take at least the delay time for additional pages
    expect(duration).toBeGreaterThan(500); // At least some delay
  });

  test('should handle memory usage efficiently', async () => {
    const initialMemory = process.memoryUsage();
    
    await service.initialize();
    
    // Scrape multiple brands to test memory usage
    for (let i = 0; i < 10; i++) {
      await service.scrapeBrand(`brand-${i}`);
    }
    
    await service.cleanup();
    
    const finalMemory = process.memoryUsage();
    const memoryIncrease = finalMemory.heapUsed - initialMemory.heapUsed;
    
    // Memory increase should be reasonable (less than 100MB)
    expect(memoryIncrease).toBeLessThan(100 * 1024 * 1024);
  });

  test('should handle large page content efficiently', async () => {
    // Mock large page content
    const puppeteer = require('puppeteer');
    const mockBrowser = {
      newPage: jest.fn().mockResolvedValue({
        goto: jest.fn().mockResolvedValue(undefined),
        content: jest.fn().mockResolvedValue('<html><body>' + 'x'.repeat(1000000) + '</body></html>'), // 1MB content
        close: jest.fn().mockResolvedValue(undefined),
        setUserAgent: jest.fn().mockResolvedValue(undefined),
        setViewport: jest.fn().mockResolvedValue(undefined),
        waitForTimeout: jest.fn().mockResolvedValue(undefined),
        evaluate: jest.fn().mockResolvedValue({}),
        $$eval: jest.fn().mockResolvedValue([]),
      }),
      close: jest.fn().mockResolvedValue(undefined),
    };
    puppeteer.launch.mockResolvedValue(mockBrowser);

    const startTime = performance.now();
    
    await service.initialize();
    const result = await service.scrapeBrand('brand-id');
    await service.cleanup();
    
    const endTime = performance.now();
    const duration = endTime - startTime;

    expect(duration).toBeLessThan(15000); // Should handle large content within 15 seconds
    expect(result.textContent.length).toBeGreaterThan(0);
  });

  test('should handle network timeouts gracefully', async () => {
    // Mock network timeout
    const puppeteer = require('puppeteer');
    const mockBrowser = {
      newPage: jest.fn().mockResolvedValue({
        goto: jest.fn().mockRejectedValue(new Error('Navigation timeout')),
        close: jest.fn().mockResolvedValue(undefined),
        setUserAgent: jest.fn().mockResolvedValue(undefined),
        setViewport: jest.fn().mockResolvedValue(undefined),
      }),
      close: jest.fn().mockResolvedValue(undefined),
    };
    puppeteer.launch.mockResolvedValue(mockBrowser);

    const startTime = performance.now();
    
    await service.initialize();
    const result = await service.scrapeBrand('brand-id');
    await service.cleanup();
    
    const endTime = performance.now();
    const duration = endTime - startTime;

    expect(duration).toBeLessThan(5000); // Should fail fast
    expect(result.errors.length).toBeGreaterThan(0);
  });

  test('should optimize asset processing', async () => {
    // Mock many assets
    const mockAssets = Array.from({ length: 100 }, (_, i) => ({
      src: `https://example.com/image-${i}.jpg`,
      alt: `Image ${i}`,
    }));

    const puppeteer = require('puppeteer');
    const mockBrowser = {
      newPage: jest.fn().mockResolvedValue({
        goto: jest.fn().mockResolvedValue(undefined),
        content: jest.fn().mockResolvedValue('<html><body>Test</body></html>'),
        close: jest.fn().mockResolvedValue(undefined),
        setUserAgent: jest.fn().mockResolvedValue(undefined),
        setViewport: jest.fn().mockResolvedValue(undefined),
        waitForTimeout: jest.fn().mockResolvedValue(undefined),
        evaluate: jest.fn().mockResolvedValue({}),
        $$eval: jest.fn()
          .mockResolvedValueOnce(mockAssets) // Images
          .mockResolvedValueOnce([]), // Links
      }),
      close: jest.fn().mockResolvedValue(undefined),
    };
    puppeteer.launch.mockResolvedValue(mockBrowser);

    const startTime = performance.now();
    
    await service.initialize();
    const result = await service.scrapeBrand('brand-id');
    await service.cleanup();
    
    const endTime = performance.now();
    const duration = endTime - startTime;

    expect(duration).toBeLessThan(20000); // Should process 100 assets within 20 seconds
    expect(result.assets.length).toBeLessThanOrEqual(100);
  });

  test('should measure scraping throughput', async () => {
    const brandCount = 5;
    const startTime = performance.now();
    
    await service.initialize();
    
    const results = await Promise.all(
      Array.from({ length: brandCount }, (_, i) => 
        service.scrapeBrand(`brand-${i}`)
      )
    );
    
    await service.cleanup();
    
    const endTime = performance.now();
    const duration = endTime - startTime;
    const throughput = brandCount / (duration / 1000); // brands per second

    expect(throughput).toBeGreaterThan(0.1); // At least 0.1 brands per second
    expect(results).toHaveLength(brandCount);
    
    console.log(`Scraping throughput: ${throughput.toFixed(2)} brands/second`);
  });
});
