import puppeteer, { Browser } from 'puppeteer';
import robotsParser from 'robots-parser';
import { createServerSupabase } from '@/lib/supabase-server';
import { uploadFile } from '@/lib/storage';
import { extractDomain, sleep } from '@/lib/utils';
import { VisualBrandAnalyzer } from './visual-brand-analyzer';
import {
  ScrapingError,
  TimeoutError,
  NetworkError,
  RobotsBlockedError,
  createScrapingError,
  logError
} from '@/lib/errors';

export interface ScrapingConfig {
  maxPages: number;
  includeImages: boolean;
  includeDocuments: boolean;
  respectRobots: boolean;
  delayBetweenRequests: number;
  maxConcurrent: number;
}

export interface ScrapedAsset {
  type: 'logo' | 'image' | 'document' | 'video';
  url: string;
  filename: string;
  alt?: string;
  context?: string;
}

export interface VisualBrandData {
  logos: {
    primary?: string;
    variations: string[];
    favicon?: string;
  };
  colorPalette: {
    primary: string[];
    secondary: string[];
    accent: string[];
    dominantColor: string;
  };
  typography: {
    headingFonts: string[];
    bodyFonts: string[];
    fontPairings: string[];
  };
  visualStyle: {
    mood: string;
    personality: string[];
    designTrends: string[];
  };
  screenshots: {
    homepage: string;
    keyPages: string[];
    mobile: string[];
  };
}

export interface ScrapingResult {
  brandId: string;
  assets: ScrapedAsset[];
  textContent: string[];
  visualData: VisualBrandData;
  metadata: {
    title: string;
    description: string;
    keywords: string[];
    socialMedia: Record<string, string>;
  };
  errors: string[];
}

export class BrandScraperService {
  private browser: Browser | null = null;
  private config: ScrapingConfig;
  private visualAnalyzer: VisualBrandAnalyzer;

  constructor(config: Partial<ScrapingConfig> = {}) {
    this.config = {
      maxPages: 10,
      includeImages: true,
      includeDocuments: true,
      respectRobots: true,
      delayBetweenRequests: 2000,
      maxConcurrent: 3,
      ...config,
    };
    this.visualAnalyzer = new VisualBrandAnalyzer();
  }

  async initialize(): Promise<void> {
    if (!this.browser) {
      this.browser = await puppeteer.launch({
        headless: 'new',
        args: [
          '--no-sandbox',
          '--disable-setuid-sandbox',
          '--disable-dev-shm-usage',
          '--disable-accelerated-2d-canvas',
          '--no-first-run',
          '--no-zygote',
          '--disable-gpu',
        ],
      });
    }
  }

  async cleanup(): Promise<void> {
    if (this.browser) {
      try {
        // Add timeout to prevent hanging
        await Promise.race([
          this.browser.close(),
          new Promise((_, reject) =>
            setTimeout(() => reject(new TimeoutError('browser-cleanup', 5000)), 5000)
          )
        ]);
      } catch (error) {
        logError(error, { context: 'browser-cleanup' });
      } finally {
        this.browser = null;
      }
    }
  }

  async checkRobotsTxt(baseUrl: string, userAgent = '*'): Promise<boolean> {
    if (!this.config.respectRobots) return true;

    try {
      const robotsUrl = new URL('/robots.txt', baseUrl).toString();
      const response = await fetch(robotsUrl, {
        signal: AbortSignal.timeout(5000) // 5 second timeout
      });

      if (!response.ok) return true; // No robots.txt, allow scraping

      const robotsTxt = await response.text();
      const robots = robotsParser(robotsUrl, robotsTxt);

      const isAllowed = robots.isAllowed(baseUrl, userAgent) ?? true;

      if (!isAllowed) {
        throw new RobotsBlockedError(baseUrl);
      }

      return isAllowed;
    } catch (error) {
      if (error instanceof RobotsBlockedError) {
        throw error; // Re-throw robots blocking error
      }

      logError(error, { context: 'robots-txt-check', baseUrl });
      return true; // Default to allowing if check fails
    }
  }

  // Overload for different method signatures
  async scrapeBrand(brandId: string, config?: Partial<ScrapingConfig>): Promise<ScrapingResult>;
  async scrapeBrand(brandId: string, websiteUrl: string): Promise<ScrapingResult>;
  async scrapeBrand(brandId: string, websiteUrlOrConfig?: string | Partial<ScrapingConfig>): Promise<ScrapingResult> {
    const result: ScrapingResult = {
      brandId,
      assets: [],
      textContent: [],
      visualData: {
        logos: {
          variations: [],
        },
        colorPalette: {
          primary: [],
          secondary: [],
          accent: [],
          dominantColor: '#000000',
        },
        typography: {
          headingFonts: [],
          bodyFonts: [],
          fontPairings: [],
        },
        visualStyle: {
          mood: '',
          personality: [],
          designTrends: [],
        },
        screenshots: {
          homepage: '',
          keyPages: [],
          mobile: [],
        },
      },
      metadata: {
        title: '',
        description: '',
        keywords: [],
        socialMedia: {},
      },
      errors: [],
    };

    try {
      // Handle different method signatures
      let websiteUrl: string;

      if (typeof websiteUrlOrConfig === 'string') {
        // Called with (brandId, websiteUrl)
        websiteUrl = websiteUrlOrConfig;
      } else {
        // Called with (brandId, config) - need to get URL from database
        const supabase = createServerSupabase();
        const { data: brand } = await supabase
          .from('brands')
          .select('website_url')
          .eq('id', brandId)
          .single();

        if (!brand?.website_url) {
          result.errors.push('Brand website URL not found');
          return result;
        }
        websiteUrl = brand.website_url;
      }

      await this.initialize();

      // Check robots.txt
      try {
        await this.checkRobotsTxt(websiteUrl);
      } catch (error) {
        if (error instanceof RobotsBlockedError) {
          result.errors.push(error.message);
          await this.updateBrandStatus(brandId, 'failed');
          return result;
        }
        // Log but continue for other robots.txt errors
        logError(error, { context: 'robots-check', websiteUrl });
      }

      // Update brand status
      await this.updateBrandStatus(brandId, 'in_progress');

      // Scrape main page with visual analysis
      const mainPageResult = await this.scrapePageWithVisuals(websiteUrl);
      result.assets.push(...mainPageResult.assets);
      result.textContent.push(...mainPageResult.textContent);
      result.metadata = { ...result.metadata, ...mainPageResult.metadata };
      result.visualData = mainPageResult.visualData;

      // Find and scrape additional pages
      const additionalUrls = this.findAdditionalUrls(mainPageResult.links, websiteUrl);
      const limitedUrls = additionalUrls.slice(0, this.config.maxPages - 1);

      for (const url of limitedUrls) {
        try {
          await sleep(this.config.delayBetweenRequests);
          const pageResult = await this.scrapePage(url);
          result.assets.push(...pageResult.assets);
          result.textContent.push(...pageResult.textContent);
        } catch (error) {
          const scrapingError = createScrapingError(url, error);
          result.errors.push(scrapingError.message);
          logError(scrapingError, { context: 'page-scraping', url });
        }
      }

      // Process and upload assets
      await this.processAssets(result.assets, brandId);

      // Update brand status
      await this.updateBrandStatus(brandId, 'completed');

    } catch (error) {
      // Use a fallback URL if websiteUrl is not in scope
      const url = 'unknown-url';
      const scrapingError = createScrapingError(url, error);
      result.errors.push(scrapingError.message);
      logError(scrapingError, {
        context: 'brand-scraping',
        brandId
      });
      await this.updateBrandStatus(brandId, 'failed');
    }

    return result;
  }

  private async scrapePageWithVisuals(url: string): Promise<{
    assets: ScrapedAsset[];
    textContent: string[];
    metadata: any;
    links: string[];
    visualData: VisualBrandData;
  }> {
    if (!this.browser) throw new Error('Browser not initialized');

    const page = await this.browser.newPage();

    try {
      // Set user agent and viewport
      await page.setUserAgent('Mozilla/5.0 (compatible; BrandAuditBot/1.0)');
      await page.setViewport({ width: 1920, height: 1080 });

      // Navigate to page
      await page.goto(url, {
        waitUntil: 'networkidle2',
        timeout: 30000
      });

      // Wait for dynamic content
      await new Promise(resolve => setTimeout(resolve, 2000));

      // Perform visual analysis
      const visualData = await this.visualAnalyzer.analyzeVisualBrand(page, url);

      // Extract regular page content
      const content = await page.evaluate(() => {
        const assets: ScrapedAsset[] = [];
        const textContent: string[] = [];
        const links: string[] = [];

        // Extract images
        document.querySelectorAll('img').forEach(img => {
          const src = img.src || img.getAttribute('data-src');
          if (src && src.startsWith('http')) {
            assets.push({
              type: 'image',
              url: src,
              filename: src.split('/').pop() || 'image',
              alt: img.alt || '',
              context: img.closest('section')?.className || '',
            });
          }
        });

        // Extract logos (common selectors)
        const logoSelectors = [
          '.logo img',
          '.brand img',
          '.header img',
          '[class*="logo"] img',
          '[id*="logo"] img',
        ];

        logoSelectors.forEach(selector => {
          document.querySelectorAll(selector).forEach(img => {
            const src = (img as HTMLImageElement).src;
            if (src && src.startsWith('http')) {
              assets.push({
                type: 'logo',
                url: src,
                filename: src.split('/').pop() || 'logo',
                alt: (img as HTMLImageElement).alt || '',
                context: 'logo',
              });
            }
          });
        });

        // Extract documents
        document.querySelectorAll('a[href]').forEach(link => {
          const href = (link as HTMLAnchorElement).href;
          if (href && (href.includes('.pdf') || href.includes('.doc'))) {
            assets.push({
              type: 'document',
              url: href,
              filename: href.split('/').pop() || 'document',
              context: link.textContent?.trim() || '',
            });
          }
        });

        // Extract text content
        const textElements = document.querySelectorAll('h1, h2, h3, p, .tagline, .slogan, .mission, .vision');
        textElements.forEach(el => {
          const text = el.textContent?.trim();
          if (text && text.length > 10 && text.length < 500) {
            textContent.push(text);
          }
        });

        // Extract links
        document.querySelectorAll('a[href]').forEach(link => {
          const href = (link as HTMLAnchorElement).href;
          if (href && href.startsWith('http')) {
            links.push(href);
          }
        });

        // Extract metadata
        const title = document.title || '';
        const description = document.querySelector('meta[name="description"]')?.getAttribute('content') || '';
        const keywords = document.querySelector('meta[name="keywords"]')?.getAttribute('content')?.split(',') || [];

        // Extract social media links
        const socialMedia: Record<string, string> = {};
        document.querySelectorAll('a[href*="facebook"], a[href*="twitter"], a[href*="instagram"], a[href*="linkedin"]').forEach(link => {
          const href = (link as HTMLAnchorElement).href;
          if (href.includes('facebook')) socialMedia.facebook = href;
          if (href.includes('twitter')) socialMedia.twitter = href;
          if (href.includes('instagram')) socialMedia.instagram = href;
          if (href.includes('linkedin')) socialMedia.linkedin = href;
        });

        return {
          assets,
          textContent,
          links,
          metadata: {
            title,
            description,
            keywords,
            socialMedia,
          },
        };
      });

      return {
        ...content,
        visualData,
      };

    } finally {
      await page.close();
    }
  }

  private async scrapePage(url: string): Promise<{
    assets: ScrapedAsset[];
    textContent: string[];
    metadata: any;
    links: string[];
  }> {
    if (!this.browser) throw new Error('Browser not initialized');

    const page = await this.browser.newPage();
    
    try {
      // Set user agent and viewport
      await page.setUserAgent('Mozilla/5.0 (compatible; BrandAuditBot/1.0)');
      await page.setViewport({ width: 1920, height: 1080 });

      // Navigate to page
      await page.goto(url, { 
        waitUntil: 'networkidle2',
        timeout: 30000 
      });

      // Wait for dynamic content
      await new Promise(resolve => setTimeout(resolve, 2000));

      // Extract page content
      const content = await page.evaluate(() => {
        const assets: ScrapedAsset[] = [];
        const textContent: string[] = [];
        const links: string[] = [];

        // Extract images
        document.querySelectorAll('img').forEach(img => {
          const src = img.src || img.getAttribute('data-src');
          if (src && src.startsWith('http')) {
            assets.push({
              type: 'image',
              url: src,
              filename: src.split('/').pop() || 'image',
              alt: img.alt || '',
              context: img.closest('section')?.className || '',
            });
          }
        });

        // Extract logos (common selectors)
        const logoSelectors = [
          '.logo img',
          '.brand img',
          '.header img',
          '[class*="logo"] img',
          '[id*="logo"] img',
        ];

        logoSelectors.forEach(selector => {
          document.querySelectorAll(selector).forEach(img => {
            const src = (img as HTMLImageElement).src;
            if (src && src.startsWith('http')) {
              assets.push({
                type: 'logo',
                url: src,
                filename: src.split('/').pop() || 'logo',
                alt: (img as HTMLImageElement).alt || '',
                context: 'logo',
              });
            }
          });
        });

        // Extract documents
        document.querySelectorAll('a[href]').forEach(link => {
          const href = (link as HTMLAnchorElement).href;
          if (href && (href.includes('.pdf') || href.includes('.doc'))) {
            assets.push({
              type: 'document',
              url: href,
              filename: href.split('/').pop() || 'document',
              context: link.textContent?.trim() || '',
            });
          }
        });

        // Extract text content
        const textElements = document.querySelectorAll('h1, h2, h3, p, .tagline, .slogan, .mission, .vision');
        textElements.forEach(el => {
          const text = el.textContent?.trim();
          if (text && text.length > 10 && text.length < 500) {
            textContent.push(text);
          }
        });

        // Extract links
        document.querySelectorAll('a[href]').forEach(link => {
          const href = (link as HTMLAnchorElement).href;
          if (href && href.startsWith('http')) {
            links.push(href);
          }
        });

        // Extract metadata
        const title = document.title || '';
        const description = document.querySelector('meta[name="description"]')?.getAttribute('content') || '';
        const keywords = document.querySelector('meta[name="keywords"]')?.getAttribute('content')?.split(',') || [];

        // Extract social media links
        const socialMedia: Record<string, string> = {};
        document.querySelectorAll('a[href*="facebook"], a[href*="twitter"], a[href*="instagram"], a[href*="linkedin"]').forEach(link => {
          const href = (link as HTMLAnchorElement).href;
          if (href.includes('facebook')) socialMedia.facebook = href;
          if (href.includes('twitter')) socialMedia.twitter = href;
          if (href.includes('instagram')) socialMedia.instagram = href;
          if (href.includes('linkedin')) socialMedia.linkedin = href;
        });

        return {
          assets,
          textContent,
          links,
          metadata: {
            title,
            description,
            keywords,
            socialMedia,
          },
        };
      });

      return content;

    } finally {
      await page.close();
    }
  }

  private findAdditionalUrls(links: string[], baseUrl: string): string[] {
    const domain = extractDomain(baseUrl);
    const relevantPages = [
      'about',
      'brand',
      'story',
      'mission',
      'vision',
      'values',
      'press',
      'media',
      'news',
    ];

    return links
      .filter(link => {
        try {
          const linkDomain = extractDomain(link);
          return linkDomain === domain;
        } catch {
          return false;
        }
      })
      .filter(link => 
        relevantPages.some(page => 
          link.toLowerCase().includes(page)
        )
      )
      .slice(0, this.config.maxPages);
  }

  private async processAssets(assets: ScrapedAsset[], brandId: string): Promise<void> {
    const supabase = createServerSupabase();

    for (const asset of assets) {
      try {
        // Download asset
        const response = await fetch(asset.url);
        if (!response.ok) continue;

        const buffer = await response.arrayBuffer();
        const uint8Array = new Uint8Array(buffer);

        // Generate filename
        const timestamp = Date.now();
        const filename = `${brandId}/${timestamp}-${asset.filename}`;

        // Determine bucket based on asset type
        const bucket = asset.type === 'logo' ? 'brand-logos' : 'campaign-assets';

        // Upload to Supabase Storage
        await uploadFile(bucket, filename, uint8Array, {
          contentType: response.headers.get('content-type') || 'application/octet-stream',
        });

        // Save asset record to database
        await supabase.from('assets').insert({
          brand_id: brandId,
          type: asset.type,
          url: `${bucket}/${filename}`,
          filename: asset.filename,
          file_size: buffer.byteLength,
          mime_type: response.headers.get('content-type') || 'application/octet-stream',
          alt_text: asset.alt,
          metadata: {
            original_url: asset.url,
            context: asset.context,
            scraped_at: new Date().toISOString(),
          },
        });

      } catch (error) {
        console.error(`Error processing asset ${asset.url}:`, error);
      }
    }
  }

  private async updateBrandStatus(brandId: string, status: 'pending' | 'in_progress' | 'completed' | 'failed'): Promise<void> {
    const supabase = createServerSupabase();
    
    await supabase
      .from('brands')
      .update({ 
        scraping_status: status,
        updated_at: new Date().toISOString(),
      })
      .eq('id', brandId);
  }
}

// Export alias for backward compatibility
export { BrandScraperService as ScraperService };
