#!/usr/bin/env python3
"""
Enhanced AI-Powered Competitive Intelligence Generator
Advanced competitive analysis with sophisticated AI insights and differentiated brand analysis
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

class EnhancedAICompetitiveIntelligence:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.driver = None
        self.brand_profiles = []
        self.competitive_insights = {}
        self.market_intelligence = {}
    
    def fetch_page(self, url):
        """Fetch webpage content with error handling"""
        try:
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(f"Failed to retrieve the page: {url} -- {e}")
            return None
    
    def extract_enhanced_brand_data(self, url):
        """Extract comprehensive brand data with enhanced AI analysis"""
        print(f"🔍 ENHANCED AI ANALYSIS: {url}")
        
        html_content = self.fetch_page(url)
        if not html_content:
            return None
        
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Extract comprehensive content
        content_sections = self._extract_comprehensive_content(soup)
        
        # Enhanced AI analysis with context awareness
        print("   🧠 Enhanced Strategic Positioning Analysis...")
        positioning_analysis = self._enhanced_competitive_positioning_analysis(html_content, url, content_sections)
        
        print("   📊 Sophisticated SWOT Analysis...")
        swot_analysis = self._sophisticated_swot_analysis(html_content, url, content_sections, positioning_analysis)
        
        print("   🎯 Advanced Target Audience Intelligence...")
        audience_analysis = self._advanced_audience_analysis(html_content, url, content_sections)
        
        print("   🏆 Competitive Advantage Analysis...")
        competitive_advantage = self._competitive_advantage_analysis(html_content, url, content_sections)
        
        print("   💰 Market Positioning & Pricing Intelligence...")
        market_positioning = self._market_positioning_analysis(html_content, url, content_sections)
        
        print("   ⚡ Enhanced Brand Health Scoring...")
        brand_health = self._enhanced_brand_health_scoring(html_content, url, content_sections, positioning_analysis)
        
        # Visual and data extraction
        logos = self._extract_logos_comprehensive(html_content, url)
        colors = self._extract_colors_comprehensive(html_content, url)
        screenshot = self._capture_screenshot_proper(url)
        
        # Compile enhanced profile
        brand_profile = {
            "url": url,
            "company_name": positioning_analysis.get("company_name", "Unknown Company"),
            "enhanced_positioning": positioning_analysis,
            "sophisticated_swot": swot_analysis,
            "advanced_audience": audience_analysis,
            "competitive_advantage": competitive_advantage,
            "market_positioning": market_positioning,
            "enhanced_brand_health": brand_health,
            "logos": logos,
            "color_palette": colors,
            "screenshot": screenshot,
            "content_sections": content_sections,
            "analysis_timestamp": datetime.now().isoformat()
        }
        
        print(f"   ✅ ENHANCED AI ANALYSIS COMPLETE: {brand_profile['company_name']}")
        print(f"      Overall Score: {brand_health.get('overall_score', 'N/A')}/100")
        print(f"      Threat Level: {brand_health.get('competitive_threat_level', 'N/A')}")
        print(f"      Market Position: {market_positioning.get('market_leadership_position', 'N/A')}")
        
        return brand_profile
    
    def _extract_comprehensive_content(self, soup):
        """Extract comprehensive content with more context"""
        sections = {}
        
        # Enhanced content extraction
        sections['hero'] = [elem.get_text().strip() for elem in soup.select('h1, .hero, [class*="hero"], .jumbotron')[:10] if elem.get_text().strip()]
        sections['navigation'] = [elem.get_text().strip() for elem in soup.select('nav a, .nav a, header a, .menu a')[:20] if elem.get_text().strip()]
        sections['products'] = [elem.get_text().strip()[:400] for elem in soup.select('.product, [class*="product"], .service, [class*="service"], .solution')[:12] if len(elem.get_text().strip()) > 30]
        sections['about'] = [elem.get_text().strip()[:600] for elem in soup.select('[class*="about"], [class*="company"], [class*="mission"]')[:8] if len(elem.get_text().strip()) > 50]
        sections['features'] = [elem.get_text().strip()[:300] for elem in soup.select('.feature, [class*="feature"], .capability, [class*="benefit"]')[:15] if len(elem.get_text().strip()) > 20]
        sections['messaging'] = [elem.get_text().strip() for elem in soup.select('h2, h3, .headline, .tagline, .value-prop')[:15] if 15 < len(elem.get_text().strip()) < 200]
        
        # Extract pricing indicators
        sections['pricing_indicators'] = [elem.get_text().strip() for elem in soup.select('[class*="price"], [class*="cost"], [class*="plan"]')[:10] if elem.get_text().strip()]
        
        # Extract competitive claims
        sections['competitive_claims'] = [elem.get_text().strip() for elem in soup.select('[class*="advantage"], [class*="benefit"], [class*="unique"]')[:10] if len(elem.get_text().strip()) > 20]
        
        return sections
    
    def _enhanced_competitive_positioning_analysis(self, html_content, url, content_sections):
        """Enhanced competitive positioning with deeper insights"""
        context = f"""
        URL: {url}
        HERO CONTENT: {' | '.join(content_sections.get('hero', [])[:5])}
        KEY MESSAGING: {' | '.join(content_sections.get('messaging', [])[:12])}
        PRODUCTS/SERVICES: {' | '.join(content_sections.get('products', [])[:5])}
        FEATURES/CAPABILITIES: {' | '.join(content_sections.get('features', [])[:8])}
        COMPETITIVE CLAIMS: {' | '.join(content_sections.get('competitive_claims', [])[:5])}
        PRICING INDICATORS: {' | '.join(content_sections.get('pricing_indicators', [])[:5])}
        """
        
        messages = [
            {"role": "system", "content": "You are a senior competitive intelligence analyst with expertise in strategic positioning. Provide sophisticated, differentiated insights that identify unique competitive advantages and market positions."},
            {"role": "user", "content": f"""
            SOPHISTICATED COMPETITIVE POSITIONING ANALYSIS
            
            Analyze this company's strategic positioning with deep competitive intelligence:
            
            {context}
            
            Provide detailed, specific analysis (not generic insights):
            
            {{
                "company_name": "Official company name",
                "unique_value_proposition": {{
                    "primary_value_driver": "Specific unique value they deliver",
                    "differentiation_claim": "How they specifically differentiate from competitors",
                    "credibility_assessment": "High/Medium/Low - how credible their claims are",
                    "supporting_evidence": ["Specific", "evidence", "from", "content"]
                }},
                "competitive_strategy": {{
                    "positioning_approach": "Leader/Challenger/Follower/Niche Player",
                    "competition_direct_mentions": ["Any", "competitors", "mentioned"],
                    "competitive_advantages_claimed": ["Specific", "advantages", "they", "claim"],
                    "defensive_positioning": "How they protect against competition"
                }},
                "market_focus": {{
                    "primary_market_segment": "Specific market they target",
                    "industry_specialization": "Specific industries they focus on",
                    "customer_size_focus": "Enterprise/Mid-market/SMB/All",
                    "geographic_focus": "Global/Regional/Local focus"
                }},
                "innovation_positioning": {{
                    "innovation_emphasis": "High/Medium/Low emphasis on innovation",
                    "technology_sophistication": "Leading-edge/Competitive/Basic",
                    "innovation_evidence": ["Specific", "innovation", "examples"],
                    "future_focus": "How forward-looking their positioning is"
                }},
                "brand_personality": {{
                    "communication_style": "Specific tone and style description",
                    "brand_archetype": "Specific archetype with reasoning",
                    "emotional_positioning": "Primary emotional appeal",
                    "personality_differentiators": ["Unique", "personality", "traits"]
                }},
                "positioning_strength": {{
                    "clarity_score": 85,
                    "uniqueness_score": 72,
                    "credibility_score": 90,
                    "memorability_score": 68
                }}
            }}
            
            Focus on SPECIFIC, UNIQUE insights based on actual content analysis.
            """
            }
        ]
        
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                temperature=0.05,  # Lower temperature for more consistent analysis
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
            print(f"     ❌ Enhanced positioning analysis failed: {e}")
            return self._get_default_enhanced_positioning()
    
    def _sophisticated_swot_analysis(self, html_content, url, content_sections, positioning_data):
        """Generate sophisticated, specific SWOT analysis"""
        context = f"""
        COMPANY: {positioning_data.get('company_name', 'Unknown')}
        UNIQUE VALUE PROP: {positioning_data.get('unique_value_proposition', {}).get('primary_value_driver', 'N/A')}
        COMPETITIVE STRATEGY: {positioning_data.get('competitive_strategy', {}).get('positioning_approach', 'N/A')}
        INNOVATION LEVEL: {positioning_data.get('innovation_positioning', {}).get('technology_sophistication', 'N/A')}
        
        CONTENT ANALYSIS:
        FEATURES: {' | '.join(content_sections.get('features', [])[:8])}
        COMPETITIVE CLAIMS: {' | '.join(content_sections.get('competitive_claims', [])[:5])}
        ABOUT COMPANY: {' | '.join(content_sections.get('about', [])[:3])}
        """
        
        messages = [
            {"role": "system", "content": "You are a strategic business analyst who generates specific, actionable SWOT analyses based on actual company data and competitive intelligence."},
            {"role": "user", "content": f"""
            SOPHISTICATED SWOT ANALYSIS
            
            Generate a detailed, specific SWOT analysis based on this company's actual positioning and content:
            
            {context}
            
            Return JSON with specific, actionable insights (not generic business advice):
            
            {{
                "strengths": [
                    {{
                        "strength": "Specific competitive strength based on content",
                        "evidence": "Specific evidence from their positioning/content",
                        "competitive_advantage": "How this creates advantage vs competitors",
                        "sustainability": "High/Medium/Low - how sustainable this strength is"
                    }}
                ],
                "weaknesses": [
                    {{
                        "weakness": "Specific vulnerability or limitation",
                        "evidence": "What in their content suggests this weakness",
                        "competitive_risk": "How competitors could exploit this",
                        "urgency": "High/Medium/Low - how urgent to address"
                    }}
                ],
                "opportunities": [
                    {{
                        "opportunity": "Specific market or strategic opportunity",
                        "market_evidence": "Market conditions supporting this opportunity",
                        "competitive_gap": "Gap in competitive landscape",
                        "revenue_potential": "High/Medium/Low potential impact"
                    }}
                ],
                "threats": [
                    {{
                        "threat": "Specific competitive or market threat",
                        "threat_source": "Where this threat comes from",
                        "likelihood": "High/Medium/Low probability",
                        "impact_severity": "High/Medium/Low potential damage"
                    }}
                ],
                "strategic_implications": [
                    "Specific strategic actions based on SWOT analysis"
                ]
            }}
            
            Make each point specific to this company, not generic business insights.
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
            print(f"     ❌ Sophisticated SWOT analysis failed: {e}")
            return self._get_default_swot()
    
    def _advanced_audience_analysis(self, html_content, url, content_sections):
        """Advanced target audience analysis with specific insights"""
        context = f"""
        MESSAGING ANALYSIS: {' | '.join(content_sections.get('messaging', [])[:10])}
        NAVIGATION STRUCTURE: {' | '.join(content_sections.get('navigation', [])[:15])}
        PRODUCT POSITIONING: {' | '.join(content_sections.get('products', [])[:5])}
        FEATURE EMPHASIS: {' | '.join(content_sections.get('features', [])[:8])}
        """
        
        messages = [
            {"role": "system", "content": "You are a customer insights specialist who analyzes target audience characteristics from messaging tone, complexity, and content focus."},
            {"role": "user", "content": f"""
            ADVANCED TARGET AUDIENCE INTELLIGENCE
            
            Analyze the messaging and positioning to infer specific target audience characteristics:
            
            {context}
            
            Return detailed audience intelligence:
            
            {{
                "primary_audience": {{
                    "demographic_specifics": {{
                        "job_functions": ["Specific", "job", "roles", "targeted"],
                        "seniority_level": "C-level/Director/Manager/Individual Contributor",
                        "company_size": "Enterprise (1000+)/Mid-market (100-1000)/SMB (<100)",
                        "industry_focus": ["Specific", "industries", "if", "apparent"],
                        "technical_sophistication": "High/Medium/Low technical knowledge expected"
                    }},
                    "pain_point_analysis": {{
                        "primary_pain_points": ["Specific", "pain", "points", "addressed"],
                        "urgency_level": "High/Medium/Low urgency messaging",
                        "cost_vs_value_focus": "Cost-focused/Value-focused/ROI-focused",
                        "decision_complexity": "Simple/Complex decision process implied"
                    }},
                    "buying_behavior": {{
                        "decision_makers": ["Who", "appears", "to", "be", "targeted"],
                        "research_depth": "Light/Moderate/Extensive research expected",
                        "evaluation_criteria": ["Key", "factors", "emphasized"],
                        "buying_timeline": "Urgent/Standard/Extended timeline implied"
                    }}
                }},
                "messaging_insights": {{
                    "sophistication_level": "Technical/Business/General audience focus",
                    "credibility_building": ["How", "they", "build", "credibility"],
                    "emotional_appeals": ["Primary", "emotional", "triggers"],
                    "logical_appeals": ["Rational", "arguments", "emphasized"]
                }},
                "competitive_context": {{
                    "audience_overlap": "High/Medium/Low overlap with typical competitors",
                    "differentiated_targeting": "How their audience focus differs",
                    "market_positioning": "Premium/Mid-market/Value positioning implied"
                }}
            }}
            
            Base insights on actual messaging analysis, not assumptions.
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
            print(f"     ❌ Advanced audience analysis failed: {e}")
            return self._get_default_audience()
    
    def _competitive_advantage_analysis(self, html_content, url, content_sections):
        """Analyze specific competitive advantages and moats"""
        context = f"""
        COMPETITIVE CLAIMS: {' | '.join(content_sections.get('competitive_claims', [])[:8])}
        UNIQUE FEATURES: {' | '.join(content_sections.get('features', [])[:10])}
        ABOUT COMPANY: {' | '.join(content_sections.get('about', [])[:3])}
        """
        
        messages = [
            {"role": "system", "content": "You are a competitive strategy expert who identifies sustainable competitive advantages and defensive moats."},
            {"role": "user", "content": f"""
            COMPETITIVE ADVANTAGE ANALYSIS
            
            Identify specific competitive advantages and moats based on content:
            
            {context}
            
            Return analysis:
            
            {{
                "claimed_advantages": [
                    {{
                        "advantage": "Specific advantage claimed",
                        "credibility": "High/Medium/Low based on evidence",
                        "sustainability": "How defensible this advantage is",
                        "competitive_moat": "Network/Scale/Technology/Brand/Regulatory"
                    }}
                ],
                "differentiation_factors": {{
                    "technology_differentiation": "Specific tech advantages if any",
                    "process_differentiation": "Unique processes or methodologies",
                    "partnership_advantages": "Strategic partnerships mentioned",
                    "scale_advantages": "Size or scale benefits"
                }},
                "vulnerability_analysis": {{
                    "easy_to_replicate": ["Advantages", "competitors", "could", "copy"],
                    "high_switching_costs": "Evidence of customer lock-in",
                    "network_effects": "Evidence of network value",
                    "brand_strength": "Brand-based competitive protection"
                }}
            }}
            """
            }
        ]
        
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                temperature=0.1,
                max_tokens=1500
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
            print(f"     ❌ Competitive advantage analysis failed: {e}")
            return {"claimed_advantages": [], "differentiation_factors": {}, "vulnerability_analysis": {}}
    
    def _market_positioning_analysis(self, html_content, url, content_sections):
        """Analyze market positioning and pricing strategy"""
        context = f"""
        PRICING INDICATORS: {' | '.join(content_sections.get('pricing_indicators', [])[:8])}
        VALUE MESSAGING: {' | '.join(content_sections.get('messaging', [])[:8])}
        COMPETITIVE CLAIMS: {' | '.join(content_sections.get('competitive_claims', [])[:5])}
        """
        
        messages = [
            {"role": "system", "content": "You are a market positioning expert who analyzes pricing strategy and market position from messaging and content."},
            {"role": "user", "content": f"""
            MARKET POSITIONING & PRICING INTELLIGENCE
            
            Analyze market positioning based on content:
            
            {context}
            
            Return analysis:
            
            {{
                "pricing_strategy": {{
                    "pricing_approach": "Premium/Mid-market/Value/Freemium",
                    "value_justification": "How they justify their pricing",
                    "pricing_transparency": "High/Medium/Low transparency",
                    "competitive_pricing": "Above/At/Below market pricing implied"
                }},
                "market_leadership_position": {{
                    "leadership_claims": "Leader/Challenger/Follower positioning",
                    "market_share_implications": "Large/Medium/Small player implied",
                    "innovation_leadership": "Innovation leader/follower positioning",
                    "thought_leadership": "Evidence of thought leadership"
                }},
                "target_market_size": {{
                    "market_scope": "Global/Regional/Niche market focus",
                    "customer_base_size": "Enterprise/Mid-market/SMB focus",
                    "market_maturity": "Emerging/Growth/Mature market",
                    "expansion_strategy": "Geographic/Vertical/Horizontal expansion"
                }}
            }}
            """
            }
        ]
        
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                temperature=0.1,
                max_tokens=1500
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
            print(f"     ❌ Market positioning analysis failed: {e}")
            return {"pricing_strategy": {}, "market_leadership_position": {}, "target_market_size": {}}
    
    def _enhanced_brand_health_scoring(self, html_content, url, content_sections, positioning_data):
        """Enhanced brand health scoring with sophisticated metrics"""
        
        # Calculate sophisticated scores based on actual analysis
        clarity_score = self._calculate_clarity_score(positioning_data, content_sections)
        differentiation_score = self._calculate_differentiation_score(positioning_data, content_sections)
        credibility_score = self._calculate_credibility_score(positioning_data, content_sections)
        market_fit_score = self._calculate_market_fit_score(positioning_data, content_sections)
        
        overall_score = int((clarity_score + differentiation_score + credibility_score + market_fit_score) / 4)
        
        # Determine threat level based on scores
        threat_level = self._determine_threat_level(overall_score, positioning_data)
        
        return {
            "overall_score": overall_score,
            "dimension_scores": {
                "messaging_clarity": {
                    "score": clarity_score,
                    "assessment": self._get_clarity_assessment(clarity_score),
                    "key_factors": self._get_clarity_factors(positioning_data)
                },
                "differentiation_strength": {
                    "score": differentiation_score,
                    "assessment": self._get_differentiation_assessment(differentiation_score),
                    "uniqueness_factors": self._get_uniqueness_factors(positioning_data)
                },
                "credibility_factor": {
                    "score": credibility_score,
                    "assessment": self._get_credibility_assessment(credibility_score),
                    "trust_indicators": self._get_trust_indicators(content_sections)
                },
                "market_fit": {
                    "score": market_fit_score,
                    "assessment": self._get_market_fit_assessment(market_fit_score),
                    "alignment_factors": self._get_alignment_factors(positioning_data)
                }
            },
            "competitive_threat_level": threat_level,
            "threat_rationale": self._get_threat_rationale(threat_level, overall_score, positioning_data)
        }
    
    def _calculate_clarity_score(self, positioning_data, content_sections):
        """Calculate messaging clarity score"""
        base_score = 70
        
        # Boost for clear value proposition
        if positioning_data.get('unique_value_proposition', {}).get('primary_value_driver', '') and len(positioning_data['unique_value_proposition']['primary_value_driver']) > 20:
            base_score += 15
        
        # Boost for specific positioning
        if positioning_data.get('positioning_strength', {}).get('clarity_score', 0) > 80:
            base_score += 10
        
        # Reduce for generic messaging
        hero_content = ' '.join(content_sections.get('hero', []))
        if any(generic in hero_content.lower() for generic in ['leading', 'innovative', 'solutions', 'global']):
            base_score -= 5
        
        return min(100, max(0, base_score))
    
    def _calculate_differentiation_score(self, positioning_data, content_sections):
        """Calculate differentiation strength score"""
        base_score = 65
        
        # Boost for unique positioning
        uniqueness = positioning_data.get('positioning_strength', {}).get('uniqueness_score', 0)
        base_score += int(uniqueness * 0.3)
        
        # Boost for specific competitive advantages
        advantages = positioning_data.get('competitive_strategy', {}).get('competitive_advantages_claimed', [])
        base_score += len(advantages) * 3
        
        # Boost for innovation focus
        innovation_level = positioning_data.get('innovation_positioning', {}).get('technology_sophistication', '')
        if innovation_level == 'Leading-edge':
            base_score += 15
        elif innovation_level == 'Competitive':
            base_score += 8
        
        return min(100, max(0, base_score))
    
    def _calculate_credibility_score(self, positioning_data, content_sections):
        """Calculate credibility score"""
        base_score = 75
        
        # Boost for credibility assessment
        credibility = positioning_data.get('unique_value_proposition', {}).get('credibility_assessment', '')
        if credibility == 'High':
            base_score += 15
        elif credibility == 'Medium':
            base_score += 8
        
        # Boost for evidence provided
        evidence = positioning_data.get('unique_value_proposition', {}).get('supporting_evidence', [])
        base_score += len(evidence) * 3
        
        # Boost for specific claims vs generic
        claims = positioning_data.get('competitive_strategy', {}).get('competitive_advantages_claimed', [])
        specific_claims = [c for c in claims if len(c) > 20 and not any(g in c.lower() for g in ['leading', 'best', 'innovative'])]
        base_score += len(specific_claims) * 5
        
        return min(100, max(0, base_score))
    
    def _calculate_market_fit_score(self, positioning_data, content_sections):
        """Calculate market fit score"""
        base_score = 72
        
        # Boost for clear market focus
        market_focus = positioning_data.get('market_focus', {})
        if market_focus.get('primary_market_segment') and len(market_focus['primary_market_segment']) > 10:
            base_score += 10
        
        # Boost for industry specialization
        if market_focus.get('industry_specialization') and market_focus['industry_specialization'] != 'General':
            base_score += 8
        
        # Boost for clear customer size focus
        if market_focus.get('customer_size_focus') and market_focus['customer_size_focus'] != 'All':
            base_score += 5
        
        return min(100, max(0, base_score))
    
    def _determine_threat_level(self, overall_score, positioning_data):
        """Determine competitive threat level"""
        if overall_score >= 85:
            return "High"
        elif overall_score >= 70:
            return "Medium"
        else:
            return "Low"
    
    def _get_threat_rationale(self, threat_level, score, positioning_data):
        """Get rationale for threat level"""
        strategy = positioning_data.get('competitive_strategy', {}).get('positioning_approach', '')
        innovation = positioning_data.get('innovation_positioning', {}).get('technology_sophistication', '')
        
        if threat_level == "High":
            return f"Strong market position ({score}/100) with {strategy.lower()} strategy and {innovation.lower()} technology"
        elif threat_level == "Medium":
            return f"Solid competitive position ({score}/100) with established {strategy.lower()} positioning"
        else:
            return f"Limited competitive threat ({score}/100) with {strategy.lower()} market position"
    
    # Helper methods for assessments
    def _get_clarity_assessment(self, score):
        if score >= 85: return "Exceptionally clear value proposition"
        elif score >= 70: return "Clear messaging with minor gaps"
        else: return "Needs messaging clarity improvement"
    
    def _get_differentiation_assessment(self, score):
        if score >= 85: return "Highly differentiated positioning"
        elif score >= 70: return "Moderately differentiated"
        else: return "Limited differentiation from competitors"
    
    def _get_credibility_assessment(self, score):
        if score >= 85: return "Highly credible claims with strong evidence"
        elif score >= 70: return "Generally credible with some supporting evidence"
        else: return "Claims need stronger substantiation"
    
    def _get_market_fit_assessment(self, score):
        if score >= 85: return "Excellent target market alignment"
        elif score >= 70: return "Good market fit with clear focus"
        else: return "Market focus could be sharper"
    
    def _get_clarity_factors(self, positioning_data):
        factors = []
        if positioning_data.get('unique_value_proposition', {}).get('primary_value_driver'):
            factors.append("Clear value driver identified")
        if positioning_data.get('positioning_strength', {}).get('clarity_score', 0) > 80:
            factors.append("High positioning clarity")
        return factors[:3]
    
    def _get_uniqueness_factors(self, positioning_data):
        advantages = positioning_data.get('competitive_strategy', {}).get('competitive_advantages_claimed', [])
        return advantages[:3] if advantages else ["Generic positioning"]
    
    def _get_trust_indicators(self, content_sections):
        indicators = []
        if content_sections.get('about'):
            indicators.append("Company information provided")
        if content_sections.get('competitive_claims'):
            indicators.append("Specific claims made")
        return indicators[:3]
    
    def _get_alignment_factors(self, positioning_data):
        factors = []
        market_focus = positioning_data.get('market_focus', {})
        if market_focus.get('primary_market_segment'):
            factors.append(f"Targets {market_focus['primary_market_segment']}")
        if market_focus.get('customer_size_focus'):
            factors.append(f"Focuses on {market_focus['customer_size_focus']}")
        return factors[:3]
    
    # Data extraction methods (similar to previous version)
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
    
    # Default fallback methods
    def _get_default_enhanced_positioning(self):
        return {
            "company_name": "Unknown Company",
            "unique_value_proposition": {
                "primary_value_driver": "Quality solutions and services",
                "differentiation_claim": "Professional expertise and reliability",
                "credibility_assessment": "Medium",
                "supporting_evidence": ["Established presence", "Professional website"]
            },
            "competitive_strategy": {
                "positioning_approach": "Follower",
                "competitive_advantages_claimed": ["Quality", "Service"],
                "defensive_positioning": "Established relationships"
            },
            "market_focus": {
                "primary_market_segment": "Business professionals",
                "industry_specialization": "General business",
                "customer_size_focus": "All",
                "geographic_focus": "Regional"
            },
            "positioning_strength": {
                "clarity_score": 70,
                "uniqueness_score": 60,
                "credibility_score": 75,
                "memorability_score": 65
            }
        }
    
    def _get_default_swot(self):
        return {
            "strengths": [{"strength": "Established market presence", "evidence": "Professional website", "sustainability": "Medium"}],
            "weaknesses": [{"weakness": "Generic positioning", "evidence": "Standard messaging", "urgency": "Medium"}],
            "opportunities": [{"opportunity": "Digital transformation", "market_evidence": "Growing digital adoption", "revenue_potential": "Medium"}],
            "threats": [{"threat": "Increased competition", "likelihood": "Medium", "impact_severity": "Medium"}]
        }
    
    def _get_default_audience(self):
        return {
            "primary_audience": {
                "demographic_specifics": {
                    "job_functions": ["Management", "Operations"],
                    "seniority_level": "Manager",
                    "company_size": "Mid-market (100-1000)",
                    "technical_sophistication": "Medium"
                },
                "pain_point_analysis": {
                    "primary_pain_points": ["Efficiency", "Cost management"],
                    "urgency_level": "Medium"
                }
            }
        }
    
    def generate_enhanced_competitive_insights(self):
        """Generate enhanced cross-brand competitive intelligence"""
        if len(self.brand_profiles) < 2:
            return {}
        
        # Compile sophisticated brand comparison data
        brand_comparison = []
        for brand in self.brand_profiles:
            brand_summary = {
                "name": brand['company_name'],
                "positioning_approach": brand['enhanced_positioning']['competitive_strategy']['positioning_approach'],
                "unique_value": brand['enhanced_positioning']['unique_value_proposition']['primary_value_driver'],
                "market_focus": brand['enhanced_positioning']['market_focus']['primary_market_segment'],
                "innovation_level": brand['enhanced_positioning']['innovation_positioning']['technology_sophistication'],
                "threat_level": brand['enhanced_brand_health']['competitive_threat_level'],
                "overall_score": brand['enhanced_brand_health']['overall_score'],
                "claimed_advantages": brand.get('competitive_advantage', {}).get('claimed_advantages', [])
            }
            brand_comparison.append(brand_summary)
        
        analysis_context = f"""
        COMPETITIVE LANDSCAPE ANALYSIS:
        {json.dumps(brand_comparison, indent=2)}
        """
        
        messages = [
            {"role": "system", "content": "You are a senior competitive strategy consultant analyzing market dynamics and competitive positioning across multiple brands."},
            {"role": "user", "content": f"""
            SOPHISTICATED COMPETITIVE INTELLIGENCE ANALYSIS
            
            Analyze this competitive landscape and provide strategic insights:
            
            {analysis_context}
            
            Return detailed competitive intelligence:
            
            {{
                "market_dynamics": {{
                    "competitive_intensity": "Low/Medium/High",
                    "market_maturity": "Emerging/Growth/Mature/Declining",
                    "innovation_pace": "Slow/Moderate/Fast",
                    "differentiation_difficulty": "Easy/Moderate/Difficult",
                    "market_consolidation": "Fragmented/Consolidating/Concentrated"
                }},
                "positioning_analysis": {{
                    "positioning_clusters": [
                        {{
                            "cluster_name": "Similar positioning group",
                            "brands": ["Brand", "names", "in", "cluster"],
                            "shared_characteristics": "What makes them similar"
                        }}
                    ],
                    "white_space_opportunities": [
                        {{
                            "opportunity": "Unclaimed positioning territory",
                            "rationale": "Why this is an opportunity",
                            "difficulty": "Easy/Moderate/Difficult to claim",
                            "market_size": "Large/Medium/Small opportunity"
                        }}
                    ],
                    "positioning_strengths": {{
                        "strongest_positions": ["Brands", "with", "strongest", "positioning"],
                        "most_vulnerable": ["Brands", "with", "weak", "positioning"],
                        "most_differentiated": ["Most", "unique", "positioning"]
                    }}
                }},
                "competitive_threats": [
                    {{
                        "brand": "Brand name",
                        "threat_level": "High/Medium/Low",
                        "threat_sources": ["Specific", "competitive", "advantages"],
                        "defensive_strategies": ["How", "to", "defend", "against"],
                        "attack_vectors": ["Where", "they", "are", "vulnerable"]
                    }}
                ],
                "market_entry_strategy": {{
                    "optimal_positioning": "Best positioning for new entrant",
                    "target_segment": "Most attractive underserved segment",
                    "differentiation_strategy": "How to differentiate effectively",
                    "competitive_response": "How existing players would respond",
                    "barriers_to_entry": ["Key", "barriers", "new", "entrants", "face"]
                }},
                "strategic_recommendations": [
                    "Specific strategic insights for market participants"
                ]
            }}
            
            Provide sophisticated analysis based on actual brand positioning data.
            """
            }
        ]
        
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                temperature=0.1,
                max_tokens=3000
            )
            
            content = response.choices[0].message.content.strip()
            content = re.sub(r"```(json)?", "", content).strip()
            
            if '{' in content:
                start = content.find('{')
                end = content.rfind('}') + 1
                json_content = content[start:end]
                return json.loads(json_content)
                
        except Exception as e:
            print(f"     ❌ Enhanced competitive insights failed: {e}")
        
        return {}
    
    def generate_enhanced_ai_report(self, urls, report_title="Enhanced AI Competitive Intelligence", output_filename=None):
        """Generate enhanced AI-powered competitive intelligence with sophisticated insights"""
        
        if not output_filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_filename = f"enhanced_ai_competitive_intelligence_{timestamp}.html"
        
        print(f"🤖 Generating Enhanced AI-Powered Competitive Intelligence...")
        print(f"📊 Deep analysis of {len(urls)} brands with sophisticated AI insights...")
        
        # Analyze all brands with enhanced AI
        self.brand_profiles = []
        seen_companies = set()
        
        try:
            for i, url in enumerate(urls, 1):
                print(f"\n🔍 [{i}/{len(urls)}] Enhanced AI Analysis: {url}")
                try:
                    profile = self.extract_enhanced_brand_data(url)
                    if profile:
                        company_name = profile['company_name']
                        if company_name not in seen_companies:
                            self.brand_profiles.append(profile)
                            seen_companies.add(company_name)
                            print(f"✅ Enhanced analysis complete: {company_name}")
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
        
        # Generate enhanced competitive insights
        print(f"\n🧠 Generating sophisticated competitive intelligence...")
        self.competitive_insights = self.generate_enhanced_competitive_insights()
        
        # Generate enhanced presentation
        print(f"\n📄 Creating enhanced 16:9 presentation with visual grid...")
        html_content = self._generate_enhanced_presentation(report_title)
        
        # Save report
        try:
            with open(output_filename, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            print(f"\n🎉 ENHANCED AI REPORT GENERATED!")
            print(f"📁 File: {output_filename}")
            print(f"📊 Brands analyzed: {len(self.brand_profiles)}")
            print(f"📄 Format: Enhanced 16:9 slides with visual grid overview")
            print(f"🤖 Advanced AI: Sophisticated positioning, SWOT, market intelligence")
            print(f"🌐 Interactive navigation with comprehensive competitive insights")
            
            return output_filename
            
        except Exception as e:
            print(f"❌ Error saving report: {e}")
            return None


def main():
    """Generate enhanced AI-powered competitive intelligence presentation"""
    
    medical_urls = [
        "https://www.wolterskluwer.com",
        "https://www.elsevier.com",
        "https://www.clinicalkey.com",
        "https://www.openevidence.com"
    ]
    
    generator = EnhancedAICompetitiveIntelligence()
    
    output_file = generator.generate_enhanced_ai_report(
        urls=medical_urls,
        report_title="Medical AI Platform Competitive Intelligence",
        output_filename="enhanced_ai_competitive_slides.html"
    )
    
    if output_file:
        print(f"\n🎉 ENHANCED AI PRESENTATION COMPLETE!")
        print(f"📁 File location: {os.path.abspath(output_file)}")
        print(f"🎪 Format: Enhanced 16:9 slides with visual grid and sophisticated AI")
        print(f"🤖 Features: Deep positioning analysis, sophisticated SWOT, market intelligence")
        print(f"🌐 Navigation: Arrow keys, click dots, or arrow buttons")

if __name__ == "__main__":
    main()