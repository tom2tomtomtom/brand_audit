#!/usr/bin/env python3
"""
Quick Medical Competitive Analysis
Generate the medical competitive grid you need
"""

from competitive_grid_generator import CompetitiveGridGenerator

def main():
    print("🏥 Starting Medical Competitive Analysis...")
    
    # Medical/Healthcare information platforms
    medical_urls = [
        "https://www.wolterskluwer.com",
        "https://www.elsevier.com", 
        "https://www.clinicalkey.com",
        "https://www.openevidence.com"
    ]
    
    generator = CompetitiveGridGenerator()
    
    # Generate comprehensive medical competitive grid
    output_file = generator.generate_competitive_landscape_report(
        urls=medical_urls,
        page_title="Medical Information & AI Platform Competitive Landscape",
        output_filename="medical_competitive_grid_final.html"
    )
    
    if output_file:
        print(f"\n🎉 SUCCESS! Medical competitive grid is ready!")
        print(f"📁 File: {output_file}")
        print(f"🌐 Open this HTML file in your browser to view the professional grid")
    else:
        print("❌ Failed to generate grid")

if __name__ == "__main__":
    main()