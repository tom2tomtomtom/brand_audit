#!/usr/bin/env python3
"""
Test Premium 6-Row Grid Generation
Quick test of the premium design without full AI analysis
"""

from strategic_competitive_intelligence import StrategicCompetitiveIntelligence
import json
import os

def main():
    """Generate test report with premium 6-row grid"""
    
    # Use simple test URLs
    test_urls = [
        "https://www.apple.com",
        "https://www.microsoft.com", 
        "https://www.google.com"
    ]
    
    print("🔧 Starting Premium Grid Test...")
    
    generator = StrategicCompetitiveIntelligence()
    
    # Mock basic brand data for testing
    generator.brand_profiles = [
        {
            "company_name": "Apple",
            "url": "https://www.apple.com",
            "logos": ["data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="],
            "color_palette": ["#007AFF", "#FF3B30", "#FF9500", "#FFCC02", "#34C759", "#5AC8FA"],
            "screenshot": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==",
            "ai_brand_story": "Innovation-driven technology leader",
            "ai_personality_traits": ["Innovative", "Premium", "User-Centric", "Design-Forward"],
            "ai_typography_analysis": {"primary_font": "San Francisco", "secondary_font": "Helvetica Neue", "font_personality": "Modern, Clean"},
            "enhanced_positioning": {"competitive_strategy": {"positioning_approach": "Premium Leader"}},
            "enhanced_brand_health": {"overall_score": 95, "competitive_threat_level": "Low"}
        },
        {
            "company_name": "Microsoft", 
            "url": "https://www.microsoft.com",
            "logos": ["data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="],
            "color_palette": ["#0078D4", "#106EBE", "#005A9E", "#004578", "#003064", "#002050"],
            "screenshot": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==",
            "ai_brand_story": "Enterprise-focused productivity pioneer",
            "ai_personality_traits": ["Professional", "Reliable", "Enterprise-Grade", "Collaborative"],
            "ai_typography_analysis": {"primary_font": "Segoe UI", "secondary_font": "Calibri", "font_personality": "Professional, Reliable"},
            "enhanced_positioning": {"competitive_strategy": {"positioning_approach": "Enterprise Champion"}},
            "enhanced_brand_health": {"overall_score": 88, "competitive_threat_level": "Medium"}
        },
        {
            "company_name": "Google",
            "url": "https://www.google.com", 
            "logos": ["data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="],
            "color_palette": ["#4285F4", "#34A853", "#FBBC05", "#EA4335", "#9AA0A6", "#5F6368"],
            "screenshot": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==",
            "ai_brand_story": "Information accessibility and AI innovation leader",
            "ai_personality_traits": ["Data-Driven", "Accessible", "AI-Forward", "Global"],
            "ai_typography_analysis": {"primary_font": "Product Sans", "secondary_font": "Roboto", "font_personality": "Friendly, Accessible"},
            "enhanced_positioning": {"competitive_strategy": {"positioning_approach": "Innovation Leader"}},
            "enhanced_brand_health": {"overall_score": 92, "competitive_threat_level": "Low"}
        }
    ]
    
    print("✅ Mock data created")
    
    # Generate the premium grid HTML directly
    html_content = generator._generate_visual_brand_grid()
    
    # Get the premium CSS from the main generator
    premium_css = generator._get_strategic_report_css()
    
    # Create a complete HTML page for testing
    full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Premium 6-Row Grid Test</title>
    <style>
        {premium_css}
        
        /* Additional test page styling */
        body {{
            padding: 40px;
            background: #f5f7fa;
        }}
        h1 {{
            text-align: center;
            color: #2c3e50;
            margin-bottom: 40px;
            font-size: 2.5em;
            font-weight: 700;
        }}
        .test-info {{
            background: white;
            padding: 20px;
            border-radius: 12px;
            margin-bottom: 30px;
            box-shadow: 0 4px 16px rgba(0,0,0,0.1);
        }}
    </style>
</head>
<body>
    <h1>Premium 6-Row Competitive Grid Test</h1>
    <div class="test-info">
        <h3>🎨 Premium Features Demonstrated:</h3>
        <ul>
            <li>✅ 6-row structure: Brand Identity, Brand Story, Personality, Colors, Typography, Touchpoints</li>
            <li>✅ Larger color swatches (40px × 40px) with premium styling</li>
            <li>✅ Gradient backgrounds and sophisticated shadows</li>
            <li>✅ Enhanced typography with real font samples</li>
            <li>✅ Hover effects and smooth transitions</li>
        </ul>
    </div>
    {html_content}
</body>
</html>"""
    
    # Save test file
    output_file = "premium_grid_test.html"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(full_html)
    
    print(f"✅ Premium grid test generated: {os.path.abspath(output_file)}")
    print("🎨 Features tested:")
    print("   - 6-row structure (Logo, Brand Story, Personality, Color, Typography, Photography)")
    print("   - Larger color swatches (40px x 40px)")
    print("   - Premium gradient styling")
    print("   - Enhanced visual effects and shadows")

if __name__ == "__main__":
    main()