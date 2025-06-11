interface WebsiteData {
  url: string;
  title: string;
  metaDescription: string;
  metaKeywords: string;
  headings: string[];
  content: string;
  links: string[];
  images: string[];
  detectedIndustry?: string;
  recentContent?: any[];
  structuredData?: any;
  performance?: {
    loadTime?: number;
    pageSize?: number;
  };
}

export async function analyzeWebsite(url: string): Promise<WebsiteData> {
  try {
    console.log(`🌐 STARTING REAL FETCH for: ${url}`);
    
    // Fetch the website with a reasonable timeout
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 15000); // 15 second timeout
    
    // Use CORS proxy for client-side fetching (this is why it was failing instantly)
    const proxyUrl = `https://api.allorigins.win/get?url=${encodeURIComponent(url)}`;
    console.log(`🔄 Using CORS proxy: ${proxyUrl}`);
    
    const response = await fetch(proxyUrl, {
      headers: {
        'Accept': 'application/json',
      },
      signal: controller.signal,
    });
    
    clearTimeout(timeoutId);

    if (!response.ok) {
      throw new Error(`Proxy HTTP ${response.status}: ${response.statusText}`);
    }

    const proxyData = await response.json();
    if (proxyData.status?.http_code && proxyData.status.http_code !== 200) {
      throw new Error(`Website returned ${proxyData.status.http_code}`);
    }
    
    const html = proxyData.contents || '';
    console.log(`✅ Successfully fetched ${html.length} characters from ${url} via proxy`);

    // Parse HTML content
    const websiteData = parseHTMLContent(html, url);
    
    return websiteData;

  } catch (error) {
    console.error(`❌ REAL FETCH FAILED for ${url}:`, error);
    
    // Don't return fake data - throw the error so the API knows it failed
    throw new Error(`Failed to fetch website ${url}: ${error instanceof Error ? error.message : 'Unknown error'}`);
  }
}

function parseHTMLContent(html: string, url: string): WebsiteData {
  // Extract title
  const titleMatch = html.match(/<title[^>]*>([^<]+)<\/title>/i);
  const title = titleMatch ? titleMatch[1].trim() : '';

  // Extract meta description
  const descMatch = html.match(/<meta[^>]*name=["\']description["\'][^>]*content=["\']([^"\']+)["\'][^>]*>/i);
  const metaDescription = descMatch ? descMatch[1].trim() : '';

  // Extract meta keywords
  const keywordsMatch = html.match(/<meta[^>]*name=["\']keywords["\'][^>]*content=["\']([^"\']+)["\'][^>]*>/i);
  const metaKeywords = keywordsMatch ? keywordsMatch[1].trim() : '';

  // Extract headings (H1, H2, H3)
  const headingMatches = html.match(/<h[1-3][^>]*>([^<]+)<\/h[1-3]>/gi) || [];
  const headings = headingMatches.map(h => h.replace(/<[^>]+>/g, '').trim()).filter(h => h.length > 0);

  // Extract text content (remove HTML tags)
  const contentMatch = html.replace(/<script[^>]*>[\s\S]*?<\/script>/gi, '')
                          .replace(/<style[^>]*>[\s\S]*?<\/style>/gi, '')
                          .replace(/<[^>]+>/g, ' ')
                          .replace(/\s+/g, ' ')
                          .trim();
  const content = contentMatch.substring(0, 3000); // First 3000 characters for analysis

  // Extract links
  const linkMatches = html.match(/href=["\']([^"\']+)["\']/gi) || [];
  const links = linkMatches.map(l => l.replace(/href=['"]([^'"]+)['"]/, '$1'))
                           .filter(l => l.startsWith('http') || l.startsWith('/'))
                           .slice(0, 20); // Limit to 20 links

  // Extract images
  const imageMatches = html.match(/<img[^>]*src=["\']([^"\']+)["\'][^>]*>/gi) || [];
  const images = imageMatches.map(img => {
    const srcMatch = img.match(/src=["\']([^"\']+)["\']/);
    return srcMatch ? srcMatch[1] : '';
  }).filter(src => src.length > 0).slice(0, 10); // Limit to 10 images

  // Detect industry based on content
  const detectedIndustry = detectIndustryFromContent(title + ' ' + metaDescription + ' ' + content);

  // Look for recent content (news, blog posts, press releases)
  const recentContent = extractRecentContent(html);

  return {
    url,
    title,
    metaDescription,
    metaKeywords,
    headings,
    content,
    links,
    images,
    detectedIndustry,
    recentContent,
  };
}

function detectIndustryFromContent(text: string): string {
  const content = text.toLowerCase();
  
  // Healthcare & Medical
  if (content.includes('health') || content.includes('medical') || content.includes('clinical') || 
      content.includes('patient') || content.includes('healthcare') || content.includes('medicine') ||
      content.includes('pharmaceutical') || content.includes('diagnostic') || content.includes('therapy')) {
    return 'Healthcare & Medical';
  }
  
  // Technology
  if (content.includes('software') || content.includes('technology') || content.includes('digital') ||
      content.includes('platform') || content.includes('cloud') || content.includes('ai') ||
      content.includes('artificial intelligence') || content.includes('saas') || content.includes('tech')) {
    return 'Technology';
  }
  
  // Financial Services
  if (content.includes('financial') || content.includes('banking') || content.includes('investment') ||
      content.includes('insurance') || content.includes('finance') || content.includes('wealth') ||
      content.includes('trading') || content.includes('loan') || content.includes('credit')) {
    return 'Financial Services';
  }
  
  // Education
  if (content.includes('education') || content.includes('learning') || content.includes('university') ||
      content.includes('school') || content.includes('academic') || content.includes('student') ||
      content.includes('course') || content.includes('training')) {
    return 'Education';
  }
  
  // Retail & E-commerce
  if (content.includes('retail') || content.includes('shop') || content.includes('store') ||
      content.includes('ecommerce') || content.includes('marketplace') || content.includes('buy') ||
      content.includes('sell') || content.includes('product')) {
    return 'Retail & E-commerce';
  }
  
  // Consulting & Professional Services
  if (content.includes('consulting') || content.includes('advisory') || content.includes('professional services') ||
      content.includes('strategy') || content.includes('management') || content.includes('expertise')) {
    return 'Consulting & Professional Services';
  }
  
  return 'General Business';
}

function extractRecentContent(html: string): any[] {
  const recentContent = [];
  
  // Look for news/blog sections
  const newsMatches = html.match(/<article[^>]*>[\s\S]*?<\/article>/gi) || [];
  newsMatches.slice(0, 3).forEach((article, index) => {
    const titleMatch = article.match(/<h[1-4][^>]*>([^<]+)<\/h[1-4]>/i);
    const title = titleMatch ? titleMatch[1].trim() : `Article ${index + 1}`;
    
    const dateMatch = article.match(/(\d{4}[-\/]\d{1,2}[-\/]\d{1,2}|\d{1,2}[-\/]\d{1,2}[-\/]\d{4})/);
    const date = dateMatch ? dateMatch[1] : 'Recent';
    
    recentContent.push({
      type: 'article',
      title,
      date,
      source: 'website'
    });
  });
  
  // Look for press release indicators
  const pressMatches = html.match(/press.{0,10}release|news.{0,10}announcement/gi) || [];
  if (pressMatches.length > 0) {
    recentContent.push({
      type: 'press',
      title: 'Recent press releases and announcements',
      date: 'Recent',
      source: 'website'
    });
  }
  
  return recentContent;
}

function createFallbackWebsiteData(url: string, error: any): WebsiteData {
  const domain = url.replace(/https?:\/\//, '').replace(/www\./, '').split('/')[0];
  const brandName = domain.split('.')[0];
  
  return {
    url,
    title: `${brandName.charAt(0).toUpperCase() + brandName.slice(1)} - Official Website`,
    metaDescription: `${brandName} provides innovative solutions and services.`,
    metaKeywords: brandName,
    headings: [`Welcome to ${brandName}`, 'Our Services', 'About Us'],
    content: `${brandName} is a leading company providing innovative solutions to customers worldwide. We focus on delivering high-quality products and exceptional customer service.`,
    links: [],
    images: [],
    detectedIndustry: 'General Business',
    recentContent: [{
      type: 'notice',
      title: 'Website analysis limited due to access restrictions',
      date: new Date().toISOString().split('T')[0],
      source: 'system'
    }],
  };
}