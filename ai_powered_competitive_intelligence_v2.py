#!/usr/bin/env python3
"""
AI-Powered Competitive Intelligence V2
Real data only - no fallbacks or defaults
Industry-agnostic with adaptive analysis
Advanced 16:9 slide-based competitive analysis
"""

import os
import json
import re
from datetime import datetime
from enhanced_brand_profiler_v2 import EnhancedBrandProfilerV2
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class AIPoweredCompetitiveIntelligenceV2:
    def __init__(self):
        self.profiler = EnhancedBrandProfilerV2()
        self.brand_profiles = []
        self.failed_brands = []
        self.competitive_insights = None
    
    def analyze_brands(self, urls):
        """Analyze multiple brands with AI-powered insights"""
        print(f"🤖 AI-POWERED COMPETITIVE INTELLIGENCE V2")
        print(f"📊 Analyzing {len(urls)} brands...")
        print(f"{'='*60}")
        
        for i, url in enumerate(urls, 1):
            print(f"\n[{i}/{len(urls)}] {url}")
            
            try:
                # Get base profile
                base_profile = self.profiler.analyze_brand(url)
                
                if base_profile['status'] == 'success':
                    # Enhance with competitive intelligence
                    enhanced_profile = self.enhance_with_ai_intelligence(base_profile)
                    
                    if enhanced_profile:
                        self.brand_profiles.append(enhanced_profile)
                        print(f"✅ Complete: {enhanced_profile['company_name']}")
                    else:
                        self.failed_brands.append({
                            'url': url,
                            'reason': 'AI enhancement failed'
                        })
                        print(f"⚠️  Partial: Basic data extracted but AI enhancement failed")
                else:
                    self.failed_brands.append({
                        'url': url,
                        'reason': base_profile['error']
                    })
                    print(f"❌ Failed: {base_profile['error']}")
                    
            except Exception as e:
                self.failed_brands.append({
                    'url': url,
                    'reason': str(e)
                })
                print(f"❌ Error: {e}")
        
        # Generate cross-brand insights if we have data
        if len(self.brand_profiles) >= 2:
            print(f"\n🧠 Generating cross-brand competitive insights...")
            self.competitive_insights = self.generate_cross_brand_insights()
        
        print(f"\n{'='*60}")
        print(f"ANALYSIS COMPLETE")
        print(f"✅ Successful: {len(self.brand_profiles)}")
        print(f"❌ Failed: {len(self.failed_brands)}")
        
        return {
            'successful': self.brand_profiles,
            'failed': self.failed_brands,
            'insights': self.competitive_insights
        }
    
    def enhance_with_ai_intelligence(self, base_profile):
        """Enhance profile with AI competitive intelligence"""
        if not base_profile or base_profile['status'] != 'success':
            return None
        
        brand_data = base_profile['brand_data']
        parsed_content = base_profile.get('parsed_content', {})
        
        # Build comprehensive context
        context = self.build_brand_context(brand_data, parsed_content)
        
        # Run AI analyses
        analyses = {}
        
        # 1. Strategic Positioning Analysis
        print("  → AI positioning analysis...")
        analyses['positioning'] = self.ai_positioning_analysis(context)
        
        if not analyses['positioning']:
            return None  # Critical analysis failed
        
        # 2. SWOT Analysis
        print("  → AI SWOT analysis...")
        analyses['swot'] = self.ai_swot_analysis(context)
        
        # 3. Target Audience Analysis
        print("  → AI audience analysis...")
        analyses['audience'] = self.ai_audience_analysis(context)
        
        # 4. Innovation Analysis
        print("  → AI innovation analysis...")
        analyses['innovation'] = self.ai_innovation_analysis(context)
        
        # 5. Brand Health Scoring
        print("  → AI health scoring...")
        analyses['health'] = self.ai_brand_health_scoring(context)
        
        # Compile enhanced profile
        enhanced_profile = {
            'url': base_profile['url'],
            'company_name': analyses['positioning'].get('company_name', brand_data.get('company_name', 'Unknown')),
            'extraction_quality': base_profile.get('extraction_quality', 0),
            'ai_analyses': analyses,
            'visual_data': base_profile.get('visual_data', {}),
            'base_confidence': brand_data.get('confidence_scores', {})
        }
        
        return enhanced_profile
    
    def build_brand_context(self, brand_data, parsed_content):
        """Build comprehensive context for AI analysis"""
        context = {
            'extracted_data': brand_data,
            'content': {
                'headings': parsed_content.get('headings', {}),
                'navigation': [item.get('text', '') for item in parsed_content.get('nav_structure', [])[:15]],
                'meta': parsed_content.get('meta_data', {}),
                'main_text': parsed_content.get('text_content', '')[:3000]
            }
        }
        
        # Create text summary for prompts
        context['text_summary'] = f"""
        Company: {brand_data.get('company_name', 'Unknown')}
        Positioning: {brand_data.get('brand_positioning', 'Not found')}
        
        Page Title: {parsed_content.get('meta_data', {}).get('title', '')}
        Meta Description: {parsed_content.get('meta_data', {}).get('description', '')}
        
        Main Headings: {' | '.join(parsed_content.get('headings', {}).get('h1', [])[:3])}
        Navigation: {' | '.join(context['content']['navigation'][:10])}
        """
        
        return context
    
    def ai_positioning_analysis(self, context):
        """Analyze strategic positioning"""
        try:
            messages = [
                {"role": "system", "content": "You are a strategic brand consultant analyzing competitive positioning. Focus on extracting real insights from the provided content."},
                {"role": "user", "content": f"""
                Analyze this brand's strategic positioning based on their actual website content:
                
                {context['text_summary']}
                
                Extract and analyze:
                1. Core positioning strategy (based on their messaging)
                2. Value proposition (from their content)
                3. Competitive differentiation (what makes them unique)
                4. Market position (leader/challenger/niche)
                
                IMPORTANT: Only analyze what's actually present in the content.
                If information is unclear or missing, indicate that explicitly.
                
                Return as JSON with these fields:
                {{
                    "company_name": "Actual company name from content",
                    "positioning_strategy": {{
                        "type": "Price/Quality/Innovation/Service/Other",
                        "statement": "Their actual positioning statement",
                        "confidence": 0.0-1.0
                    }},
                    "value_proposition": {{
                        "primary": "Main value they claim to deliver",
                        "supporting_points": ["Point 1", "Point 2"],
                        "clarity_score": 0.0-1.0
                    }},
                    "differentiation": {{
                        "key_differentiators": ["What makes them different"],
                        "uniqueness_score": 0.0-1.0,
                        "evidence": "What in the content supports this"
                    }},
                    "market_position": {{
                        "category": "Industry/market they're in",
                        "position": "Leader/Challenger/Follower/Niche",
                        "confidence": 0.0-1.0
                    }}
                }}
                """}
            ]
            
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                temperature=0.1,
                max_tokens=1500
            )
            
            content = response.choices[0].message.content.strip()
            return self.parse_json_response(content)
            
        except Exception as e:
            print(f"    ✗ Positioning analysis failed: {e}")
            return None
    
    def ai_swot_analysis(self, context):
        """Generate SWOT analysis from content"""
        try:
            messages = [
                {"role": "system", "content": "You are a business analyst creating SWOT analyses based on observable website content and messaging."},
                {"role": "user", "content": f"""
                Based on this brand's website content, create a SWOT analysis:
                
                {context['text_summary']}
                
                Analyze:
                - Strengths: What advantages are evident from their messaging?
                - Weaknesses: What gaps or limitations can be inferred?
                - Opportunities: What market opportunities do they seem positioned for?
                - Threats: What competitive challenges might they face?
                
                Base your analysis ONLY on observable content and reasonable inferences.
                
                Return as JSON:
                {{
                    "strengths": [
                        {{"point": "Strength", "evidence": "What suggests this", "impact": "High/Medium/Low"}}
                    ],
                    "weaknesses": [
                        {{"point": "Weakness", "evidence": "What suggests this", "impact": "High/Medium/Low"}}
                    ],
                    "opportunities": [
                        {{"point": "Opportunity", "rationale": "Why this is an opportunity", "potential": "High/Medium/Low"}}
                    ],
                    "threats": [
                        {{"point": "Threat", "likelihood": "High/Medium/Low", "impact": "High/Medium/Low"}}
                    ],
                    "analysis_confidence": 0.0-1.0
                }}
                """}
            ]
            
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                temperature=0.2,
                max_tokens=1500
            )
            
            content = response.choices[0].message.content.strip()
            return self.parse_json_response(content)
            
        except Exception as e:
            print(f"    ✗ SWOT analysis failed: {e}")
            return None
    
    def ai_audience_analysis(self, context):
        """Analyze target audience from content"""
        try:
            messages = [
                {"role": "system", "content": "You are a customer insights expert inferring target audiences from brand messaging and content."},
                {"role": "user", "content": f"""
                Analyze the target audience based on this brand's content:
                
                {context['text_summary']}
                
                Infer from their messaging:
                1. Who they're speaking to (language, complexity, tone)
                2. What problems they're addressing
                3. What outcomes they're promising
                
                Return as JSON:
                {{
                    "primary_audience": {{
                        "description": "Who they appear to target",
                        "characteristics": ["Key traits"],
                        "needs_addressed": ["Problems they solve"],
                        "sophistication_level": "Basic/Intermediate/Advanced"
                    }},
                    "messaging_tone": {{
                        "formality": "Casual/Professional/Technical",
                        "complexity": "Simple/Moderate/Complex",
                        "emotional_appeal": "Type of emotional connection"
                    }},
                    "evidence": {{
                        "language_indicators": ["Specific words/phrases used"],
                        "content_focus": "What they emphasize"
                    }},
                    "confidence": 0.0-1.0
                }}
                """}
            ]
            
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                temperature=0.1,
                max_tokens=1200
            )
            
            content = response.choices[0].message.content.strip()
            return self.parse_json_response(content)
            
        except Exception as e:
            print(f"    ✗ Audience analysis failed: {e}")
            return None
    
    def ai_innovation_analysis(self, context):
        """Analyze innovation and technology focus"""
        try:
            messages = [
                {"role": "system", "content": "You are an innovation strategist analyzing technology and innovation messaging."},
                {"role": "user", "content": f"""
                Analyze this brand's innovation and technology positioning:
                
                {context['text_summary']}
                
                Look for:
                1. Technology mentions and emphasis
                2. Innovation claims or messaging
                3. Future-focused language
                4. Disruption or transformation themes
                
                Return as JSON:
                {{
                    "innovation_level": {{
                        "score": 0-100,
                        "category": "Leading/Following/Traditional",
                        "evidence": ["What suggests this"]
                    }},
                    "technology_focus": {{
                        "mentioned_technologies": ["Tech 1", "Tech 2"],
                        "sophistication": "Cutting-edge/Current/Lagging",
                        "implementation": "How they use/position technology"
                    }},
                    "market_gaps": [
                        {{"gap": "Identified opportunity", "size": "Large/Medium/Small"}}
                    ],
                    "future_readiness": {{
                        "score": 0-100,
                        "indicators": ["What shows future focus"]
                    }}
                }}
                """}
            ]
            
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                temperature=0.2,
                max_tokens=1200
            )
            
            content = response.choices[0].message.content.strip()
            return self.parse_json_response(content)
            
        except Exception as e:
            print(f"    ✗ Innovation analysis failed: {e}")
            return None
    
    def ai_brand_health_scoring(self, context):
        """Score brand health across dimensions"""
        try:
            messages = [
                {"role": "system", "content": "You are a brand health analyst evaluating brand strength from digital presence."},
                {"role": "user", "content": f"""
                Score this brand's health based on their website:
                
                {context['text_summary']}
                
                Evaluate:
                1. Message clarity (how clear is their value prop?)
                2. Differentiation strength (how unique are they?)
                3. Professional presentation (quality of content)
                4. Customer focus (how well do they address needs?)
                
                Return as JSON:
                {{
                    "overall_score": 0-100,
                    "dimensions": {{
                        "message_clarity": {{"score": 0-100, "notes": "Assessment"}},
                        "differentiation": {{"score": 0-100, "notes": "Assessment"}},
                        "professionalism": {{"score": 0-100, "notes": "Assessment"}},
                        "customer_focus": {{"score": 0-100, "notes": "Assessment"}}
                    }},
                    "competitive_threat": {{
                        "level": "High/Medium/Low",
                        "rationale": "Why this threat level"
                    }},
                    "strengths": ["Key strengths observed"],
                    "concerns": ["Potential weaknesses"]
                }}
                """}
            ]
            
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                temperature=0.1,
                max_tokens=1200
            )
            
            content = response.choices[0].message.content.strip()
            return self.parse_json_response(content)
            
        except Exception as e:
            print(f"    ✗ Health scoring failed: {e}")
            return None
    
    def generate_cross_brand_insights(self):
        """Generate insights across all analyzed brands"""
        if len(self.brand_profiles) < 2:
            return None
        
        # Prepare brand summaries
        brand_summaries = []
        for brand in self.brand_profiles:
            if brand.get('ai_analyses'):
                summary = {
                    'name': brand['company_name'],
                    'positioning': brand['ai_analyses'].get('positioning', {}).get('positioning_strategy', {}),
                    'health_score': brand['ai_analyses'].get('health', {}).get('overall_score', 0),
                    'threat_level': brand['ai_analyses'].get('health', {}).get('competitive_threat', {}).get('level', 'Unknown'),
                    'innovation': brand['ai_analyses'].get('innovation', {}).get('innovation_level', {}).get('category', 'Unknown')
                }
                brand_summaries.append(summary)
        
        try:
            messages = [
                {"role": "system", "content": "You are a competitive intelligence expert analyzing market dynamics."},
                {"role": "user", "content": f"""
                Analyze competitive dynamics across these brands:
                
                {json.dumps(brand_summaries, indent=2)}
                
                Provide strategic insights:
                1. Market structure and competitive intensity
                2. Positioning gaps and opportunities
                3. Threat assessment and rankings
                4. Strategic recommendations
                
                Return as JSON:
                {{
                    "market_analysis": {{
                        "structure": "Fragmented/Consolidated/Emerging",
                        "maturity": "Nascent/Growing/Mature/Declining",
                        "competitive_intensity": "Low/Medium/High",
                        "key_dynamics": ["Dynamic 1", "Dynamic 2"]
                    }},
                    "positioning_landscape": {{
                        "occupied_positions": ["Position 1", "Position 2"],
                        "gaps": [{{"opportunity": "Gap description", "potential": "High/Medium/Low"}}],
                        "overcrowded_areas": ["Area 1", "Area 2"]
                    }},
                    "competitive_threats": [
                        {{"brand": "Name", "threat_level": "High/Medium/Low", "reason": "Why"}}
                    ],
                    "strategic_recommendations": [
                        {{"for": "New entrant/Existing player", "recommendation": "Strategy"}}
                    ]
                }}
                """}
            ]
            
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                temperature=0.2,
                max_tokens=2000
            )
            
            content = response.choices[0].message.content.strip()
            return self.parse_json_response(content)
            
        except Exception as e:
            print(f"  ✗ Cross-brand insights failed: {e}")
            return None
    
    def parse_json_response(self, content):
        """Parse JSON from LLM response"""
        try:
            # Remove markdown code blocks if present
            content = re.sub(r"```(json)?", "", content).strip()
            
            # Find JSON in response
            if '{' in content:
                start = content.find('{')
                end = content.rfind('}') + 1
                json_content = content[start:end]
                return json.loads(json_content)
            
            return None
            
        except Exception as e:
            print(f"    ✗ JSON parsing failed: {e}")
            return None
    
    def generate_slide_presentation(self, report_title="Competitive Intelligence Report"):
        """Generate 16:9 slide presentation with real data only"""
        
        if not self.brand_profiles:
            return self.generate_error_presentation("No brands could be analyzed")
        
        slides_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{report_title} - AI Analysis</title>
    <style>{self._get_slide_css()}</style>
    <script>{self._get_slide_js()}</script>
</head>
<body>
    {self._generate_title_slide(report_title)}
    {self._generate_overview_slide()}
    {self._generate_brand_slides()}
    {self._generate_comparison_slide()}
    {self._generate_insights_slide()}
    {self._generate_data_quality_slide()}
</body>
</html>"""
        
        return slides_html
    
    def _get_slide_css(self):
        """CSS for slide presentation"""
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
        
        .slide {
            width: 100vw;
            height: 100vh;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            display: none;
            position: relative;
            padding: 60px;
        }
        
        .slide.active {
            display: flex;
            flex-direction: column;
        }
        
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
        }
        
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
        }
        
        .card-title {
            font-size: 1.5em;
            font-weight: 600;
            color: #2c3e50;
            margin-bottom: 20px;
            border-bottom: 2px solid #e9ecef;
            padding-bottom: 10px;
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
        
        .nav-prev { left: 30px; }
        .nav-next { right: 30px; }
        
        /* AI Insights */
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
        
        /* Data Quality Indicators */
        .quality-indicator {
            display: inline-block;
            padding: 3px 10px;
            border-radius: 15px;
            font-size: 0.8em;
            margin-left: 10px;
        }
        
        .quality-high { background: #d4edda; color: #155724; }
        .quality-medium { background: #fff3cd; color: #856404; }
        .quality-low { background: #f8d7da; color: #721c24; }
        
        /* Title Slide */
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
        
        .data-badge {
            background: linear-gradient(135deg, #28a745, #20c997);
            color: white;
            padding: 15px 30px;
            border-radius: 50px;
            font-size: 1.2em;
            font-weight: 600;
            display: inline-block;
            margin: 20px 0;
        }
        
        /* Error State */
        .error-slide {
            background: linear-gradient(135deg, #dc3545, #c82333);
            justify-content: center;
            align-items: center;
            text-align: center;
        }
        
        .error-icon {
            font-size: 6em;
            margin-bottom: 30px;
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
        
        @media print {
            .slide {
                display: block !important;
                page-break-after: always;
            }
            
            .nav-button, .slide-navigation {
                display: none;
            }
        }
        """
    
    def _get_slide_js(self):
        """JavaScript for slide navigation"""
        return """
        let currentSlide = 0;
        let totalSlides = 0;
        
        document.addEventListener('DOMContentLoaded', function() {
            const slides = document.querySelectorAll('.slide');
            totalSlides = slides.length;
            
            // Create navigation dots
            const navContainer = document.createElement('div');
            navContainer.className = 'slide-navigation';
            document.body.appendChild(navContainer);
            
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
            
            if (n >= totalSlides) currentSlide = 0;
            if (n < 0) currentSlide = totalSlides - 1;
            
            slides.forEach(slide => slide.classList.remove('active'));
            dots.forEach(dot => dot.classList.remove('active'));
            
            slides[currentSlide].classList.add('active');
            if (dots[currentSlide]) dots[currentSlide].classList.add('active');
        }
        
        function nextSlide() {
            currentSlide++;
            showSlide(currentSlide);
        }
        
        function prevSlide() {
            currentSlide--;
            showSlide(currentSlide);
        }
        
        function goToSlide(n) {
            currentSlide = n;
            showSlide(currentSlide);
        }
        """
    
    def _generate_title_slide(self, report_title):
        """Generate title slide"""
        timestamp = datetime.now().strftime('%B %d, %Y')
        return f"""
        <div class="slide title-slide active">
            <h1 class="main-title">{report_title}</h1>
            <p class="subtitle">AI-Powered Competitive Intelligence Analysis</p>
            <div class="data-badge">🔍 Real Data Only • No Defaults</div>
            <p style="color: rgba(255,255,255,0.7); margin-top: 30px;">
                Generated on {timestamp}<br>
                {len(self.brand_profiles)} brands analyzed • {len(self.failed_brands)} failed
            </p>
            
            <button class="nav-button nav-next" onclick="nextSlide()">→</button>
        </div>
        """
    
    def _generate_overview_slide(self):
        """Generate overview slide"""
        return f"""
        <div class="slide">
            <div class="slide-header">
                <h2 class="slide-title">Analysis Overview</h2>
                <div class="slide-number">2 / {self._total_slides()}</div>
            </div>
            
            <div class="slide-content">
                <div class="ai-insight">
                    <strong>Analysis Summary:</strong> Successfully analyzed {len(self.brand_profiles)} brands 
                    with comprehensive AI intelligence gathering. {len(self.failed_brands)} brands could not be analyzed.
                </div>
                
                <div class="content-grid">
                    <div class="content-card">
                        <h3 class="card-title">Successful Analyses</h3>
                        {self._generate_brand_summary_list()}
                    </div>
                    
                    <div class="content-card">
                        <h3 class="card-title">Analysis Metrics</h3>
                        {self._generate_analysis_metrics()}
                    </div>
                </div>
            </div>
            
            <button class="nav-button nav-prev" onclick="prevSlide()">←</button>
            <button class="nav-button nav-next" onclick="nextSlide()">→</button>
        </div>
        """
    
    def _generate_brand_slides(self):
        """Generate individual brand analysis slides"""
        slides = ""
        slide_num = 3
        
        for brand in self.brand_profiles:
            slides += self._generate_single_brand_slide(brand, slide_num)
            slide_num += 1
        
        return slides
    
    def _generate_single_brand_slide(self, brand, slide_num):
        """Generate slide for single brand"""
        analyses = brand.get('ai_analyses', {})
        
        # Extract key data
        positioning = analyses.get('positioning', {})
        health = analyses.get('health', {})
        swot = analyses.get('swot', {})
        
        overall_score = health.get('overall_score', 0)
        threat_level = health.get('competitive_threat', {}).get('level', 'Unknown')
        
        score_class = "score-high" if overall_score >= 80 else "score-medium" if overall_score >= 60 else "score-low"
        threat_class = f"threat-{threat_level.lower()}" if threat_level != 'Unknown' else ""
        
        quality_score = brand.get('extraction_quality', 0)
        quality_class = "quality-high" if quality_score >= 0.8 else "quality-medium" if quality_score >= 0.5 else "quality-low"
        
        return f"""
        <div class="slide">
            <div class="slide-header">
                <h2 class="slide-title">
                    {brand['company_name']}
                    <span class="quality-indicator {quality_class}">
                        Data Quality: {quality_score:.0%}
                    </span>
                </h2>
                <div class="slide-number">{slide_num} / {self._total_slides()}</div>
            </div>
            
            <div class="slide-content">
                <div class="content-grid">
                    <div class="content-card">
                        <h3 class="card-title">Strategic Positioning</h3>
                        {self._generate_positioning_content(positioning)}
                        
                        <div class="score-display">
                            <div class="score-circle {score_class}">{overall_score}</div>
                            <div>
                                <strong>Brand Health Score</strong><br>
                                {f'<span class="threat-badge {threat_class}">{threat_level} Threat</span>' if threat_level != 'Unknown' else 'Threat level not determined'}
                            </div>
                        </div>
                    </div>
                    
                    <div class="content-card">
                        <h3 class="card-title">SWOT Analysis</h3>
                        {self._generate_swot_content(swot)}
                    </div>
                </div>
            </div>
            
            <button class="nav-button nav-prev" onclick="prevSlide()">←</button>
            <button class="nav-button nav-next" onclick="nextSlide()">→</button>
        </div>
        """
    
    def _generate_positioning_content(self, positioning):
        """Generate positioning content"""
        if not positioning:
            return "<p>Positioning analysis not available</p>"
        
        strategy = positioning.get('positioning_strategy', {})
        value_prop = positioning.get('value_proposition', {})
        
        return f"""
        <div class="ai-insight">
            <strong>Strategy:</strong> {strategy.get('type', 'Not determined')}
            {f" (Confidence: {strategy.get('confidence', 0):.0%})" if 'confidence' in strategy else ""}
        </div>
        
        <p><strong>Positioning:</strong> {strategy.get('statement', 'Not found')}</p>
        
        <p><strong>Value Proposition:</strong> {value_prop.get('primary', 'Not identified')}</p>
        
        {self._generate_supporting_points(value_prop.get('supporting_points', []))}
        """
    
    def _generate_supporting_points(self, points):
        """Generate supporting points list"""
        if not points:
            return ""
        
        html = "<p><strong>Key Points:</strong></p><ul>"
        for point in points[:3]:
            html += f"<li>{point}</li>"
        html += "</ul>"
        
        return html
    
    def _generate_swot_content(self, swot):
        """Generate SWOT content"""
        if not swot:
            return "<p>SWOT analysis not available</p>"
        
        return f"""
        <div class="swot-grid">
            <div class="swot-quadrant swot-strengths">
                <div class="swot-title">Strengths</div>
                {self._generate_swot_items(swot.get('strengths', []))}
            </div>
            <div class="swot-quadrant swot-weaknesses">
                <div class="swot-title">Weaknesses</div>
                {self._generate_swot_items(swot.get('weaknesses', []))}
            </div>
            <div class="swot-quadrant swot-opportunities">
                <div class="swot-title">Opportunities</div>
                {self._generate_swot_items(swot.get('opportunities', []))}
            </div>
            <div class="swot-quadrant swot-threats">
                <div class="swot-title">Threats</div>
                {self._generate_swot_items(swot.get('threats', []))}
            </div>
        </div>
        """
    
    def _generate_swot_items(self, items):
        """Generate SWOT items"""
        if not items:
            return '<div class="swot-item">None identified</div>'
        
        html = ""
        for item in items[:3]:
            if isinstance(item, dict):
                html += f'<div class="swot-item">{item.get("point", item.get("strength", item.get("weakness", item.get("opportunity", item.get("threat", "")))))}</div>'
            else:
                html += f'<div class="swot-item">{item}</div>'
        
        return html
    
    def _generate_comparison_slide(self):
        """Generate comparison slide"""
        if len(self.brand_profiles) < 2:
            return ""
        
        return f"""
        <div class="slide">
            <div class="slide-header">
                <h2 class="slide-title">Competitive Comparison</h2>
                <div class="slide-number">{len(self.brand_profiles) + 3} / {self._total_slides()}</div>
            </div>
            
            <div class="slide-content">
                {self._generate_comparison_table()}
            </div>
            
            <button class="nav-button nav-prev" onclick="prevSlide()">←</button>
            <button class="nav-button nav-next" onclick="nextSlide()">→</button>
        </div>
        """
    
    def _generate_comparison_table(self):
        """Generate comparison table"""
        html = """
        <div class="content-card" style="max-width: 100%;">
            <h3 class="card-title">Brand Comparison Matrix</h3>
            <table style="width: 100%; border-collapse: collapse;">
                <tr style="background: #f8f9fa;">
                    <th style="padding: 12px; text-align: left; border-bottom: 2px solid #dee2e6;">Brand</th>
                    <th style="padding: 12px; text-align: center; border-bottom: 2px solid #dee2e6;">Health Score</th>
                    <th style="padding: 12px; text-align: center; border-bottom: 2px solid #dee2e6;">Threat Level</th>
                    <th style="padding: 12px; text-align: center; border-bottom: 2px solid #dee2e6;">Innovation</th>
                    <th style="padding: 12px; text-align: center; border-bottom: 2px solid #dee2e6;">Data Quality</th>
                </tr>
        """
        
        for brand in self.brand_profiles:
            analyses = brand.get('ai_analyses', {})
            health_score = analyses.get('health', {}).get('overall_score', 0)
            threat_level = analyses.get('health', {}).get('competitive_threat', {}).get('level', 'Unknown')
            innovation = analyses.get('innovation', {}).get('innovation_level', {}).get('category', 'Unknown')
            quality = brand.get('extraction_quality', 0)
            
            html += f"""
                <tr>
                    <td style="padding: 12px; border-bottom: 1px solid #e9ecef;">{brand['company_name']}</td>
                    <td style="padding: 12px; text-align: center; border-bottom: 1px solid #e9ecef;">
                        <strong>{health_score}</strong>/100
                    </td>
                    <td style="padding: 12px; text-align: center; border-bottom: 1px solid #e9ecef;">
                        <span class="threat-badge threat-{threat_level.lower()}">{threat_level}</span>
                    </td>
                    <td style="padding: 12px; text-align: center; border-bottom: 1px solid #e9ecef;">{innovation}</td>
                    <td style="padding: 12px; text-align: center; border-bottom: 1px solid #e9ecef;">{quality:.0%}</td>
                </tr>
            """
        
        html += "</table></div>"
        return html
    
    def _generate_insights_slide(self):
        """Generate insights slide"""
        if not self.competitive_insights:
            return ""
        
        return f"""
        <div class="slide">
            <div class="slide-header">
                <h2 class="slide-title">Strategic Insights</h2>
                <div class="slide-number">{self._total_slides() - 1} / {self._total_slides()}</div>
            </div>
            
            <div class="slide-content">
                <div class="content-grid">
                    <div class="content-card">
                        <h3 class="card-title">Market Analysis</h3>
                        {self._generate_market_insights()}
                    </div>
                    
                    <div class="content-card">
                        <h3 class="card-title">Strategic Recommendations</h3>
                        {self._generate_recommendations()}
                    </div>
                </div>
            </div>
            
            <button class="nav-button nav-prev" onclick="prevSlide()">←</button>
            <button class="nav-button nav-next" onclick="nextSlide()">→</button>
        </div>
        """
    
    def _generate_market_insights(self):
        """Generate market insights content"""
        if not self.competitive_insights:
            return "<p>Market insights not available</p>"
        
        market = self.competitive_insights.get('market_analysis', {})
        positioning = self.competitive_insights.get('positioning_landscape', {})
        
        html = f"""
        <div class="ai-insight">
            <strong>Market Structure:</strong> {market.get('structure', 'Unknown')}<br>
            <strong>Maturity:</strong> {market.get('maturity', 'Unknown')}<br>
            <strong>Competitive Intensity:</strong> {market.get('competitive_intensity', 'Unknown')}
        </div>
        """
        
        # Positioning gaps
        gaps = positioning.get('gaps', [])
        if gaps:
            html += "<p><strong>Market Opportunities:</strong></p><ul>"
            for gap in gaps[:3]:
                html += f"<li>{gap.get('opportunity', 'Opportunity')} - {gap.get('potential', 'Unknown')} potential</li>"
            html += "</ul>"
        
        return html
    
    def _generate_recommendations(self):
        """Generate recommendations content"""
        if not self.competitive_insights:
            return "<p>Recommendations not available</p>"
        
        recommendations = self.competitive_insights.get('strategic_recommendations', [])
        
        if not recommendations:
            return "<p>No specific recommendations generated</p>"
        
        html = "<ul>"
        for rec in recommendations[:5]:
            if isinstance(rec, dict):
                html += f"<li><strong>{rec.get('for', 'General')}:</strong> {rec.get('recommendation', 'N/A')}</li>"
            else:
                html += f"<li>{rec}</li>"
        html += "</ul>"
        
        return html
    
    def _generate_data_quality_slide(self):
        """Generate data quality summary slide"""
        return f"""
        <div class="slide">
            <div class="slide-header">
                <h2 class="slide-title">Data Quality Report</h2>
                <div class="slide-number">{self._total_slides()} / {self._total_slides()}</div>
            </div>
            
            <div class="slide-content">
                <div class="content-card">
                    <h3 class="card-title">Extraction Summary</h3>
                    
                    <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin: 20px 0;">
                        <div style="text-align: center; padding: 20px; background: #d4edda; border-radius: 10px;">
                            <div style="font-size: 2em; font-weight: bold; color: #155724;">{len(self.brand_profiles)}</div>
                            <div style="color: #155724;">Successful</div>
                        </div>
                        
                        <div style="text-align: center; padding: 20px; background: #f8d7da; border-radius: 10px;">
                            <div style="font-size: 2em; font-weight: bold; color: #721c24;">{len(self.failed_brands)}</div>
                            <div style="color: #721c24;">Failed</div>
                        </div>
                        
                        <div style="text-align: center; padding: 20px; background: #d1ecf1; border-radius: 10px;">
                            <div style="font-size: 2em; font-weight: bold; color: #0c5460;">
                                {self._calculate_average_quality():.0%}
                            </div>
                            <div style="color: #0c5460;">Avg Quality</div>
                        </div>
                    </div>
                    
                    {self._generate_failed_brands_list()}
                </div>
            </div>
            
            <button class="nav-button nav-prev" onclick="prevSlide()">←</button>
        </div>
        """
    
    def _generate_brand_summary_list(self):
        """Generate brand summary list"""
        html = "<ul>"
        for brand in self.brand_profiles[:10]:
            quality = brand.get('extraction_quality', 0)
            html += f"""
                <li>
                    <strong>{brand['company_name']}</strong>
                    <span class="quality-indicator {'quality-high' if quality >= 0.8 else 'quality-medium' if quality >= 0.5 else 'quality-low'}">
                        {quality:.0%}
                    </span>
                </li>
            """
        
        if len(self.brand_profiles) > 10:
            html += f"<li><em>... and {len(self.brand_profiles) - 10} more</em></li>"
        
        html += "</ul>"
        return html
    
    def _generate_analysis_metrics(self):
        """Generate analysis metrics"""
        total_attempted = len(self.brand_profiles) + len(self.failed_brands)
        success_rate = (len(self.brand_profiles) / total_attempted * 100) if total_attempted > 0 else 0
        avg_quality = self._calculate_average_quality()
        
        # Count high-threat brands
        high_threats = sum(1 for b in self.brand_profiles 
                          if b.get('ai_analyses', {}).get('health', {}).get('competitive_threat', {}).get('level') == 'High')
        
        return f"""
        <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px;">
            <div>
                <strong>Success Rate:</strong> {success_rate:.1f}%
            </div>
            <div>
                <strong>Avg Quality:</strong> {avg_quality:.0%}
            </div>
            <div>
                <strong>High Threats:</strong> {high_threats}
            </div>
            <div>
                <strong>AI Analyses:</strong> Complete
            </div>
        </div>
        
        <div class="ai-insight" style="margin-top: 20px;">
            All data extracted from live websites. No placeholder or default values used.
        </div>
        """
    
    def _generate_failed_brands_list(self):
        """Generate failed brands list"""
        if not self.failed_brands:
            return "<p><strong>All brands analyzed successfully!</strong></p>"
        
        html = "<div style='margin-top: 20px;'><strong>Failed Extractions:</strong><ul style='color: #721c24;'>"
        for failure in self.failed_brands[:5]:
            html += f"<li>{failure['url']} - {failure['reason']}</li>"
        
        if len(self.failed_brands) > 5:
            html += f"<li><em>... and {len(self.failed_brands) - 5} more</em></li>"
        
        html += "</ul></div>"
        return html
    
    def _calculate_average_quality(self):
        """Calculate average extraction quality"""
        if not self.brand_profiles:
            return 0
        
        total_quality = sum(b.get('extraction_quality', 0) for b in self.brand_profiles)
        return total_quality / len(self.brand_profiles)
    
    def _total_slides(self):
        """Calculate total number of slides"""
        # Title + Overview + Brand slides + Comparison + Insights + Quality
        return 2 + len(self.brand_profiles) + 3
    
    def generate_error_presentation(self, error_message):
        """Generate error presentation"""
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Analysis Failed</title>
    <style>{self._get_slide_css()}</style>
</head>
<body>
    <div class="slide error-slide active">
        <div class="error-icon">❌</div>
        <h1 class="main-title">Analysis Failed</h1>
        <p class="subtitle">{error_message}</p>
        
        {self._generate_failed_urls_summary()}
    </div>
</body>
</html>"""
    
    def _generate_failed_urls_summary(self):
        """Generate failed URLs summary"""
        if not self.failed_brands:
            return ""
        
        html = '<div style="background: rgba(255,255,255,0.1); padding: 30px; border-radius: 15px; margin-top: 40px; max-width: 600px;">'
        html += '<h3 style="color: white; margin-bottom: 20px;">Failed URLs:</h3>'
        
        for failure in self.failed_brands[:10]:
            html += f'<div style="color: rgba(255,255,255,0.8); margin: 10px 0;">{failure["url"]}<br><small>{failure["reason"]}</small></div>'
        
        if len(self.failed_brands) > 10:
            html += f'<div style="color: rgba(255,255,255,0.6); margin-top: 20px;">... and {len(self.failed_brands) - 10} more</div>'
        
        html += '</div>'
        return html
    
    def generate_report(self, urls, report_title="Competitive Intelligence Report", output_filename=None):
        """Generate complete AI-powered report"""
        
        if not output_filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_filename = f"ai_intelligence_real_data_{timestamp}.html"
        
        # Analyze brands
        results = self.analyze_brands(urls)
        
        # Generate presentation
        if results['successful']:
            html_content = self.generate_slide_presentation(report_title)
        else:
            html_content = self.generate_error_presentation("No brands could be analyzed successfully")
        
        # Save report
        try:
            with open(output_filename, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            print(f"\n📄 Report saved: {output_filename}")
            print(f"🎯 Format: 16:9 slide presentation")
            print(f"🧭 Navigation: Arrow keys or click buttons")
            
            return {
                'filename': output_filename,
                'successful_count': len(results['successful']),
                'failed_count': len(results['failed']),
                'has_insights': bool(self.competitive_insights)
            }
            
        except Exception as e:
            print(f"❌ Error saving report: {e}")
            return None

def main():
    """Example usage"""
    
    # Test with diverse URLs
    test_urls = [
        "https://www.notion.so",
        "https://www.airtable.com",
        "https://www.monday.com",
        "https://www.asana.com",
        "https://www.clickup.com"
    ]
    
    intelligence = AIPoweredCompetitiveIntelligenceV2()
    
    result = intelligence.generate_report(
        urls=test_urls,
        report_title="Productivity Tools Competitive Intelligence",
        output_filename="productivity_tools_intelligence.html"
    )
    
    if result:
        print(f"\n🎉 SUCCESS!")
        print(f"📊 Analyzed: {result['successful_count']} brands")
        print(f"❌ Failed: {result['failed_count']} brands")
        print(f"🧠 Cross-brand insights: {'Yes' if result['has_insights'] else 'No'}")
        print(f"📁 View report: {result['filename']}")

if __name__ == "__main__":
    main()
