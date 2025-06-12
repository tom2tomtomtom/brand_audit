#!/usr/bin/env python3
"""
Simple script to run competitive analysis with real URLs
"""

from pure_live_grid_generator import PureLiveGridGenerator
from datetime import datetime

def run_analysis(urls, title="Competitive Landscape Analysis"):
    """Run competitive analysis on provided URLs"""
    
    if not urls:
        print("❌ No URLs provided")
        return
    
    print(f"🎯 COMPETITIVE ANALYSIS - {title}")
    print("🔥 ZERO FAKE DATA - Only real extracted information")
    print("=" * 60)
    print(f"📋 Analyzing {len(urls)} URLs:")
    for i, url in enumerate(urls, 1):
        print(f"   {i}. {url}")
    print()
    
    generator = PureLiveGridGenerator()
    html_content, profiles = generator.generate_pure_grid_html(urls, title)
    
    if html_content and profiles:
        # Save file
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_filename = f"competitive_analysis_{timestamp}.html"
        
        try:
            with open(output_filename, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            print(f"\n✅ SUCCESS!")
            print(f"📁 HTML Report: {output_filename}")
            print(f"📊 Brands analyzed: {len(profiles)}")
            print(f"🌐 Open the HTML file in your browser")
            
            # Summary of what was extracted
            print(f"\n📋 Extraction Summary:")
            for profile in profiles:
                name = profile.get("company_name", "Brand")
                logo = "✓ Logo" if profile.get("logo_base64") else ""
                positioning = "✓ Positioning" if profile.get("brand_positioning") else ""
                colors = f"✓ {len(profile.get('color_palette', []))} Colors" if profile.get("color_palette") else ""
                
                extracted = [x for x in [logo, positioning, colors] if x]
                if extracted:
                    print(f"   • {name}: {' | '.join(extracted)}")
                else:
                    print(f"   • {name}: Basic info only")
            
            return output_filename
            
        except Exception as e:
            print(f"❌ Error saving file: {e}")
            return None
    else:
        print("❌ No usable data could be extracted from any URLs")
        return None

if __name__ == "__main__":
    # Example: Financial Services Analysis
    financial_urls = [
        "https://www.schwab.com",
        "https://www.fidelity.com", 
        "https://www.vanguard.com",
        "https://www.edwardjones.com",
        "https://www.ml.com",
        "https://www.morganstanley.com"
    ]
    
    # Example: Tech Companies Analysis  
    tech_urls = [
        "https://www.apple.com",
        "https://www.microsoft.com",
        "https://www.netflix.com",
        "https://www.spotify.com",
        "https://www.stripe.com",
        "https://www.figma.com"
    ]
    
    # Run analysis
    print("Choose analysis type:")
    print("1. Financial Services")
    print("2. Tech Companies") 
    print("3. Custom URLs")
    
    choice = input("\nEnter choice (1-3): ").strip()
    
    if choice == "1":
        run_analysis(financial_urls, "Financial Services Competitive Analysis")
    elif choice == "2":
        run_analysis(tech_urls, "Tech Companies Competitive Analysis")
    elif choice == "3":
        print("\nEnter URLs (one per line, press Enter twice when done):")
        custom_urls = []
        while True:
            url = input().strip()
            if not url:
                break
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            custom_urls.append(url)
        
        if custom_urls:
            title = input("Enter analysis title (optional): ").strip()
            if not title:
                title = "Custom Competitive Analysis"
            run_analysis(custom_urls, title)
        else:
            print("❌ No URLs provided")
    else:
        print("❌ Invalid choice")