#!/usr/bin/env python3
"""
Standalone HTML Grid Generator
Generates the exact 5-row competitive landscape grid as specified
"""

from datetime import datetime

def generate_competitive_grid_html(brand_profiles=None, page_title="There is a huge opportunity in the category"):
    """Generate the exact 5-row competitive landscape grid as HTML"""
    
    # Default financial services example data if none provided
    if not brand_profiles:
        brand_profiles = [
            {
                "company_name": "TD Ameritrade",
                "brand_positioning": "Empowering clients by helping them take control of their financial lives through innovative technology and comprehensive investment solutions designed for today's modern investor.",
                "personality_descriptors": ["Confident", "Wise", "Empowering", "Innovative"],
                "color_palette": ["#00a651", "#003d2b", "#ffffff", "#f5f5f5", "#666666", "#333333"],
                "logo_url": None,
                "visual_style": "Modern technology-focused design"
            },
            {
                "company_name": "Edward Jones",
                "brand_positioning": "Building relationships with individuals they help achieve their financial goals through personal attention and deep thinking about what's important to their clients.",
                "personality_descriptors": ["Personal", "Engaging", "Deep", "Thoughtful"],
                "color_palette": ["#004890", "#00a0dc", "#ffffff", "#f8f8f8", "#555555", "#000000"],
                "logo_url": None,
                "visual_style": "Personal relationship-focused"
            },
            {
                "company_name": "Charles Schwab",
                "brand_positioning": "Championing every client's goals with passion and integrity by providing modern, thoughtful solutions for financial success.",
                "personality_descriptors": ["Modern", "Dynamic", "Persuasive", "Provoking"],
                "color_palette": ["#0033a0", "#ffffff", "#f5f5f5", "#333333", "#e6e6e6", "#999999"],
                "logo_url": None,
                "visual_style": "Clean modern interface"
            },
            {
                "company_name": "John Hancock",
                "brand_positioning": "Offering clients a solid foundation for the financial future through responsible wealth management and insurance solutions.",
                "personality_descriptors": ["Traditional", "Wise", "Responsible", "Cautious"],
                "color_palette": ["#003087", "#f39800", "#ffffff", "#f8f8f8", "#444444", "#888888"],
                "logo_url": None,
                "visual_style": "Traditional professional design"
            },
            {
                "company_name": "Prudential",
                "brand_positioning": "Helping companies and people grow and protect their wealth for 140 years through expertise, innovation, and financial strength.",
                "personality_descriptors": ["Caring", "Realistic", "Reliable", "Protective"],
                "color_palette": ["#0f4c81", "#f79100", "#ffffff", "#f7f7f7", "#666666", "#333333"],
                "logo_url": None,
                "visual_style": "Heritage-focused branding"
            },
            {
                "company_name": "Fidelity",
                "brand_positioning": "Industry pioneers sharing our financial expertise to help people live the lives they want through accessible investing and planning tools.",
                "personality_descriptors": ["Warm", "Grounded", "Supportive", "Expert"],
                "color_palette": ["#00754a", "#f47920", "#ffffff", "#f8f8f8", "#555555", "#000000"],
                "logo_url": None,
                "visual_style": "App design • Web interface"
            },
            {
                "company_name": "Vanguard",
                "brand_positioning": "Leading the industry in putting client's interests first by offering low-cost investment products that deliver long-term value.",
                "personality_descriptors": ["Rational", "Straightforward", "Collaborative", "Optimistic"],
                "color_palette": ["#c5282f", "#ffffff", "#f5f5f5", "#333333", "#666666", "#999999"],
                "logo_url": None,
                "visual_style": "Minimalist design • Clean typography"
            },
            {
                "company_name": "Merrill Lynch",
                "brand_positioning": "Helping people succeed by providing leadership resources and financial guidance backed by the strength of Bank of America.",
                "personality_descriptors": ["Delivers", "Established", "Intelligent", "Modern"],
                "color_palette": ["#0066b2", "#e31837", "#ffffff", "#f8f8f8", "#444444", "#777777"],
                "logo_url": None,
                "visual_style": "Corporate identity • Professional design"
            },
            {
                "company_name": "Morgan Stanley",
                "brand_positioning": "Putting capital to work to benefit people and build a better world through comprehensive wealth management and investment banking.",
                "personality_descriptors": ["Savvy", "Dynamic", "Intellectual", "Creative"],
                "color_palette": ["#00adef", "#f58220", "#ffffff", "#f7f7f7", "#555555", "#333333"],
                "logo_url": None,
                "visual_style": "Brand applications • Visual system"
            },
            {
                "company_name": "Ameriprise",
                "brand_positioning": "We shape financial solutions for a lifetime by helping clients feel confident in their financial decisions and future.",
                "personality_descriptors": ["Approachable", "Genuine", "Knowledgeable", "Responsible"],
                "color_palette": ["#ff6900", "#00b04f", "#ffffff", "#f8f8f8", "#666666", "#444444"],
                "logo_url": None,
                "visual_style": "Consumer-friendly • Approachable design"
            }
        ]
    
    # Ensure we have exactly 10 brands (pad with empty slots if needed)
    while len(brand_profiles) < 10:
        brand_profiles.append({
            "company_name": f"Brand {len(brand_profiles) + 1}",
            "brand_positioning": "Analysis pending...",
            "personality_descriptors": ["TBD", "TBD", "TBD", "TBD"],
            "color_palette": ["#e9ecef", "#dee2e6", "#ced4da", "#adb5bd", "#6c757d", "#495057"],
            "logo_url": None,
            "visual_style": "Pending analysis"
        })
    
    # Truncate to 10 brands if more provided
    brand_profiles = brand_profiles[:10]
    
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Competitive Landscape Analysis - {datetime.now().strftime('%B %d, %Y')}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.4;
            color: #333;
            background: #f8f9fa;
        }}
        
        .page {{
            width: 100vw;
            min-height: 100vh;
            background: white;
            margin: 0;
            padding: 20px;
        }}
        
        .page-header {{
            text-align: center;
            margin-bottom: 30px;
            position: relative;
        }}
        
        .page-number {{
            position: absolute;
            top: 0;
            right: 0;
            font-size: 0.9em;
            color: #6c757d;
            background: white;
            padding: 5px 10px;
            border-radius: 3px;
            border: 1px solid #e9ecef;
        }}
        
        .main-title {{
            font-size: 2.5em;
            font-weight: 700;
            color: #2c3e50;
            margin-bottom: 10px;
            line-height: 1.2;
        }}
        
        .subtitle {{
            font-size: 1.1em;
            color: #6c757d;
            margin-bottom: 5px;
        }}
        
        .analysis-date {{
            font-size: 0.9em;
            color: #8e9ba8;
        }}
        
        /* ===== 5-ROW BRAND GRID SYSTEM ===== */
        .brand-grid-container {{
            background: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            overflow: hidden;
            max-width: 100%;
        }}
        
        .brand-grid {{
            display: grid;
            grid-template-columns: repeat(10, 1fr);
            grid-template-rows: 70px 140px 90px 70px 180px;
            gap: 12px;
            min-height: 550px;
        }}
        
        /* Row 1: Company Logos */
        .logo-cell {{
            grid-row: 1;
            background: white;
            border: 1px solid #e9ecef;
            border-radius: 8px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }}
        
        .brand-logo-img {{
            max-width: 100%;
            max-height: 35px;
            object-fit: contain;
            margin-bottom: 5px;
        }}
        
        .brand-logo-placeholder {{
            width: 100%;
            height: 35px;
            background: linear-gradient(135deg, #e9ecef, #dee2e6);
            border-radius: 4px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.7em;
            color: #6c757d;
            font-weight: 600;
            margin-bottom: 5px;
            text-align: center;
            line-height: 1.1;
        }}
        
        .brand-name {{
            font-size: 0.65em;
            font-weight: 600;
            color: #495057;
            text-align: center;
            line-height: 1.1;
        }}
        
        /* Row 2: Brand Positioning Statements */
        .positioning-cell {{
            grid-row: 2;
            background: white;
            border: 1px solid #e9ecef;
            border-radius: 8px;
            padding: 12px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            overflow: hidden;
        }}
        
        .positioning-text {{
            font-size: 0.75em;
            line-height: 1.3;
            color: #495057;
            text-align: left;
            overflow: hidden;
            display: -webkit-box;
            -webkit-line-clamp: 8;
            -webkit-box-orient: vertical;
        }}
        
        /* Row 3: Brand Personality Descriptors */
        .personality-cell {{
            grid-row: 3;
            background: white;
            border: 1px solid #e9ecef;
            border-radius: 8px;
            padding: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            display: flex;
            flex-direction: column;
            justify-content: flex-start;
        }}
        
        .personality-words {{
            display: flex;
            flex-wrap: wrap;
            gap: 4px;
        }}
        
        .personality-tag {{
            background: #f8f9fa;
            border: 1px solid #e9ecef;
            border-radius: 12px;
            padding: 3px 8px;
            font-size: 0.65em;
            font-weight: 500;
            color: #495057;
            white-space: nowrap;
        }}
        
        /* Row 4: Color Palette Swatches */
        .color-cell {{
            grid-row: 4;
            background: white;
            border: 1px solid #e9ecef;
            border-radius: 8px;
            padding: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            display: flex;
            flex-direction: column;
        }}
        
        .color-swatches {{
            display: grid;
            grid-template-columns: repeat(6, 1fr);
            gap: 3px;
            flex-grow: 1;
        }}
        
        .color-swatch {{
            height: 25px;
            border-radius: 3px;
            border: 1px solid #dee2e6;
            position: relative;
            cursor: pointer;
        }}
        
        .color-labels {{
            font-size: 0.6em;
            color: #6c757d;
            text-align: center;
            margin-top: 4px;
            line-height: 1.1;
        }}
        
        /* Row 5: Visual Assets & Screenshots */
        .visual-cell {{
            grid-row: 5;
            background: white;
            border: 1px solid #e9ecef;
            border-radius: 8px;
            padding: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            display: flex;
            flex-direction: column;
        }}
        
        .screenshot-container {{
            flex-grow: 1;
            background: #f8f9fa;
            border-radius: 4px;
            border: 1px solid #e9ecef;
            overflow: hidden;
            position: relative;
            margin-bottom: 6px;
        }}
        
        .screenshot-placeholder {{
            width: 100%;
            height: 100%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.7em;
            color: #6c757d;
            text-align: center;
            line-height: 1.2;
        }}
        
        .visual-assets-list {{
            font-size: 0.6em;
            color: #6c757d;
            line-height: 1.2;
        }}
        
        /* Grid positioning for each brand column */
        .brand-col-1 {{ grid-column: 1; }}
        .brand-col-2 {{ grid-column: 2; }}
        .brand-col-3 {{ grid-column: 3; }}
        .brand-col-4 {{ grid-column: 4; }}
        .brand-col-5 {{ grid-column: 5; }}
        .brand-col-6 {{ grid-column: 6; }}
        .brand-col-7 {{ grid-column: 7; }}
        .brand-col-8 {{ grid-column: 8; }}
        .brand-col-9 {{ grid-column: 9; }}
        .brand-col-10 {{ grid-column: 10; }}
        
        /* Responsive Design */
        @media (max-width: 1200px) {{
            .brand-grid {{
                grid-template-columns: repeat(5, 1fr);
            }}
            
            .brand-col-1, .brand-col-6 {{ grid-column: 1; }}
            .brand-col-2, .brand-col-7 {{ grid-column: 2; }}
            .brand-col-3, .brand-col-8 {{ grid-column: 3; }}
            .brand-col-4, .brand-col-9 {{ grid-column: 4; }}
            .brand-col-5, .brand-col-10 {{ grid-column: 5; }}
        }}
        
        @media print {{
            .page {{
                page-break-after: always;
                width: 210mm;
                min-height: 297mm;
            }}
            
            body {{
                print-color-adjust: exact;
                -webkit-print-color-adjust: exact;
            }}
        }}
    </style>
</head>
<body>
    <div class="page">
        <div class="page-header">
            <div class="page-number">Page 1</div>
            <h1 class="main-title">{page_title}</h1>
            <p class="subtitle">Competitive Landscape Analysis</p>
            <p class="analysis-date">Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
        </div>
        
        <div class="brand-grid-container">
            <div class="brand-grid">"""

    # Generate grid cells for each brand
    for i, brand in enumerate(brand_profiles, 1):
        col_class = f"brand-col-{i}"
        
        # Row 1: Company Logos
        logo_html = f'<img src="{brand["logo_url"]}" alt="{brand["company_name"]} logo" class="brand-logo-img">' if brand.get("logo_url") else f'<div class="brand-logo-placeholder">{brand["company_name"].upper()}</div>'
        
        html_content += f"""
                <!-- Brand {i}: {brand["company_name"]} -->
                <!-- Row 1: Logo -->
                <div class="logo-cell {col_class}">
                    {logo_html}
                    <div class="brand-name">{brand["company_name"]}</div>
                </div>
                
                <!-- Row 2: Positioning -->
                <div class="positioning-cell {col_class}">
                    <div class="positioning-text">{brand["brand_positioning"]}</div>
                </div>
                
                <!-- Row 3: Personality -->
                <div class="personality-cell {col_class}">
                    <div class="personality-words">"""
        
        # Add personality tags
        for descriptor in brand["personality_descriptors"]:
            html_content += f'<span class="personality-tag">{descriptor}</span>'
        
        html_content += f"""
                    </div>
                </div>
                
                <!-- Row 4: Colors -->
                <div class="color-cell {col_class}">
                    <div class="color-swatches">"""
        
        # Add color swatches
        for color in brand["color_palette"]:
            html_content += f'<div class="color-swatch" style="background-color: {color};"></div>'
        
        # Add primary colors in labels
        primary_colors = " • ".join(brand["color_palette"][:3])
        html_content += f"""
                    </div>
                    <div class="color-labels">{primary_colors}</div>
                </div>
                
                <!-- Row 5: Visual Assets -->
                <div class="visual-cell {col_class}">
                    <div class="screenshot-container">
                        <div class="screenshot-placeholder">Homepage Screenshot</div>
                    </div>
                    <div class="visual-assets-list">{brand["visual_style"]} • Brand materials</div>
                </div>"""
    
    html_content += """
            </div>
        </div>
    </div>
</body>
</html>"""
    
    return html_content

def main():
    """Generate the competitive landscape grid HTML file"""
    print("🎯 Generating Competitive Landscape Grid...")
    
    # Generate the HTML
    html_content = generate_competitive_grid_html()
    
    # Save to file
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_filename = f"competitive_landscape_grid_{timestamp}.html"
    
    try:
        with open(output_filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ SUCCESS! Your competitive landscape grid is ready!")
        print(f"📁 File: {output_filename}")
        print(f"🌐 Open this HTML file in your browser")
        print(f"📊 Features:")
        print(f"   • 5-Row Grid Layout (Logos, Positioning, Personality, Colors, Visuals)")
        print(f"   • 10 Financial Services Brands")
        print(f"   • Professional Print-Ready Format")
        print(f"   • Responsive Design")
        print(f"   • Color Palette Analysis")
        
    except Exception as e:
        print(f"❌ Error saving file: {e}")

if __name__ == "__main__":
    main()