#!/usr/bin/env python3
"""
AI-First Competitive Intelligence System
Primary: AI research for comprehensive company intelligence
Secondary: Targeted scraping for visual elements only
"""

from openai import OpenAI
import os
import json
from datetime import datetime
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
import base64
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

class AIFirstCompetitiveIntelligence:
    """AI-first approach to competitive intelligence"""
    
    def __init__(self):
        # Initialize OpenAI client
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def analyze_company(self, company_input, progress_callback=None):
        """Main analysis method: AI-first, then visual enhancement"""
        
        # Phase 1: AI Research (Primary Intelligence)
        if progress_callback:
            progress_callback(f"🧠 AI Research Phase: {company_input}")
        
        ai_profile = self._ai_comprehensive_research(company_input)
        
        # Phase 2: URL Discovery (if needed)
        if not ai_profile.get('official_url'):
            if progress_callback:
                progress_callback(f"🔍 Finding official URL for {company_input}")
            ai_profile['official_url'] = self._find_company_url(company_input)
        
        # Phase 3: Visual Extraction (Secondary Enhancement)
        if ai_profile.get('official_url'):
            if progress_callback:
                progress_callback(f"🎨 Visual extraction from {ai_profile['official_url']}")
            visual_data = self._extract_visual_elements(ai_profile['official_url'])
            ai_profile.update(visual_data)
        
        # Phase 4: Data Validation & Enhancement
        if progress_callback:
            progress_callback(f"✅ Finalizing profile for {ai_profile['company_name']}")
        
        return self._finalize_company_profile(ai_profile)
    
    def _ai_comprehensive_research(self, company_input):
        """Comprehensive AI research - primary intelligence gathering"""
        
        research_prompt = f"""
You are a senior business intelligence analyst. Provide comprehensive, factual information about this company.

COMPANY: {company_input}

Provide detailed information in this JSON format:

{{
    "company_name": "Official company name",
    "official_url": "Primary website URL (if known)",
    "company_overview": {{
        "description": "2-3 sentence company description",
        "industry": "Primary industry/sector",
        "business_model": "Revenue model (SaaS, licensing, services, etc.)",
        "target_market": "Primary customer segments",
        "company_size": "Employee count or size category",
        "founded": "Year founded",
        "headquarters": "Location"
    }},
    "products_services": {{
        "main_products": ["List of primary products/services with actual names"],
        "product_categories": ["Types of solutions offered"],
        "key_features": ["Notable capabilities or features"],
        "industries_served": ["Target industries"]
    }},
    "market_position": {{
        "market_leadership": "Market position (leader/challenger/niche)",
        "key_differentiators": ["What sets them apart from competitors"],
        "value_propositions": ["Core value propositions"],
        "competitive_advantages": ["Strategic advantages"]
    }},
    "competitive_landscape": {{
        "main_competitors": ["Direct competitors"],
        "competitive_threats": ["Key competitive challenges"],
        "market_opportunities": ["Growth opportunities"]
    }},
    "strategic_intelligence": {{
        "recent_developments": ["Recent news, funding, partnerships, products"],
        "notable_clients": ["Known major customers if public"],
        "partnerships": ["Strategic partnerships"],
        "financial_highlights": ["Revenue, funding, growth if known"]
    }},
    "brand_positioning": {{
        "brand_personality": ["Brand attributes"],
        "messaging_themes": ["Key messaging pillars"],
        "positioning_statement": "How they position themselves"
    }}
}}

Focus on factual, verifiable information. If uncertain about something, indicate "Unknown" rather than guessing.
"""
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a senior business intelligence analyst providing factual company research. Return only valid JSON."},
                    {"role": "user", "content": research_prompt}
                ],
                temperature=0.2,
                max_tokens=3000
            )
            
            ai_data = json.loads(response.choices[0].message.content)
            print(f"✅ AI Research complete for {ai_data.get('company_name', company_input)}")
            return ai_data
            
        except Exception as e:
            print(f"❌ AI research failed: {e}")
            # Return minimal structure
            return {
                "company_name": company_input,
                "error": str(e),
                "company_overview": {"description": "AI research unavailable"},
                "products_services": {"main_products": []},
                "market_position": {"key_differentiators": []},
                "competitive_landscape": {"main_competitors": []},
                "strategic_intelligence": {"recent_developments": []},
                "brand_positioning": {"brand_personality": []}
            }
    
    def _find_company_url(self, company_name):
        """Find official company URL using AI"""
        try:
            url_prompt = f"""
Find the official website URL for: {company_name}

Requirements:
- Must be the main corporate website
- Prefer .com if available
- Return ONLY the URL, nothing else

Company: {company_name}
"""
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Return only URLs, no explanations."},
                    {"role": "user", "content": url_prompt}
                ],
                temperature=0.1,
                max_tokens=50
            )
            
            url = response.choices[0].message.content.strip()
            url = url.replace('"', '').replace("'", '').strip()
            
            if not url.startswith('http'):
                url = f"https://{url}"
            
            print(f"✅ Found URL: {url}")
            return url
            
        except Exception as e:
            print(f"❌ URL discovery failed: {e}")
            return None
    
    def _extract_visual_elements(self, url):
        """Extract visual elements: colors, fonts, screenshots, logos"""
        visual_data = {
            "visual_identity": {
                "colors": [],
                "fonts": {},
                "screenshots": []
            }
        }
        
        try:
            # Get page content for color extraction
            print(f"   📄 Fetching page content from {url}")
            response = self.session.get(url, timeout=10)
            if response.status_code == 200:
                # Extract colors from CSS
                visual_data["visual_identity"]["colors"] = self._extract_colors_from_css(response.text, url)
            
            # Take screenshot and extract fonts with Selenium
            print(f"   📸 Capturing visual elements...")
            visual_data["visual_identity"]["screenshots"] = self._capture_screenshots(url)
            visual_data["visual_identity"]["fonts"] = self._extract_fonts_selenium(url)
            
        except Exception as e:
            print(f"   ⚠️ Visual extraction error: {e}")
        
        return visual_data
    
    def _extract_colors_from_css(self, html_content, url):
        """Extract brand colors from CSS"""
        import re
        from collections import defaultdict
        
        colors = []
        color_frequency = defaultdict(int)
        
        # Extract colors from HTML
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # From inline styles
        for element in soup.find_all(style=True):
            style = element.get('style', '')
            found_colors = re.findall(r'#[0-9a-fA-F]{6}|#[0-9a-fA-F]{3}|rgb\([^)]+\)', style)
            for color in found_colors:
                color_frequency[color] += 1
        
        # From style tags
        for style_tag in soup.find_all('style'):
            css_content = style_tag.get_text()
            found_colors = re.findall(r'#[0-9a-fA-F]{6}|#[0-9a-fA-F]{3}|rgb\([^)]+\)', css_content)
            for color in found_colors:
                color_frequency[color] += 2  # Weight internal CSS higher
        
        # Sort by frequency and return top colors
        sorted_colors = sorted(color_frequency.items(), key=lambda x: x[1], reverse=True)
        colors = [color for color, _ in sorted_colors[:6]]
        
        return colors if colors else ['#333333', '#666666', '#999999', '#cccccc', '#ffffff']
    
    def _capture_screenshots(self, url):
        """Capture website screenshot"""
        try:
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--window-size=1920,1080')
            chrome_options.add_argument('--disable-gpu')
            
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)
            
            driver.get(url)
            
            # Wait for page load
            WebDriverWait(driver, 10).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
            time.sleep(3)
            
            # Take screenshot
            screenshot = driver.get_screenshot_as_png()
            screenshot_b64 = base64.b64encode(screenshot).decode('utf-8')
            
            driver.quit()
            
            return [f"data:image/png;base64,{screenshot_b64}"]
            
        except Exception as e:
            print(f"   ❌ Screenshot failed: {e}")
            return []
    
    def _extract_fonts_selenium(self, url):
        """Extract typography using Selenium"""
        try:
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)
            driver.get(url)
            
            # Get computed fonts
            fonts = driver.execute_script("""
                const fonts = new Set();
                const elements = ['h1', 'h2', 'h3', 'p', 'body', 'nav', 'header'];
                
                elements.forEach(selector => {
                    const els = document.querySelectorAll(selector);
                    for(let el of els) {
                        const computed = window.getComputedStyle(el);
                        if(computed.fontFamily) {
                            fonts.add(computed.fontFamily);
                        }
                    }
                });
                
                return Array.from(fonts);
            """)
            
            driver.quit()
            
            # Clean up font names
            clean_fonts = []
            for font in fonts:
                # Remove quotes and clean up
                clean_font = font.replace('"', '').replace("'", '').split(',')[0].strip()
                if clean_font and len(clean_font) > 2:
                    clean_fonts.append(clean_font)
            
            return {
                "primary_font": clean_fonts[0] if clean_fonts else "Unknown",
                "secondary_font": clean_fonts[1] if len(clean_fonts) > 1 else "Standard",
                "font_stack": clean_fonts[:3]
            }
            
        except Exception as e:
            print(f"   ❌ Font extraction failed: {e}")
            return {"primary_font": "Unknown", "secondary_font": "Standard"}
    
    def _finalize_company_profile(self, ai_profile):
        """Finalize and structure the complete company profile"""
        
        # Add analysis metadata
        ai_profile["analysis_metadata"] = {
            "extraction_method": "AI-first with visual enhancement",
            "analysis_timestamp": datetime.now().isoformat(),
            "data_sources": ["OpenAI GPT-4", "Website visual extraction"],
            "confidence_level": "High" if ai_profile.get("company_overview", {}).get("description") != "AI research unavailable" else "Low"
        }
        
        # Generate brand story using AI data
        ai_profile["brand_story"] = self._generate_brand_story_from_ai_data(ai_profile)
        
        return ai_profile
    
    def _generate_brand_story_from_ai_data(self, ai_profile):
        """Generate brand story using rich AI data"""
        
        company = ai_profile.get("company_name", "Company")
        products = ai_profile.get("products_services", {}).get("main_products", [])
        differentiators = ai_profile.get("market_position", {}).get("key_differentiators", [])
        positioning = ai_profile.get("brand_positioning", {}).get("positioning_statement", "")
        
        try:
            story_prompt = f"""
Create a unique, specific brand story for {company}.

ACTUAL COMPANY DATA:
- Products: {', '.join(products[:5])}
- Key Differentiators: {', '.join(differentiators[:3])}
- Positioning: {positioning}
- Industry: {ai_profile.get("company_overview", {}).get("industry", "")}

Create a 2-3 sentence brand story that:
1. Uses their actual products and differentiators
2. Is specific to this company only
3. Avoids ALL generic corporate clichés
4. Focuses on their unique market position

FORBIDDEN: beacon, pioneer, leading, cutting-edge, world-class, revolutionary, transforming
"""
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Create specific, unique brand stories. No corporate clichés."},
                    {"role": "user", "content": story_prompt}
                ],
                temperature=0.7,
                max_tokens=200
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            # Fallback using AI data
            if products and differentiators:
                return f"{company} specializes in {products[0]} and {products[1] if len(products) > 1 else 'related solutions'}, distinguished by {differentiators[0] if differentiators else 'their market expertise'}. Their approach focuses on {positioning[:100] if positioning else 'delivering measurable value to their target market'}."
            else:
                return f"{company} delivers specialized solutions with a focus on their core market expertise and client success."

def main():
    """Test the AI-first system"""
    analyzer = AIFirstCompetitiveIntelligence()
    
    # Test companies
    test_companies = ["Microsoft", "Elsevier", "Wolters Kluwer"]
    
    for company in test_companies:
        print(f"\n🔍 Analyzing {company}...")
        profile = analyzer.analyze_company(company)
        print(f"✅ {profile['company_name']} analysis complete")
        print(f"   Products: {len(profile.get('products_services', {}).get('main_products', []))}")
        print(f"   Confidence: {profile.get('analysis_metadata', {}).get('confidence_level', 'Unknown')}")

if __name__ == "__main__":
    main()