#!/usr/bin/env python3
"""
Deep Website Scraper for Comprehensive Competitive Intelligence
Scrapes multiple pages including About, Products, Pricing, Blog, Team, Case Studies
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import re
import time
from typing import Dict, List, Any, Optional
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os

class DeepWebsiteScraper:
    """Comprehensive multi-page website scraper"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        self.driver = None
        
    def setup_selenium_driver(self):
        """Setup Selenium driver for JavaScript-heavy pages"""
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument('--disable-web-security')
        chrome_options.add_argument('--allow-running-insecure-content')
        
        # Railway/Docker specific
        if os.environ.get('DISPLAY'):
            chrome_options.add_argument(f'--display={os.environ.get("DISPLAY")}')
        
        try:
            # Use webdriver-manager to automatically handle ChromeDriver
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        except Exception as e:
            print(f"Selenium setup failed: {e}")
            self.driver = None
    
    def discover_key_pages(self, base_url: str, progress_callback=None) -> Dict[str, List[str]]:
        """Discover key pages on the website"""
        if progress_callback:
            progress_callback("Discovering website structure...")
            
        discovered_pages = {
            'about': [],
            'products': [],
            'pricing': [], 
            'blog': [],
            'team': [],
            'case_studies': [],
            'contact': [],
            'careers': []
        }
        
        try:
            # Get homepage content
            response = self.session.get(base_url, timeout=15)
            soup = BeautifulSoup(response.text, 'html.parser')
            domain = urlparse(base_url).netloc
            
            # Find all navigation links
            nav_links = []
            
            # Common navigation selectors
            nav_selectors = [
                'nav a', 'header a', '.nav a', '.navigation a', 
                '.menu a', '.navbar a', '.header a', '.top-menu a',
                '[role="navigation"] a', '.main-nav a', '.primary-nav a'
            ]
            
            for selector in nav_selectors:
                links = soup.select(selector)
                nav_links.extend(links)
            
            # Also check footer links
            footer_links = soup.select('footer a, .footer a')
            nav_links.extend(footer_links)
            
            # Process all found links
            for link in nav_links:
                href = link.get('href', '')
                text = link.get_text(strip=True).lower()
                
                if not href:
                    continue
                    
                # Convert relative URLs to absolute
                full_url = urljoin(base_url, href)
                
                # Only include URLs from the same domain
                if urlparse(full_url).netloc != domain:
                    continue
                
                # Categorize links based on text and URL patterns
                self._categorize_link(full_url, text, discovered_pages)
            
            # Additional sitemap check
            self._check_sitemap(base_url, discovered_pages)
            
            # Remove duplicates and limit
            for category in discovered_pages:
                discovered_pages[category] = list(set(discovered_pages[category]))[:5]  # Max 5 per category
                
            if progress_callback:
                total_found = sum(len(pages) for pages in discovered_pages.values())
                progress_callback(f"Found {total_found} key pages to analyze")
                
        except Exception as e:
            print(f"❌ Page discovery error: {e}")
        
        return discovered_pages
    
    def _categorize_link(self, url: str, text: str, discovered_pages: Dict[str, List[str]]):
        """Categorize a link based on URL and text content"""
        url_lower = url.lower()
        text_lower = text.lower()
        
        # About page patterns
        about_patterns = ['about', 'our story', 'who we are', 'company', 'mission', 'vision', 'history']
        if any(pattern in url_lower or pattern in text_lower for pattern in about_patterns):
            discovered_pages['about'].append(url)
            return
        
        # Products page patterns
        product_patterns = ['product', 'solution', 'service', 'offering', 'platform', 'software', 'tool']
        if any(pattern in url_lower or pattern in text_lower for pattern in product_patterns):
            discovered_pages['products'].append(url)
            return
        
        # Pricing page patterns
        pricing_patterns = ['pricing', 'price', 'cost', 'plan', 'subscription', 'billing']
        if any(pattern in url_lower or pattern in text_lower for pattern in pricing_patterns):
            discovered_pages['pricing'].append(url)
            return
        
        # Blog page patterns
        blog_patterns = ['blog', 'news', 'article', 'insight', 'post', 'update', 'resource']
        if any(pattern in url_lower or pattern in text_lower for pattern in blog_patterns):
            discovered_pages['blog'].append(url)
            return
        
        # Team page patterns
        team_patterns = ['team', 'people', 'staff', 'leadership', 'management', 'founder', 'executive']
        if any(pattern in url_lower or pattern in text_lower for pattern in team_patterns):
            discovered_pages['team'].append(url)
            return
        
        # Case studies patterns
        case_patterns = ['case', 'success', 'customer', 'client', 'testimonial', 'portfolio', 'example']
        if any(pattern in url_lower or pattern in text_lower for pattern in case_patterns):
            discovered_pages['case_studies'].append(url)
            return
        
        # Contact patterns
        contact_patterns = ['contact', 'reach', 'support', 'help']
        if any(pattern in url_lower or pattern in text_lower for pattern in contact_patterns):
            discovered_pages['contact'].append(url)
            return
        
        # Careers patterns
        career_patterns = ['career', 'job', 'hire', 'join', 'work', 'opportunity']
        if any(pattern in url_lower or pattern in text_lower for pattern in career_patterns):
            discovered_pages['careers'].append(url)
            return
    
    def _check_sitemap(self, base_url: str, discovered_pages: Dict[str, List[str]]):
        """Check sitemap.xml for additional pages"""
        try:
            sitemap_urls = [
                urljoin(base_url, '/sitemap.xml'),
                urljoin(base_url, '/sitemap_index.xml'),
                urljoin(base_url, '/robots.txt')
            ]
            
            for sitemap_url in sitemap_urls:
                try:
                    response = self.session.get(sitemap_url, timeout=10)
                    if response.status_code == 200:
                        # Parse sitemap or robots.txt for URLs
                        if 'sitemap' in sitemap_url:
                            soup = BeautifulSoup(response.text, 'xml')
                            urls = [loc.text for loc in soup.find_all('loc')]
                            for url in urls[:20]:  # Limit to first 20 URLs
                                url_text = urlparse(url).path.lower()
                                self._categorize_link(url, url_text, discovered_pages)
                        break
                except:
                    continue
        except Exception as e:
            print(f"Sitemap check error: {e}")
    
    def scrape_page_content(self, url: str, page_type: str, progress_callback=None) -> Dict[str, Any]:
        """Scrape comprehensive content from a single page"""
        if progress_callback:
            progress_callback(f"Analyzing {page_type} page: {urlparse(url).path}")
        
        content = {
            'url': url,
            'page_type': page_type,
            'title': '',
            'headings': [],
            'paragraphs': [],
            'key_info': [],
            'images': [],
            'links': [],
            'meta_description': '',
            'success': False
        }
        
        try:
            # Try requests first (faster)
            response = self.session.get(url, timeout=15)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                content.update(self._extract_content_from_soup(soup, page_type))
                content['success'] = True
            
            # If minimal content or failed, try Selenium
            if not content['success'] or len(content['paragraphs']) < 3:
                content.update(self._scrape_with_selenium(url, page_type))
                
        except Exception as e:
            print(f"❌ Error scraping {url}: {e}")
            # Try with Selenium as fallback
            try:
                content.update(self._scrape_with_selenium(url, page_type))
            except Exception as e2:
                print(f"❌ Selenium fallback failed for {url}: {e2}")
        
        return content
    
    def _extract_content_from_soup(self, soup: BeautifulSoup, page_type: str) -> Dict[str, Any]:
        """Extract content using BeautifulSoup"""
        content = {}
        
        # Title
        title_tag = soup.find('title')
        content['title'] = title_tag.text.strip() if title_tag else ''
        
        # Meta description
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        content['meta_description'] = meta_desc.get('content', '') if meta_desc else ''
        
        # Headings (prioritize H1-H3)
        headings = []
        for h_tag in soup.find_all(['h1', 'h2', 'h3'], limit=20):
            text = h_tag.get_text(strip=True)
            if text and len(text) > 3:
                headings.append({
                    'level': h_tag.name,
                    'text': text
                })
        content['headings'] = headings
        
        # Paragraphs and content blocks
        paragraphs = []
        
        # Remove script, style, and nav elements
        for element in soup(['script', 'style', 'nav', 'header', 'footer']):
            element.decompose()
        
        # Get meaningful text content
        for p in soup.find_all(['p', 'div', 'section'], limit=50):
            text = p.get_text(strip=True)
            if text and len(text) > 30 and len(text) < 1000:  # Filter meaningful content
                paragraphs.append(text)
        
        content['paragraphs'] = paragraphs[:20]  # Limit to top 20
        
        # Extract key information based on page type
        content['key_info'] = self._extract_page_specific_info(soup, page_type)
        
        # Images
        images = []
        for img in soup.find_all('img', limit=10):
            src = img.get('src', '')
            alt = img.get('alt', '')
            if src:
                images.append({
                    'src': src,
                    'alt': alt
                })
        content['images'] = images
        
        # Important links
        links = []
        for link in soup.find_all('a', href=True, limit=20):
            href = link.get('href', '')
            text = link.get_text(strip=True)
            if href and text and len(text) < 100:
                links.append({
                    'url': href,
                    'text': text
                })
        content['links'] = links
        
        return content
    
    def _extract_page_specific_info(self, soup: BeautifulSoup, page_type: str) -> List[str]:
        """Extract information specific to page type"""
        key_info = []
        
        if page_type == 'pricing':
            # Look for price indicators
            price_patterns = [r'\$[\d,]+', r'€[\d,]+', r'£[\d,]+', r'[\d,]+\s*per\s*month', r'free', r'trial']
            text = soup.get_text()
            for pattern in price_patterns:
                matches = re.finditer(pattern, text, re.IGNORECASE)
                for match in matches:
                    key_info.append(f"Pricing: {match.group()}")
        
        elif page_type == 'team':
            # Look for employee names and titles
            for element in soup.find_all(['h3', 'h4', 'strong', '.name', '.title']):
                text = element.get_text(strip=True)
                if text and len(text) < 50:
                    key_info.append(f"Team member: {text}")
        
        elif page_type == 'products':
            # Look for product features and benefits
            feature_indicators = soup.find_all(['li', '.feature', '.benefit'])
            for feature in feature_indicators:
                text = feature.get_text(strip=True)
                if text and 10 < len(text) < 200:
                    key_info.append(f"Feature: {text}")
        
        return key_info[:15]  # Limit key info
    
    def _scrape_with_selenium(self, url: str, page_type: str) -> Dict[str, Any]:
        """Scrape page using Selenium for JavaScript content"""
        if not self.driver:
            self.setup_selenium_driver()
        
        if not self.driver:
            return {'success': False}
        
        try:
            self.driver.get(url)
            time.sleep(3)  # Wait for page load
            
            # Wait for content to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Get page source and parse
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            content = self._extract_content_from_soup(soup, page_type)
            content['success'] = True
            
            return content
            
        except Exception as e:
            print(f"Selenium scraping error for {url}: {e}")
            return {'success': False}
    
    def take_multiple_screenshots(self, urls: List[str], progress_callback=None) -> Dict[str, str]:
        """Take screenshots of multiple pages"""
        if not self.driver:
            self.setup_selenium_driver()
        
        if not self.driver:
            return {}
        
        screenshots = {}
        
        for i, url in enumerate(urls[:5]):  # Limit to 5 screenshots per brand
            try:
                if progress_callback:
                    progress_callback(f"Taking screenshot {i+1}/5: {urlparse(url).path}")
                
                self.driver.get(url)
                time.sleep(3)
                
                # Handle privacy dialogs
                self._handle_privacy_dialogs()
                time.sleep(2)
                
                # Take screenshot
                screenshot_data = self.driver.get_screenshot_as_base64()
                page_name = urlparse(url).path.split('/')[-1] or 'homepage'
                screenshots[page_name] = screenshot_data
                
            except Exception as e:
                print(f"Screenshot error for {url}: {e}")
        
        return screenshots
    
    def _handle_privacy_dialogs(self):
        """Handle common privacy and cookie dialogs"""
        try:
            # Common privacy dialog selectors
            privacy_selectors = [
                '[id*="cookie"] button', '[class*="cookie"] button',
                '[id*="privacy"] button', '[class*="privacy"] button',
                'button[id*="accept"]', 'button[class*="accept"]',
                'button[id*="consent"]', 'button[class*="consent"]',
                '.cookie-banner button', '.privacy-banner button',
                '[aria-label*="accept" i]', '[aria-label*="agree" i]'
            ]
            
            for selector in privacy_selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for element in elements:
                        if element.is_displayed() and element.is_enabled():
                            element.click()
                            time.sleep(1)
                            break
                except:
                    continue
                    
        except Exception as e:
            print(f"Privacy dialog handling error: {e}")
    
    def cleanup(self):
        """Clean up resources"""
        if self.driver:
            self.driver.quit()
            self.driver = None
        
        self.session.close()

# Integration methods for the main system
def enhance_brand_analysis_with_deep_scraping(brand_profile: Dict[str, Any], progress_callback=None) -> Dict[str, Any]:
    """Enhance brand analysis with deep multi-page scraping"""
    scraper = DeepWebsiteScraper()
    
    try:
        # Discover key pages
        discovered_pages = scraper.discover_key_pages(brand_profile['url'], progress_callback)
        
        # Scrape content from each page type
        deep_content = {}
        total_pages = sum(len(pages) for pages in discovered_pages.values())
        scraped_count = 0
        
        for page_type, urls in discovered_pages.items():
            deep_content[page_type] = []
            
            for url in urls[:3]:  # Max 3 pages per type
                scraped_count += 1
                if progress_callback:
                    progress_callback(f"Deep analysis: {scraped_count}/{total_pages} pages")
                
                page_content = scraper.scrape_page_content(url, page_type, progress_callback)
                if page_content['success']:
                    deep_content[page_type].append(page_content)
                
                time.sleep(1)  # Be respectful
        
        # Take multiple screenshots
        all_urls = []
        for urls in discovered_pages.values():
            all_urls.extend(urls[:2])  # 2 per category max
        
        if all_urls:
            screenshots = scraper.take_multiple_screenshots(all_urls[:5], progress_callback)
            brand_profile['multiple_screenshots'] = screenshots
        
        # Add deep content to brand profile
        brand_profile['deep_content'] = deep_content
        brand_profile['discovered_pages'] = {k: len(v) for k, v in discovered_pages.items()}
        
        if progress_callback:
            progress_callback(f"Deep analysis complete: {scraped_count} pages analyzed")
        
    except Exception as e:
        print(f"Deep scraping error: {e}")
    finally:
        scraper.cleanup()
    
    return brand_profile