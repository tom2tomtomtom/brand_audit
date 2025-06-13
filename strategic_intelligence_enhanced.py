"""
Enhanced Strategic Intelligence Analysis Methods
Improves brand story generation and analysis quality
"""

import openai
import re
from collections import defaultdict

class EnhancedAnalysisMethods:
    """Enhanced methods for more sophisticated analysis"""
    
    def _generate_enhanced_brand_story(self, brand, external_research=True):
        """Generate sophisticated brand story with external research"""
        try:
            # Extract comprehensive content
            hero_content = ' '.join(brand.get('comprehensive_content', {}).get('hero_sections', [])[:3])
            about_content = ' '.join(brand.get('comprehensive_content', {}).get('about_content', [])[:3])
            value_props = ' '.join(brand.get('comprehensive_content', {}).get('value_propositions', [])[:5])
            mission = brand.get('comprehensive_content', {}).get('mission_statements', [])
            vision = brand.get('comprehensive_content', {}).get('vision_statements', [])
            
            # Extract actual quotes and specific language
            quotes = self._extract_quotes(hero_content + about_content)
            specific_terms = self._extract_industry_terms(hero_content + about_content + ' '.join(value_props))
            
            # First, get external context about the company
            if external_research:
                external_context = self._get_external_company_context(brand['company_name'], brand['url'])
            else:
                external_context = ""
            
            story_prompt = f"""
Analyze {brand['company_name']} and create a sophisticated, unique brand narrative.

DIRECT QUOTES FROM THEIR WEBSITE:
{chr(10).join(quotes[:5])}

THEIR ACTUAL VALUE PROPOSITIONS:
{chr(10).join(value_props[:5])}

MISSION/VISION STATEMENTS:
{chr(10).join(mission[:2] + vision[:2])}

INDUSTRY-SPECIFIC TERMS THEY USE:
{', '.join(specific_terms[:10])}

EXTERNAL CONTEXT:
{external_context}

TASK: Create a 2-3 sentence brand story that:

1. MUST be completely unique to {brand['company_name']} - no generic phrases
2. MUST incorporate their actual language and terminology
3. MUST reflect their specific market position and differentiation
4. MUST avoid clichés like "beacon of", "pioneering", "leading the way", "transforming"
5. MUST be grounded in their actual business model and customer value

FORBIDDEN PHRASES:
- "beacon of innovation/excellence"
- "pioneering solutions"
- "leading the way"
- "transforming the industry"
- "cutting-edge technology"
- "state-of-the-art"
- Any generic corporate speak

Instead, use:
- Their specific technology/methodology names
- Their actual customer outcomes
- Their unique approach or philosophy
- Their measurable impact
- Their distinctive market position

Write as a brand strategist who deeply understands this specific company.
"""
            
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert brand strategist who creates highly specific, differentiated brand narratives based on deep company analysis. You never use generic corporate language."},
                    {"role": "user", "content": story_prompt}
                ],
                temperature=0.7,  # Higher creativity
                max_tokens=250
            )
            
            return response["choices"][0]["message"]["content"].strip()
            
        except Exception as e:
            print(f"Enhanced brand story generation failed: {e}")
            return self._generate_fallback_brand_story(brand)
    
    def _get_external_company_context(self, company_name, url):
        """Get additional context about the company using AI"""
        try:
            research_prompt = f"""
Provide specific, factual information about {company_name} ({url}):

1. Their actual market position and key differentiators
2. Notable clients or partnerships (if publicly known)
3. Specific technologies or methodologies they're known for
4. Recent achievements or milestones
5. Their unique approach compared to competitors

Provide only verifiable, specific facts. If unsure, don't include.
Keep response under 150 words.
"""
            
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a market research analyst providing factual company intelligence."},
                    {"role": "user", "content": research_prompt}
                ],
                temperature=0.3,
                max_tokens=200
            )
            
            return response["choices"][0]["message"]["content"].strip()
            
        except:
            return ""
    
    def _extract_quotes(self, text):
        """Extract actual quotes and key phrases"""
        # Look for quoted text
        quotes = re.findall(r'"([^"]+)"', text)
        
        # Also extract strong statements (sentences with action verbs)
        sentences = text.split('.')
        strong_statements = []
        action_verbs = ['deliver', 'enable', 'provide', 'create', 'build', 'develop', 'transform', 'accelerate', 'optimize']
        
        for sentence in sentences:
            if any(verb in sentence.lower() for verb in action_verbs) and len(sentence) > 20:
                strong_statements.append(sentence.strip())
        
        return quotes + strong_statements[:3]
    
    def _extract_industry_terms(self, text):
        """Extract industry-specific terminology"""
        # Remove common words
        common_words = set(['the', 'and', 'for', 'with', 'that', 'this', 'from', 'your', 'our', 'are', 'can', 'will', 'all', 'more', 'how', 'what', 'when', 'where', 'who'])
        
        # Find capitalized terms and technical words
        words = re.findall(r'\b[A-Z][a-z]+\b|\b[A-Z]{2,}\b|\b\w+(?:tion|ment|ance|ence|ity|ics|ware|tech|data|cloud|AI|ML)\b', text)
        
        # Filter and deduplicate
        industry_terms = []
        seen = set()
        for word in words:
            if word.lower() not in common_words and word not in seen and len(word) > 3:
                industry_terms.append(word)
                seen.add(word)
        
        return industry_terms
    
    def _generate_enhanced_strategic_insights(self, brand_data, competitors):
        """Generate more specific, actionable strategic insights"""
        
        # Analyze specific competitive gaps
        competitive_gaps = self._analyze_competitive_gaps(brand_data, competitors)
        
        # Identify unique strengths
        unique_strengths = self._identify_unique_strengths(brand_data, competitors)
        
        insights_prompt = f"""
Provide highly specific strategic insights for {brand_data['company_name']}.

THEIR UNIQUE STRENGTHS VS COMPETITORS:
{chr(10).join(unique_strengths)}

COMPETITIVE GAPS IDENTIFIED:
{chr(10).join(competitive_gaps)}

SPECIFIC COMPETITOR THREATS:
{self._format_competitor_threats(brand_data, competitors)}

Generate 5 SPECIFIC, ACTIONABLE strategic recommendations:

1. Each must reference specific competitors and their weaknesses
2. Each must leverage identified unique strengths
3. Each must include concrete tactics (not generic strategy)
4. Each must have measurable outcomes
5. Each must be implementable within 6-12 months

Format each as:
**[Specific Action]**: [Detailed tactic addressing specific competitor weakness] → [Measurable outcome]

Avoid generic recommendations. Be specific about:
- Which competitor vulnerability to exploit
- Which product/feature to develop
- Which market segment to target
- Which partnership to pursue
- Which message to emphasize

Base everything on actual competitive intelligence gathered.
"""
        
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a senior McKinsey strategy consultant providing specific, actionable competitive intelligence."},
                {"role": "user", "content": insights_prompt}
            ],
            temperature=0.4,
            max_tokens=800
        )
        
        return response["choices"][0]["message"]["content"]
    
    def _analyze_competitive_gaps(self, brand_data, competitors):
        """Identify specific gaps in competitive offerings"""
        gaps = []
        
        # Analyze product gaps
        brand_products = set(brand_data['product_portfolio']['main_products'])
        for comp in competitors:
            comp_products = set(comp['product_portfolio']['main_products'])
            unique_products = brand_products - comp_products
            if unique_products:
                gaps.append(f"{comp['company_name']} lacks: {', '.join(list(unique_products)[:2])}")
        
        # Analyze messaging gaps
        brand_values = set(brand_data['comprehensive_content']['value_propositions'])
        for comp in competitors:
            comp_values = set(comp['comprehensive_content']['value_propositions'])
            unique_values = brand_values - comp_values
            if unique_values:
                gaps.append(f"{comp['company_name']} doesn't emphasize: {list(unique_values)[0][:50]}...")
        
        return gaps[:5]
    
    def _identify_unique_strengths(self, brand_data, competitors):
        """Identify what makes this brand unique"""
        strengths = []
        
        # Unique products
        all_competitor_products = set()
        for comp in competitors:
            all_competitor_products.update(comp['product_portfolio']['main_products'])
        
        unique_products = set(brand_data['product_portfolio']['main_products']) - all_competitor_products
        if unique_products:
            strengths.append(f"Exclusive offerings: {', '.join(list(unique_products)[:3])}")
        
        # Unique positioning
        brand_terms = self._extract_industry_terms(' '.join(brand_data['comprehensive_content']['hero_sections']))
        competitor_terms = set()
        for comp in competitors:
            competitor_terms.update(self._extract_industry_terms(' '.join(comp['comprehensive_content']['hero_sections'])))
        
        unique_terms = set(brand_terms) - competitor_terms
        if unique_terms:
            strengths.append(f"Unique positioning around: {', '.join(list(unique_terms)[:3])}")
        
        return strengths
    
    def _format_competitor_threats(self, brand_data, competitors):
        """Format specific competitor threats"""
        threats = []
        for comp in competitors[:3]:  # Top 3 competitors
            threat = f"{comp['company_name']}: Strong in {comp['product_portfolio']['main_products'][0] if comp['product_portfolio']['main_products'] else 'core offering'}"
            threats.append(threat)
        return '\n'.join(threats)
    
    def _generate_fallback_brand_story(self, brand):
        """Generate specific fallback story based on scraped content"""
        # Use actual scraped content to create specific story
        products = brand['product_portfolio']['main_products'][:2]
        values = brand['comprehensive_content']['value_propositions'][:2]
        
        if products and values:
            return f"{brand['company_name']} specializes in {' and '.join(products)}, focused on {values[0].lower()}. Their approach centers on {values[1].lower() if len(values) > 1 else 'delivering measurable value to clients'}."
        else:
            return f"{brand['company_name']} delivers specialized solutions tailored to their market segment, with a focus on practical outcomes and client success."


# Integration example for the main class:
"""
To integrate these enhanced methods into your StrategicCompetitiveIntelligence class:

1. Replace _generate_brand_story with _generate_enhanced_brand_story
2. Add the helper methods (_extract_quotes, _extract_industry_terms, etc.)
3. Update generate_strategic_brand_analysis to use _generate_enhanced_strategic_insights
4. Add external research capability as an option

This will produce:
- More unique, specific brand stories without generic language
- Deeper competitive insights based on actual gaps
- Actionable recommendations tied to specific competitors
- Better use of scraped content in analysis
"""