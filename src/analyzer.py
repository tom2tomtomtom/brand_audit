"""
Brand Analyzer Module
Uses OpenAI GPT-4 to analyze scraped brand data and generate insights
"""

import os
import time
import logging
import openai
import json
from typing import Dict, List, Any

logger = logging.getLogger(__name__)

class BrandAnalyzer:
    def __init__(self):
        """Initialize the Brand Analyzer with OpenAI configuration"""
        self.client = None
        self.setup_openai()
    
    def setup_openai(self):
        """Setup OpenAI client"""
        try:
            api_key = os.getenv('OPENAI_API_KEY')
            if not api_key or api_key == 'your_openai_api_key_here':
                logger.error("No valid OpenAI API key found. Analysis cannot proceed.")
                return
            
            self.client = openai.OpenAI(api_key=api_key)
            logger.info("OpenAI client initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize OpenAI client: {str(e)}")
    
    def analyze_brand(self, brand_data: Dict) -> Dict:
        """Analyze a single brand's scraped data"""
        logger.info(f"Starting analysis for {brand_data['name']}")
        
        try:
            # Prepare analysis data
            analysis_input = self.prepare_analysis_input(brand_data)
            
            # Try AI analysis first
            if self.client:
                try:
                    ai_analysis = self.perform_ai_analysis(analysis_input)
                    if ai_analysis:
                        logger.info(f"AI analysis completed for {brand_data['name']}")
                        return ai_analysis
                except Exception as e:
                    logger.warning(f"AI analysis failed for {brand_data['name']}: {str(e)}")
            
            # Require real AI analysis or fail
            logger.error(f"AI analysis failed for {brand_data['name']}: No OpenAI API key provided")
            raise Exception("Analysis requires OpenAI API key - no fallback data generation allowed")
            
        except Exception as e:
            logger.error(f"Error analyzing {brand_data['name']}: {str(e)}")
            raise Exception(f"Brand analysis failed: {str(e)}")
    
    def prepare_analysis_input(self, brand_data: Dict) -> Dict:
        """Prepare data for analysis"""
        # Combine all page content
        all_content = ""
        all_headings = []
        
        for page in brand_data.get('pages_scraped', []):
            if page.get('content'):
                all_content += " " + page['content']
            if page.get('headings'):
                all_headings.extend([h['text'] for h in page['headings']])
        
        return {
            'brand_name': brand_data['name'],
            'url': brand_data['url'],
            'content': all_content[:4000],  # Limit content for API
            'headings': all_headings[:20],
            'visual_assets': brand_data.get('visual_assets', {}),
            'content_analysis': brand_data.get('content_analysis', {}),
            'technical_info': brand_data.get('technical_info', {}),
            'recent_content': brand_data.get('recent_content', [])
        }
    
    def perform_ai_analysis(self, analysis_input: Dict) -> Dict:
        """Perform AI-powered brand analysis using GPT-4"""
        try:
            # Create comprehensive prompt
            prompt = self.create_analysis_prompt(analysis_input)
            
            # Call OpenAI API
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a professional brand strategist and competitive analyst. Provide comprehensive, actionable brand analysis in valid JSON format."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=2500,
                temperature=0.7
            )
            
            # Parse response
            ai_response = response.choices[0].message.content
            
            # Clean and parse JSON
            json_start = ai_response.find('{')
            json_end = ai_response.rfind('}') + 1
            
            if json_start != -1 and json_end > json_start:
                json_content = ai_response[json_start:json_end]
                analysis_result = json.loads(json_content)
                
                # Add metadata
                analysis_result['analysis_method'] = 'ai'
                analysis_result['analyzed_at'] = time.strftime('%Y-%m-%d %H:%M:%S')
                
                return analysis_result
            else:
                raise ValueError("No valid JSON found in AI response")
                
        except Exception as e:
            logger.error(f"AI analysis failed: {str(e)}")
            raise
    
    def create_analysis_prompt(self, analysis_input: Dict) -> str:
        """Create a comprehensive analysis prompt for GPT-4"""
        
        prompt = f"""
Analyze this brand comprehensively and provide detailed insights in JSON format:

BRAND INFORMATION:
- Brand Name: {analysis_input['brand_name']}
- Website: {analysis_input['url']}

CONTENT SAMPLE:
{analysis_input['content'][:2000]}

KEY HEADINGS:
{', '.join(analysis_input['headings'][:10])}

VISUAL ASSETS:
- Logo: {analysis_input['visual_assets'].get('logo', 'Not found')}
- Brand Colors: {', '.join(analysis_input['visual_assets'].get('brand_colors', [])[:5])}
- Fonts: {', '.join(analysis_input['visual_assets'].get('font_families', [])[:3])}

TECHNICAL INFO:
- SSL Enabled: {analysis_input['technical_info'].get('ssl_enabled', 'Unknown')}
- Mobile Responsive: {analysis_input['technical_info'].get('mobile_responsive', 'Unknown')}
- Technologies: {', '.join(analysis_input['technical_info'].get('technology_stack', []))}

CONTENT STATISTICS:
- Total Words: {analysis_input['content_analysis'].get('total_words', 0)}
- Pages Analyzed: {analysis_input['content_analysis'].get('total_pages', 0)}
- Industry Keywords: {analysis_input['content_analysis'].get('industry_keywords', {})}

Please provide a comprehensive JSON response with these exact fields:

{{
  "brand_name": "{analysis_input['brand_name']}",
  "industry": "Specific industry category",
  "business_model": "B2B/B2C/B2B2C/Marketplace",
  "company_size": "Startup/SME/Enterprise/Corporation",
  "market_position": "Leader/Challenger/Follower/Niche",
  
  "brand_identity": {{
    "brand_personality": "Key personality traits",
    "brand_voice": "Communication style and tone",
    "value_proposition": "Core value proposition",
    "target_audience": "Primary target customers",
    "positioning_statement": "Brand positioning in market"
  }},
  
  "digital_presence": {{
    "website_quality": "Score 1-10 with explanation",
    "user_experience": "Score 1-10 with explanation", 
    "content_quality": "Score 1-10 with explanation",
    "seo_optimization": "Score 1-10 with explanation",
    "mobile_experience": "Score 1-10 with explanation"
  }},
  
  "competitive_analysis": {{
    "key_strengths": ["5 specific competitive strengths"],
    "key_weaknesses": ["4 areas needing improvement"],
    "opportunities": ["3 market opportunities"],
    "threats": ["2 competitive threats"],
    "differentiation": "How this brand differentiates from competitors"
  }},
  
  "strategic_recommendations": {{
    "immediate_priorities": ["3 immediate action items"],
    "medium_term_goals": ["3 goals for next 6-12 months"], 
    "long_term_vision": ["2 strategic long-term objectives"],
    "investment_areas": ["Areas requiring investment/focus"]
  }},
  
  "content_insights": {{
    "content_themes": ["Main content themes identified"],
    "messaging_consistency": "Assessment of message consistency",
    "thought_leadership": "Evidence of thought leadership",
    "customer_focus": "How customer-centric the content is"
  }},
  
  "technical_assessment": {{
    "website_performance": "Performance assessment",
    "security_features": "Security implementation",
    "modern_standards": "Adherence to modern web standards",
    "accessibility": "Accessibility considerations"
  }},
  
  "overall_score": {{
    "total_score": "Overall score out of 100",
    "score_breakdown": {{
      "brand_clarity": "Score out of 20",
      "digital_execution": "Score out of 20", 
      "content_quality": "Score out of 20",
      "user_experience": "Score out of 20",
      "competitive_position": "Score out of 20"
    }}
  }}
}}

Make your analysis specific, actionable, and based on the actual content provided. Avoid generic statements.
"""
        
        return prompt
    
    
    def generate_comparative_analysis(self, brand_analyses: List[Dict]) -> Dict:
        """Generate comparative analysis across all analyzed brands"""
        logger.info(f"Generating comparative analysis for {len(brand_analyses)} brands")
        
        try:
            if not brand_analyses:
                return {}
            
            # Extract key metrics for comparison
            comparison_data = {
                'brand_count': len(brand_analyses),
                'industries_represented': [],
                'business_models': [],
                'company_sizes': [],
                'average_scores': {},
                'top_performers': {},
                'common_strengths': [],
                'common_weaknesses': [],
                'market_insights': {}
            }
            
            # Collect data from all brands
            all_scores = []
            all_strengths = []
            all_weaknesses = []
            
            for analysis in brand_analyses:
                # Collect industries and business models
                comparison_data['industries_represented'].append(analysis.get('industry', 'Unknown'))
                comparison_data['business_models'].append(analysis.get('business_model', 'Unknown'))
                comparison_data['company_sizes'].append(analysis.get('company_size', 'Unknown'))
                
                # Collect scores
                overall_score = analysis.get('overall_score', {})
                if overall_score.get('total_score'):
                    score_value = int(overall_score['total_score'].split('/')[0])
                    all_scores.append(score_value)
                
                # Collect strengths and weaknesses
                competitive = analysis.get('competitive_analysis', {})
                all_strengths.extend(competitive.get('key_strengths', []))
                all_weaknesses.extend(competitive.get('key_weaknesses', []))
            
            # Calculate averages and insights
            if all_scores:
                comparison_data['average_scores']['overall'] = sum(all_scores) / len(all_scores)
                comparison_data['average_scores']['highest'] = max(all_scores)
                comparison_data['average_scores']['lowest'] = min(all_scores)
            
            # Find common patterns
            comparison_data['common_strengths'] = self.find_common_themes(all_strengths)[:5]
            comparison_data['common_weaknesses'] = self.find_common_themes(all_weaknesses)[:5]
            
            # Generate market insights
            comparison_data['market_insights'] = self.generate_market_insights(brand_analyses)
            
            # Identify top performers in different categories
            comparison_data['top_performers'] = self.identify_top_performers(brand_analyses)
            
            return comparison_data
            
        except Exception as e:
            logger.error(f"Error in comparative analysis: {str(e)}")
            return {'error': str(e)}
    
    def find_common_themes(self, items: List[str]) -> List[str]:
        """Find common themes in a list of items"""
        from collections import Counter
        
        # Count word frequency across all items
        all_words = []
        for item in items:
            words = item.lower().split()
            all_words.extend([word for word in words if len(word) > 3])
        
        word_counts = Counter(all_words)
        return [word for word, count in word_counts.most_common(10) if count > 1]
    
    def generate_market_insights(self, brand_analyses: List[Dict]) -> Dict:
        """Generate market-level insights from brand analyses"""
        insights = {
            'industry_trends': [],
            'competitive_landscape': '',
            'market_opportunities': [],
            'technology_adoption': []
        }
        
        # Analyze industry distribution
        industries = [analysis.get('industry', '') for analysis in brand_analyses]
        industry_counts = {industry: industries.count(industry) for industry in set(industries)}
        
        if industry_counts:
            dominant_industry = max(industry_counts, key=industry_counts.get)
            insights['competitive_landscape'] = f"Market dominated by {dominant_industry} sector"
        
        # Technology trends
        tech_indicators = []
        for analysis in brand_analyses:
            tech_assessment = analysis.get('technical_assessment', {})
            if tech_assessment:
                tech_indicators.append(tech_assessment)
        
        insights['technology_adoption'] = ["Modern web standards adoption", "Mobile-first approaches"]
        
        return insights
    
    def identify_top_performers(self, brand_analyses: List[Dict]) -> Dict:
        """Identify top performing brands in different categories"""
        top_performers = {}
        
        try:
            # Find highest overall score
            highest_score = 0
            top_overall = None
            
            for analysis in brand_analyses:
                overall_score = analysis.get('overall_score', {})
                if overall_score.get('total_score'):
                    score_value = int(overall_score['total_score'].split('/')[0])
                    if score_value > highest_score:
                        highest_score = score_value
                        top_overall = analysis.get('brand_name', 'Unknown')
            
            if top_overall:
                top_performers['overall_leader'] = top_overall
                top_performers['overall_score'] = highest_score
            
            return top_performers
            
        except Exception as e:
            logger.error(f"Error identifying top performers: {str(e)}")
            return {}
    
