#!/usr/bin/env python3
"""
Generate Premium 6-Row Competitive Intelligence Report
Full system with real data scraping and premium design
"""

from strategic_competitive_intelligence import StrategicCompetitiveIntelligence
import os

def main():
    """Generate premium competitive intelligence report with 6-row grid"""
    
    # Medical AI platform URLs for real competitive analysis
    medical_urls = [
        "https://www.wolterskluwer.com",
        "https://www.elsevier.com", 
        "https://www.openevidence.com"
    ]
    
    print("🚀 Starting Premium 6-Row Competitive Intelligence Generation...")
    print(f"📊 Analyzing {len(medical_urls)} medical AI platforms")
    print("⚡ Features: Premium 6-row grid, larger color swatches, enhanced styling")
    
    generator = StrategicCompetitiveIntelligence()
    
    try:
        output_file = generator.generate_strategic_intelligence_report(
            urls=medical_urls,
            report_title="Medical AI Platform Strategic Competitive Intelligence",
            output_filename="premium_competitive_intelligence_report.html"
        )
        
        if output_file:
            print(f"\n🎉 PREMIUM COMPETITIVE INTELLIGENCE COMPLETE!")
            print(f"📁 File: {os.path.abspath(output_file)}")
            print(f"🎨 Design: Premium 6-row grid with enhanced styling")
            print(f"🔍 Rows: Logo | Brand Story | Personality | Color | Typography | Touchpoints")
            print(f"🌈 Colors: Larger 40px swatches with real brand colors")
            print(f"✨ Features: Gradients, shadows, hover effects, premium typography")
            
    except Exception as e:
        print(f"❌ Error generating report: {e}")
        print("🔧 Try the test version: python3 test_premium_grid.py")

if __name__ == "__main__":
    main()