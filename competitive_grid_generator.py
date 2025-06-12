#!/usr/bin/env python3
"""
Competitive Landscape Grid Generator
Generates exactly the 5-row brand comparison grid as specified in the user requirements
"""

import requests
from bs4 import BeautifulSoup
import openai
from openai import OpenAI
import pandas as pd
import os
import json
import re
from PIL import Image
import io
import base64
from urllib.parse import urljoin, urlparse
import numpy as np
from sklearn.cluster import KMeans
import colorsys
from datetime import datetime

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class CompetitiveGridGenerator:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def fetch_page(self, url):
        """Fetch webpage content with error handling"""
        try:
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(f"Failed to retrieve the page: {url} -- {e}")
            return None
    
    def extract_logos(self, html_content, base_url):
        """Extract logo URLs from webpage"""
        soup = BeautifulSoup(html_content, 'html.parser')
        logo_urls = []
        
        # Common logo selectors
        logo_selectors = [
            'img[alt*="logo" i]',
            'img[src*="logo" i]',
            'img[class*="logo" i]',
            '.logo img',
            '.header img',
            '.brand img',
            'header img'
        ]
        
        for selector in logo_selectors:
            logos = soup.select(selector)
            for logo in logos:
                src = logo.get('src')
                if src:
                    full_url = urljoin(base_url, src)
                    if self._is_likely_logo(src, logo.get('alt', '')):
                        logo_urls.append(full_url)
        
        return list(set(logo_urls))[:3]  # Return top 3 logo candidates
    
    def _is_likely_logo(self, src, alt_text):
        """Determine if an image is likely a logo"""
        logo_indicators = ['logo', 'brand', 'header']
        src_lower = src.lower()
        alt_lower = alt_text.lower()
        
        # Check for logo indicators in src or alt text
        for indicator in logo_indicators:
            if indicator in src_lower or indicator in alt_lower:
                return True
        
        # Avoid common non-logo patterns
        avoid_patterns = ['banner', 'hero', 'background', 'icon', 'social']
        for pattern in avoid_patterns:
            if pattern in src_lower:
                return False
                
        return False
    
    def extract_colors_from_html(self, html_content):
        """Extract dominant colors from webpage HTML/CSS"""
        soup = BeautifulSoup(html_content, 'html.parser')
        colors = []
        
        # Extract colors from CSS styles
        styles = soup.find_all('style')
        for style in styles:
            css_content = style.get_text()
            color_matches = re.findall(r'#[0-9a-fA-F]{6}|#[0-9a-fA-F]{3}|rgb\([^)]+\)', css_content)
            colors.extend(color_matches)
        
        # Extract colors from inline styles
        for element in soup.find_all(style=True):
            style_content = element.get('style', '')
            color_matches = re.findall(r'#[0-9a-fA-F]{6}|#[0-9a-fA-F]{3}|rgb\([^)]+\)', style_content)
            colors.extend(color_matches)
        
        return self._process_colors(colors)
    
    def _process_colors(self, color_list):
        """Process and cluster colors to get dominant palette"""
        processed_colors = []
        
        for color in color_list:
            try:
                if color.startswith('#'):
                    # Convert hex to RGB
                    if len(color) == 4:  # #abc format
                        color = '#' + ''.join([c*2 for c in color[1:]])
                    rgb = tuple(int(color[i:i+2], 16) for i in (1, 3, 5))
                elif color.startswith('rgb'):
                    # Extract RGB values
                    rgb_values = re.findall(r'\d+', color)
                    rgb = tuple(int(val) for val in rgb_values[:3])
                else:
                    continue
                
                # Filter out very light/dark colors and ensure valid RGB
                if all(0 <= val <= 255 for val in rgb) and not (all(val > 240 for val in rgb) or all(val < 15 for val in rgb)):
                    processed_colors.append(rgb)
            except:
                continue
        
        if not processed_colors:
            return ['#666666', '#999999', '#cccccc', '#e9ecef', '#f8f9fa', '#ffffff']  # Default colors
        
        # Use K-means clustering to find dominant colors
        try:
            colors_array = np.array(processed_colors)
            n_colors = min(6, len(set(map(tuple, processed_colors))))
            
            if n_colors > 1:
                kmeans = KMeans(n_clusters=n_colors, random_state=42, n_init=10)
                kmeans.fit(colors_array)
                dominant_colors = kmeans.cluster_centers_.astype(int)
            else:
                dominant_colors = colors_array[:6]
            
            # Convert back to hex
            hex_colors = []
            for rgb in dominant_colors:
                hex_color = '#{:02x}{:02x}{:02x}'.format(int(rgb[0]), int(rgb[1]), int(rgb[2]))
                hex_colors.append(hex_color)
            
            return hex_colors[:6]
        except:
            return ['#666666', '#999999', '#cccccc', '#e9ecef', '#f8f9fa', '#ffffff']
    
    def extract_brand_info(self, html_content, url):
        """Extract brand information using AI"""
        truncated_html = html_content[:15000]
        
        messages = [
            {"role": "system", "content": "You are an expert brand analyst. Extract detailed brand information from webpage content."},
            {"role": "user", "content": f"""
            Analyze the following webpage content and extract comprehensive brand information.
            
            Return your response as valid JSON with these exact keys:
            {{
                "company_name": "Official company/brand name",
                "brand_positioning": "Main value proposition and positioning statement (2-3 sentences from hero section)",
                "personality_descriptors": ["Confident", "Modern", "Trustworthy", "Innovative"], // 4-6 adjectives that describe brand voice/personality
                "primary_messages": ["Key message 1", "Key message 2", "Key message 3"], // Main value propositions
                "target_audience": "Primary target customer description",
                "brand_voice": "Description of communication style and tone",
                "visual_style": "Description of visual design approach"
            }}
            
            Focus on extracting the hero headline, main value propositions, and brand personality from the content.
            
            Webpage content:
            {truncated_html}
            """}
        ]
        
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                temperature=0.3,
                max_tokens=1000
            )
            
            content = response.choices[0].message.content.strip()
            # Clean JSON response
            content = re.sub(r"```(json)?", "", content).strip()
            parsed_response = json.loads(content)
            
            return parsed_response
        except Exception as e:
            print(f"Error extracting brand info: {e}")
            return self._get_default_brand_info()
    
    def _get_default_brand_info(self):
        """Return default brand info structure"""
        return {
            "company_name": "Unknown Company",
            "brand_positioning": "No positioning statement found",
            "personality_descriptors": ["Professional", "Reliable", "Modern", "Trustworthy"],
            "primary_messages": ["Quality products and services"],
            "target_audience": "General consumers",
            "brand_voice": "Professional and informative",
            "visual_style": "Clean and modern"
        }
    
    def analyze_brand(self, url):
        """Analyze a single brand for the grid"""
        print(f"Analyzing brand: {url}")
        
        # Fetch webpage content
        html_content = self.fetch_page(url)
        if not html_content:
            return None
        
        # Extract brand information
        brand_info = self.extract_brand_info(html_content, url)
        
        # Extract logos
        logos = self.extract_logos(html_content, url)
        
        # Extract colors
        colors = self.extract_colors_from_html(html_content)
        
        # Compile brand profile for grid
        brand_profile = {
            "url": url,
            "company_name": brand_info.get("company_name", "Unknown"),
            "brand_positioning": brand_info.get("brand_positioning", ""),
            "personality_descriptors": brand_info.get("personality_descriptors", [])[:4],  # Limit to 4
            "color_palette": colors[:6],  # Limit to 6 colors
            "logo_url": logos[0] if logos else None,
            "visual_style": brand_info.get("visual_style", ""),
            "analysis_timestamp": datetime.now().isoformat()
        }
        
        return brand_profile
    
    def generate_grid_html(self, brand_profiles, page_title="There is a huge opportunity in the category"):
        """Generate the exact 5-row competitive landscape grid as HTML"""
        
        # Ensure we have 10 brands (pad with empty slots if needed)
        while len(brand_profiles) < 10:
            brand_profiles.append({
                "company_name": f"Brand {len(brand_profiles) + 1}",
                "brand_positioning": "Analysis pending...",
                "personality_descriptors": ["TBD", "TBD", "TBD", "TBD"],
                "color_palette": ["#e9ecef", "#dee2e6", "#ced4da", "#adb5bd", "#6c757d", "#495057"],
                "logo_url": None,
                "visual_style": "Pending analysis"
            })
        
        # Truncate to 10 brands if more provided
        brand_profiles = brand_profiles[:10]
        
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Competitive Landscape Analysis - {datetime.now().strftime('%B %d, %Y')}</title>
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
        
        /* ===== 5-ROW BRAND GRID SYSTEM ===== */
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
            grid-template-rows: 70px 140px 90px 70px 180px;
            gap: 12px;
            min-height: 550px;
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
        
        /* Row 2: Brand Positioning Statements */
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
        
        /* Row 3: Brand Personality Descriptors */
        .personality-cell {{
            grid-row: 3;
            background: white;
            border: 1px solid #e9ecef;
            border-radius: 8px;
            padding: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            display: flex;
            flex-direction: column;
            justify-content: flex-start;
        }}
        
        .personality-words {{
            display: flex;
            flex-wrap: wrap;
            gap: 4px;
        }}
        
        .personality-tag {{
            background: #f8f9fa;
            border: 1px solid #e9ecef;
            border-radius: 12px;
            padding: 3px 8px;
            font-size: 0.65em;
            font-weight: 500;
            color: #495057;
            white-space: nowrap;
        }}
        
        /* Row 4: Color Palette Swatches */
        .color-cell {{
            grid-row: 4;
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
        
        /* Row 5: Visual Assets & Screenshots */
        .visual-cell {{
            grid-row: 5;
            background: white;
            border: 1px solid #e9ecef;
            border-radius: 8px;
            padding: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            display: flex;
            flex-direction: column;
        }}
        
        .screenshot-container {{
            flex-grow: 1;
            background: #f8f9fa;
            border-radius: 4px;
            border: 1px solid #e9ecef;
            overflow: hidden;
            position: relative;
            margin-bottom: 6px;
        }}
        
        .screenshot-placeholder {{
            width: 100%;
            height: 100%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.7em;
            color: #6c757d;
            text-align: center;
            line-height: 1.2;
        }}
        
        .visual-assets-list {{
            font-size: 0.6em;
            color: #6c757d;
            line-height: 1.2;
        }}
        
        /* Grid positioning for each brand column */
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
        
        /* Responsive Design */
        @media (max-width: 1200px) {{
            .brand-grid {{
                grid-template-columns: repeat(5, 1fr);
            }}
            
            .brand-col-1, .brand-col-6 {{ grid-column: 1; }}
            .brand-col-2, .brand-col-7 {{ grid-column: 2; }}
            .brand-col-3, .brand-col-8 {{ grid-column: 3; }}
            .brand-col-4, .brand-col-9 {{ grid-column: 4; }}
            .brand-col-5, .brand-col-10 {{ grid-column: 5; }}
        }}
        
        @media print {{
            .page {{
                page-break-after: always;
                width: 210mm;
                min-height: 297mm;
            }}
            
            body {{
                print-color-adjust: exact;
                -webkit-print-color-adjust: exact;
            }}
        }}
    </style>
</head>
<body>
    <div class="page">
        <div class="page-header">
            <div class="page-number">Page 1</div>
            <h1 class="main-title">{page_title}</h1>
            <p class="subtitle">Competitive Landscape Analysis</p>
            <p class="analysis-date">Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
        </div>
        
        <div class="brand-grid-container">
            <div class="brand-grid">"""

        # Generate grid cells for each brand
        for i, brand in enumerate(brand_profiles, 1):
            col_class = f"brand-col-{i}"
            
            # Row 1: Company Logos
            logo_html = f'<img src="{brand["logo_url"]}" alt="{brand["company_name"]} logo" class="brand-logo-img">' if brand.get("logo_url") else f'<div class="brand-logo-placeholder">{brand["company_name"].upper()}</div>'
            
            html_content += f"""
                <!-- Brand {i}: {brand["company_name"]} -->
                <!-- Row 1: Logo -->
                <div class="logo-cell {col_class}">
                    {logo_html}
                    <div class="brand-name">{brand["company_name"]}</div>
                </div>
                
                <!-- Row 2: Positioning -->
                <div class="positioning-cell {col_class}">
                    <div class="positioning-text">{brand["brand_positioning"]}</div>
                </div>
                
                <!-- Row 3: Personality -->
                <div class="personality-cell {col_class}">
                    <div class="personality-words">"""
            
            # Add personality tags
            for descriptor in brand["personality_descriptors"]:
                html_content += f'<span class="personality-tag">{descriptor}</span>'
            
            html_content += f"""
                    </div>
                </div>
                
                <!-- Row 4: Colors -->
                <div class="color-cell {col_class}">
                    <div class="color-swatches">"""
            
            # Add color swatches
            for color in brand["color_palette"]:
                html_content += f'<div class="color-swatch" style="background-color: {color};"></div>'
            
            # Add primary colors in labels
            primary_colors = " • ".join(brand["color_palette"][:3])
            html_content += f"""
                    </div>
                    <div class="color-labels">{primary_colors}</div>
                </div>
                
                <!-- Row 5: Visual Assets -->
                <div class="visual-cell {col_class}">
                    <div class="screenshot-container">
                        <div class="screenshot-placeholder">Homepage Screenshot</div>
                    </div>
                    <div class="visual-assets-list">{brand["visual_style"]} • Brand materials</div>
                </div>"""
        
        html_content += """
            </div>
        </div>
    </div>
</body>
</html>"""
        
        return html_content
    
    def generate_competitive_landscape_report(self, urls, page_title="There is a huge opportunity in the category", output_filename=None):
        """Generate complete competitive landscape report"""
        
        if not output_filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_filename = f"competitive_landscape_{timestamp}.html"
        
        print(f"Analyzing {len(urls)} brands for competitive landscape grid...")
        
        # Analyze all brands
        brand_profiles = []
        for url in urls:
            try:
                profile = self.analyze_brand(url)
                if profile:
                    brand_profiles.append(profile)
                    print(f"✓ Analyzed: {profile['company_name']}")
                else:
                    print(f"✗ Failed to analyze: {url}")
            except Exception as e:
                print(f"✗ Error analyzing {url}: {e}")
        
        # Generate HTML report
        html_content = self.generate_grid_html(brand_profiles, page_title)
        
        # Save to file
        try:
            with open(output_filename, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            print(f"\n✅ Competitive landscape report generated: {output_filename}")
            print(f"📊 Brands analyzed: {len(brand_profiles)}")
            print(f"📄 Open the HTML file in your browser to view the grid")
            
            return output_filename
            
        except Exception as e:
            print(f"Error saving report: {e}")
            return None

def main():
    """Example usage of the competitive grid generator"""
    
    # Financial services example (as shown in your requirements)
    financial_urls = [
        "https://www.tdameritrade.com",
        "https://www.edwardjones.com", 
        "https://www.schwab.com",
        "https://www.johnhancock.com",
        "https://www.prudential.com",
        "https://www.fidelity.com",
        "https://www.vanguard.com",
        "https://www.ml.com",
        "https://www.morganstanley.com",
        "https://www.ameriprise.com"
    ]
    
    generator = CompetitiveGridGenerator()
    
    # Generate the exact grid you specified
    output_file = generator.generate_competitive_landscape_report(
        urls=financial_urls,
        page_title="There is a huge opportunity in the category",
        output_filename="competitive_landscape_grid.html"
    )
    
    if output_file:
        print(f"\n🎉 Success! Your competitive landscape grid is ready!")
        print(f"📁 File location: {os.path.abspath(output_file)}")
        print(f"🌐 Open in browser to view the professional 5-row grid layout")

if __name__ == "__main__":
    main()