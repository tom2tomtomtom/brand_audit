// Test script to verify Playwright browser automation is working
const { chromium } = require('playwright');

async function testPlaywright() {
  console.log('🧪 Testing Playwright browser automation...');
  
  let browser;
  try {
    console.log('🚀 Launching browser...');
    browser = await chromium.launch({ headless: true });
    
    const context = await browser.newContext({
      viewport: { width: 1920, height: 1080 }
    });
    
    const page = await context.newPage();
    
    // Test with Wolters Kluwer
    const testUrl = 'https://wolterskluwer.com';
    console.log(`📡 Navigating to ${testUrl}...`);
    
    const start = Date.now();
    await page.goto(testUrl, { waitUntil: 'networkidle' });
    const loadTime = Date.now() - start;
    
    console.log(`✅ Page loaded in ${loadTime}ms`);
    
    // Extract basic data
    const title = await page.title();
    const description = await page.locator('meta[name="description"]').getAttribute('content');
    const headings = await page.locator('h1, h2, h3').allTextContents();
    
    console.log('📊 Extracted Data:');
    console.log(`Title: ${title}`);
    console.log(`Description: ${description?.slice(0, 100)}...`);
    console.log(`Headings found: ${headings.length}`);
    console.log(`First heading: ${headings[0]}`);
    
    // Test color extraction
    const colors = await page.evaluate(() => {
      const foundColors = new Set();
      const elements = document.querySelectorAll('header, nav, .logo, .brand');
      
      elements.forEach(el => {
        const computed = window.getComputedStyle(el);
        const bgColor = computed.backgroundColor;
        if (bgColor && bgColor !== 'rgba(0, 0, 0, 0)') {
          foundColors.add(bgColor);
        }
      });
      
      return Array.from(foundColors);
    });
    
    console.log(`🎨 Colors found: ${colors.length}`);
    console.log('Colors:', colors.slice(0, 3));
    
    console.log('✅ Playwright test completed successfully!');
    
  } catch (error) {
    console.error('❌ Playwright test failed:', error);
  } finally {
    if (browser) {
      await browser.close();
      console.log('🔒 Browser closed');
    }
  }
}

testPlaywright();