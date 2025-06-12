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

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
openai.api_key = os.getenv("OPENAI_API_KEY")

MAX_CONTENT_LENGTH = 15000

class EnhancedBrandProfiler:
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
            return ['#666666', '#999999', '#cccccc']  # Default colors
        
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
            return ['#666666', '#999999', '#cccccc']
    
    def extract_enhanced_brand_info(self, html_content, url):
        """Extract comprehensive brand information using AI"""
        truncated_html = html_content[:MAX_CONTENT_LENGTH]
        
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
                "visual_style": "Description of visual design approach",
                "social_media_urls": ["url1", "url2"], // Any social media links found
                "key_differentiators": ["Unique point 1", "Unique point 2"], // What makes them different
                "brand_story": "Brief brand story or mission statement"
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
            "personality_descriptors": ["Professional", "Reliable", "Modern"],
            "primary_messages": ["Quality products and services"],
            "target_audience": "General consumers",
            "brand_voice": "Professional and informative",
            "visual_style": "Clean and modern",
            "social_media_urls": [],
            "key_differentiators": ["Quality focus"],
            "brand_story": "No brand story available"
        }
    
    def capture_screenshot_data(self, url):
        """Simulate screenshot capture (placeholder for actual implementation)"""
        # In a real implementation, you'd use something like Selenium or Playwright
        # For now, return placeholder data
        return {
            "screenshot_url": f"screenshot_placeholder_{hash(url) % 10000}.png",
            "visual_elements": ["Homepage layout", "Navigation structure", "Color scheme"],
            "design_patterns": ["Modern", "Clean", "Responsive"]
        }
    
    def analyze_brand_comprehensive(self, url):
        """Main method to perform comprehensive brand analysis"""
        print(f"Analyzing brand: {url}")
        
        # Fetch webpage content
        html_content = self.fetch_page(url)
        if not html_content:
            return None
        
        # Extract logos
        logos = self.extract_logos(html_content, url)
        
        # Extract colors
        colors = self.extract_colors_from_html(html_content)
        
        # Extract comprehensive brand information
        brand_info = self.extract_enhanced_brand_info(html_content, url)
        
        # Capture screenshot data
        screenshot_data = self.capture_screenshot_data(url)
        
        # Compile comprehensive brand profile
        brand_profile = {
            "url": url,
            "company_name": brand_info.get("company_name", "Unknown"),
            "brand_positioning": brand_info.get("brand_positioning", ""),
            "personality_descriptors": brand_info.get("personality_descriptors", []),
            "primary_messages": brand_info.get("primary_messages", []),
            "target_audience": brand_info.get("target_audience", ""),
            "brand_voice": brand_info.get("brand_voice", ""),
            "visual_style": brand_info.get("visual_style", ""),
            "logo_urls": logos,
            "color_palette": colors,
            "social_media_urls": brand_info.get("social_media_urls", []),
            "key_differentiators": brand_info.get("key_differentiators", []),
            "brand_story": brand_info.get("brand_story", ""),
            "screenshot_data": screenshot_data,
            "analysis_timestamp": pd.Timestamp.now().isoformat()
        }
        
        return brand_profile

def analyze_competitor_brands(urls):
    """Analyze multiple competitor brands and return comprehensive data"""
    profiler = EnhancedBrandProfiler()
    brand_profiles = []
    
    for url in urls:
        try:
            profile = profiler.analyze_brand_comprehensive(url)
            if profile:
                brand_profiles.append(profile)
                print(f"Successfully analyzed: {profile['company_name']}")
            else:
                print(f"Failed to analyze: {url}")
        except Exception as e:
            print(f"Error analyzing {url}: {e}")
    
    return brand_profiles

def generate_enhanced_report_data(brand_profiles):
    """Generate data structure for enhanced report template"""
    report_data = {
        "page_title": "There is a huge opportunity in the category",
        "analysis_date": pd.Timestamp.now().strftime("%B %d, %Y"),
        "brands": []
    }
    
    for profile in brand_profiles:
        brand_data = {
            "name": profile["company_name"],
            "url": profile["url"],
            "positioning": profile["brand_positioning"],
            "personality": profile["personality_descriptors"][:4],  # Limit to 4 for display
            "colors": profile["color_palette"][:6],  # Limit to 6 colors
            "logo_url": profile["logo_urls"][0] if profile["logo_urls"] else None,
            "visual_assets": {
                "screenshot": profile["screenshot_data"]["screenshot_url"],
                "elements": profile["screenshot_data"]["visual_elements"]
            },
            "messages": profile["primary_messages"],
            "voice": profile["brand_voice"],
            "differentiators": profile["key_differentiators"],
            "story": profile["brand_story"]
        }
        report_data["brands"].append(brand_data)
    
    return report_data

if __name__ == "__main__":
    # Example usage
    test_urls = [
        "https://www.tdameritrade.com",
        "https://www.edwardjones.com",
        "https://www.schwab.com"
    ]
    
    # Analyze brands
    profiles = analyze_competitor_brands(test_urls)
    
    # Generate report data
    report_data = generate_enhanced_report_data(profiles)
    
    # Save to JSON for template use
    with open("enhanced_brand_analysis.json", "w") as f:
        json.dump(report_data, f, indent=2)
    
    print(f"Analysis complete. {len(profiles)} brands analyzed.")
    print("Report data saved to enhanced_brand_analysis.json")