#!/usr/bin/env python3
"""
Brand Audit V2 - Quick Start
Get started with the real-data-only brand analysis system
"""

import os
import sys
from competitive_grid_generator_v2 import CompetitiveGridGeneratorV2
from enhanced_brand_profiler_v2 import EnhancedBrandProfilerV2
from datetime import datetime

def quick_analyze():
    """Quick analysis of provided URLs"""
    
    print("\n🚀 BRAND AUDIT V2 - QUICK START")
    print("="*50)
    print("Real data only • No fallbacks • Industry agnostic")
    print("="*50)
    
    # Get URLs from user
    print("\nEnter URLs to analyze (one per line, empty line to finish):")
    urls = []
    while True:
        url = input("> ").strip()
        if not url:
            break
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        urls.append(url)
    
    if not urls:
        # Default demo URLs
        print("\nNo URLs provided. Using demo URLs:")
        urls = [
            "https://www.stripe.com",
            "https://www.shopify.com",
            "https://www.square.com"
        ]
        for url in urls:
            print(f"  • {url}")
    
    # Choose analysis type
    print(f"\nAnalysis options for {len(urls)} URLs:")
    print("1. Quick Analysis (console output)")
    print("2. Full Grid Report (HTML)")
    print("3. Individual Profiles (detailed)")
    
    choice = input("\nSelect option (1-3, default=2): ").strip() or "2"
    
    if choice == "1":
        quick_analysis(urls)
    elif choice == "2":
        generate_grid_report(urls)
    else:
        individual_analysis(urls)

def quick_analysis(urls):
    """Quick console analysis"""
    print(f"\n🔍 Quick Analysis of {len(urls)} brands...")
    print("-"*50)
    
    profiler = EnhancedBrandProfilerV2()
    results = []
    
    for url in urls:
        print(f"\nAnalyzing: {url}")
        profile = profiler.analyze_brand(url)
        
        if profile['status'] == 'success':
            brand = profile['brand_data']
            print(f"✅ {brand.get('company_name', 'Unknown')}")
            print(f"   Quality: {profile['extraction_quality']:.0%}")
            if brand.get('brand_positioning'):
                print(f"   Positioning: {brand['brand_positioning'][:60]}...")
            results.append(('success', brand.get('company_name', 'Unknown'), profile['extraction_quality']))
        else:
            print(f"❌ Failed: {profile['error']}")
            results.append(('failed', url, 0))
    
    # Summary
    print(f"\n{'='*50}")
    print("SUMMARY:")
    successful = [r for r in results if r[0] == 'success']
    print(f"✅ Successful: {len(successful)}/{len(urls)}")
    if successful:
        avg_quality = sum(r[2] for r in successful) / len(successful)
        print(f"📊 Average Quality: {avg_quality:.0%}")

def generate_grid_report(urls):
    """Generate full HTML grid report"""
    print(f"\n📊 Generating Competitive Grid Report...")
    
    # Ask for report title
    title = input("Report title (or press Enter for default): ").strip()
    if not title:
        title = "Competitive Brand Analysis"
    
    generator = CompetitiveGridGeneratorV2()
    
    # Generate with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"brand_analysis_{timestamp}.html"
    
    print(f"\nAnalyzing {len(urls)} brands...")
    print("This may take 10-20 seconds per brand...\n")
    
    result = generator.generate_report(
        urls=urls,
        report_title=title,
        output_filename=filename
    )
    
    if result:
        print(f"\n✅ REPORT GENERATED SUCCESSFULLY!")
        print(f"📄 File: {filename}")
        print(f"📊 Analyzed: {result['successful_count']} brands")
        if result['failed_count'] > 0:
            print(f"❌ Failed: {result['failed_count']} brands")
        
        # Open in browser
        if sys.platform == 'darwin':  # macOS
            os.system(f'open {filename}')
        elif sys.platform == 'win32':  # Windows
            os.system(f'start {filename}')
        else:  # Linux
            os.system(f'xdg-open {filename}')
            
        print("\n✨ Report opened in browser!")

def individual_analysis(urls):
    """Detailed individual analysis"""
    print(f"\n🔬 Detailed Individual Analysis...")
    
    profiler = EnhancedBrandProfilerV2()
    all_profiles = []
    
    for i, url in enumerate(urls, 1):
        print(f"\n{'='*50}")
        print(f"[{i}/{len(urls)}] {url}")
        print(f"{'='*50}")
        
        profile = profiler.analyze_brand(url)
        all_profiles.append(profile)
        
        if profile['status'] == 'success':
            brand = profile['brand_data']
            visual = profile.get('visual_data', {})
            
            print(f"\n✅ EXTRACTION SUCCESSFUL")
            print(f"Method: {profile['extraction_method']}")
            print(f"Quality: {profile['extraction_quality']:.0%}")
            
            print(f"\n📋 BRAND INFORMATION:")
            print(f"Company: {brand.get('company_name', 'Not found')}")
            print(f"Confidence: {brand.get('confidence_scores', {}).get('company_name', 0):.0%}")
            
            if brand.get('brand_positioning'):
                print(f"\nPositioning:")
                print(f"  {brand['brand_positioning']}")
                
            if brand.get('key_messages'):
                print(f"\nKey Messages:")
                for msg in brand['key_messages'][:3]:
                    print(f"  • {msg}")
                    
            if brand.get('target_audience'):
                print(f"\nTarget Audience: {brand['target_audience']}")
                
            if brand.get('brand_personality'):
                print(f"\nPersonality: {', '.join(brand['brand_personality'])}")
            
            # Visual elements
            if visual:
                print(f"\n🎨 VISUAL ELEMENTS:")
                
                # Logos
                logo_count = len(visual.get('logo_extraction', []))
                if logo_count > 0:
                    print(f"Logos found: {logo_count}")
                    
                # Colors
                all_colors = []
                for method in ['css_extraction', 'screenshot_analysis', 'svg_parsing']:
                    if visual.get(method):
                        all_colors.extend(visual[method])
                
                if all_colors:
                    unique_colors = list(set(all_colors))[:6]
                    print(f"Colors: {', '.join(unique_colors)}")
        else:
            print(f"\n❌ EXTRACTION FAILED")
            print(f"Error: {profile['error']}")
    
    # Save detailed results
    save = input("\n💾 Save detailed results to JSON? (y/N): ").strip().lower()
    if save == 'y':
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"brand_profiles_{timestamp}.json"
        
        import json
        with open(filename, 'w') as f:
            json.dump(all_profiles, f, indent=2)
        
        print(f"✅ Saved to: {filename}")

def check_requirements():
    """Check if all requirements are met"""
    
    # Check API key
    if not os.getenv("OPENAI_API_KEY"):
        print("\n❌ ERROR: OpenAI API key not found!")
        print("\nTo fix this:")
        print("1. Get your API key from: https://platform.openai.com/api-keys")
        print("2. Set it in your environment:")
        print("   export OPENAI_API_KEY='your-key-here'")
        print("\nOr create a .env file with:")
        print("   OPENAI_API_KEY=your-key-here")
        return False
    
    # Check imports
    try:
        import requests
        import bs4
        import openai
        import pandas
        import sklearn
        import selenium
        print("✅ All requirements installed")
        return True
    except ImportError as e:
        print(f"\n❌ Missing requirement: {e}")
        print("\nInstall requirements with:")
        print("   pip install -r requirements_v2.txt")
        return False

if __name__ == "__main__":
    print("🚀 BRAND AUDIT V2 - QUICK START")
    print("="*50)
    
    if not check_requirements():
        exit(1)
    
    try:
        quick_analyze()
    except KeyboardInterrupt:
        print("\n\n👋 Analysis cancelled. Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nFor help, check the documentation or run:")
        print("   python demo_v2_comprehensive.py")
