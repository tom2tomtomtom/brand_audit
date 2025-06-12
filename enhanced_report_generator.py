import json
import os
from datetime import datetime
from jinja2 import Template

class EnhancedReportGenerator:
    def __init__(self, template_path=None):
        self.template_path = template_path or "enhanced_brand_audit_template.html"
        
    def load_template(self):
        """Load the HTML template"""
        try:
            with open(self.template_path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            print(f"Template file not found: {self.template_path}")
            return None
    
    def generate_grid_html(self, brand_data):
        """Generate the 5-row grid HTML for competitive landscape"""
        if not brand_data or len(brand_data) == 0:
            return self._generate_placeholder_grid()
        
        # Ensure we have exactly 10 brands for the grid
        brands = brand_data[:10]  # Take first 10
        while len(brands) < 10:
            brands.append(self._get_placeholder_brand(len(brands) + 1))
        
        grid_html = ""
        
        # Row 1: Company Logos
        for i, brand in enumerate(brands, 1):
            logo_html = f'''
                <div class="logo-cell brand-col-{i}">
                    <div class="brand-logo-placeholder">{brand.get("name", f"BRAND {i}").upper()}</div>
                    <div class="brand-name">{brand.get("name", f"Brand {i}")}</div>
                </div>'''
            grid_html += logo_html
        
        # Row 2: Brand Positioning Statements
        for i, brand in enumerate(brands, 1):
            positioning = brand.get("positioning", "No positioning statement available.")
            positioning_html = f'''
                <div class="positioning-cell brand-col-{i}">
                    <div class="positioning-text">{positioning}</div>
                </div>'''
            grid_html += positioning_html
        
        # Row 3: Brand Personality Descriptors
        for i, brand in enumerate(brands, 1):
            personality_words = brand.get("personality", ["Professional", "Reliable", "Modern"])[:4]
            tags_html = "".join([f'<span class="personality-tag">{word}</span>' for word in personality_words])
            personality_html = f'''
                <div class="personality-cell brand-col-{i}">
                    <div class="personality-words">
                        {tags_html}
                    </div>
                </div>'''
            grid_html += personality_html
        
        # Row 4: Color Palette Swatches
        for i, brand in enumerate(brands, 1):
            colors = brand.get("colors", ["#666666", "#999999", "#cccccc"])[:6]
            swatches_html = "".join([f'<div class="color-swatch" style="background-color: {color};"></div>' for color in colors])
            color_labels = " • ".join(colors[:3])
            colors_html = f'''
                <div class="color-cell brand-col-{i}">
                    <div class="color-swatches">
                        {swatches_html}
                    </div>
                    <div class="color-labels">{color_labels}</div>
                </div>'''
            grid_html += colors_html
        
        # Row 5: Visual Assets & Screenshots
        for i, brand in enumerate(brands, 1):
            visual_assets = brand.get("visual_assets", {})
            elements = visual_assets.get("elements", ["Website design", "Brand materials"])
            elements_text = " • ".join(elements[:3])
            visuals_html = f'''
                <div class="visual-cell brand-col-{i}">
                    <div class="screenshot-container">
                        <div class="screenshot-placeholder">Homepage Screenshot</div>
                    </div>
                    <div class="visual-assets-list">{elements_text}</div>
                </div>'''
            grid_html += visuals_html
        
        return grid_html
    
    def generate_stripe_pages(self, brand_data):
        """Generate Stripe-style deep-dive pages for each brand"""
        if not brand_data:
            return ""
        
        pages_html = ""
        
        for brand in brand_data[:5]:  # Generate deep-dive for first 5 brands
            brand_name = brand.get("name", "Unknown Brand")
            
            # Strategy framework
            strategy_html = f'''
                <div class="framework-item">
                    <strong>Why:</strong> {brand.get("story", "Brand mission and purpose")}
                </div>
                <div class="framework-item">
                    <strong>How:</strong> {brand.get("voice", "Brand approach and methodology")}
                </div>
                <div class="framework-item">
                    <strong>What:</strong> {", ".join(brand.get("messages", ["Products and services"]))}
                </div>
                <div class="framework-item">
                    <strong>Who:</strong> {brand.get("target_audience", "Target customer base")}
                </div>'''
            
            # Messaging analysis
            personality_list = "".join([f'<li>{trait}</li>' for trait in brand.get("personality", ["Professional"])[:4]])
            messages_list = "".join([f'<li>{msg}</li>' for msg in brand.get("messages", ["Key value proposition"])[:3]])
            differentiators_list = "".join([f'<li>{diff}</li>' for diff in brand.get("differentiators", ["Unique approach"])[:2]])
            
            messaging_html = f'''
                <div class="messaging-characteristics">
                    <h4>Voice Characteristics:</h4>
                    <ul>
                        {personality_list}
                    </ul>
                </div>
                
                <div class="key-messages">
                    <h4>Key Messages:</h4>
                    <ul>
                        {messages_list}
                    </ul>
                </div>
                
                <div class="takeaway">
                    <h4>Takeaway:</h4>
                    <ul>
                        {differentiators_list}
                    </ul>
                </div>'''
            
            page_html = f'''
    <!-- PAGE {brand_data.index(brand) + 2}: {brand_name.upper()} DEEP-DIVE -->
    <div class="page brand-deep-dive-page">
        <div class="brand-header">
            <div class="brand-header-logo">
                <div class="brand-logo-placeholder" style="font-size: 0.9em;">{brand_name.upper()}</div>
            </div>
            <div class="brand-header-info">
                <h1>{brand_name}</h1>
                <p class="subtitle">Brand Strategy & Verbal Expression</p>
            </div>
        </div>
        
        <div class="two-column-layout">
            <div class="strategy-framework">
                <h3>Strategy</h3>
                {strategy_html}
            </div>
            
            <div class="messaging-analysis">
                <h3>Messaging</h3>
                {messaging_html}
            </div>
        </div>
    </div>'''
            
            pages_html += page_html
        
        return pages_html
    
    def generate_enhanced_report(self, brand_data_list, output_filename="enhanced_brand_audit.html"):
        """Generate the complete enhanced brand audit report"""
        template_content = self.load_template()
        if not template_content:
            return False
        
        # Prepare data
        report_data = {
            "page_title": "There is a huge opportunity in the category",
            "subtitle": "Competitive Landscape Analysis",
            "analysis_date": datetime.now().strftime("%B %d, %Y"),
            "brands": brand_data_list
        }
        
        # Generate grid HTML
        grid_html = self.generate_grid_html(brand_data_list)
        
        # Generate Stripe-style pages
        stripe_pages_html = self.generate_stripe_pages(brand_data_list)
        
        # Replace placeholders in template
        enhanced_html = template_content.replace(
            '<!-- BRAND GRID PLACEHOLDER -->', 
            grid_html
        ).replace(
            '<!-- STRIPE PAGES PLACEHOLDER -->', 
            stripe_pages_html
        )
        
        # Update title and subtitle
        enhanced_html = enhanced_html.replace(
            'There is a huge opportunity in the category',
            report_data["page_title"]
        ).replace(
            'Competitive Landscape Analysis - Financial Services',
            f'Competitive Landscape Analysis - {report_data["analysis_date"]}'
        )
        
        # Save the report
        try:
            with open(output_filename, 'w', encoding='utf-8') as f:
                f.write(enhanced_html)
            print(f"Enhanced brand audit report generated: {output_filename}")
            return True
        except Exception as e:
            print(f"Error saving report: {e}")
            return False
    
    def _generate_placeholder_grid(self):
        """Generate placeholder grid when no data is available"""
        placeholder_brands = [self._get_placeholder_brand(i) for i in range(1, 11)]
        return self.generate_grid_html(placeholder_brands)
    
    def _get_placeholder_brand(self, index):
        """Get placeholder brand data"""
        return {
            "name": f"Brand {index}",
            "positioning": "Placeholder positioning statement for competitive analysis grid layout.",
            "personality": ["Professional", "Modern", "Reliable", "Innovative"],
            "colors": ["#666666", "#999999", "#cccccc", "#e0e0e0", "#f5f5f5", "#333333"],
            "visual_assets": {
                "elements": ["Website design", "Brand materials", "Social media"]
            },
            "messages": ["Key value proposition", "Secondary message"],
            "voice": "Professional and informative brand voice",
            "differentiators": ["Unique approach", "Market leadership"],
            "story": "Brand mission and purpose statement"
        }

# Integration function for Flask app
def generate_report_from_profiles(brand_profiles, output_path="enhanced_brand_audit.html"):
    """Main function to generate report from brand profiles"""
    generator = EnhancedReportGenerator()
    
    # Convert profiles to report format
    brand_data = []
    for profile in brand_profiles:
        brand_item = {
            "name": profile.get("company_name", "Unknown"),
            "positioning": profile.get("brand_positioning", "No positioning available"),
            "personality": profile.get("personality_descriptors", ["Professional"])[:4],
            "colors": profile.get("color_palette", ["#666666"])[:6],
            "visual_assets": profile.get("screenshot_data", {"elements": ["Website"]}),
            "messages": profile.get("primary_messages", ["Value proposition"]),
            "voice": profile.get("brand_voice", "Professional"),
            "differentiators": profile.get("key_differentiators", ["Unique approach"]),
            "story": profile.get("brand_story", "Brand mission"),
            "target_audience": profile.get("target_audience", "Target customers")
        }
        brand_data.append(brand_item)
    
    return generator.generate_enhanced_report(brand_data, output_path)

if __name__ == "__main__":
    # Test with sample data
    sample_brands = [
        {
            "name": "TD Ameritrade",
            "positioning": "Empowering clients by helping them take control of their financial lives through innovative technology and comprehensive investment solutions.",
            "personality": ["Confident", "Wise", "Empowering", "Innovative"],
            "colors": ["#00a651", "#003d2b", "#ffffff", "#f5f5f5", "#666666", "#333333"],
            "visual_assets": {"elements": ["Homepage", "Trading platform", "Mobile app"]},
            "messages": ["Take control of your financial future", "Advanced trading tools", "Educational resources"],
            "voice": "Confident and empowering",
            "differentiators": ["Technology leadership", "Educational focus"],
            "story": "Democratizing investing through technology and education"
        }
    ]
    
    generator = EnhancedReportGenerator()
    success = generator.generate_enhanced_report(sample_brands, "test_enhanced_report.html")
    if success:
        print("Test report generated successfully!")
    else:
        print("Failed to generate test report.")