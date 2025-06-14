#!/usr/bin/env python3
"""
Brand Audit V2 - Comprehensive Demo
Shows all features of the improved real-data-only system
"""

import os
import json
from datetime import datetime
from competitive_grid_generator_v2 import CompetitiveGridGeneratorV2
from enhanced_brand_profiler_v2 import EnhancedBrandProfilerV2

def print_header(text):
    """Print formatted header"""
    print(f"\n{'='*60}")
    print(f"{text.center(60)}")
    print(f"{'='*60}\n")

def demo_single_brand_analysis():
    """Demo: Analyze a single brand with detailed output"""
    print_header("DEMO 1: Single Brand Analysis")
    
    profiler = EnhancedBrandProfilerV2()
    
    # Analyze a single brand
    url = "https://www.stripe.com"
    print(f"Analyzing: {url}")
    print("-" * 40)
    
    profile = profiler.analyze_brand(url)
    
    if profile['status'] == 'success':
        brand_data = profile['brand_data']
        
        print(f"✅ EXTRACTION SUCCESSFUL")
        print(f"\nExtraction Method: {profile['extraction_method']}")
        print(f"Quality Score: {profile['extraction_quality']:.2f}")
        
        print(f"\n📊 BRAND DATA:")
        print(f"Company Name: {brand_data.get('company_name', 'Not found')}")
        print(f"Confidence: {brand_data.get('confidence_scores', {}).get('company_name', 0):.0%}")
        
        if brand_data.get('brand_positioning'):
            print(f"\nBrand Positioning:")
            print(f"  {brand_data['brand_positioning']}")
            print(f"  Confidence: {brand_data.get('confidence_scores', {}).get('positioning', 0):.0%}")
        
        if brand_data.get('key_messages'):
            print(f"\nKey Messages:")
            for msg in brand_data['key_messages'][:3]:
                print(f"  • {msg}")
        
        if brand_data.get('target_audience'):
            print(f"\nTarget Audience: {brand_data['target_audience']}")
        
        if brand_data.get('brand_personality'):
            print(f"\nBrand Personality: {', '.join(brand_data['brand_personality'])}")
        
        # Visual data
        visual_data = profile.get('visual_data', {})
        if visual_data:
            print(f"\n🎨 VISUAL ELEMENTS:")
            
            if visual_data.get('logo_extraction'):
                print(f"Logos Found: {len(visual_data['logo_extraction'])}")
                for logo in visual_data['logo_extraction'][:2]:
                    print(f"  • {logo}")
            
            colors = []
            for method in ['css_extraction', 'screenshot_analysis', 'svg_parsing']:
                if visual_data.get(method):
                    colors.extend(visual_data[method])
            
            if colors:
                unique_colors = list(set(colors))[:6]
                print(f"\nColor Palette: {', '.join(unique_colors)}")
        
    else:
        print(f"❌ EXTRACTION FAILED")
        print(f"Error: {profile['error']}")
    
    return profile

def demo_multi_brand_comparison():
    """Demo: Compare multiple brands"""
    print_header("DEMO 2: Multi-Brand Comparison")
    
    generator = CompetitiveGridGeneratorV2()
    
    # Different industry examples
    test_sets = {
        "Payment Platforms": [
            "https://www.stripe.com",
            "https://www.square.com",
            "https://www.paypal.com"
        ],
        "E-commerce Platforms": [
            "https://www.shopify.com",
            "https://www.bigcommerce.com",
            "https://www.woocommerce.com"
        ],
        "Cloud Providers": [
            "https://aws.amazon.com",
            "https://cloud.google.com",
            "https://azure.microsoft.com"
        ]
    }
    
    print("Choose a test set:")
    for i, (name, urls) in enumerate(test_sets.items(), 1):
        print(f"{i}. {name} ({len(urls)} brands)")
    
    choice = input("\nEnter choice (1-3) or press Enter for Payment Platforms: ").strip()
    
    if choice == "2":
        selected_name = "E-commerce Platforms"
        selected_urls = test_sets["E-commerce Platforms"]
    elif choice == "3":
        selected_name = "Cloud Providers"
        selected_urls = test_sets["Cloud Providers"]
    else:
        selected_name = "Payment Platforms"
        selected_urls = test_sets["Payment Platforms"]
    
    print(f"\nAnalyzing {selected_name}...")
    
    # Generate report
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"{selected_name.lower().replace(' ', '_')}_analysis_{timestamp}.html"
    
    result = generator.generate_report(
        urls=selected_urls,
        report_title=f"{selected_name} Competitive Analysis",
        output_filename=filename
    )
    
    if result:
        print(f"\n📊 ANALYSIS COMPLETE:")
        print(f"✅ Successful: {result['successful_count']}")
        print(f"❌ Failed: {result['failed_count']}")
        print(f"📄 Report saved: {result['filename']}")
        
        # Show extracted brands
        if result['brands']:
            print(f"\nExtracted Brands:")
            for brand in result['brands']:
                print(f"  • {brand['company_name']} - Quality: {brand['extraction_quality']:.2f}")

def demo_challenging_sites():
    """Demo: Handle challenging websites"""
    print_header("DEMO 3: Challenging Websites")
    
    challenging_urls = [
        ("JavaScript-heavy SPA", "https://www.notion.so"),
        ("Minimal content", "https://www.example.com"),
        ("Complex enterprise", "https://www.salesforce.com"),
        ("Media-rich", "https://www.spotify.com")
    ]
    
    profiler = EnhancedBrandProfilerV2()
    results = []
    
    for site_type, url in challenging_urls:
        print(f"\n{site_type}: {url}")
        print("-" * 40)
        
        profile = profiler.analyze_brand(url)
        results.append({
            'type': site_type,
            'url': url,
            'status': profile['status'],
            'method': profile.get('extraction_method', 'N/A'),
            'quality': profile.get('extraction_quality', 0),
            'error': profile.get('error', '')
        })
        
        if profile['status'] == 'success':
            print(f"✅ Success with {profile['extraction_method']}")
            print(f"   Company: {profile['brand_data'].get('company_name', 'Unknown')}")
            print(f"   Quality: {profile['extraction_quality']:.2f}")
        else:
            print(f"❌ Failed: {profile['error']}")
    
    # Summary
    print(f"\n📊 CHALLENGING SITES SUMMARY:")
    successful = [r for r in results if r['status'] == 'success']
    print(f"Success Rate: {len(successful)}/{len(results)} ({len(successful)/len(results)*100:.0f}%)")
    
    if successful:
        avg_quality = sum(r['quality'] for r in successful) / len(successful)
        print(f"Average Quality: {avg_quality:.2f}")
        
        # Methods used
        methods = {}
        for r in successful:
            methods[r['method']] = methods.get(r['method'], 0) + 1
        
        print(f"\nExtraction Methods Used:")
        for method, count in methods.items():
            print(f"  • {method}: {count}")

def demo_visual_extraction():
    """Demo: Visual element extraction capabilities"""
    print_header("DEMO 4: Visual Element Extraction")
    
    # Sites with strong visual branding
    visual_brands = [
        "https://www.airbnb.com",
        "https://www.coca-cola.com",
        "https://www.nike.com"
    ]
    
    profiler = EnhancedBrandProfilerV2()
    
    for url in visual_brands:
        print(f"\nAnalyzing visual elements for: {url}")
        print("-" * 40)
        
        profile = profiler.analyze_brand(url)
        
        if profile['status'] == 'success' and profile.get('visual_data'):
            visual_data = profile['visual_data']
            
            print(f"✅ Visual extraction successful")
            
            # Logos
            if visual_data.get('logo_extraction'):
                print(f"\n🖼️  Logos found: {len(visual_data['logo_extraction'])}")
                for i, logo in enumerate(visual_data['logo_extraction'][:2], 1):
                    print(f"   {i}. {logo[:80]}...")
            
            # Colors from different methods
            print(f"\n🎨 Color extraction methods:")
            for method in ['css_extraction', 'screenshot_analysis', 'svg_parsing']:
                if visual_data.get(method):
                    colors = visual_data[method]
                    print(f"   • {method}: {len(colors)} colors")
                    print(f"     {', '.join(colors[:3])}")
            
            # Brand personality from visual style
            brand_data = profile['brand_data']
            if brand_data.get('brand_personality'):
                print(f"\n✨ Visual personality: {', '.join(brand_data['brand_personality'][:3])}")
        else:
            print(f"❌ Visual extraction failed")

def demo_export_formats():
    """Demo: Different export formats"""
    print_header("DEMO 5: Export Formats")
    
    profiler = EnhancedBrandProfilerV2()
    url = "https://www.github.com"
    
    print(f"Analyzing {url} for export demo...")
    profile = profiler.analyze_brand(url)
    
    if profile['status'] == 'success':
        # JSON export
        json_file = "brand_profile_export.json"
        with open(json_file, 'w') as f:
            json.dump(profile, f, indent=2)
        print(f"✅ JSON export: {json_file}")
        
        # CSV export (simplified)
        import csv
        csv_file = "brand_profile_export.csv"
        
        brand_data = profile['brand_data']
        with open(csv_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Field', 'Value', 'Confidence'])
            writer.writerow(['Company Name', brand_data.get('company_name', ''), 
                           brand_data.get('confidence_scores', {}).get('company_name', 0)])
            writer.writerow(['Positioning', brand_data.get('brand_positioning', ''), 
                           brand_data.get('confidence_scores', {}).get('positioning', 0)])
            writer.writerow(['Quality Score', profile['extraction_quality'], 1.0])
        
        print(f"✅ CSV export: {csv_file}")
        
        # Summary report
        summary = {
            'analysis_date': datetime.now().isoformat(),
            'url': url,
            'success': True,
            'extraction_method': profile['extraction_method'],
            'quality_score': profile['extraction_quality'],
            'company_name': brand_data.get('company_name'),
            'has_positioning': bool(brand_data.get('brand_positioning')),
            'has_visual_data': bool(profile.get('visual_data')),
            'confidence_avg': sum(brand_data.get('confidence_scores', {}).values()) / len(brand_data.get('confidence_scores', {})) if brand_data.get('confidence_scores') else 0
        }
        
        summary_file = "brand_analysis_summary.json"
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)
        print(f"✅ Summary export: {summary_file}")

def interactive_demo():
    """Interactive demo menu"""
    print_header("BRAND AUDIT V2 - COMPREHENSIVE DEMO")
    
    print("This demo showcases the improved V2 system:")
    print("• Real data only - no fallbacks")
    print("• Industry agnostic analysis")
    print("• Multi-strategy extraction")
    print("• Quality scoring and validation")
    
    while True:
        print("\n" + "="*60)
        print("DEMO MENU:")
        print("1. Single Brand Analysis (Detailed)")
        print("2. Multi-Brand Comparison Grid")
        print("3. Challenging Websites Test")
        print("4. Visual Element Extraction")
        print("5. Export Formats Demo")
        print("6. Run All Demos")
        print("0. Exit")
        
        choice = input("\nSelect demo (0-6): ").strip()
        
        if choice == "0":
            print("\nExiting demo. Thank you!")
            break
        elif choice == "1":
            demo_single_brand_analysis()
        elif choice == "2":
            demo_multi_brand_comparison()
        elif choice == "3":
            demo_challenging_sites()
        elif choice == "4":
            demo_visual_extraction()
        elif choice == "5":
            demo_export_formats()
        elif choice == "6":
            print("\nRunning all demos...")
            demo_single_brand_analysis()
            demo_challenging_sites()
            demo_visual_extraction()
            demo_export_formats()
            print("\n✅ All demos complete!")
        else:
            print("Invalid choice. Please try again.")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    # Check for API key
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ ERROR: OPENAI_API_KEY environment variable not set")
        print("Please set it: export OPENAI_API_KEY='your-key-here'")
        exit(1)
    
    # Run interactive demo
    interactive_demo()
