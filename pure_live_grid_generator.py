#!/usr/bin/env python3
"""
Pure Live Grid Generator - ZERO placeholders, ZERO fallbacks, ZERO fake data
Only shows what it can actually extract from websites
"""

import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin, urlparse
import base64
from datetime import datetime
import json
import os

class PureLiveGridGenerator:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def fetch_page(self, url):
        """Fetch webpage content - returns None if fails"""
        try:
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(f"❌ Failed to fetch {url}: {e}")
            return None
    
    def extract_real_logo_base64(self, html_content, base_url):
        """Extract actual logo and convert to base64 - returns None if not found"""
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Prioritized logo selectors
        logo_selectors = [
            'img[alt*="logo" i]',
            'img[src*="logo" i]', 
            'img[class*="logo" i]',
            '.logo img',
            '.header img:first-child',
            'header img:first-child',
            '.brand img',
            '.navbar-brand img',
            '.site-logo img'
        ]
        
        for selector in logo_selectors:
            logos = soup.select(selector)
            for logo in logos:
                src = logo.get('src')
                if src and self._is_definitely_logo(src, logo.get('alt', '')):
                    full_url = urljoin(base_url, src)
                    base64_image = self._download_image_as_base64(full_url)
                    if base64_image:
                        return base64_image
        
        return None  # No fallback
    
    def _is_definitely_logo(self, src, alt_text):
        """Strict logo detection - only returns True if definitely a logo"""
        src_lower = src.lower()
        alt_lower = alt_text.lower()
        
        # Must contain these
        required_indicators = ['logo']
        has_required = any(indicator in src_lower or indicator in alt_lower for indicator in required_indicators)
        
        # Must NOT contain these
        forbidden_patterns = ['banner', 'hero', 'background', 'social', 'icon-', 'favicon', 'sprite']
        has_forbidden = any(pattern in src_lower for pattern in forbidden_patterns)
        
        return has_required and not has_forbidden
    
    def _download_image_as_base64(self, url):
        """Download image and convert to base64 - returns None if fails"""
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            # Must be an image
            content_type = response.headers.get('content-type', '')
            if not content_type.startswith('image/'):
                return None
            
            # Convert to base64
            image_data = base64.b64encode(response.content).decode('utf-8')
            return f"data:{content_type};base64,{image_data}"
            
        except Exception:
            return None  # Silent fail, no logging
    
    def extract_real_colors_only(self, html_content):
        """Extract only real colors found in CSS - returns empty list if none found"""
        colors = set()
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # From style tags
        for style_tag in soup.find_all('style'):
            css_content = style_tag.get_text()
            colors.update(re.findall(r'#[0-9a-fA-F]{6}', css_content))
            colors.update(re.findall(r'#[0-9a-fA-F]{3}', css_content))
        
        # From inline styles
        for element in soup.find_all(style=True):
            style_content = element.get('style')
            colors.update(re.findall(r'#[0-9a-fA-F]{6}', style_content))
            colors.update(re.findall(r'#[0-9a-fA-F]{3}', style_content))
        
        # Clean colors
        cleaned_colors = []
        for color in colors:
            if len(color) == 4:  # #abc format
                color = '#' + ''.join([c*2 for c in color[1:]])
            
            # Filter out very light/dark colors (these are usually backgrounds/text)
            try:
                r = int(color[1:3], 16)
                g = int(color[3:5], 16) 
                b = int(color[5:7], 16)
                
                # Only include colors that are clearly branded colors
                if not (all(c > 240 for c in [r,g,b]) or all(c < 15 for c in [r,g,b])):
                    # Only include colors that appear multiple times (likely brand colors)
                    if css_content.count(color) > 1:
                        cleaned_colors.append(color)
            except:
                continue
        
        # Return only unique colors found, or empty list
        return list(dict.fromkeys(cleaned_colors))
    
    def extract_real_positioning_only(self, html_content):
        """Extract actual hero/positioning text - returns None if not found"""
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Only look for clear hero sections
        hero_selectors = [
            '.hero h1',
            '.hero-title',
            '.hero-content h1',
            '.hero-section h1',
            '.jumbotron h1',
            '.banner h1',
            'h1[class*="hero"]',
            'h1[class*="title"]'
        ]
        
        for selector in hero_selectors:
            elements = soup.select(selector)
            for element in elements:
                text = element.get_text().strip()
                # Must be substantial and not just navigation
                if 30 <= len(text) <= 150 and not any(nav_word in text.lower() for nav_word in ['menu', 'navigation', 'login', 'sign in']):
                    return text
        
        return None  # No fallback to title or domain
    
    def extract_real_brand_name_only(self, html_content):
        """Extract actual brand name - returns None if not clearly identifiable"""
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Look for clear brand indicators
        brand_selectors = [
            '.logo',
            '.brand',
            '.site-title', 
            '.company-name',
            '[class*="brand"]',
            '[class*="logo"]'
        ]
        
        for selector in brand_selectors:
            elements = soup.select(selector)
            for element in elements:
                text = element.get_text().strip()
                if text and 2 <= len(text) <= 50 and text.replace(' ', '').isalnum():
                    return text
        
        return None  # No fallback to title or domain
    
    def analyze_website_pure(self, url):
        """Analyze website with ZERO fallbacks - returns None if insufficient data"""
        print(f"🔍 Analyzing: {url}")
        
        html_content = self.fetch_page(url)
        if not html_content:
            return None
        
        # Extract only real data
        brand_name = self.extract_real_brand_name_only(html_content)
        positioning = self.extract_real_positioning_only(html_content)
        colors = self.extract_real_colors_only(html_content)
        logo_base64 = self.extract_real_logo_base64(html_content, url)
        
        # Only return if we found meaningful data
        if brand_name or positioning or colors or logo_base64:
            result = {
                "url": url,
                "analysis_timestamp": datetime.now().isoformat()
            }
            
            if brand_name:
                result["company_name"] = brand_name
            if positioning:
                result["brand_positioning"] = positioning  
            if colors:
                result["color_palette"] = colors
            if logo_base64:
                result["logo_base64"] = logo_base64
            
            print(f"✅ {brand_name or 'Unknown'} - Colors: {len(colors)}, Logo: {'✓' if logo_base64 else '✗'}, Positioning: {'✓' if positioning else '✗'}")
            return result
        else:
            print(f"❌ {url} - Insufficient data extracted")
            return None
    
    def generate_pure_grid_html(self, urls, page_title="Competitive Landscape Analysis"):
        """Generate grid with ONLY real extracted data"""
        
        print(f"🚀 Analyzing {len(urls)} websites for REAL data only...")
        print("=" * 60)
        
        # Analyze all URLs - only keep successful extractions
        brand_profiles = []
        for url in urls:
            try:
                profile = self.analyze_website_pure(url)
                if profile:
                    brand_profiles.append(profile)
            except Exception as e:
                print(f"❌ Error analyzing {url}: {e}")
        
        if not brand_profiles:
            print("❌ No brands successfully analyzed")
            return None, []
        
        print(f"\n📊 Successfully extracted data from {len(brand_profiles)} brands")
        
        # Generate HTML with only real data
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pure Competitive Analysis - {datetime.now().strftime('%B %d, %Y')}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.4;
            color: #333;
            background: #f8f9fa;
        }}
        
        .page {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            padding: 20px;
            min-height: 100vh;
        }}
        
        .page-header {{
            text-align: center;
            margin-bottom: 30px;
            position: relative;
        }}
        
        .main-title {{
            font-size: 2.5em;
            font-weight: 700;
            color: #2c3e50;
            margin-bottom: 10px;
        }}
        
        .subtitle {{
            font-size: 1.1em;
            color: #6c757d;
            margin-bottom: 5px;
        }}
        
        .analysis-date {{
            font-size: 0.9em;
            color: #8e9ba8;
        }}
        
        .brand-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
        }}
        
        .brand-card {{
            background: white;
            border: 1px solid #e9ecef;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }}
        
        .brand-header {{
            display: flex;
            align-items: center;
            margin-bottom: 15px;
            min-height: 60px;
        }}
        
        .brand-logo {{
            max-width: 120px;
            max-height: 50px;
            object-fit: contain;
            margin-right: 15px;
        }}
        
        .brand-name {{
            font-size: 1.2em;
            font-weight: 600;
            color: #2c3e50;
        }}
        
        .brand-positioning {{
            font-size: 0.9em;
            line-height: 1.4;
            color: #495057;
            margin-bottom: 15px;
            min-height: 60px;
        }}
        
        .color-palette {{
            margin-bottom: 15px;
        }}
        
        .color-palette-title {{
            font-size: 0.8em;
            color: #6c757d;
            margin-bottom: 8px;
            font-weight: 600;
        }}
        
        .color-swatches {{
            display: flex;
            gap: 5px;
            flex-wrap: wrap;
        }}
        
        .color-swatch {{
            width: 30px;
            height: 30px;
            border-radius: 4px;
            border: 1px solid #dee2e6;
            cursor: pointer;
            position: relative;
        }}
        
        .color-swatch:hover::after {{
            content: attr(data-color);
            position: absolute;
            bottom: -25px;
            left: 50%;
            transform: translateX(-50%);
            background: #333;
            color: white;
            padding: 2px 6px;
            border-radius: 3px;
            font-size: 0.7em;
            white-space: nowrap;
        }}
        
        .url-info {{
            font-size: 0.8em;
            color: #8e9ba8;
            border-top: 1px solid #e9ecef;
            padding-top: 10px;
            margin-top: 15px;
        }}
        
        .empty-state {{
            text-align: center;
            color: #6c757d;
            font-style: italic;
        }}
    </style>
</head>
<body>
    <div class="page">
        <div class="page-header">
            <h1 class="main-title">{page_title}</h1>
            <p class="subtitle">Live Data - No Placeholders</p>
            <p class="analysis-date">Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
        </div>
        
        <div class="brand-grid">"""

        # Generate cards for each successfully analyzed brand
        for brand in brand_profiles:
            html_content += f"""
            <div class="brand-card">
                <div class="brand-header">"""
            
            # Logo (only if actually found)
            if brand.get("logo_base64"):
                html_content += f'<img src="{brand["logo_base64"]}" alt="Logo" class="brand-logo">'
            
            # Brand name (only if actually extracted)
            if brand.get("company_name"):
                html_content += f'<div class="brand-name">{brand["company_name"]}</div>'
            
            html_content += """
                </div>"""
            
            # Positioning (only if actually found)
            if brand.get("brand_positioning"):
                html_content += f'<div class="brand-positioning">{brand["brand_positioning"]}</div>'
            
            # Colors (only if actually extracted)
            if brand.get("color_palette"):
                html_content += f"""
                <div class="color-palette">
                    <div class="color-palette-title">Extracted Colors ({len(brand["color_palette"])} found)</div>
                    <div class="color-swatches">"""
                
                for color in brand["color_palette"]:
                    html_content += f'<div class="color-swatch" style="background-color: {color};" data-color="{color}"></div>'
                
                html_content += """
                    </div>
                </div>"""
            
            # URL info
            html_content += f"""
                <div class="url-info">
                    Source: {brand["url"]}<br>
                    Analyzed: {datetime.fromisoformat(brand["analysis_timestamp"]).strftime('%m/%d/%Y %I:%M %p')}
                </div>
            </div>"""
        
        html_content += """
        </div>
    </div>
</body>
</html>"""
        
        return html_content, brand_profiles

def main():
    """Generate pure competitive analysis with zero fake data"""
    
    # Test URLs
    urls = [
        "https://www.apple.com",
        "https://www.microsoft.com",
        "https://www.google.com",
        "https://www.amazon.com",
        "https://www.netflix.com",
        "https://www.spotify.com",
        "https://www.adobe.com",
        "https://www.salesforce.com"
    ]
    
    generator = PureLiveGridGenerator()
    
    print("🔥 PURE LIVE ANALYSIS - ZERO FAKE DATA")
    print("Only showing what can actually be extracted")
    print("=" * 60)
    
    html_content, profiles = generator.generate_pure_grid_html(urls)
    
    if html_content:
        # Save file
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_filename = f"pure_competitive_analysis_{timestamp}.html"
        
        try:
            with open(output_filename, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            print(f"\n🎉 SUCCESS! Pure analysis generated!")
            print(f"📁 File: {output_filename}")
            print(f"🌐 ZERO placeholders - only real extracted data")
            print(f"📊 Successfully analyzed: {len(profiles)} brands")
            
            # Show what was extracted
            for profile in profiles:
                name = profile.get("company_name", "Unknown")
                has_logo = "✓" if profile.get("logo_base64") else "✗"
                has_positioning = "✓" if profile.get("brand_positioning") else "✗"
                color_count = len(profile.get("color_palette", []))
                print(f"   • {name}: Logo {has_logo}, Positioning {has_positioning}, Colors {color_count}")
            
            # Save raw data
            json_filename = f"pure_brand_data_{timestamp}.json"
            with open(json_filename, 'w') as f:
                json.dump(profiles, f, indent=2)
            print(f"💾 Raw data: {json_filename}")
            
        except Exception as e:
            print(f"❌ Error saving file: {e}")
    else:
        print("❌ No data could be extracted from any URLs")

if __name__ == "__main__":
    main()