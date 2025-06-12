#!/usr/bin/env python3
"""
Simple test of the competitive grid generator with mock data
"""

from competitive_grid_generator import CompetitiveGridGenerator
from datetime import datetime

def create_mock_brand_profiles():
    """Create mock brand profiles for testing the grid layout"""
    return [
        {
            "url": "https://www.tdameritrade.com",
            "company_name": "TD Ameritrade",
            "brand_positioning": "Empowering clients by helping them take control of their financial lives through innovative technology and comprehensive investment solutions designed for today's modern investor.",
            "personality_descriptors": ["Confident", "Wise", "Empowering", "Innovative"],
            "color_palette": ["#00a651", "#003d2b", "#ffffff", "#f5f5f5", "#666666", "#333333"],
            "visual_style": "Modern technology-focused design"
        },
        {
            "url": "https://www.edwardjones.com",
            "company_name": "Edward Jones",
            "brand_positioning": "Building relationships with individuals they help achieve their financial goals through personal attention and deep thinking about what's important to their clients.",
            "personality_descriptors": ["Personal", "Engaging", "Deep", "Thoughtful"],
            "color_palette": ["#004890", "#00a0dc", "#ffffff", "#f8f8f8", "#555555", "#000000"],
            "visual_style": "Personal relationship-focused"
        },
        {
            "url": "https://www.schwab.com",
            "company_name": "Charles Schwab",
            "brand_positioning": "Championing every client's goals with passion and integrity by providing modern, thoughtful solutions for financial success.",
            "personality_descriptors": ["Modern", "Dynamic", "Persuasive", "Provoking"],
            "color_palette": ["#0033a0", "#ffffff", "#f5f5f5", "#333333", "#e6e6e6", "#999999"],
            "visual_style": "Clean modern interface"
        },
        {
            "url": "https://www.johnhancock.com",
            "company_name": "John Hancock",
            "brand_positioning": "Offering clients a solid foundation for the financial future through responsible wealth management and insurance solutions.",
            "personality_descriptors": ["Traditional", "Wise", "Responsible", "Cautious"],
            "color_palette": ["#003087", "#f39800", "#ffffff", "#f8f8f8", "#444444", "#888888"],
            "visual_style": "Traditional professional design"
        },
        {
            "url": "https://www.prudential.com",
            "company_name": "Prudential",
            "brand_positioning": "Helping companies and people grow and protect their wealth for 140 years through expertise, innovation, and financial strength.",
            "personality_descriptors": ["Caring", "Realistic", "Reliable", "Protective"],
            "color_palette": ["#0f4c81", "#f79100", "#ffffff", "#f7f7f7", "#666666", "#333333"],
            "visual_style": "Heritage-focused branding"
        }
    ]

def main():
    """Test the grid generator with mock data"""
    print("Testing Competitive Grid Generator with mock data...")
    
    generator = CompetitiveGridGenerator()
    mock_profiles = create_mock_brand_profiles()
    
    # Generate HTML with mock data
    html_content = generator.generate_grid_html(
        brand_profiles=mock_profiles,
        page_title="There is a huge opportunity in the category"
    )
    
    # Save test file
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_filename = f"test_competitive_grid_{timestamp}.html"
    
    try:
        with open(output_filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ Test grid generated successfully!")
        print(f"📁 File: {output_filename}")
        print(f"🌐 Open this HTML file in your browser to see the 5-row competitive landscape grid")
        print(f"📊 Grid includes: Logos, Positioning, Personality, Colors, Visual Assets")
        
    except Exception as e:
        print(f"❌ Error saving test file: {e}")

if __name__ == "__main__":
    main()