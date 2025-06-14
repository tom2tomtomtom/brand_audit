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
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
from playwright.sync_api import sync_playwright

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class EnhancedBrandProfilerV2:
    """Real data only brand profiler with multi-strategy extraction"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.driver = None
    
    def analyze_brand(self, url):
        """Main entry point - returns real data or None"""
        print(f"🔍 Analyzing: {url}")
        
        # Try multiple extraction strategies
        extraction_result = self.extract_with_fallbacks(url)
        
        if not extraction_result or extraction_result.get("status") == "failed":
            return self.handle_extraction_failure(url, "No content could be extracted")
        
        # Process extracted content
        content = extraction_result.get("content")
        if not content:
            return self.handle_extraction_failure(url, "Empty content")
        
        # Intelligent content parsing
        parsed_content = self.intelligent_content_extraction(content)
        
        # Extract brand data with validation
        brand_data = self.extract_with_retry(parsed_content, url)
        
        if not brand_data:
            return self.handle_extraction_failure(url, "Brand data extraction failed")
        
        # Validate extraction quality
        if not self.validate_extraction(brand_data):
            return self.handle_extraction_failure(url, "Extracted data failed validation")
        
        # Extract visual elements
        visual_data = self.extract_visual_elements(url, content)
        
        # Compile final profile
        brand_profile = {
            "status": "success",
            "url": url,
            "extraction_method": extraction_result.get("method"),
            "brand_data": brand_data,
            "visual_data": visual_data,
            "extraction_quality": self.score_extraction_quality(brand_data),
            "timestamp": pd.Timestamp.now().isoformat()
        }
        
        return brand_profile
    
    def handle_extraction_failure(self, url, error_type):
        """Handle failed extractions without fallback data"""
        return {
            "status": "failed",
            "url": url,
            "error": error_type,
            "extracted_data": None,
            "timestamp": pd.Timestamp.now().isoformat()
        }
    
    def extract_with_fallbacks(self, url):
        """Try multiple extraction strategies"""
        strategies = [
            ("beautifulsoup", self.extract_with_beautifulsoup),
            ("selenium", self.extract_with_selenium),
            ("playwright", self.extract_with_playwright),
        ]
        
        for strategy_name, strategy_func in strategies:
            try:
                print(f"  → Trying {strategy_name}...")
                result = strategy_func(url)
                if result and result.get("content"):
                    print(f"  ✓ Success with {strategy_name}")
                    return {
                        "status": "success",
                        "method": strategy_name,
                        "content": result["content"]
                    }
            except Exception as e:
                print(f"  ✗ {strategy_name} failed: {str(e)[:50]}")
                continue
        
        return {"status": "failed", "url": url}
    
    def extract_with_beautifulsoup(self, url):
        """Basic extraction with BeautifulSoup"""
        try:
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            return {"content": response.text}
        except Exception as e:
            raise Exception(f"BeautifulSoup extraction failed: {e}")
    
    def extract_with_selenium(self, url):
        """Selenium extraction for JavaScript-heavy sites"""
        driver = None
        try:
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--window-size=1920,1080')
            
            driver = webdriver.Chrome(options=chrome_options)
            driver.get(url)
            
            # Wait for dynamic content
            time.sleep(5)
            
            # Scroll to load lazy content
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
            time.sleep(2)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            
            content = driver.page_source
            return {"content": content}
            
        except Exception as e:
            raise Exception(f"Selenium extraction failed: {e}")
        finally:
            if driver:
                driver.quit()
    
    def extract_with_playwright(self, url):
        """Playwright extraction for modern web apps"""
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                context = browser.new_context(
                    viewport={'width': 1920, 'height': 1080},
                    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                )
                page = context.new_page()
                
                # Navigate and wait for network idle
                page.goto(url, wait_until='networkidle')
                
                # Additional wait for SPA rendering
                page.wait_for_timeout(3000)
                
                content = page.content()
                browser.close()
                
                return {"content": content}
                
        except Exception as e:
            raise Exception(f"Playwright extraction failed: {e}")
    
    def intelligent_content_extraction(self, html_content):
        """Extract only meaningful content, no truncation"""
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        content = {
            "headings": self.extract_all_headings(soup),
            "nav_structure": self.extract_navigation_tree(soup),
            "main_content": self.extract_main_content_blocks(soup),
            "structured_data": self.extract_json_ld(soup),
            "meta_data": self.extract_all_meta_tags(soup),
            "semantic_sections": self.extract_semantic_html5(soup),
            "text_content": self.extract_visible_text(soup)
        }
        
        return content
    
    def extract_all_headings(self, soup):
        """Extract all headings with hierarchy"""
        headings = {}
        for level in range(1, 7):
            headings[f'h{level}'] = [h.get_text(strip=True) for h in soup.find_all(f'h{level}') if h.get_text(strip=True)]
        return headings
    
    def extract_navigation_tree(self, soup):
        """Extract navigation structure"""
        nav_items = []
        nav_selectors = ['nav', '[role="navigation"]', '.nav', '.menu', 'header']
        
        for selector in nav_selectors:
            elements = soup.select(selector)
            for elem in elements:
                links = elem.find_all('a')
                for link in links:
                    text = link.get_text(strip=True)
                    href = link.get('href', '')
                    if text and len(text) < 50:  # Avoid long text blocks
                        nav_items.append({
                            'text': text,
                            'href': href
                        })
        
        return nav_items
    
    def extract_main_content_blocks(self, soup):
        """Extract main content areas"""
        content_blocks = []
        content_selectors = [
            'main', 'article', '[role="main"]', '.content', '#content',
            '.hero', '[class*="hero"]', '.banner'
        ]
        
        for selector in content_selectors:
            elements = soup.select(selector)
            for elem in elements:
                text = elem.get_text(separator=' ', strip=True)
                if len(text) > 50:  # Meaningful content
                    content_blocks.append({
                        'selector': selector,
                        'text': text[:2000],  # Limit per block
                        'word_count': len(text.split())
                    })
        
        return content_blocks
    
    def extract_json_ld(self, soup):
        """Extract structured data"""
        json_ld_scripts = soup.find_all('script', type='application/ld+json')
        structured_data = []
        
        for script in json_ld_scripts:
            try:
                data = json.loads(script.string)
                structured_data.append(data)
            except:
                continue
        
        return structured_data
    
    def extract_all_meta_tags(self, soup):
        """Extract all meta information"""
        meta_data = {}
        
        # Title
        title_tag = soup.find('title')
        if title_tag:
            meta_data['title'] = title_tag.get_text(strip=True)
        
        # Meta tags
        for meta in soup.find_all('meta'):
            name = meta.get('name') or meta.get('property', '')
            content = meta.get('content', '')
            if name and content:
                meta_data[name] = content
        
        return meta_data
    
    def extract_semantic_html5(self, soup):
        """Extract semantic HTML5 sections"""
        semantic_tags = ['header', 'main', 'footer', 'article', 'section', 'aside']
        semantic_content = {}
        
        for tag in semantic_tags:
            elements = soup.find_all(tag)
            if elements:
                semantic_content[tag] = [elem.get_text(separator=' ', strip=True)[:500] for elem in elements[:3]]
        
        return semantic_content
    
    def extract_visible_text(self, soup):
        """Extract all visible text content"""
        # Get text from body
        body = soup.find('body')
        if body:
            text = body.get_text(separator=' ', strip=True)
            # Clean up multiple spaces
            text = ' '.join(text.split())
            return text
        return ""
    
    def detect_industry_context(self, content):
        """Dynamically detect industry from content"""
        all_text = ' '.join([
            content.get('text_content', ''),
            ' '.join(content.get('headings', {}).get('h1', [])),
            ' '.join(content.get('headings', {}).get('h2', []))
        ])
        
        messages = [
            {"role": "system", "content": "You are an expert at identifying business industries and sectors."},
            {"role": "user", "content": f"""
            Based on this website content, identify:
            1. Primary industry/sector
            2. Business model type (B2B/B2C/B2B2C)
            3. Key industry-specific terminology found
            
            Content preview: {all_text[:1000]}
            
            Return as JSON:
            {{
                "industry": "Primary industry",
                "business_model": "B2B/B2C/B2B2C",
                "key_terms": ["term1", "term2", "term3"]
            }}
            """}
        ]
        
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                temperature=0.1,
                max_tokens=200
            )
            
            content = response.choices[0].message.content.strip()
            return json.loads(re.sub(r"```(json)?", "", content).strip())
        except:
            return None
    
    def extract_with_retry(self, content, url, max_attempts=3):
        """Extract with retry logic using different prompts"""
        industry_context = self.detect_industry_context(content)
        
        prompts = [
            self.detailed_extraction_prompt,
            self.simplified_extraction_prompt,
            self.guided_extraction_prompt
        ]
        
        for i, prompt_func in enumerate(prompts):
            try:
                prompt = prompt_func(content, url, industry_context)
                result = self.call_llm_with_validation(prompt, content)
                
                if result and self.validate_extraction(result):
                    return result
                    
            except Exception as e:
                print(f"  → Attempt {i+1} failed: {str(e)[:50]}")
                if i == len(prompts) - 1:
                    return None
                continue
        
        return None
    
    def detailed_extraction_prompt(self, content, url, industry_context):
        """Detailed extraction prompt"""
        return f"""
        Analyze this website content and extract brand information.
        URL: {url}
        {f"Detected Industry: {industry_context.get('industry')}" if industry_context else ""}
        
        Extract the following from the actual content:
        1. Company name (from title, headers, logo alt text, or about sections)
        2. Brand positioning (main value proposition from hero section or headlines)
        3. Key messages (primary benefit statements or value props)
        4. Target audience (who they serve based on content)
        5. Brand personality (tone and style of communication)
        
        Content to analyze:
        Title: {content.get('meta_data', {}).get('title', '')}
        H1 headings: {content.get('headings', {}).get('h1', [])}
        Main content preview: {content.get('text_content', '')[:1000]}
        
        IMPORTANT: Only extract what you can clearly identify from the content. 
        If you cannot find clear evidence for a field, set it to null.
        Do not make assumptions or provide generic placeholders.
        
        Return as valid JSON with confidence scores for each field.
        """
    
    def simplified_extraction_prompt(self, content, url, industry_context):
        """Simplified extraction prompt"""
        return f"""
        Extract basic brand information from this website:
        
        1. What is the company name? (Look in title, headers, about)
        2. What do they do? (Main headline or value proposition)
        3. Who do they serve? (Target audience from content)
        
        Content:
        Page title: {content.get('meta_data', {}).get('title', '')}
        Main headings: {' | '.join(content.get('headings', {}).get('h1', [])[:3])}
        
        Only include information explicitly found in the content.
        Return as JSON with only the fields you can confidently extract.
        """
    
    def guided_extraction_prompt(self, content, url, industry_context):
        """Step-by-step guided extraction"""
        return f"""
        Let's extract brand information step-by-step:
        
        Step 1: Find the company name
        - Check the <title> tag: {content.get('meta_data', {}).get('title', '')}
        - Check H1 headings: {content.get('headings', {}).get('h1', [])}
        - Check meta description: {content.get('meta_data', {}).get('description', '')}
        
        Step 2: Find the main value proposition
        - Look for hero section text
        - Check prominent headlines
        - First major text block: {content.get('text_content', '')[:300]}
        
        Step 3: Identify key messages
        - Look for benefit statements
        - Check feature lists
        - Repeated themes in navigation: {[item['text'] for item in content.get('nav_structure', [])[:10]]}
        
        Only extract what is clearly present. Return null for unclear fields.
        Include confidence scores (0-1) for each extraction.
        """
    
    def call_llm_with_validation(self, prompt, content):
        """Call LLM with structured output validation"""
        
        # Select model based on content complexity
        model = self.select_model_for_content(content)
        
        messages = [
            {"role": "system", "content": "You are an expert at extracting factual information from websites. Only extract what is clearly present in the content."},
            {"role": "user", "content": prompt}
        ]
        
        # Use function calling for structured output
        functions = [{
            "name": "extract_brand_data",
            "description": "Extract brand information from website content",
            "parameters": {
                "type": "object",
                "properties": {
                    "company_name": {
                        "type": ["string", "null"],
                        "description": "Official company name if found"
                    },
                    "brand_positioning": {
                        "type": ["string", "null"],
                        "description": "Main value proposition or positioning statement"
                    },
                    "key_messages": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Primary messages or benefits"
                    },
                    "target_audience": {
                        "type": ["string", "null"],
                        "description": "Target customer description"
                    },
                    "brand_personality": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Brand personality traits"
                    },
                    "confidence_scores": {
                        "type": "object",
                        "properties": {
                            "company_name": {"type": "number", "minimum": 0, "maximum": 1},
                            "positioning": {"type": "number", "minimum": 0, "maximum": 1},
                            "overall": {"type": "number", "minimum": 0, "maximum": 1}
                        }
                    }
                },
                "required": ["confidence_scores"]
            }
        }]
        
        try:
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                functions=functions,
                function_call={"name": "extract_brand_data"},
                temperature=0.1,
                max_tokens=1500
            )
            
            function_call = response.choices[0].message.function_call
            if function_call and function_call.name == "extract_brand_data":
                return json.loads(function_call.arguments)
            
        except Exception as e:
            print(f"  ✗ LLM call failed: {e}")
            return None
    
    def select_model_for_content(self, content):
        """Choose appropriate model based on content"""
        text_length = len(content.get('text_content', ''))
        
        # Estimate complexity
        has_structured_data = bool(content.get('structured_data'))
        nav_items = len(content.get('nav_structure', []))
        
        if text_length > 50000 or has_structured_data or nav_items > 20:
            return "gpt-4"  # Better for complex analysis
        elif text_length < 5000:
            return "gpt-4o-mini"  # Sufficient for simple sites
        else:
            return "gpt-4o"  # Balanced choice
    
    def validate_extraction(self, data):
        """Validate extraction without providing defaults"""
        if not data:
            return False
        
        # Check confidence scores
        confidence = data.get('confidence_scores', {})
        if confidence.get('overall', 0) < 0.5:
            return False
        
        # Validate required fields
        if not data.get('company_name') or data['company_name'] == 'Unknown':
            return False
        
        # At least one key field should be present
        has_content = any([
            data.get('brand_positioning'),
            data.get('key_messages'),
            data.get('target_audience')
        ])
        
        return has_content
    
    def validate_with_feedback(self, extraction, original_content):
        """Validate extraction against original content"""
        issues = []
        
        # Check if company name appears in content
        if extraction.get('company_name'):
            name_lower = extraction['company_name'].lower()
            content_lower = original_content.lower()
            if name_lower not in content_lower:
                issues.append("Company name not found in original content")
        
        # Check positioning statement
        if extraction.get('brand_positioning'):
            # Allow for paraphrasing but check key terms
            position_words = extraction['brand_positioning'].lower().split()
            found_words = sum(1 for word in position_words if word in original_content.lower())
            if found_words < len(position_words) * 0.3:  # Less than 30% match
                issues.append("Positioning statement has low content match")
        
        return {"valid": len(issues) == 0, "issues": issues}
    
    def score_extraction_quality(self, extracted_data):
        """Score extraction quality"""
        if not extracted_data:
            return 0
        
        quality_score = 0
        max_score = 0
        
        # Company name quality
        if extracted_data.get('company_name'):
            name = extracted_data['company_name']
            if len(name) > 2 and not name.lower() in ['unknown', 'company', 'brand']:
                quality_score += extracted_data.get('confidence_scores', {}).get('company_name', 0.5)
            max_score += 1
        
        # Positioning quality
        if extracted_data.get('brand_positioning'):
            positioning = extracted_data['brand_positioning']
            if len(positioning) > 20 and len(positioning) < 500:
                quality_score += extracted_data.get('confidence_scores', {}).get('positioning', 0.5)
            max_score += 1
        
        # Messages quality
        messages = extracted_data.get('key_messages', [])
        if messages and len(messages) > 0:
            valid_messages = [m for m in messages if len(m) > 10]
            quality_score += min(len(valid_messages) / 3, 1.0)
        max_score += 1
        
        # Target audience quality
        if extracted_data.get('target_audience'):
            audience = extracted_data['target_audience']
            if len(audience) > 15 and not any(generic in audience.lower() for generic in ['everyone', 'all', 'general']):
                quality_score += 0.8
            max_score += 1
        
        return quality_score / max_score if max_score > 0 else 0
    
    def extract_visual_elements(self, url, html_content):
        """Multi-method visual extraction"""
        methods = {
            "css_extraction": lambda: self.extract_from_computed_styles(html_content),
            "screenshot_analysis": lambda: self.analyze_screenshot_colors(url),
            "svg_parsing": lambda: self.extract_svg_colors(html_content),
            "logo_extraction": lambda: self.extract_logos_comprehensive(html_content, url)
        }
        
        visual_data = {}
        for method_name, method_func in methods.items():
            try:
                result = method_func()
                if result:
                    visual_data[method_name] = result
            except Exception as e:
                print(f"  → {method_name} failed: {str(e)[:50]}")
                continue
        
        return visual_data if visual_data else None
    
    def extract_from_computed_styles(self, html_content):
        """Extract colors from CSS"""
        soup = BeautifulSoup(html_content, 'html.parser')
        colors = set()
        
        # Extract from inline styles
        for element in soup.find_all(style=True):
            style = element.get('style', '')
            found_colors = re.findall(r'#[0-9a-fA-F]{6}|#[0-9a-fA-F]{3}|rgb\([^)]+\)|rgba\([^)]+\)', style)
            colors.update(found_colors)
        
        # Extract from style tags
        for style_tag in soup.find_all('style'):
            css_content = style_tag.get_text()
            found_colors = re.findall(r'#[0-9a-fA-F]{6}|#[0-9a-fA-F]{3}|rgb\([^)]+\)|rgba\([^)]+\)', css_content)
            colors.update(found_colors)
        
        # Process and filter colors
        processed_colors = self.process_colors(list(colors))
        return processed_colors if processed_colors else None
    
    def analyze_screenshot_colors(self, url):
        """Analyze colors from screenshot"""
        driver = None
        try:
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--window-size=1200,800')
            
            driver = webdriver.Chrome(options=chrome_options)
            driver.get(url)
            time.sleep(3)
            
            screenshot = driver.get_screenshot_as_png()
            img = Image.open(io.BytesIO(screenshot))
            
            # Sample colors from image
            img_rgb = img.convert('RGB')
            pixels = []
            
            # Sample evenly across image
            width, height = img_rgb.size
            sample_points = 100
            
            for i in range(sample_points):
                x = int((i % 10) * width / 10)
                y = int((i // 10) * height / 10)
                if x < width and y < height:
                    pixels.append(img_rgb.getpixel((x, y)))
            
            # Cluster colors
            if len(pixels) > 10:
                kmeans = KMeans(n_clusters=min(6, len(set(map(tuple, pixels)))), random_state=42)
                kmeans.fit(pixels)
                
                colors = []
                for center in kmeans.cluster_centers_:
                    hex_color = '#{:02x}{:02x}{:02x}'.format(int(center[0]), int(center[1]), int(center[2]))
                    colors.append(hex_color)
                
                return colors
                
        except Exception as e:
            raise Exception(f"Screenshot color analysis failed: {e}")
        finally:
            if driver:
                driver.quit()
        
        return None
    
    def extract_svg_colors(self, html_content):
        """Extract colors from SVG elements"""
        soup = BeautifulSoup(html_content, 'html.parser')
        colors = set()
        
        # Find all SVG elements
        for svg in soup.find_all('svg'):
            svg_content = str(svg)
            found_colors = re.findall(r'fill="(#[0-9a-fA-F]{6}|#[0-9a-fA-F]{3})"', svg_content)
            colors.update(found_colors)
            found_colors = re.findall(r'stroke="(#[0-9a-fA-F]{6}|#[0-9a-fA-F]{3})"', svg_content)
            colors.update(found_colors)
        
        return list(colors) if colors else None
    
    def extract_logos_comprehensive(self, html_content, base_url):
        """Comprehensive logo extraction"""
        soup = BeautifulSoup(html_content, 'html.parser')
        logo_candidates = []
        
        # Extended selectors
        logo_selectors = [
            'img[alt*="logo" i]', 'img[src*="logo" i]', 'img[class*="logo" i]',
            'img[id*="logo" i]', '.logo img', '#logo img', '[class*="brand"] img',
            'header img', '.header img', 'a[href="/"] img', '.navbar-brand img',
            'picture source', 'picture img'
        ]
        
        for selector in logo_selectors:
            elements = soup.select(selector)
            for elem in elements:
                if elem.name == 'source':
                    srcset = elem.get('srcset', '')
                    if srcset:
                        # Parse srcset
                        urls = [url.strip().split(' ')[0] for url in srcset.split(',')]
                        logo_candidates.extend(urls)
                else:
                    src = elem.get('src') or elem.get('data-src') or elem.get('data-lazy-src')
                    if src:
                        logo_candidates.append(src)
        
        # Process and validate logos
        valid_logos = []
        for logo_url in logo_candidates:
            full_url = urljoin(base_url, logo_url)
            if self.is_likely_logo_url(full_url):
                valid_logos.append(full_url)
        
        return list(set(valid_logos))[:3] if valid_logos else None
    
    def is_likely_logo_url(self, url):
        """Validate if URL is likely a logo"""
        url_lower = url.lower()
        
        # Positive indicators
        logo_indicators = ['logo', 'brand', 'identity', 'mark']
        if any(indicator in url_lower for indicator in logo_indicators):
            return True
        
        # Negative indicators
        avoid_patterns = ['banner', 'hero', 'background', 'slide', 'feature', 'product', 'team', 'testimonial']
        if any(pattern in url_lower for pattern in avoid_patterns):
            return False
        
        # Check file extension
        image_extensions = ['.png', '.jpg', '.jpeg', '.svg', '.webp']
        if any(url_lower.endswith(ext) for ext in image_extensions):
            # Additional check for header/nav images
            if any(loc in url_lower for loc in ['header', 'nav', 'top']):
                return True
        
        return False
    
    def process_colors(self, color_list):
        """Process and cluster colors"""
        if not color_list:
            return None
        
        processed_colors = []
        
        for color in color_list:
            try:
                rgb = None
                
                if color.startswith('#'):
                    # Hex color
                    if len(color) == 4:  # #abc format
                        color = '#' + ''.join([c*2 for c in color[1:]])
                    rgb = tuple(int(color[i:i+2], 16) for i in (1, 3, 5))
                    
                elif color.startswith('rgb'):
                    # RGB/RGBA color
                    numbers = re.findall(r'\d+', color)
                    if len(numbers) >= 3:
                        rgb = tuple(int(n) for n in numbers[:3])
                
                if rgb and all(0 <= val <= 255 for val in rgb):
                    # Filter out very light/dark colors
                    if not (all(val > 240 for val in rgb) or all(val < 20 for val in rgb)):
                        # Filter out grays
                        if max(rgb) - min(rgb) > 20:
                            processed_colors.append(rgb)
                            
            except:
                continue
        
        if not processed_colors:
            return None
        
        # Cluster similar colors
        try:
            unique_colors = list(set(map(tuple, processed_colors)))
            if len(unique_colors) > 6:
                colors_array = np.array(unique_colors)
                kmeans = KMeans(n_clusters=6, random_state=42, n_init=10)
                kmeans.fit(colors_array)
                
                hex_colors = []
                for center in kmeans.cluster_centers_:
                    hex_color = '#{:02x}{:02x}{:02x}'.format(
                        int(center[0]), int(center[1]), int(center[2])
                    )
                    hex_colors.append(hex_color)
                
                return hex_colors
            else:
                # Convert to hex
                hex_colors = []
                for rgb in unique_colors:
                    hex_color = '#{:02x}{:02x}{:02x}'.format(rgb[0], rgb[1], rgb[2])
                    hex_colors.append(hex_color)
                
                return hex_colors
                
        except:
            return None

def analyze_brands_real_data_only(urls):
    """Analyze multiple brands with real data only"""
    profiler = EnhancedBrandProfilerV2()
    results = []
    
    for url in urls:
        try:
            print(f"\n{'='*60}")
            print(f"Analyzing: {url}")
            print(f"{'='*60}")
            
            profile = profiler.analyze_brand(url)
            results.append(profile)
            
            if profile['status'] == 'success':
                print(f"✅ Success: {profile['brand_data'].get('company_name', 'Unknown')}")
                print(f"   Quality Score: {profile['extraction_quality']:.2f}")
            else:
                print(f"❌ Failed: {profile['error']}")
                
        except Exception as e:
            print(f"❌ Error: {e}")
            results.append({
                "status": "failed",
                "url": url,
                "error": str(e),
                "extracted_data": None
            })
    
    # Summary
    successful = [r for r in results if r['status'] == 'success']
    failed = [r for r in results if r['status'] == 'failed']
    
    print(f"\n{'='*60}")
    print(f"ANALYSIS COMPLETE")
    print(f"{'='*60}")
    print(f"✅ Successful: {len(successful)}")
    print(f"❌ Failed: {len(failed)}")
    
    if successful:
        print(f"\nSuccessfully analyzed:")
        for r in successful:
            print(f"  • {r['brand_data']['company_name']} - Quality: {r['extraction_quality']:.2f}")
    
    if failed:
        print(f"\nFailed to analyze:")
        for r in failed:
            print(f"  • {r['url']} - {r['error']}")
    
    return results

if __name__ == "__main__":
    # Test with real URLs
    test_urls = [
        "https://www.apple.com",
        "https://www.microsoft.com",
        "https://www.google.com"
    ]
    
    results = analyze_brands_real_data_only(test_urls)
    
    # Save results
    timestamp = pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')
    with open(f'real_brand_analysis_{timestamp}.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nResults saved to: real_brand_analysis_{timestamp}.json")
