#!/usr/bin/env python3
"""
Demo script for Brand Audit V2
Shows how to use the real-data-only approach
"""

import os
import sys
from datetime import datetime
from enhanced_brand_profiler_v2 import EnhancedBrandProfilerV2
from competitive_grid_generator_v2 import CompetitiveGridGeneratorV2
from ai_powered_competitive_intelligence_v2 import AIPoweredCompetitiveIntelligenceV2

def demo_single_brand_analysis():
    """Demo: Analyze a single brand"""
    print("\n" + "="*60)
    print("DEMO 1: Single Brand Analysis")
    print("="*60)
    
    profiler = EnhancedBrandProfilerV2()
    
    # Test with a real brand
    url = "https://www.apple.com"
    print(f"\nAnalyzing: {url}")
    
    result = profiler.analyze_brand(url)
    
    if result['status'] == 'success':
        brand_data = result['brand_data']
        print(f"\n✅ SUCCESS!")
        print(f"Company: {brand_data.get('company_name', 'Unknown')}")
        print(f"Positioning: {brand_data.get('brand_positioning', 'Not found')}")
        print(f"Extraction Quality: {result['extraction_quality']:.0%}")
        print(f"Extraction Method: {result['extraction_method']}")
        
        # Show confidence scores
        confidence = brand_data.get('confidence_scores', {})
        print(f"\nConfidence Scores:")
        print(f"  - Company Name: {confidence.get('company_name', 0):.0%}")
        print(f"  - Positioning: {confidence.get('positioning', 0):.0%}")
        print(f"  - Overall: {confidence.get('overall', 0):.0%}")
        
        # Show visual data if extracted
        visual_data = result.get('visual_data', {})
        if visual_data:
            print(f"\nVisual Elements Extracted:")
            for method, data in visual_data.items():
                if data:
                    print(f"  - {method}: ✓")
    else:
        print(f"\n❌ FAILED!")
        print(f"Error: {result['error']}")
        print("No fallback data provided - this is intentional!")

def demo_competitive_grid():
    """Demo: Generate competitive grid"""
    print("\n" + "="*60)
    print("DEMO 2: Competitive Grid Generation")
    print("="*60)
    
    # Test with multiple brands
    urls = [
        "https://www.stripe.com",
        "https://www.square.com",
        "https://www.paypal.com",
        "https://www.adyen.com",
        "https://www.doesnotexist12345.com"  # This will fail
    ]
    
    print(f"\nAnalyzing {len(urls)} brands for competitive grid...")
    
    generator = CompetitiveGridGeneratorV2()
    result = generator.generate_report(
        urls=urls,
        report_title="Payment Platforms Analysis - Real Data Only",
        output_filename="demo_competitive_grid.html"
    )
    
    if result:
        print(f"\n✅ Grid Generated!")
        print(f"Successful: {result['successful_count']} brands")
        print(f"Failed: {result['failed_count']} brands")
        print(f"Report: {result['filename']}")
        
        # Show extracted brands
        if result['brands']:
            print(f"\nExtracted Brands:")
            for brand in result['brands']:
                print(f"  - {brand['company_name']} (Quality: {brand['extraction_quality']:.0%})")
    else:
        print(f"\n❌ Grid generation failed!")

def demo_ai_intelligence():
    """Demo: AI-powered competitive intelligence"""
    print("\n" + "="*60)
    print("DEMO 3: AI-Powered Competitive Intelligence")
    print("="*60)
    
    # Test with brands that should work well
    urls = [
        "https://www.notion.so",
        "https://www.obsidian.md",
        "https://www.roamresearch.com",
        "https://www.evernote.com"
    ]
    
    print(f"\nGenerating AI intelligence for {len(urls)} brands...")
    
    intelligence = AIPoweredCompetitiveIntelligenceV2()
    result = intelligence.generate_report(
        urls=urls,
        report_title="Note-Taking Apps Competitive Intelligence",
        output_filename="demo_ai_intelligence.html"
    )
    
    if result:
        print(f"\n✅ Intelligence Report Generated!")
        print(f"Successful: {result['successful_count']} brands")
        print(f"Failed: {result['failed_count']} brands")
        print(f"Cross-brand insights: {'Yes' if result['has_insights'] else 'No'}")
        print(f"Report: {result['filename']}")
    else:
        print(f"\n❌ Intelligence generation failed!")

def demo_failure_handling():
    """Demo: How failures are handled"""
    print("\n" + "="*60)
    print("DEMO 4: Failure Handling (No Fallbacks)")
    print("="*60)
    
    profiler = EnhancedBrandProfilerV2()
    
    # Test with URLs that will likely fail
    test_cases = [
        ("https://this-website-definitely-does-not-exist-12345.com", "Non-existent site"),
        ("https://localhost:8080", "Local URL"),
        ("https://example.com/404", "404 page")
    ]
    
    for url, description in test_cases:
        print(f"\nTesting {description}: {url}")
        result = profiler.analyze_brand(url)
        
        print(f"Status: {result['status']}")
        if result['status'] == 'failed':
            print(f"Error: {result['error']}")
            print(f"Extracted Data: {result['extracted_data']} (None - no fallbacks!)")

def main():
    """Run all demos"""
    print("\n🚀 BRAND AUDIT V2 DEMO - REAL DATA ONLY")
    print("No fallbacks, no defaults, no fake data!")
    
    # Check for API key
    if not os.getenv("OPENAI_API_KEY"):
        print("\n⚠️  Warning: OPENAI_API_KEY not set!")
        print("Some features may not work without it.")
        print("Set it with: export OPENAI_API_KEY='your-key'")
    
    # Run demos
    try:
        demo_single_brand_analysis()
        input("\nPress Enter to continue to next demo...")
        
        demo_competitive_grid()
        input("\nPress Enter to continue to next demo...")
        
        demo_ai_intelligence()
        input("\nPress Enter to continue to next demo...")
        
        demo_failure_handling()
        
    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user.")
        sys.exit(0)
    
    print("\n" + "="*60)
    print("DEMO COMPLETE!")
    print("="*60)
    print("\nKey Takeaways:")
    print("1. Only real data is extracted - no placeholders")
    print("2. Failed extractions are clearly marked")
    print("3. Quality scores indicate reliability")
    print("4. Multiple extraction methods improve success rate")
    print("5. AI analysis is based on actual content only")
    
    print("\nGenerated Files:")
    for filename in ["demo_competitive_grid.html", "demo_ai_intelligence.html"]:
        if os.path.exists(filename):
            print(f"  - {filename}")

if __name__ == "__main__":
    main()
