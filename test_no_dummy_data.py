#!/usr/bin/env python3
"""
Comprehensive test to verify no dummy data generation in brand audit tool
"""

import os
import sys
import tempfile
import shutil
sys.path.append('src')

from dotenv import load_dotenv
from scraper import WebScraper
from analyzer import BrandAnalyzer

def test_scraper_no_dummy_data():
    """Test that scraper fails properly without generating dummy data"""
    print("\n🔍 Testing Scraper - No Dummy Data Generation")
    print("-" * 50)
    
    scraper = WebScraper()
    
    # Test 1: Invalid URL should fail
    print("Test 1: Invalid URL handling")
    try:
        result = scraper.scrape_brand("https://this-is-not-a-real-website-12345.com", "NonExistent")
        print("   ❌ FAILED: Scraper should have failed but returned data")
        print(f"   Data returned: {result}")
        return False
    except Exception as e:
        print(f"   ✅ PASSED: Scraper failed properly: {str(e)[:100]}...")
    
    # Test 2: Test with a real website (should work)
    print("Test 2: Real website scraping")
    try:
        result = scraper.scrape_brand("https://example.com", "Example")
        if result and result.get('pages_scraped'):
            pages_with_content = [p for p in result['pages_scraped'] if p.get('content') and len(p.get('content', '').strip()) >= 50]
            if pages_with_content:
                print("   ✅ PASSED: Successfully scraped real content")
            else:
                print("   ❌ WARNING: No meaningful content extracted")
                return False
        else:
            print("   ❌ FAILED: No pages scraped")
            return False
    except Exception as e:
        print(f"   ❌ FAILED: Scraper failed on valid URL: {str(e)}")
        return False
    
    return True

def test_analyzer_no_dummy_data():
    """Test that analyzer fails properly without OpenAI API key"""
    print("\n🧠 Testing Analyzer - No Dummy Data Generation")
    print("-" * 50)
    
    # Backup current environment
    original_api_key = os.getenv('OPENAI_API_KEY')
    
    # Test 1: No API key should fail
    print("Test 1: No OpenAI API key")
    os.environ['OPENAI_API_KEY'] = ''
    
    try:
        analyzer = BrandAnalyzer()
        # Create minimal brand data for testing
        test_brand_data = {
            'name': 'Test Brand',
            'url': 'https://example.com',
            'pages_scraped': [{
                'url': 'https://example.com',
                'title': 'Test Page',
                'content': 'This is test content for analysis. ' * 20,  # Sufficient content
                'images': [],
                'links': []
            }],
            'visual_elements': {
                'colors': ['#000000', '#ffffff'],
                'fonts': ['Arial'],
                'logo_urls': []
            }
        }
        
        result = analyzer.analyze_brand(test_brand_data)
        print("   ❌ FAILED: Analyzer should have failed but returned analysis")
        print(f"   Analysis returned: {type(result)}")
        return False
        
    except Exception as e:
        print(f"   ✅ PASSED: Analyzer failed properly: {str(e)[:100]}...")
    
    # Test 2: Invalid API key should fail
    print("Test 2: Invalid OpenAI API key")
    os.environ['OPENAI_API_KEY'] = 'invalid_key_12345'
    
    try:
        analyzer = BrandAnalyzer()
        result = analyzer.analyze_brand(test_brand_data)
        print("   ❌ FAILED: Analyzer should have failed with invalid key")
        return False
        
    except Exception as e:
        print(f"   ✅ PASSED: Analyzer failed with invalid key: {str(e)[:100]}...")
    
    # Restore original API key
    if original_api_key:
        os.environ['OPENAI_API_KEY'] = original_api_key
    elif 'OPENAI_API_KEY' in os.environ:
        del os.environ['OPENAI_API_KEY']
    
    return True

def scan_for_dummy_data_patterns():
    """Scan source code for dummy data generation patterns"""
    print("\n🔎 Scanning Source Code for Dummy Data Patterns")
    print("-" * 50)
    
    suspicious_patterns = [
        'dummy',
        'fallback.*data',
        'fake.*data',
        'placeholder.*content',
        'generate.*random',
        'mock.*data',
        'sample.*content',
        'default.*analysis',
        'lorem ipsum'
    ]
    
    source_files = [
        'src/scraper.py',
        'src/analyzer.py',
        'src/report_generator.py',
        'app.py'
    ]
    
    findings = []
    
    for file_path in source_files:
        if not os.path.exists(file_path):
            continue
            
        with open(file_path, 'r') as f:
            content = f.read().lower()
            
        for i, line in enumerate(content.split('\\n'), 1):
            for pattern in suspicious_patterns:
                if pattern in line and not line.strip().startswith('#'):
                    # Skip comments and documentation
                    if 'no fallback' in line or 'no dummy' in line:
                        continue
                    findings.append(f"{file_path}:{i} - {line.strip()[:80]}")
    
    if findings:
        print("   ⚠️  POTENTIAL ISSUES FOUND:")
        for finding in findings[:10]:  # Show first 10
            print(f"      {finding}")
        if len(findings) > 10:
            print(f"      ... and {len(findings) - 10} more")
        return False
    else:
        print("   ✅ PASSED: No suspicious dummy data patterns found")
        return True

def test_environment_requirements():
    """Test that environment requirements are properly enforced"""
    print("\n⚙️ Testing Environment Requirements")
    print("-" * 50)
    
    load_dotenv()
    
    openai_key = os.getenv('OPENAI_API_KEY')
    
    print("OpenAI API Key Check:")
    if not openai_key or openai_key == 'your_openai_api_key_here':
        print("   ⚠️  OpenAI API key not configured")
        print("   💡 This is expected for testing - app should fail gracefully")
    else:
        print("   ✅ OpenAI API key is configured")
    
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_ANON_KEY')
    
    print("Supabase Configuration Check:")
    if (not supabase_url or supabase_url == 'https://your-project.supabase.co' or
        not supabase_key or supabase_key == 'your_supabase_anon_key_here'):
        print("   ⚠️  Supabase not configured - using fallback tracker")
        print("   💡 This is acceptable - jobs will use in-memory storage")
    else:
        print("   ✅ Supabase is configured")
    
    return True

def main():
    """Run all tests to verify no dummy data generation"""
    print("🚀 Brand Audit Tool - No Dummy Data Verification")
    print("=" * 60)
    
    tests = [
        ("Environment Requirements", test_environment_requirements),
        ("Scraper No Dummy Data", test_scraper_no_dummy_data),
        ("Analyzer No Dummy Data", test_analyzer_no_dummy_data),
        ("Code Pattern Scan", scan_for_dummy_data_patterns)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"   ❌ Test '{test_name}' crashed: {str(e)}")
            results.append((test_name, False))
    
    # Summary
    print("\\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{status:12} {test_name}")
        if result:
            passed += 1
    
    print(f"\\nOverall: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("\\n🎉 SUCCESS: No dummy data generation detected!")
        print("✅ The application properly fails when real data cannot be obtained")
        print("✅ No fallback dummy content is generated")
        print("✅ All requirements are properly enforced")
    else:
        print("\\n⚠️  ISSUES DETECTED: Some tests failed")
        print("💡 Review the failing tests and ensure no dummy data is generated")
    
    return passed == len(results)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)