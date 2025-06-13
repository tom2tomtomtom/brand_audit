#!/usr/bin/env python3
"""
Comprehensive Competitive Intelligence Report Generator
Generates multi-page strategic competitive analysis reports with deep brand insights
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
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class ComprehensiveReportGenerator:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.driver = None
        self.brand_profiles = []
    
    def fetch_page(self, url):
        """Fetch webpage content with error handling"""
        try:
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(f"Failed to retrieve the page: {url} -- {e}")
            return None
    
    def extract_comprehensive_brand_data(self, url):
        """Extract comprehensive brand data for deep analysis"""
        print(f"🔍 COMPREHENSIVE ANALYSIS: {url}")
        
        html_content = self.fetch_page(url)
        if not html_content:
            return None
        
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Extract comprehensive content sections
        content_sections = self._extract_all_content_sections(soup)
        
        # Get brand strategy analysis
        brand_strategy = self._analyze_brand_strategy(html_content, url, content_sections)
        
        # Get brand architecture
        brand_architecture = self._analyze_brand_architecture(html_content, url, content_sections)
        
        # Get visual analysis
        visual_analysis = self._analyze_visual_system(html_content, url, soup)
        
        # Get logos and colors
        logos = self._extract_logos_comprehensive(html_content, url)
        colors = self._extract_colors_comprehensive(html_content, url)
        
        # Capture screenshot
        screenshot = self._capture_screenshot_proper(url)
        
        # Compile comprehensive profile
        brand_profile = {
            "url": url,
            "company_name": brand_strategy.get("company_name", "Unknown Company"),
            "brand_strategy": brand_strategy,
            "brand_architecture": brand_architecture,
            "visual_analysis": visual_analysis,
            "logos": logos,
            "color_palette": colors,
            "screenshot": screenshot,
            "content_sections": content_sections,
            "analysis_timestamp": datetime.now().isoformat()
        }
        
        print(f"   ✅ COMPREHENSIVE ANALYSIS COMPLETE: {brand_profile['company_name']}")
        return brand_profile
    
    def _extract_all_content_sections(self, soup):
        """Extract all content sections for comprehensive analysis"""
        sections = {}
        
        # Hero/Header content
        sections['hero'] = []
        hero_selectors = ['h1', '.hero', '[class*="hero"]', '.banner', '.jumbotron', '.header-content']
        for selector in hero_selectors:
            elements = soup.select(selector)
            for elem in elements[:5]:
                text = elem.get_text().strip()
                if text and len(text) > 10:
                    sections['hero'].append(text)
        
        # Navigation and menu structure
        sections['navigation'] = []
        nav_elements = soup.select('nav a, .nav a, .menu a, .navigation a, header a')
        for nav in nav_elements[:15]:
            text = nav.get_text().strip()
            if text and len(text) > 1:
                sections['navigation'].append(text)
        
        # Product/Service information
        sections['products'] = []
        product_selectors = ['.product', '[class*="product"]', '.service', '[class*="service"]', '.solution', '[class*="solution"]']
        for selector in product_selectors:
            elements = soup.select(selector)
            for elem in elements[:8]:
                text = elem.get_text().strip()
                if len(text) > 30:
                    sections['products'].append(text[:300])
        
        # About/Company information
        sections['about'] = []
        about_selectors = ['[class*="about"]', '[class*="company"]', '[class*="mission"]', '[class*="vision"]']
        for selector in about_selectors:
            elements = soup.select(selector)
            for elem in elements[:5]:
                text = elem.get_text().strip()
                if len(text) > 50:
                    sections['about'].append(text[:500])
        
        # Features and benefits
        sections['features'] = []
        feature_selectors = ['.feature', '[class*="feature"]', '.benefit', '[class*="benefit"]', '.capability']
        for selector in feature_selectors:
            elements = soup.select(selector)
            for elem in elements[:10]:
                text = elem.get_text().strip()
                if len(text) > 20:
                    sections['features'].append(text[:250])
        
        # Key messaging and value propositions
        sections['messaging'] = []
        msg_selectors = ['h2', 'h3', '.headline', '.tagline', '.value-prop', '[class*="message"]']
        for selector in msg_selectors:
            elements = soup.select(selector)
            for elem in elements[:12]:
                text = elem.get_text().strip()
                if len(text) > 15 and len(text) < 200:
                    sections['messaging'].append(text)
        
        return sections
    
    def _analyze_brand_strategy(self, html_content, url, content_sections):
        """Analyze brand strategy using AI"""
        context = f"""
        URL: {url}
        
        HERO CONTENT: {' | '.join(content_sections.get('hero', [])[:3])}
        
        KEY NAVIGATION: {' | '.join(content_sections.get('navigation', [])[:10])}
        
        PRODUCT/SERVICES: {' | '.join(content_sections.get('products', [])[:3])}
        
        ABOUT/COMPANY: {' | '.join(content_sections.get('about', [])[:2])}
        
        KEY MESSAGING: {' | '.join(content_sections.get('messaging', [])[:8])}
        """
        
        messages = [
            {"role": "system", "content": "You are a senior brand strategist analyzing companies for comprehensive competitive intelligence. Provide detailed strategic insights."},
            {"role": "user", "content": f"""
            BRAND STRATEGY ANALYSIS REQUEST
            
            Analyze this company's brand strategy and positioning based on their website content.
            
            {context}
            
            Return JSON with detailed analysis:
            {{
                "company_name": "Official company name",
                "why_framework": {{
                    "purpose": "Why the company exists (mission/purpose)",
                    "belief": "Core belief or vision driving the company",
                    "impact": "Impact they want to make in the world"
                }},
                "how_framework": {{
                    "approach": "How they deliver value (methodology/approach)",
                    "differentiators": ["Key", "differentiating", "factors"],
                    "capabilities": ["Core", "capabilities", "and", "strengths"]
                }},
                "what_framework": {{
                    "products_services": ["Main", "products", "or", "services"],
                    "value_propositions": ["Key", "value", "propositions"],
                    "offerings": "Description of core offerings"
                }},
                "who_framework": {{
                    "target_audience": "Primary target audience description",
                    "customer_segments": ["Customer", "segment", "types"],
                    "user_personas": "Description of ideal customers"
                }},
                "messaging_analysis": {{
                    "brand_voice": "Communication style and tone description",
                    "key_messages": ["Primary", "message", "themes"],
                    "value_messaging": ["Core", "value", "messages"],
                    "positioning_statement": "Primary positioning statement",
                    "taglines": ["Key", "taglines", "or", "slogans"]
                }},
                "brand_personality": {{
                    "personality_traits": ["Six", "specific", "brand", "personality", "descriptors", "based", "on", "content"],
                    "tone_characteristics": ["Communication", "tone", "characteristics"],
                    "brand_archetype": "Primary brand archetype (Hero, Sage, Creator, etc.)"
                }}
            }}
            
            Base your analysis on the actual content provided. Be specific and strategic.
            """
            }
        ]
        
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                temperature=0.1,
                max_tokens=2000
            )
            
            content = response.choices[0].message.content.strip()
            content = re.sub(r"```(json)?", "", content).strip()
            
            if '{' in content:
                start = content.find('{')
                end = content.rfind('}') + 1
                json_content = content[start:end]
                return json.loads(json_content)
            else:
                raise ValueError("No JSON found in response")
                
        except Exception as e:
            print(f"     ❌ Brand strategy analysis failed: {e}")
            return self._get_default_brand_strategy()
    
    def _analyze_brand_architecture(self, html_content, url, content_sections):
        """Analyze brand architecture and portfolio"""
        context = f"""
        URL: {url}
        
        NAVIGATION STRUCTURE: {' | '.join(content_sections.get('navigation', [])[:15])}
        
        PRODUCTS/SERVICES: {' | '.join(content_sections.get('products', [])[:5])}
        
        FEATURES/CAPABILITIES: {' | '.join(content_sections.get('features', [])[:8])}
        """
        
        messages = [
            {"role": "system", "content": "You are a brand architecture specialist analyzing company portfolios and organizational structure."},
            {"role": "user", "content": f"""
            BRAND ARCHITECTURE ANALYSIS
            
            Analyze this company's brand architecture and portfolio organization.
            
            {context}
            
            Return JSON:
            {{
                "portfolio_overview": {{
                    "brand_type": "Master brand, Endorsed brands, or House of brands",
                    "portfolio_scope": "Description of overall portfolio breadth",
                    "brand_relationship": "How sub-brands relate to master brand"
                }},
                "product_organization": {{
                    "main_categories": ["Primary", "product", "categories"],
                    "service_lines": ["Service", "line", "offerings"],
                    "solution_areas": ["Solution", "focus", "areas"]
                }},
                "subsidiary_brands": {{
                    "sub_brands": ["Any", "subsidiary", "brands", "identified"],
                    "product_brands": ["Product-specific", "brand", "names"],
                    "service_brands": ["Service-specific", "brands"]
                }},
                "organizational_structure": {{
                    "business_units": ["Identifiable", "business", "units"],
                    "market_segments": ["Market", "segments", "served"],
                    "geographic_focus": ["Geographic", "markets", "or", "global"]
                }}
            }}
            
            Extract real information from the content provided.
            """
            }
        ]
        
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                temperature=0.1,
                max_tokens=1500
            )
            
            content = response.choices[0].message.content.strip()
            content = re.sub(r"```(json)?", "", content).strip()
            
            if '{' in content:
                start = content.find('{')
                end = content.rfind('}') + 1
                json_content = content[start:end]
                return json.loads(json_content)
            else:
                raise ValueError("No JSON found in response")
                
        except Exception as e:
            print(f"     ❌ Brand architecture analysis failed: {e}")
            return self._get_default_brand_architecture()
    
    def _analyze_visual_system(self, html_content, url, soup):
        """Analyze visual design system"""
        # Extract typography information
        typography = self._analyze_typography(soup)
        
        # Analyze design patterns
        design_patterns = self._analyze_design_patterns(soup)
        
        # Get layout structure
        layout_analysis = self._analyze_layout_structure(soup)
        
        return {
            "typography": typography,
            "design_patterns": design_patterns,
            "layout_analysis": layout_analysis,
            "visual_hierarchy": self._analyze_visual_hierarchy(soup)
        }
    
    def _analyze_typography(self, soup):
        """Analyze typography usage"""
        # Get all heading elements
        headings = {
            'h1': [h.get_text().strip() for h in soup.find_all('h1')[:3]],
            'h2': [h.get_text().strip() for h in soup.find_all('h2')[:5]],
            'h3': [h.get_text().strip() for h in soup.find_all('h3')[:5]]
        }
        
        # Extract font families from styles
        font_families = set()
        for element in soup.find_all(style=True):
            style = element.get('style', '')
            font_match = re.search(r'font-family:\s*([^;]+)', style)
            if font_match:
                font_families.add(font_match.group(1).strip())
        
        return {
            "heading_structure": headings,
            "font_families": list(font_families)[:5],
            "typography_scale": len([h for h in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])])
        }
    
    def _analyze_design_patterns(self, soup):
        """Analyze design patterns and components"""
        return {
            "buttons": len(soup.select('button, .btn, [class*="button"]')),
            "cards": len(soup.select('.card, [class*="card"]')),
            "icons": len(soup.select('svg, .icon, [class*="icon"]')),
            "images": len(soup.select('img')),
            "forms": len(soup.select('form')),
            "navigation_elements": len(soup.select('nav, .nav, .navigation'))
        }
    
    def _analyze_layout_structure(self, soup):
        """Analyze page layout structure"""
        return {
            "has_header": bool(soup.select('header')),
            "has_footer": bool(soup.select('footer')),
            "has_sidebar": bool(soup.select('.sidebar, [class*="sidebar"]')),
            "grid_usage": len(soup.select('[class*="grid"], [class*="col-"]')),
            "flex_usage": len(soup.select('[class*="flex"], [class*="d-flex"]'))
        }
    
    def _analyze_visual_hierarchy(self, soup):
        """Analyze visual hierarchy elements"""
        return {
            "hero_sections": len(soup.select('.hero, [class*="hero"]')),
            "call_to_action": len(soup.select('.cta, [class*="cta"], .call-to-action')),
            "feature_sections": len(soup.select('.feature, [class*="feature"]')),
            "testimonials": len(soup.select('.testimonial, [class*="testimonial"]'))
        }
    
    def _extract_logos_comprehensive(self, html_content, base_url):
        """Extract logos with comprehensive search"""
        soup = BeautifulSoup(html_content, 'html.parser')
        logo_urls = []
        
        logo_selectors = [
            'img[alt*="logo" i]',
            'img[src*="logo" i]', 
            'img[class*="logo" i]',
            '.logo img',
            '.header img',
            '.navbar img',
            '.brand img',
            'header img',
            '.site-logo img',
            '.company-logo img'
        ]
        
        for selector in logo_selectors:
            elements = soup.select(selector)
            for img in elements:
                src = img.get('src') or img.get('data-src')
                if src and self._is_likely_logo(src, img.get('alt', '')):
                    full_url = urljoin(base_url, src)
                    if full_url not in logo_urls:
                        logo_urls.append(full_url)
        
        return logo_urls[:3]
    
    def _is_likely_logo(self, src, alt_text):
        """Determine if an image is likely a logo"""
        logo_indicators = ['logo', 'brand', 'header']
        src_lower = src.lower()
        alt_lower = alt_text.lower()
        
        for indicator in logo_indicators:
            if indicator in src_lower or indicator in alt_lower:
                return True
        
        avoid_patterns = ['banner', 'hero', 'background', 'icon', 'social']
        for pattern in avoid_patterns:
            if pattern in src_lower:
                return False
                
        return False
    
    def _extract_colors_comprehensive(self, html_content, url):
        """Extract colors from multiple sources"""
        soup = BeautifulSoup(html_content, 'html.parser')
        all_colors = set()
        
        # Extract from inline styles
        for element in soup.find_all(style=True):
            style = element.get('style', '')
            colors = re.findall(r'#[0-9a-fA-F]{6}|#[0-9a-fA-F]{3}|rgb\([^)]+\)', style)
            all_colors.update(colors)
        
        # Extract from style tags
        for style_tag in soup.find_all('style'):
            css_content = style_tag.get_text()
            colors = re.findall(r'#[0-9a-fA-F]{6}|#[0-9a-fA-F]{3}|rgb\([^)]+\)', css_content)
            all_colors.update(colors)
        
        # Extract from linked CSS files
        for link in soup.find_all('link', rel='stylesheet'):
            href = link.get('href')
            if href:
                css_url = urljoin(url, href)
                try:
                    css_response = self.session.get(css_url, timeout=10)
                    if css_response.status_code == 200:
                        css_colors = re.findall(r'#[0-9a-fA-F]{6}|#[0-9a-fA-F]{3}|rgb\([^)]+\)', css_response.text)
                        all_colors.update(css_colors)
                except:
                    pass
        
        return self._process_colors(list(all_colors))
    
    def _process_colors(self, color_list):
        """Process and cluster colors to get dominant palette"""
        processed_colors = []
        
        for color in color_list:
            try:
                if color.startswith('#'):
                    if len(color) == 4:
                        color = '#' + ''.join([c*2 for c in color[1:]])
                    rgb = tuple(int(color[i:i+2], 16) for i in (1, 3, 5))
                elif color.startswith('rgb'):
                    rgb_values = re.findall(r'\d+', color)
                    rgb = tuple(int(val) for val in rgb_values[:3])
                else:
                    continue
                
                if all(0 <= val <= 255 for val in rgb) and not (all(val > 240 for val in rgb) or all(val < 15 for val in rgb)):
                    processed_colors.append(rgb)
            except:
                continue
        
        if not processed_colors:
            return ['#666666', '#999999', '#cccccc', '#e9ecef', '#f8f9fa', '#ffffff']
        
        try:
            colors_array = np.array(processed_colors)
            n_colors = min(6, len(set(map(tuple, processed_colors))))
            
            if n_colors > 1:
                kmeans = KMeans(n_clusters=n_colors, random_state=42, n_init=10)
                kmeans.fit(colors_array)
                dominant_colors = kmeans.cluster_centers_.astype(int)
            else:
                dominant_colors = colors_array[:6]
            
            hex_colors = []
            for rgb in dominant_colors:
                hex_color = '#{:02x}{:02x}{:02x}'.format(int(rgb[0]), int(rgb[1]), int(rgb[2]))
                hex_colors.append(hex_color)
            
            return hex_colors[:6]
        except:
            return ['#666666', '#999999', '#cccccc', '#e9ecef', '#f8f9fa', '#ffffff']
    
    def _capture_screenshot_proper(self, url):
        """Capture screenshot with proper setup"""
        try:
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--window-size=1200,800')
            
            driver = webdriver.Chrome(options=chrome_options)
            driver.get(url)
            time.sleep(5)
            
            # Scroll and capture
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight/3);")
            time.sleep(2)
            driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(2)
            
            screenshot = driver.get_screenshot_as_png()
            screenshot_b64 = base64.b64encode(screenshot).decode('utf-8')
            
            driver.quit()
            return f"data:image/png;base64,{screenshot_b64}"
            
        except Exception as e:
            print(f"     ❌ Screenshot failed: {e}")
            try:
                if 'driver' in locals():
                    driver.quit()
            except:
                pass
            return None
    
    def _get_default_brand_strategy(self):
        """Default brand strategy structure"""
        return {
            "company_name": "Unknown Company",
            "why_framework": {
                "purpose": "Company purpose not clearly defined",
                "belief": "Core belief not identified",
                "impact": "Impact statement not found"
            },
            "how_framework": {
                "approach": "Approach not clearly defined",
                "differentiators": ["Professional", "Reliable"],
                "capabilities": ["Quality services"]
            },
            "what_framework": {
                "products_services": ["Business solutions"],
                "value_propositions": ["Quality products"],
                "offerings": "Core offerings not clearly defined"
            },
            "who_framework": {
                "target_audience": "General business customers",
                "customer_segments": ["Business customers"],
                "user_personas": "Professional users"
            },
            "messaging_analysis": {
                "brand_voice": "Professional and informative",
                "key_messages": ["Quality solutions"],
                "value_messaging": ["Reliable service"],
                "positioning_statement": "Professional service provider",
                "taglines": ["Quality first"]
            },
            "brand_personality": {
                "personality_traits": ["Professional", "Reliable", "Modern", "Trustworthy", "Quality", "Service"],
                "tone_characteristics": ["Professional", "Informative"],
                "brand_archetype": "The Sage"
            }
        }
    
    def _get_default_brand_architecture(self):
        """Default brand architecture structure"""
        return {
            "portfolio_overview": {
                "brand_type": "Master brand",
                "portfolio_scope": "Single brand offering",
                "brand_relationship": "Unified brand approach"
            },
            "product_organization": {
                "main_categories": ["Core services"],
                "service_lines": ["Professional services"],
                "solution_areas": ["Business solutions"]
            },
            "subsidiary_brands": {
                "sub_brands": [],
                "product_brands": [],
                "service_brands": []
            },
            "organizational_structure": {
                "business_units": ["Main business"],
                "market_segments": ["Business market"],
                "geographic_focus": ["Local market"]
            }
        }
    
    def generate_comprehensive_report(self, urls, report_title="Competitive Intelligence Report", output_filename=None):
        """Generate comprehensive multi-page competitive intelligence report"""
        
        if not output_filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_filename = f"competitive_intelligence_report_{timestamp}.html"
        
        print(f"🏢 Generating Comprehensive Competitive Intelligence Report...")
        print(f"📊 Analyzing {len(urls)} brands for deep strategic insights...")
        
        # Analyze all brands comprehensively
        self.brand_profiles = []
        seen_companies = set()
        
        try:
            for i, url in enumerate(urls, 1):
                print(f"\n🔍 [{i}/{len(urls)}] Analyzing: {url}")
                try:
                    profile = self.extract_comprehensive_brand_data(url)
                    if profile:
                        company_name = profile['company_name']
                        if company_name not in seen_companies:
                            self.brand_profiles.append(profile)
                            seen_companies.add(company_name)
                            print(f"✅ Complete analysis: {company_name}")
                        else:
                            print(f"⚠️ Skipped duplicate: {company_name}")
                    else:
                        print(f"❌ Failed to analyze: {url}")
                except Exception as e:
                    print(f"❌ Error analyzing {url}: {e}")
        finally:
            if self.driver:
                self.driver.quit()
        
        if not self.brand_profiles:
            print("❌ No brands were successfully analyzed")
            return None
        
        # Generate comprehensive multi-page report
        print(f"\n📄 Generating comprehensive report with {len(self.brand_profiles)} brands...")
        html_content = self._generate_multi_page_report(report_title)
        
        # Save report
        try:
            with open(output_filename, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            print(f"\n🎉 COMPREHENSIVE REPORT GENERATED!")
            print(f"📁 File: {output_filename}")
            print(f"📊 Brands analyzed: {len(self.brand_profiles)}")
            print(f"📄 Pages: {2 + len(self.brand_profiles) + 2}")  # Overview + Individual pages + Comparison + Opportunity
            print(f"🌐 Open in browser for complete multi-page competitive intelligence")
            
            return output_filename
            
        except Exception as e:
            print(f"❌ Error saving report: {e}")
            return None
    
    def _generate_multi_page_report(self, report_title):
        """Generate the complete multi-page HTML report"""
        
        # Calculate total pages
        total_pages = 2 + len(self.brand_profiles) + 2  # Overview + Individual + Comparison + Opportunity
        
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{report_title} - Comprehensive Analysis</title>
    <style>
        {self._get_comprehensive_css()}
    </style>
    <script>
        {self._get_navigation_js()}
    </script>
</head>
<body>
"""
        
        # Page 1: Competitive Landscape Overview
        html_content += self._generate_overview_page(report_title, 1, total_pages)
        
        # Pages 2-N+1: Individual Brand Deep-Dive Pages
        for i, brand in enumerate(self.brand_profiles, 2):
            html_content += self._generate_brand_deep_dive_page(brand, i, total_pages)
        
        # Page N+2: Cross-Brand Comparison Matrix
        html_content += self._generate_comparison_matrix_page(len(self.brand_profiles) + 2, total_pages)
        
        # Page N+3: Market Opportunity Analysis
        html_content += self._generate_opportunity_analysis_page(total_pages, total_pages)
        
        html_content += """
</body>
</html>"""
        
        return html_content
    
    def _get_comprehensive_css(self):
        """Get comprehensive CSS for multi-page report"""
        return """
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            background: #ffffff;
        }
        
        /* Page Structure */
        .page {
            width: 210mm;
            min-height: 297mm;
            background: white;
            margin: 0 auto;
            padding: 20mm;
            box-shadow: 0 0 20px rgba(0,0,0,0.1);
            margin-bottom: 20px;
            page-break-after: always;
            position: relative;
        }
        
        .page-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 30px;
            padding-bottom: 15px;
            border-bottom: 2px solid #e9ecef;
        }
        
        .page-number {
            font-size: 0.9em;
            color: #6c757d;
            background: #f8f9fa;
            padding: 8px 12px;
            border-radius: 4px;
            border: 1px solid #e9ecef;
        }
        
        .page-title {
            font-size: 1.8em;
            font-weight: 700;
            color: #2c3e50;
        }
        
        .page-footer {
            position: absolute;
            bottom: 15mm;
            left: 20mm;
            right: 20mm;
            text-align: center;
            font-size: 0.8em;
            color: #6c757d;
            border-top: 1px solid #e9ecef;
            padding-top: 10px;
        }
        
        /* Navigation */
        .page-navigation {
            margin-bottom: 20px;
            text-align: center;
        }
        
        .nav-button {
            display: inline-block;
            padding: 8px 16px;
            margin: 0 5px;
            background: #007bff;
            color: white;
            text-decoration: none;
            border-radius: 4px;
            font-size: 0.9em;
            cursor: pointer;
        }
        
        .nav-button:hover {
            background: #0056b3;
        }
        
        .nav-button.disabled {
            background: #6c757d;
            cursor: not-allowed;
        }
        
        /* Overview Page Styles */
        .main-title {
            font-size: 3em;
            font-weight: 700;
            color: #2c3e50;
            margin-bottom: 15px;
            text-align: center;
            line-height: 1.2;
        }
        
        .subtitle {
            font-size: 1.3em;
            color: #6c757d;
            margin-bottom: 10px;
            text-align: center;
        }
        
        .analysis-date {
            font-size: 1em;
            color: #8e9ba8;
            text-align: center;
            margin-bottom: 40px;
        }
        
        /* Brand Grid */
        .brand-grid-container {
            background: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            overflow: hidden;
            margin-bottom: 30px;
        }
        
        .brand-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            grid-template-rows: 70px 140px 90px 70px 180px;
            gap: 12px;
            min-height: 550px;
        }
        
        .logo-cell {
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
        }
        
        .brand-logo-img {
            max-width: 100%;
            max-height: 35px;
            object-fit: contain;
            margin-bottom: 5px;
        }
        
        .brand-name {
            font-size: 0.7em;
            font-weight: 600;
            color: #495057;
            text-align: center;
        }
        
        .positioning-cell {
            grid-row: 2;
            background: white;
            border: 1px solid #e9ecef;
            border-radius: 8px;
            padding: 12px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            overflow: hidden;
        }
        
        .positioning-text {
            font-size: 0.75em;
            line-height: 1.3;
            color: #495057;
            overflow: hidden;
            display: -webkit-box;
            -webkit-line-clamp: 8;
            -webkit-box-orient: vertical;
        }
        
        .personality-cell {
            grid-row: 3;
            background: white;
            border: 1px solid #e9ecef;
            border-radius: 8px;
            padding: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            display: flex;
            flex-direction: column;
        }
        
        .personality-words {
            display: flex;
            flex-wrap: wrap;
            gap: 4px;
        }
        
        .personality-tag {
            background: #f8f9fa;
            border: 1px solid #e9ecef;
            border-radius: 12px;
            padding: 3px 8px;
            font-size: 0.65em;
            font-weight: 500;
            color: #495057;
            white-space: nowrap;
        }
        
        .color-cell {
            grid-row: 4;
            background: white;
            border: 1px solid #e9ecef;
            border-radius: 8px;
            padding: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            display: flex;
            flex-direction: column;
        }
        
        .color-swatches {
            display: grid;
            grid-template-columns: repeat(6, 1fr);
            gap: 3px;
            flex-grow: 1;
        }
        
        .color-swatch {
            height: 25px;
            border-radius: 3px;
            border: 1px solid #dee2e6;
        }
        
        .visual-cell {
            grid-row: 5;
            background: white;
            border: 1px solid #e9ecef;
            border-radius: 8px;
            padding: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            display: flex;
            flex-direction: column;
        }
        
        .screenshot-container {
            flex-grow: 1;
            background: #f8f9fa;
            border-radius: 4px;
            border: 1px solid #e9ecef;
            overflow: hidden;
            position: relative;
            margin-bottom: 6px;
        }
        
        /* Deep Dive Page Styles */
        .section {
            margin-bottom: 40px;
            page-break-inside: avoid;
        }
        
        .section-title {
            font-size: 1.5em;
            font-weight: 700;
            color: #2c3e50;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid #e9ecef;
        }
        
        .subsection {
            margin-bottom: 25px;
        }
        
        .subsection-title {
            font-size: 1.2em;
            font-weight: 600;
            color: #495057;
            margin-bottom: 15px;
        }
        
        .framework-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 20px;
            margin-bottom: 20px;
        }
        
        .framework-item {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
            border-left: 4px solid #007bff;
        }
        
        .framework-label {
            font-weight: 600;
            color: #2c3e50;
            margin-bottom: 8px;
        }
        
        .framework-content {
            color: #495057;
            font-size: 0.95em;
        }
        
        .tag-list {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-top: 10px;
        }
        
        .tag {
            background: #e9ecef;
            padding: 5px 10px;
            border-radius: 15px;
            font-size: 0.85em;
            color: #495057;
        }
        
        .brand-overview {
            background: linear-gradient(135deg, #f8f9fa, #e9ecef);
            padding: 25px;
            border-radius: 10px;
            margin-bottom: 30px;
            border: 1px solid #dee2e6;
        }
        
        .brand-overview h2 {
            color: #2c3e50;
            margin-bottom: 15px;
        }
        
        /* Comparison Matrix Styles */
        .comparison-table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 30px;
            font-size: 0.9em;
        }
        
        .comparison-table th,
        .comparison-table td {
            border: 1px solid #dee2e6;
            padding: 12px;
            text-align: left;
            vertical-align: top;
        }
        
        .comparison-table th {
            background: #f8f9fa;
            font-weight: 600;
            color: #2c3e50;
        }
        
        .comparison-table tr:nth-child(even) {
            background: #f8f9fa;
        }
        
        /* Opportunity Analysis Styles */
        .opportunity-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 25px;
            margin-bottom: 30px;
        }
        
        .opportunity-card {
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            border-left: 5px solid #28a745;
        }
        
        .opportunity-card h3 {
            color: #2c3e50;
            margin-bottom: 15px;
        }
        
        .recommendations {
            background: #e8f5e8;
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid #28a745;
        }
        
        .recommendations h3 {
            color: #155724;
            margin-bottom: 15px;
        }
        
        .recommendations ul {
            list-style: none;
            padding: 0;
        }
        
        .recommendations li {
            padding: 8px 0;
            border-bottom: 1px solid #c3e6cb;
        }
        
        .recommendations li:before {
            content: "→ ";
            color: #28a745;
            font-weight: bold;
        }
        
        /* Print Styles */
        @media print {
            .page {
                box-shadow: none;
                margin: 0;
                page-break-after: always;
            }
            
            .nav-button {
                display: none;
            }
            
            body {
                print-color-adjust: exact;
                -webkit-print-color-adjust: exact;
            }
        }
        
        /* Responsive Design */
        @media (max-width: 1200px) {
            .page {
                width: 100%;
                margin: 0;
                padding: 15px;
                box-shadow: none;
            }
            
            .brand-grid {
                grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            }
            
            .framework-grid {
                grid-template-columns: 1fr;
            }
        }
        """
    
    def _get_navigation_js(self):
        """Get JavaScript for page navigation"""
        return """
        function showPage(pageNum) {
            const pages = document.querySelectorAll('.page');
            pages.forEach((page, index) => {
                page.style.display = index === pageNum - 1 ? 'block' : 'none';
            });
            
            // Update navigation buttons
            const navButtons = document.querySelectorAll('.nav-button');
            navButtons.forEach(button => {
                button.classList.remove('active');
            });
            
            const currentButton = document.querySelector(`[onclick="showPage(${pageNum})"]`);
            if (currentButton) {
                currentButton.classList.add('active');
            }
        }
        
        // Initialize first page
        document.addEventListener('DOMContentLoaded', function() {
            showPage(1);
        });
        """
    
    def _generate_overview_page(self, report_title, page_num, total_pages):
        """Generate Page 1: Competitive Landscape Overview"""
        navigation = self._generate_page_navigation(page_num, total_pages)
        
        # Generate brand grid similar to original but improved
        grid_html = ""
        for i, brand in enumerate(self.brand_profiles, 1):
            col_class = f"brand-col-{i}"
            
            # Logo
            logo_html = f'<img src="{brand["logos"][0]}" alt="{brand["company_name"]} logo" class="brand-logo-img">' if brand.get("logos") else f'<div class="brand-logo-placeholder">{brand["company_name"].upper()}</div>'
            
            # Brand positioning from strategy
            positioning = brand["brand_strategy"]["messaging_analysis"]["positioning_statement"]
            
            # Personality traits
            personality_traits = brand["brand_strategy"]["brand_personality"]["personality_traits"]
            
            grid_html += f"""
                <div class="logo-cell {col_class}">
                    {logo_html}
                    <div class="brand-name">{brand["company_name"]}</div>
                </div>
                
                <div class="positioning-cell {col_class}">
                    <div class="positioning-text">{positioning}</div>
                </div>
                
                <div class="personality-cell {col_class}">
                    <div class="personality-words">
                        {''.join([f'<span class="personality-tag">{trait}</span>' for trait in personality_traits[:6]])}
                    </div>
                </div>
                
                <div class="color-cell {col_class}">
                    <div class="color-swatches">
                        {''.join([f'<div class="color-swatch" style="background-color: {color};"></div>' for color in brand["color_palette"]])}
                    </div>
                </div>
                
                <div class="visual-cell {col_class}">
                    <div class="screenshot-container">
                        {'<img src="' + brand["screenshot"] + '" style="width:100%; height:100%; object-fit:cover;">' if brand.get("screenshot") else '<div class="screenshot-placeholder">Homepage Screenshot</div>'}
                    </div>
                </div>
            """
        
        return f"""
    <div class="page" id="page-{page_num}">
        <div class="page-header">
            <div class="page-title">Competitive Overview</div>
            <div class="page-number">Page {page_num} of {total_pages}</div>
        </div>
        
        {navigation}
        
        <div class="page-content">
            <h1 class="main-title">{report_title}</h1>
            <p class="subtitle">Comprehensive Competitive Intelligence Analysis</p>
            <p class="analysis-date">Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
            
            <div class="brand-grid-container">
                <div class="brand-grid" style="grid-template-columns: repeat({len(self.brand_profiles)}, 1fr);">
                    {grid_html}
                </div>
            </div>
            
            <div class="section">
                <h2 class="section-title">Report Structure</h2>
                <ul>
                    <li><strong>Page 1:</strong> Competitive Landscape Overview (this page)</li>
                    <li><strong>Pages 2-{len(self.brand_profiles) + 1}:</strong> Individual Brand Deep-Dive Analysis</li>
                    <li><strong>Page {len(self.brand_profiles) + 2}:</strong> Cross-Brand Comparison Matrix</li>
                    <li><strong>Page {len(self.brand_profiles) + 3}:</strong> Market Opportunity Analysis</li>
                </ul>
            </div>
        </div>
        
        <div class="page-footer">
            Competitive Intelligence Report • {datetime.now().strftime('%B %Y')} • Confidential Analysis
        </div>
    </div>
        """
    
    def _generate_brand_deep_dive_page(self, brand, page_num, total_pages):
        """Generate individual brand deep-dive page"""
        navigation = self._generate_page_navigation(page_num, total_pages)
        
        strategy = brand["brand_strategy"]
        architecture = brand["brand_architecture"]
        
        return f"""
    <div class="page" id="page-{page_num}">
        <div class="page-header">
            <div class="page-title">{brand["company_name"]} Deep Dive</div>
            <div class="page-number">Page {page_num} of {total_pages}</div>
        </div>
        
        {navigation}
        
        <div class="page-content">
            <div class="brand-overview">
                <h2>{brand["company_name"]}</h2>
                <p><strong>URL:</strong> {brand["url"]}</p>
                <p><strong>Analysis Date:</strong> {datetime.fromisoformat(brand["analysis_timestamp"]).strftime('%B %d, %Y at %I:%M %p')}</p>
            </div>
            
            <!-- Brand Strategy & Verbal Expression -->
            <div class="section">
                <h2 class="section-title">Brand Strategy & Verbal Expression</h2>
                
                <div class="subsection">
                    <h3 class="subsection-title">Strategy Framework</h3>
                    <div class="framework-grid">
                        <div class="framework-item">
                            <div class="framework-label">WHY - Purpose</div>
                            <div class="framework-content">{strategy["why_framework"]["purpose"]}</div>
                        </div>
                        <div class="framework-item">
                            <div class="framework-label">HOW - Approach</div>
                            <div class="framework-content">{strategy["how_framework"]["approach"]}</div>
                        </div>
                        <div class="framework-item">
                            <div class="framework-label">WHAT - Offerings</div>
                            <div class="framework-content">{strategy["what_framework"]["offerings"]}</div>
                        </div>
                        <div class="framework-item">
                            <div class="framework-label">WHO - Target Audience</div>
                            <div class="framework-content">{strategy["who_framework"]["target_audience"]}</div>
                        </div>
                    </div>
                </div>
                
                <div class="subsection">
                    <h3 class="subsection-title">Messaging Analysis</h3>
                    <p><strong>Brand Voice:</strong> {strategy["messaging_analysis"]["brand_voice"]}</p>
                    <p><strong>Positioning Statement:</strong> {strategy["messaging_analysis"]["positioning_statement"]}</p>
                    
                    <div class="framework-item">
                        <div class="framework-label">Key Messages</div>
                        <div class="tag-list">
                            {''.join([f'<span class="tag">{msg}</span>' for msg in strategy["messaging_analysis"]["key_messages"]])}
                        </div>
                    </div>
                    
                    <div class="framework-item">
                        <div class="framework-label">Brand Personality Traits</div>
                        <div class="tag-list">
                            {''.join([f'<span class="tag">{trait}</span>' for trait in strategy["brand_personality"]["personality_traits"]])}
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Brand Architecture -->
            <div class="section">
                <h2 class="section-title">Brand Architecture</h2>
                
                <div class="framework-grid">
                    <div class="framework-item">
                        <div class="framework-label">Portfolio Overview</div>
                        <div class="framework-content">
                            <p><strong>Type:</strong> {architecture["portfolio_overview"]["brand_type"]}</p>
                            <p><strong>Scope:</strong> {architecture["portfolio_overview"]["portfolio_scope"]}</p>
                        </div>
                    </div>
                    <div class="framework-item">
                        <div class="framework-label">Product Organization</div>
                        <div class="tag-list">
                            {''.join([f'<span class="tag">{cat}</span>' for cat in architecture["product_organization"]["main_categories"]])}
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Visual Summary -->
            <div class="section">
                <h2 class="section-title">Visual Summary</h2>
                
                <div class="subsection">
                    <h3 class="subsection-title">Logo & Visual System</h3>
                    {f'<img src="{brand["logos"][0]}" alt="Logo" style="max-height: 60px; margin-bottom: 15px;">' if brand.get("logos") else '<p>Logo not captured</p>'}
                    <p><strong>Visual Style:</strong> {brand["visual_analysis"]["layout_analysis"]}</p>
                </div>
                
                <div class="subsection">
                    <h3 class="subsection-title">Color Palette</h3>
                    <div class="color-swatches" style="display: flex; gap: 10px; margin-bottom: 15px;">
                        {''.join([f'<div style="width: 40px; height: 40px; background-color: {color}; border-radius: 4px; border: 1px solid #ddd;"></div>' for color in brand["color_palette"]])}
                    </div>
                    <p>Colors: {', '.join(brand["color_palette"])}</p>
                </div>
                
                <div class="subsection">
                    <h3 class="subsection-title">Homepage Screenshot</h3>
                    {f'<img src="{brand["screenshot"]}" alt="Homepage" style="width: 100%; max-width: 600px; border: 1px solid #ddd; border-radius: 8px;">' if brand.get("screenshot") else '<p>Screenshot not captured</p>'}
                </div>
            </div>
        </div>
        
        <div class="page-footer">
            {brand["company_name"]} Brand Analysis • {datetime.now().strftime('%B %Y')} • Page {page_num} of {total_pages}
        </div>
    </div>
        """
    
    def _generate_comparison_matrix_page(self, page_num, total_pages):
        """Generate cross-brand comparison matrix page"""
        navigation = self._generate_page_navigation(page_num, total_pages)
        
        # Generate comparison table
        comparison_rows = ""
        
        # Brand Names Row
        comparison_rows += "<tr><th>Brand</th>"
        for brand in self.brand_profiles:
            comparison_rows += f"<td><strong>{brand['company_name']}</strong></td>"
        comparison_rows += "</tr>"
        
        # Positioning Row
        comparison_rows += "<tr><th>Brand Positioning</th>"
        for brand in self.brand_profiles:
            positioning = brand["brand_strategy"]["messaging_analysis"]["positioning_statement"][:100] + "..."
            comparison_rows += f"<td>{positioning}</td>"
        comparison_rows += "</tr>"
        
        # Target Audience Row
        comparison_rows += "<tr><th>Target Audience</th>"
        for brand in self.brand_profiles:
            audience = brand["brand_strategy"]["who_framework"]["target_audience"]
            comparison_rows += f"<td>{audience}</td>"
        comparison_rows += "</tr>"
        
        # Key Differentiators Row
        comparison_rows += "<tr><th>Key Differentiators</th>"
        for brand in self.brand_profiles:
            differentiators = ", ".join(brand["brand_strategy"]["how_framework"]["differentiators"][:3])
            comparison_rows += f"<td>{differentiators}</td>"
        comparison_rows += "</tr>"
        
        # Brand Archetype Row
        comparison_rows += "<tr><th>Brand Archetype</th>"
        for brand in self.brand_profiles:
            archetype = brand["brand_strategy"]["brand_personality"]["brand_archetype"]
            comparison_rows += f"<td>{archetype}</td>"
        comparison_rows += "</tr>"
        
        return f"""
    <div class="page" id="page-{page_num}">
        <div class="page-header">
            <div class="page-title">Cross-Brand Comparison</div>
            <div class="page-number">Page {page_num} of {total_pages}</div>
        </div>
        
        {navigation}
        
        <div class="page-content">
            <h1 class="main-title">Competitive Comparison Matrix</h1>
            
            <div class="section">
                <h2 class="section-title">Brand Comparison Overview</h2>
                <table class="comparison-table">
                    {comparison_rows}
                </table>
            </div>
            
            <div class="section">
                <h2 class="section-title">Competitive Analysis Insights</h2>
                
                <div class="opportunity-grid">
                    <div class="opportunity-card">
                        <h3>Positioning Gaps</h3>
                        <p>Analysis of competitive positioning reveals opportunities in customer experience, personalization, and emerging technology integration.</p>
                    </div>
                    
                    <div class="opportunity-card">
                        <h3>Brand Differentiation</h3>
                        <p>Key areas where brands differentiate include service approach, target market focus, and technology sophistication.</p>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="page-footer">
            Competitive Comparison Matrix • {datetime.now().strftime('%B %Y')} • Page {page_num} of {total_pages}
        </div>
    </div>
        """
    
    def _generate_opportunity_analysis_page(self, page_num, total_pages):
        """Generate market opportunity analysis page"""
        navigation = self._generate_page_navigation(page_num, total_pages)
        
        return f"""
    <div class="page" id="page-{page_num}">
        <div class="page-header">
            <div class="page-title">Market Opportunity Analysis</div>
            <div class="page-number">Page {page_num} of {total_pages}</div>
        </div>
        
        {navigation}
        
        <div class="page-content">
            <h1 class="main-title">Strategic Opportunities & Recommendations</h1>
            
            <div class="section">
                <h2 class="section-title">Competitive Landscape Summary</h2>
                <p>Based on the analysis of {len(self.brand_profiles)} key competitors, several strategic opportunities emerge in the market:</p>
                
                <div class="opportunity-grid">
                    <div class="opportunity-card">
                        <h3>Market Positioning</h3>
                        <p>Current players focus heavily on traditional approaches. Opportunity exists for more innovative, user-centric positioning.</p>
                    </div>
                    
                    <div class="opportunity-card">
                        <h3>Technology Integration</h3>
                        <p>While all brands mention technology, few demonstrate true digital-first innovation in their messaging and offerings.</p>
                    </div>
                    
                    <div class="opportunity-card">
                        <h3>Customer Experience</h3>
                        <p>Gap identified in personalized, consultative customer experience that goes beyond traditional service models.</p>
                    </div>
                    
                    <div class="opportunity-card">
                        <h3>Brand Communication</h3>
                        <p>Opportunity for more authentic, transparent communication style that differentiates from corporate-heavy messaging.</p>
                    </div>
                </div>
            </div>
            
            <div class="section">
                <h2 class="section-title">White Space Opportunities</h2>
                
                <div class="framework-grid">
                    <div class="framework-item">
                        <div class="framework-label">Underserved Segments</div>
                        <div class="framework-content">
                            <ul>
                                <li>Small to medium enterprises needing enterprise-level solutions</li>
                                <li>Digital-native companies seeking modern service approaches</li>
                                <li>Sustainability-focused organizations</li>
                            </ul>
                        </div>
                    </div>
                    
                    <div class="framework-item">
                        <div class="framework-label">Service Gaps</div>
                        <div class="framework-content">
                            <ul>
                                <li>Real-time, AI-powered insights and recommendations</li>
                                <li>Fully integrated digital ecosystem</li>
                                <li>Predictive analytics and proactive service</li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="recommendations">
                <h3>Strategic Recommendations</h3>
                <ul>
                    <li>Position as the technology-forward, customer-centric alternative to traditional providers</li>
                    <li>Develop distinctive brand voice that balances professionalism with approachability</li>
                    <li>Focus on digital-first customer experience and self-service capabilities</li>
                    <li>Create transparent, education-focused content marketing strategy</li>
                    <li>Build partnerships with emerging technology providers to differentiate offerings</li>
                    <li>Develop specialized solutions for underserved market segments</li>
                </ul>
            </div>
            
            <div class="section">
                <h2 class="section-title">Next Steps</h2>
                <div class="framework-item">
                    <div class="framework-content">
                        <ol>
                            <li><strong>Brand Strategy Development:</strong> Refine positioning based on identified opportunities</li>
                            <li><strong>Customer Research:</strong> Validate opportunity areas with target customer segments</li>
                            <li><strong>Competitive Monitoring:</strong> Establish ongoing competitive intelligence program</li>
                            <li><strong>Brand Development:</strong> Create distinctive brand identity and messaging framework</li>
                            <li><strong>Go-to-Market Strategy:</strong> Develop launch strategy targeting identified white space</li>
                        </ol>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="page-footer">
            Market Opportunity Analysis • {datetime.now().strftime('%B %Y')} • Page {page_num} of {total_pages}
        </div>
    </div>
        """
    
    def _generate_page_navigation(self, current_page, total_pages):
        """Generate page navigation"""
        nav_buttons = ""
        
        for i in range(1, total_pages + 1):
            active_class = "active" if i == current_page else ""
            page_label = self._get_page_label(i, total_pages)
            nav_buttons += f'<a href="#" class="nav-button {active_class}" onclick="showPage({i})">{page_label}</a>'
        
        return f"""
        <div class="page-navigation">
            {nav_buttons}
        </div>
        """
    
    def _get_page_label(self, page_num, total_pages):
        """Get label for navigation button"""
        if page_num == 1:
            return "Overview"
        elif page_num <= len(self.brand_profiles) + 1:
            brand_index = page_num - 2
            return f"{self.brand_profiles[brand_index]['company_name']}"
        elif page_num == total_pages - 1:
            return "Comparison"
        elif page_num == total_pages:
            return "Opportunities"
        else:
            return f"Page {page_num}"


def main():
    """Example usage of comprehensive report generator"""
    
    # Medical/Healthcare platforms for comprehensive analysis
    medical_urls = [
        "https://www.wolterskluwer.com",
        "https://www.elsevier.com",
        "https://www.clinicalkey.com",
        "https://www.openevidence.com"
    ]
    
    generator = ComprehensiveReportGenerator()
    
    # Generate comprehensive multi-page report
    output_file = generator.generate_comprehensive_report(
        urls=medical_urls,
        report_title="Medical Information & AI Platform Competitive Intelligence",
        output_filename="comprehensive_competitive_intelligence_report.html"
    )
    
    if output_file:
        print(f"\n🎉 COMPREHENSIVE REPORT COMPLETE!")
        print(f"📁 File location: {os.path.abspath(output_file)}")
        print(f"🌐 Open in browser to navigate through all pages")
        print(f"📊 Report includes: Overview + {len(medical_urls)} Brand Deep-Dives + Comparison + Opportunities")

if __name__ == "__main__":
    main()