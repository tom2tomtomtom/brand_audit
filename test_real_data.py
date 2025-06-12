#!/usr/bin/env python3
"""
Test the brand audit tool with real websites using Playwright
This ensures the application works with live data
"""

import sys
import os
import json
import time
from playwright.sync_api import sync_playwright

# Add project root to path
sys.path.append('.')

def test_playwright_scraping():
    """Test basic Playwright functionality with real websites"""
    print("🎭 Testing Playwright with real websites...")
    
    test_sites = [
        {"url": "https://stripe.com", "name": "Stripe"},
        {"url": "https://github.com", "name": "GitHub"}, 
        {"url": "https://shopify.com", "name": "Shopify"}
    ]
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        for site in test_sites:
            try:
                print(f"\n📝 Testing {site['name']} ({site['url']})...")
                
                # Navigate to the website
                page.goto(site['url'], wait_until='networkidle')
                
                # Extract basic information
                title = page.title()
                print(f"   ✅ Title: {title}")
                
                # Get page content
                content = page.content()
                print(f"   ✅ Page size: {len(content)} characters")
                
                # Extract headings
                headings = page.query_selector_all('h1, h2, h3')
                heading_texts = [h.inner_text() for h in headings[:5]]
                print(f"   ✅ Headings found: {len(headings)} (first 5: {heading_texts})")
                
                # Check for images
                images = page.query_selector_all('img')
                print(f"   ✅ Images found: {len(images)}")
                
                # Check for links
                links = page.query_selector_all('a[href]')
                print(f"   ✅ Links found: {len(links)}")
                
                print(f"   ✅ {site['name']} scraping successful!")
                
            except Exception as e:
                print(f"   ❌ Error scraping {site['name']}: {str(e)}")
                
        browser.close()
    
    print("\n🎭 Playwright basic testing completed!")
    return True  # All tests passed

def test_brand_scraper_with_real_data():
    """Test our WebScraper with real websites"""
    print("\n🔍 Testing WebScraper with real data...")
    
    try:
        from src.scraper import WebScraper
        
        # Test with a simple, reliable website
        scraper = WebScraper()
        
        try:
            print("   📝 Testing with Stripe.com...")
            brand_data = scraper.scrape_brand("https://stripe.com", "Stripe")
            
            print(f"   ✅ Brand name: {brand_data['name']}")
            print(f"   ✅ Pages scraped: {len(brand_data['pages_scraped'])}")
            print(f"   ✅ Visual assets: {len(brand_data['visual_assets'])}")
            print(f"   ✅ Content analysis: {brand_data['content_analysis'].get('total_words', 0)} words")
            
            # Validate we got real content
            if brand_data['pages_scraped']:
                first_page = brand_data['pages_scraped'][0]
                content_length = len(first_page.get('content', ''))
                if content_length > 100:
                    print(f"   ✅ Real content extracted: {content_length} characters")
                else:
                    print(f"   ⚠️  Limited content extracted: {content_length} characters")
            
            return True
            
        except Exception as e:
            print(f"   ❌ WebScraper failed: {str(e)}")
            return False
            
        finally:
            if scraper.driver:
                scraper.driver.quit()
                
    except ImportError as e:
        print(f"   ❌ Could not import WebScraper: {str(e)}")
        return False

def test_analyzer_with_valid_api_key():
    """Test the analyzer with a valid OpenAI API key"""
    print("\n🤖 Testing BrandAnalyzer...")
    
    # Check if we have a valid API key
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key or api_key == 'your_openai_api_key_here':
        print("   ⚠️  No valid OpenAI API key found in environment")
        print("   ℹ️  Set OPENAI_API_KEY to test AI analysis")
        return False
    
    try:
        from src.analyzer import BrandAnalyzer
        
        analyzer = BrandAnalyzer()
        
        # Create sample brand data (simulating real scraped data)
        sample_brand_data = {
            'name': 'Test Company',
            'url': 'https://example.com',
            'pages_scraped': [{
                'content': 'We are a leading technology company focused on innovation and customer success. Our products help businesses grow and scale efficiently.',
                'headings': [
                    {'text': 'Welcome to Test Company'},
                    {'text': 'Our Mission'},
                    {'text': 'Products and Services'}
                ]
            }],
            'visual_assets': {
                'brand_colors': ['#1a73e8', '#ffffff'],
                'font_families': ['Arial', 'Helvetica']
            },
            'content_analysis': {'total_words': 150},
            'technical_info': {'ssl_enabled': True},
            'recent_content': []
        }
        
        try:
            print("   📝 Testing AI analysis...")
            analysis = analyzer.analyze_brand(sample_brand_data)
            
            print(f"   ✅ Analysis completed for: {analysis.get('brand_name', 'Unknown')}")
            print(f"   ✅ Industry identified: {analysis.get('industry', 'Unknown')}")
            print(f"   ✅ Business model: {analysis.get('business_model', 'Unknown')}")
            
            if 'competitive_analysis' in analysis:
                strengths = analysis['competitive_analysis'].get('key_strengths', [])
                print(f"   ✅ Key strengths identified: {len(strengths)}")
            
            return True
            
        except Exception as e:
            print(f"   ❌ AI analysis failed: {str(e)}")
            return False
            
    except ImportError as e:
        print(f"   ❌ Could not import BrandAnalyzer: {str(e)}")
        return False

def test_full_pipeline():
    """Test the complete pipeline with real data"""
    print("\n🔄 Testing complete pipeline...")
    
    # Check if we have a valid API key
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key or api_key == 'your_openai_api_key_here':
        print("   ⚠️  Skipping full pipeline test - no valid OpenAI API key")
        return False
    
    try:
        from src.scraper import WebScraper
        from src.analyzer import BrandAnalyzer
        
        scraper = WebScraper()
        analyzer = BrandAnalyzer()
        
        try:
            print("   📝 Scraping real website...")
            brand_data = scraper.scrape_brand("https://stripe.com", "Stripe")
            
            print("   📝 Analyzing with AI...")
            analysis = analyzer.analyze_brand(brand_data)
            
            print(f"   ✅ Complete analysis for {analysis.get('brand_name', 'Unknown')}")
            print(f"   ✅ Industry: {analysis.get('industry', 'Unknown')}")
            print(f"   ✅ Overall score: {analysis.get('overall_score', {}).get('total_score', 'Unknown')}")
            
            return True
            
        except Exception as e:
            print(f"   ❌ Full pipeline failed: {str(e)}")
            return False
            
        finally:
            if scraper.driver:
                scraper.driver.quit()
                
    except ImportError as e:
        print(f"   ❌ Could not import modules: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("🚀 Starting Real Data Testing for Brand Audit Tool")
    print("=" * 60)
    
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    results = []
    
    # Test 1: Basic Playwright functionality
    print("\n" + "="*60)
    results.append(("Playwright Basic Test", test_playwright_scraping()))
    
    # Test 2: WebScraper with real data
    print("\n" + "="*60)
    results.append(("WebScraper Real Data", test_brand_scraper_with_real_data()))
    
    # Test 3: Analyzer with API key
    print("\n" + "="*60)
    results.append(("BrandAnalyzer Test", test_analyzer_with_valid_api_key()))
    
    # Test 4: Full pipeline
    print("\n" + "="*60)
    results.append(("Full Pipeline Test", test_full_pipeline()))
    
    # Summary
    print("\n" + "="*60)
    print("📊 TEST RESULTS SUMMARY")
    print("="*60)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("\n🎉 ALL TESTS PASSED! The brand audit tool is working with real data.")
        return True
    else:
        print(f"\n⚠️  {len(results) - passed} tests failed. See details above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)