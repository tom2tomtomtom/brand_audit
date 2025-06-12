#!/usr/bin/env python3
"""
Live Brand Grid Generator - Pulls Real Logos, Colors, and Data
"""

import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin, urlparse
import base64
from datetime import datetime
import json
import os

class LiveBrandGridGenerator:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def fetch_page(self, url):
        """Fetch webpage content"""
        try:
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(f"Failed to fetch {url}: {e}")
            return None
    
    def extract_logo_as_base64(self, html_content, base_url):
        """Extract logo and convert to base64 for embedding"""
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Logo selectors (prioritized)
        logo_selectors = [
            'img[alt*="logo" i]',
            'img[src*="logo" i]',
            'img[class*="logo" i]',
            '.logo img',
            '.header img:first-child',
            'header img:first-child',
            '.brand img',
            '.navbar-brand img'
        ]
        
        for selector in logo_selectors:
            logos = soup.select(selector)
            for logo in logos:
                src = logo.get('src')
                if src and self._is_likely_logo(src, logo.get('alt', '')):
                    full_url = urljoin(base_url, src)
                    base64_image = self._download_image_as_base64(full_url)
                    if base64_image:
                        return base64_image
        
        return None
    
    def _is_likely_logo(self, src, alt_text):
        """Check if image is likely a logo"""
        logo_indicators = ['logo', 'brand']
        src_lower = src.lower()
        alt_lower = alt_text.lower()
        
        # Must contain logo indicators
        has_logo_indicator = any(indicator in src_lower or indicator in alt_lower for indicator in logo_indicators)
        
        # Avoid these patterns
        avoid_patterns = ['banner', 'hero', 'background', 'social', 'icon-', 'favicon']
        has_avoid_pattern = any(pattern in src_lower for pattern in avoid_patterns)
        
        return has_logo_indicator and not has_avoid_pattern
    
    def _download_image_as_base64(self, url):
        """Download image and convert to base64"""
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            # Check if it's actually an image
            content_type = response.headers.get('content-type', '')
            if not content_type.startswith('image/'):
                return None
            
            # Convert to base64
            image_data = base64.b64encode(response.content).decode('utf-8')
            return f"data:{content_type};base64,{image_data}"
            
        except Exception as e:
            print(f"Failed to download image {url}: {e}")
            return None
    
    def extract_real_colors(self, html_content):
        """Extract actual colors from website CSS"""
        colors = set()
        
        # Extract from CSS styles
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
        
        # From CSS classes (common color patterns)
        for element in soup.find_all(class_=True):
            classes = ' '.join(element.get('class'))
            # Look for color classes
            color_matches = re.findall(r'(?:bg-|text-|border-)?(?:#[0-9a-fA-F]{6}|#[0-9a-fA-F]{3})', classes)
            colors.update(color_matches)
        
        # Clean and filter colors
        cleaned_colors = []
        for color in colors:
            if len(color) == 4:  # #abc format
                color = '#' + ''.join([c*2 for c in color[1:]])
            
            # Convert to RGB to filter out very light/dark colors
            try:
                r = int(color[1:3], 16)
                g = int(color[3:5], 16)
                b = int(color[5:7], 16)
                
                # Skip very light or very dark colors
                if not (all(c > 240 for c in [r,g,b]) or all(c < 15 for c in [r,g,b])):
                    cleaned_colors.append(color)
            except:
                continue
        
        # Return top 6 unique colors
        unique_colors = list(dict.fromkeys(cleaned_colors))[:6]
        
        # Ensure we have 6 colors (pad with defaults if needed)
        while len(unique_colors) < 6:
            defaults = ['#666666', '#999999', '#cccccc', '#e9ecef', '#f8f9fa', '#ffffff']
            for default in defaults:
                if default not in unique_colors:
                    unique_colors.append(default)
                    break
        
        return unique_colors[:6]
    
    def extract_brand_positioning(self, html_content):
        """Extract hero/main headline from website"""
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Common hero/headline selectors
        hero_selectors = [
            'h1',
            '.hero h1',
            '.hero-title',
            '.main-headline',
            '.hero .headline',
            '.banner h1',
            '.jumbotron h1',
            '.hero-content h1',
            '.hero-section h1'
        ]
        
        for selector in hero_selectors:
            elements = soup.select(selector)
            for element in elements:
                text = element.get_text().strip()
                if len(text) > 20 and len(text) < 200:  # Reasonable length
                    return text
        
        # Fallback to title or first substantial heading
        title = soup.find('title')
        if title:
            return title.get_text().strip()
        
        return "No positioning statement found"
    
    def extract_brand_name(self, html_content, url):
        """Extract brand/company name"""
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Try title tag first
        title = soup.find('title')
        if title:
            title_text = title.get_text().strip()
            # Clean up common title patterns
            for separator in [' | ', ' - ', ' :: ', ' — ']:
                if separator in title_text:
                    return title_text.split(separator)[0].strip()
            return title_text
        
        # Fallback to domain name
        domain = urlparse(url).netloc
        return domain.replace('www.', '').replace('.com', '').title()
    
    def analyze_live_brand(self, url):
        """Analyze a brand website and extract real data"""
        print(f"🔍 Analyzing: {url}")
        
        html_content = self.fetch_page(url)
        if not html_content:
            return None
        
        # Extract real data
        brand_name = self.extract_brand_name(html_content, url)
        positioning = self.extract_brand_positioning(html_content)
        colors = self.extract_real_colors(html_content)
        logo_base64 = self.extract_logo_as_base64(html_content, url)
        
        print(f"✅ {brand_name} - Found {len(colors)} colors, Logo: {'✓' if logo_base64 else '✗'}")
        
        return {
            "url": url,
            "company_name": brand_name,
            "brand_positioning": positioning,
            "color_palette": colors,
            "logo_base64": logo_base64,
            "analysis_timestamp": datetime.now().isoformat()
        }
    
    def generate_live_grid_html(self, urls, page_title="There is a huge opportunity in the category"):
        """Generate grid with real live data"""
        
        print(f"🚀 Analyzing {len(urls)} websites for live data...")
        
        # Analyze all URLs
        brand_profiles = []
        for url in urls:
            try:
                profile = self.analyze_live_brand(url)
                if profile:
                    brand_profiles.append(profile)
            except Exception as e:
                print(f"❌ Error analyzing {url}: {e}")
        
        # Pad to 10 brands if needed
        while len(brand_profiles) < 10:
            brand_profiles.append({
                "company_name": f"Brand {len(brand_profiles) + 1}",
                "brand_positioning": "Analysis pending...",
                "color_palette": ["#e9ecef", "#dee2e6", "#ced4da", "#adb5bd", "#6c757d", "#495057"],
                "logo_base64": None
            })
        
        # Generate HTML with real data
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Live Competitive Landscape Analysis - {datetime.now().strftime('%B %d, %Y')}</title>
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
            width: 100vw;
            min-height: 100vh;
            background: white;
            margin: 0;
            padding: 20px;
        }}
        
        .page-header {{
            text-align: center;
            margin-bottom: 30px;
            position: relative;
        }}
        
        .page-number {{
            position: absolute;
            top: 0;
            right: 0;
            font-size: 0.9em;
            color: #6c757d;
            background: white;
            padding: 5px 10px;
            border-radius: 3px;
            border: 1px solid #e9ecef;
        }}
        
        .main-title {{
            font-size: 2.5em;
            font-weight: 700;
            color: #2c3e50;
            margin-bottom: 10px;
            line-height: 1.2;
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
        
        .brand-grid-container {{
            background: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            overflow: hidden;
            max-width: 100%;
        }}
        
        .brand-grid {{
            display: grid;
            grid-template-columns: repeat(10, 1fr);
            grid-template-rows: 70px 140px 70px;
            gap: 12px;
            min-height: 350px;
        }}
        
        /* Row 1: Company Logos */
        .logo-cell {{
            grid-row: 1;
            background: white;
            border: 1px solid #e9ecef;
            border-radius: 8px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }}
        
        .brand-logo-img {{
            max-width: 100%;
            max-height: 35px;
            object-fit: contain;
            margin-bottom: 5px;
        }}
        
        .brand-logo-placeholder {{
            width: 100%;
            height: 35px;
            background: linear-gradient(135deg, #e9ecef, #dee2e6);
            border-radius: 4px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.7em;
            color: #6c757d;
            font-weight: 600;
            margin-bottom: 5px;
            text-align: center;
            line-height: 1.1;
        }}
        
        .brand-name {{
            font-size: 0.65em;
            font-weight: 600;
            color: #495057;
            text-align: center;
            line-height: 1.1;
        }}
        
        /* Row 2: Brand Positioning */
        .positioning-cell {{
            grid-row: 2;
            background: white;
            border: 1px solid #e9ecef;
            border-radius: 8px;
            padding: 12px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            overflow: hidden;
        }}
        
        .positioning-text {{
            font-size: 0.75em;
            line-height: 1.3;
            color: #495057;
            text-align: left;
            overflow: hidden;
            display: -webkit-box;
            -webkit-line-clamp: 8;
            -webkit-box-orient: vertical;
        }}
        
        /* Row 3: Color Palettes */
        .color-cell {{
            grid-row: 3;
            background: white;
            border: 1px solid #e9ecef;
            border-radius: 8px;
            padding: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            display: flex;
            flex-direction: column;
        }}
        
        .color-swatches {{
            display: grid;
            grid-template-columns: repeat(6, 1fr);
            gap: 3px;
            flex-grow: 1;
        }}
        
        .color-swatch {{
            height: 25px;
            border-radius: 3px;
            border: 1px solid #dee2e6;
            position: relative;
            cursor: pointer;
        }}
        
        .color-labels {{
            font-size: 0.6em;
            color: #6c757d;
            text-align: center;
            margin-top: 4px;
            line-height: 1.1;
        }}
        
        /* Grid positioning */
        .brand-col-1 {{ grid-column: 1; }}
        .brand-col-2 {{ grid-column: 2; }}
        .brand-col-3 {{ grid-column: 3; }}
        .brand-col-4 {{ grid-column: 4; }}
        .brand-col-5 {{ grid-column: 5; }}
        .brand-col-6 {{ grid-column: 6; }}
        .brand-col-7 {{ grid-column: 7; }}
        .brand-col-8 {{ grid-column: 8; }}
        .brand-col-9 {{ grid-column: 9; }}
        .brand-col-10 {{ grid-column: 10; }}
        
        @media (max-width: 1200px) {{
            .brand-grid {{
                grid-template-columns: repeat(5, 1fr);
            }}
        }}
    </style>
</head>
<body>
    <div class="page">
        <div class="page-header">
            <div class="page-number">Page 1</div>
            <h1 class="main-title">{page_title}</h1>
            <p class="subtitle">Live Competitive Landscape Analysis</p>
            <p class="analysis-date">Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
        </div>
        
        <div class="brand-grid-container">
            <div class="brand-grid">"""

        # Generate cells for each brand
        for i, brand in enumerate(brand_profiles[:10], 1):
            col_class = f"brand-col-{i}"
            
            # Logo (real or placeholder)
            if brand.get("logo_base64"):
                logo_html = f'<img src="{brand["logo_base64"]}" alt="{brand["company_name"]} logo" class="brand-logo-img">'
            else:
                logo_html = f'<div class="brand-logo-placeholder">{brand["company_name"].upper()}</div>'
            
            html_content += f"""
                <!-- Brand {i}: {brand["company_name"]} -->
                <div class="logo-cell {col_class}">
                    {logo_html}
                    <div class="brand-name">{brand["company_name"]}</div>
                </div>
                
                <div class="positioning-cell {col_class}">
                    <div class="positioning-text">{brand["brand_positioning"]}</div>
                </div>
                
                <div class="color-cell {col_class}">
                    <div class="color-swatches">"""
            
            # Real color swatches
            for color in brand["color_palette"]:
                html_content += f'<div class="color-swatch" style="background-color: {color};" title="{color}"></div>'
            
            primary_colors = " • ".join(brand["color_palette"][:3])
            html_content += f"""
                    </div>
                    <div class="color-labels">{primary_colors}</div>
                </div>"""
        
        html_content += """
            </div>
        </div>
    </div>
</body>
</html>"""
        
        return html_content, brand_profiles

def main():
    """Generate live competitive grid with real data"""
    
    # Financial services URLs
    urls = [
        "https://www.tdameritrade.com",
        "https://www.schwab.com", 
        "https://www.fidelity.com",
        "https://www.vanguard.com",
        "https://www.edwardjones.com"
    ]
    
    generator = LiveBrandGridGenerator()
    
    print("🔥 GENERATING LIVE COMPETITIVE GRID WITH REAL DATA")
    print("=" * 60)
    
    html_content, profiles = generator.generate_live_grid_html(urls)
    
    # Save file
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_filename = f"live_competitive_grid_{timestamp}.html"
    
    try:
        with open(output_filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"\n🎉 SUCCESS! Live competitive grid generated!")
        print(f"📁 File: {output_filename}")
        print(f"🌐 Open in browser to see REAL logos, colors, and positioning")
        print(f"📊 Analyzed {len([p for p in profiles if p.get('analysis_timestamp')])} brands successfully")
        
        # Save data as JSON for reference
        json_filename = f"brand_data_{timestamp}.json"
        with open(json_filename, 'w') as f:
            json.dump(profiles, f, indent=2)
        print(f"💾 Brand data saved to: {json_filename}")
        
    except Exception as e:
        print(f"❌ Error saving file: {e}")

if __name__ == "__main__":
    main()