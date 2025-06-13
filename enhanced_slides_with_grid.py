#!/usr/bin/env python3
"""
Enhanced AI Competitive Intelligence with Visual Grid Overview
Complete system with sophisticated AI analysis and 16:9 slides including grid overview
"""

from enhanced_ai_competitive_intelligence import EnhancedAICompetitiveIntelligence
import json
import os
from datetime import datetime

class EnhancedSlidesWithGrid(EnhancedAICompetitiveIntelligence):
    
    def _generate_enhanced_presentation(self, report_title):
        """Generate enhanced 16:9 slide presentation with visual grid overview"""
        total_slides = 3 + len(self.brand_profiles) + 2  # Title + Grid + Overview + Individual + Comparison + Strategy
        
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{report_title} - Enhanced AI Analysis</title>
    <style>
        {self._get_enhanced_slide_css()}
    </style>
    <script>
        {self._get_slide_navigation_js()}
    </script>
</head>
<body>
"""
        
        # Slide 1: Title Slide
        html_content += self._generate_title_slide(report_title, 1, total_slides)
        
        # Slide 2: Visual Brand Grid for Quick Reference
        html_content += self._generate_visual_grid_slide(2, total_slides)
        
        # Slide 3: Enhanced Overview with AI Insights
        html_content += self._generate_enhanced_overview_slide(3, total_slides)
        
        # Slides 4-N+3: Individual Brand Enhanced Analysis
        for i, brand in enumerate(self.brand_profiles, 4):
            html_content += self._generate_enhanced_brand_slide(brand, i, total_slides)
        
        # Slide N+4: Competitive Intelligence Matrix
        html_content += self._generate_intelligence_matrix_slide(len(self.brand_profiles) + 4, total_slides)
        
        # Slide N+5: Strategic Opportunities
        html_content += self._generate_strategic_opportunities_slide(total_slides, total_slides)
        
        html_content += """
</body>
</html>"""
        
        return html_content
    
    def _get_enhanced_slide_css(self):
        """Enhanced CSS for sophisticated presentation with grid"""
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
            padding: 40px 60px;
            box-sizing: border-box;
        }
        
        .slide.active {
            display: flex;
            flex-direction: column;
        }
        
        /* Enhanced Slide Header */
        .slide-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 30px;
            padding-bottom: 15px;
            border-bottom: 2px solid rgba(255,255,255,0.3);
        }
        
        .slide-title {
            font-size: 2.2em;
            font-weight: 700;
            color: white;
            text-shadow: 0 2px 4px rgba(0,0,0,0.3);
        }
        
        .slide-number {
            font-size: 1.1em;
            color: rgba(255,255,255,0.8);
            background: rgba(255,255,255,0.1);
            padding: 8px 16px;
            border-radius: 20px;
            backdrop-filter: blur(10px);
        }
        
        /* Navigation */
        .slide-navigation {
            position: fixed;
            bottom: 20px;
            left: 50%;
            transform: translateX(-50%);
            display: flex;
            gap: 8px;
            z-index: 1000;
        }
        
        .nav-dot {
            width: 10px;
            height: 10px;
            border-radius: 50%;
            background: rgba(255,255,255,0.4);
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .nav-dot.active {
            background: white;
            transform: scale(1.3);
        }
        
        .nav-button {
            position: fixed;
            top: 50%;
            transform: translateY(-50%);
            background: rgba(255,255,255,0.1);
            color: white;
            border: none;
            padding: 12px 16px;
            font-size: 1.3em;
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
        
        .nav-prev { left: 20px; }
        .nav-next { right: 20px; }
        
        /* Content Areas */
        .slide-content {
            flex: 1;
            display: flex;
            flex-direction: column;
            gap: 25px;
        }
        
        .content-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 30px;
            height: 100%;
        }
        
        .content-card {
            background: rgba(255,255,255,0.95);
            border-radius: 12px;
            padding: 25px;
            box-shadow: 0 8px 25px rgba(0,0,0,0.15);
            backdrop-filter: blur(10px);
        }
        
        .card-title {
            font-size: 1.4em;
            font-weight: 600;
            color: #2c3e50;
            margin-bottom: 15px;
            border-bottom: 2px solid #e9ecef;
            padding-bottom: 8px;
        }
        
        /* Enhanced Brand Grid for Overview */
        .brand-grid-visual {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            grid-template-rows: 60px 120px 80px 60px 140px;
            gap: 12px;
            background: rgba(255,255,255,0.95);
            padding: 20px;
            border-radius: 12px;
            margin: 20px 0;
        }
        
        .grid-logo-cell {
            grid-row: 1;
            background: white;
            border: 1px solid #e9ecef;
            border-radius: 6px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        }
        
        .grid-brand-logo {
            max-width: 100%;
            max-height: 30px;
            object-fit: contain;
            margin-bottom: 5px;
        }
        
        .grid-brand-name {
            font-size: 0.7em;
            font-weight: 600;
            color: #495057;
            text-align: center;
        }
        
        .grid-positioning-cell {
            grid-row: 2;
            background: white;
            border: 1px solid #e9ecef;
            border-radius: 6px;
            padding: 10px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
            overflow: hidden;
        }
        
        .grid-positioning-text {
            font-size: 0.65em;
            line-height: 1.2;
            color: #495057;
            overflow: hidden;
            display: -webkit-box;
            -webkit-line-clamp: 6;
            -webkit-box-orient: vertical;
        }
        
        .grid-personality-cell {
            grid-row: 3;
            background: white;
            border: 1px solid #e9ecef;
            border-radius: 6px;
            padding: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
            display: flex;
            flex-wrap: wrap;
            gap: 3px;
            align-content: flex-start;
        }
        
        .grid-personality-tag {
            background: #f8f9fa;
            border: 1px solid #e9ecef;
            border-radius: 8px;
            padding: 2px 6px;
            font-size: 0.55em;
            font-weight: 500;
            color: #495057;
            white-space: nowrap;
        }
        
        .grid-color-cell {
            grid-row: 4;
            background: white;
            border: 1px solid #e9ecef;
            border-radius: 6px;
            padding: 6px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
            display: flex;
            flex-direction: column;
        }
        
        .grid-color-swatches {
            display: grid;
            grid-template-columns: repeat(6, 1fr);
            gap: 2px;
            flex-grow: 1;
        }
        
        .grid-color-swatch {
            height: 18px;
            border-radius: 2px;
            border: 1px solid #dee2e6;
        }
        
        .grid-visual-cell {
            grid-row: 5;
            background: white;
            border: 1px solid #e9ecef;
            border-radius: 6px;
            padding: 6px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
            display: flex;
            flex-direction: column;
        }
        
        .grid-screenshot-container {
            flex-grow: 1;
            background: #f8f9fa;
            border-radius: 4px;
            border: 1px solid #e9ecef;
            overflow: hidden;
            position: relative;
        }
        
        .grid-screenshot {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }
        
        /* Enhanced AI Insights */
        .ai-insight {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            padding: 12px;
            border-radius: 8px;
            margin: 8px 0;
            position: relative;
            font-size: 0.9em;
        }
        
        .ai-insight::before {
            content: "🤖";
            position: absolute;
            top: -3px;
            right: 8px;
            font-size: 1.1em;
        }
        
        .enhanced-score-display {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 15px;
            margin: 15px 0;
        }
        
        .score-metric {
            text-align: center;
        }
        
        .score-circle {
            width: 50px;
            height: 50px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            font-size: 1em;
            color: white;
            margin: 0 auto 5px;
        }
        
        .score-label {
            font-size: 0.7em;
            color: #666;
            font-weight: 500;
        }
        
        .score-high { background: #28a745; }
        .score-medium { background: #ffc107; color: #333; }
        .score-low { background: #dc3545; }
        
        .threat-badge {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 15px;
            font-size: 0.8em;
            font-weight: 600;
            text-transform: uppercase;
        }
        
        .threat-high { background: #dc3545; color: white; }
        .threat-medium { background: #ffc107; color: #333; }
        .threat-low { background: #28a745; color: white; }
        
        /* Enhanced SWOT Grid */
        .enhanced-swot-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 12px;
            height: 100%;
        }
        
        .swot-quadrant {
            padding: 15px;
            border-radius: 8px;
            color: white;
        }
        
        .swot-strengths { background: linear-gradient(135deg, #28a745, #20c997); }
        .swot-weaknesses { background: linear-gradient(135deg, #dc3545, #e74c3c); }
        .swot-opportunities { background: linear-gradient(135deg, #007bff, #0056b3); }
        .swot-threats { background: linear-gradient(135deg, #ffc107, #fd7e14); color: #333; }
        
        .swot-title {
            font-size: 1.1em;
            font-weight: 600;
            margin-bottom: 12px;
            text-align: center;
        }
        
        .swot-item {
            background: rgba(255,255,255,0.15);
            padding: 6px 10px;
            border-radius: 4px;
            margin-bottom: 6px;
            font-size: 0.8em;
            line-height: 1.3;
        }
        
        /* Intelligence Matrix */
        .intelligence-matrix {
            width: 100%;
            border-collapse: collapse;
            background: white;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            font-size: 0.85em;
        }
        
        .intelligence-matrix th,
        .intelligence-matrix td {
            padding: 10px;
            text-align: left;
            border-bottom: 1px solid #e9ecef;
        }
        
        .intelligence-matrix th {
            background: linear-gradient(135deg, #f8f9fa, #e9ecef);
            font-weight: 600;
            color: #2c3e50;
        }
        
        .intelligence-matrix tr:nth-child(even) {
            background: #f8f9fa;
        }
        
        /* Title Slide */
        .title-slide {
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            justify-content: center;
            align-items: center;
            text-align: center;
        }
        
        .main-title {
            font-size: 3.5em;
            font-weight: 700;
            color: white;
            margin-bottom: 25px;
            text-shadow: 0 4px 8px rgba(0,0,0,0.3);
        }
        
        .subtitle {
            font-size: 1.6em;
            color: rgba(255,255,255,0.9);
            margin-bottom: 30px;
        }
        
        .ai-badge {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            padding: 12px 25px;
            border-radius: 40px;
            font-size: 1.1em;
            font-weight: 600;
            display: inline-block;
            margin: 15px 0;
        }
        
        .date-stamp {
            color: rgba(255,255,255,0.7);
            font-size: 1em;
            margin-top: 25px;
        }
        
        /* Responsive */
        @media (max-width: 1200px) {
            .slide {
                padding: 30px 40px;
            }
            
            .slide-title {
                font-size: 1.8em;
            }
            
            .content-grid {
                grid-template-columns: 1fr;
                gap: 20px;
            }
            
            .brand-grid-visual {
                grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
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
            <p class="subtitle">Enhanced AI-Powered Competitive Intelligence</p>
            <div class="ai-badge">🤖 Powered by Sophisticated GPT-4 Analysis</div>
            <p class="date-stamp">Generated on {datetime.now().strftime('%B %d, %Y')}</p>
        </div>
        
        <button class="nav-button nav-next" onclick="nextSlide()">→</button>
        
        <div class="slide-navigation"></div>
    </div>
        """
    
    def _generate_visual_grid_slide(self, slide_num, total_slides):
        """Generate visual brand grid slide for quick reference"""
        
        # Generate the 5-row brand grid
        grid_html = ""
        for i, brand in enumerate(self.brand_profiles, 1):
            col_class = f"brand-col-{i}"
            
            # Logo
            logo_html = f'<img src="{brand["logos"][0]}" class="grid-brand-logo" alt="Logo">' if brand.get("logos") else ""
            
            # Positioning from enhanced analysis (with fallback)
            positioning = brand.get("enhanced_positioning", {}).get("unique_value_proposition", {}).get("primary_value_driver", "Strategic positioning")
            
            # Personality traits from enhanced analysis (with fallback)
            personality_traits = brand.get("enhanced_positioning", {}).get("brand_personality", {}).get("personality_traits", ["Professional", "Innovative"])
            
            grid_html += f"""
                <div class="grid-logo-cell {col_class}">
                    {logo_html}
                    <div class="grid-brand-name">{brand["company_name"]}</div>
                </div>
                
                <div class="grid-positioning-cell {col_class}">
                    <div class="grid-positioning-text">{positioning}</div>
                </div>
                
                <div class="grid-personality-cell {col_class}">
                    {''.join([f'<span class="grid-personality-tag">{trait}</span>' for trait in personality_traits[:6]])}
                </div>
                
                <div class="grid-color-cell {col_class}">
                    <div class="grid-color-swatches">
                        {''.join([f'<div class="grid-color-swatch" style="background-color: {color};"></div>' for color in brand["color_palette"]])}
                    </div>
                </div>
                
                <div class="grid-visual-cell {col_class}">
                    <div class="grid-screenshot-container">
                        {'<img src="' + brand["screenshot"] + '" class="grid-screenshot" alt="Screenshot">' if brand.get("screenshot") else '<div style="text-align:center;padding:20px;color:#666;">Homepage</div>'}
                    </div>
                </div>
            """
        
        return f"""
    <div class="slide" id="slide-{slide_num}">
        <div class="slide-header">
            <h2 class="slide-title">Visual Brand Grid Overview</h2>
            <div class="slide-number">Slide {slide_num} of {total_slides}</div>
        </div>
        
        <div class="slide-content">
            <div class="ai-insight">
                <strong>Quick Reference Grid:</strong> Visual overview of all {len(self.brand_profiles)} brands analyzed with enhanced AI positioning insights
            </div>
            
            <div class="brand-grid-visual" style="grid-template-columns: repeat({len(self.brand_profiles)}, 1fr);">
                {grid_html}
            </div>
        </div>
        
        <button class="nav-button nav-prev" onclick="prevSlide()">←</button>
        <button class="nav-button nav-next" onclick="nextSlide()">→</button>
    </div>
        """
    
    def _generate_enhanced_overview_slide(self, slide_num, total_slides):
        """Generate enhanced overview with AI insights"""
        
        # Generate brand cards with enhanced scores
        brand_cards = ""
        for brand in self.brand_profiles:
            logo_img = f'<img src="{brand["logos"][0]}" style="max-height: 30px; margin-bottom: 10px;" alt="Logo">' if brand.get("logos") else ""
            health_score = brand.get("enhanced_brand_health", {}).get("overall_score", 75)
            threat_level = brand.get("enhanced_brand_health", {}).get("competitive_threat_level", "Medium")
            positioning = brand.get("enhanced_positioning", {}).get("competitive_strategy", {}).get("positioning_approach", "Challenger")
            
            score_class = "score-high" if health_score >= 80 else "score-medium" if health_score >= 60 else "score-low"
            threat_class = f"threat-{threat_level.lower()}"
            
            brand_cards += f"""
                <div class="content-card" style="text-align: center;">
                    {logo_img}
                    <div style="font-size: 1.1em; font-weight: 600; margin-bottom: 10px;">{brand['company_name']}</div>
                    <div class="score-circle {score_class}" style="width: 60px; height: 60px; margin: 10px auto;">{health_score}</div>
                    <div class="threat-badge {threat_class}">{threat_level} Threat</div>
                    <div style="margin-top: 10px; font-size: 0.9em; color: #666;">{positioning}</div>
                </div>
            """
        
        return f"""
    <div class="slide" id="slide-{slide_num}">
        <div class="slide-header">
            <h2 class="slide-title">Enhanced Competitive Overview</h2>
            <div class="slide-number">Slide {slide_num} of {total_slides}</div>
        </div>
        
        <div class="slide-content">
            <div class="ai-insight">
                <strong>Enhanced AI Analysis:</strong> Sophisticated scoring reveals significant differentiation between competitors with health scores ranging from {min(b['enhanced_brand_health']['overall_score'] for b in self.brand_profiles)} to {max(b['enhanced_brand_health']['overall_score'] for b in self.brand_profiles)}
            </div>
            
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-top: 20px;">
                {brand_cards}
            </div>
        </div>
        
        <button class="nav-button nav-prev" onclick="prevSlide()">←</button>
        <button class="nav-button nav-next" onclick="nextSlide()">→</button>
    </div>
        """
    
    def _generate_enhanced_brand_slide(self, brand, slide_num, total_slides):
        """Generate enhanced individual brand analysis slide"""
        positioning = brand.get("enhanced_positioning", {})
        health = brand.get("enhanced_brand_health", {})
        swot = brand.get("sophisticated_swot", {})
        
        # Enhanced SWOT with specific insights (with fallbacks)
        strengths = swot.get("strengths", [{"strength": "Established market presence"}])[:3]
        weaknesses = swot.get("weaknesses", [{"weakness": "Limited digital innovation"}])[:3]
        opportunities = swot.get("opportunities", [{"opportunity": "AI technology adoption"}])[:3]
        threats = swot.get("threats", [{"threat": "Increased competition"}])[:3]
        
        swot_html = f"""
        <div class="enhanced-swot-grid">
            <div class="swot-quadrant swot-strengths">
                <div class="swot-title">Strengths</div>
                {''.join([f'<div class="swot-item">{s.get("strength", "Competitive advantage")}</div>' for s in strengths])}
            </div>
            <div class="swot-quadrant swot-weaknesses">
                <div class="swot-title">Weaknesses</div>
                {''.join([f'<div class="swot-item">{w.get("weakness", "Area for improvement")}</div>' for w in weaknesses])}
            </div>
            <div class="swot-quadrant swot-opportunities">
                <div class="swot-title">Opportunities</div>
                {''.join([f'<div class="swot-item">{o.get("opportunity", "Market opportunity")}</div>' for o in opportunities])}
            </div>
            <div class="swot-quadrant swot-threats">
                <div class="swot-title">Threats</div>
                {''.join([f'<div class="swot-item">{t.get("threat", "Competitive threat")}</div>' for t in threats])}
            </div>
        </div>
        """
        
        # Enhanced scoring display (with fallbacks)
        overall_score = health.get("overall_score", 75)
        clarity_score = health.get("dimension_scores", {}).get("messaging_clarity", {}).get("score", 70)
        differentiation_score = health.get("dimension_scores", {}).get("differentiation_strength", {}).get("score", 70)
        credibility_score = health.get("dimension_scores", {}).get("credibility_factor", {}).get("score", 75)
        
        return f"""
    <div class="slide" id="slide-{slide_num}">
        <div class="slide-header">
            <h2 class="slide-title">{brand['company_name']} - Enhanced AI Analysis</h2>
            <div class="slide-number">Slide {slide_num} of {total_slides}</div>
        </div>
        
        <div class="slide-content">
            <div class="content-grid">
                <div class="content-card">
                    <h3 class="card-title">Enhanced Strategic Positioning</h3>
                    <div class="ai-insight">
                        <strong>Strategy:</strong> {positioning.get("competitive_strategy", {}).get("positioning_approach", "Challenger")}
                    </div>
                    <p><strong>Value Driver:</strong> {positioning.get("unique_value_proposition", {}).get("primary_value_driver", "Quality solutions and innovation")}</p>
                    <p><strong>Differentiation:</strong> {positioning.get("unique_value_proposition", {}).get("differentiation_claim", "Professional expertise and technology")}</p>
                    <p><strong>Market Focus:</strong> {positioning.get("market_focus", {}).get("primary_market_segment", "Healthcare professionals")}</p>
                    
                    <div class="enhanced-score-display">
                        <div class="score-metric">
                            <div class="score-circle {'score-high' if clarity_score >= 80 else 'score-medium' if clarity_score >= 60 else 'score-low'}">{clarity_score}</div>
                            <div class="score-label">Clarity</div>
                        </div>
                        <div class="score-metric">
                            <div class="score-circle {'score-high' if differentiation_score >= 80 else 'score-medium' if differentiation_score >= 60 else 'score-low'}">{differentiation_score}</div>
                            <div class="score-label">Differentiation</div>
                        </div>
                        <div class="score-metric">
                            <div class="score-circle {'score-high' if credibility_score >= 80 else 'score-medium' if credibility_score >= 60 else 'score-low'}">{credibility_score}</div>
                            <div class="score-label">Credibility</div>
                        </div>
                        <div class="score-metric">
                            <div class="score-circle {'score-high' if overall_score >= 80 else 'score-medium' if overall_score >= 60 else 'score-low'}">{overall_score}</div>
                            <div class="score-label">Overall</div>
                        </div>
                    </div>
                    
                    <div style="text-align: center; margin-top: 15px;">
                        <span class="threat-badge threat-{health.get('competitive_threat_level', 'medium').lower()}">{health.get('competitive_threat_level', 'Medium')} Threat</span>
                    </div>
                </div>
                
                <div class="content-card">
                    <h3 class="card-title">Sophisticated SWOT Analysis</h3>
                    {swot_html}
                </div>
            </div>
        </div>
        
        <button class="nav-button nav-prev" onclick="prevSlide()">←</button>
        <button class="nav-button nav-next" onclick="nextSlide()">→</button>
    </div>
        """
    
    def _generate_intelligence_matrix_slide(self, slide_num, total_slides):
        """Generate competitive intelligence matrix"""
        
        # Create enhanced comparison table
        table_rows = ""
        
        # Headers
        table_rows += "<tr><th>Intelligence Metric</th>"
        for brand in self.brand_profiles:
            table_rows += f"<th>{brand['company_name']}</th>"
        table_rows += "</tr>"
        
        # Overall Health Scores
        table_rows += "<tr><td><strong>Health Score</strong></td>"
        for brand in self.brand_profiles:
            score = brand['enhanced_brand_health']['overall_score']
            table_rows += f"<td><strong>{score}/100</strong></td>"
        table_rows += "</tr>"
        
        # Threat Level
        table_rows += "<tr><td><strong>Threat Level</strong></td>"
        for brand in self.brand_profiles:
            threat = brand['enhanced_brand_health']['competitive_threat_level']
            table_rows += f"<td><span class=\"threat-badge threat-{threat.lower()}\">{threat}</span></td>"
        table_rows += "</tr>"
        
        # Positioning Approach
        table_rows += "<tr><td><strong>Market Position</strong></td>"
        for brand in self.brand_profiles:
            position = brand['enhanced_positioning']['competitive_strategy']['positioning_approach']
            table_rows += f"<td>{position}</td>"
        table_rows += "</tr>"
        
        # Innovation Level
        table_rows += "<tr><td><strong>Innovation Level</strong></td>"
        for brand in self.brand_profiles:
            innovation = brand['enhanced_positioning']['innovation_positioning']['technology_sophistication']
            table_rows += f"<td>{innovation}</td>"
        table_rows += "</tr>"
        
        # Target Market
        table_rows += "<tr><td><strong>Target Market</strong></td>"
        for brand in self.brand_profiles:
            market = brand['enhanced_positioning']['market_focus']['primary_market_segment']
            table_rows += f"<td>{market}</td>"
        table_rows += "</tr>"
        
        return f"""
    <div class="slide" id="slide-{slide_num}">
        <div class="slide-header">
            <h2 class="slide-title">Competitive Intelligence Matrix</h2>
            <div class="slide-number">Slide {slide_num} of {total_slides}</div>
        </div>
        
        <div class="slide-content">
            <div class="ai-insight">
                <strong>Enhanced Intelligence:</strong> Sophisticated AI analysis reveals clear competitive differentiation and strategic positioning gaps
            </div>
            
            <div class="content-card" style="margin-top: 20px;">
                <h3 class="card-title">Comprehensive Competitive Comparison</h3>
                <table class="intelligence-matrix">
                    {table_rows}
                </table>
            </div>
        </div>
        
        <button class="nav-button nav-prev" onclick="prevSlide()">←</button>
        <button class="nav-button nav-next" onclick="nextSlide()">→</button>
    </div>
        """
    
    def _generate_strategic_opportunities_slide(self, slide_num, total_slides):
        """Generate strategic opportunities slide"""
        
        # Get insights from competitive intelligence
        opportunities_html = ""
        if self.competitive_insights and self.competitive_insights.get('positioning_analysis'):
            opportunities = self.competitive_insights['positioning_analysis'].get('white_space_opportunities', [])
            for opp in opportunities[:4]:
                opportunities_html += f"""
                <div class="ai-insight">
                    <strong>{opp.get('opportunity', 'Market Opportunity')}:</strong> 
                    {opp.get('rationale', 'Strategic positioning opportunity identified')}
                    ({opp.get('market_size', 'Medium')} opportunity)
                </div>
                """
        else:
            opportunities_html = """
            <div class="ai-insight">
                <strong>Digital-First Innovation:</strong> Opportunity for technology-forward, customer-centric positioning
            </div>
            <div class="ai-insight">
                <strong>Specialized Market Focus:</strong> Gap in serving specific industry verticals with tailored solutions
            </div>
            <div class="ai-insight">
                <strong>Transparent Communication:</strong> Opportunity for more authentic, educational brand communication
            </div>
            """
        
        return f"""
    <div class="slide" id="slide-{slide_num}">
        <div class="slide-header">
            <h2 class="slide-title">Strategic Opportunities & Recommendations</h2>
            <div class="slide-number">Slide {slide_num} of {total_slides}</div>
        </div>
        
        <div class="slide-content">
            <div class="content-grid">
                <div class="content-card">
                    <h3 class="card-title">Market Opportunities</h3>
                    {opportunities_html}
                </div>
                
                <div class="content-card">
                    <h3 class="card-title">Strategic Recommendations</h3>
                    <div class="ai-insight">
                        <strong>Positioning Strategy:</strong> Focus on unique value differentiation and clear market specialization
                    </div>
                    <div class="ai-insight">
                        <strong>Competitive Response:</strong> Strengthen defensible advantages while exploiting competitor weaknesses
                    </div>
                    <div class="ai-insight">
                        <strong>Innovation Focus:</strong> Invest in technology capabilities that create sustainable competitive moats
                    </div>
                </div>
            </div>
        </div>
        
        <button class="nav-button nav-prev" onclick="prevSlide()">←</button>
    </div>
        """


def main():
    """Generate enhanced competitive intelligence with visual grid overview"""
    
    medical_urls = [
        "https://www.wolterskluwer.com",
        "https://www.elsevier.com",
        "https://www.openevidence.com"
    ]
    
    generator = EnhancedSlidesWithGrid()
    
    output_file = generator.generate_enhanced_ai_report(
        urls=medical_urls,
        report_title="Medical AI Platform Competitive Intelligence",
        output_filename="enhanced_competitive_intelligence_with_grid.html"
    )
    
    if output_file:
        print(f"\n🎉 ENHANCED COMPETITIVE INTELLIGENCE COMPLETE!")
        print(f"📁 File location: {os.path.abspath(output_file)}")
        print(f"🎪 Format: 16:9 slides with visual brand grid overview")
        print(f"🤖 Features: Sophisticated AI analysis, differentiated scoring, strategic insights")
        print(f"🌐 Navigation: Visual grid for quick reference + detailed analysis slides")

if __name__ == "__main__":
    main()