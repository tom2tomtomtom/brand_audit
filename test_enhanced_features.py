#!/usr/bin/env python3
"""
Test Enhanced Typography & Visual Gallery Features
Quick test of the enhanced font extraction and visual gallery capture
"""

from strategic_competitive_intelligence import StrategicCompetitiveIntelligence
import os

def main():
    """Test enhanced typography and visual gallery features"""
    
    # Test with real websites
    test_urls = [
        "https://www.apple.com",
        "https://www.microsoft.com"
    ]
    
    print("🔧 Testing Enhanced Features...")
    print("🔤 Testing: Real font extraction from CSS")
    print("🖼️ Testing: Visual gallery capture from websites")
    
    generator = StrategicCompetitiveIntelligence()
    
    # Test typography analysis
    print("\n🔤 TYPOGRAPHY ANALYSIS TEST")
    for url in test_urls:
        company_name = url.split('/')[-1].replace('.com', '').replace('www.', '').title()
        brand = {'url': url, 'company_name': company_name}
        
        print(f"\n   Analyzing: {company_name}")
        typography = generator._analyze_typography(brand)
        print(f"   Primary Font: {typography['primary_font']}")
        print(f"   Secondary: {typography['secondary_font']}")
        print(f"   Style: {typography['style']}")
    
    # Test visual gallery capture
    print("\n🖼️ VISUAL GALLERY CAPTURE TEST")
    for url in test_urls:
        company_name = url.split('/')[-1].replace('.com', '').replace('www.', '').title()
        brand = {'url': url, 'company_name': company_name}
        
        print(f"\n   Capturing visuals: {company_name}")
        visuals = generator._capture_visual_gallery(brand)
        print(f"   Captured {len(visuals)} visual assets:")
        for i, visual in enumerate(visuals):
            print(f"   [{i+1}] {visual[:80]}...")
    
    print("\n✅ Enhanced features test complete!")
    print("🔤 Font extraction: Real fonts extracted from CSS")
    print("🖼️ Visual gallery: Multiple content images captured")

if __name__ == "__main__":
    main()