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
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class CompetitiveGridGenerator:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.driver = None
    
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
        """Extract comprehensive brand information using AI"""
        
        # Use more content for better analysis
        truncated_html = html_content[:25000]
        
        # Extract specific sections for better analysis
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Get hero section
        hero_text = ""
        hero_selectors = ['h1', '.hero', '[class*="hero"]', '.banner', '.main-heading']
        for selector in hero_selectors:
            elements = soup.select(selector)
            for elem in elements[:3]:
                hero_text += elem.get_text().strip() + " "
        
        # Get about/description text  
        about_text = ""
        about_selectors = ['[class*="about"]', '[class*="description"]', 'p']
        for selector in about_selectors:
            elements = soup.select(selector)
            for elem in elements[:5]:
                text = elem.get_text().strip()
                if len(text) > 50:
                    about_text += text + " "
        
        messages = [
            {"role": "system", "content": "You are an expert brand analyst specializing in medical/healthcare technology companies. Extract detailed, accurate brand information from webpage content."},
            {"role": "user", "content": f"""
            DEEP ANALYSIS REQUEST: Analyze this medical/healthcare company's webpage and extract comprehensive brand information.
            
            URL: {url}
            
            Hero Section Text: {hero_text[:1000]}
            About/Description Text: {about_text[:2000]}
            
            Return your response as valid JSON with these exact keys:
            {{
                "company_name": "Exact official company/brand name (not generic)",
                "brand_positioning": "Complete value proposition and positioning statement (3-4 sentences describing what they do and their unique value)",
                "personality_descriptors": ["Specific", "Unique", "Descriptive", "Adjectives", "About", "Brand"], // 6 specific adjectives that capture their brand personality
                "primary_messages": ["Key message 1", "Key message 2", "Key message 3"], // Main value propositions from homepage
                "target_audience": "Specific target customer description (be detailed about who uses their products)",
                "brand_voice": "Detailed description of communication style and tone",
                "visual_style": "Detailed description of visual design approach and brand aesthetics"
            }}
            
            Focus on being specific and accurate. Extract real information, not generic descriptions.
            
            Full webpage content:
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
    
    def capture_screenshot(self, url):
        """Capture homepage screenshot using Selenium"""
        try:
            if not self.driver:
                chrome_options = Options()
                chrome_options.add_argument('--headless')
                chrome_options.add_argument('--no-sandbox')
                chrome_options.add_argument('--disable-dev-shm-usage')
                chrome_options.add_argument('--window-size=1200,800')
                self.driver = webdriver.Chrome(options=chrome_options)
            
            self.driver.get(url)
            time.sleep(3)  # Wait for page to load
            
            # Take screenshot
            screenshot = self.driver.get_screenshot_as_png()
            
            # Convert to base64
            screenshot_b64 = base64.b64encode(screenshot).decode('utf-8')
            return f"data:image/png;base64,{screenshot_b64}"
            
        except Exception as e:
            print(f"Screenshot capture failed for {url}: {e}")
            return None
    
    def extract_better_colors(self, html_content, url):
        """Enhanced color extraction with better filtering"""
        try:
            # First try screenshot-based color extraction
            if not self.driver:
                chrome_options = Options()
                chrome_options.add_argument('--headless')
                chrome_options.add_argument('--no-sandbox')
                chrome_options.add_argument('--disable-dev-shm-usage')
                chrome_options.add_argument('--window-size=1200,800')
                self.driver = webdriver.Chrome(options=chrome_options)
            
            self.driver.get(url)
            time.sleep(2)
            
            # Get screenshot for color analysis
            screenshot = self.driver.get_screenshot_as_png()
            img = Image.open(io.BytesIO(screenshot))
            
            # Convert to RGB and get dominant colors
            img_rgb = img.convert('RGB')
            img_array = np.array(img_rgb)
            pixels = img_array.reshape(-1, 3)
            
            # Filter out common web colors (white, black, grays)
            filtered_pixels = []
            for pixel in pixels:
                r, g, b = pixel
                # Skip very light, very dark, or very gray colors
                if not (all(c > 240 for c in [r,g,b]) or all(c < 15 for c in [r,g,b]) or 
                       (max(r,g,b) - min(r,g,b) < 30)):
                    filtered_pixels.append(pixel)
            
            if len(filtered_pixels) > 100:
                # Use K-means to find dominant colors
                kmeans = KMeans(n_clusters=6, random_state=42, n_init=10)
                kmeans.fit(filtered_pixels[:5000])  # Sample for performance
                
                hex_colors = []
                for center in kmeans.cluster_centers_:
                    r, g, b = [int(c) for c in center]
                    hex_color = f"#{r:02X}{g:02X}{b:02X}"
                    hex_colors.append(hex_color)
                
                return hex_colors
            
        except Exception as e:
            print(f"Enhanced color extraction failed for {url}: {e}")
        
        # Fallback to CSS-based extraction
        return self.extract_colors_from_html(html_content)
    
    def extract_logos_deep(self, html_content, base_url):
        """Deep logo extraction with multiple approaches"""
        soup = BeautifulSoup(html_content, 'html.parser')
        logo_urls = []
        
        print("     🔍 Searching header logos...")
        # More comprehensive logo selectors
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
            '.company-logo img',
            '[class*="brand"] img',
            '[id*="logo"] img'
        ]
        
        for selector in logo_selectors:
            elements = soup.select(selector)
            for img in elements:
                src = img.get('src') or img.get('data-src')
                if src and self._is_likely_logo(src, img.get('alt', '')):
                    full_url = urljoin(base_url, src)
                    if full_url not in logo_urls:
                        logo_urls.append(full_url)
                        print(f"     ✓ Found logo: {src}")
        
        print(f"     📊 Total logos found: {len(logo_urls)}")
        return logo_urls[:3]  # Return top 3
    
    def extract_colors_deep(self, html_content, url):
        """Deep color extraction with multiple methods"""
        print("     🎨 Analyzing CSS files...")
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
                        print(f"     ✓ Analyzed CSS file: {href}")
                except:
                    pass
        
        # Process and filter colors
        processed_colors = self._process_colors(list(all_colors))
        print(f"     📊 Extracted {len(processed_colors)} brand colors")
        return processed_colors
    
    def capture_screenshot_proper(self, url):
        """Proper screenshot capture with error handling"""
        try:
            print("     📸 Setting up browser...")
            
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--window-size=1200,800')
            chrome_options.add_argument('--disable-web-security')
            chrome_options.add_argument('--allow-running-insecure-content')
            
            # Try to create driver
            driver = webdriver.Chrome(options=chrome_options)
            
            print("     🌐 Loading webpage...")
            driver.get(url)
            
            print("     ⏳ Waiting for page load...")
            time.sleep(5)  # Wait for page to fully load
            
            # Scroll to capture more content
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight/3);")
            time.sleep(2)
            driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(2)
            
            print("     📷 Taking screenshot...")
            screenshot = driver.get_screenshot_as_png()
            
            # Convert to base64
            screenshot_b64 = base64.b64encode(screenshot).decode('utf-8')
            
            driver.quit()
            print("     ✓ Screenshot captured successfully")
            return f"data:image/png;base64,{screenshot_b64}"
            
        except Exception as e:
            print(f"     ❌ Screenshot failed: {e}")
            try:
                if 'driver' in locals():
                    driver.quit()
            except:
                pass
            return None
    
    def _extract_content_sections(self, soup):
        """Extract different content sections for comprehensive analysis"""
        sections = {}
        
        # Hero section
        hero_selectors = ['h1', '.hero', '[class*="hero"]', '.banner', '.jumbotron']
        sections['hero'] = []
        for selector in hero_selectors:
            elements = soup.select(selector)
            for elem in elements[:3]:
                text = elem.get_text().strip()
                if text and len(text) > 10:
                    sections['hero'].append(text)
        
        # Navigation and key sections
        sections['navigation'] = []
        nav_elements = soup.select('nav a, .nav a, .menu a')
        for nav in nav_elements[:10]:
            text = nav.get_text().strip()
            if text:
                sections['navigation'].append(text)
        
        # Feature/product descriptions
        sections['features'] = []
        feature_selectors = ['.feature', '[class*="product"]', '[class*="service"]', '.card']
        for selector in feature_selectors:
            elements = soup.select(selector)
            for elem in elements[:5]:
                text = elem.get_text().strip()
                if len(text) > 30:
                    sections['features'].append(text[:200])
        
        # About/company information
        sections['about'] = []
        about_selectors = ['[class*="about"]', '[class*="company"]', '[class*="mission"]']
        for selector in about_selectors:
            elements = soup.select(selector)
            for elem in elements[:3]:
                text = elem.get_text().strip()
                if len(text) > 50:
                    sections['about'].append(text[:300])
        
        return sections
    
    def extract_brand_info_comprehensive(self, html_content, url, content_sections):
        """Enhanced AI brand analysis with structured content"""
        
        # Create comprehensive context
        context = f"""
        URL: {url}
        
        HERO CONTENT: {' | '.join(content_sections.get('hero', [])[:3])}
        
        KEY NAVIGATION: {' | '.join(content_sections.get('navigation', [])[:8])}
        
        FEATURES/SERVICES: {' | '.join(content_sections.get('features', [])[:3])}
        
        ABOUT/COMPANY: {' | '.join(content_sections.get('about', [])[:2])}
        """
        
        messages = [
            {"role": "system", "content": "You are a senior brand strategist analyzing medical/healthcare technology companies. Provide detailed, specific insights based on actual content."},
            {"role": "user", "content": f"""
            COMPREHENSIVE BRAND ANALYSIS REQUEST
            
            Analyze this medical/healthcare company's website and provide detailed brand intelligence.
            
            {context}
            
            Based on the actual content above, return JSON with these keys:
            {{
                "company_name": "Official company name (extract from content, not URL)",
                "brand_positioning": "Specific value proposition based on actual hero/feature content (3-4 sentences)",
                "personality_descriptors": ["6", "specific", "adjectives", "based", "on", "content"], 
                "primary_messages": ["Actual key message 1", "Actual key message 2", "Actual key message 3"],
                "target_audience": "Specific audience based on content analysis",
                "brand_voice": "Communication style based on actual copy",
                "visual_style": "Design approach based on page structure"
            }}
            
            Extract REAL information from the content provided. Be specific and accurate.
            """}
        ]
        
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                temperature=0.1,  # Lower temperature for more consistent results
                max_tokens=1200
            )
            
            content = response.choices[0].message.content.strip()
            # Clean up response
            content = re.sub(r"```(json)?", "", content).strip()
            content = content.replace("```", "").strip()
            
            # Try to find JSON in response
            if '{' in content:
                start = content.find('{')
                end = content.rfind('}') + 1
                json_content = content[start:end]
                parsed_response = json.loads(json_content)
            else:
                raise ValueError("No JSON found in response")
            
            return parsed_response
        except Exception as e:
            print(f"     ❌ AI analysis failed: {e}")
            return self._get_default_brand_info()
    
    def extract_logos_comprehensive(self, html_content, base_url):
        """Comprehensive logo extraction with multiple methods"""
        return self.extract_logos_deep(html_content, base_url)
    
    def extract_colors_comprehensive(self, html_content, url):
        """Comprehensive color extraction"""
        return self.extract_colors_deep(html_content, url)
    
    def _analyze_visual_elements(self, soup):
        """Analyze visual design elements"""
        elements = {
            'has_hero_image': bool(soup.select('.hero img, [class*="hero"] img')),
            'button_styles': len(soup.select('button, .btn, [class*="button"]')),
            'card_elements': len(soup.select('.card, [class*="card"]')),
            'icon_usage': len(soup.select('svg, .icon, [class*="icon"]')),
            'typography_elements': len(soup.select('h1, h2, h3, h4, h5, h6'))
        }
        return elements
    
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
        """Comprehensive brand analysis with thorough extraction"""
        print(f"🔍 COMPREHENSIVE ANALYSIS: {url}")
        
        # Fetch webpage content
        html_content = self.fetch_page(url)
        if not html_content:
            return None
        
        print("   📊 Analyzing page structure...")
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Extract multiple content sections for comprehensive analysis
        print("   📝 Extracting content sections...")
        content_sections = self._extract_content_sections(soup)
        
        print("   🧠 Deep AI brand analysis...")
        # Extract brand information with comprehensive content
        brand_info = self.extract_brand_info_comprehensive(html_content, url, content_sections)
        
        print("   🖼️ Comprehensive logo search...")
        # Extract logos with multiple methods
        logos = self.extract_logos_comprehensive(html_content, url)
        
        print("   🎨 Advanced color analysis...")
        # Extract colors from multiple sources
        colors = self.extract_colors_comprehensive(html_content, url)
        
        print("   📸 Capturing homepage screenshot...")
        # Capture screenshot
        screenshot = self.capture_screenshot_proper(url)
        
        print("   🔬 Analyzing visual elements...")
        # Extract additional visual information
        visual_elements = self._analyze_visual_elements(soup)
        
        print("   ✅ Compiling comprehensive brand profile...")
        
        # Compile comprehensive brand profile
        brand_profile = {
            "url": url,
            "company_name": brand_info.get("company_name", "Unknown Company"),
            "brand_positioning": brand_info.get("brand_positioning", "No positioning available"),
            "personality_descriptors": brand_info.get("personality_descriptors", ["Professional", "Reliable"])[:6],
            "primary_messages": brand_info.get("primary_messages", ["Quality solutions"]),
            "target_audience": brand_info.get("target_audience", "Healthcare professionals"),
            "brand_voice": brand_info.get("brand_voice", "Professional"),
            "color_palette": colors[:6] if colors else ["#666666", "#999999", "#cccccc"],
            "logo_url": logos[0] if logos else None,
            "visual_style": brand_info.get("visual_style", "Modern and clean"),
            "screenshot": screenshot,
            "visual_elements": visual_elements,
            "analysis_timestamp": datetime.now().isoformat(),
            "analysis_depth": "comprehensive"
        }
        
        print(f"   ✅ ANALYSIS COMPLETE: {brand_profile['company_name']}")
        print(f"      Logo: {'✓' if brand_profile['logo_url'] else '✗'}")
        print(f"      Colors: {len(brand_profile['color_palette'])}")
        print(f"      Screenshot: {'✓' if brand_profile['screenshot'] else '✗'}")
        print(f"      Personality traits: {len(brand_profile['personality_descriptors'])}")
        
        return brand_profile
    
    def cleanup(self):
        """Clean up resources"""
        if self.driver:
            self.driver.quit()
            self.driver = None
    
    def generate_grid_html(self, brand_profiles, page_title="There is a huge opportunity in the category"):
        """Generate the exact 5-row competitive landscape grid as HTML"""
        
        # Use actual number of brands analyzed (no padding or truncating)
        num_brands = len(brand_profiles)
        
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
            grid-template-columns: repeat({num_brands}, 1fr);
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
                    <div class="screenshot-container">"""
            
            # Add actual screenshot or placeholder
            if brand.get("screenshot"):
                html_content += f'<img src="{brand["screenshot"]}" alt="Homepage Screenshot" style="width:100%; height:100%; object-fit:cover; border-radius:4px;">'
            else:
                html_content += '<div class="screenshot-placeholder">Homepage Screenshot</div>'
            
            html_content += f"""
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
        seen_companies = set()
        
        try:
            for url in urls:
                try:
                    profile = self.analyze_brand(url)
                    if profile:
                        company_name = profile['company_name']
                        # Deduplicate by company name
                        if company_name not in seen_companies:
                            brand_profiles.append(profile)
                            seen_companies.add(company_name)
                            print(f"✓ Analyzed: {company_name}")
                        else:
                            print(f"⚠ Skipped duplicate: {company_name}")
                    else:
                        print(f"✗ Failed to analyze: {url}")
                except Exception as e:
                    print(f"✗ Error analyzing {url}: {e}")
        finally:
            # Always cleanup driver
            self.cleanup()
        
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
    
    # Medical/Healthcare information platforms - comprehensive analysis
    medical_urls = [
        "https://www.wolterskluwer.com",
        "https://www.elsevier.com",
        "https://www.clinicalkey.com",
        "https://www.openevidence.com",
        "https://www.dynamed.com",
        "https://www.uptodate.com"
    ]
    
    generator = CompetitiveGridGenerator()
    
    # Generate the exact grid you specified
    output_file = generator.generate_competitive_landscape_report(
        urls=medical_urls,
        page_title="Medical Information & AI Platform Competitive Landscape",
        output_filename="medical_competitive_landscape_grid.html"
    )
    
    if output_file:
        print(f"\n🎉 Success! Your competitive landscape grid is ready!")
        print(f"📁 File location: {os.path.abspath(output_file)}")
        print(f"🌐 Open in browser to view the professional 5-row grid layout")

if __name__ == "__main__":
    main()