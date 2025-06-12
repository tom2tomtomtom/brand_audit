"""
Report Generator Module
Generates professional PDF reports using ReportLab
"""

import os
import time
import logging
from typing import Dict, List
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import Color, HexColor
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle,
    PageBreak, KeepTogether, HRFlowable
)
from reportlab.platypus.frames import Frame
from reportlab.platypus.doctemplate import PageTemplate
from reportlab.graphics.shapes import Drawing, Rect
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from datetime import datetime
import requests
from io import BytesIO

logger = logging.getLogger(__name__)

class ReportGenerator:
    def __init__(self):
        """Initialize the report generator"""
        self.styles = getSampleStyleSheet()
        self.setup_custom_styles()
        
        # Brand colors (professional blue theme)
        self.primary_color = HexColor('#1e40af')
        self.secondary_color = HexColor('#3b82f6')
        self.accent_color = HexColor('#0ea5e9')
        self.text_color = HexColor('#1f2937')
        self.light_gray = HexColor('#f3f4f6')
        
    def setup_custom_styles(self):
        """Setup custom paragraph styles"""
        # Title style
        if 'CustomTitle' not in self.styles:
            self.styles.add(ParagraphStyle(
                name='CustomTitle',
                parent=self.styles['Heading1'],
                fontSize=24,
                spaceAfter=30,
                textColor=HexColor('#1e40af'),
                alignment=TA_CENTER
            ))
        
        # Section heading
        if 'SectionHead' not in self.styles:
            self.styles.add(ParagraphStyle(
                name='SectionHead',
                parent=self.styles['Heading2'],
                fontSize=16,
                spaceAfter=12,
                spaceBefore=20,
                textColor=HexColor('#1e40af'),
                borderWidth=0,
                borderColor=HexColor('#1e40af'),
                borderPadding=5
            ))
        
        # Subsection heading
        if 'SubHead' not in self.styles:
            self.styles.add(ParagraphStyle(
                name='SubHead',
                parent=self.styles['Heading3'],
                fontSize=14,
                spaceAfter=8,
                spaceBefore=12,
                textColor=HexColor('#374151')
            ))
        
        # Body text
        if 'CustomBodyText' not in self.styles:
            self.styles.add(ParagraphStyle(
                name='CustomBodyText',
                parent=self.styles['Normal'],
                fontSize=11,
                spaceAfter=8,
                alignment=TA_JUSTIFY,
                textColor=HexColor('#1f2937')
            ))
        
        # Bullet points
        if 'BulletText' not in self.styles:
            self.styles.add(ParagraphStyle(
                name='BulletText',
                parent=self.styles['Normal'],
                fontSize=10,
                spaceAfter=4,
                leftIndent=20,
                bulletIndent=10,
                textColor=HexColor('#374151')
            ))
    
    def generate_report(self, brand_data_list: List[Dict], analysis_results: List[Dict], 
                       comparative_analysis: Dict, output_path: str):
        """Generate the complete PDF report"""
        logger.info(f"Generating PDF report with {len(brand_data_list)} brands")
        
        try:
            # Create document
            doc = SimpleDocTemplate(
                output_path,
                pagesize=A4,
                rightMargin=72,
                leftMargin=72,
                topMargin=72,
                bottomMargin=18
            )
            
            # Build content
            story = []
            
            # Cover page
            story.extend(self.create_cover_page(len(brand_data_list)))
            story.append(PageBreak())
            
            # Executive summary
            story.extend(self.create_executive_summary(analysis_results, comparative_analysis))
            story.append(PageBreak())
            
            # Individual brand analyses
            for i, (brand_data, analysis) in enumerate(zip(brand_data_list, analysis_results)):
                story.extend(self.create_brand_analysis_section(brand_data, analysis, i + 1))
                if i < len(brand_data_list) - 1:  # Don't add page break after last brand
                    story.append(PageBreak())
            
            # Comparative analysis
            story.append(PageBreak())
            story.extend(self.create_comparative_analysis_section(comparative_analysis, analysis_results))
            
            # Recommendations
            story.append(PageBreak())
            story.extend(self.create_recommendations_section(analysis_results))
            
            # Build PDF
            doc.build(story)
            
            logger.info(f"PDF report generated successfully: {output_path}")
            
        except Exception as e:
            logger.error(f"Error generating PDF report: {str(e)}")
            raise
    
    def create_cover_page(self, brand_count: int) -> List:
        """Create the cover page"""
        content = []
        
        # Add some space from top
        content.append(Spacer(1, 2*inch))
        
        # Main title
        title = Paragraph("Brand Competitive Analysis Report", self.styles['CustomTitle'])
        content.append(title)
        content.append(Spacer(1, 0.5*inch))
        
        # Subtitle
        subtitle = Paragraph(
            f"Comprehensive Analysis of {brand_count} Competing Brands",
            self.styles['Heading2']
        )
        content.append(subtitle)
        content.append(Spacer(1, 1*inch))
        
        # Report details
        report_date = datetime.now().strftime("%B %d, %Y")
        details = [
            f"<b>Report Date:</b> {report_date}",
            f"<b>Brands Analyzed:</b> {brand_count}",
            f"<b>Analysis Type:</b> Digital Brand Audit & Competitive Analysis",
            f"<b>Generated by:</b> Brand Analysis Tool"
        ]
        
        for detail in details:
            content.append(Paragraph(detail, self.styles['CustomBodyText']))
            content.append(Spacer(1, 12))
        
        content.append(Spacer(1, 1*inch))
        
        # Disclaimer
        disclaimer = """
        <i>This report contains confidential and proprietary information. The analysis and 
        recommendations contained herein are based on publicly available information and 
        automated analysis tools. Results should be validated through additional research 
        and professional judgment.</i>
        """
        content.append(Paragraph(disclaimer, self.styles['CustomBodyText']))
        
        return content
    
    def create_executive_summary(self, analysis_results: List[Dict], 
                                comparative_analysis: Dict) -> List:
        """Create executive summary section"""
        content = []
        
        content.append(Paragraph("Executive Summary", self.styles['SectionHead']))
        content.append(Spacer(1, 12))
        
        # Overview
        overview = f"""
        This report presents a comprehensive competitive analysis of {len(analysis_results)} brands 
        within their respective market segments. The analysis examines digital presence, brand 
        positioning, content strategy, and competitive advantages to provide actionable insights 
        for strategic decision-making.
        """
        content.append(Paragraph(overview, self.styles['CustomBodyText']))
        content.append(Spacer(1, 16))
        
        # Key findings
        content.append(Paragraph("Key Findings", self.styles['SubHead']))
        
        # Calculate summary statistics
        total_scores = []
        industries = []
        
        for analysis in analysis_results:
            if analysis.get('overall_score', {}).get('total_score'):
                try:
                    score = int(analysis['overall_score']['total_score'].split('/')[0])
                    total_scores.append(score)
                except:
                    pass
            
            if analysis.get('industry'):
                industries.append(analysis['industry'])
        
        if total_scores:
            avg_score = sum(total_scores) / len(total_scores)
            top_score = max(total_scores)
            findings = [
                f"Average competitive score across all brands: {avg_score:.1f}/100",
                f"Highest performing brand scored: {top_score}/100",
                f"Primary industries represented: {', '.join(set(industries[:3]))}",
                "All brands demonstrate established digital presence",
                "Opportunities identified for enhanced user experience and content strategy"
            ]
        else:
            findings = [
                "Comprehensive digital presence analysis completed",
                "Brand positioning and messaging strategies evaluated",
                "Technical infrastructure and user experience assessed",
                "Competitive strengths and opportunities identified"
            ]
        
        for finding in findings:
            content.append(Paragraph(f"• {finding}", self.styles['BulletText']))
        
        content.append(Spacer(1, 16))
        
        # Methodology
        content.append(Paragraph("Analysis Methodology", self.styles['SubHead']))
        methodology = """
        This analysis employed a multi-stage approach combining automated web scraping, 
        content analysis, visual asset extraction, and AI-powered brand assessment. Each brand's 
        digital presence was comprehensively evaluated across multiple dimensions including 
        website quality, user experience, content strategy, and competitive positioning.
        """
        content.append(Paragraph(methodology, self.styles['CustomBodyText']))
        
        return content
    
    def create_brand_analysis_section(self, brand_data: Dict, analysis: Dict, 
                                    brand_number: int) -> List:
        """Create individual brand analysis section"""
        content = []
        
        brand_name = brand_data.get('name', f'Brand {brand_number}')
        
        # Section header
        content.append(Paragraph(f"Brand Analysis #{brand_number}: {brand_name}", 
                                self.styles['SectionHead']))
        content.append(Spacer(1, 12))
        
        # Brand overview
        content.append(Paragraph("Brand Overview", self.styles['SubHead']))
        
        # Basic information table
        basic_info = [
            ['Website', brand_data.get('url', 'N/A')],
            ['Industry', analysis.get('industry', 'N/A')],
            ['Business Model', analysis.get('business_model', 'N/A')],
            ['Company Size', analysis.get('company_size', 'N/A')],
            ['Analysis Date', brand_data.get('scraped_at', 'N/A')]
        ]
        
        basic_table = Table(basic_info, colWidths=[2*inch, 4*inch])
        basic_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), self.light_gray),
            ('TEXTCOLOR', (0, 0), (-1, -1), self.text_color),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))
        
        content.append(basic_table)
        content.append(Spacer(1, 16))
        
        # Brand identity
        brand_identity = analysis.get('brand_identity', {})
        if brand_identity:
            content.append(Paragraph("Brand Identity", self.styles['SubHead']))
            
            identity_items = [
                ('Value Proposition', brand_identity.get('value_proposition')),
                ('Target Audience', brand_identity.get('target_audience')),
                ('Brand Personality', brand_identity.get('brand_personality')),
                ('Positioning', brand_identity.get('positioning_statement'))
            ]
            
            for label, value in identity_items:
                if value:
                    content.append(Paragraph(f"<b>{label}:</b> {value}", self.styles['CustomBodyText']))
            
            content.append(Spacer(1, 16))
        
        # Digital presence scores
        digital_presence = analysis.get('digital_presence', {})
        if digital_presence:
            content.append(Paragraph("Digital Presence Assessment", self.styles['SubHead']))
            
            # Create scores table
            scores_data = [['Metric', 'Score', 'Assessment']]
            
            for metric, score_info in digital_presence.items():
                if isinstance(score_info, str) and '/' in score_info:
                    score_part = score_info.split(' - ')
                    score = score_part[0]
                    assessment = score_part[1] if len(score_part) > 1 else 'Standard'
                    metric_name = metric.replace('_', ' ').title()
                    scores_data.append([metric_name, score, assessment])
            
            if len(scores_data) > 1:
                scores_table = Table(scores_data, colWidths=[2*inch, 1*inch, 3*inch])
                scores_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), self.primary_color),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                    ('FONTSIZE', (0, 0), (-1, -1), 9),
                    ('GRID', (0, 0), (-1, -1), 1, colors.grey),
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ]))
                
                content.append(scores_table)
                content.append(Spacer(1, 16))
        
        # Competitive analysis
        competitive = analysis.get('competitive_analysis', {})
        if competitive:
            content.append(Paragraph("Competitive Analysis", self.styles['SubHead']))
            
            # Strengths
            strengths = competitive.get('key_strengths', [])
            if strengths:
                content.append(Paragraph("<b>Key Strengths:</b>", self.styles['CustomBodyText']))
                for strength in strengths[:5]:
                    content.append(Paragraph(f"• {strength}", self.styles['BulletText']))
                content.append(Spacer(1, 8))
            
            # Weaknesses
            weaknesses = competitive.get('key_weaknesses', [])
            if weaknesses:
                content.append(Paragraph("<b>Areas for Improvement:</b>", self.styles['CustomBodyText']))
                for weakness in weaknesses[:4]:
                    content.append(Paragraph(f"• {weakness}", self.styles['BulletText']))
                content.append(Spacer(1, 8))
            
            # Opportunities
            opportunities = competitive.get('opportunities', [])
            if opportunities:
                content.append(Paragraph("<b>Market Opportunities:</b>", self.styles['CustomBodyText']))
                for opportunity in opportunities[:3]:
                    content.append(Paragraph(f"• {opportunity}", self.styles['BulletText']))
        
        return content
    
    def create_comparative_analysis_section(self, comparative_analysis: Dict, 
                                          analysis_results: List[Dict]) -> List:
        """Create comparative analysis section"""
        content = []
        
        content.append(Paragraph("Comparative Analysis", self.styles['SectionHead']))
        content.append(Spacer(1, 12))
        
        # Market overview
        content.append(Paragraph("Market Overview", self.styles['SubHead']))
        
        if comparative_analysis:
            brand_count = comparative_analysis.get('brand_count', len(analysis_results))
            industries = comparative_analysis.get('industries_represented', [])
            
            overview = f"""
            This analysis covers {brand_count} brands across {len(set(industries))} industry 
            segments. The competitive landscape shows diverse approaches to digital presence 
            and brand positioning, with opportunities for differentiation and market leadership.
            """
            content.append(Paragraph(overview, self.styles['CustomBodyText']))
            content.append(Spacer(1, 16))
        
        # Performance comparison
        content.append(Paragraph("Performance Comparison", self.styles['SubHead']))
        
        # Create performance comparison table
        comparison_data = [['Brand', 'Overall Score', 'Industry', 'Key Strength']]
        
        for analysis in analysis_results:
            brand_name = analysis.get('brand_name', 'Unknown')
            
            # Extract overall score
            overall_score = analysis.get('overall_score', {})
            score = overall_score.get('total_score', 'N/A')
            
            industry = analysis.get('industry', 'N/A')
            
            # Get top strength
            strengths = analysis.get('competitive_analysis', {}).get('key_strengths', [])
            top_strength = strengths[0] if strengths else 'Professional presentation'
            
            comparison_data.append([brand_name, score, industry, top_strength])
        
        if len(comparison_data) > 1:
            comparison_table = Table(comparison_data, colWidths=[1.5*inch, 1*inch, 1.5*inch, 2*inch])
            comparison_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), self.primary_color),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('GRID', (0, 0), (-1, -1), 1, colors.grey),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ]))
            
            content.append(comparison_table)
            content.append(Spacer(1, 16))
        
        # Common patterns
        if comparative_analysis:
            common_strengths = comparative_analysis.get('common_strengths', [])
            common_weaknesses = comparative_analysis.get('common_weaknesses', [])
            
            if common_strengths:
                content.append(Paragraph("Industry Strengths", self.styles['SubHead']))
                for strength in common_strengths[:5]:
                    content.append(Paragraph(f"• {strength.title()}", self.styles['BulletText']))
                content.append(Spacer(1, 12))
            
            if common_weaknesses:
                content.append(Paragraph("Common Improvement Areas", self.styles['SubHead']))
                for weakness in common_weaknesses[:5]:
                    content.append(Paragraph(f"• {weakness.title()}", self.styles['BulletText']))
        
        return content
    
    def create_recommendations_section(self, analysis_results: List[Dict]) -> List:
        """Create strategic recommendations section"""
        content = []
        
        content.append(Paragraph("Strategic Recommendations", self.styles['SectionHead']))
        content.append(Spacer(1, 12))
        
        # Aggregate recommendations across all brands
        all_immediate = []
        all_medium_term = []
        all_long_term = []
        
        for analysis in analysis_results:
            strategic_recs = analysis.get('strategic_recommendations', {})
            
            all_immediate.extend(strategic_recs.get('immediate_priorities', []))
            all_medium_term.extend(strategic_recs.get('medium_term_goals', []))
            all_long_term.extend(strategic_recs.get('long_term_vision', []))
        
        # Immediate priorities
        if all_immediate:
            content.append(Paragraph("Immediate Priorities (0-3 months)", self.styles['SubHead']))
            
            # Get unique recommendations
            unique_immediate = list(set(all_immediate))[:6]
            for rec in unique_immediate:
                content.append(Paragraph(f"• {rec}", self.styles['BulletText']))
            
            content.append(Spacer(1, 16))
        
        # Medium-term goals
        if all_medium_term:
            content.append(Paragraph("Medium-term Goals (3-12 months)", self.styles['SubHead']))
            
            unique_medium = list(set(all_medium_term))[:6]
            for rec in unique_medium:
                content.append(Paragraph(f"• {rec}", self.styles['BulletText']))
            
            content.append(Spacer(1, 16))
        
        # Long-term vision
        if all_long_term:
            content.append(Paragraph("Long-term Strategic Vision (12+ months)", self.styles['SubHead']))
            
            unique_long = list(set(all_long_term))[:4]
            for rec in unique_long:
                content.append(Paragraph(f"• {rec}", self.styles['BulletText']))
            
            content.append(Spacer(1, 16))
        
        # Implementation notes
        content.append(Paragraph("Implementation Notes", self.styles['SubHead']))
        implementation_notes = """
        These recommendations are based on comprehensive analysis of competitive digital presence 
        and industry best practices. Priority should be given to initiatives that address multiple 
        improvement areas while aligning with overall business strategy and available resources.
        
        Regular monitoring and measurement of implementation progress is recommended to ensure 
        optimal results and ROI from strategic investments.
        """
        content.append(Paragraph(implementation_notes, self.styles['CustomBodyText']))
        
        return content