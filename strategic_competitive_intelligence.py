#!/usr/bin/env python3
"""
Strategic Competitive Intelligence System
Comprehensive competitive analysis with deep multi-page insights
"""

import requests
from bs4 import BeautifulSoup
import openai
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
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Import deep scraping capabilities
try:
    from deep_scraper import enhance_brand_analysis_with_deep_scraping
    DEEP_SCRAPING_AVAILABLE = True
except ImportError:
    print("❌ Deep scraping module not available")
    DEEP_SCRAPING_AVAILABLE = False

# Initialize OpenAI
import openai
openai.api_key = os.getenv("OPENAI_API_KEY")

class StrategicCompetitiveIntelligence:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.driver = None
        self.brand_profiles = []
        self.market_intelligence = {}
        self.comprehensive_analysis = {}
    
    def fetch_page(self, url):
        """Fetch webpage content with error handling"""
        try:
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(f"Failed to retrieve the page: {url} -- {e}")
            return None
    
    def extract_comprehensive_brand_data(self, url, progress_callback=None):
        """Extract comprehensive brand data for strategic analysis"""
        print(f"🔍 STRATEGIC ANALYSIS: {url}")
        
        html_content = self.fetch_page(url)
        if not html_content:
            return None
        
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Comprehensive content extraction
        print("   📊 Extracting comprehensive website content...")
        comprehensive_content = self._extract_comprehensive_website_content(soup, url)
        
        print("   🎯 Extracting strategic messaging and positioning...")
        strategic_messaging = self._extract_strategic_messaging(soup)
        
        print("   💼 Analyzing product/service portfolio...")
        product_portfolio = self._extract_product_portfolio(soup)
        
        print("   🎨 Extracting visual identity and brand elements...")
        visual_identity = self._extract_comprehensive_visual_identity(html_content, url)
        
        print("   🎨 Analyzing brand colors from visual elements...")
        visual_identity = self._enhance_color_analysis(visual_identity, html_content, url)
        
        # Get company name first
        company_name = self._extract_company_name(soup, url)
        
        print("   📋 Searching for brand guidelines and style guides...")
        brand_guidelines = self._search_brand_guidelines(url, company_name)
        if brand_guidelines:
            visual_identity['brand_guidelines'] = brand_guidelines
        
        print("   📈 Extracting pricing and business model indicators...")
        business_model = self._extract_business_model_indicators(soup)
        
        print("   🤝 Analyzing partnerships and integrations...")
        partnerships = self._extract_partnership_indicators(soup)
        
        # Screenshot for visual analysis
        screenshot = self._capture_screenshot_proper(url)
        
        # Compile comprehensive profile
        brand_profile = {
            "url": url,
            "company_name": self._extract_company_name(soup, url),
            "comprehensive_content": comprehensive_content,
            "strategic_messaging": strategic_messaging,
            "product_portfolio": product_portfolio,
            "visual_identity": visual_identity,
            "business_model": business_model,
            "partnerships": partnerships,
            "screenshot": screenshot,
            "extraction_timestamp": datetime.now().isoformat()
        }
        
        print(f"   ✅ COMPREHENSIVE EXTRACTION COMPLETE: {brand_profile['company_name']}")
        
        # Check for missing data and use AI to fill gaps
        print("   🤖 Checking for data gaps and enhancing with AI...")
        brand_profile = self._enhance_missing_data_with_ai(brand_profile, html_content)
        
        # Search external sources for additional company information
        print("   🌐 Searching external sources for additional company data...")
        brand_profile = self._search_external_sources(brand_profile)
        
        # Deep multi-page analysis (new comprehensive feature)
        if DEEP_SCRAPING_AVAILABLE:
            print("   🔬 DEEP ANALYSIS: Scanning multiple pages for comprehensive insights...")
            print("   📄 This includes: About, Products, Pricing, Blog, Team, Case Studies")
            if progress_callback:
                progress_callback(f"Deep analysis: {brand_profile['company_name']}")
            brand_profile = enhance_brand_analysis_with_deep_scraping(brand_profile, progress_callback)
            print("   ✅ Deep multi-page analysis complete")
        else:
            print("   ⚠️ Deep scraping not available - using homepage analysis only")
        
        return brand_profile
    
    def _enhance_missing_data_with_ai(self, brand_profile, html_content):
        """Use AI to fill in missing data gaps"""
        missing_data = []
        
        # Check what's missing
        if not brand_profile['comprehensive_content']['hero_sections']:
            missing_data.append('hero_messaging')
        if not brand_profile['product_portfolio']['main_products']:
            missing_data.append('product_portfolio')
        if not brand_profile['strategic_messaging']['taglines']:
            missing_data.append('value_propositions')
        if not brand_profile['comprehensive_content']['value_propositions']:
            missing_data.append('key_differentiators')
        
        if missing_data:
            print(f"      📝 Missing data detected: {', '.join(missing_data)}")
            print(f"      🔍 Using AI to extract missing information...")
            
            # Extract text content for AI analysis
            soup = BeautifulSoup(html_content, 'html.parser')
            full_text = soup.get_text(separator=' ', strip=True)[:5000]  # First 5000 chars
            
            # Create AI prompt to extract missing data - REAL DATA ONLY
            missing_data_prompt = f"""
You are a professional web content analyst. Extract ONLY real, actual information that is explicitly stated in the website content.

CRITICAL: Do NOT create, infer, or make up ANY information. Extract ONLY what is literally written on the website.

COMPANY: {brand_profile['company_name']}
URL: {brand_profile['url']}

WEBSITE CONTENT:
{full_text}

MISSING DATA TO EXTRACT: {', '.join(missing_data)}

INSTRUCTIONS:
1. Extract ONLY text that appears exactly on the website
2. Use direct quotes from the content when possible
3. If information is not explicitly stated, return empty array [] or "Not found on website"
4. Do NOT infer, assume, or create any information

Return JSON format:
{{
    "hero_messaging": ["Exact headline text from website", "Exact subheading text"],
    "product_portfolio": ["Exact product names mentioned", "Exact service names listed"],
    "value_propositions": ["Exact value statements from site", "Exact benefit claims"],
    "key_differentiators": ["Exact competitive claims made", "Exact unique features mentioned"],
    "positioning_statement": "Exact description found on website or 'Not found on website'",
    "target_audience": "Exact customer descriptions mentioned or 'Not found on website'",
    "business_model": "Exact pricing/business model mentioned or 'Not found on website'"
}}

REMEMBER: Extract ONLY real, actual content from the website. No assumptions, no inferences, no made-up data.
"""
            
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You are a professional web content analyst who extracts specific information from website content. Always return valid JSON."},
                        {"role": "user", "content": missing_data_prompt}
                    ],
                    temperature=0.1,
                    max_tokens=1500
                )
                
                ai_content = response['choices'][0]['message']['content'].strip()
                ai_content = re.sub(r"```(json)?", "", ai_content).strip()
                
                if '{' in ai_content:
                    start = ai_content.find('{')
                    end = ai_content.rfind('}') + 1
                    json_content = ai_content[start:end]
                    ai_data = json.loads(json_content)
                    
                    # Fill in missing data - ONLY real data validation
                    def is_real_data(items):
                        """Validate that data is real, not generic/fake"""
                        if not items:
                            return False
                        generic_terms = ['not found', 'not available', 'not clearly', 'product 1', 'service 1', 'solution 1', 'platform', 'software', 'technology']
                        for item in items:
                            if any(term in item.lower() for term in generic_terms):
                                return False
                            if len(item.strip()) < 5:  # Too short to be real
                                return False
                        return True
                    
                    if 'hero_messaging' in missing_data and ai_data.get('hero_messaging'):
                        real_hero = [item for item in ai_data['hero_messaging'] if 'not found' not in item.lower() and len(item.strip()) > 10]
                        if real_hero and is_real_data(real_hero):
                            brand_profile['comprehensive_content']['hero_sections'].extend(real_hero)
                            print(f"         ✅ Added real hero messaging: {len(real_hero)} items")
                        else:
                            print(f"         ⚠️ Hero messaging not found on website")
                    
                    if 'product_portfolio' in missing_data and ai_data.get('product_portfolio'):
                        real_products = [item for item in ai_data['product_portfolio'] if 'not found' not in item.lower() and len(item.strip()) > 3]
                        if real_products and is_real_data(real_products):
                            brand_profile['product_portfolio']['main_products'].extend(real_products)
                            print(f"         ✅ Added real products: {len(real_products)} items")
                        else:
                            print(f"         ⚠️ Products not clearly specified on website")
                    
                    if 'value_propositions' in missing_data and ai_data.get('value_propositions'):
                        real_props = [item for item in ai_data['value_propositions'] if 'not found' not in item.lower() and len(item.strip()) > 15]
                        if real_props and is_real_data(real_props):
                            brand_profile['comprehensive_content']['value_propositions'].extend(real_props)
                            print(f"         ✅ Added real value propositions: {len(real_props)} items")
                        else:
                            print(f"         ⚠️ Value propositions not clearly stated on website")
                    
                    if 'key_differentiators' in missing_data and ai_data.get('key_differentiators'):
                        real_diff = [item for item in ai_data['key_differentiators'] if 'not found' not in item.lower() and len(item.strip()) > 10]
                        if real_diff and is_real_data(real_diff):
                            brand_profile['strategic_messaging']['competitive_claims'].extend(real_diff)
                            print(f"         ✅ Added real differentiators: {len(real_diff)} items")
                        else:
                            print(f"         ⚠️ Differentiators not explicitly stated on website")
                    
                    # Add additional extracted info - only if real
                    if ai_data.get('positioning_statement') and 'not found' not in ai_data['positioning_statement'].lower():
                        brand_profile['ai_extracted_positioning'] = ai_data['positioning_statement']
                        print(f"         ✅ Added positioning statement from website")
                    if ai_data.get('target_audience') and 'not found' not in ai_data['target_audience'].lower():
                        brand_profile['ai_extracted_audience'] = ai_data['target_audience']
                        print(f"         ✅ Added target audience from website")
                    if ai_data.get('business_model') and 'not found' not in ai_data['business_model'].lower():
                        brand_profile['business_model']['ai_detected_model'] = ai_data['business_model']
                        print(f"         ✅ Added business model from website")
                    
                    print(f"      ✅ AI enhancement complete")
                
            except Exception as e:
                print(f"      ❌ AI enhancement failed: {e}")
        else:
            print(f"      ✅ No missing data detected")
        
        return brand_profile
    
    def _search_external_sources(self, brand_profile):
        """Search external sources for additional company information"""
        company_name = brand_profile['company_name']
        
        # Identify what additional information we need
        needs_products = len(brand_profile['product_portfolio']['main_products']) < 3
        needs_positioning = len(brand_profile['comprehensive_content']['hero_sections']) < 2
        needs_business_info = not brand_profile.get('ai_extracted_positioning')
        
        if needs_products or needs_positioning or needs_business_info:
            print(f"      🔍 Searching for external information about {company_name}...")
            
            # Create search queries for external information
            search_queries = []
            if needs_products:
                search_queries.append(f"{company_name} products services offerings portfolio")
            if needs_positioning:
                search_queries.append(f"{company_name} company overview what does description")
            if needs_business_info:
                search_queries.append(f"{company_name} business model revenue funding investors")
            
            # Use AI to search for and extract external information
            external_info = self._ai_external_research(company_name, search_queries, brand_profile['url'])
            
            if external_info:
                # Merge external information with existing profile
                if external_info.get('products') and needs_products:
                    new_products = [p for p in external_info['products'] if p not in brand_profile['product_portfolio']['main_products']]
                    brand_profile['product_portfolio']['main_products'].extend(new_products[:5])
                    if new_products:
                        print(f"         ✅ Added {len(new_products)} products from external sources")
                
                if external_info.get('positioning') and needs_positioning:
                    brand_profile['comprehensive_content']['hero_sections'].extend(external_info['positioning'][:3])
                    print(f"         ✅ Added positioning info from external sources")
                
                if external_info.get('business_info'):
                    brand_profile['external_business_info'] = external_info['business_info']
                    print(f"         ✅ Added business information from external sources")
                
                if external_info.get('competitive_info'):
                    brand_profile['external_competitive_context'] = external_info['competitive_info']
                    print(f"         ✅ Added competitive context from external sources")
        else:
            print(f"      ✅ Sufficient data available, external search not needed")
        
        return brand_profile
    
    def _ai_external_research(self, company_name, search_queries, company_url):
        """Use AI to research external information about the company"""
        research_prompt = f"""
You are a business research analyst with access to general business knowledge. Research and provide factual information about this company.

COMPANY: {company_name}
WEBSITE: {company_url}
RESEARCH FOCUS: {', '.join(search_queries)}

Based on your knowledge of this company from public sources, provide factual information in this JSON format:

{{
    "products": ["Actual product names", "Real service offerings", "Known solutions"],
    "positioning": ["Company mission statement", "Known value propositions", "Public positioning statements"],
    "business_info": {{
        "industry": "Specific industry classification",
        "business_model": "Known revenue model",
        "target_market": "Known customer segments",
        "company_size": "Estimated employee count or size category",
        "founding_info": "Year founded and key facts"
    }},
    "competitive_info": {{
        "main_competitors": ["Known direct competitors"],
        "market_position": "Market leader/challenger/niche position",
        "key_differentiators": ["Known competitive advantages"]
    }},
    "recent_developments": ["Recent news, funding, partnerships, product launches"]
}}

CRITICAL INSTRUCTIONS:
1. Provide ONLY factual information you are confident about
2. Use "Unknown" or empty arrays [] if information is not available
3. Do NOT make up or infer information
4. Base answers on your training data knowledge of this company
5. Be specific and factual, not generic

Focus on providing accurate, verifiable information about {company_name}.
"""
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a business research analyst who provides only factual, verifiable information from your knowledge base. Never make up or infer information."},
                    {"role": "user", "content": research_prompt}
                ],
                temperature=0.1,
                max_tokens=2000
            )
            
            ai_content = response["choices"][0]["message"]["content"].strip()
            ai_content = re.sub(r"```(json)?", "", ai_content).strip()
            
            if '{' in ai_content:
                start = ai_content.find('{')
                end = ai_content.rfind('}') + 1
                json_content = ai_content[start:end]
                external_data = json.loads(json_content)
                
                # Validate that the data is real (not "Unknown" or generic)
                def clean_external_data(data):
                    if isinstance(data, list):
                        return [item for item in data if item and item != "Unknown" and len(item) > 5]
                    elif isinstance(data, dict):
                        return {k: clean_external_data(v) for k, v in data.items() if v and v != "Unknown"}
                    elif isinstance(data, str):
                        return data if data != "Unknown" and len(data) > 5 else None
                    return data
                
                cleaned_data = clean_external_data(external_data)
                return cleaned_data if cleaned_data else None
                
        except Exception as e:
            print(f"         ❌ External research failed: {e}")
            return None
    
    def _extract_comprehensive_website_content(self, soup, url):
        """Extract comprehensive website content for deep analysis"""
        content = {
            "full_text": soup.get_text(separator=' ', strip=True),
            "page_title": soup.find('title').get_text() if soup.find('title') else "",
            "meta_description": "",
            "hero_sections": [],
            "value_propositions": [],
            "feature_descriptions": [],
            "customer_testimonials": [],
            "case_studies": [],
            "pricing_content": [],
            "about_content": [],
            "team_content": [],
            "blog_content": [],
            "footer_content": [],
            "navigation_structure": []
        }
        
        # Meta description
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc:
            content["meta_description"] = meta_desc.get('content', '')
        
        # Hero sections and main messaging - enhanced selectors
        hero_selectors = [
            'h1', 'h2', '.hero', '[class*="hero"]', '.banner', '[class*="banner"]',
            '.jumbotron', '.main-header', '.page-header', '.intro', '[class*="intro"]',
            '.headline', '[class*="headline"]', '.title', '[class*="title"]',
            'main h1', 'main h2', 'section h1', 'section h2'
        ]
        for selector in hero_selectors:
            elements = soup.select(selector)
            for elem in elements:
                text = elem.get_text(strip=True)
                if len(text) > 15 and len(text) < 500:
                    content["hero_sections"].append(text)
        
        # If no hero sections found, try broader search
        if not content["hero_sections"]:
            fallback_selectors = ['p', 'div']
            for selector in fallback_selectors:
                elements = soup.select(selector)[:10]  # Only check first 10
                for elem in elements:
                    text = elem.get_text(strip=True)
                    if 50 < len(text) < 300 and not any(skip in text.lower() for skip in ['cookie', 'privacy', 'terms']):
                        content["hero_sections"].append(text)
                        if len(content["hero_sections"]) >= 3:
                            break
                if content["hero_sections"]:
                    break
        
        # Value propositions and key messaging
        value_prop_selectors = [
            'h2', 'h3', '.value-prop', '[class*="value"]', '.benefit', '[class*="benefit"]',
            '.feature-title', '.advantage', '[class*="advantage"]', '.unique', '[class*="unique"]'
        ]
        for selector in value_prop_selectors:
            elements = soup.select(selector)
            for elem in elements:
                text = elem.get_text(strip=True)
                if 30 < len(text) < 300:
                    content["value_propositions"].append(text)
        
        # Feature descriptions
        feature_selectors = [
            '.feature', '[class*="feature"]', '.capability', '[class*="capability"]',
            '.service', '[class*="service"]', '.solution', '[class*="solution"]'
        ]
        for selector in feature_selectors:
            elements = soup.select(selector)
            for elem in elements:
                text = elem.get_text(strip=True)
                if 50 < len(text) < 800:
                    content["feature_descriptions"].append(text)
        
        # Customer testimonials
        testimonial_selectors = [
            '.testimonial', '[class*="testimonial"]', '.review', '[class*="review"]',
            '.quote', '[class*="quote"]', '.customer-story', '[class*="customer"]'
        ]
        for selector in testimonial_selectors:
            elements = soup.select(selector)
            for elem in elements:
                text = elem.get_text(strip=True)
                if 50 < len(text) < 1000:
                    content["customer_testimonials"].append(text)
        
        # Case studies
        case_study_selectors = [
            '.case-study', '[class*="case"]', '.success-story', '[class*="success"]',
            '.use-case', '[class*="use-case"]'
        ]
        for selector in case_study_selectors:
            elements = soup.select(selector)
            for elem in elements:
                text = elem.get_text(strip=True)
                if 100 < len(text) < 2000:
                    content["case_studies"].append(text)
        
        # Pricing content
        pricing_selectors = [
            '.pricing', '[class*="pricing"]', '.price', '[class*="price"]',
            '.plan', '[class*="plan"]', '.cost', '[class*="cost"]'
        ]
        for selector in pricing_selectors:
            elements = soup.select(selector)
            for elem in elements:
                text = elem.get_text(strip=True)
                if 20 < len(text) < 500:
                    content["pricing_content"].append(text)
        
        # About content
        about_selectors = [
            '.about', '[class*="about"]', '.company', '[class*="company"]',
            '.mission', '[class*="mission"]', '.vision', '[class*="vision"]'
        ]
        for selector in about_selectors:
            elements = soup.select(selector)
            for elem in elements:
                text = elem.get_text(strip=True)
                if 100 < len(text) < 2000:
                    content["about_content"].append(text)
        
        # Navigation structure
        nav_selectors = ['nav a', '.nav a', 'header a', '.menu a', '.navigation a']
        for selector in nav_selectors:
            elements = soup.select(selector)
            for elem in elements:
                text = elem.get_text(strip=True)
                if 2 < len(text) < 50:
                    content["navigation_structure"].append(text)
        
        return content
    
    def _extract_strategic_messaging(self, soup):
        """Extract strategic messaging and positioning elements"""
        messaging = {
            "taglines": [],
            "value_statements": [],
            "competitive_claims": [],
            "target_audience_indicators": [],
            "use_case_mentions": [],
            "industry_focus": [],
            "technology_mentions": []
        }
        
        # Taglines and slogans
        tagline_selectors = [
            '.tagline', '.slogan', '.motto', '[class*="tagline"]', '[class*="slogan"]'
        ]
        for selector in tagline_selectors:
            elements = soup.select(selector)
            for elem in elements:
                text = elem.get_text(strip=True)
                if 5 < len(text) < 100:
                    messaging["taglines"].append(text)
        
        # Look for competitive language
        competitive_keywords = [
            'leading', 'best', 'top', 'first', 'only', 'unique', 'unlike',
            'better than', 'superior', 'advanced', 'innovative', 'revolutionary'
        ]
        
        all_text = soup.get_text().lower()
        for keyword in competitive_keywords:
            if keyword in all_text:
                # Find sentences containing these keywords
                sentences = re.split(r'[.!?]', soup.get_text())
                for sentence in sentences:
                    if keyword in sentence.lower() and 10 < len(sentence.strip()) < 200:
                        messaging["competitive_claims"].append(sentence.strip())
        
        # Target audience indicators
        audience_keywords = [
            'enterprise', 'small business', 'startup', 'developer', 'healthcare',
            'education', 'finance', 'retail', 'manufacturing', 'professional'
        ]
        for keyword in audience_keywords:
            if keyword in all_text:
                messaging["target_audience_indicators"].append(keyword)
        
        return messaging
    
    def _extract_product_portfolio(self, soup):
        """Extract product/service portfolio information"""
        portfolio = {
            "main_products": [],
            "service_categories": [],
            "feature_lists": [],
            "integration_mentions": [],
            "platform_capabilities": []
        }
        
        # Product names and categories - enhanced extraction
        product_selectors = [
            '.product', '[class*="product"]', '.solution', '[class*="solution"]',
            '.service', '[class*="service"]', '.offering', '[class*="offering"]',
            '.feature', '[class*="feature"]', '.capability', '[class*="capability"]',
            'nav a', '.nav a', '.menu a'  # Navigation often contains product names
        ]
        
        for selector in product_selectors:
            elements = soup.select(selector)
            for elem in elements:
                # Get product title from various elements
                title_elem = elem.find(['h1', 'h2', 'h3', 'h4', 'h5', 'a'])
                if title_elem:
                    title = title_elem.get_text(strip=True)
                    if 3 < len(title) < 50 and title not in portfolio["main_products"]:
                        portfolio["main_products"].append(title)
                
                # Also try just the element text itself for navigation items
                if selector in ['nav a', '.nav a', '.menu a']:
                    text = elem.get_text(strip=True)
                    if 3 < len(text) < 30 and text not in portfolio["main_products"]:
                        # Filter out common navigation items
                        skip_terms = ['home', 'about', 'contact', 'login', 'sign up', 'privacy', 'terms', 'blog', 'news']
                        if not any(skip in text.lower() for skip in skip_terms):
                            portfolio["main_products"].append(text)
                
                # Get product description
                text = elem.get_text(strip=True)
                if 50 < len(text) < 1000:
                    portfolio["service_categories"].append(text)
        
        # If no products found, extract from meta description or title
        if not portfolio["main_products"]:
            meta_desc = soup.find('meta', attrs={'name': 'description'})
            if meta_desc:
                desc_text = meta_desc.get('content', '')
                # Extract potential product names from description
                words = desc_text.split()
                for i, word in enumerate(words):
                    if word.lower() in ['platform', 'solution', 'software', 'tool', 'system', 'service']:
                        if i > 0:
                            potential_product = ' '.join(words[max(0, i-2):i+1])
                            if 5 < len(potential_product) < 30:
                                portfolio["main_products"].append(potential_product)
        
        return portfolio
    
    def _extract_comprehensive_visual_identity(self, html_content, url):
        """Extract comprehensive visual identity elements"""
        soup = BeautifulSoup(html_content, 'html.parser')
        visual_identity = {
            "logos": [],
            "color_palette": [],
            "fonts": [],
            "visual_style_indicators": [],
            "image_types": []
        }
        
        # Extract logos
        visual_identity["logos"] = self._extract_logos_comprehensive(html_content, url)
        
        # Extract colors
        visual_identity["color_palette"] = self._extract_colors_comprehensive(html_content, url)
        
        # Extract font information
        style_tags = soup.find_all('style')
        for style_tag in style_tags:
            css_content = style_tag.get_text()
            font_families = re.findall(r'font-family:\s*([^;]+)', css_content)
            visual_identity["fonts"].extend(font_families)
        
        return visual_identity
    
    def _enhance_color_analysis(self, visual_identity, html_content, url):
        """Enhanced color analysis using AI to identify brand colors from visual elements"""
        current_colors = visual_identity.get('color_palette', [])
        
        # Check if we only have generic colors (greys, whites, blacks)
        generic_colors = ['#666666', '#999999', '#cccccc', '#e9ecef', '#f8f9fa', '#ffffff', '#000000', '#333333']
        is_generic = all(color in generic_colors for color in current_colors)
        
        if is_generic or len(current_colors) < 3:
            print("      🔍 Generic colors detected, performing enhanced color analysis...")
            
            # Use AI to analyze the visual content for brand colors
            enhanced_colors = self._ai_visual_color_analysis(html_content, url)
            if enhanced_colors:
                visual_identity['color_palette'] = enhanced_colors
                print(f"         ✅ Enhanced color palette extracted: {len(enhanced_colors)} colors")
            else:
                print("         ⚠️ Could not extract enhanced colors, keeping existing")
        
        return visual_identity
    
    def _ai_visual_color_analysis(self, html_content, url):
        """Use AI to analyze visual elements and extract brand colors"""
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Extract CSS content more thoroughly
        css_content = ""
        
        # Get all style tags
        for style_tag in soup.find_all('style'):
            css_content += style_tag.get_text() + "\n"
        
        # Get inline styles from key elements
        key_elements = soup.find_all(['header', 'nav', 'button', 'a', 'div'], class_=True)
        inline_styles = []
        for elem in key_elements[:20]:  # Limit to first 20 for performance
            style = elem.get('style', '')
            if style:
                inline_styles.append(f"{elem.name}.{' '.join(elem.get('class', []))}: {style}")
        
        # Get key visual elements for analysis
        visual_context = {
            'page_title': soup.find('title').get_text() if soup.find('title') else '',
            'headers': [h.get_text().strip() for h in soup.find_all(['h1', 'h2'])[:5]],
            'nav_items': [a.get_text().strip() for a in soup.select('nav a, .nav a')[:10]],
            'button_text': [btn.get_text().strip() for btn in soup.find_all('button')[:5]]
        }
        
        color_analysis_prompt = f"""
You are a brand color analyst examining a website to extract the primary brand color palette.

WEBSITE: {url}
VISUAL CONTEXT: {visual_context}

CSS CONTENT (first 2000 chars):
{css_content[:2000]}

INLINE STYLES:
{chr(10).join(inline_styles[:10])}

Analyze the visual design and extract the brand's primary color palette. Look for:
1. Header/navigation colors
2. Button and link colors  
3. Brand accent colors
4. Background colors (non-white/grey)
5. Text colors (beyond black/grey)

Return ONLY the hex color codes in this JSON format:
{{
    "primary_colors": ["#color1", "#color2", "#color3"],
    "secondary_colors": ["#color4", "#color5"],
    "accent_colors": ["#color6"]
}}

CRITICAL INSTRUCTIONS:
1. Extract ONLY colors that appear to be intentional brand colors
2. Exclude pure white (#ffffff), pure black (#000000), and generic greys
3. Look for colors used in logos, buttons, links, headers, and key UI elements
4. Return empty arrays if no brand colors are found
5. Ensure all color codes are valid hex format (#RRGGBB)

Focus on colors that represent the brand identity, not just any color on the page.
"""
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a professional brand color analyst who extracts brand color palettes from website CSS and visual elements. Always return valid JSON with hex colors."},
                    {"role": "user", "content": color_analysis_prompt}
                ],
                temperature=0.1,
                max_tokens=1000
            )
            
            ai_content = response["choices"][0]["message"]["content"].strip()
            ai_content = re.sub(r"```(json)?", "", ai_content).strip()
            
            if '{' in ai_content:
                start = ai_content.find('{')
                end = ai_content.rfind('}') + 1
                json_content = ai_content[start:end]
                color_data = json.loads(json_content)
                
                # Combine all colors and validate
                all_colors = []
                for color_group in ['primary_colors', 'secondary_colors', 'accent_colors']:
                    colors = color_data.get(color_group, [])
                    for color in colors:
                        if self._is_valid_hex_color(color) and color not in all_colors:
                            all_colors.append(color)
                
                return all_colors[:6] if all_colors else None
                
        except Exception as e:
            print(f"         ❌ AI color analysis failed: {e}")
            return None
    
    def _is_valid_hex_color(self, color_string):
        """Validate hex color format"""
        if not color_string or not color_string.startswith('#'):
            return False
        if len(color_string) != 7:
            return False
        try:
            int(color_string[1:], 16)
            return True
        except ValueError:
            return False
    
    def _search_brand_guidelines(self, base_url, company_name):
        """Search for brand guidelines and style guides"""
        print(f"         🔍 Searching for brand guidelines for {company_name}...")
        
        # Common brand guideline URLs to try
        guideline_paths = [
            '/brand-guidelines',
            '/brand-guide',
            '/style-guide',
            '/brand-assets',
            '/brand',
            '/media-kit',
            '/press-kit',
            '/brand-center',
            '/brand-resources',
            '/design-system',
            '/brand-identity'
        ]
        
        domain = base_url.rstrip('/')
        found_guidelines = []
        
        for path in guideline_paths:
            try:
                test_url = f"{domain}{path}"
                response = self.session.get(test_url, timeout=10)
                if response.status_code == 200:
                    # Check if this looks like a brand guidelines page
                    content_lower = response.text.lower()
                    if any(term in content_lower for term in ['brand guide', 'style guide', 'brand color', 'logo download', 'brand asset']):
                        found_guidelines.append({
                            'url': test_url,
                            'type': 'brand_guidelines'
                        })
                        print(f"            ✅ Found brand guidelines: {test_url}")
                        
                        # Extract colors from brand guidelines
                        guidelines_colors = self._extract_colors_from_guidelines(response.text)
                        if guidelines_colors:
                            found_guidelines[-1]['colors'] = guidelines_colors
                            print(f"            🎨 Extracted {len(guidelines_colors)} colors from guidelines")
            except:
                continue
        
        # Also use AI to search for brand guideline information
        if not found_guidelines:
            ai_guidelines = self._ai_search_brand_guidelines(company_name, base_url)
            if ai_guidelines:
                found_guidelines.append(ai_guidelines)
        
        return found_guidelines if found_guidelines else None
    
    def _extract_colors_from_guidelines(self, guidelines_html):
        """Extract colors specifically from brand guidelines pages"""
        soup = BeautifulSoup(guidelines_html, 'html.parser')
        
        # Look for color swatches, color codes, and color-related content
        colors = set()
        
        # Search for hex colors in text content
        hex_pattern = r'#[0-9a-fA-F]{6}'
        hex_colors = re.findall(hex_pattern, guidelines_html)
        colors.update(hex_colors)
        
        # Search for RGB values
        rgb_pattern = r'rgb\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)'
        rgb_matches = re.findall(rgb_pattern, guidelines_html)
        for r, g, b in rgb_matches:
            hex_color = f"#{int(r):02x}{int(g):02x}{int(b):02x}"
            colors.add(hex_color)
        
        # Look for CSS custom properties (variables) that might contain colors
        css_var_pattern = r'--[^:]+:\s*(#[0-9a-fA-F]{6}|rgb\([^)]+\))'
        css_var_matches = re.findall(css_var_pattern, guidelines_html)
        for color in css_var_matches:
            if color.startswith('#'):
                colors.add(color)
        
        # Filter out common non-brand colors
        brand_colors = []
        exclude_colors = {'#ffffff', '#000000', '#cccccc', '#999999', '#666666', '#333333'}
        
        for color in colors:
            if color not in exclude_colors and len(color) == 7:
                brand_colors.append(color)
        
        return brand_colors[:8] if brand_colors else None
    
    def _ai_search_brand_guidelines(self, company_name, website_url):
        """Use AI knowledge to find brand guideline information"""
        guidelines_prompt = f"""
Based on your knowledge, does {company_name} (website: {website_url}) have publicly available brand guidelines, style guides, or brand color information?

If you know of specific brand colors, guidelines, or visual identity information for this company, provide it in this JSON format:

{{
    "has_guidelines": true/false,
    "known_brand_colors": ["#color1", "#color2", "#color3"],
    "brand_guideline_info": "Brief description of their brand identity if known",
    "typical_guideline_locations": ["Common URL paths where their guidelines might be found"]
}}

Provide ONLY factual information you are confident about. If you don't have specific knowledge about {company_name}'s brand guidelines, return has_guidelines: false.
"""
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a brand research specialist with knowledge of corporate brand guidelines and visual identities."},
                    {"role": "user", "content": guidelines_prompt}
                ],
                temperature=0.1,
                max_tokens=800
            )
            
            ai_content = response["choices"][0]["message"]["content"].strip()
            ai_content = re.sub(r"```(json)?", "", ai_content).strip()
            
            if '{' in ai_content:
                start = ai_content.find('{')
                end = ai_content.rfind('}') + 1
                json_content = ai_content[start:end]
                guideline_data = json.loads(json_content)
                
                if guideline_data.get('has_guidelines') and guideline_data.get('known_brand_colors'):
                    print(f"            ✅ Found known brand colors from AI knowledge")
                    return {
                        'type': 'ai_knowledge',
                        'colors': guideline_data['known_brand_colors'],
                        'info': guideline_data.get('brand_guideline_info', '')
                    }
            
        except Exception as e:
            print(f"            ⚠️ AI brand guidelines search failed: {e}")
        
        return None
    
    def _extract_business_model_indicators(self, soup):
        """Extract business model and pricing indicators"""
        business_model = {
            "pricing_model": "unknown",
            "pricing_indicators": [],
            "trial_offers": [],
            "subscription_mentions": [],
            "enterprise_focus": False,
            "self_service_indicators": []
        }
        
        text_content = soup.get_text().lower()
        
        # Pricing model indicators
        if any(term in text_content for term in ['subscription', 'monthly', 'annual', 'per month']):
            business_model["pricing_model"] = "subscription"
        elif any(term in text_content for term in ['one-time', 'perpetual', 'license']):
            business_model["pricing_model"] = "one-time"
        elif any(term in text_content for term in ['free', 'freemium', 'free tier']):
            business_model["pricing_model"] = "freemium"
        
        # Enterprise focus
        if any(term in text_content for term in ['enterprise', 'custom pricing', 'contact sales']):
            business_model["enterprise_focus"] = True
        
        return business_model
    
    def _extract_partnership_indicators(self, soup):
        """Extract partnership and integration information"""
        partnerships = {
            "technology_partners": [],
            "integration_mentions": [],
            "marketplace_presence": [],
            "certification_mentions": []
        }
        
        # Look for partner logos and mentions
        partner_selectors = [
            '.partner', '[class*="partner"]', '.integration', '[class*="integration"]',
            '.marketplace', '[class*="marketplace"]'
        ]
        
        for selector in partner_selectors:
            elements = soup.select(selector)
            for elem in elements:
                text = elem.get_text(strip=True)
                if 5 < len(text) < 200:
                    partnerships["technology_partners"].append(text)
        
        return partnerships
    
    def _extract_company_name(self, soup, url):
        """Extract company name from various sources"""
        # Try title tag first
        title_tag = soup.find('title')
        if title_tag:
            title_text = title_tag.get_text()
            # Remove common suffixes
            for suffix in [' | Home', ' - Home', ' | Official Site', ' - Official Site']:
                title_text = title_text.replace(suffix, '')
            if len(title_text) < 50:
                return title_text
        
        # Try h1 tags
        h1_tags = soup.find_all('h1')
        for h1 in h1_tags:
            text = h1.get_text(strip=True)
            if 5 < len(text) < 30:
                return text
        
        # Fallback to domain name
        domain = urlparse(url).netloc
        return domain.replace('www.', '').replace('.com', '').title()
    
    def get_comprehensive_competitive_analysis(self, brand_data, all_competitors_data):
        """Generate comprehensive McKinsey-level competitive analysis"""
        
        comprehensive_prompt = f"""
You are a senior strategy consultant at McKinsey & Company conducting a detailed competitive intelligence analysis. 

BRAND TO ANALYZE: {brand_data['company_name']}
COMPETITOR SET: {[comp['company_name'] for comp in all_competitors_data if comp['company_name'] != brand_data['company_name']]}

TASK: Provide a comprehensive strategic analysis with specific, actionable insights.

## 1. STRATEGIC POSITIONING ANALYSIS
Analyze this brand's positioning strategy by examining their messaging, value propositions, and market approach:

**Website Content**: {' '.join(brand_data['comprehensive_content']['hero_sections'][:5])}
**Key Messages**: {' '.join(brand_data['comprehensive_content']['value_propositions'][:8])}
**Product Portfolio**: {' '.join(brand_data['product_portfolio']['main_products'][:5])}

Determine:
- **Primary Positioning Strategy**: Cost leadership, differentiation, focus, or hybrid? Provide specific evidence from their content.
- **Target Customer Segment**: Who exactly are they targeting? (job titles, company sizes, specific use cases based on their messaging)
- **Value Proposition Strength**: Rate 1-10 with specific reasoning based on clarity, uniqueness, and credibility
- **Positioning Credibility**: What specific evidence supports their claims? Quote their actual content.
- **Unique Differentiators**: What specific advantages do they claim vs competitors? Use exact quotes.

## 2. COMPETITIVE DIFFERENTIATION ANALYSIS
Compare against these competitors with their positioning:
{chr(10).join([f"**{comp['company_name']}**: {' '.join(comp['comprehensive_content']['hero_sections'][:2])}" for comp in all_competitors_data if comp['company_name'] != brand_data['company_name']])}

Identify:
- **Head-to-Head Competitors**: Which brands compete most directly and why? Provide specific evidence.
- **Differentiation Gaps**: What does this brand offer that others don't? Be specific with features/capabilities.
- **Vulnerability Points**: Where are they weakest vs competitors? What do competitors offer that they don't?
- **Competitive Moats**: What sustainable advantages do they have? Technology, partnerships, market position?
- **Positioning Overlap**: Which competitors have similar messaging? Quote similar language.

## 3. DETAILED SWOT ANALYSIS
Generate specific, evidence-based SWOT points (not generic business advice):

**STRENGTHS** (Find 4-5 specific advantages):
- Analyze: unique capabilities, market position, technology, partnerships, brand recognition
- Provide evidence from their website content with specific quotes
- Rate impact: High/Medium/Low

**WEAKNESSES** (Identify 3-4 specific vulnerabilities):
- Look for: messaging gaps, missing capabilities, positioning problems, feature gaps
- Compare to competitor strengths and identify what they lack
- Rate severity: High/Medium/Low

**OPPORTUNITIES** (Find 3-4 specific market opportunities):
- Analyze: underserved segments, technology trends, competitor gaps, market expansion
- Focus on actionable opportunities based on their current capabilities
- Rate potential: High/Medium/Low

**THREATS** (Identify 3-4 specific competitive threats):
- Look for: competitor strengths, market trends, disruption risks, competitive pressure
- Be specific about which competitors pose threats and why
- Rate likelihood: High/Medium/Low

## 4. BRAND HEALTH SCORING
Provide detailed scoring (1-100) with methodology:

**Brand Clarity Score** (/25): How clear and compelling is their value proposition? Quote specific examples.
**Differentiation Score** (/25): How unique is their positioning vs competitors? Provide comparative analysis.
**Market Fit Score** (/25): How well-aligned with target market needs? Evidence from their messaging.
**Execution Score** (/25): How well do they deliver on their brand promise? Evidence from website quality, content depth.

**Total Brand Health Score**: /100
**Threat Level**: High/Medium/Low with specific reasoning

## 5. STRATEGIC RECOMMENDATIONS
Based on your analysis, provide specific, actionable recommendations:

**Key Strategic Vulnerabilities**: What could competitors exploit? How?
**Defensive Strategies**: How should they protect their position? Specific actions.
**Growth Opportunities**: Where could they expand or improve? Market segments, features, partnerships.
**Competitive Response**: How might they respond to competitive threats? Strategic moves.
**Innovation Priorities**: What should they focus on to maintain competitive advantage?

## 6. MARKET INTELLIGENCE INSIGHTS
Provide specific insights about:

**Pricing Strategy Implications**: Premium, value, or competitive pricing based on positioning evidence
**Innovation Focus Areas**: What technologies/features are they emphasizing? Evidence from content.
**Customer Acquisition Strategy**: How do they attract customers based on messaging and content?
**Partnership Strategy**: What types of partnerships would fit their positioning? Evidence from current partners.
**Market Expansion Opportunities**: Based on their capabilities and positioning, where could they expand?

## OUTPUT FORMAT REQUIREMENTS:
- Be specific and actionable, not generic business consulting speak
- Provide evidence and quotes for all claims
- Use competitive context in every insight
- Include specific examples from their content
- Rate confidence level (High/Medium/Low) for each major insight
- Focus on insights a business strategist would find immediately valuable
- Use data from their actual website content, not assumptions

BRAND COMPREHENSIVE CONTENT:
Hero Sections: {brand_data['comprehensive_content']['hero_sections']}
Value Propositions: {brand_data['comprehensive_content']['value_propositions']}
Features: {brand_data['comprehensive_content']['feature_descriptions'][:5]}
About Content: {brand_data['comprehensive_content']['about_content'][:3]}
Pricing Content: {brand_data['comprehensive_content']['pricing_content'][:3]}
"""

        return comprehensive_prompt
    
    def get_market_landscape_analysis(self, all_competitors_data):
        """Generate comprehensive market landscape analysis"""
        
        market_analysis_prompt = f"""
You are a senior market research analyst providing strategic market intelligence.

COMPETITIVE SET ANALYZED: {len(all_competitors_data)} major players
COMPETITOR PROFILES:
{chr(10).join([f"**{comp['company_name']}**: {' '.join(comp['comprehensive_content']['hero_sections'][:2])} | Products: {', '.join(comp['product_portfolio']['main_products'][:3])}" for comp in all_competitors_data])}

## COMPREHENSIVE MARKET LANDSCAPE ANALYSIS

### 1. COMPETITIVE INTENSITY ASSESSMENT
Analyze the competitive dynamics:
- **Market Concentration**: How concentrated is this market? (Fragmented/Moderate/Concentrated) - provide evidence
- **Competitive Dynamics**: Price competition, feature wars, or differentiation-based? Cite specific examples
- **Barriers to Entry**: What prevents new competitors from entering? Technology, partnerships, brand, capital?
- **Market Maturity**: Emerging, growth, mature, or declining stage? Evidence from messaging and positioning

### 2. STRATEGIC POSITIONING MAP ANALYSIS
Create a comprehensive positioning framework:
- **Primary Competitive Dimensions**: What are the 2-3 key factors that differentiate these brands? Provide evidence
- **Positioning Clusters**: Which brands compete in similar positioning territories? Group them and explain why
- **White Space Opportunities**: What positioning territories are unoccupied? Be specific about market gaps
- **Crowded Segments**: Where is competition most intense? Which brands are fighting for the same space?
- **Unique Positioning**: Which brand has the most differentiated position? Why?

### 3. MARKET OPPORTUNITY IDENTIFICATION
Based on competitive gap analysis:
- **Underserved Customer Segments**: What specific customer needs aren't being well addressed? Evidence from messaging gaps
- **Technology Gaps**: What capabilities are missing from current offerings? Compare feature sets
- **Messaging Gaps**: What value propositions aren't being claimed effectively? Identify opportunity areas
- **Geographic Opportunities**: Any regional market gaps based on company focus?
- **Vertical Market Opportunities**: Industry-specific needs not being addressed?

### 4. COMPREHENSIVE COMPETITIVE THREAT MATRIX
Rank each competitor by multiple threat dimensions:

For each competitor, analyze:
- **Market Position Threat**: Strong positioning and brand recognition
- **Innovation Threat**: Technology leadership and R&D capabilities
- **Customer Base Threat**: Strong customer relationships and switching costs
- **Financial Threat**: Resources for competitive moves and price wars
- **Partnership Threat**: Strategic alliances and ecosystem strength

**Overall Threat Ranking**: 1-{len(all_competitors_data)} with specific reasoning for each

### 5. STRATEGIC RECOMMENDATIONS FOR MARKET PARTICIPANTS

**For Market Leaders**: How to maintain position and fend off challengers
**For Challengers**: How to attack market leaders and gain share
**For Niche Players**: How to expand without triggering competitive response
**For New Entrants**: Optimal entry strategy based on current competitive gaps

### 6. MARKET EVOLUTION PREDICTIONS
Based on current positioning and trends:

**Likely Consolidation Scenarios**: Which brands might merge or be acquired? Why?
**Technology Disruption Threats**: What innovations could reshape competition? Evidence from current R&D focus
**Pricing Pressure Points**: Where is pricing competition likely to intensify? Why?
**New Entrant Threat Assessment**: What types of companies might enter this market? From which industries?
**Partnership Evolution**: How might strategic alliances reshape the competitive landscape?

### 7. ACTIONABLE STRATEGIC INSIGHTS

**Investment Priorities**: Where should market participants focus R&D and product development?
**Acquisition Targets**: What capabilities or companies should market leaders consider acquiring?
**Partnership Opportunities**: What strategic alliances would create competitive advantage?
**Market Expansion Strategies**: How can companies expand into adjacent markets or segments?

## OUTPUT FORMAT REQUIREMENTS:
- Provide specific, evidence-based insights with examples
- Quote actual messaging and positioning from competitors
- Rate confidence levels for predictions (High/Medium/Low)
- Focus on actionable strategic intelligence
- Avoid generic market analysis - be specific to this competitive set
- Include quantitative assessments where possible

COMPREHENSIVE COMPETITOR DATA FOR ANALYSIS:
{json.dumps([{
    'name': comp['company_name'],
    'hero_messaging': comp['comprehensive_content']['hero_sections'][:3],
    'value_props': comp['comprehensive_content']['value_propositions'][:5],
    'products': comp['product_portfolio']['main_products'][:5],
    'business_model': comp['business_model']['pricing_model'],
    'enterprise_focus': comp['business_model']['enterprise_focus']
} for comp in all_competitors_data], indent=2)}
"""

        return market_analysis_prompt
    
    def generate_strategic_brand_analysis(self, brand_data, all_competitors):
        """Generate McKinsey-level strategic analysis for individual brand"""
        print(f"🧠 Generating comprehensive strategic analysis for {brand_data['company_name']}...")
        
        brand_prompt = self.get_comprehensive_competitive_analysis(brand_data, all_competitors)
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a senior strategy consultant with 15+ years experience in competitive intelligence and market analysis. Provide detailed, evidence-based strategic insights."},
                    {"role": "user", "content": brand_prompt}
                ],
                temperature=0.2,  # Lower temperature for more consistent analysis
                max_tokens=4000   # Increased for comprehensive analysis
            )
            
            return response["choices"][0]["message"]["content"]
            
        except Exception as e:
            print(f"     ❌ Strategic analysis failed for {brand_data['company_name']}: {e}")
            return "Strategic analysis unavailable due to API error."
    
    def generate_market_intelligence(self, all_competitors):
        """Generate comprehensive market landscape intelligence"""
        print("🌐 Generating comprehensive market landscape analysis...")
        
        market_prompt = self.get_market_landscape_analysis(all_competitors)
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a senior market research analyst specializing in competitive landscape analysis with expertise in strategic intelligence."},
                    {"role": "user", "content": market_prompt}
                ],
                temperature=0.2,
                max_tokens=4000
            )
            
            return response["choices"][0]["message"]["content"]
            
        except Exception as e:
            print(f"     ❌ Market intelligence analysis failed: {e}")
            return "Market intelligence unavailable due to API error."
    
    # Include visual extraction methods from previous system
    def _extract_logos_comprehensive(self, html_content, base_url):
        """Extract logos with comprehensive search"""
        soup = BeautifulSoup(html_content, 'html.parser')
        logo_urls = []
        
        logo_selectors = [
            'img[alt*="logo" i]', 'img[src*="logo" i]', 'img[class*="logo" i]',
            '.logo img', '.header img', '.navbar img', '.brand img', 'header img'
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
        """Extract and process brand colors with improved accuracy"""
        soup = BeautifulSoup(html_content, 'html.parser')
        all_colors = set()
        color_frequency = defaultdict(int)
        
        # Extract colors from inline styles
        for element in soup.find_all(style=True):
            style = element.get('style', '')
            colors = re.findall(r'#[0-9a-fA-F]{6}|#[0-9a-fA-F]{3}|rgb\([^)]+\)|rgba\([^)]+\)', style)
            for color in colors:
                all_colors.add(color)
                color_frequency[color] += 1
        
        # Extract colors from style tags
        for style_tag in soup.find_all('style'):
            css_content = style_tag.get_text()
            colors = re.findall(r'#[0-9a-fA-F]{6}|#[0-9a-fA-F]{3}|rgb\([^)]+\)|rgba\([^)]+\)', css_content)
            for color in colors:
                all_colors.add(color)
                color_frequency[color] += 5  # Weight CSS colors higher
        
        # Try to extract colors from external CSS files
        try:
            for link in soup.find_all('link', {'rel': 'stylesheet'}):
                css_url = urljoin(url, link.get('href', ''))
                if css_url and css_url.endswith('.css'):
                    try:
                        css_response = self.session.get(css_url, timeout=5)
                        if css_response.status_code == 200:
                            css_content = css_response.text
                            colors = re.findall(r'#[0-9a-fA-F]{6}|#[0-9a-fA-F]{3}|rgb\([^)]+\)|rgba\([^)]+\)', css_content)
                            for color in colors:
                                all_colors.add(color)
                                color_frequency[color] += 3  # Weight external CSS colors
                    except:
                        continue
        except:
            pass
        
        # Sort colors by frequency to prioritize brand colors
        sorted_colors = sorted(color_frequency.items(), key=lambda x: x[1], reverse=True)
        prioritized_colors = [color for color, _ in sorted_colors]
        
        return self._process_colors(prioritized_colors)
    
    def _process_colors(self, color_list):
        """Process and return dominant colors"""
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
        """Capture screenshot for visual analysis with improved reliability"""
        max_retries = 3
        for retry in range(max_retries):
            try:
                chrome_options = Options()
                chrome_options.add_argument('--headless')
                chrome_options.add_argument('--no-sandbox')
                chrome_options.add_argument('--disable-dev-shm-usage')
                chrome_options.add_argument('--window-size=1920,1080')  # Larger size for better capture
                chrome_options.add_argument('--disable-web-security')
                chrome_options.add_argument('--disable-features=VizDisplayCompositor')
                chrome_options.add_argument('--disable-gpu')
                chrome_options.add_argument('--disable-software-rasterizer')
                chrome_options.add_argument('--disable-background-timer-throttling')
                chrome_options.add_argument('--disable-backgrounding-occluded-windows')
                chrome_options.add_argument('--disable-renderer-backgrounding')
                chrome_options.add_argument('--disable-extensions')
                chrome_options.add_argument('--disable-plugins')
                chrome_options.add_argument('--disable-default-apps')
                chrome_options.add_argument('--remote-debugging-port=9222')
                # Block common tracking and cookie dialogs
                chrome_options.add_argument('--disable-popup-blocking')
                chrome_options.add_argument('--disable-notifications')
                # Railway/Docker specific
                chrome_options.add_argument('--single-process')
                chrome_options.add_argument('--disable-background-networking')
                chrome_options.add_argument('--disable-sync')
                # Force color profile
                chrome_options.add_argument('--force-color-profile=srgb')
                
                try:
                    # Use webdriver-manager to automatically handle ChromeDriver
                    if retry == 0:
                        print("Installing/locating ChromeDriver...")
                    chrome_driver_path = ChromeDriverManager().install()
                    if retry == 0:
                        print(f"ChromeDriver path: {chrome_driver_path}")
                    
                    service = Service(chrome_driver_path)
                    driver = webdriver.Chrome(service=service, options=chrome_options)
                    if retry == 0:
                        print("Chrome driver initialized successfully")
                except Exception as e:
                    if retry == 0:
                        print(f"Chrome driver initialization failed: {e}")
                        import traceback
                        traceback.print_exc()
                    # Try with explicit Chrome binary location
                    chrome_options.binary_location = "/usr/bin/google-chrome-stable"
                    chrome_driver_path = ChromeDriverManager().install()
                    service = Service(chrome_driver_path)
                    driver = webdriver.Chrome(service=service, options=chrome_options)
                
                driver.get(url)
                
                # Wait for page to fully load
                from selenium.webdriver.support.ui import WebDriverWait
                wait = WebDriverWait(driver, 10)
                wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
                
                # Additional wait for dynamic content
                time.sleep(4)
                
                # Try to handle privacy/cookie dialogs
                self._handle_privacy_dialogs(driver)
                
                # Wait for any animations
                time.sleep(2)
                
                # Scroll to trigger lazy loading
                driver.execute_script("window.scrollTo(0, 500);")
                time.sleep(1)
                driver.execute_script("window.scrollTo(0, 0);")
                time.sleep(1)
                
                # Take screenshot
                screenshot = driver.get_screenshot_as_png()
                
                # Verify screenshot is not blank
                if len(screenshot) < 10000:  # Too small, likely blank
                    raise Exception("Screenshot appears to be blank")
                
                screenshot_b64 = base64.b64encode(screenshot).decode('utf-8')
                
                driver.quit()
                print(f"     ✅ Screenshot captured successfully (attempt {retry+1})")
                return f"data:image/png;base64,{screenshot_b64}"
                
            except Exception as e:
                print(f"     ⚠️  Screenshot attempt {retry+1} failed: {e}")
                try:
                    if 'driver' in locals():
                        driver.quit()
                except:
                    pass
                
                if retry == max_retries - 1:
                    print(f"     ❌ All screenshot attempts failed for {url}")
                    return None
                else:
                    time.sleep(2)  # Wait before retry
    
    def _handle_privacy_dialogs(self, driver):
        """Try to dismiss privacy dialogs, cookie banners, and consent popups"""
        try:
            # Common selectors for cookie/privacy dialogs
            dialog_selectors = [
                # Cookie banners
                '[id*="cookie"]', '[class*="cookie"]', '[data-testid*="cookie"]',
                '[id*="consent"]', '[class*="consent"]', '[data-testid*="consent"]',
                '[id*="privacy"]', '[class*="privacy"]', '[data-testid*="privacy"]',
                '[id*="gdpr"]', '[class*="gdpr"]', '[data-testid*="gdpr"]',
                # Generic modals and overlays
                '.modal', '.overlay', '.popup', '.banner',
                '[role="dialog"]', '[role="alertdialog"]',
                # Common button text patterns
                'button[aria-label*="Accept"]', 'button[aria-label*="Close"]',
                'button[aria-label*="Dismiss"]', 'button[aria-label*="Continue"]'
            ]
            
            # Button text patterns to look for
            button_texts = [
                'accept', 'accept all', 'accept cookies', 'agree', 'ok', 'continue',
                'close', 'dismiss', 'i understand', 'got it', 'allow all',
                'agree and close', 'i agree', 'proceed'
            ]
            
            # Try to find and click dismiss buttons
            for selector in dialog_selectors:
                try:
                    elements = driver.find_elements("css selector", selector)
                    for element in elements:
                        if element.is_displayed():
                            # Try to click the element if it's a button
                            if element.tag_name in ['button', 'a'] or 'btn' in element.get_attribute('class').lower():
                                element.click()
                                time.sleep(1)
                                break
                except:
                    continue
            
            # Try to find buttons by text content
            for text in button_texts:
                try:
                    # Find buttons with specific text
                    xpath_expressions = [
                        f"//button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{text}')]",
                        f"//a[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{text}')]",
                        f"//*[@role='button'][contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{text}')]"
                    ]
                    
                    for xpath in xpath_expressions:
                        try:
                            buttons = driver.find_elements("xpath", xpath)
                            for button in buttons:
                                if button.is_displayed() and button.is_enabled():
                                    button.click()
                                    time.sleep(1)
                                    return  # Exit after first successful click
                        except:
                            continue
                except:
                    continue
            
            # Try pressing Escape key to close dialogs
            try:
                driver.find_element("tag name", "body").send_keys(Keys.ESCAPE)
                time.sleep(1)
            except:
                pass
                
        except Exception as e:
            print(f"     ⚠️ Privacy dialog handling failed: {e}")
            pass  # Continue even if dialog handling fails
    
    def generate_strategic_intelligence_report(self, urls, report_title="Strategic Competitive Intelligence", output_filename=None, progress_callback=None):
        """Generate comprehensive strategic intelligence report"""
        
        if not output_filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_filename = f"strategic_competitive_intelligence_{timestamp}.html"
        
        print(f"🎯 GENERATING STRATEGIC COMPETITIVE INTELLIGENCE...")
        print(f"📊 Comprehensive analysis of {len(urls)} market participants...")
        
        # Extract comprehensive data for all brands
        self.brand_profiles = []
        seen_companies = set()
        
        try:
            for i, url in enumerate(urls, 1):
                print(f"\n🔍 [{i}/{len(urls)}] Comprehensive Data Extraction: {url}")
                if progress_callback:
                    progress_callback(f"Analyzing brand {i}/{len(urls)}: {urlparse(url).netloc}")
                try:
                    profile = self.extract_comprehensive_brand_data(url, progress_callback)
                    if profile:
                        company_name = profile['company_name']
                        if company_name not in seen_companies:
                            self.brand_profiles.append(profile)
                            seen_companies.add(company_name)
                            print(f"✅ Data extraction complete: {company_name}")
                        else:
                            print(f"⚠️ Skipped duplicate: {company_name}")
                    else:
                        print(f"❌ Failed to extract data: {url}")
                except Exception as e:
                    print(f"❌ Error extracting {url}: {e}")
        finally:
            if self.driver:
                self.driver.quit()
        
        if not self.brand_profiles:
            print("❌ No brands were successfully analyzed")
            return None
        
        # Generate strategic analysis for each brand
        print(f"\n🧠 Generating strategic analysis for each brand...")
        for brand in self.brand_profiles:
            strategic_analysis = self.generate_strategic_brand_analysis(brand, self.brand_profiles)
            brand['strategic_analysis'] = strategic_analysis
        
        # Generate market intelligence
        print(f"\n🌐 Generating market landscape intelligence...")
        self.market_intelligence = self.generate_market_intelligence(self.brand_profiles)
        
        # Generate strategic report
        print(f"\n📄 Creating strategic intelligence report...")
        html_content = self._generate_strategic_report(report_title)
        
        # Save report
        try:
            with open(output_filename, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            print(f"\n🎉 STRATEGIC INTELLIGENCE REPORT GENERATED!")
            print(f"📁 File: {output_filename}")
            print(f"📊 Brands analyzed: {len(self.brand_profiles)}")
            print(f"📄 Format: Comprehensive strategic analysis with actionable insights")
            print(f"🧠 Analysis: McKinsey-level competitive intelligence with market landscape")
            
            return output_filename
            
        except Exception as e:
            print(f"❌ Error saving report: {e}")
            return None
    
    def _generate_strategic_report(self, report_title):
        """Generate comprehensive strategic report HTML"""
        
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{report_title} - Strategic Intelligence</title>
    <style>
        {self._get_strategic_report_css()}
    </style>
</head>
<body>
    <div class="report-container">
        
        <!-- Executive Summary Slide -->
        <div class="report-slide">
            <div class="slide-header">
                <h1>{report_title}</h1>
                <div class="slide-meta">Strategic Competitive Intelligence | {datetime.now().strftime('%B %d, %Y')}</div>
            </div>
            
            <div class="executive-summary">
                <h2>Executive Summary</h2>
                <div class="summary-grid">
                    <div class="summary-card">
                        <h3>Market Participants</h3>
                        <div class="metric">{len(self.brand_profiles)}</div>
                        <p>Companies analyzed with comprehensive strategic intelligence</p>
                    </div>
                    <div class="summary-card">
                        <h3>Analysis Depth</h3>
                        <div class="metric">6</div>
                        <p>Strategic dimensions analyzed per competitor</p>
                    </div>
                    <div class="summary-card">
                        <h3>Insights Generated</h3>
                        <div class="metric">{len(self.brand_profiles) * 5 + 1}</div>
                        <p>Strategic recommendations and market insights</p>
                    </div>
                </div>
                
                <div class="competitor-overview">
                    <h3>Competitive Landscape Overview</h3>
                    <div class="competitor-grid">
                        {self._generate_competitor_cards()}
                    </div>
                </div>
                
                <div class="visual-grid-overview">
                    <h3>Strategic Brand Analysis Matrix</h3>
                    <p style="margin-bottom: 20px; color: #6c757d; font-style: italic;">
                        Comprehensive competitive intelligence across six critical brand dimensions, 
                        providing immediate strategic insights for informed decision-making.
                    </p>
                    <div class="brand-grid-visual">
                        {self._generate_visual_brand_grid()}
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Market Intelligence Slide -->
        <div class="report-slide">
            <div class="slide-header">
                <h2>Strategic Market Intelligence</h2>
                <div class="slide-meta">Advanced Competitive Landscape Analysis & Strategic Insights</div>
            </div>
            
            <div class="market-intelligence-content">
                <div style="background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); padding: 20px; border-radius: 8px; margin-bottom: 30px;">
                    <h4 style="color: #495057; margin-bottom: 10px;">Executive Intelligence Summary</h4>
                    <p style="color: #6c757d; font-style: italic; margin: 0;">
                        This strategic analysis provides actionable intelligence across market positioning, competitive dynamics, 
                        and emerging opportunities within the healthcare technology ecosystem.
                    </p>
                </div>
                <div class="intelligence-text">
                    {self._format_market_intelligence()}
                </div>
            </div>
        </div>
        
        <!-- Individual Brand Analysis Slides -->
        {self._generate_brand_analysis_slides()}
        
    </div>
</body>
</html>"""
        
        return html_content
    
    def _get_strategic_report_css(self):
        """CSS for strategic report format"""
        return """
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #2c3e50;
            background: #f8f9fa;
        }
        
        .report-container {
            max-width: 1400px;
            margin: 0 auto;
            background: white;
        }
        
        .report-slide {
            min-height: 100vh;
            padding: 60px;
            border-bottom: 3px solid #e9ecef;
            page-break-after: always;
        }
        
        .slide-header {
            margin-bottom: 40px;
            border-bottom: 3px solid #3498db;
            padding-bottom: 20px;
        }
        
        .slide-header h1 {
            font-size: 2.5em;
            color: #2c3e50;
            margin-bottom: 10px;
        }
        
        .slide-header h2 {
            font-size: 2em;
            color: #2c3e50;
            margin-bottom: 10px;
        }
        
        .slide-meta {
            font-size: 1.1em;
            color: #7f8c8d;
            font-weight: 500;
        }
        
        .executive-summary {
            margin-bottom: 40px;
        }
        
        .summary-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 30px;
            margin: 30px 0;
        }
        
        .summary-card {
            background: #f8f9fa;
            padding: 25px;
            border-radius: 8px;
            text-align: center;
            border-left: 4px solid #3498db;
        }
        
        .summary-card h3 {
            font-size: 1.1em;
            color: #2c3e50;
            margin-bottom: 15px;
        }
        
        .metric {
            font-size: 3em;
            font-weight: bold;
            color: #3498db;
            margin-bottom: 10px;
        }
        
        .competitor-overview {
            margin-top: 40px;
        }
        
        .competitor-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }
        
        .competitor-card {
            background: white;
            border: 1px solid #e9ecef;
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        .competitor-card h4 {
            font-size: 1.2em;
            color: #2c3e50;
            margin-bottom: 10px;
        }
        
        .market-intelligence-content {
            background: white;
            padding: 40px;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        
        .intelligence-text {
            line-height: 1.8;
        }
        
        .intelligence-text h3 {
            color: #2c3e50;
            margin: 30px 0 15px 0;
            font-size: 1.4em;
            border-bottom: 2px solid #3498db;
            padding-bottom: 8px;
        }
        
        .intelligence-text h4 {
            color: #34495e;
            margin: 20px 0 10px 0;
            font-size: 1.2em;
        }
        
        .intelligence-text p {
            margin-bottom: 15px;
            font-size: 1.05em;
        }
        
        .intelligence-text ul {
            margin: 15px 0 15px 30px;
        }
        
        .intelligence-text li {
            margin-bottom: 8px;
            font-size: 1.05em;
        }
        
        .brand-analysis-slide {
            margin-bottom: 0;
        }
        
        .brand-analysis-content {
            background: white;
            padding: 40px;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        
        .brand-analysis-content h3 {
            color: #2c3e50;
            margin: 30px 0 15px 0;
            font-size: 1.4em;
            border-bottom: 2px solid #e74c3c;
            padding-bottom: 8px;
        }
        
        .brand-analysis-content h4 {
            color: #34495e;
            margin: 20px 0 10px 0;
            font-size: 1.2em;
        }
        
        .brand-analysis-content p {
            margin-bottom: 15px;
            font-size: 1.05em;
        }
        
        .brand-analysis-content ul {
            margin: 15px 0 15px 30px;
        }
        
        .brand-analysis-content li {
            margin-bottom: 8px;
            font-size: 1.05em;
        }
        
        .strategic-insight {
            background: #f8f9fa;
            border-left: 4px solid #3498db;
            padding: 20px;
            margin: 20px 0;
        }
        
        .strategic-insight h4 {
            color: #2c3e50;
            margin-bottom: 10px;
        }
        
        /* Visual Brand Grid Styles */
        .visual-grid-overview {
            margin-top: 40px;
            padding-top: 30px;
            border-top: 2px solid #e9ecef;
        }
        
        /* Premium 6-Row Brand Analysis Grid */
        .competitive-landscape-grid {
            display: grid;
            grid-template-rows: repeat(6, auto);
            gap: 25px;
            margin: 30px 0;
            background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
            padding: 40px;
            border-radius: 16px;
            border: none;
            box-shadow: 0 8px 32px rgba(0,0,0,0.08);
        }
        
        .grid-row {
            display: grid;
            grid-template-columns: 200px repeat(var(--brand-count, 4), 1fr);
            gap: 20px;
            padding: 20px 0;
            border-bottom: 1px solid rgba(0,0,0,0.06);
            position: relative;
        }
        
        .grid-row:last-child {
            border-bottom: none;
        }
        
        .grid-row-header {
            font-weight: 700;
            color: #1a202c;
            text-align: left;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1em;
            color: white;
            text-transform: uppercase;
            letter-spacing: 1px;
            box-shadow: 0 4px 16px rgba(102, 126, 234, 0.3);
        }
        
        .grid-cell {
            background: #ffffff;
            padding: 20px;
            border-radius: 12px;
            text-align: center;
            min-height: 120px;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-direction: column;
            border: 1px solid rgba(0,0,0,0.08);
            box-shadow: 0 4px 20px rgba(0,0,0,0.08);
            transition: all 0.3s ease;
            position: relative;
        }
        
        .grid-cell:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 32px rgba(0,0,0,0.12);
        }
        
        /* Premium Row-specific styling */
        .logos-row .grid-cell {
            min-height: 100px;
            background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        }
        
        .logos-row .brand-logo {
            max-width: 80%;
            max-height: 60px;
            object-fit: contain;
            margin-bottom: 12px;
            filter: drop-shadow(0 2px 8px rgba(0,0,0,0.1));
        }
        
        .logos-row .brand-name {
            font-size: 0.9em;
            font-weight: 700;
            color: #2d3748;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .brand-story-row .grid-cell {
            min-height: 160px;
            padding: 20px;
            text-align: left;
        }
        
        .brand-story-text {
            font-size: 0.85em;
            line-height: 1.5;
            color: #4a5568;
            text-align: left;
            font-style: italic;
            overflow: hidden;
            display: -webkit-box;
            -webkit-line-clamp: 6;
            -webkit-box-orient: vertical;
        }
        
        .personality-row .grid-cell {
            min-height: 100px;
            padding: 15px;
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            align-content: flex-start;
            justify-content: center;
        }
        
        .personality-trait {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border: none;
            border-radius: 20px;
            padding: 8px 16px;
            font-size: 0.7em;
            font-weight: 600;
            color: white;
            white-space: nowrap;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
        }
        
        .colors-row .grid-cell {
            min-height: 80px;
            padding: 15px;
            display: flex;
            flex-direction: row;
            flex-wrap: wrap;
            gap: 8px;
            align-content: center;
            justify-content: center;
        }
        
        .color-swatch {
            width: 40px;
            height: 40px;
            border-radius: 8px;
            border: 2px solid #ffffff;
            flex-shrink: 0;
            box-shadow: 0 2px 8px rgba(0,0,0,0.15);
            position: relative;
        }
        
        .color-swatch::after {
            content: attr(title);
            position: absolute;
            bottom: -20px;
            left: 50%;
            transform: translateX(-50%);
            font-size: 0.6em;
            color: #718096;
            white-space: nowrap;
        }
        
        .typography-row .grid-cell {
            min-height: 120px;
            padding: 20px;
            text-align: left;
        }
        
        .typography-sample {
            margin-bottom: 8px;
        }
        
        .font-primary {
            font-size: 1.2em;
            font-weight: 700;
            color: #2d3748;
            margin-bottom: 4px;
        }
        
        .font-secondary {
            font-size: 0.9em;
            font-weight: 400;
            color: #4a5568;
            line-height: 1.4;
        }
        
        .visuals-row .grid-cell {
            min-height: 180px;
            padding: 12px;
        }
        
        .visual-screenshot {
            width: 100%;
            height: 100%;
            object-fit: cover;
            border-radius: 8px;
            border: 2px solid #ffffff;
            box-shadow: 0 4px 16px rgba(0,0,0,0.1);
        }
        
        .visual-placeholder {
            background: linear-gradient(135deg, #f7fafc 0%, #edf2f7 100%);
            color: #718096;
            font-size: 0.8em;
            text-align: center;
            display: flex;
            align-items: center;
            justify-content: center;
            height: 100%;
            border-radius: 8px;
            border: 2px dashed #cbd5e0;
        }
        
        .visual-gallery-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            grid-template-rows: 1fr 1fr;
            gap: 4px;
            height: 100%;
            border-radius: 8px;
            overflow: hidden;
        }
        
        .gallery-image {
            width: 100%;
            height: 100%;
            object-fit: cover;
            border-radius: 4px;
            transition: transform 0.2s ease;
        }
        
        .gallery-image:hover {
            transform: scale(1.05);
            z-index: 2;
            position: relative;
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        }
        
        .grid-logo-cell {
            grid-row: 1;
            background: white;
            border: 1px solid #e9ecef;
            border-radius: 6px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        }
        
        .grid-brand-logo {
            max-width: 100%;
            max-height: 30px;
            object-fit: contain;
            margin-bottom: 5px;
        }
        
        .grid-brand-name {
            font-size: 0.7em;
            font-weight: 600;
            color: #495057;
            text-align: center;
        }
        
        .grid-positioning-cell {
            grid-row: 2;
            background: white;
            border: 1px solid #e9ecef;
            border-radius: 6px;
            padding: 10px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
            overflow: hidden;
        }
        
        .grid-positioning-text {
            font-size: 0.65em;
            line-height: 1.2;
            color: #495057;
            overflow: hidden;
            display: -webkit-box;
            -webkit-line-clamp: 6;
            -webkit-box-orient: vertical;
        }
        
        .grid-products-cell {
            grid-row: 3;
            background: white;
            border: 1px solid #e9ecef;
            border-radius: 6px;
            padding: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
            display: flex;
            flex-wrap: wrap;
            gap: 3px;
            align-content: flex-start;
        }
        
        .grid-product-tag {
            background: #e3f2fd;
            border: 1px solid #bbdefb;
            border-radius: 8px;
            padding: 2px 6px;
            font-size: 0.55em;
            font-weight: 500;
            color: #1976d2;
            white-space: nowrap;
        }
        
        .grid-color-cell {
            grid-row: 4;
            background: white;
            border: 1px solid #e9ecef;
            border-radius: 6px;
            padding: 6px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
            display: flex;
            flex-direction: column;
        }
        
        .grid-color-swatches {
            display: grid;
            grid-template-columns: repeat(6, 1fr);
            gap: 2px;
            flex-grow: 1;
        }
        
        .grid-color-swatch {
            height: 18px;
            border-radius: 2px;
            border: 1px solid #dee2e6;
        }
        
        .grid-visual-cell {
            grid-row: 5;
            background: white;
            border: 1px solid #e9ecef;
            border-radius: 6px;
            padding: 6px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
            display: flex;
            flex-direction: column;
        }
        
        .grid-screenshot-container {
            flex-grow: 1;
            background: #f8f9fa;
            border-radius: 4px;
            border: 1px solid #e9ecef;
            overflow: hidden;
            position: relative;
        }
        
        .grid-screenshot {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }
        
        @media print {
            .report-slide {
                page-break-after: always;
                min-height: auto;
            }
        }
        """
    
    def _generate_competitor_cards(self):
        """Generate competitor overview cards"""
        cards_html = ""
        for brand in self.brand_profiles:
            hero_text = ' '.join(brand['comprehensive_content']['hero_sections'][:2])
            if len(hero_text) > 150:
                hero_text = hero_text[:150] + "..."
            
            cards_html += f"""
            <div class="competitor-card">
                <h4>{brand['company_name']}</h4>
                <p>{hero_text}</p>
                <div style="margin-top: 10px; font-size: 0.9em; color: #7f8c8d;">
                    Products: {len(brand['product_portfolio']['main_products'])} identified |
                    Business Model: {brand['business_model']['pricing_model'].title()}
                </div>
            </div>
            """
        return cards_html
    
    def _generate_visual_brand_grid(self):
        """Generate premium 6-row brand analysis grid"""
        brand_count = len(self.brand_profiles)
        
        # Generate enhanced brand analysis using AI
        for brand in self.brand_profiles:
            if not brand.get('ai_personality_traits'):
                brand['ai_personality_traits'] = self._generate_brand_personality_traits(brand)
            if not brand.get('ai_brand_story'):
                brand['ai_brand_story'] = self._generate_brand_story(brand)
            if not brand.get('ai_typography_analysis'):
                brand['ai_typography_analysis'] = self._analyze_typography(brand)
        
        grid_html = f"""
        <div class="competitive-landscape-grid" style="--brand-count: {brand_count};">
            
            <!-- Row 1: Brand Logos & Identity -->
            <div class="grid-row logos-row">
                <div class="grid-row-header">Brand Identity</div>
                {self._generate_logos_row()}
            </div>
            
            <!-- Row 2: Brand Story & Narrative -->
            <div class="grid-row brand-story-row">
                <div class="grid-row-header">Brand Story</div>
                {self._generate_brand_story_row()}
            </div>
            
            <!-- Row 3: Brand Personality -->
            <div class="grid-row personality-row">
                <div class="grid-row-header">Personality</div>
                {self._generate_personality_row()}
            </div>
            
            <!-- Row 4: Color Palette -->
            <div class="grid-row colors-row">
                <div class="grid-row-header">Color Palette</div>
                {self._generate_colors_row()}
            </div>
            
            <!-- Row 5: Typography -->
            <div class="grid-row typography-row">
                <div class="grid-row-header">Typography</div>
                {self._generate_typography_row()}
            </div>
            
            <!-- Row 6: Visual Touchpoints -->
            <div class="grid-row visuals-row">
                <div class="grid-row-header">Touchpoints</div>
                {self._generate_visuals_row()}
            </div>
            
        </div>
        """
        
        return grid_html
    
    def _generate_logos_row(self):
        """Generate Row 1: Company Logos & Brand Names"""
        row_html = ""
        for brand in self.brand_profiles:
            logos = brand.get("visual_identity", {}).get("logos", [])
            if logos:
                logo_html = f'<img src="{logos[0]}" class="brand-logo" alt="{brand["company_name"]} Logo">'
            else:
                # Create text-based logo placeholder
                logo_html = f'<div style="font-weight:600;color:#2c3e50;font-size:0.9em;">{brand["company_name"]}</div>'
            
            row_html += f"""
            <div class="grid-cell">
                {logo_html}
                <div class="brand-name">{brand["company_name"]}</div>
            </div>
            """
        return row_html
    
    def _generate_brand_story_row(self):
        """Generate Row 2: Brand Story & Narrative"""
        row_html = ""
        for brand in self.brand_profiles:
            brand_story = brand.get('ai_brand_story', 'A forward-thinking organization focused on delivering exceptional value through innovative solutions and professional excellence.')
            
            row_html += f"""
            <div class="grid-cell">
                <div class="brand-story-text">{brand_story}</div>
            </div>
            """
        return row_html
    
    def _generate_positioning_row(self):
        """Generate Row 2: Brand Positioning Statements"""
        row_html = ""
        for brand in self.brand_profiles:
            # Get hero sections and value propositions
            hero_sections = brand.get('comprehensive_content', {}).get('hero_sections', [])
            value_props = brand.get('comprehensive_content', {}).get('value_propositions', [])
            
            # Create positioning statement
            if hero_sections:
                positioning_text = hero_sections[0]
            elif value_props:
                positioning_text = value_props[0]
            else:
                # Fallback based on company name and meta description
                meta_desc = brand.get('comprehensive_content', {}).get('meta_description', '')
                if meta_desc and len(meta_desc) > 20:
                    positioning_text = meta_desc
                else:
                    positioning_text = f"Professional {brand['company_name'].split()[0] if brand['company_name'] else 'Healthcare'} solutions for modern organizations"
            
            # Truncate if too long
            if len(positioning_text) > 150:
                positioning_text = positioning_text[:150] + "..."
            
            row_html += f"""
            <div class="grid-cell">
                <div class="positioning-text">"{positioning_text}"</div>
            </div>
            """
        return row_html
    
    def _generate_personality_row(self):
        """Generate Row 3: Brand Personality Descriptors"""
        row_html = ""
        for brand in self.brand_profiles:
            personality_traits = brand.get('ai_personality_traits', ['Professional', 'Innovative', 'Trustworthy'])
            
            traits_html = ""
            for trait in personality_traits[:4]:  # Show max 4 traits
                traits_html += f'<span class="personality-trait">{trait}</span>'
            
            row_html += f"""
            <div class="grid-cell">
                {traits_html}
            </div>
            """
        return row_html
    
    def _generate_colors_row(self):
        """Generate Row 4: Color Palette Representation"""
        row_html = ""
        for brand in self.brand_profiles:
            # Check multiple possible locations for color data
            colors = (brand.get("visual_identity", {}).get("color_palette", []) or 
                     brand.get("color_palette", []) or
                     brand.get("colors", []))
            
            colors_html = ""
            for color in colors[:6]:  # Show max 6 colors
                colors_html += f'<div class="color-swatch" style="background-color: {color};" title="{color}"></div>'
            
            # If no colors, show placeholder
            if not colors_html:
                colors_html = '<div class="color-swatch" style="background-color: #f8f9fa;"></div><div class="color-swatch" style="background-color: #e9ecef;"></div>'
            
            row_html += f"""
            <div class="grid-cell">
                {colors_html}
            </div>
            """
        return row_html
    
    def _generate_typography_row(self):
        """Generate Row 5: Typography Analysis"""
        row_html = ""
        for brand in self.brand_profiles:
            typography = brand.get('ai_typography_analysis', {
                'primary_font': 'Modern Sans-Serif',
                'secondary_font': 'Clean body typography with professional hierarchy',
                'style': 'Contemporary & Accessible'
            })
            
            primary_font = typography.get('primary_font', 'Sans-Serif')
            secondary_text = typography.get('secondary_font', 'Professional body text')
            
            row_html += f"""
            <div class="grid-cell">
                <div class="typography-sample">
                    <div class="font-primary" style="font-family: {primary_font}, 'Segoe UI', Arial, sans-serif;">
                        {brand['company_name']}
                    </div>
                    <div class="font-secondary">
                        {secondary_text}
                    </div>
                </div>
            </div>
            """
        return row_html
    
    def _generate_visuals_row(self):
        """Generate Row 6: Visual Assets & Graphics Collection"""
        row_html = ""
        for brand in self.brand_profiles:
            # Generate visual gallery if not already present
            if not brand.get('visual_gallery'):
                brand['visual_gallery'] = self._capture_visual_gallery(brand)
            
            visual_gallery = brand.get('visual_gallery', [])
            
            if visual_gallery and len(visual_gallery) > 0:
                # Create a grid of visual assets
                visual_html = '<div class="visual-gallery-grid">'
                for i, visual in enumerate(visual_gallery[:4]):  # Max 4 visuals
                    visual_html += f'<img src="{visual}" class="gallery-image" alt="{brand["company_name"]} Visual {i+1}" loading="lazy">'
                visual_html += '</div>'
            else:
                # Fallback to homepage screenshot
                screenshot = brand.get("screenshot")
                if screenshot:
                    visual_html = f'<img src="{screenshot}" class="visual-screenshot" alt="{brand["company_name"]} Homepage">'
                else:
                    visual_html = f'<div class="visual-placeholder">Homepage<br>{brand["company_name"]}</div>'
            
            row_html += f"""
            <div class="grid-cell">
                {visual_html}
            </div>
            """
        return row_html
    
    def _capture_visual_gallery(self, brand):
        """Capture multiple visual assets from website"""
        visuals = []
        try:
            print(f"         🖼️ Capturing visual gallery for {brand['company_name']}...")
            
            # Fetch the webpage
            response = self.session.get(brand['url'], timeout=15)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find and collect various visual elements
            image_sources = []
            
            # Hero images and banners
            hero_selectors = [
                'img[class*="hero"]', 'img[class*="banner"]', 'img[class*="featured"]',
                '.hero img', '.banner img', '.featured img',
                'img[src*="hero"]', 'img[src*="banner"]', 'img[src*="featured"]'
            ]
            
            for selector in hero_selectors:
                for img in soup.select(selector):
                    src = img.get('src') or img.get('data-src')
                    if src and not any(x in src.lower() for x in ['logo', 'icon', 'avatar']):
                        image_sources.append(src)
            
            # Product/service images
            product_selectors = [
                'img[class*="product"]', 'img[class*="service"]', 'img[class*="solution"]',
                '.product img', '.service img', '.solution img',
                'img[alt*="product"]', 'img[alt*="service"]', 'img[alt*="solution"]'
            ]
            
            for selector in product_selectors:
                for img in soup.select(selector):
                    src = img.get('src') or img.get('data-src')
                    if src and not any(x in src.lower() for x in ['logo', 'icon', 'avatar']):
                        image_sources.append(src)
            
            # General content images (larger ones)
            for img in soup.find_all('img'):
                src = img.get('src') or img.get('data-src')
                if src and not any(x in src.lower() for x in ['logo', 'icon', 'avatar', 'sprite']):
                    # Check if image is likely to be substantial content
                    width = img.get('width')
                    height = img.get('height')
                    if width and height:
                        try:
                            w, h = int(width), int(height)
                            if w > 200 and h > 150:  # Reasonable size filter
                                image_sources.append(src)
                        except:
                            image_sources.append(src)
                    else:
                        image_sources.append(src)
            
            # Convert relative URLs to absolute
            for src in image_sources[:8]:  # Limit to first 8 for performance
                if src:
                    absolute_url = urljoin(brand['url'], src)
                    # Basic validation
                    if absolute_url.startswith(('http://', 'https://')) and any(ext in absolute_url.lower() for ext in ['.jpg', '.jpeg', '.png', '.webp', '.svg']):
                        visuals.append(absolute_url)
                        if len(visuals) >= 4:  # Limit to 4 visuals
                            break
            
            # Remove duplicates while preserving order
            seen = set()
            unique_visuals = []
            for visual in visuals:
                if visual not in seen:
                    seen.add(visual)
                    unique_visuals.append(visual)
            
            print(f"         ✅ Captured {len(unique_visuals)} visual assets")
            return unique_visuals[:4]  # Max 4 visuals
            
        except Exception as e:
            print(f"         ⚠️ Visual gallery capture failed: {e}")
            
        # Fallback to homepage screenshot if available
        if brand.get('screenshot'):
            return [brand['screenshot']]
        
        return []
    
    def _generate_brand_personality_traits(self, brand):
        """Generate AI-powered brand personality traits"""
        try:
            # Extract content for personality analysis
            hero_content = ' '.join(brand.get('comprehensive_content', {}).get('hero_sections', [])[:3])
            value_props = ' '.join(brand.get('comprehensive_content', {}).get('value_propositions', [])[:3])
            about_content = ' '.join(brand.get('comprehensive_content', {}).get('about_content', [])[:2])
            
            analysis_content = f"{hero_content} {value_props} {about_content}"[:1000]
            
            personality_prompt = f"""
Analyze the brand personality of {brand['company_name']} based on their website content and messaging.

WEBSITE CONTENT:
{analysis_content}

Based on this content, identify 3-4 personality traits that best describe this brand's character and tone. Choose from professional brand personality descriptors such as:

Expert, Innovative, Trustworthy, Professional, Authoritative, Approachable, Cutting-edge, Reliable, Clinical, Scientific, Accessible, Premium, Collaborative, Evidence-based, User-friendly, Comprehensive, Specialized, Global, Leading, Advanced

Return only a JSON array of 3-4 personality traits:
["Trait1", "Trait2", "Trait3", "Trait4"]

Focus on traits that are clearly supported by their messaging and positioning.
"""
            
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a brand personality analyst. Return only a JSON array of personality traits."},
                    {"role": "user", "content": personality_prompt}
                ],
                temperature=0.2,
                max_tokens=200
            )
            
            content = response["choices"][0]["message"]["content"].strip()
            # Extract JSON array
            if '[' in content and ']' in content:
                start = content.find('[')
                end = content.rfind(']') + 1
                traits_json = content[start:end]
                traits = json.loads(traits_json)
                return traits[:4]  # Max 4 traits
            
        except Exception as e:
            print(f"         ⚠️ Personality trait generation failed: {e}")
        
        # Fallback personality traits based on company type
        if 'evidence' in brand['company_name'].lower():
            return ['Evidence-based', 'Scientific', 'Reliable', 'Professional']
        elif 'elsevier' in brand['company_name'].lower():
            return ['Authoritative', 'Global', 'Expert', 'Comprehensive']
        elif 'wolters' in brand['company_name'].lower():
            return ['Professional', 'Trusted', 'Expert', 'Innovative']
        else:
            return ['Professional', 'Innovative', 'Trustworthy', 'Expert']
    
    def _generate_brand_story(self, brand):
        """Generate AI-powered brand story and narrative"""
        try:
            # Extract content for brand story analysis
            hero_content = ' '.join(brand.get('comprehensive_content', {}).get('hero_sections', [])[:2])
            about_content = ' '.join(brand.get('comprehensive_content', {}).get('about_content', [])[:1])
            value_props = ' '.join(brand.get('comprehensive_content', {}).get('value_propositions', [])[:2])
            
            story_content = f"{hero_content} {about_content} {value_props}"[:800]
            
            story_prompt = f"""
Based on the website content below, craft a sophisticated brand story that captures the essence and narrative of {brand['company_name']}.

WEBSITE CONTENT:
{story_content}

Create a premium brand story (2-3 sentences) that:
1. Captures their unique value proposition and mission
2. Reflects their professional positioning in the market
3. Uses sophisticated, consultancy-level language
4. Focuses on impact and transformation they deliver

Write in the style of a premium brand consultancy. Be specific to their actual business, not generic.

Return only the brand story text, no additional commentary.
"""
            
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a premium brand strategist who crafts sophisticated brand narratives for professional organizations."},
                    {"role": "user", "content": story_prompt}
                ],
                temperature=0.3,
                max_tokens=200
            )
            
            story = response["choices"][0]["message"]["content"].strip()
            if len(story) > 50:
                return story
            
        except Exception as e:
            print(f"         ⚠️ Brand story generation failed: {e}")
        
        # Fallback brand stories based on company type
        if 'evidence' in brand['company_name'].lower():
            return "Pioneering evidence-based healthcare solutions that transform clinical decision-making through cutting-edge AI and comprehensive medical intelligence platforms."
        elif 'elsevier' in brand['company_name'].lower():
            return "The global leader in information analytics, empowering healthcare professionals and researchers with trusted knowledge and innovative technology solutions."
        elif 'wolters' in brand['company_name'].lower():
            return "Delivering expert solutions that combine deep domain knowledge with advanced technology to help professionals achieve better outcomes for their organizations."
        else:
            return "A forward-thinking organization focused on delivering exceptional value through innovative solutions and professional excellence."
    
    def _analyze_typography(self, brand):
        """Analyze typography and font usage from website using enhanced CSS extraction"""
        try:
            print(f"         🔤 Analyzing typography for {brand['company_name']}...")
            
            # Try to fetch fresh CSS and extract fonts
            fonts = self._extract_website_fonts(brand['url'])
            
            # Also check existing visual identity data
            existing_fonts = brand.get('visual_identity', {}).get('fonts', [])
            if existing_fonts:
                fonts.extend(existing_fonts)
            
            # Analyze and select best fonts
            font_analysis = self._analyze_font_stack(fonts, brand['company_name'])
            
            print(f"         ✅ Typography analyzed: {font_analysis['primary_font']}")
            return font_analysis
            
        except Exception as e:
            print(f"         ⚠️ Typography analysis failed: {e}")
            
        # Fallback typography analysis
        return {
            'primary_font': 'Modern Sans-Serif',
            'secondary_font': 'Professional body typography with clear hierarchy',
            'style': 'Contemporary & Accessible'
        }
    
    def _extract_website_fonts(self, url):
        """Extract actual fonts used on website from CSS"""
        fonts = []
        try:
            # Fetch the webpage
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract font families from style attributes and CSS
            font_families = set()
            
            # Check inline styles
            for element in soup.find_all(style=True):
                style = element.get('style', '')
                if 'font-family' in style:
                    # Extract font-family value
                    font_match = re.search(r'font-family:\s*([^;]+)', style)
                    if font_match:
                        font_families.add(font_match.group(1).strip())
            
            # Check CSS files and style tags
            for style_tag in soup.find_all('style'):
                css_content = style_tag.get_text()
                font_matches = re.findall(r'font-family:\s*([^;}]+)', css_content)
                for match in font_matches:
                    font_families.add(match.strip())
            
            # Check external CSS files (basic parsing)
            for link in soup.find_all('link', {'rel': 'stylesheet'}):
                try:
                    css_url = urljoin(url, link.get('href', ''))
                    if css_url and (css_url.endswith('.css') or 'css' in css_url):
                        css_response = self.session.get(css_url, timeout=5)
                        if css_response.status_code == 200:
                            css_content = css_response.text
                            font_matches = re.findall(r'font-family:\s*([^;}]+)', css_content)
                            for match in font_matches:
                                font_families.add(match.strip())
                except:
                    continue
            
            # Try to extract fonts using Selenium for computed styles
            if not font_families or len(font_families) < 2:
                try:
                    print("         📱 Using Selenium for deep font extraction...")
                    fonts_from_selenium = self._extract_fonts_with_selenium(url)
                    font_families.update(fonts_from_selenium)
                except Exception as e:
                    print(f"         ⚠️ Selenium font extraction failed: {e}")
            
            # Clean and filter font families
            for font_family in font_families:
                # Remove quotes and split by comma
                clean_fonts = [f.strip().replace('"', '').replace("'", '') for f in font_family.split(',')]
                fonts.extend(clean_fonts)
            
            # Remove generic fonts and empty strings
            fonts = [f for f in fonts if f and f.lower() not in ['serif', 'sans-serif', 'monospace', 'cursive', 'fantasy', 'inherit', 'initial', 'unset']]
            
            return list(set(fonts))  # Remove duplicates
            
        except Exception as e:
            print(f"         ⚠️ Font extraction failed: {e}")
            return []
    
    def _analyze_font_stack(self, fonts, company_name):
        """Analyze extracted fonts and determine primary/secondary fonts"""
        # Priority order for primary fonts (prefer custom/brand fonts over system fonts)
        custom_fonts = []
        system_fonts = []
        
        common_system_fonts = ['arial', 'helvetica', 'times', 'georgia', 'verdana', 'trebuchet', 'courier', 'impact', 'comic sans', 'segoe ui', 'roboto', 'open sans']
        
        for font in fonts:
            font_lower = font.lower()
            if any(sys_font in font_lower for sys_font in common_system_fonts):
                system_fonts.append(font)
            else:
                custom_fonts.append(font)
        
        # Select primary font (prefer custom fonts)
        primary_font = 'Modern Sans-Serif'
        if custom_fonts:
            primary_font = custom_fonts[0]
        elif system_fonts:
            primary_font = system_fonts[0]
        
        # Select secondary font or generate description
        secondary_font = 'Professional body typography'
        if len(fonts) > 1:
            if custom_fonts and len(custom_fonts) > 1:
                secondary_font = custom_fonts[1]
            elif system_fonts:
                secondary_font = system_fonts[0] if primary_font in custom_fonts else (system_fonts[1] if len(system_fonts) > 1 else system_fonts[0])
        
        # If secondary is same as primary, generate description
        if secondary_font == primary_font or secondary_font == 'Professional body typography':
            company_type = company_name.lower()
            if 'medical' in company_type or 'health' in company_type:
                secondary_font = 'Clinical precision with accessible hierarchy'
            elif 'tech' in company_type or 'software' in company_type:
                secondary_font = 'Technical clarity with modern spacing'
            else:
                secondary_font = 'Professional readability with structured layout'
        
        # Determine font personality/style
        style = 'Contemporary'
        primary_lower = primary_font.lower()
        if any(word in primary_lower for word in ['modern', 'neue', 'gotham', 'avenir', 'proxima', 'brandon']):
            style = 'Modern & Clean'
        elif any(word in primary_lower for word in ['times', 'georgia', 'serif', 'minion', 'garamond']):
            style = 'Traditional & Authoritative'
        elif any(word in primary_lower for word in ['helvetica', 'arial', 'segoe', 'roboto', 'open sans']):
            style = 'Clean & Professional'
        elif any(word in primary_lower for word in ['custom', 'brand', 'proprietary']):
            style = 'Custom & Distinctive'
        
        return {
            'primary_font': primary_font,
            'secondary_font': secondary_font,
            'style': style,
            'font_personality': f"{style.split(' & ')[0]}, {secondary_font.split(' ')[0]}"
        }
    
    def _format_market_intelligence(self):
        """Format market intelligence for display"""
        if not self.market_intelligence:
            return "<p>Market intelligence analysis not available.</p>"
        
        # Convert markdown-style content to HTML
        formatted_text = self.market_intelligence.replace('\n\n', '</p><p>')
        formatted_text = formatted_text.replace('\n', '<br>')
        formatted_text = f"<p>{formatted_text}</p>"
        
        # Format headers
        formatted_text = re.sub(r'### (.*?)</p>', r'<h4>\1</h4>', formatted_text)
        formatted_text = re.sub(r'## (.*?)</p>', r'<h3>\1</h3>', formatted_text)
        formatted_text = re.sub(r'# (.*?)</p>', r'<h2>\1</h2>', formatted_text)
        
        # Format bold text
        formatted_text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', formatted_text)
        
        # Format lists
        formatted_text = re.sub(r'- (.*?)<br>', r'<li>\1</li>', formatted_text)
        formatted_text = re.sub(r'(<li>.*?</li>)', r'<ul>\1</ul>', formatted_text, flags=re.DOTALL)
        
        return formatted_text
    
    def _generate_brand_analysis_slides(self):
        """Generate individual brand analysis slides"""
        slides_html = ""
        
        for brand in self.brand_profiles:
            analysis_content = self._format_brand_analysis(brand.get('strategic_analysis', 'Analysis not available'))
            
            slides_html += f"""
            <div class="report-slide brand-analysis-slide">
                <div class="slide-header">
                    <h2>{brand['company_name']} - Strategic Intelligence Profile</h2>
                    <div class="slide-meta">Advanced Competitive Analysis & Strategic Positioning Assessment</div>
                </div>
                
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; border-radius: 8px; margin-bottom: 30px; color: white;">
                    <h4 style="margin-bottom: 10px;">Strategic Assessment Overview</h4>
                    <p style="margin: 0; opacity: 0.9; font-style: italic;">
                        Comprehensive analysis of {brand['company_name']}'s market position, competitive advantages, 
                        strategic vulnerabilities, and growth opportunities within the competitive landscape.
                    </p>
                </div>
                
                <div class="brand-analysis-content">
                    {analysis_content}
                </div>
            </div>
            """
        
        return slides_html
    
    def _format_brand_analysis(self, analysis_text):
        """Format brand analysis for display"""
        if not analysis_text or analysis_text == "Analysis not available":
            return "<p>Strategic analysis not available for this brand.</p>"
        
        # Convert markdown-style content to HTML
        formatted_text = analysis_text.replace('\n\n', '</p><p>')
        formatted_text = formatted_text.replace('\n', '<br>')
        formatted_text = f"<p>{formatted_text}</p>"
        
        # Format headers
        formatted_text = re.sub(r'### (.*?)</p>', r'<h4>\1</h4>', formatted_text)
        formatted_text = re.sub(r'## (.*?)</p>', r'<h3>\1</h3>', formatted_text)
        formatted_text = re.sub(r'# (.*?)</p>', r'<h2>\1</h2>', formatted_text)
        
        # Format bold text
        formatted_text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', formatted_text)
        
        # Format lists
        formatted_text = re.sub(r'- (.*?)<br>', r'<li>\1</li>', formatted_text)
        formatted_text = re.sub(r'(<li>.*?</li>)', r'<ul>\1</ul>', formatted_text, flags=re.DOTALL)
        
        return formatted_text


    def _extract_fonts_with_selenium(self, url):
        """Extract fonts using Selenium to get computed styles"""
        fonts = set()
        driver = None
        try:
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--window-size=1920,1080')
            chrome_options.add_argument('--force-color-profile=srgb')
            
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)
            driver.get(url)
            
            # Wait for page load
            from selenium.webdriver.support.ui import WebDriverWait
            WebDriverWait(driver, 10).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
            time.sleep(2)
            
            # Execute JavaScript to get computed fonts
            font_data = driver.execute_script("""
                const fonts = new Set();
                const elements = document.querySelectorAll('*');
                
                // Sample elements across the page
                const sampleElements = [];
                const step = Math.max(1, Math.floor(elements.length / 100)); // Sample up to 100 elements
                
                for(let i = 0; i < elements.length; i += step) {
                    const el = elements[i];
                    if(el.offsetWidth > 0 && el.offsetHeight > 0) { // Only visible elements
                        const computed = window.getComputedStyle(el);
                        const fontFamily = computed.fontFamily;
                        if(fontFamily) {
                            fonts.add(fontFamily);
                        }
                    }
                }
                
                // Also check specific important elements
                const importantSelectors = ['h1', 'h2', 'h3', 'p', 'body', 'nav', 'header', '.logo', '.brand'];
                importantSelectors.forEach(selector => {
                    document.querySelectorAll(selector).forEach(el => {
                        const computed = window.getComputedStyle(el);
                        const fontFamily = computed.fontFamily;
                        if(fontFamily) {
                            fonts.add(fontFamily);
                        }
                    });
                });
                
                return Array.from(fonts);
            """)
            
            if font_data:
                for font_family in font_data:
                    fonts.add(font_family)
                
        except Exception as e:
            print(f"Selenium font extraction error: {e}")
        finally:
            if driver:
                driver.quit()
                
        return fonts

def main():
    """Generate strategic competitive intelligence report"""
    
    medical_urls = [
        "https://www.wolterskluwer.com",
        "https://www.elsevier.com", 
        "https://www.openevidence.com"
    ]
    
    generator = StrategicCompetitiveIntelligence()
    
    output_file = generator.generate_strategic_intelligence_report(
        urls=medical_urls,
        report_title="Medical AI Platform Strategic Competitive Intelligence",
        output_filename="strategic_competitive_intelligence_5row_grid.html"
    )
    
    if output_file:
        print(f"\n🎉 STRATEGIC INTELLIGENCE REPORT COMPLETE!")
        print(f"📁 File location: {os.path.abspath(output_file)}")
        print(f"🎯 Format: Comprehensive strategic analysis with actionable insights")
        print(f"🧠 Features: McKinsey-level competitive intelligence and market landscape analysis")
        print(f"📊 Content: Deep strategic insights with evidence-based recommendations")

if __name__ == "__main__":
    main()