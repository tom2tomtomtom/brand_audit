"""
Web Scraper Module
Handles comprehensive website scraping using Selenium and BeautifulSoup
"""

import time
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin, urlparse
import re
from PIL import Image
import io
import base64

logger = logging.getLogger(__name__)

class WebScraper:
    def __init__(self):
        self.driver = None
        self.setup_driver()
    
    def setup_driver(self):
        """Initialize Chrome WebDriver with appropriate options"""
        try:
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--window-size=1920,1080')
            chrome_options.add_argument('--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
            
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.driver.set_page_load_timeout(30)
            
            logger.info("Chrome WebDriver initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize WebDriver: {str(e)}")
            raise
    
    def scrape_brand(self, url, brand_name):
        """Scrape comprehensive data from a brand's website"""
        logger.info(f"Starting comprehensive scrape for {brand_name} at {url}")
        
        brand_data = {
            'name': brand_name,
            'url': url,
            'scraped_at': time.strftime('%Y-%m-%d %H:%M:%S'),
            'pages_scraped': [],
            'visual_assets': {},
            'content_analysis': {},
            'technical_info': {},
            'recent_content': []
        }
        
        try:
            # Scrape main homepage
            homepage_data = self.scrape_page(url, "Homepage")
            brand_data['pages_scraped'].append(homepage_data)
            
            # Extract key pages to scrape
            key_pages = self.find_key_pages(url, homepage_data['links'])
            
            # Scrape additional key pages
            for page_url, page_type in key_pages:
                try:
                    logger.info(f"Scraping {page_type} page: {page_url}")
                    page_data = self.scrape_page(page_url, page_type)
                    brand_data['pages_scraped'].append(page_data)
                    time.sleep(3)  # Respectful delay between requests
                except Exception as e:
                    logger.warning(f"Failed to scrape {page_type} page: {str(e)}")
            
            # Validate that we actually scraped meaningful content
            if not brand_data['pages_scraped'] or all(not page.get('content') or len(page.get('content', '').strip()) < 50 for page in brand_data['pages_scraped']):
                raise Exception(f"Failed to extract meaningful content from {url} - insufficient data")
            
            # Extract visual assets
            brand_data['visual_assets'] = self.extract_visual_assets(url)
            
            # Analyze content across all pages
            brand_data['content_analysis'] = self.analyze_content(brand_data['pages_scraped'])
            
            # Extract recent content/news
            brand_data['recent_content'] = self.extract_recent_content(brand_data['pages_scraped'])
            
            # Technical analysis
            brand_data['technical_info'] = self.analyze_technical_aspects(url)
            
            logger.info(f"Completed comprehensive scrape for {brand_name}")
            return brand_data
            
        except Exception as e:
            logger.error(f"Error scraping {brand_name}: {str(e)}")
            raise Exception(f"Failed to scrape {brand_name}: {str(e)}")
    
    def scrape_page(self, url, page_type):
        """Scrape detailed data from a single page"""
        try:
            logger.info(f"Scraping {page_type}: {url}")
            
            # Navigate to page
            self.driver.get(url)
            
            # Wait for page to load
            time.sleep(5)
            
            # Get page source and create BeautifulSoup object
            page_source = self.driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            
            # Extract comprehensive page data
            page_data = {
                'url': url,
                'type': page_type,
                'title': self.driver.title,
                'meta_description': self.extract_meta_description(soup),
                'headings': self.extract_headings(soup),
                'content': self.extract_main_content(soup),
                'links': self.extract_links(soup, url),
                'images': self.extract_images(soup, url),
                'forms': self.extract_forms(soup),
                'load_time': 0,  # Could implement performance monitoring
                'word_count': 0
            }
            
            # Calculate word count
            page_data['word_count'] = len(page_data['content'].split())
            
            return page_data
            
        except Exception as e:
            logger.error(f"Error scraping page {url}: {str(e)}")
            return {
                'url': url,
                'type': page_type,
                'error': str(e),
                'title': '',
                'content': '',
                'links': [],
                'images': []
            }
    
    def find_key_pages(self, base_url, homepage_links):
        """Identify key pages to scrape based on homepage links"""
        key_pages = []
        
        # Define important page types to look for
        page_patterns = {
            'about': ['about', 'company', 'who-we-are', 'our-story'],
            'products': ['products', 'services', 'solutions'],
            'news': ['news', 'blog', 'press', 'updates', 'media'],
            'contact': ['contact', 'reach-us', 'get-in-touch'],
            'careers': ['careers', 'jobs', 'work-with-us', 'join-us']
        }
        
        for link in homepage_links[:30]:  # Check first 30 links
            if not link.startswith(('http', 'https')):
                link = urljoin(base_url, link)
            
            # Check if it's from the same domain
            if urlparse(link).netloc != urlparse(base_url).netloc:
                continue
            
            link_lower = link.lower()
            
            for page_type, patterns in page_patterns.items():
                for pattern in patterns:
                    if pattern in link_lower and len(key_pages) < 8:  # Limit to 8 additional pages
                        key_pages.append((link, page_type))
                        break
                if len(key_pages) >= 8:
                    break
        
        return key_pages
    
    def extract_visual_assets(self, url):
        """Extract visual brand assets"""
        try:
            visual_assets = {
                'logo': None,
                'favicon': None,
                'brand_colors': [],
                'font_families': [],
                'images': []
            }
            
            # Extract logo
            logo_selectors = [
                'img[alt*="logo" i]',
                'img[src*="logo" i]',
                '.logo img',
                '.brand img',
                'header img:first-of-type'
            ]
            
            for selector in logo_selectors:
                try:
                    logo_element = self.driver.find_element(By.CSS_SELECTOR, selector)
                    logo_src = logo_element.get_attribute('src')
                    if logo_src:
                        visual_assets['logo'] = urljoin(url, logo_src)
                        break
                except:
                    continue
            
            # Extract brand colors using JavaScript
            try:
                colors = self.driver.execute_script("""
                    const colors = new Set();
                    const elements = document.querySelectorAll('header, nav, .brand, .logo, [class*="primary"], [class*="brand"]');
                    
                    elements.forEach(el => {
                        const styles = window.getComputedStyle(el);
                        const bgColor = styles.backgroundColor;
                        const textColor = styles.color;
                        const borderColor = styles.borderColor;
                        
                        [bgColor, textColor, borderColor].forEach(color => {
                            if (color && color !== 'rgba(0, 0, 0, 0)' && color !== 'transparent') {
                                colors.add(color);
                            }
                        });
                    });
                    
                    return Array.from(colors);
                """)
                
                visual_assets['brand_colors'] = colors[:8]  # Top 8 colors
            except:
                pass
            
            # Extract font families
            try:
                fonts = self.driver.execute_script("""
                    const fonts = new Set();
                    const elements = document.querySelectorAll('h1, h2, h3, .title, body');
                    
                    elements.forEach(el => {
                        const fontFamily = window.getComputedStyle(el).fontFamily;
                        if (fontFamily) {
                            fontFamily.split(',').forEach(font => {
                                const cleanFont = font.trim().replace(/['"]/g, '');
                                if (cleanFont && !cleanFont.includes('serif') && !cleanFont.includes('sans-serif')) {
                                    fonts.add(cleanFont);
                                }
                            });
                        }
                    });
                    
                    return Array.from(fonts);
                """)
                
                visual_assets['font_families'] = fonts[:5]  # Top 5 fonts
            except:
                pass
            
            return visual_assets
            
        except Exception as e:
            logger.error(f"Error extracting visual assets: {str(e)}")
            return {}
    
    def extract_meta_description(self, soup):
        """Extract meta description"""
        try:
            meta_desc = soup.find('meta', attrs={'name': 'description'})
            return meta_desc.get('content', '') if meta_desc else ''
        except:
            return ''
    
    def extract_headings(self, soup):
        """Extract all headings"""
        try:
            headings = []
            for tag in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
                text = tag.get_text(strip=True)
                if text and len(text) > 3:
                    headings.append({
                        'level': tag.name,
                        'text': text
                    })
            return headings[:20]  # Top 20 headings
        except:
            return []
    
    def extract_main_content(self, soup):
        """Extract main page content"""
        try:
            # Remove script and style elements
            for element in soup(['script', 'style', 'nav', 'header', 'footer']):
                element.decompose()
            
            # Get text content
            text = soup.get_text()
            
            # Clean up whitespace
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            
            return text[:5000]  # First 5000 characters
        except:
            return ''
    
    def extract_links(self, soup, base_url):
        """Extract all links"""
        try:
            links = []
            for link in soup.find_all('a', href=True):
                href = link['href']
                full_url = urljoin(base_url, href)
                if full_url not in links:
                    links.append(full_url)
            return links[:50]  # First 50 links
        except:
            return []
    
    def extract_images(self, soup, base_url):
        """Extract all images"""
        try:
            images = []
            for img in soup.find_all('img', src=True):
                src = img['src']
                full_url = urljoin(base_url, src)
                alt_text = img.get('alt', '')
                images.append({
                    'src': full_url,
                    'alt': alt_text
                })
            return images[:20]  # First 20 images
        except:
            return []
    
    def extract_forms(self, soup):
        """Extract form information"""
        try:
            forms = []
            for form in soup.find_all('form'):
                form_data = {
                    'action': form.get('action', ''),
                    'method': form.get('method', 'GET'),
                    'fields': []
                }
                
                for input_field in form.find_all(['input', 'textarea', 'select']):
                    field_type = input_field.get('type', 'text')
                    field_name = input_field.get('name', '')
                    if field_name:
                        form_data['fields'].append({
                            'name': field_name,
                            'type': field_type
                        })
                
                forms.append(form_data)
            
            return forms
        except:
            return []
    
    def analyze_content(self, pages_data):
        """Analyze content across all scraped pages"""
        try:
            all_content = ""
            total_words = 0
            
            for page in pages_data:
                if 'content' in page:
                    all_content += " " + page['content']
                    total_words += page.get('word_count', 0)
            
            # Basic content analysis
            content_analysis = {
                'total_words': total_words,
                'total_pages': len(pages_data),
                'average_words_per_page': total_words / len(pages_data) if pages_data else 0,
                'key_topics': self.extract_key_topics(all_content),
                'industry_keywords': self.extract_industry_keywords(all_content)
            }
            
            return content_analysis
        except:
            return {}
    
    def extract_key_topics(self, content):
        """Extract key topics from content"""
        try:
            # Simple keyword frequency analysis
            words = re.findall(r'\b\w{4,}\b', content.lower())
            word_freq = {}
            
            for word in words:
                if word not in ['this', 'that', 'with', 'have', 'will', 'from', 'they', 'been', 'more', 'were']:
                    word_freq[word] = word_freq.get(word, 0) + 1
            
            # Return top 10 most frequent words
            return sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:10]
        except:
            return []
    
    def extract_industry_keywords(self, content):
        """Extract industry-specific keywords"""
        try:
            industry_terms = {
                'healthcare': ['health', 'medical', 'patient', 'clinical', 'care', 'treatment', 'therapy'],
                'technology': ['software', 'platform', 'digital', 'cloud', 'data', 'ai', 'innovation'],
                'finance': ['financial', 'investment', 'banking', 'capital', 'fund', 'wealth'],
                'education': ['education', 'learning', 'student', 'academic', 'university', 'course']
            }
            
            content_lower = content.lower()
            found_keywords = {}
            
            for industry, keywords in industry_terms.items():
                count = sum(content_lower.count(keyword) for keyword in keywords)
                if count > 0:
                    found_keywords[industry] = count
            
            return found_keywords
        except:
            return {}
    
    def extract_recent_content(self, pages_data):
        """Extract recent content like news, blog posts, press releases"""
        try:
            recent_content = []
            
            for page in pages_data:
                if page.get('type') in ['news', 'blog']:
                    # Look for date patterns in content
                    content = page.get('content', '')
                    headings = page.get('headings', [])
                    
                    # Extract potential news items from headings
                    for heading in headings:
                        if len(heading['text']) > 20:  # Substantial headings
                            recent_content.append({
                                'title': heading['text'],
                                'type': page['type'],
                                'url': page['url'],
                                'date': 'Recent'  # Could implement date extraction
                            })
            
            return recent_content[:10]  # Top 10 recent items
        except:
            return []
    
    def analyze_technical_aspects(self, url):
        """Analyze technical aspects of the website"""
        try:
            technical_info = {
                'domain': urlparse(url).netloc,
                'ssl_enabled': url.startswith('https'),
                'mobile_responsive': self.check_mobile_responsiveness(),
                'page_speed': self.estimate_page_speed(),
                'technology_stack': self.detect_technologies()
            }
            
            return technical_info
        except:
            return {}
    
    def check_mobile_responsiveness(self):
        """Check if site is mobile responsive"""
        try:
            # Check viewport meta tag
            viewport = self.driver.find_element(By.CSS_SELECTOR, 'meta[name="viewport"]')
            return viewport is not None
        except:
            return False
    
    def estimate_page_speed(self):
        """Estimate page loading speed"""
        try:
            # Basic timing information
            timing = self.driver.execute_script("""
                return {
                    loadTime: performance.timing.loadEventEnd - performance.timing.navigationStart,
                    domContentLoaded: performance.timing.domContentLoadedEventEnd - performance.timing.navigationStart
                };
            """)
            return timing
        except:
            return {}
    
    def detect_technologies(self):
        """Detect technologies used on the website"""
        try:
            technologies = []
            
            # Check for common frameworks/libraries in page source
            page_source = self.driver.page_source.lower()
            
            tech_indicators = {
                'React': ['react', '_react'],
                'Vue.js': ['vue.js', '__vue__'],
                'Angular': ['angular', 'ng-'],
                'jQuery': ['jquery', '$'],
                'Bootstrap': ['bootstrap'],
                'WordPress': ['wp-content', 'wordpress'],
                'Shopify': ['shopify'],
                'Squarespace': ['squarespace']
            }
            
            for tech, indicators in tech_indicators.items():
                if any(indicator in page_source for indicator in indicators):
                    technologies.append(tech)
            
            return technologies
        except:
            return []
    
    
    def __del__(self):
        """Clean up WebDriver"""
        if self.driver:
            try:
                self.driver.quit()
            except:
                pass