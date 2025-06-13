#!/usr/bin/env python3
"""
Test Enhanced Screenshot Capture with Privacy Dialog Handling
"""

from strategic_competitive_intelligence import StrategicCompetitiveIntelligence
import os

def main():
    """Test screenshot capture with privacy dialog handling"""
    
    # Test with websites that commonly have privacy dialogs
    test_urls = [
        "https://www.elsevier.com",  # Often has cookie banners
        "https://www.wolterskluwer.com",  # May have consent dialogs
        "https://www.openevidence.com"  # Healthcare site with potential privacy notices
    ]
    
    print("🔧 Testing Enhanced Screenshot Capture with Privacy Dialog Handling...")
    
    generator = StrategicCompetitiveIntelligence()
    
    for url in test_urls:
        company_name = url.split('/')[-1].replace('.com', '').replace('www.', '').title()
        print(f"\n📸 Testing screenshot capture: {company_name}")
        print(f"   URL: {url}")
        
        screenshot = generator._capture_screenshot_proper(url)
        
        if screenshot:
            print(f"   ✅ Screenshot captured successfully")
            print(f"   📊 Data size: {len(screenshot)} characters")
            
            # Save a test HTML file to verify the screenshot
            test_html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Screenshot Test - {company_name}</title>
    <style>
        body {{ font-family: Arial, sans-serif; padding: 40px; text-align: center; }}
        img {{ max-width: 100%; border: 2px solid #ddd; border-radius: 8px; }}
        h1 {{ color: #333; }}
    </style>
</head>
<body>
    <h1>Screenshot Test: {company_name}</h1>
    <p>URL: {url}</p>
    <p>Privacy Dialog Handling: Enhanced</p>
    <img src="{screenshot}" alt="{company_name} Screenshot">
</body>
</html>"""
            
            test_file = f"screenshot_test_{company_name.lower()}.html"
            with open(test_file, 'w', encoding='utf-8') as f:
                f.write(test_html)
            
            print(f"   💾 Test file saved: {test_file}")
        else:
            print(f"   ❌ Screenshot capture failed")
    
    print("\n✅ Screenshot privacy dialog handling test complete!")
    print("🔍 Check the generated test HTML files to verify screenshot quality")

if __name__ == "__main__":
    main()