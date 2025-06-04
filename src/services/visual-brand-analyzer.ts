import { Page } from 'puppeteer';
import { VisualBrandData } from './scraper';

export class VisualBrandAnalyzer {
  
  async analyzeVisualBrand(page: Page, _websiteUrl: string): Promise<VisualBrandData> {
    const visualData: VisualBrandData = {
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
    };

    try {
      // Take homepage screenshot
      const screenshotBuffer = await page.screenshot({
        fullPage: true,
        type: 'png',
      });
      
      // Convert to base64 for storage
      visualData.screenshots.homepage = `data:image/png;base64,${screenshotBuffer.toString('base64')}`;

      // Extract visual elements
      const extractedData = await page.evaluate(() => {
        const results = {
          logos: [] as string[],
          colors: [] as string[],
          fonts: [] as string[],
          images: [] as string[],
        };

        // Extract logos with enhanced selectors
        const logoSelectors = [
          '.logo img',
          '.brand img', 
          '.header img',
          '.navbar img',
          '[class*="logo"] img',
          '[id*="logo"] img',
          '[alt*="logo" i] img',
          '[alt*="brand" i] img',
          'header img[src*="logo"]',
          'nav img[src*="logo"]',
        ];

        logoSelectors.forEach(selector => {
          document.querySelectorAll(selector).forEach(img => {
            const src = (img as HTMLImageElement).src;
            if (src && src.startsWith('http') && !results.logos.includes(src)) {
              results.logos.push(src);
            }
          });
        });

        // Extract favicon
        const favicon = document.querySelector('link[rel*="icon"]') as HTMLLinkElement;
        if (favicon?.href) {
          results.logos.push(favicon.href);
        }

        // Extract colors from CSS
        const extractColorsFromElement = (element: Element): string[] => {
          const colors: string[] = [];
          const computedStyle = window.getComputedStyle(element);
          
          // Get background colors
          const bgColor = computedStyle.backgroundColor;
          if (bgColor && bgColor !== 'rgba(0, 0, 0, 0)' && bgColor !== 'transparent') {
            colors.push(bgColor);
          }

          // Get text colors
          const textColor = computedStyle.color;
          if (textColor && textColor !== 'rgba(0, 0, 0, 0)') {
            colors.push(textColor);
          }

          // Get border colors
          const borderColor = computedStyle.borderColor;
          if (borderColor && borderColor !== 'rgba(0, 0, 0, 0)') {
            colors.push(borderColor);
          }

          return colors;
        };

        // Extract colors from key elements
        const keyElements = document.querySelectorAll('header, nav, .hero, .banner, .cta, button, .btn, .primary, .secondary, .accent');
        keyElements.forEach(element => {
          const elementColors = extractColorsFromElement(element);
          elementColors.forEach(color => {
            if (!results.colors.includes(color)) {
              results.colors.push(color);
            }
          });
        });

        // Extract fonts
        const extractFontsFromElement = (element: Element): string[] => {
          const fonts: string[] = [];
          const computedStyle = window.getComputedStyle(element);
          const fontFamily = computedStyle.fontFamily;
          
          if (fontFamily) {
            // Clean up font family string
            const cleanFonts = fontFamily
              .split(',')
              .map(font => font.trim().replace(/['"]/g, ''))
              .filter(font => !['serif', 'sans-serif', 'monospace', 'cursive', 'fantasy'].includes(font.toLowerCase()));
            
            fonts.push(...cleanFonts);
          }
          
          return fonts;
        };

        // Extract fonts from headings and body text
        const headingElements = document.querySelectorAll('h1, h2, h3, h4, h5, h6');
        const bodyElements = document.querySelectorAll('p, div, span, .text, .content');

        headingElements.forEach(element => {
          const elementFonts = extractFontsFromElement(element);
          elementFonts.forEach(font => {
            if (!results.fonts.includes(font)) {
              results.fonts.push(font);
            }
          });
        });

        bodyElements.forEach(element => {
          const elementFonts = extractFontsFromElement(element);
          elementFonts.forEach(font => {
            if (!results.fonts.includes(font)) {
              results.fonts.push(font);
            }
          });
        });

        // Extract key brand images
        const brandImages = document.querySelectorAll('img[src*="hero"], img[src*="banner"], .hero img, .banner img, .featured img');
        brandImages.forEach(img => {
          const src = (img as HTMLImageElement).src;
          if (src && src.startsWith('http') && !results.images.includes(src)) {
            results.images.push(src);
          }
        });

        return results;
      });

      // Process extracted data
      visualData.logos.variations = extractedData.logos;
      if (extractedData.logos.length > 0 && extractedData.logos[0]) {
        visualData.logos.primary = extractedData.logos[0]; // First logo as primary
      }
      
      // Process colors
      const processedColors = this.processColors(extractedData.colors);
      visualData.colorPalette = processedColors;

      // Process fonts
      visualData.typography.headingFonts = extractedData.fonts.slice(0, 3);
      visualData.typography.bodyFonts = extractedData.fonts.slice(3, 6);

      // Analyze visual style
      visualData.visualStyle = await this.analyzeVisualStyle(page);

      // Take mobile screenshot
      await page.setViewport({ width: 375, height: 667 });
      const mobileScreenshot = await page.screenshot({
        fullPage: true,
        type: 'png',
      });
      visualData.screenshots.mobile = [`data:image/png;base64,${mobileScreenshot.toString('base64')}`];

      // Reset viewport
      await page.setViewport({ width: 1920, height: 1080 });

    } catch (error) {
      console.error('Error analyzing visual brand:', error);
    }

    return visualData;
  }

  private processColors(rawColors: string[]): VisualBrandData['colorPalette'] {
    const colors = rawColors
      .map(color => this.normalizeColor(color))
      .filter(color => color !== null) as string[];

    // Remove duplicates
    const uniqueColors = Array.from(new Set(colors));

    // Sort by frequency and brightness
    const sortedColors = uniqueColors.sort((a, b) => {
      const brightnessA = this.getColorBrightness(a);
      const brightnessB = this.getColorBrightness(b);
      return brightnessB - brightnessA;
    });

    return {
      primary: sortedColors.slice(0, 3),
      secondary: sortedColors.slice(3, 6),
      accent: sortedColors.slice(6, 9),
      dominantColor: sortedColors[0] || '#000000',
    };
  }

  private normalizeColor(color: string): string | null {
    // Convert rgb/rgba to hex
    const rgbMatch = color.match(/rgba?\((\d+),\s*(\d+),\s*(\d+)(?:,\s*[\d.]+)?\)/);
    if (rgbMatch && rgbMatch[1] && rgbMatch[2] && rgbMatch[3]) {
      const r = rgbMatch[1];
      const g = rgbMatch[2];
      const b = rgbMatch[3];
      return `#${parseInt(r).toString(16).padStart(2, '0')}${parseInt(g).toString(16).padStart(2, '0')}${parseInt(b).toString(16).padStart(2, '0')}`;
    }

    // Return hex colors as-is
    if (color.startsWith('#')) {
      return color;
    }

    return null;
  }

  private getColorBrightness(hex: string): number {
    const r = parseInt(hex.slice(1, 3), 16);
    const g = parseInt(hex.slice(3, 5), 16);
    const b = parseInt(hex.slice(5, 7), 16);
    return (r * 299 + g * 587 + b * 114) / 1000;
  }

  private async analyzeVisualStyle(page: Page): Promise<VisualBrandData['visualStyle']> {
    const styleAnalysis = await page.evaluate(() => {
      const style = {
        mood: 'neutral',
        personality: [] as string[],
        designTrends: [] as string[],
      };

      // Analyze design elements
      const hasGradients = Array.from(document.querySelectorAll('*')).some(el => {
        const computedStyle = window.getComputedStyle(el);
        return computedStyle.background.includes('gradient');
      });

      const hasRoundedCorners = Array.from(document.querySelectorAll('*')).some(el => {
        const computedStyle = window.getComputedStyle(el);
        return parseFloat(computedStyle.borderRadius) > 10;
      });

      const hasShadows = Array.from(document.querySelectorAll('*')).some(el => {
        const computedStyle = window.getComputedStyle(el);
        return computedStyle.boxShadow !== 'none';
      });

      // Determine design trends
      if (hasGradients) style.designTrends.push('gradients');
      if (hasRoundedCorners) style.designTrends.push('rounded-design');
      if (hasShadows) style.designTrends.push('depth-shadows');

      // Analyze layout for personality
      const isMinimalist = document.querySelectorAll('*').length < 100;
      const hasAnimations = Array.from(document.querySelectorAll('*')).some(el => {
        const computedStyle = window.getComputedStyle(el);
        return computedStyle.animation !== 'none' || computedStyle.transition !== 'all 0s ease 0s';
      });

      if (isMinimalist) style.personality.push('minimalist');
      if (hasAnimations) style.personality.push('dynamic');

      // Determine mood based on colors and content
      const darkElements = Array.from(document.querySelectorAll('*')).filter(el => {
        const computedStyle = window.getComputedStyle(el);
        const bgColor = computedStyle.backgroundColor;
        return bgColor.includes('rgb(0') || bgColor.includes('#000');
      });

      if (darkElements.length > 10) {
        style.mood = 'sophisticated';
      } else {
        style.mood = 'friendly';
      }

      return style;
    });

    return styleAnalysis;
  }
}
