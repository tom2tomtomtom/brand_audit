#!/usr/bin/env python3
"""
Enhanced Brand Profiler V2 - Real Data Only
Multi-strategy extraction with no fallbacks
"""

import os
import json
import time
import re
from typing import Dict, List, Optional, Any, Tuple
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, WebDriverException
import openai
from urllib.parse import urlparse, urljoin
import hashlib
from collections import Counter
from PIL import Image
import io
import colorsys

class EnhancedBrandProfilerV2:
    def __init__(self, openai_api_key: str):
        # Try to use the new OpenAI client (v1.0+)
        self.openai_api_key = openai_api_key
        self.openai_client = None
        self.legacy_mode = False
        
        try:
            # Try new import style (OpenAI v1.0+)
            from openai import OpenAI
            self.openai_client = OpenAI(api_key=openai_api_key)
            print("Using OpenAI v1.0+ client")
        except ImportError:
            # Fall back to legacy mode (OpenAI < v1.0)
            openai.api_key = openai_api_key
            self.legacy_mode = True
            print("Using legacy OpenAI client (< v1.0)")
        
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def _call_openai_chat(self, messages: List[Dict[str, str]], model: str = "gpt-4o-mini", 
                          temperature: float = 0.3, max_tokens: int = 1000, 
                          response_format: Optional[Dict] = None) -> Any:
        """Wrapper to handle both old and new OpenAI API calls"""
        try:
            if self.legacy_mode:
                # Legacy API call (OpenAI < v1.0)
                kwargs = {
                    "model": model,
                    "messages": messages,
                    "temperature": temperature,
                    "max_tokens": max_tokens
                }
                # Note: response_format is not supported in legacy versions
                response = openai.ChatCompletion.create(**kwargs)
                return response
            else:
                # New API call (OpenAI v1.0+)
                kwargs = {
                    "model": model,
                    "messages": messages,
                    "temperature": temperature,
                    "max_tokens": max_tokens
                }
                if response_format:
                    kwargs["response_format"] = response_format
                response = self.openai_client.chat.completions.create(**kwargs)
                return response
        except Exception as e:
            print(f"OpenAI API call error: {e}")
            raise
        
    def profile_brand(self, url: str, max_retries: int = 3) -> Dict[str, Any]:
        """
        Profile a brand using multiple extraction strategies
        Returns only real extracted data, no fallbacks
        """
        start_time = time.time()
        profile_result = {
            'url': url,
            'timestamp': time.time(),
            'extraction_methods_attempted': [],
            'retry_count': 0
        }
        
        # Progressive extraction strategies
        extraction_strategies = [
            ('basic_scraping', self._extract_with_beautifulsoup),
            ('selenium_extraction', self._extract_with_selenium),
            ('visual_analysis', self._extract_visual_elements),
            ('structured_data', self._extract_structured_data),
            ('api_endpoints', self._extract_from_api_endpoints)
        ]
        
        cumulative_data = {}
        
        for retry in range(max_retries):
            profile_result['retry_count'] = retry
            
            for strategy_name, strategy_func in extraction_strategies:
                if strategy_name not in profile_result['extraction_methods_attempted']:
                    profile_result['extraction_methods_attempted'].append(strategy_name)
                
                try:
                    print(f"Attempting {strategy_name} for {url}...")
                    extracted_data = strategy_func(url)
                    
                    if extracted_data and self._validate_extraction(extracted_data):
                        cumulative_data.update(extracted_data)
                        
                        # Check if we have sufficient data
                        if self._has_sufficient_data(cumulative_data):
                            profile_result.update({
                                'status': 'success',
                                'extraction_method': {
                                    'primary': strategy_name,
                                    'all_used': profile_result['extraction_methods_attempted']
                                },
                                'data': self._enhance_with_ai_analysis(cumulative_data, url),
                                'extraction_duration': time.time() - start_time,
                                'extraction_confidence': self._calculate_confidence(cumulative_data)
                            })
                            return profile_result
                            
                except Exception as e:
                    print(f"Error with {strategy_name}: {str(e)}")
                    continue
            
            # If we have partial data, try AI enhancement
            if cumulative_data:
                enhanced = self._enhance_with_ai_analysis(cumulative_data, url)
                if self._validate_extraction(enhanced):
                    profile_result.update({
                        'status': 'partial_success',
                        'data': enhanced,
                        'extraction_duration': time.time() - start_time,
                        'extraction_confidence': self._calculate_confidence(enhanced)
                    })
                    return profile_result
        
        # No successful extraction
        profile_result.update({
            'status': 'failed',
            'error': 'Unable to extract sufficient brand data',
            'partial_data': cumulative_data if cumulative_data else None,
            'extraction_duration': time.time() - start_time
        })
        
        return profile_result
    
    def _extract_with_beautifulsoup(self, url: str) -> Optional[Dict[str, Any]]:
        """Extract data using BeautifulSoup"""
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Intelligent content extraction
            extracted = {
                'html_content': self._extract_meaningful_content(soup),
                'meta_data': self._extract_meta_tags(soup),
                'headings': self._extract_heading_hierarchy(soup),
                'navigation': self._extract_navigation_structure(soup),
                'semantic_sections': self._extract_semantic_html5(soup),
                'contact_info': self._extract_contact_information(soup),
                'social_links': self._extract_social_links(soup)
            }
            
            # Extract visual elements
            visual_data = self._extract_visual_from_html(soup, url)
            if visual_data:
                extracted.update(visual_data)
            
            return extracted
            
        except Exception as e:
            print(f"BeautifulSoup extraction error: {e}")
            return None
    
    def _extract_meaningful_content(self, soup: BeautifulSoup) -> Dict[str, str]:
        """Extract only meaningful content sections"""
        content = {}
        
        # Hero/Banner content
        hero_selectors = ['[class*="hero"]', '[class*="banner"]', '[class*="jumbotron"]', 
                         'header > div', 'section:first-of-type']
        for selector in hero_selectors:
            element = soup.select_one(selector)
            if element:
                content['hero_content'] = self._clean_text(element.get_text())
                break
        
        # Main content areas
        main_selectors = ['main', '[role="main"]', '#main', '.main-content', 'article']
        for selector in main_selectors:
            element = soup.select_one(selector)
            if element:
                # Get first few paragraphs
                paragraphs = element.find_all('p', limit=5)
                if paragraphs:
                    content['main_content'] = ' '.join(self._clean_text(p.get_text()) for p in paragraphs)
                break
        
        # About content
        about_selectors = ['[class*="about"]', '#about', '[id*="about-us"]']
        for selector in about_selectors:
            element = soup.select_one(selector)
            if element:
                content['about_content'] = self._clean_text(element.get_text())[:500]
                break
        
        # Features/Services
        feature_selectors = ['[class*="feature"]', '[class*="service"]', '[class*="benefit"]']
        features = []
        for selector in feature_selectors:
            elements = soup.select(selector)[:5]  # Limit to 5
            for element in elements:
                text = self._clean_text(element.get_text())
                if text and len(text) > 20:
                    features.append(text)
        
        if features:
            content['features'] = features
        
        return content
    
    def _extract_meta_tags(self, soup: BeautifulSoup) -> Dict[str, str]:
        """Extract all relevant meta tags"""
        meta_data = {}
        
        # Title
        title = soup.find('title')
        if title:
            meta_data['title'] = self._clean_text(title.string)
        
        # Meta tags
        meta_tags = soup.find_all('meta')
        for tag in meta_tags:
            name = tag.get('name') or tag.get('property')
            content = tag.get('content')
            
            if name and content:
                # Focus on relevant meta tags
                relevant_names = ['description', 'keywords', 'author', 'company', 
                                'og:title', 'og:description', 'og:site_name',
                                'twitter:title', 'twitter:description']
                if any(rel in name.lower() for rel in relevant_names):
                    meta_data[name] = content
        
        return meta_data
    
    def _extract_heading_hierarchy(self, soup: BeautifulSoup) -> Dict[str, List[str]]:
        """Extract heading hierarchy for structure understanding"""
        headings = {}
        
        for level in range(1, 4):  # h1, h2, h3
            heading_tags = soup.find_all(f'h{level}')
            heading_texts = [self._clean_text(h.get_text()) for h in heading_tags 
                           if self._clean_text(h.get_text())]
            if heading_texts:
                headings[f'h{level}'] = heading_texts[:10]  # Limit to 10 per level
        
        return headings
    
    def _extract_navigation_structure(self, soup: BeautifulSoup) -> List[str]:
        """Extract navigation menu items"""
        nav_items = []
        
        # Find navigation elements
        nav_selectors = ['nav', '[role="navigation"]', '.navigation', '#navigation', 
                        '.navbar', '.menu', '#menu']
        
        for selector in nav_selectors:
            nav = soup.select_one(selector)
            if nav:
                # Extract link texts
                links = nav.find_all('a')
                for link in links:
                    text = self._clean_text(link.get_text())
                    if text and len(text) > 1 and text not in nav_items:
                        nav_items.append(text)
                
                if nav_items:
                    break
        
        return nav_items[:20]  # Limit to 20 items
    
    def _extract_semantic_html5(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Extract content from semantic HTML5 elements"""
        semantic_content = {}
        
        # Semantic elements to check
        semantic_elements = ['article', 'section', 'aside', 'header', 'footer']
        
        for element_type in semantic_elements:
            elements = soup.find_all(element_type)
            if elements:
                # Get the most relevant content from each type
                content_list = []
                for element in elements[:3]:  # Limit to 3 per type
                    # Look for headings and first paragraph
                    heading = element.find(['h1', 'h2', 'h3', 'h4'])
                    paragraph = element.find('p')
                    
                    if heading or paragraph:
                        content_item = {}
                        if heading:
                            content_item['heading'] = self._clean_text(heading.get_text())
                        if paragraph:
                            content_item['content'] = self._clean_text(paragraph.get_text())
                        content_list.append(content_item)
                
                if content_list:
                    semantic_content[element_type] = content_list
        
        return semantic_content
    
    def _extract_visual_from_html(self, soup: BeautifulSoup, base_url: str) -> Dict[str, Any]:
        """Extract visual elements from HTML"""
        visual_data = {}
        
        # Extract logo
        logo_url = self._find_logo_url(soup, base_url)
        if logo_url:
            visual_data['logo_url'] = logo_url
        
        # Extract colors from inline styles
        colors = self._extract_colors_from_styles(soup)
        if colors:
            visual_data['colors'] = colors
        
        # Extract favicon
        favicon = self._find_favicon(soup, base_url)
        if favicon:
            visual_data['favicon_url'] = favicon
        
        return visual_data
    
    def _find_logo_url(self, soup: BeautifulSoup, base_url: str) -> Optional[str]:
        """Find logo URL using multiple strategies"""
        logo_selectors = [
            'img[class*="logo"]',
            'img[id*="logo"]',
            'img[alt*="logo" i]',
            'img[src*="logo" i]',
            '.logo img',
            '#logo img',
            'header img',
            'a[href="/"] img',
            'a[href="./"] img'
        ]
        
        for selector in logo_selectors:
            logo = soup.select_one(selector)
            if logo and logo.get('src'):
                logo_url = urljoin(base_url, logo['src'])
                # Validate it's an image
                if any(ext in logo_url.lower() for ext in ['.png', '.jpg', '.jpeg', '.svg', '.webp']):
                    return logo_url
        
        return None
    
    def _extract_colors_from_styles(self, soup: BeautifulSoup) -> List[str]:
        """Extract colors from inline styles and CSS"""
        colors = []
        color_pattern = re.compile(r'#[0-9a-fA-F]{3,6}|rgb\([^)]+\)|rgba\([^)]+\)')
        
        # Check inline styles
        elements_with_style = soup.find_all(style=True)
        for element in elements_with_style:
            style = element.get('style', '')
            found_colors = color_pattern.findall(style)
            colors.extend(found_colors)
        
        # Check style tags
        style_tags = soup.find_all('style')
        for style_tag in style_tags:
            if style_tag.string:
                found_colors = color_pattern.findall(style_tag.string)
                colors.extend(found_colors)
        
        # Clean and deduplicate
        unique_colors = []
        seen = set()
        
        for color in colors:
            # Normalize color format
            normalized = self._normalize_color(color)
            if normalized and normalized not in seen:
                seen.add(normalized)
                unique_colors.append(normalized)
        
        return unique_colors[:10]  # Return top 10 unique colors
    
    def _normalize_color(self, color: str) -> Optional[str]:
        """Normalize color to hex format"""
        color = color.strip()
        
        # Already hex
        if color.startswith('#'):
            if len(color) == 4:  # Convert #RGB to #RRGGBB
                return f"#{color[1]*2}{color[2]*2}{color[3]*2}"
            elif len(color) == 7:
                return color.upper()
        
        # RGB/RGBA
        elif color.startswith(('rgb(', 'rgba(')):
            numbers = re.findall(r'\d+', color)
            if len(numbers) >= 3:
                r, g, b = int(numbers[0]), int(numbers[1]), int(numbers[2])
                return f"#{r:02X}{g:02X}{b:02X}"
        
        return None
    
    def _find_favicon(self, soup: BeautifulSoup, base_url: str) -> Optional[str]:
        """Find favicon URL"""
        favicon_selectors = [
            'link[rel="icon"]',
            'link[rel="shortcut icon"]',
            'link[rel="apple-touch-icon"]'
        ]
        
        for selector in favicon_selectors:
            favicon = soup.select_one(selector)
            if favicon and favicon.get('href'):
                return urljoin(base_url, favicon['href'])
        
        # Try default location
        default_favicon = urljoin(base_url, '/favicon.ico')
        try:
            response = self.session.head(default_favicon, timeout=5)
            if response.status_code == 200:
                return default_favicon
        except:
            pass
        
        return None
    
    def _extract_contact_information(self, soup: BeautifulSoup) -> Dict[str, str]:
        """Extract contact information"""
        contact_info = {}
        
        # Email patterns
        email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
        emails = email_pattern.findall(str(soup))
        if emails:
            # Filter out common non-contact emails
            contact_emails = [e for e in emails if not any(x in e.lower() for x in 
                            ['noreply', 'no-reply', 'donotreply', 'example.com'])]
            if contact_emails:
                contact_info['email'] = contact_emails[0]
        
        # Phone patterns
        phone_pattern = re.compile(r'[\+]?[(]?[0-9]{1,4}[)]?[-\s\.]?[(]?[0-9]{1,4}[)]?[-\s\.]?[0-9]{1,5}[-\s\.]?[0-9]{1,5}')
        phones = phone_pattern.findall(str(soup))
        if phones:
            # Filter out too short numbers
            valid_phones = [p for p in phones if len(re.sub(r'\D', '', p)) >= 10]
            if valid_phones:
                contact_info['phone'] = valid_phones[0]
        
        # Address - look for common address containers
        address_selectors = ['address', '[class*="address"]', '[itemtype*="PostalAddress"]']
        for selector in address_selectors:
            address = soup.select_one(selector)
            if address:
                contact_info['address'] = self._clean_text(address.get_text())
                break
        
        return contact_info
    
    def _extract_social_links(self, soup: BeautifulSoup) -> Dict[str, str]:
        """Extract social media links"""
        social_links = {}
        
        social_patterns = {
            'twitter': r'twitter\.com/([^/\s]+)',
            'facebook': r'facebook\.com/([^/\s]+)',
            'linkedin': r'linkedin\.com/company/([^/\s]+)',
            'instagram': r'instagram\.com/([^/\s]+)',
            'youtube': r'youtube\.com/(@?[^/\s]+)'
        }
        
        all_links = soup.find_all('a', href=True)
        
        for link in all_links:
            href = link.get('href', '')
            for platform, pattern in social_patterns.items():
                if platform in href:
                    match = re.search(pattern, href)
                    if match:
                        social_links[platform] = match.group(1)
        
        return social_links
    
    def _extract_with_selenium(self, url: str) -> Optional[Dict[str, Any]]:
        """Extract data using Selenium for JavaScript-rendered content"""
        driver = None
        try:
            options = Options()
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-gpu')
            options.add_argument('--window-size=1920,1080')
            
            driver = webdriver.Chrome(options=options)
            driver.get(url)
            
            # Wait for content to load
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Additional wait for dynamic content
            time.sleep(2)
            
            # Get page source after JavaScript execution
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            
            # Extract using BeautifulSoup methods
            extracted = self._extract_with_beautifulsoup_from_soup(soup, url)
            
            # Additional Selenium-specific extractions
            if extracted:
                # Get computed styles for colors
                computed_colors = self._extract_computed_colors(driver)
                if computed_colors:
                    extracted['computed_colors'] = computed_colors
                
                # Take screenshot for visual analysis
                screenshot = driver.get_screenshot_as_png()
                if screenshot:
                    extracted['screenshot'] = screenshot
            
            return extracted
            
        except Exception as e:
            print(f"Selenium extraction error: {e}")
            return None
        finally:
            if driver:
                driver.quit()
    
    def _extract_with_beautifulsoup_from_soup(self, soup: BeautifulSoup, url: str) -> Dict[str, Any]:
        """Extract data from pre-parsed soup"""
        extracted = {
            'html_content': self._extract_meaningful_content(soup),
            'meta_data': self._extract_meta_tags(soup),
            'headings': self._extract_heading_hierarchy(soup),
            'navigation': self._extract_navigation_structure(soup),
            'semantic_sections': self._extract_semantic_html5(soup),
            'contact_info': self._extract_contact_information(soup),
            'social_links': self._extract_social_links(soup)
        }
        
        visual_data = self._extract_visual_from_html(soup, url)
        if visual_data:
            extracted.update(visual_data)
        
        return extracted
    
    def _extract_computed_colors(self, driver) -> List[str]:
        """Extract computed colors using Selenium"""
        try:
            # Get colors from key elements
            selectors = ['body', 'header', 'nav', '.hero', '.banner', 'footer', 
                        'h1', 'h2', '.button', '.btn', 'a']
            
            colors = set()
            
            for selector in selectors:
                try:
                    elements = driver.find_elements(By.CSS_SELECTOR, selector)
                    for element in elements[:3]:  # Limit per selector
                        # Get background color
                        bg_color = element.value_of_css_property('background-color')
                        if bg_color and bg_color != 'rgba(0, 0, 0, 0)':
                            hex_color = self._rgb_to_hex(bg_color)
                            if hex_color:
                                colors.add(hex_color)
                        
                        # Get text color
                        text_color = element.value_of_css_property('color')
                        if text_color:
                            hex_color = self._rgb_to_hex(text_color)
                            if hex_color:
                                colors.add(hex_color)
                except:
                    continue
            
            return list(colors)[:10]
            
        except Exception as e:
            print(f"Error extracting computed colors: {e}")
            return []
    
    def _rgb_to_hex(self, rgb_string: str) -> Optional[str]:
        """Convert RGB string to hex"""
        try:
            # Extract numbers from rgb/rgba string
            numbers = re.findall(r'\d+', rgb_string)
            if len(numbers) >= 3:
                r, g, b = int(numbers[0]), int(numbers[1]), int(numbers[2])
                return f"#{r:02X}{g:02X}{b:02X}"
        except:
            pass
        return None
    
    def _extract_visual_elements(self, url: str) -> Optional[Dict[str, Any]]:
        """Extract visual elements through screenshot analysis"""
        driver = None
        try:
            options = Options()
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--window-size=1920,1080')
            
            driver = webdriver.Chrome(options=options)
            driver.get(url)
            
            # Wait for page load
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            time.sleep(2)
            
            # Take screenshot
            screenshot = driver.get_screenshot_as_png()
            
            # Analyze screenshot for colors
            visual_data = self._analyze_screenshot(screenshot)
            
            return visual_data
            
        except Exception as e:
            print(f"Visual extraction error: {e}")
            return None
        finally:
            if driver:
                driver.quit()
    
    def _analyze_screenshot(self, screenshot_data: bytes) -> Dict[str, Any]:
        """Analyze screenshot for visual elements"""
        try:
            # Open image
            image = Image.open(io.BytesIO(screenshot_data))
            
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Get dominant colors
            colors = self._extract_dominant_colors(image)
            
            return {
                'screenshot_colors': colors,
                'screenshot_analyzed': True
            }
            
        except Exception as e:
            print(f"Screenshot analysis error: {e}")
            return {}
    
    def _extract_dominant_colors(self, image: Image.Image, num_colors: int = 5) -> List[str]:
        """Extract dominant colors from image"""
        try:
            # Resize for performance
            image = image.resize((150, 150))
            
            # Get colors
            pixels = list(image.getdata())
            
            # Count colors (simple approach)
            color_counts = Counter(pixels)
            
            # Get most common colors
            dominant_colors = []
            
            for color, count in color_counts.most_common(50):
                # Convert to hex
                hex_color = f"#{color[0]:02X}{color[1]:02X}{color[2]:02X}"
                
                # Skip near white/black/gray
                r, g, b = color
                
                # Check if it's not too close to white
                if r > 240 and g > 240 and b > 240:
                    continue
                
                # Check if it's not too close to black
                if r < 15 and g < 15 and b < 15:
                    continue
                
                # Check if it's not too gray (low saturation)
                h, s, v = colorsys.rgb_to_hsv(r/255, g/255, b/255)
                if s < 0.1:  # Low saturation means gray
                    continue
                
                dominant_colors.append(hex_color)
                
                if len(dominant_colors) >= num_colors:
                    break
            
            return dominant_colors
            
        except Exception as e:
            print(f"Color extraction error: {e}")
            return []
    
    def _extract_structured_data(self, url: str) -> Optional[Dict[str, Any]]:
        """Extract structured data (JSON-LD, microdata)"""
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            structured_data = {}
            
            # Extract JSON-LD
            json_ld_scripts = soup.find_all('script', type='application/ld+json')
            if json_ld_scripts:
                json_ld_data = []
                for script in json_ld_scripts:
                    try:
                        data = json.loads(script.string)
                        json_ld_data.append(data)
                    except:
                        continue
                
                if json_ld_data:
                    structured_data['json_ld'] = json_ld_data
            
            # Extract OpenGraph data
            og_data = {}
            og_tags = soup.find_all('meta', property=re.compile(r'^og:'))
            for tag in og_tags:
                property_name = tag.get('property', '').replace('og:', '')
                content = tag.get('content')
                if property_name and content:
                    og_data[property_name] = content
            
            if og_data:
                structured_data['open_graph'] = og_data
            
            # Extract Twitter Card data
            twitter_data = {}
            twitter_tags = soup.find_all('meta', attrs={'name': re.compile(r'^twitter:')})
            for tag in twitter_tags:
                name = tag.get('name', '').replace('twitter:', '')
                content = tag.get('content')
                if name and content:
                    twitter_data[name] = content
            
            if twitter_data:
                structured_data['twitter_card'] = twitter_data
            
            return structured_data if structured_data else None
            
        except Exception as e:
            print(f"Structured data extraction error: {e}")
            return None
    
    def _extract_from_api_endpoints(self, url: str) -> Optional[Dict[str, Any]]:
        """Try to extract data from common API endpoints"""
        try:
            parsed_url = urlparse(url)
            base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
            
            # Common API endpoints to try
            api_endpoints = [
                '/api/config',
                '/api/site-info',
                '/api/about',
                '/.well-known/site-info',
                '/site.webmanifest',
                '/manifest.json'
            ]
            
            api_data = {}
            
            for endpoint in api_endpoints:
                try:
                    api_url = urljoin(base_url, endpoint)
                    response = self.session.get(api_url, timeout=5)
                    
                    if response.status_code == 200:
                        content_type = response.headers.get('content-type', '')
                        
                        if 'json' in content_type:
                            data = response.json()
                            api_data[endpoint] = data
                        elif endpoint.endswith('.json'):
                            try:
                                data = response.json()
                                api_data[endpoint] = data
                            except:
                                pass
                except:
                    continue
            
            return api_data if api_data else None
            
        except Exception as e:
            print(f"API endpoint extraction error: {e}")
            return None
    
    def _enhance_with_ai_analysis(self, raw_data: Dict[str, Any], url: str) -> Dict[str, Any]:
        """Enhance extracted data with AI analysis"""
        try:
            # Prepare content for AI analysis
            content_summary = self._prepare_content_for_ai(raw_data)
            
            if not content_summary:
                return raw_data
            
            # Detect industry first
            industry = self._detect_industry(content_summary)
            
            # Generate adaptive prompts based on content
            prompts = self._generate_adaptive_prompts(content_summary, industry)
            
            # Extract brand information with multiple attempts
            brand_info = None
            for prompt_type, prompt in prompts.items():
                brand_info = self._extract_brand_info_with_ai(content_summary, prompt)
                if brand_info and self._validate_ai_extraction(brand_info):
                    break
            
            if not brand_info:
                return raw_data
            
            # Merge AI insights with raw data
            enhanced_data = raw_data.copy()
            enhanced_data.update(brand_info)
            
            # Add extraction metadata
            enhanced_data['ai_enhanced'] = True
            enhanced_data['industry_detected'] = industry
            enhanced_data['url'] = url
            
            return enhanced_data
            
        except Exception as e:
            print(f"AI enhancement error: {e}")
            return raw_data
    
    def _prepare_content_for_ai(self, raw_data: Dict[str, Any]) -> str:
        """Prepare extracted content for AI analysis"""
        content_parts = []
        
        # Add meta data
        if raw_data.get('meta_data'):
            meta = raw_data['meta_data']
            if meta.get('title'):
                content_parts.append(f"Title: {meta['title']}")
            if meta.get('description'):
                content_parts.append(f"Description: {meta['description']}")
        
        # Add headings
        if raw_data.get('headings'):
            for level, headings in raw_data['headings'].items():
                content_parts.append(f"{level.upper()}: {', '.join(headings[:5])}")
        
        # Add main content
        if raw_data.get('html_content'):
            content = raw_data['html_content']
            if content.get('hero_content'):
                content_parts.append(f"Hero: {content['hero_content'][:500]}")
            if content.get('main_content'):
                content_parts.append(f"Main: {content['main_content'][:500]}")
            if content.get('about_content'):
                content_parts.append(f"About: {content['about_content'][:500]}")
        
        # Add navigation
        if raw_data.get('navigation'):
            content_parts.append(f"Navigation: {', '.join(raw_data['navigation'][:10])}")
        
        # Add structured data insights
        if raw_data.get('json_ld'):
            content_parts.append("Structured data found")
        
        return '\n\n'.join(content_parts)
    
    def _detect_industry(self, content: str) -> str:
        """Detect industry from content"""
        try:
            messages = [
                {"role": "system", "content": "You are an expert at identifying business industries."},
                {"role": "user", "content": f"""Based on this website content, identify the primary industry/sector.
Be specific but concise (e.g., "SaaS project management", "E-commerce fashion", 
"Healthcare technology", "Financial services").

Content:
{content[:2000]}

Industry:"""}
            ]
            
            response = self._call_openai_chat(messages, temperature=0.3, max_tokens=50)
            
            if self.legacy_mode:
                return response.choices[0].message['content'].strip()
            else:
                return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"Industry detection error: {e}")
            return "Unknown"
    
    def _generate_adaptive_prompts(self, content: str, industry: str) -> Dict[str, str]:
        """Generate adaptive prompts based on content and industry"""
        prompts = {}
        
        # Detailed extraction prompt
        prompts['detailed'] = f"""
        Analyze this {industry} company's website content and extract:
        
        1. Company name (from title, headers, or about section)
        2. Brand positioning statement (main value proposition from hero/homepage)
        3. Key messages (3-5 main points they emphasize)
        4. Target audience (who they're speaking to)
        5. Unique differentiation factors
        
        Content:
        {content}
        
        Extract only what you can clearly identify from the content. 
        Return null for any fields you cannot determine with confidence.
        
        Return as JSON:
        {{
            "company_name": "...",
            "positioning": "...",
            "value_proposition": "...",
            "messages": ["...", "..."],
            "target_audience": ["...", "..."],
            "personality_traits": ["...", "..."],
            "differentiation_factors": ["...", "..."]
        }}
        """
        
        # Simplified prompt for fallback
        prompts['simplified'] = """
        From this website content, extract:
        1. Company name
        2. What they do (one sentence)
        3. Who they serve
        
        Content:
        {content}
        
        Return only clearly identifiable information as JSON:
        {{
            "company_name": "...",
            "positioning": "...",
            "target_audience": ["..."]
        }}
        """
        
        # Guided extraction with examples
        prompts['guided'] = f"""
        Step-by-step analysis of this {industry} website:
        
        Step 1: Find the company name
        - Check: title tags, logo alt text, headers, about sections
        
        Step 2: Identify main value proposition
        - Check: hero headlines, taglines, first prominent text
        
        Step 3: Extract key messages
        - Check: subheadings, repeated themes, benefit statements
        
        Content:
        {content}
        
        Only include findings you're confident about. Return as JSON.
        """
        
        return prompts
    
    def _extract_brand_info_with_ai(self, content: str, prompt_template: str) -> Optional[Dict[str, Any]]:
        """Extract brand information using AI"""
        try:
            # Format prompt with content
            prompt = prompt_template.format(content=content[:3000])  # Limit content length
            
            messages = [
                {"role": "system", "content": "You are a brand analysis expert. Extract only real, identifiable information. Never make up or infer information that isn't clearly present."},
                {"role": "user", "content": prompt}
            ]
            
            # Use JSON mode only for new API
            kwargs = {}
            if not self.legacy_mode:
                kwargs['response_format'] = {"type": "json_object"}
            
            response = self._call_openai_chat(
                messages, 
                model="gpt-4o" if not self.legacy_mode else "gpt-4", 
                temperature=0.2,
                max_tokens=1000,
                **kwargs
            )
            
            if self.legacy_mode:
                content = response.choices[0].message['content']
            else:
                content = response.choices[0].message.content
            
            result = json.loads(content)
            
            # Clean up the result
            cleaned_result = {}
            for key, value in result.items():
                if value and value != "null" and value != "Unknown":
                    if isinstance(value, list):
                        # Filter out empty or placeholder values from lists
                        cleaned_list = [v for v in value if v and v != "Unknown"]
                        if cleaned_list:
                            cleaned_result[key] = cleaned_list
                    else:
                        cleaned_result[key] = value
            
            return cleaned_result if cleaned_result else None
            
        except Exception as e:
            print(f"AI extraction error: {e}")
            return None
    
    def _validate_extraction(self, data: Dict[str, Any]) -> bool:
        """Validate extracted data has minimum required information"""
        if not data:
            return False
        
        # Minimum required fields
        required_fields = ['company_name', 'positioning']
        
        for field in required_fields:
            if field not in data or not data[field]:
                return False
            
            # Check for placeholder values
            value = data[field]
            if isinstance(value, str):
                if value.lower() in ['unknown', 'n/a', 'not found', '']:
                    return False
        
        return True
    
    def _validate_ai_extraction(self, data: Dict[str, Any]) -> bool:
        """Validate AI-extracted data"""
        if not data:
            return False
        
        # Check for minimum content
        if len(data) < 2:  # At least 2 fields
            return False
        
        # Check for actual content vs placeholders
        total_fields = 0
        valid_fields = 0
        
        for key, value in data.items():
            total_fields += 1
            
            if isinstance(value, str):
                if len(value) > 10 and value.lower() not in ['unknown', 'n/a', 'not found']:
                    valid_fields += 1
            elif isinstance(value, list):
                if value and any(len(str(v)) > 5 for v in value):
                    valid_fields += 1
        
        # Require at least 50% valid fields
        return valid_fields / total_fields >= 0.5 if total_fields > 0 else False
    
    def _has_sufficient_data(self, data: Dict[str, Any]) -> bool:
        """Check if we have sufficient data to stop extraction"""
        # Define what constitutes sufficient data
        required_elements = {
            'company_name': lambda x: x and len(x) > 0,
            'positioning': lambda x: x and len(x) > 20,
            'messages': lambda x: x and len(x) >= 2,
            'colors': lambda x: x and len(x) >= 2
        }
        
        score = 0
        for field, validator in required_elements.items():
            if field in data and validator(data[field]):
                score += 1
        
        # Require at least 75% of elements
        return score >= len(required_elements) * 0.75
    
    def _calculate_confidence(self, data: Dict[str, Any]) -> float:
        """Calculate confidence score for extracted data"""
        scores = []
        
        # Company name confidence
        if data.get('company_name'):
            name = data['company_name']
            score = 1.0 if len(name) > 3 else 0.5
            # Check if it appears in multiple places
            if data.get('meta_data', {}).get('title', '').lower().find(name.lower()) >= 0:
                score = 1.0
            scores.append(score)
        
        # Positioning confidence
        if data.get('positioning'):
            positioning = data['positioning']
            score = min(len(positioning) / 100, 1.0)  # Longer = more confident
            scores.append(score)
        
        # Messages confidence
        if data.get('messages'):
            messages = data['messages']
            score = min(len(messages) / 5, 1.0)  # More messages = more confident
            scores.append(score)
        
        # Visual elements confidence
        if data.get('colors') or data.get('logo_url'):
            scores.append(0.9)
        
        # AI enhancement confidence
        if data.get('ai_enhanced'):
            scores.append(0.8)
        
        return sum(scores) / len(scores) if scores else 0.0
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        if not text:
            return ""
        
        # Remove excess whitespace
        text = ' '.join(text.split())
        
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s\-.,!?;:\'""]', ' ', text)
        
        # Remove multiple spaces
        text = re.sub(r'\s+', ' ', text)
        
        return text.strip()
