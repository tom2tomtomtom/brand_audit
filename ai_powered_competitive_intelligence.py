#!/usr/bin/env python3
"""
AI-Powered Competitive Intelligence Generator
Advanced 16:9 slide-based competitive analysis with sophisticated AI insights
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

class AIPoweredCompetitiveIntelligence:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.driver = None
        self.brand_profiles = []
        self.competitive_insights = {}
    
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
        """Extract comprehensive brand data with AI-powered analysis"""
        print(f"🔍 AI-POWERED ANALYSIS: {url}")
        
        html_content = self.fetch_page(url)
        if not html_content:
            return None
        
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Extract comprehensive content
        content_sections = self._extract_all_content_sections(soup)
        
        # AI-powered strategic analysis
        print("   🧠 AI Strategic Positioning Analysis...")
        positioning_analysis = self._ai_competitive_positioning_analysis(html_content, url, content_sections)
        
        print("   📊 AI SWOT Analysis Generation...")
        swot_analysis = self._ai_swot_analysis(html_content, url, content_sections)
        
        print("   🎯 AI Target Audience Intelligence...")
        audience_analysis = self._ai_target_audience_analysis(html_content, url, content_sections)
        
        print("   💡 AI Innovation Opportunity Detection...")
        innovation_analysis = self._ai_innovation_opportunities(html_content, url, content_sections)
        
        print("   ⚡ AI Brand Health Scoring...")
        brand_health = self._ai_brand_health_scoring(html_content, url, content_sections)
        
        # Visual and data extraction
        logos = self._extract_logos_comprehensive(html_content, url)
        colors = self._extract_colors_comprehensive(html_content, url)
        screenshot = self._capture_screenshot_proper(url)
        
        # Compile enhanced profile
        brand_profile = {
            "url": url,
            "company_name": positioning_analysis.get("company_name", "Unknown Company"),
            "ai_positioning_analysis": positioning_analysis,
            "ai_swot_analysis": swot_analysis,
            "ai_audience_analysis": audience_analysis,
            "ai_innovation_analysis": innovation_analysis,
            "ai_brand_health": brand_health,
            "logos": logos,
            "color_palette": colors,
            "screenshot": screenshot,
            "content_sections": content_sections,
            "analysis_timestamp": datetime.now().isoformat()
        }
        
        print(f"   ✅ AI ANALYSIS COMPLETE: {brand_profile['company_name']}")
        print(f"      Health Score: {brand_health.get('overall_score', 'N/A')}/100")
        print(f"      Threat Level: {brand_health.get('competitive_threat_level', 'N/A')}")
        
        return brand_profile
    
    def _extract_all_content_sections(self, soup):
        """Extract comprehensive content sections"""
        sections = {}
        
        # Extract text content from different sections
        sections['hero'] = [elem.get_text().strip() for elem in soup.select('h1, .hero, [class*="hero"]')[:5] if elem.get_text().strip()]
        sections['navigation'] = [elem.get_text().strip() for elem in soup.select('nav a, .nav a, header a')[:15] if elem.get_text().strip()]
        sections['products'] = [elem.get_text().strip()[:300] for elem in soup.select('.product, [class*="product"], .service, [class*="service"]')[:8] if len(elem.get_text().strip()) > 30]
        sections['about'] = [elem.get_text().strip()[:500] for elem in soup.select('[class*="about"], [class*="company"]')[:5] if len(elem.get_text().strip()) > 50]
        sections['features'] = [elem.get_text().strip()[:250] for elem in soup.select('.feature, [class*="feature"]')[:10] if len(elem.get_text().strip()) > 20]
        sections['messaging'] = [elem.get_text().strip() for elem in soup.select('h2, h3, .headline, .tagline')[:12] if 15 < len(elem.get_text().strip()) < 200]
        
        return sections
    
    def _ai_competitive_positioning_analysis(self, html_content, url, content_sections):
        """Advanced AI competitive positioning analysis"""
        context = f"""
        URL: {url}
        HERO CONTENT: {' | '.join(content_sections.get('hero', [])[:3])}
        KEY MESSAGING: {' | '.join(content_sections.get('messaging', [])[:8])}
        PRODUCTS/SERVICES: {' | '.join(content_sections.get('products', [])[:3])}
        """
        
        messages = [
            {"role": "system", "content": "You are an expert strategic brand consultant with deep expertise in competitive positioning analysis. Provide sophisticated strategic insights."},
            {"role": "user", "content": f"""
            ADVANCED COMPETITIVE POSITIONING ANALYSIS
            
            Analyze this company's strategic positioning with sophisticated insights:
            
            {context}
            
            Return detailed JSON analysis:
            {{
                "company_name": "Official company name",
                "core_positioning_strategy": {{
                    "primary_strategy": "Price/Quality/Innovation/Service/Experience",
                    "positioning_statement": "Clear 1-2 sentence positioning",
                    "value_proposition": "Primary value delivered to customers",
                    "competitive_advantage": "Key sustainable advantage"
                }},
                "target_audience_strategy": {{
                    "primary_segment": "Main target customer segment",
                    "secondary_segments": ["Other", "target", "segments"],
                    "psychographic_profile": "Detailed customer psychology/motivations",
                    "decision_factors": ["Key", "factors", "in", "purchase", "decisions"]
                }},
                "differentiation_approach": {{
                    "primary_differentiator": "Main way they stand out",
                    "supporting_differentiators": ["Secondary", "differentiation", "factors"],
                    "uniqueness_score": 85,
                    "differentiation_sustainability": "How sustainable is their differentiation"
                }},
                "brand_archetype": {{
                    "primary_archetype": "Hero/Sage/Creator/Ruler/Caregiver/Explorer/etc",
                    "archetype_confidence": 90,
                    "personality_traits": ["Specific", "brand", "personality", "descriptors"],
                    "emotional_appeal": "Primary emotional connection strategy"
                }},
                "market_position": {{
                    "market_category": "Primary market category they compete in",
                    "subcategory_focus": "Specific niche or specialization",
                    "competitive_set": "Who they compete against",
                    "market_leadership_status": "Leader/Challenger/Follower/Niche"
                }}
            }}
            
            Provide strategic, sophisticated analysis based on the content.
            """
            }
        ]
        
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
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
            print(f"     ❌ AI positioning analysis failed: {e}")
            return self._get_default_positioning_analysis()
    
    def _ai_swot_analysis(self, html_content, url, content_sections):
        """AI-generated SWOT analysis"""
        context = f"""
        COMPANY CONTENT: {' | '.join(content_sections.get('about', [])[:2])}
        PRODUCTS/SERVICES: {' | '.join(content_sections.get('products', [])[:3])}
        KEY FEATURES: {' | '.join(content_sections.get('features', [])[:5])}
        """
        
        messages = [
            {"role": "system", "content": "You are a strategic business analyst specializing in competitive SWOT analysis. Provide actionable insights."},
            {"role": "user", "content": f"""
            COMPREHENSIVE SWOT ANALYSIS
            
            Based on this company's digital presence and messaging, generate a detailed SWOT analysis:
            
            {context}
            
            Return JSON:
            {{
                "strengths": [
                    {{
                        "strength": "Specific strength identified",
                        "evidence": "Why this is a strength based on content",
                        "impact_level": "High/Medium/Low"
                    }}
                ],
                "weaknesses": [
                    {{
                        "weakness": "Potential weakness or vulnerability",
                        "evidence": "What suggests this weakness",
                        "impact_level": "High/Medium/Low"
                    }}
                ],
                "opportunities": [
                    {{
                        "opportunity": "Market or strategic opportunity",
                        "rationale": "Why this is an opportunity",
                        "potential_impact": "High/Medium/Low"
                    }}
                ],
                "threats": [
                    {{
                        "threat": "Competitive or market threat",
                        "likelihood": "High/Medium/Low",
                        "potential_impact": "High/Medium/Low"
                    }}
                ],
                "strategic_priorities": [
                    "Key strategic focus areas based on SWOT"
                ]
            }}
            
            Focus on actionable insights that could inform strategic decisions.
            """
            }
        ]
        
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                temperature=0.2,
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
            print(f"     ❌ AI SWOT analysis failed: {e}")
            return self._get_default_swot_analysis()
    
    def _ai_target_audience_analysis(self, html_content, url, content_sections):
        """AI target audience inference and analysis"""
        context = f"""
        MESSAGING: {' | '.join(content_sections.get('messaging', [])[:8])}
        NAVIGATION: {' | '.join(content_sections.get('navigation', [])[:10])}
        FEATURES: {' | '.join(content_sections.get('features', [])[:5])}
        """
        
        messages = [
            {"role": "system", "content": "You are a customer insights specialist who infers target audience characteristics from brand messaging and content."},
            {"role": "user", "content": f"""
            TARGET AUDIENCE INTELLIGENCE ANALYSIS
            
            Analyze the messaging and content to infer detailed target audience characteristics:
            
            {context}
            
            Return JSON:
            {{
                "primary_audience": {{
                    "demographic_profile": {{
                        "age_range": "Estimated age range",
                        "income_level": "Estimated income bracket",
                        "education_level": "Likely education background",
                        "job_titles": ["Common", "job", "titles"],
                        "company_size": "Target company sizes if B2B"
                    }},
                    "psychographic_profile": {{
                        "values": ["Core", "values", "that", "matter"],
                        "pain_points": ["Primary", "pain", "points", "addressed"],
                        "motivations": ["Key", "driving", "motivations"],
                        "decision_triggers": ["What", "drives", "purchase", "decisions"]
                    }},
                    "behavioral_patterns": {{
                        "research_behavior": "How they likely research solutions",
                        "buying_process": "Typical buying journey characteristics",
                        "communication_preferences": "Preferred communication style",
                        "technology_adoption": "Early/mainstream/late adopter profile"
                    }}
                }},
                "secondary_audiences": [
                    {{
                        "audience_type": "Secondary audience segment",
                        "characteristics": "Key characteristics",
                        "messaging_approach": "How messaging differs for this group"
                    }}
                ],
                "audience_sophistication": {{
                    "industry_knowledge_level": "Beginner/Intermediate/Expert",
                    "solution_awareness": "Problem/solution aware or unaware",
                    "decision_complexity": "Simple/moderate/complex decision process"
                }}
            }}
            
            Base insights on actual messaging tone, complexity, and content focus.
            """
            }
        ]
        
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
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
            print(f"     ❌ AI audience analysis failed: {e}")
            return self._get_default_audience_analysis()
    
    def _ai_innovation_opportunities(self, html_content, url, content_sections):
        """AI-powered innovation opportunity detection"""
        context = f"""
        PRODUCTS/SERVICES: {' | '.join(content_sections.get('products', [])[:5])}
        FEATURES: {' | '.join(content_sections.get('features', [])[:8])}
        MESSAGING: {' | '.join(content_sections.get('messaging', [])[:6])}
        """
        
        messages = [
            {"role": "system", "content": "You are an innovation strategist who identifies market gaps and innovation opportunities from competitive analysis."},
            {"role": "user", "content": f"""
            INNOVATION OPPORTUNITY DETECTION
            
            Analyze this company's offerings and identify innovation opportunities:
            
            {context}
            
            Return JSON:
            {{
                "current_innovation_level": {{
                    "innovation_score": 75,
                    "innovation_areas": ["Areas", "where", "they", "innovate"],
                    "technology_sophistication": "Leading/competitive/lagging",
                    "innovation_messaging": "How prominently they position innovation"
                }},
                "market_gaps_identified": [
                    {{
                        "gap_area": "Specific market gap or unmet need",
                        "opportunity_size": "Large/Medium/Small",
                        "evidence": "What suggests this gap exists",
                        "difficulty_to_address": "Easy/Moderate/Difficult"
                    }}
                ],
                "emerging_technology_opportunities": [
                    {{
                        "technology": "AI/Blockchain/IoT/etc",
                        "application_potential": "How it could be applied",
                        "competitive_advantage": "Advantage it could provide",
                        "implementation_complexity": "Low/Medium/High"
                    }}
                ],
                "customer_experience_gaps": [
                    {{
                        "experience_area": "Specific CX improvement area",
                        "current_limitation": "What's limiting current experience",
                        "improvement_opportunity": "How it could be enhanced"
                    }}
                ],
                "strategic_recommendations": [
                    "Specific innovation recommendations based on analysis"
                ]
            }}
            
            Focus on actionable innovation opportunities.
            """
            }
        ]
        
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                temperature=0.2,
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
            print(f"     ❌ AI innovation analysis failed: {e}")
            return self._get_default_innovation_analysis()
    
    def _ai_brand_health_scoring(self, html_content, url, content_sections):
        """AI-powered brand health scoring system"""
        context = f"""
        COMPANY: {url}
        HERO MESSAGING: {' | '.join(content_sections.get('hero', [])[:3])}
        KEY MESSAGES: {' | '.join(content_sections.get('messaging', [])[:8])}
        FEATURES: {' | '.join(content_sections.get('features', [])[:6])}
        """
        
        messages = [
            {"role": "system", "content": "You are a brand strategist who evaluates brand health across multiple dimensions. Provide quantitative scores and qualitative insights."},
            {"role": "user", "content": f"""
            COMPREHENSIVE BRAND HEALTH SCORING
            
            Evaluate this brand's health across key dimensions:
            
            {context}
            
            Return JSON with scores (0-100):
            {{
                "overall_score": 85,
                "dimension_scores": {{
                    "messaging_clarity": {{
                        "score": 90,
                        "assessment": "How clear and compelling the value proposition is",
                        "strengths": ["Specific", "messaging", "strengths"],
                        "improvements": ["Areas", "for", "improvement"]
                    }},
                    "differentiation_strength": {{
                        "score": 75,
                        "assessment": "How unique and defensible the positioning is",
                        "uniqueness_factors": ["What", "makes", "them", "unique"],
                        "commoditization_risk": "Low/Medium/High"
                    }},
                    "digital_presence": {{
                        "score": 80,
                        "assessment": "Quality of digital brand experience",
                        "strengths": ["Digital", "presence", "strengths"],
                        "weaknesses": ["Areas", "needing", "improvement"]
                    }},
                    "market_fit": {{
                        "score": 85,
                        "assessment": "Alignment with target audience needs",
                        "fit_indicators": ["Evidence", "of", "good", "market", "fit"],
                        "misalignment_risks": ["Potential", "misalignment", "areas"]
                    }}
                }},
                "competitive_threat_level": "High/Medium/Low",
                "threat_assessment": {{
                    "threat_level_rationale": "Why this threat level was assigned",
                    "competitive_advantages": ["Key", "competitive", "advantages"],
                    "vulnerability_areas": ["Areas", "of", "competitive", "vulnerability"]
                }},
                "strategic_health_indicators": {{
                    "innovation_capability": "Strong/Moderate/Weak",
                    "market_position": "Leader/Strong/Moderate/Weak",
                    "brand_momentum": "Growing/Stable/Declining",
                    "strategic_clarity": "High/Medium/Low"
                }}
            }}
            
            Provide accurate scores based on content analysis.
            """
            }
        ]
        
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                temperature=0.1,
                max_tokens=2500
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
            print(f"     ❌ AI brand health scoring failed: {e}")
            return self._get_default_brand_health()
    
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
        """Extract and process brand colors"""
        soup = BeautifulSoup(html_content, 'html.parser')
        all_colors = set()
        
        # Extract from various sources
        for element in soup.find_all(style=True):
            style = element.get('style', '')
            colors = re.findall(r'#[0-9a-fA-F]{6}|#[0-9a-fA-F]{3}|rgb\([^)]+\)', style)
            all_colors.update(colors)
        
        for style_tag in soup.find_all('style'):
            css_content = style_tag.get_text()
            colors = re.findall(r'#[0-9a-fA-F]{6}|#[0-9a-fA-F]{3}|rgb\([^)]+\)', css_content)
            all_colors.update(colors)
        
        return self._process_colors(list(all_colors))
    
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
        """Capture screenshot for visual analysis"""
        try:
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--window-size=1200,800')
            
            driver = webdriver.Chrome(options=chrome_options)
            driver.get(url)
            time.sleep(5)
            
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
    
    def generate_cross_brand_insights(self):
        """Generate AI-powered cross-brand competitive insights"""
        if len(self.brand_profiles) < 2:
            return {}
        
        # Compile all brand data for cross-analysis
        brand_summary = ""
        for brand in self.brand_profiles:
            brand_summary += f"""
            Brand: {brand['company_name']}
            Positioning: {brand['ai_positioning_analysis']['core_positioning_strategy']['positioning_statement']}
            Target: {brand['ai_audience_analysis']['primary_audience']['demographic_profile']}
            Health Score: {brand['ai_brand_health']['overall_score']}
            Threat Level: {brand['ai_brand_health']['competitive_threat_level']}
            ---
            """
        
        messages = [
            {"role": "system", "content": "You are a competitive intelligence expert analyzing market dynamics across multiple brands."},
            {"role": "user", "content": f"""
            CROSS-BRAND COMPETITIVE INTELLIGENCE ANALYSIS
            
            Analyze these competing brands and provide strategic insights:
            
            {brand_summary}
            
            Return JSON:
            {{
                "market_dynamics": {{
                    "market_maturity": "Emerging/Growth/Mature/Declining",
                    "competitive_intensity": "Low/Medium/High",
                    "differentiation_difficulty": "Easy/Moderate/Difficult",
                    "innovation_pace": "Slow/Moderate/Fast"
                }},
                "positioning_gaps": [
                    {{
                        "gap_area": "Unclaimed positioning territory",
                        "opportunity_size": "Large/Medium/Small",
                        "rationale": "Why this is a gap"
                    }}
                ],
                "threat_rankings": [
                    {{
                        "brand": "Brand name",
                        "threat_level": "High/Medium/Low",
                        "threat_rationale": "Why they're this level of threat"
                    }}
                ],
                "market_entry_strategy": {{
                    "recommended_positioning": "Optimal positioning for new entrant",
                    "target_segment": "Best target segment to focus on",
                    "differentiation_strategy": "How to differentiate effectively",
                    "competitive_response_likely": "How competitors might respond"
                }},
                "strategic_recommendations": [
                    "Actionable strategic insights for market participants"
                ]
            }}
            """
            }
        ]
        
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
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
                
        except Exception as e:
            print(f"     ❌ Cross-brand analysis failed: {e}")
        
        return {}
    
    # Default fallback methods
    def _get_default_positioning_analysis(self):
        return {
            "company_name": "Unknown Company",
            "core_positioning_strategy": {
                "primary_strategy": "Quality",
                "positioning_statement": "Professional service provider",
                "value_proposition": "Quality solutions",
                "competitive_advantage": "Experience and reliability"
            },
            "target_audience_strategy": {
                "primary_segment": "Business professionals",
                "psychographic_profile": "Quality-focused professionals",
                "decision_factors": ["Quality", "Reliability", "Service"]
            },
            "differentiation_approach": {
                "primary_differentiator": "Professional expertise",
                "uniqueness_score": 70,
                "differentiation_sustainability": "Moderate"
            },
            "brand_archetype": {
                "primary_archetype": "The Sage",
                "archetype_confidence": 75,
                "personality_traits": ["Professional", "Reliable", "Trustworthy"],
                "emotional_appeal": "Trust and competence"
            },
            "market_position": {
                "market_category": "Professional services",
                "competitive_set": "Industry competitors",
                "market_leadership_status": "Follower"
            }
        }
    
    def _get_default_swot_analysis(self):
        return {
            "strengths": [{"strength": "Professional positioning", "evidence": "Clear professional messaging", "impact_level": "Medium"}],
            "weaknesses": [{"weakness": "Limited differentiation", "evidence": "Generic messaging", "impact_level": "Medium"}],
            "opportunities": [{"opportunity": "Digital transformation", "rationale": "Growing digital adoption", "potential_impact": "High"}],
            "threats": [{"threat": "Increased competition", "likelihood": "High", "potential_impact": "Medium"}],
            "strategic_priorities": ["Strengthen differentiation", "Enhance digital presence"]
        }
    
    def _get_default_audience_analysis(self):
        return {
            "primary_audience": {
                "demographic_profile": {
                    "age_range": "30-55",
                    "income_level": "Middle to upper-middle class",
                    "education_level": "College educated",
                    "job_titles": ["Manager", "Director", "Executive"]
                },
                "psychographic_profile": {
                    "values": ["Quality", "Reliability", "Professionalism"],
                    "pain_points": ["Need for reliable solutions"],
                    "motivations": ["Professional success", "Risk mitigation"]
                }
            }
        }
    
    def _get_default_innovation_analysis(self):
        return {
            "current_innovation_level": {
                "innovation_score": 65,
                "technology_sophistication": "Competitive"
            },
            "market_gaps_identified": [{"gap_area": "Digital experience", "opportunity_size": "Medium"}],
            "strategic_recommendations": ["Invest in digital capabilities", "Focus on customer experience"]
        }
    
    def _get_default_brand_health(self):
        return {
            "overall_score": 70,
            "dimension_scores": {
                "messaging_clarity": {"score": 75, "assessment": "Moderate clarity"},
                "differentiation_strength": {"score": 65, "assessment": "Limited differentiation"},
                "digital_presence": {"score": 70, "assessment": "Standard digital presence"},
                "market_fit": {"score": 75, "assessment": "Good market alignment"}
            },
            "competitive_threat_level": "Medium",
            "threat_assessment": {
                "threat_level_rationale": "Standard competitive positioning",
                "competitive_advantages": ["Professional reputation"],
                "vulnerability_areas": ["Digital innovation"]
            }
        }
    
    def generate_ai_powered_report(self, urls, report_title="AI-Powered Competitive Intelligence", output_filename=None):
        """Generate comprehensive AI-powered competitive intelligence report in 16:9 slide format"""
        
        if not output_filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_filename = f"ai_competitive_intelligence_{timestamp}.html"
        
        print(f"🤖 Generating AI-Powered Competitive Intelligence Report...")
        print(f"📊 Analyzing {len(urls)} brands with advanced AI insights...")
        
        # Analyze all brands with AI
        self.brand_profiles = []
        seen_companies = set()
        
        try:
            for i, url in enumerate(urls, 1):
                print(f"\n🔍 [{i}/{len(urls)}] Advanced AI Analysis: {url}")
                try:
                    profile = self.extract_comprehensive_brand_data(url)
                    if profile:
                        company_name = profile['company_name']
                        if company_name not in seen_companies:
                            self.brand_profiles.append(profile)
                            seen_companies.add(company_name)
                            print(f"✅ AI analysis complete: {company_name}")
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
        
        # Generate cross-brand competitive insights
        print(f"\n🧠 Generating cross-brand AI insights...")
        self.competitive_insights = self.generate_cross_brand_insights()
        
        # Generate 16:9 slide-based report
        print(f"\n📄 Creating 16:9 slide presentation...")
        html_content = self._generate_slide_presentation(report_title)
        
        # Save report
        try:
            with open(output_filename, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            print(f"\n🎉 AI-POWERED REPORT GENERATED!")
            print(f"📁 File: {output_filename}")
            print(f"📊 Brands analyzed: {len(self.brand_profiles)}")
            print(f"📄 Format: 16:9 presentation slides")
            print(f"🤖 AI insights: Positioning, SWOT, Audience, Innovation, Brand Health")
            print(f"🌐 Open in browser for interactive slide navigation")
            
            return output_filename
            
        except Exception as e:
            print(f"❌ Error saving report: {e}")
            return None
    
    def _generate_slide_presentation(self, report_title):
        """Generate 16:9 slide-based presentation"""
        total_slides = 2 + len(self.brand_profiles) + 2  # Title + Overview + Individual + Comparison + Strategy
        
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{report_title} - AI-Powered Analysis</title>
    <style>
        {self._get_slide_css()}
    </style>
    <script>
        {self._get_slide_navigation_js()}
    </script>
</head>
<body>
"""
        
        # Slide 1: Title Slide
        html_content += self._generate_title_slide(report_title, 1, total_slides)
        
        # Slide 2: Competitive Overview
        html_content += self._generate_overview_slide(2, total_slides)
        
        # Slides 3-N+2: Individual Brand AI Analysis
        for i, brand in enumerate(self.brand_profiles, 3):
            html_content += self._generate_brand_ai_slide(brand, i, total_slides)
        
        # Slide N+3: Cross-Brand Comparison & Insights
        html_content += self._generate_comparison_slide(len(self.brand_profiles) + 3, total_slides)
        
        # Slide N+4: Strategic Recommendations
        html_content += self._generate_strategy_slide(total_slides, total_slides)
        
        html_content += """
</body>
</html>"""
        
        return html_content
    
    def _get_slide_css(self):
        """16:9 slide presentation CSS"""
        return """
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #1a1a1a;
            color: #333;
            overflow: hidden;
        }
        
        /* 16:9 Slide Container */
        .slide {
            width: 100vw;
            height: 100vh;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            display: none;
            position: relative;
            padding: 60px;
            box-sizing: border-box;
        }
        
        .slide.active {
            display: flex;
            flex-direction: column;
        }
        
        /* Slide Header */
        .slide-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 40px;
            padding-bottom: 20px;
            border-bottom: 2px solid rgba(255,255,255,0.3);
        }
        
        .slide-title {
            font-size: 2.5em;
            font-weight: 700;
            color: white;
            text-shadow: 0 2px 4px rgba(0,0,0,0.3);
        }
        
        .slide-number {
            font-size: 1.2em;
            color: rgba(255,255,255,0.8);
            background: rgba(255,255,255,0.1);
            padding: 10px 20px;
            border-radius: 25px;
            backdrop-filter: blur(10px);
        }
        
        /* Navigation */
        .slide-navigation {
            position: fixed;
            bottom: 30px;
            left: 50%;
            transform: translateX(-50%);
            display: flex;
            gap: 10px;
            z-index: 1000;
        }
        
        .nav-dot {
            width: 12px;
            height: 12px;
            border-radius: 50%;
            background: rgba(255,255,255,0.4);
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .nav-dot.active {
            background: white;
            transform: scale(1.2);
        }
        
        .nav-button {
            position: fixed;
            top: 50%;
            transform: translateY(-50%);
            background: rgba(255,255,255,0.1);
            color: white;
            border: none;
            padding: 15px 20px;
            font-size: 1.5em;
            cursor: pointer;
            border-radius: 50%;
            backdrop-filter: blur(10px);
            transition: all 0.3s ease;
            z-index: 1000;
        }
        
        .nav-button:hover {
            background: rgba(255,255,255,0.2);
            transform: translateY(-50%) scale(1.1);
        }
        
        .nav-prev {
            left: 30px;
        }
        
        .nav-next {
            right: 30px;
        }
        
        /* Content Areas */
        .slide-content {
            flex: 1;
            display: flex;
            flex-direction: column;
            gap: 30px;
        }
        
        .content-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 40px;
            height: 100%;
        }
        
        .content-card {
            background: rgba(255,255,255,0.95);
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            backdrop-filter: blur(10px);
        }
        
        .card-title {
            font-size: 1.5em;
            font-weight: 600;
            color: #2c3e50;
            margin-bottom: 20px;
            border-bottom: 2px solid #e9ecef;
            padding-bottom: 10px;
        }
        
        /* AI Insights Styling */
        .ai-insight {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            padding: 15px;
            border-radius: 10px;
            margin: 10px 0;
            position: relative;
        }
        
        .ai-insight::before {
            content: "🤖";
            position: absolute;
            top: -5px;
            right: 10px;
            font-size: 1.2em;
        }
        
        .score-display {
            display: flex;
            align-items: center;
            gap: 15px;
            margin: 15px 0;
        }
        
        .score-circle {
            width: 60px;
            height: 60px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            font-size: 1.2em;
            color: white;
        }
        
        .score-high { background: #28a745; }
        .score-medium { background: #ffc107; color: #333; }
        .score-low { background: #dc3545; }
        
        .threat-badge {
            display: inline-block;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.9em;
            font-weight: 600;
            text-transform: uppercase;
        }
        
        .threat-high { background: #dc3545; color: white; }
        .threat-medium { background: #ffc107; color: #333; }
        .threat-low { background: #28a745; color: white; }
        
        /* Brand Grid for Overview */
        .brand-overview-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }
        
        .brand-card {
            background: rgba(255,255,255,0.95);
            border-radius: 10px;
            padding: 20px;
            text-align: center;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        
        .brand-logo {
            max-height: 40px;
            margin-bottom: 15px;
        }
        
        .brand-name {
            font-size: 1.2em;
            font-weight: 600;
            color: #2c3e50;
            margin-bottom: 10px;
        }
        
        .brand-score {
            font-size: 2em;
            font-weight: bold;
            margin: 10px 0;
        }
        
        /* SWOT Grid */
        .swot-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 15px;
            height: 100%;
        }
        
        .swot-quadrant {
            padding: 20px;
            border-radius: 10px;
            color: white;
        }
        
        .swot-strengths { background: #28a745; }
        .swot-weaknesses { background: #dc3545; }
        .swot-opportunities { background: #007bff; }
        .swot-threats { background: #ffc107; color: #333; }
        
        .swot-title {
            font-size: 1.2em;
            font-weight: 600;
            margin-bottom: 15px;
            text-align: center;
        }
        
        .swot-item {
            background: rgba(255,255,255,0.1);
            padding: 8px 12px;
            border-radius: 5px;
            margin-bottom: 8px;
            font-size: 0.9em;
        }
        
        /* Comparison Table */
        .comparison-table {
            width: 100%;
            border-collapse: collapse;
            background: white;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        
        .comparison-table th,
        .comparison-table td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #e9ecef;
        }
        
        .comparison-table th {
            background: #f8f9fa;
            font-weight: 600;
            color: #2c3e50;
        }
        
        /* Title Slide Specific */
        .title-slide {
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            justify-content: center;
            align-items: center;
            text-align: center;
        }
        
        .main-title {
            font-size: 4em;
            font-weight: 700;
            color: white;
            margin-bottom: 30px;
            text-shadow: 0 4px 8px rgba(0,0,0,0.3);
        }
        
        .subtitle {
            font-size: 1.8em;
            color: rgba(255,255,255,0.9);
            margin-bottom: 40px;
        }
        
        .ai-badge {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            padding: 15px 30px;
            border-radius: 50px;
            font-size: 1.2em;
            font-weight: 600;
            display: inline-block;
            margin: 20px 0;
        }
        
        .date-stamp {
            color: rgba(255,255,255,0.7);
            font-size: 1.1em;
            margin-top: 30px;
        }
        
        /* Responsive */
        @media (max-width: 1200px) {
            .slide {
                padding: 40px;
            }
            
            .slide-title {
                font-size: 2em;
            }
            
            .content-grid {
                grid-template-columns: 1fr;
                gap: 20px;
            }
        }
        
        /* Print styles */
        @media print {
            .slide {
                display: block !important;
                page-break-after: always;
                height: 297mm;
                width: 210mm;
            }
            
            .nav-button, .slide-navigation {
                display: none;
            }
        }
        """
    
    def _get_slide_navigation_js(self):
        """JavaScript for slide navigation"""
        return """
        let currentSlide = 0;
        let totalSlides = 0;
        
        document.addEventListener('DOMContentLoaded', function() {
            const slides = document.querySelectorAll('.slide');
            totalSlides = slides.length;
            
            // Create navigation dots
            const navContainer = document.querySelector('.slide-navigation');
            for (let i = 0; i < totalSlides; i++) {
                const dot = document.createElement('div');
                dot.className = 'nav-dot';
                dot.onclick = () => goToSlide(i);
                navContainer.appendChild(dot);
            }
            
            showSlide(0);
            
            // Keyboard navigation
            document.addEventListener('keydown', function(e) {
                if (e.key === 'ArrowRight' || e.key === ' ') {
                    nextSlide();
                } else if (e.key === 'ArrowLeft') {
                    prevSlide();
                }
            });
        });
        
        function showSlide(n) {
            const slides = document.querySelectorAll('.slide');
            const dots = document.querySelectorAll('.nav-dot');
            
            slides.forEach(slide => slide.classList.remove('active'));
            dots.forEach(dot => dot.classList.remove('active'));
            
            if (n >= totalSlides) currentSlide = 0;
            if (n < 0) currentSlide = totalSlides - 1;
            
            slides[currentSlide].classList.add('active');
            dots[currentSlide].classList.add('active');
        }
        
        function nextSlide() {
            currentSlide++;
            if (currentSlide >= totalSlides) currentSlide = 0;
            showSlide(currentSlide);
        }
        
        function prevSlide() {
            currentSlide--;
            if (currentSlide < 0) currentSlide = totalSlides - 1;
            showSlide(currentSlide);
        }
        
        function goToSlide(n) {
            currentSlide = n;
            showSlide(currentSlide);
        }
        """
    
    def _generate_title_slide(self, report_title, slide_num, total_slides):
        """Generate title slide"""
        return f"""
    <div class="slide title-slide" id="slide-{slide_num}">
        <div class="slide-content">
            <h1 class="main-title">{report_title}</h1>
            <p class="subtitle">Advanced AI-Powered Competitive Intelligence</p>
            <div class="ai-badge">🤖 Powered by GPT-4 Strategic Analysis</div>
            <p class="date-stamp">Generated on {datetime.now().strftime('%B %d, %Y')}</p>
        </div>
        
        <button class="nav-button nav-next" onclick="nextSlide()">→</button>
        
        <div class="slide-navigation"></div>
    </div>
        """
    
    def _generate_overview_slide(self, slide_num, total_slides):
        """Generate competitive overview slide"""
        brand_cards = ""
        for brand in self.brand_profiles:
            logo_img = f'<img src="{brand["logos"][0]}" class="brand-logo" alt="Logo">' if brand.get("logos") else ""
            health_score = brand["ai_brand_health"]["overall_score"]
            threat_level = brand["ai_brand_health"]["competitive_threat_level"]
            
            score_class = "score-high" if health_score >= 80 else "score-medium" if health_score >= 60 else "score-low"
            threat_class = f"threat-{threat_level.lower()}"
            
            brand_cards += f"""
                <div class="brand-card">
                    {logo_img}
                    <div class="brand-name">{brand['company_name']}</div>
                    <div class="brand-score {score_class}">{health_score}</div>
                    <div class="threat-badge {threat_class}">{threat_level} Threat</div>
                </div>
            """
        
        return f"""
    <div class="slide" id="slide-{slide_num}">
        <div class="slide-header">
            <h2 class="slide-title">Competitive Landscape Overview</h2>
            <div class="slide-number">Slide {slide_num} of {total_slides}</div>
        </div>
        
        <div class="slide-content">
            <div class="ai-insight">
                <strong>AI Market Analysis:</strong> {self.competitive_insights.get('market_dynamics', {}).get('competitive_intensity', 'Medium')} competitive intensity with {len(self.brand_profiles)} key players analyzed
            </div>
            
            <div class="brand-overview-grid">
                {brand_cards}
            </div>
        </div>
        
        <button class="nav-button nav-prev" onclick="prevSlide()">←</button>
        <button class="nav-button nav-next" onclick="nextSlide()">→</button>
    </div>
        """
    
    def _generate_brand_ai_slide(self, brand, slide_num, total_slides):
        """Generate individual brand AI analysis slide"""
        positioning = brand["ai_positioning_analysis"]["core_positioning_strategy"]
        health = brand["ai_brand_health"]
        swot = brand["ai_swot_analysis"]
        
        # Create SWOT grid
        swot_html = f"""
        <div class="swot-grid">
            <div class="swot-quadrant swot-strengths">
                <div class="swot-title">Strengths</div>
                {''.join([f'<div class="swot-item">{s["strength"]}</div>' for s in swot["strengths"][:3]])}
            </div>
            <div class="swot-quadrant swot-weaknesses">
                <div class="swot-title">Weaknesses</div>
                {''.join([f'<div class="swot-item">{w["weakness"]}</div>' for w in swot["weaknesses"][:3]])}
            </div>
            <div class="swot-quadrant swot-opportunities">
                <div class="swot-title">Opportunities</div>
                {''.join([f'<div class="swot-item">{o["opportunity"]}</div>' for o in swot["opportunities"][:3]])}
            </div>
            <div class="swot-quadrant swot-threats">
                <div class="swot-title">Threats</div>
                {''.join([f'<div class="swot-item">{t["threat"]}</div>' for t in swot["threats"][:3]])}
            </div>
        </div>
        """
        
        # Health scores
        overall_score = health["overall_score"]
        score_class = "score-high" if overall_score >= 80 else "score-medium" if overall_score >= 60 else "score-low"
        
        return f"""
    <div class="slide" id="slide-{slide_num}">
        <div class="slide-header">
            <h2 class="slide-title">{brand['company_name']} - AI Strategic Analysis</h2>
            <div class="slide-number">Slide {slide_num} of {total_slides}</div>
        </div>
        
        <div class="slide-content">
            <div class="content-grid">
                <div class="content-card">
                    <h3 class="card-title">AI Positioning Analysis</h3>
                    <div class="ai-insight">
                        <strong>Strategy:</strong> {positioning["primary_strategy"]}
                    </div>
                    <p><strong>Positioning:</strong> {positioning["positioning_statement"]}</p>
                    <p><strong>Value Prop:</strong> {positioning["value_proposition"]}</p>
                    <p><strong>Competitive Advantage:</strong> {positioning["competitive_advantage"]}</p>
                    
                    <div class="score-display">
                        <div class="score-circle {score_class}">{overall_score}</div>
                        <div>
                            <strong>Brand Health Score</strong><br>
                            <span class="threat-badge threat-{health['competitive_threat_level'].lower()}">{health['competitive_threat_level']} Threat</span>
                        </div>
                    </div>
                </div>
                
                <div class="content-card">
                    <h3 class="card-title">AI SWOT Analysis</h3>
                    {swot_html}
                </div>
            </div>
        </div>
        
        <button class="nav-button nav-prev" onclick="prevSlide()">←</button>
        <button class="nav-button nav-next" onclick="nextSlide()">→</button>
    </div>
        """
    
    def _generate_comparison_slide(self, slide_num, total_slides):
        """Generate cross-brand comparison slide"""
        # Create comparison table
        table_rows = ""
        
        # Headers
        table_rows += "<tr><th>Metric</th>"
        for brand in self.brand_profiles:
            table_rows += f"<th>{brand['company_name']}</th>"
        table_rows += "</tr>"
        
        # Health Scores
        table_rows += "<tr><td><strong>Health Score</strong></td>"
        for brand in self.brand_profiles:
            score = brand['ai_brand_health']['overall_score']
            table_rows += f"<td><strong>{score}/100</strong></td>"
        table_rows += "</tr>"
        
        # Threat Level
        table_rows += "<tr><td><strong>Threat Level</strong></td>"
        for brand in self.brand_profiles:
            threat = brand['ai_brand_health']['competitive_threat_level']
            table_rows += f"<td><span class=\"threat-badge threat-{threat.lower()}\">{threat}</span></td>"
        table_rows += "</tr>"
        
        # Positioning Strategy
        table_rows += "<tr><td><strong>Primary Strategy</strong></td>"
        for brand in self.brand_profiles:
            strategy = brand['ai_positioning_analysis']['core_positioning_strategy']['primary_strategy']
            table_rows += f"<td>{strategy}</td>"
        table_rows += "</tr>"
        
        # Market insights
        market_insights = ""
        if self.competitive_insights:
            dynamics = self.competitive_insights.get('market_dynamics', {})
            market_insights = f"""
            <div class="ai-insight">
                <strong>AI Market Intelligence:</strong><br>
                • Competitive Intensity: {dynamics.get('competitive_intensity', 'Medium')}<br>
                • Market Maturity: {dynamics.get('market_maturity', 'Growth')}<br>
                • Innovation Pace: {dynamics.get('innovation_pace', 'Moderate')}
            </div>
            """
        
        return f"""
    <div class="slide" id="slide-{slide_num}">
        <div class="slide-header">
            <h2 class="slide-title">Cross-Brand Competitive Intelligence</h2>
            <div class="slide-number">Slide {slide_num} of {total_slides}</div>
        </div>
        
        <div class="slide-content">
            {market_insights}
            
            <div class="content-card" style="margin-top: 20px;">
                <h3 class="card-title">AI-Powered Competitive Comparison</h3>
                <table class="comparison-table">
                    {table_rows}
                </table>
            </div>
        </div>
        
        <button class="nav-button nav-prev" onclick="prevSlide()">←</button>
        <button class="nav-button nav-next" onclick="nextSlide()">→</button>
    </div>
        """
    
    def _generate_strategy_slide(self, slide_num, total_slides):
        """Generate strategic recommendations slide"""
        recommendations = ""
        if self.competitive_insights:
            strategy = self.competitive_insights.get('market_entry_strategy', {})
            recommendations = f"""
            <div class="content-grid">
                <div class="content-card">
                    <h3 class="card-title">AI Strategic Recommendations</h3>
                    <div class="ai-insight">
                        <strong>Recommended Positioning:</strong> {strategy.get('recommended_positioning', 'Customer-centric innovation leader')}
                    </div>
                    <p><strong>Target Segment:</strong> {strategy.get('target_segment', 'Underserved premium market')}</p>
                    <p><strong>Differentiation Strategy:</strong> {strategy.get('differentiation_strategy', 'Technology-forward customer experience')}</p>
                </div>
                
                <div class="content-card">
                    <h3 class="card-title">Market Opportunities</h3>
                    {''.join([f'<div class="ai-insight">• {gap["gap_area"]} ({gap["opportunity_size"]} opportunity)</div>' for gap in self.competitive_insights.get('positioning_gaps', [])[:4]])}
                </div>
            </div>
            """
        else:
            recommendations = """
            <div class="content-card">
                <h3 class="card-title">Strategic Recommendations</h3>
                <div class="ai-insight">Focus on digital-first customer experience and innovative positioning to differentiate from traditional competitors.</div>
            </div>
            """
        
        return f"""
    <div class="slide" id="slide-{slide_num}">
        <div class="slide-header">
            <h2 class="slide-title">Strategic Recommendations & Market Opportunities</h2>
            <div class="slide-number">Slide {slide_num} of {total_slides}</div>
        </div>
        
        <div class="slide-content">
            {recommendations}
        </div>
        
        <button class="nav-button nav-prev" onclick="prevSlide()">←</button>
    </div>
        """


def main():
    """Generate AI-powered competitive intelligence presentation"""
    
    medical_urls = [
        "https://www.wolterskluwer.com",
        "https://www.elsevier.com",
        "https://www.clinicalkey.com",
        "https://www.openevidence.com"
    ]
    
    generator = AIPoweredCompetitiveIntelligence()
    
    output_file = generator.generate_ai_powered_report(
        urls=medical_urls,
        report_title="Medical AI Platform Competitive Intelligence",
        output_filename="ai_powered_competitive_slides.html"
    )
    
    if output_file:
        print(f"\n🎉 AI-POWERED PRESENTATION COMPLETE!")
        print(f"📁 File location: {os.path.abspath(output_file)}")
        print(f"🎪 Format: Interactive 16:9 slides with AI insights")
        print(f"🤖 Features: GPT-4 analysis, SWOT, positioning, health scoring")
        print(f"🌐 Navigation: Arrow keys, click dots, or arrow buttons")

if __name__ == "__main__":
    main()