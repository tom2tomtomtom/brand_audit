import { Page } from 'puppeteer';
import { VisualBrandAnalyzer } from '../visual-brand-analyzer';
import { VisualBrandData } from '../scraper';

// Mock puppeteer page
const mockPage = {
  screenshot: jest.fn(),
  setViewport: jest.fn(),
  evaluate: jest.fn(),
} as unknown as Page;

describe('VisualBrandAnalyzer', () => {
  let analyzer: VisualBrandAnalyzer;

  beforeEach(() => {
    analyzer = new VisualBrandAnalyzer();
    jest.clearAllMocks();
  });

  describe('analyzeVisualBrand', () => {
    it('should extract visual brand data from a webpage', async () => {
      // Mock screenshot
      const mockScreenshotBuffer = Buffer.from('fake-screenshot');
      mockPage.screenshot = jest.fn().mockResolvedValue(mockScreenshotBuffer);

      // Mock page evaluation results
      const mockExtractedData = {
        logos: ['https://example.com/logo.png', 'https://example.com/favicon.ico'],
        colors: ['rgb(255, 0, 0)', 'rgb(0, 255, 0)', 'rgb(0, 0, 255)', '#FF6600'],
        fonts: ['Arial', 'Helvetica', 'Roboto', 'Open Sans'],
        images: ['https://example.com/hero.jpg', 'https://example.com/banner.png'],
      };

      mockPage.evaluate = jest.fn().mockResolvedValue(mockExtractedData);

      const result = await analyzer.analyzeVisualBrand(mockPage, 'https://example.com');

      // Verify structure
      expect(result).toHaveProperty('logos');
      expect(result).toHaveProperty('colorPalette');
      expect(result).toHaveProperty('typography');
      expect(result).toHaveProperty('visualStyle');
      expect(result).toHaveProperty('screenshots');

      // Verify logos
      expect(result.logos.variations).toEqual(mockExtractedData.logos);
      expect(result.logos.primary).toBe(mockExtractedData.logos[0]);

      // Verify screenshots were taken
      expect(mockPage.screenshot).toHaveBeenCalledTimes(2); // Desktop and mobile
      expect(mockPage.setViewport).toHaveBeenCalledWith({ width: 375, height: 667 }); // Mobile
      expect(mockPage.setViewport).toHaveBeenCalledWith({ width: 1920, height: 1080 }); // Reset

      // Verify colors were processed
      expect(result.colorPalette.primary).toHaveLength(3);
      expect(result.colorPalette.dominantColor).toBeTruthy();
    });

    it('should handle errors gracefully', async () => {
      mockPage.screenshot = jest.fn().mockRejectedValue(new Error('Screenshot failed'));
      mockPage.evaluate = jest.fn().mockResolvedValue({
        logos: [],
        colors: [],
        fonts: [],
        images: [],
      });

      const result = await analyzer.analyzeVisualBrand(mockPage, 'https://example.com');

      // Should return default structure even on error
      expect(result.logos.variations).toEqual([]);
      expect(result.colorPalette.primary).toEqual([]);
      expect(result.typography.headingFonts).toEqual([]);
    });
  });

  describe('processColors', () => {
    it('should normalize and sort colors correctly', () => {
      const analyzer = new VisualBrandAnalyzer();
      const rawColors = [
        'rgb(255, 0, 0)',     // Red -> #ff0000
        'rgba(0, 255, 0, 1)', // Green -> #00ff00
        'rgb(0, 0, 255)',     // Blue -> #0000ff
        '#FFFFFF',            // White
        '#000000',            // Black
        'transparent',        // Should be filtered out
      ];

      // Access private method through any type
      const processColors = (analyzer as any).processColors.bind(analyzer);
      const result = processColors(rawColors);

      expect(result.primary).toHaveLength(3);
      expect(result.secondary).toHaveLength(2);
      expect(result.dominantColor).toBe('#FFFFFF'); // Brightest color
      
      // Verify color format
      result.primary.forEach(color => {
        expect(color).toMatch(/^#[0-9a-f]{6}$/i);
      });
    });

    it('should handle empty color array', () => {
      const analyzer = new VisualBrandAnalyzer();
      const processColors = (analyzer as any).processColors.bind(analyzer);
      const result = processColors([]);

      expect(result.primary).toEqual([]);
      expect(result.secondary).toEqual([]);
      expect(result.accent).toEqual([]);
      expect(result.dominantColor).toBe('#000000');
    });
  });

  describe('normalizeColor', () => {
    it('should convert RGB to hex format', () => {
      const analyzer = new VisualBrandAnalyzer();
      const normalizeColor = (analyzer as any).normalizeColor.bind(analyzer);

      expect(normalizeColor('rgb(255, 0, 0)')).toBe('#ff0000');
      expect(normalizeColor('rgb(0, 255, 0)')).toBe('#00ff00');
      expect(normalizeColor('rgb(0, 0, 255)')).toBe('#0000ff');
      expect(normalizeColor('rgba(255, 128, 0, 0.5)')).toBe('#ff8000');
    });

    it('should return hex colors unchanged', () => {
      const analyzer = new VisualBrandAnalyzer();
      const normalizeColor = (analyzer as any).normalizeColor.bind(analyzer);

      expect(normalizeColor('#FF0000')).toBe('#FF0000');
      expect(normalizeColor('#123456')).toBe('#123456');
    });

    it('should return null for invalid colors', () => {
      const analyzer = new VisualBrandAnalyzer();
      const normalizeColor = (analyzer as any).normalizeColor.bind(analyzer);

      expect(normalizeColor('transparent')).toBeNull();
      expect(normalizeColor('invalid')).toBeNull();
      expect(normalizeColor('')).toBeNull();
    });
  });

  describe('getColorBrightness', () => {
    it('should calculate brightness correctly', () => {
      const analyzer = new VisualBrandAnalyzer();
      const getColorBrightness = (analyzer as any).getColorBrightness.bind(analyzer);

      expect(getColorBrightness('#FFFFFF')).toBe(255); // White - max brightness
      expect(getColorBrightness('#000000')).toBe(0);   // Black - min brightness
      expect(getColorBrightness('#FF0000')).toBeCloseTo(76.245, 2); // Red
      expect(getColorBrightness('#00FF00')).toBeCloseTo(149.685, 2); // Green
      expect(getColorBrightness('#0000FF')).toBeCloseTo(29.07, 2); // Blue
    });
  });

  describe('analyzeVisualStyle', () => {
    it('should detect design trends', async () => {
      // Mock DOM with various styles
      mockPage.evaluate = jest.fn().mockImplementation((fn) => {
        // Simulate the browser environment
        const mockElements = [
          { 
            computedStyle: { 
              background: 'linear-gradient(to right, #000, #fff)',
              borderRadius: '20px',
              boxShadow: '0 4px 6px rgba(0,0,0,0.1)',
              animation: 'none',
              transition: 'all 0.3s ease',
              backgroundColor: 'rgb(255, 255, 255)'
            }
          },
          {
            computedStyle: {
              background: 'none',
              borderRadius: '0px',
              boxShadow: 'none',
              animation: 'slide 2s',
              transition: 'all 0s ease 0s',
              backgroundColor: 'rgb(0, 0, 0)'
            }
          }
        ];

        // Simple mock implementation
        if (fn.toString().includes('analyzeVisualStyle')) {
          return {
            mood: 'sophisticated',
            personality: ['minimalist', 'dynamic'],
            designTrends: ['gradients', 'rounded-design', 'depth-shadows'],
          };
        }
        return {};
      });

      const result = await (analyzer as any).analyzeVisualStyle(mockPage);

      expect(result.mood).toBeTruthy();
      expect(result.personality).toBeInstanceOf(Array);
      expect(result.designTrends).toBeInstanceOf(Array);
      expect(result.designTrends).toContain('gradients');
    });
  });

  describe('Logo extraction', () => {
    it('should extract logos from multiple selectors', async () => {
      const logos = [
        'https://example.com/logo.png',
        'https://example.com/brand.svg',
        'https://example.com/favicon.ico',
      ];

      mockPage.evaluate = jest.fn().mockResolvedValue({
        logos,
        colors: [],
        fonts: [],
        images: [],
      });

      const result = await analyzer.analyzeVisualBrand(mockPage, 'https://example.com');

      expect(result.logos.variations).toEqual(logos);
      expect(result.logos.primary).toBe(logos[0]);
      expect(result.logos.favicon).toBeUndefined(); // Not explicitly set in current implementation
    });
  });

  describe('Typography extraction', () => {
    it('should categorize fonts correctly', async () => {
      const fonts = [
        'Helvetica Neue',
        'Arial',
        'Georgia',
        'Roboto',
        'Open Sans',
        'Montserrat',
      ];

      mockPage.evaluate = jest.fn().mockResolvedValue({
        logos: [],
        colors: [],
        fonts,
        images: [],
      });

      const result = await analyzer.analyzeVisualBrand(mockPage, 'https://example.com');

      expect(result.typography.headingFonts).toEqual(fonts.slice(0, 3));
      expect(result.typography.bodyFonts).toEqual(fonts.slice(3, 6));
    });
  });

  describe('Screenshot handling', () => {
    it('should capture desktop and mobile screenshots', async () => {
      const desktopScreenshot = Buffer.from('desktop-screenshot');
      const mobileScreenshot = Buffer.from('mobile-screenshot');

      mockPage.screenshot = jest.fn()
        .mockResolvedValueOnce(desktopScreenshot)
        .mockResolvedValueOnce(mobileScreenshot);

      mockPage.evaluate = jest.fn().mockResolvedValue({
        logos: [],
        colors: [],
        fonts: [],
        images: [],
      });

      const result = await analyzer.analyzeVisualBrand(mockPage, 'https://example.com');

      // Verify screenshots were taken with correct options
      expect(mockPage.screenshot).toHaveBeenNthCalledWith(1, {
        fullPage: true,
        type: 'png',
      });

      expect(mockPage.screenshot).toHaveBeenNthCalledWith(2, {
        fullPage: true,
        type: 'png',
      });

      // Verify viewport changes
      expect(mockPage.setViewport).toHaveBeenNthCalledWith(1, { width: 375, height: 667 });
      expect(mockPage.setViewport).toHaveBeenNthCalledWith(2, { width: 1920, height: 1080 });

      // Verify base64 encoding
      expect(result.screenshots.homepage).toContain('data:image/png;base64,');
      expect(result.screenshots.mobile[0]).toContain('data:image/png;base64,');
    });
  });
});

describe('VisualBrandData type validation', () => {
  it('should have correct structure', () => {
    const data: VisualBrandData = {
      logos: {
        primary: 'https://example.com/logo.png',
        variations: ['https://example.com/logo.png'],
        favicon: 'https://example.com/favicon.ico',
      },
      colorPalette: {
        primary: ['#FF0000', '#00FF00', '#0000FF'],
        secondary: ['#FFFF00', '#FF00FF', '#00FFFF'],
        accent: ['#FF6600'],
        dominantColor: '#FF0000',
      },
      typography: {
        headingFonts: ['Arial', 'Helvetica'],
        bodyFonts: ['Georgia', 'Times'],
        fontPairings: ['Arial + Georgia'],
      },
      visualStyle: {
        mood: 'modern',
        personality: ['minimalist', 'professional'],
        designTrends: ['flat-design', 'gradients'],
      },
      screenshots: {
        homepage: 'data:image/png;base64,...',
        keyPages: ['data:image/png;base64,...'],
        mobile: ['data:image/png;base64,...'],
      },
    };

    // TypeScript will validate this at compile time
    expect(data).toBeDefined();
  });
});
