#!/usr/bin/env python3
"""
Test script for the enhanced brand audit system
Run this to test the complete pipeline with sample data
"""

import os
import sys
import json
from datetime import datetime

# Add current directory to path for imports
sys.path.append(os.path.dirname(__file__))

from enhanced_brand_profiler import analyze_competitor_brands, generate_enhanced_report_data
from enhanced_report_generator import generate_report_from_profiles

def test_enhanced_brand_audit():
    """Test the complete enhanced brand audit pipeline"""
    print("🚀 Testing Enhanced Brand Audit System")
    print("=" * 50)
    
    # Test URLs - mix of financial services companies
    test_urls = [
        "https://www.schwab.com",
        "https://www.fidelity.com", 
        "https://www.vanguard.com"
    ]
    
    print(f"📊 Testing with {len(test_urls)} URLs:")
    for i, url in enumerate(test_urls, 1):
        print(f"  {i}. {url}")
    print()
    
    try:
        # Step 1: Analyze brands
        print("🔍 Step 1: Analyzing competitor brands...")
        brand_profiles = analyze_competitor_brands(test_urls)
        
        if not brand_profiles:
            print("❌ Failed to analyze any brands")
            return False
        
        print(f"✅ Successfully analyzed {len(brand_profiles)} brands")
        
        # Display analysis results
        for profile in brand_profiles:
            print(f"  • {profile['company_name']}")
            print(f"    Positioning: {profile['brand_positioning'][:80]}...")
            print(f"    Colors: {len(profile['color_palette'])} extracted")
            print(f"    Personality: {', '.join(profile['personality_descriptors'][:3])}")
            print()
        
        # Step 2: Generate enhanced report
        print("📝 Step 2: Generating enhanced HTML report...")
        output_filename = f"test_enhanced_audit_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        
        success = generate_report_from_profiles(brand_profiles, output_filename)
        
        if success:
            print(f"✅ Enhanced report generated successfully: {output_filename}")
            
            # Check file size
            file_size = os.path.getsize(output_filename) / 1024  # KB
            print(f"📄 Report file size: {file_size:.1f} KB")
            
            return True
        else:
            print("❌ Failed to generate enhanced report")
            return False
            
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        return False

def test_report_components():
    """Test individual report components"""
    print("\n🧪 Testing Individual Components")
    print("=" * 50)
    
    try:
        from enhanced_report_generator import EnhancedReportGenerator
        
        # Test with sample data
        sample_brand_data = [
            {
                "name": "Test Company 1",
                "positioning": "Leading provider of innovative financial solutions for modern investors seeking growth and security.",
                "personality": ["Innovative", "Trustworthy", "Professional", "Forward-thinking"],
                "colors": ["#1a73e8", "#34a853", "#fbbc04", "#ea4335", "#9aa0a6", "#202124"],
                "visual_assets": {
                    "elements": ["Modern website", "Mobile app", "Professional branding"]
                },
                "messages": ["Innovation in finance", "Customer-first approach", "Secure investing"],
                "voice": "Professional yet approachable",
                "differentiators": ["Technology leadership", "Customer service excellence"],
                "story": "Empowering investors through technology and expertise",
                "target_audience": "Tech-savvy investors aged 25-45"
            },
            {
                "name": "Test Company 2", 
                "positioning": "Traditional investment firm with decades of experience serving high-net-worth clients.",
                "personality": ["Established", "Conservative", "Reliable", "Experienced"],
                "colors": ["#0f4c75", "#3282b8", "#bbe1fa", "#1b262c", "#f8f9fa", "#6c757d"],
                "visual_assets": {
                    "elements": ["Classic design", "Print materials", "Executive branding"]
                },
                "messages": ["Proven track record", "Wealth preservation", "Legacy planning"],
                "voice": "Authoritative and confident",
                "differentiators": ["Long history", "Premium service"],
                "story": "Protecting and growing wealth for generations",
                "target_audience": "High-net-worth individuals over 45"
            }
        ]
        
        generator = EnhancedReportGenerator()
        
        # Test grid generation
        print("🎯 Testing grid HTML generation...")
        grid_html = generator.generate_grid_html(sample_brand_data)
        
        if grid_html and len(grid_html) > 1000:  # Should be substantial HTML
            print("✅ Grid HTML generated successfully")
            print(f"   Generated {len(grid_html)} characters of HTML")
        else:
            print("❌ Grid HTML generation failed or too short")
            return False
        
        # Test Stripe pages generation
        print("🎯 Testing Stripe-style pages generation...")
        stripe_html = generator.generate_stripe_pages(sample_brand_data)
        
        if stripe_html and len(stripe_html) > 500:
            print("✅ Stripe pages generated successfully")
            print(f"   Generated {len(stripe_html)} characters of HTML")
        else:
            print("❌ Stripe pages generation failed or too short")
            return False
        
        # Test complete report generation
        print("🎯 Testing complete report generation...")
        test_filename = f"component_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        success = generator.generate_enhanced_report(sample_brand_data, test_filename)
        
        if success:
            print(f"✅ Complete report generated: {test_filename}")
            file_size = os.path.getsize(test_filename) / 1024
            print(f"   File size: {file_size:.1f} KB")
            return True
        else:
            print("❌ Complete report generation failed")
            return False
            
    except Exception as e:
        print(f"❌ Component testing error: {e}")
        return False

def display_system_info():
    """Display system information and requirements"""
    print("\n📋 System Information")
    print("=" * 50)
    
    # Check required packages
    required_packages = [
        'requests', 'beautifulsoup4', 'openai', 'pandas', 
        'pillow', 'numpy', 'scikit-learn', 'flask', 'jinja2'
    ]
    
    print("📦 Required packages:")
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"  ✅ {package}")
        except ImportError:
            print(f"  ❌ {package} (missing)")
    
    # Check environment variables
    print("\n🔑 Environment variables:")
    if os.getenv("OPENAI_API_KEY"):
        print("  ✅ OPENAI_API_KEY is set")
    else:
        print("  ❌ OPENAI_API_KEY is missing")
    
    # Check file structure
    print("\n📁 File structure:")
    required_files = [
        "enhanced_brand_profiler.py",
        "enhanced_report_generator.py", 
        "enhanced_brand_audit_template.html",
        "app.py"
    ]
    
    for file in required_files:
        if os.path.exists(file):
            print(f"  ✅ {file}")
        else:
            print(f"  ❌ {file} (missing)")

def main():
    """Main test function"""
    print("🎨 Enhanced Brand Audit System Test Suite")
    print("=" * 60)
    
    # Display system info
    display_system_info()
    
    # Test components
    component_success = test_report_components()
    
    # Test full system (only if components work)
    if component_success:
        print("\n" + "=" * 60)
        full_system_success = test_enhanced_brand_audit()
        
        if full_system_success:
            print("\n🎉 ALL TESTS PASSED!")
            print("✨ Enhanced brand audit system is ready to use")
            print("\n📖 Usage:")
            print("1. Start Flask server: python app.py")
            print("2. Send POST request to /api/enhanced-brand-audit")
            print("3. Include 'urls' array in request body")
            print("4. Download generated report")
        else:
            print("\n⚠️  Component tests passed but full system failed")
    else:
        print("\n❌ Component tests failed - system not ready")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()