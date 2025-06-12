#!/usr/bin/env python3
"""
Test the WebScraper with multiple real websites
"""

import sys
import os
sys.path.append('.')

from src.scraper import WebScraper
import time

def test_multiple_websites():
    """Test scraping multiple real websites"""
    print("🌐 Testing WebScraper with multiple real websites...")
    
    test_sites = [
        {"url": "https://stripe.com", "name": "Stripe"},
        {"url": "https://github.com", "name": "GitHub"},
        {"url": "https://shopify.com", "name": "Shopify"},
        {"url": "https://netflix.com", "name": "Netflix"},
        {"url": "https://spotify.com", "name": "Spotify"}
    ]
    
    scraper = WebScraper()
    successful_scrapes = 0
    total_sites = len(test_sites)
    
    try:
        for i, site in enumerate(test_sites, 1):
            print(f"\n📝 Testing {i}/{total_sites}: {site['name']} ({site['url']})")
            
            try:
                start_time = time.time()
                brand_data = scraper.scrape_brand(site['url'], site['name'])
                end_time = time.time()
                
                # Validate the scraped data
                pages_scraped = len(brand_data.get('pages_scraped', []))
                total_words = brand_data.get('content_analysis', {}).get('total_words', 0)
                visual_assets_count = len(brand_data.get('visual_assets', {}))
                
                print(f"   ✅ Success! Scraped in {end_time - start_time:.2f}s")
                print(f"   📄 Pages scraped: {pages_scraped}")
                print(f"   📝 Total words: {total_words}")
                print(f"   🎨 Visual assets: {visual_assets_count}")
                
                # Check content quality
                if pages_scraped > 0:
                    first_page = brand_data['pages_scraped'][0]
                    content_length = len(first_page.get('content', ''))
                    headings_count = len(first_page.get('headings', []))
                    
                    print(f"   📊 Content length: {content_length} chars")
                    print(f"   📋 Headings found: {headings_count}")
                    
                    if content_length > 100 and headings_count > 0:
                        print(f"   ✅ Quality data extracted for {site['name']}")
                        successful_scrapes += 1
                    else:
                        print(f"   ⚠️  Limited quality data for {site['name']}")
                else:
                    print(f"   ❌ No pages scraped for {site['name']}")
                
            except Exception as e:
                print(f"   ❌ Failed to scrape {site['name']}: {str(e)}")
            
            # Brief pause between requests to be respectful
            if i < total_sites:
                time.sleep(2)
    
    finally:
        if scraper.driver:
            scraper.driver.quit()
    
    print(f"\n📊 Results: {successful_scrapes}/{total_sites} websites successfully scraped")
    print(f"Success rate: {(successful_scrapes/total_sites)*100:.1f}%")
    
    if successful_scrapes >= 3:  # At least 60% success rate
        print("✅ WebScraper is working well with real websites!")
        return True
    else:
        print("❌ WebScraper needs improvement - low success rate")
        return False

if __name__ == "__main__":
    success = test_multiple_websites()
    sys.exit(0 if success else 1)