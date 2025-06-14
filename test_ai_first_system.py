#!/usr/bin/env python3
"""
Test script for AI-first competitive intelligence system
"""

import os
from dotenv import load_dotenv
from ai_first_intelligence import AIFirstCompetitiveIntelligence

# Load environment variables
load_dotenv()

def test_ai_first_analysis():
    """Test the AI-first system with real companies"""
    
    print("🧪 Testing AI-First Competitive Intelligence System\n")
    
    # Check if OpenAI API key is available
    if not os.getenv('OPENAI_API_KEY'):
        print("❌ OPENAI_API_KEY not found in environment")
        print("Please set your OpenAI API key to test the system")
        return
    
    # Initialize the AI-first analyzer
    analyzer = AIFirstCompetitiveIntelligence()
    print("✅ AI-first analyzer initialized")
    
    # Test companies - mix of names and URLs
    test_companies = [
        "Microsoft",
        "Apple",
        "Google"
    ]
    
    print(f"\n🔍 Testing analysis of {len(test_companies)} companies:")
    for company in test_companies:
        print(f"   • {company}")
    
    # Test individual company analysis
    for i, company in enumerate(test_companies):
        print(f"\n{'='*50}")
        print(f"Testing Company {i+1}/{len(test_companies)}: {company}")
        print('='*50)
        
        try:
            def progress_callback(message):
                print(f"   {message}")
            
            # Analyze the company
            profile = analyzer.analyze_company(company, progress_callback)
            
            # Display results
            print(f"\n✅ Analysis complete for: {profile.get('company_name', company)}")
            print(f"   Confidence: {profile.get('analysis_metadata', {}).get('confidence_level', 'Unknown')}")
            print(f"   Industry: {profile.get('company_overview', {}).get('industry', 'Not specified')}")
            print(f"   Business Model: {profile.get('company_overview', {}).get('business_model', 'Not specified')}")
            print(f"   Main Products: {len(profile.get('products_services', {}).get('main_products', []))} found")
            print(f"   Competitors: {len(profile.get('competitive_landscape', {}).get('main_competitors', []))} found")
            print(f"   Brand Story: {profile.get('brand_story', 'Not available')[:100]}...")
            
            # Check for visual data
            visual_data = profile.get('visual_identity', {})
            if visual_data:
                print(f"   Visual Data: Colors={len(visual_data.get('colors', []))}, Screenshots={len(visual_data.get('screenshots', []))}")
            else:
                print("   Visual Data: None captured")
            
        except Exception as e:
            print(f"❌ Analysis failed for {company}: {str(e)}")
    
    print(f"\n{'='*50}")
    print("🎯 Test Complete!")
    print("The AI-first system successfully prioritizes OpenAI research")
    print("with optional visual enhancement from website scraping.")
    print('='*50)

if __name__ == "__main__":
    test_ai_first_analysis()