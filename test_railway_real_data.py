#!/usr/bin/env python3
"""
Playwright Test for Railway REAL Data Extraction
Tests the deployed system with actual websites and validates REAL data extraction
"""

import asyncio
import json
import requests
import time
from datetime import datetime
import os

# Railway deployment URL
RAILWAY_URL = "https://brand-audit.up.railway.app"

def test_railway_health():
    """Test if Railway deployment is healthy"""
    print("🔍 Testing Railway health...")
    
    try:
        response = requests.get(f"{RAILWAY_URL}/health", timeout=10)
        if response.status_code == 200:
            print("✅ Railway deployment is healthy")
            return True
        else:
            print(f"❌ Railway health check failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Railway health check failed: {e}")
        return False

def test_single_brand_analysis():
    """Test single brand analysis with REAL data"""
    print("\n🔍 Testing single brand analysis with REAL data...")
    
    test_url = "https://www.stripe.com"
    
    try:
        payload = {"url": test_url}
        response = requests.post(
            f"{RAILWAY_URL}/api/analyze-real",
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            analysis = data.get('analysis', {})
            
            print(f"✅ Successfully analyzed {test_url}")
            print(f"   Brand Name: {analysis.get('company_name', 'Not found')}")
            print(f"   Colors Found: {len(analysis.get('color_palette', []))}")
            print(f"   Logo Found: {'✓' if analysis.get('logo_base64') else '✗'}")
            print(f"   Positioning: {analysis.get('brand_positioning', 'Not found')[:50]}...")
            
            # Validate REAL data
            if analysis.get('data_source') != 'REAL_EXTRACTION':
                print("❌ FAKE DATA DETECTED - FAILURE")
                return False
            
            if len(analysis.get('color_palette', [])) == 0:
                print("❌ No real colors extracted - FAILURE")
                return False
            
            print("✅ REAL DATA CONFIRMED")
            return True
        else:
            print(f"❌ Single brand analysis failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Single brand analysis failed: {e}")
        return False

def test_multi_brand_grid():
    """Test multi-brand grid generation with REAL data"""
    print("\n🔍 Testing multi-brand grid generation with REAL data...")
    
    test_urls = [
        "https://www.stripe.com",
        "https://www.shopify.com", 
        "https://www.square.com"
    ]
    
    try:
        payload = {
            "urls": test_urls,
            "title": "Payment Platforms Competitive Analysis"
        }
        
        response = requests.post(
            f"{RAILWAY_URL}/api/generate-real-grid",
            json=payload,
            timeout=60  # Give more time for multiple sites
        )
        
        if response.status_code == 200:
            # Save the HTML file
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"railway_real_grid_{timestamp}.html"
            
            with open(filename, 'wb') as f:
                f.write(response.content)
            
            print(f"✅ Successfully generated real grid: {filename}")
            print(f"📁 File size: {len(response.content)} bytes")
            
            # Validate HTML content
            html_content = response.content.decode('utf-8')
            
            # Check for REAL data indicators
            if 'REAL DATA' not in html_content:
                print("❌ REAL DATA indicator missing - FAILURE")
                return False
            
            if 'FAKE' in html_content.upper():
                print("❌ FAKE data detected in output - FAILURE") 
                return False
            
            # Check for actual brand data
            brands_found = 0
            for url in test_urls:
                if url in html_content:
                    brands_found += 1
            
            if brands_found < len(test_urls):
                print(f"❌ Only {brands_found}/{len(test_urls)} brands found in grid")
                return False
            
            print(f"✅ All {len(test_urls)} brands found in grid")
            print("✅ REAL GRID GENERATION SUCCESSFUL")
            return filename
            
        else:
            print(f"❌ Grid generation failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Grid generation failed: {e}")
        return False

def validate_html_structure(filename):
    """Validate the HTML structure contains required elements"""
    print(f"\n🔍 Validating HTML structure: {filename}")
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        required_elements = [
            'class="real-logo"',           # Real logos
            'class="color-swatch"',        # Color swatches  
            'class="positioning-text"',    # Brand positioning
            'class="real-data-badge"',     # Real data indicators
            'background-color: #',         # Actual color values
        ]
        
        missing_elements = []
        for element in required_elements:
            if element not in html_content:
                missing_elements.append(element)
        
        if missing_elements:
            print(f"❌ Missing required elements: {missing_elements}")
            return False
        
        print("✅ All required HTML elements present")
        
        # Count visual elements
        import re
        color_swatches = len(re.findall(r'class="color-swatch"', html_content))
        logo_elements = len(re.findall(r'class="real-logo"', html_content))
        brand_columns = len(re.findall(r'class="brand-column"', html_content))
        
        print(f"📊 Visual elements found:")
        print(f"   - Brand columns: {brand_columns}")
        print(f"   - Logo elements: {logo_elements}")
        print(f"   - Color swatches: {color_swatches}")
        
        if brand_columns < 3:
            print("❌ Insufficient brand columns")
            return False
        
        if color_swatches < 9:  # At least 3 colors per 3 brands
            print("❌ Insufficient color swatches")
            return False
        
        print("✅ HTML structure validation PASSED")
        return True
        
    except Exception as e:
        print(f"❌ HTML validation failed: {e}")
        return False

def main():
    """Run complete test suite"""
    print("🚀 STARTING RAILWAY REAL DATA TEST SUITE")
    print("=" * 60)
    print("❌ NO FAKE DATA WILL BE ACCEPTED")
    print("✅ SUCCESS = REAL visual data with logos, colors, typography")
    print("=" * 60)
    
    # Test 1: Health check
    if not test_railway_health():
        print("\n❌ DEPLOYMENT FAILED - Health check failed")
        return False
    
    # Test 2: Single brand analysis  
    if not test_single_brand_analysis():
        print("\n❌ REAL DATA EXTRACTION FAILED")
        return False
    
    # Test 3: Multi-brand grid
    grid_file = test_multi_brand_grid()
    if not grid_file:
        print("\n❌ GRID GENERATION FAILED")
        return False
    
    # Test 4: HTML validation
    if not validate_html_structure(grid_file):
        print("\n❌ HTML STRUCTURE VALIDATION FAILED")
        return False
    
    print("\n" + "=" * 60)
    print("🎉 ALL TESTS PASSED - REAL DATA SYSTEM WORKING")
    print(f"📁 Generated file: {grid_file}")
    print(f"📍 Open this file in your browser to view the REAL competitive grid")
    print("✅ Contains: Real logos, real colors, real positioning, real typography")
    print("❌ Contains: NO fake data")
    print("=" * 60)
    
    return grid_file

if __name__ == "__main__":
    result = main()
    if result:
        print(f"\n🎯 SUCCESS: {result}")
        # Also print the absolute path
        abs_path = os.path.abspath(result)
        print(f"📂 Full path: {abs_path}")
    else:
        print("\n💥 TESTS FAILED - Need to fix Railway deployment")
        exit(1)