#!/usr/bin/env python3
"""
Medium-difficulty improvements (4-8 hours each)
"""

import asyncio
import aiohttp
from concurrent.futures import ThreadPoolExecutor
import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Any
import re

class MediumImprovements:
    """Medium-effort enhancements"""
    
    # 1. CONCURRENT SCRAPING (4 hours)
    async def analyze_competitors_parallel(self, urls: List[str], analyzer_func) -> List[Dict]:
        """Analyze multiple competitors in parallel"""
        async def analyze_with_semaphore(url, semaphore):
            async with semaphore:
                loop = asyncio.get_event_loop()
                # Run CPU-bound analysis in thread pool
                with ThreadPoolExecutor(max_workers=1) as executor:
                    return await loop.run_in_executor(executor, analyzer_func, url)
        
        # Limit concurrent analyses to avoid overwhelming system
        semaphore = asyncio.Semaphore(3)
        tasks = [analyze_with_semaphore(url, semaphore) for url in urls]
        return await asyncio.gather(*tasks)
    
    # 2. SOCIAL MEDIA METRICS (3 hours)
    def get_social_metrics(self, company_name: str, website_url: str) -> Dict[str, Any]:
        """Extract social media presence indicators"""
        metrics = {
            'twitter_url': None,
            'linkedin_url': None,
            'youtube_url': None,
            'facebook_url': None,
            'instagram_url': None,
            'social_signals': {}
        }
        
        try:
            # Extract social links from website
            response = requests.get(website_url, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Common social media patterns
            social_patterns = {
                'twitter': r'twitter\.com/(\w+)',
                'linkedin': r'linkedin\.com/company/([\w-]+)',
                'youtube': r'youtube\.com/(channel|c|user)/([\w-]+)',
                'facebook': r'facebook\.com/([\w.-]+)',
                'instagram': r'instagram\.com/([\w.-]+)'
            }
            
            # Find all links
            for link in soup.find_all(['a', 'link']):
                href = link.get('href', '')
                for platform, pattern in social_patterns.items():
                    if platform in href:
                        match = re.search(pattern, href)
                        if match:
                            metrics[f'{platform}_url'] = href
                            metrics['social_signals'][platform] = True
            
            # Check meta tags for social profiles
            for meta in soup.find_all('meta'):
                property_val = meta.get('property', '')
                if 'twitter:site' in property_val:
                    metrics['twitter_handle'] = meta.get('content', '').replace('@', '')
                elif 'article:publisher' in property_val:
                    metrics['facebook_publisher'] = meta.get('content', '')
            
        except Exception as e:
            print(f"Social media extraction error: {e}")
        
        return metrics
    
    # 3. TECHNOLOGY STACK DETECTION (3 hours)
    def detect_technology_stack(self, url: str) -> Dict[str, List[str]]:
        """Detect technologies used by the website"""
        tech_stack = {
            'frontend': [],
            'analytics': [],
            'marketing': [],
            'cms': [],
            'ecommerce': [],
            'frameworks': []
        }
        
        try:
            response = requests.get(url, timeout=10)
            html = response.text
            headers = response.headers
            
            # Framework detection patterns
            tech_patterns = {
                # Frontend
                'React': [r'react(?:\.production\.min)?\.js', r'_react'],
                'Vue.js': [r'vue(?:\.min)?\.js', r'Vue\.version'],
                'Angular': [r'angular(?:\.min)?\.js', r'ng-version'],
                'jQuery': [r'jquery(?:-[\d.]+)?(?:\.min)?\.js'],
                
                # Analytics
                'Google Analytics': [r'google-analytics\.com/analytics\.js', r'gtag\('],
                'Google Tag Manager': [r'googletagmanager\.com/gtm\.js'],
                'Hotjar': [r'static\.hotjar\.com'],
                'Segment': [r'segment\.com/analytics\.js'],
                
                # CMS
                'WordPress': [r'/wp-content/', r'wp-json'],
                'Shopify': [r'cdn\.shopify\.com', r'shopify\.com/s/files'],
                'Webflow': [r'webflow\.com', r'\.webflow\.io'],
                'Squarespace': [r'static\d*\.squarespace\.com'],
                
                # Marketing
                'HubSpot': [r'js\.hs-scripts\.com', r'hubspot\.com'],
                'Mailchimp': [r'chimpstatic\.com', r'list-manage\.com'],
                'Intercom': [r'intercomcdn\.com', r'intercom\.io'],
                
                # Ecommerce
                'Stripe': [r'js\.stripe\.com'],
                'PayPal': [r'paypal\.com/sdk'],
                'Square': [r'square(?:cdn)?\.com']
            }
            
            # Check HTML content
            for tech, patterns in tech_patterns.items():
                for pattern in patterns:
                    if re.search(pattern, html, re.IGNORECASE):
                        category = self._categorize_tech(tech)
                        if tech not in tech_stack[category]:
                            tech_stack[category].append(tech)
                        break
            
            # Check headers
            if 'X-Powered-By' in headers:
                powered_by = headers['X-Powered-By']
                tech_stack['frameworks'].append(f"Powered by: {powered_by}")
            
            # Server detection
            if 'Server' in headers:
                server = headers['Server']
                tech_stack['frameworks'].append(f"Server: {server}")
                
        except Exception as e:
            print(f"Tech stack detection error: {e}")
        
        return tech_stack
    
    def _categorize_tech(self, tech: str) -> str:
        """Categorize technology"""
        categories = {
            'frontend': ['React', 'Vue.js', 'Angular', 'jQuery'],
            'analytics': ['Google Analytics', 'Google Tag Manager', 'Hotjar', 'Segment'],
            'cms': ['WordPress', 'Shopify', 'Webflow', 'Squarespace'],
            'marketing': ['HubSpot', 'Mailchimp', 'Intercom'],
            'ecommerce': ['Stripe', 'PayPal', 'Square']
        }
        
        for category, techs in categories.items():
            if tech in techs:
                return category
        return 'frameworks'
    
    # 4. BASIC SEO ANALYSIS (2 hours)
    def analyze_seo_signals(self, url: str) -> Dict[str, Any]:
        """Extract basic SEO signals"""
        seo_data = {
            'title': None,
            'meta_description': None,
            'h1_count': 0,
            'h2_count': 0,
            'internal_links': 0,
            'external_links': 0,
            'images_without_alt': 0,
            'schema_markup': False,
            'robots_meta': None,
            'canonical_url': None
        }
        
        try:
            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Title
            title_tag = soup.find('title')
            if title_tag:
                seo_data['title'] = title_tag.text.strip()
                seo_data['title_length'] = len(seo_data['title'])
            
            # Meta description
            meta_desc = soup.find('meta', attrs={'name': 'description'})
            if meta_desc:
                seo_data['meta_description'] = meta_desc.get('content', '')
                seo_data['description_length'] = len(seo_data['meta_description'])
            
            # Headings
            seo_data['h1_count'] = len(soup.find_all('h1'))
            seo_data['h2_count'] = len(soup.find_all('h2'))
            
            # Links
            for link in soup.find_all('a', href=True):
                href = link['href']
                if href.startswith('http') and url not in href:
                    seo_data['external_links'] += 1
                elif not href.startswith('#'):
                    seo_data['internal_links'] += 1
            
            # Images without alt
            images = soup.find_all('img')
            seo_data['total_images'] = len(images)
            seo_data['images_without_alt'] = len([img for img in images if not img.get('alt')])
            
            # Schema markup
            schema_scripts = soup.find_all('script', type='application/ld+json')
            seo_data['schema_markup'] = len(schema_scripts) > 0
            
            # Robots meta
            robots_meta = soup.find('meta', attrs={'name': 'robots'})
            if robots_meta:
                seo_data['robots_meta'] = robots_meta.get('content', '')
            
            # Canonical URL
            canonical = soup.find('link', attrs={'rel': 'canonical'})
            if canonical:
                seo_data['canonical_url'] = canonical.get('href', '')
                
        except Exception as e:
            print(f"SEO analysis error: {e}")
        
        return seo_data

# Integration example:
"""
# Add to strategic_competitive_intelligence.py:

async def enhance_with_medium_features(self, brand_profiles):
    improvements = MediumImprovements()
    
    # Run parallel analysis
    if len(brand_profiles) > 1:
        brand_profiles = await improvements.analyze_competitors_parallel(
            [p['url'] for p in brand_profiles],
            self.analyze_brand
        )
    
    # Enhance each profile
    for profile in brand_profiles:
        # Add social metrics
        profile['social_presence'] = improvements.get_social_metrics(
            profile['company_name'], 
            profile['url']
        )
        
        # Add tech stack
        profile['technology_stack'] = improvements.detect_technology_stack(
            profile['url']
        )
        
        # Add SEO signals
        profile['seo_analysis'] = improvements.analyze_seo_signals(
            profile['url']
        )
    
    return brand_profiles
"""