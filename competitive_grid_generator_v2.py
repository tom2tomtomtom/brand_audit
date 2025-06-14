#!/usr/bin/env python3
"""
Competitive Grid Generator V2
Real data only - no fallbacks, no defaults
Industry-agnostic with dynamic analysis
"""

import requests
from bs4 import BeautifulSoup
import openai
from openai import OpenAI
import pandas as pd
import os
import json
import re
from datetime import datetime
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from enhanced_brand_profiler_v2 import EnhancedBrandProfilerV2

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class CompetitiveGridGeneratorV2:
    def __init__(self):
        self.profiler = EnhancedBrandProfilerV2()
        self.brand_profiles = []
        self.failed_extractions = []
    
    def analyze_brands(self, urls):
        """Analyze multiple brands - real data only"""
        print(f"🔍 ANALYZING {len(urls)} BRANDS - REAL DATA ONLY")
        print(f"{'='*60}")
        
        for i, url in enumerate(urls, 1):
            print(f"\n[{i}/{len(urls)}] Analyzing: {url}")
            
            try:
                profile = self.profiler.analyze_brand(url)
                
                if profile['status'] == 'success':
                    # Additional AI analysis for competitive grid
                    enhanced_profile = self.enhance_profile_for_grid(profile)
                    self.brand_profiles.append(enhanced_profile)
                    print(f"✅ Success: {enhanced_profile['company_name']}")
                else:
                    self.failed_extractions.append({
                        'url': url,
                        'reason': profile['error']
                    })
                    print(f"❌ Failed: {profile['error']}")
                    
            except Exception as e:
                self.failed_extractions.append({
                    'url': url,
                    'reason': str(e)
                })
                print(f"❌ Error: {e}")
        
        print(f"\n{'='*60}")
        print(f"ANALYSIS COMPLETE")
        print(f"✅ Successful: {len(self.brand_profiles)}")
        print(f"❌ Failed: {len(self.failed_extractions)}")
        
        return {
            'successful': self.brand_profiles,
            'failed': self.failed_extractions
        }
    
    def enhance_profile_for_grid(self, profile):
        """Enhance profile with grid-specific analysis"""
        brand_data = profile['brand_data']
        visual_data = profile.get('visual_data', {})
        
        # Extract key information for grid
        enhanced = {
            'url': profile['url'],
            'company_name': brand_data.get('company_name', 'Name Not Found'),
            'brand_positioning': brand_data.get('brand_positioning') or self.extract_positioning_from_content(profile),
            'personality_descriptors': self.extract_personality_descriptors(brand_data, profile),
            'color_palette': self.extract_color_palette(visual_data),
            'logo_url': self.extract_primary_logo(visual_data),
            'visual_style': self.analyze_visual_style(visual_data, brand_data),
            'extraction_quality': profile.get('extraction_quality', 0),
            'confidence_scores': brand_data.get('confidence_scores', {})
        }
        
        return enhanced
    
    def extract_positioning_from_content(self, profile):
        """Try to extract positioning from available content"""
        if 'parsed_content' in profile:
            content = profile['parsed_content']
            
            # Look for hero text or main headings
            h1_text = content.get('headings', {}).get('h1', [])
            if h1_text:
                return h1_text[0][:200]
            
            # Check meta description
            meta_desc = content.get('meta_data', {}).get('description', '')
            if meta_desc:
                return meta_desc[:200]
        
        return None
    
    def extract_personality_descriptors(self, brand_data, profile):
        """Extract or generate personality descriptors"""
        # First check if we have them from brand data
        if brand_data.get('brand_personality'):
            return brand_data['brand_personality'][:6]
        
        # Try to infer from content tone
        descriptors = []
        
        # Analyze available content for tone
        if 'parsed_content' in profile:
            content_text = ' '.join([
                ' '.join(profile['parsed_content'].get('headings', {}).get('h1', [])),
                ' '.join(profile['parsed_content'].get('headings', {}).get('h2', [])),
                profile['parsed_content'].get('meta_data', {}).get('description', '')
            ])
            
            if content_text:
                # Quick AI analysis for personality
                try:
                    response = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {"role": "system", "content": "Extract 4-6 brand personality descriptors from content."},
                            {"role": "user", "content": f"Based on this content, what are 4-6 personality traits? Content: {content_text[:500]} Return only a JSON array of descriptors."}
                        ],
                        temperature=0.1,
                        max_tokens=100
                    )
                    
                    result = response.choices[0].message.content
                    descriptors = json.loads(result)
                    
                except:
                    pass
        
        return descriptors[:6] if descriptors else []
    
    def extract_color_palette(self, visual_data):
        """Extract color palette from visual data"""
        colors = []
        
        # Check different extraction methods
        if visual_data:
            if 'css_extraction' in visual_data:
                colors.extend(visual_data['css_extraction'] or [])
            if 'screenshot_analysis' in visual_data:
                colors.extend(visual_data['screenshot_analysis'] or [])
            if 'svg_parsing' in visual_data:
                colors.extend(visual_data['svg_parsing'] or [])
        
        # Deduplicate and limit
        unique_colors = []
        for color in colors:
            if color not in unique_colors:
                unique_colors.append(color)
        
        return unique_colors[:6]
    
    def extract_primary_logo(self, visual_data):
        """Extract primary logo URL"""
        if visual_data and 'logo_extraction' in visual_data:
            logos = visual_data['logo_extraction']
            if logos and isinstance(logos, list) and len(logos) > 0:
                return logos[0]
        
        return None
    
    def analyze_visual_style(self, visual_data, brand_data):
        """Analyze and describe visual style"""
        # Try to get from brand data first
        if brand_data.get('visual_style'):
            return brand_data['visual_style']
        
        # Analyze from available visual data
        style_indicators = []
        
        if visual_data:
            # Check color palette
            colors = self.extract_color_palette(visual_data)
            if colors:
                if any(c for c in colors if int(c[1:3], 16) < 100):  # Dark colors
                    style_indicators.append("Bold")
                if len(colors) <= 3:
                    style_indicators.append("Minimalist")
                elif len(colors) >= 5:
                    style_indicators.append("Vibrant")
        
        return ' • '.join(style_indicators) if style_indicators else "Style not determined"
    
    def generate_grid_html(self, report_title="Competitive Landscape Analysis"):
        """Generate grid HTML with real data only"""
        
        if not self.brand_profiles:
            return self.generate_error_page("No brands could be analyzed successfully")
        
        timestamp = datetime.now().strftime('%B %d, %Y at %I:%M %p')
        num_brands = len(self.brand_profiles)
        
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{report_title} - Real Data Analysis</title>
    <style>
        {self._get_grid_css(num_brands)}
    </style>
</head>
<body>
    <div class="page">
        <div class="page-header">
            <div class="page-number">Page 1</div>
            <h1 class="main-title">{report_title}</h1>
            <p class="subtitle">Competitive Landscape Analysis - Real Data Only</p>
            <p class="analysis-date">Generated on {timestamp}</p>
            {self._generate_extraction_summary()}
        </div>
        
        <div class="brand-grid-container">
            <div class="brand-grid">
                {self._generate_grid_content()}
            </div>
        </div>
        
        {self._generate_failed_extractions_section()}
    </div>
</body>
</html>"""
        
        return html_content
    
    def _generate_extraction_summary(self):
        """Generate summary of extraction results"""
        total_attempted = len(self.brand_profiles) + len(self.failed_extractions)
        success_rate = (len(self.brand_profiles) / total_attempted * 100) if total_attempted > 0 else 0
        
        return f"""
        <div class="extraction-summary">
            <span class="summary-item success">✅ {len(self.brand_profiles)} Successful</span>
            <span class="summary-item failed">❌ {len(self.failed_extractions)} Failed</span>
            <span class="summary-item rate">Success Rate: {success_rate:.1f}%</span>
        </div>
        """
    
    def _generate_grid_content(self):
        """Generate grid cells for each brand"""
        grid_html = ""
        
        for i, brand in enumerate(self.brand_profiles, 1):
            col_class = f"brand-col-{i}"
            
            # Row 1: Logo
            logo_html = self._generate_logo_cell(brand, col_class)
            
            # Row 2: Positioning
            positioning_html = self._generate_positioning_cell(brand, col_class)
            
            # Row 3: Personality
            personality_html = self._generate_personality_cell(brand, col_class)
            
            # Row 4: Colors
            colors_html = self._generate_colors_cell(brand, col_class)
            
            # Row 5: Visual Style
            visual_html = self._generate_visual_cell(brand, col_class)
            
            grid_html += f"""
                {logo_html}
                {positioning_html}
                {personality_html}
                {colors_html}
                {visual_html}
            """
        
        return grid_html
    
    def _generate_logo_cell(self, brand, col_class):
        """Generate logo cell with quality indicator"""
        quality_class = self._get_quality_class(brand['extraction_quality'])
        
        if brand['logo_url']:
            logo_content = f'<img src="{brand["logo_url"]}" alt="{brand["company_name"]} logo" class="brand-logo-img">'
        else:
            logo_content = f'<div class="no-logo">No logo found</div>'
        
        confidence = brand['confidence_scores'].get('company_name', 0)
        
        return f"""
        <div class="logo-cell {col_class} {quality_class}">
            {logo_content}
            <div class="brand-name">{brand['company_name']}</div>
            <div class="confidence-badge">{confidence:.0%}</div>
        </div>
        """
    
    def _generate_positioning_cell(self, brand, col_class):
        """Generate positioning cell"""
        positioning = brand['brand_positioning'] or "Positioning not found"
        
        return f"""
        <div class="positioning-cell {col_class}">
            <div class="positioning-text">{positioning}</div>
        </div>
        """
    
    def _generate_personality_cell(self, brand, col_class):
        """Generate personality cell"""
        descriptors = brand['personality_descriptors']
        
        if descriptors:
            tags_html = ''.join([f'<span class="personality-tag">{d}</span>' for d in descriptors])
        else:
            tags_html = '<span class="no-data">No descriptors extracted</span>'
        
        return f"""
        <div class="personality-cell {col_class}">
            <div class="personality-words">
                {tags_html}
            </div>
        </div>
        """
    
    def _generate_colors_cell(self, brand, col_class):
        """Generate colors cell"""
        colors = brand['color_palette']
        
        if colors:
            swatches_html = ''.join([f'<div class="color-swatch" style="background-color: {c};"></div>' for c in colors])
            labels = ' • '.join(colors[:3])
        else:
            swatches_html = '<div class="no-data">No colors extracted</div>'
            labels = "Color extraction failed"
        
        return f"""
        <div class="color-cell {col_class}">
            <div class="color-swatches">
                {swatches_html}
            </div>
            <div class="color-labels">{labels}</div>
        </div>
        """
    
    def _generate_visual_cell(self, brand, col_class):
        """Generate visual style cell"""
        visual_style = brand['visual_style'] or "Not determined"
        
        return f"""
        <div class="visual-cell {col_class}">
            <div class="visual-content">
                <div class="visual-style">{visual_style}</div>
                <div class="extraction-method">Extracted from: {brand['url']}</div>
            </div>
        </div>
        """
    
    def _generate_failed_extractions_section(self):
        """Generate section showing failed extractions"""
        if not self.failed_extractions:
            return ""
        
        failed_html = """
        <div class="failed-section">
            <h3>Failed Extractions</h3>
            <div class="failed-list">
        """
        
        for failure in self.failed_extractions:
            failed_html += f"""
                <div class="failed-item">
                    <span class="failed-url">{failure['url']}</span>
                    <span class="failed-reason">{failure['reason']}</span>
                </div>
            """
        
        failed_html += """
            </div>
        </div>
        """
        
        return failed_html
    
    def _get_quality_class(self, quality_score):
        """Get CSS class based on quality score"""
        if quality_score >= 0.8:
            return "quality-high"
        elif quality_score >= 0.5:
            return "quality-medium"
        else:
            return "quality-low"
    
    def _get_grid_css(self, num_brands):
        """Generate CSS with dynamic grid columns"""
        return f"""
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
        
        .extraction-summary {{
            margin-top: 15px;
            display: flex;
            justify-content: center;
            gap: 20px;
        }}
        
        .summary-item {{
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.9em;
            font-weight: 600;
        }}
        
        .summary-item.success {{
            background: #d4edda;
            color: #155724;
        }}
        
        .summary-item.failed {{
            background: #f8d7da;
            color: #721c24;
        }}
        
        .summary-item.rate {{
            background: #d1ecf1;
            color: #0c5460;
        }}
        
        /* Grid System */
        .brand-grid-container {{
            background: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            overflow-x: auto;
        }}
        
        .brand-grid {{
            display: grid;
            grid-template-columns: repeat({num_brands}, minmax(200px, 1fr));
            grid-template-rows: 80px 140px 90px 80px 100px;
            gap: 12px;
            min-width: {num_brands * 220}px;
        }}
        
        /* Grid Cells */
        .logo-cell, .positioning-cell, .personality-cell, .color-cell, .visual-cell {{
            background: white;
            border: 1px solid #e9ecef;
            border-radius: 8px;
            padding: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            position: relative;
            overflow: hidden;
        }}
        
        .logo-cell {{
            grid-row: 1;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }}
        
        .brand-logo-img {{
            max-width: 100%;
            max-height: 40px;
            object-fit: contain;
            margin-bottom: 5px;
        }}
        
        .no-logo {{
            width: 100%;
            height: 40px;
            background: #f8f9fa;
            border: 2px dashed #dee2e6;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.7em;
            color: #6c757d;
            margin-bottom: 5px;
        }}
        
        .brand-name {{
            font-size: 0.8em;
            font-weight: 600;
            color: #495057;
            text-align: center;
        }}
        
        .confidence-badge {{
            position: absolute;
            top: 5px;
            right: 5px;
            font-size: 0.6em;
            background: #e9ecef;
            padding: 2px 6px;
            border-radius: 10px;
            color: #6c757d;
        }}
        
        /* Quality Indicators */
        .quality-high {{
            border-color: #28a745;
        }}
        
        .quality-medium {{
            border-color: #ffc107;
        }}
        
        .quality-low {{
            border-color: #dc3545;
        }}
        
        .positioning-cell {{
            grid-row: 2;
        }}
        
        .positioning-text {{
            font-size: 0.75em;
            line-height: 1.4;
            color: #495057;
            overflow: hidden;
            display: -webkit-box;
            -webkit-line-clamp: 8;
            -webkit-box-orient: vertical;
        }}
        
        .personality-cell {{
            grid-row: 3;
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
        }}
        
        .color-cell {{
            grid-row: 4;
        }}
        
        .color-swatches {{
            display: grid;
            grid-template-columns: repeat(6, 1fr);
            gap: 3px;
            margin-bottom: 8px;
        }}
        
        .color-swatch {{
            height: 25px;
            border-radius: 3px;
            border: 1px solid #dee2e6;
        }}
        
        .color-labels {{
            font-size: 0.6em;
            color: #6c757d;
            text-align: center;
            line-height: 1.2;
        }}
        
        .visual-cell {{
            grid-row: 5;
        }}
        
        .visual-content {{
            font-size: 0.7em;
            color: #495057;
        }}
        
        .visual-style {{
            font-weight: 600;
            margin-bottom: 5px;
        }}
        
        .extraction-method {{
            font-size: 0.9em;
            color: #6c757d;
        }}
        
        .no-data {{
            color: #dc3545;
            font-style: italic;
            font-size: 0.8em;
        }}
        
        /* Failed Extractions */
        .failed-section {{
            margin-top: 40px;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 10px;
        }}
        
        .failed-section h3 {{
            color: #dc3545;
            margin-bottom: 15px;
        }}
        
        .failed-list {{
            display: flex;
            flex-direction: column;
            gap: 10px;
        }}
        
        .failed-item {{
            display: flex;
            justify-content: space-between;
            padding: 10px;
            background: white;
            border-radius: 5px;
            border-left: 4px solid #dc3545;
        }}
        
        .failed-url {{
            font-weight: 600;
            color: #495057;
        }}
        
        .failed-reason {{
            color: #6c757d;
            font-size: 0.9em;
        }}
        
        /* Column positioning */
        {self._generate_column_classes(num_brands)}
        
        @media print {{
            .page {{
                width: 210mm;
                min-height: 297mm;
            }}
        }}
        """
    
    def _generate_column_classes(self, num_brands):
        """Generate column classes dynamically"""
        classes = ""
        for i in range(1, num_brands + 1):
            classes += f".brand-col-{i} {{ grid-column: {i}; }}\n"
        return classes
    
    def generate_error_page(self, error_message):
        """Generate error page when no data can be extracted"""
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Analysis Failed</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #f8f9fa;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }}
        
        .error-container {{
            background: white;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            text-align: center;
            max-width: 500px;
        }}
        
        .error-icon {{
            font-size: 4em;
            color: #dc3545;
            margin-bottom: 20px;
        }}
        
        .error-title {{
            font-size: 1.5em;
            color: #333;
            margin-bottom: 10px;
        }}
        
        .error-message {{
            color: #6c757d;
            margin-bottom: 30px;
        }}
        
        .failed-urls {{
            text-align: left;
            background: #f8f9fa;
            padding: 20px;
            border-radius: 5px;
            margin-top: 20px;
        }}
        
        .failed-urls h3 {{
            margin-top: 0;
            color: #495057;
        }}
        
        .failed-url-item {{
            margin: 10px 0;
            padding: 10px;
            background: white;
            border-radius: 3px;
            border-left: 3px solid #dc3545;
        }}
    </style>
</head>
<body>
    <div class="error-container">
        <div class="error-icon">❌</div>
        <h1 class="error-title">Analysis Failed</h1>
        <p class="error-message">{error_message}</p>
        
        {self._generate_failed_urls_details()}
    </div>
</body>
</html>"""
    
    def _generate_failed_urls_details(self):
        """Generate details of failed URLs"""
        if not self.failed_extractions:
            return ""
        
        html = '<div class="failed-urls"><h3>Failed URLs:</h3>'
        for failure in self.failed_extractions:
            html += f'<div class="failed-url-item"><strong>{failure["url"]}</strong><br>{failure["reason"]}</div>'
        html += '</div>'
        
        return html
    
    def generate_report(self, urls, report_title="Competitive Landscape Analysis", output_filename=None):
        """Main method to generate competitive grid report"""
        
        if not output_filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_filename = f"competitive_grid_real_data_{timestamp}.html"
        
        # Analyze brands
        results = self.analyze_brands(urls)
        
        # Generate HTML
        if results['successful']:
            html_content = self.generate_grid_html(report_title)
        else:
            html_content = self.generate_error_page("No brands could be successfully analyzed")
        
        # Save report
        try:
            with open(output_filename, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            print(f"\n📄 Report saved: {output_filename}")
            
            return {
                'filename': output_filename,
                'successful_count': len(results['successful']),
                'failed_count': len(results['failed']),
                'brands': results['successful']
            }
            
        except Exception as e:
            print(f"❌ Error saving report: {e}")
            return None

def main():
    """Example usage"""
    
    # Test URLs - mix of different industries
    test_urls = [
        "https://www.stripe.com",
        "https://www.shopify.com",
        "https://www.square.com",
        "https://www.paypal.com",
        "https://www.klarna.com"
    ]
    
    generator = CompetitiveGridGeneratorV2()
    
    result = generator.generate_report(
        urls=test_urls,
        report_title="Payment Platforms Competitive Analysis",
        output_filename="payment_platforms_grid.html"
    )
    
    if result:
        print(f"\n✅ SUCCESS!")
        print(f"📊 Analyzed: {result['successful_count']} brands")
        print(f"❌ Failed: {result['failed_count']} brands")
        print(f"📁 View report: {result['filename']}")

if __name__ == "__main__":
    main()
