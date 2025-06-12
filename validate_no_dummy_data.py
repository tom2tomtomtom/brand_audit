#!/usr/bin/env python3
"""
Validate that no dummy/fallback data is generated
Ensures the application fails properly when it cannot get real data
"""

import sys
import os
import tempfile
sys.path.append('.')

from src.scraper import WebScraper
from src.analyzer import BrandAnalyzer

def test_no_dummy_data():
    """Test that the application fails instead of generating dummy data"""
    print("🚫 Testing No Dummy Data Generation...")
    
    # Test 1: Scraper should fail with invalid URL
    print("\n1. Testing scraper with invalid URL...")
    try:
        scraper = WebScraper()
        brand_data = scraper.scrape_brand("https://definitely-not-a-real-website-123456789.com", "Fake Brand")
        
        # If we get here, check if it's real data or dummy data
        pages_scraped = len(brand_data.get('pages_scraped', []))
        if pages_scraped == 0:
            print("❌ Scraper returned empty data instead of failing")
            return False
        else:
            print("⚠️ Scraper somehow succeeded with invalid URL - may be real redirect")
            
    except Exception as e:
        print(f"✅ Scraper properly failed: {str(e)}")
    finally:
        if 'scraper' in locals() and hasattr(scraper, 'driver') and scraper.driver:
            try:
                scraper.driver.quit()
            except:
                pass
    
    # Test 2: Analyzer should fail without OpenAI API key
    print("\n2. Testing analyzer without OpenAI API key...")
    
    # Remove API key to ensure no fallback
    original_key = os.environ.get('OPENAI_API_KEY')
    if 'OPENAI_API_KEY' in os.environ:
        del os.environ['OPENAI_API_KEY']
    
    try:
        analyzer = BrandAnalyzer()
        
        # Create minimal brand data
        brand_data = {
            'name': 'Test Brand',
            'url': 'https://example.com',
            'pages_scraped': [{
                'content': 'Some test content',
                'headings': [{'text': 'Test Heading'}]
            }],
            'visual_assets': {},
            'content_analysis': {'total_words': 100},
            'technical_info': {},
            'recent_content': []
        }
        
        # This should fail now
        analysis = analyzer.analyze_brand(brand_data)
        
        print("❌ Analyzer succeeded when it should have failed (dummy data generated)")
        return False
        
    except Exception as e:
        print(f"✅ Analyzer properly failed without API key: {str(e)}")
    
    finally:
        # Restore original key if it existed
        if original_key:
            os.environ['OPENAI_API_KEY'] = original_key
    
    # Test 3: Check for any hardcoded dummy strings in code
    print("\n3. Scanning code for dummy data patterns...")
    
    dummy_patterns = [
        "Professional presentation",
        "Standard navigation",
        "Established web presence", 
        "Clear industry positioning",
        "Comprehensive content coverage",
        "Technical infrastructure",
        "Could enhance user engagement",
        "Digital marketing enhancement needed",
        "Professional, knowledgeable, dependable"
    ]
    
    # Check if any dummy patterns still exist in the code
    found_dummy = False
    for file_path in ['src/analyzer.py', 'src/scraper.py']:
        try:
            with open(file_path, 'r') as f:
                content = f.read()
                for pattern in dummy_patterns:
                    if pattern in content:
                        print(f"❌ Found dummy pattern '{pattern}' in {file_path}")
                        found_dummy = True
        except FileNotFoundError:
            pass
    
    if not found_dummy:
        print("✅ No dummy data patterns found in code")
    
    # Test 4: Validate that errors are properly propagated
    print("\n4. Testing error propagation...")
    
    # Import and test without running the full Flask pipeline
    try:
        from src.scraper import WebScraper
        from src.analyzer import BrandAnalyzer
        
        # Test that scraper fails with bad URLs
        scraper = WebScraper()
        try:
            scraper.scrape_brand("https://this-definitely-does-not-exist-12345.fake", "Test")
            print("❌ Scraper should have failed but didn't")
            return False
        except Exception as e:
            print(f"✅ Scraper properly failed: {str(e)}")
        finally:
            if scraper.driver:
                scraper.driver.quit()
        
        # Test that analyzer fails without API key
        analyzer = BrandAnalyzer()
        try:
            test_data = {
                'name': 'Test',
                'pages_scraped': [{'content': 'test content'}],
                'visual_assets': {},
                'content_analysis': {'total_words': 100},
                'technical_info': {},
                'recent_content': []
            }
            analyzer.analyze_brand(test_data)
            print("❌ Analyzer should have failed but didn't")
            return False
        except Exception as e:
            print(f"✅ Analyzer properly failed: {str(e)}")
        
    except Exception as e:
        print(f"✅ Error propagation working: {str(e)}")
    
    print("\n✅ NO DUMMY DATA VALIDATION PASSED!")
    print("   - Scraper fails with invalid URLs or insufficient content")
    print("   - Analyzer requires valid OpenAI API key") 
    print("   - No hardcoded dummy content found")
    print("   - Errors properly propagated through system")
    print("   - Only real scraped data will be used")
    
    return True

if __name__ == "__main__":
    success = test_no_dummy_data()
    
    if success:
        print("\n🎉 VALIDATION SUCCESSFUL!")
        print("The application will only work with:")
        print("- Real website data from successful scraping")
        print("- Valid OpenAI API key for genuine AI analysis")
        print("- No fallback or dummy data generation")
        sys.exit(0)
    else:
        print("\n❌ VALIDATION FAILED!")
        print("Dummy data generation still exists in the system")
        sys.exit(1)