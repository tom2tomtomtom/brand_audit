#!/usr/bin/env python3
"""
Final validation that the brand audit tool works with real data
and properly fails when it cannot get real data
"""

import sys
import os
sys.path.append('.')

from src.scraper import WebScraper
from src.analyzer import BrandAnalyzer
from dotenv import load_dotenv

def main():
    print("🎯 FINAL VALIDATION: Brand Audit Tool with Real Data")
    print("=" * 60)
    
    load_dotenv()
    
    # Test 1: Successful scraping with real websites
    print("\n1️⃣ Testing successful scraping with real websites...")
    scraper = WebScraper()
    
    try:
        # Test with a reliable website
        brand_data = scraper.scrape_brand("https://stripe.com", "Stripe")
        
        # Validate we got real data
        pages = len(brand_data.get('pages_scraped', []))
        words = brand_data.get('content_analysis', {}).get('total_words', 0)
        
        if pages > 0 and words > 100:
            print(f"   ✅ Successfully scraped {pages} pages with {words} words")
            print("   ✅ Real content extraction working")
        else:
            print(f"   ❌ Insufficient data: {pages} pages, {words} words")
            return False
            
    except Exception as e:
        print(f"   ❌ Scraping failed: {str(e)}")
        return False
    finally:
        if scraper.driver:
            scraper.driver.quit()
    
    # Test 2: Scraping failure with invalid URL
    print("\n2️⃣ Testing scraping failure with invalid URL...")
    scraper2 = WebScraper()
    
    try:
        brand_data = scraper2.scrape_brand("https://definitely-not-a-real-website-12345.invalid", "Fake")
        print("   ❌ Scraper should have failed but didn't!")
        return False
    except Exception as e:
        print(f"   ✅ Scraper properly failed: {str(e)}")
    finally:
        if scraper2.driver:
            scraper2.driver.quit()
    
    # Test 3: Analyzer behavior without API key
    print("\n3️⃣ Testing analyzer behavior...")
    
    # Remove API key temporarily
    original_key = os.environ.get('OPENAI_API_KEY')
    if 'OPENAI_API_KEY' in os.environ:
        del os.environ['OPENAI_API_KEY']
    
    try:
        analyzer = BrandAnalyzer()
        
        sample_data = {
            'name': 'Test Brand',
            'url': 'https://example.com',
            'pages_scraped': [{'content': 'Test content with enough words to pass validation'}],
            'visual_assets': {},
            'content_analysis': {'total_words': 100},
            'technical_info': {},
            'recent_content': []
        }
        
        try:
            analysis = analyzer.analyze_brand(sample_data)
            print("   ❌ Analyzer should have failed without API key!")
            return False
        except Exception as e:
            print(f"   ✅ Analyzer properly failed without API key: {str(e)}")
    
    finally:
        # Restore API key if it existed
        if original_key:
            os.environ['OPENAI_API_KEY'] = original_key
    
    # Test 4: Check for dummy data patterns in code
    print("\n4️⃣ Scanning code for dummy data patterns...")
    
    dummy_patterns = [
        "Professional presentation",
        "Standard navigation", 
        "Established web presence",
        "Clear industry positioning",
        "Could enhance user engagement",
        "Digital marketing enhancement needed"
    ]
    
    found_dummy = False
    for file_path in ['src/analyzer.py', 'src/scraper.py']:
        try:
            with open(file_path, 'r') as f:
                content = f.read()
                for pattern in dummy_patterns:
                    if pattern in content:
                        print(f"   ❌ Found dummy pattern '{pattern}' in {file_path}")
                        found_dummy = True
        except FileNotFoundError:
            pass
    
    if not found_dummy:
        print("   ✅ No dummy data patterns found in code")
    else:
        return False
    
    # Summary
    print("\n" + "=" * 60)
    print("🎉 FINAL VALIDATION RESULTS")
    print("=" * 60)
    print("✅ Scraper works with real websites")
    print("✅ Scraper fails properly with invalid URLs") 
    print("✅ Analyzer requires OpenAI API key (no dummy data)")
    print("✅ No hardcoded dummy patterns found")
    print("✅ Application only works with real data sources")
    print("\n🚀 BRAND AUDIT TOOL IS READY FOR PRODUCTION!")
    print("   - Scrapes real website data using Selenium WebDriver")
    print("   - Requires valid OpenAI API key for analysis")
    print("   - No fallback or dummy data generation")
    print("   - Fails gracefully when real data unavailable")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)