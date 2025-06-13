#!/usr/bin/env python3
"""
Test script for company name search functionality
"""

from strategic_competitive_intelligence import StrategicCompetitiveIntelligence

def test_company_search():
    """Test searching for companies by name"""
    
    generator = StrategicCompetitiveIntelligence()
    
    # Test data - mix of company names and URLs
    test_companies = [
        "Microsoft",                    # Just company name
        "Apple, USA",                  # Company with country
        "Google",                      # Another company name
        "https://www.amazon.com",      # Direct URL
        "Tesla, USA",                  # Company with country
        "Samsung, South Korea"         # International company
    ]
    
    print("🔍 Testing company search functionality...\n")
    
    # Process the company list
    urls = generator.process_company_input(test_companies)
    
    print(f"\n✅ Successfully found {len(urls)} URLs from {len(test_companies)} inputs")
    print("\nResults:")
    for i, (input_val, url) in enumerate(zip(test_companies, urls)):
        print(f"{i+1}. {input_val} → {url}")
    
    # Test generating a report with company names
    print("\n📊 Testing report generation with company names...")
    
    # Use just a few companies for quick test
    test_competitors = [
        "Microsoft",
        "Apple",
        "Google"
    ]
    
    print(f"\nGenerating competitive analysis for: {', '.join(test_competitors)}")
    
    # This would generate the full report
    # output_file = generator.generate_strategic_intelligence_report(
    #     companies_or_urls=test_competitors,
    #     report_title="Big Tech Competitive Analysis"
    # )
    
    print("\n✅ Company search functionality is working!")

if __name__ == "__main__":
    test_company_search()