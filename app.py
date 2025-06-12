import os
from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
from dotenv import load_dotenv
from openai import OpenAI
import pandas as pd
import sys
import importlib.util
import json
from datetime import datetime

# Load environment variables
load_dotenv()

# Configure API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
# For compatibility with legacy scripts
import openai
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)
# Enable CORS for all routes with additional settings
CORS(app, resources={r"/*": {"origins": "*", "allow_headers": ["Content-Type"], "methods": ["GET", "POST", "OPTIONS"]}}, supports_credentials=True)

# Import the modules from each script
def import_module_from_file(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module

# Import scripts
project_dir = os.path.join(os.path.dirname(__file__), "Project")
competitor_profiler = import_module_from_file(
    "competitor_profiler", 
    os.path.join(project_dir, "Competitor and Product Profiler.py")
)
news_filter = import_module_from_file(
    "news_filter", 
    os.path.join(project_dir, "Filtering News Articles.py")
)
website_filter = import_module_from_file(
    "website_filter", 
    os.path.join(project_dir, "Website Content Filter.py")
)

# Import enhanced brand profiler
enhanced_profiler = import_module_from_file(
    "enhanced_profiler",
    os.path.join(os.path.dirname(__file__), "enhanced_brand_profiler.py")
)
enhanced_generator = import_module_from_file(
    "enhanced_generator",
    os.path.join(os.path.dirname(__file__), "enhanced_report_generator.py")
)

@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html>
        <head>
            <title>Competitor Intelligence API</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 0; padding: 20px; line-height: 1.6; }
                h1 { color: #333; }
                .container { max-width: 800px; margin: 0 auto; }
                .endpoint { background: #f5f5f5; padding: 15px; margin-bottom: 15px; border-radius: 5px; }
                pre { background: #eee; padding: 10px; border-radius: 3px; overflow-x: auto; }
                code { font-family: monospace; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Competitor Intelligence API</h1>
                <p>Use the following endpoints to access the competitive intelligence tools:</p>
                
                <div class="endpoint">
                    <h2>1. Competitor and Product Profiler</h2>
                    <p>Scrapes and analyzes competitor websites to extract company and product information.</p>
                    <p><strong>Endpoint:</strong> /scrape_competitor</p>
                    <p><strong>Method:</strong> POST</p>
                    <p><strong>Parameters:</strong></p>
                    <pre><code>{"url": "https://example.com"}</code></pre>
                </div>
                
                <div class="endpoint">
                    <h2>2. News Article Filter</h2>
                    <p>Filters news articles and extracts main takeaways about gut health products.</p>
                    <p><strong>Endpoint:</strong> /filter_news</p>
                    <p><strong>Method:</strong> GET</p>
                </div>
                
                <div class="endpoint">
                    <h2>3. Download Results</h2>
                    <p>Download the processed data as Excel files.</p>
                    <p><strong>Endpoint:</strong> /download/&lt;filename&gt;</p>
                    <p><strong>Method:</strong> GET</p>
                    <p><strong>Available files:</strong></p>
                    <ul>
                        <li><a href="/download/company_product_info.csv">company_product_info.csv</a></li>
                        <li><a href="/download/filtered_articles.xlsx">filtered_articles.xlsx</a></li>
                        <li><a href="/download/filtered_articles_extra.xlsx">filtered_articles_extra.xlsx</a></li>
                    </ul>
                </div>
            </div>
        </body>
    </html>
    '''

@app.route('/scrape_competitor', methods=['POST'])
def scrape_competitor():
    data = request.json
    url = data.get('url')
    
    if not url:
        return jsonify({"error": "URL is required"}), 400
    
    try:
        competitor_profiler.scrape_and_analyze(url)
        return jsonify({"status": "success", "message": "Data saved to company_product_info.csv"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/find-competitors', methods=['POST'])
def find_competitors():
    data = request.json
    url = data.get('url')
    
    if not url:
        return jsonify({"error": "URL is required"}), 400
    
    try:
        # Here we would use OpenAI to analyze the website and find competitors
        # For now, let's return mock data
        prompt = f"""
        Analyze the following website URL: {url}
        
        Identify 3-5 likely competitors in the same industry or market space.
        For each competitor, provide:
        1. Company name
        2. Website URL
        
        Return the results in JSON format with an array of objects containing 'name' and 'url' properties.
        """
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an AI that analyzes websites and identifies competitors."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )
        
        # Parse the response
        content = response.choices[0].message.content.strip()
        
        # Extract JSON from the response (it might be surrounded by markdown code blocks)
        import re
        json_match = re.search(r'```json\n([\s\S]*?)\n```', content)
        if json_match:
            json_str = json_match.group(1)
        else:
            json_str = content
        
        # Clean up any remaining markdown or text
        json_str = re.sub(r'```(json)?', '', json_str).strip()
        
        # Parse JSON
        try:
            competitors_data = json.loads(json_str)
            return jsonify(competitors_data)
        except json.JSONDecodeError:
            # If JSON parsing fails, return a structured response
            return jsonify({
                "competitors": [
                    {"name": "Competitor A", "url": "https://www.competitora.com"},
                    {"name": "Competitor B", "url": "https://www.competitorb.com"},
                    {"name": "Competitor C", "url": "https://www.competitorc.com"}
                ]
            })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/filter_news', methods=['GET'])
def filter_news():
    try:
        news_filter.main()
        return jsonify({"status": "success", "message": "Filtered articles saved to filtered_articles_extra.xlsx"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    file_path = os.path.join(project_dir, filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        return jsonify({"error": "File not found"}), 404

@app.route('/api/generate-report', methods=['POST'])
def generate_report():
    data = request.json
    website_url = data.get('websiteUrl')
    competitor_details = data.get('competitorDetails')
    
    if not website_url or not competitor_details:
        return jsonify({"error": "Website URL and competitor details are required"}), 400
    
    try:
        # Use OpenAI to generate a comprehensive report
        prompt = f"""
        Generate a comprehensive competitor intelligence report based on the following information:
        
        Main website: {website_url}
        
        Competitor information:
        {json.dumps(competitor_details, indent=2)}
        
        The report should include:
        1. Executive summary
        2. Competitive landscape overview
        3. Detailed analysis of each competitor
        4. Strategic recommendations for {website_url}
        5. Market positioning advice
        
        Format the report in Markdown with proper headings, lists, and sections.
        """
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an AI that generates detailed competitor intelligence reports."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        
        report_content = response.choices[0].message.content.strip()
        
        return jsonify({
            "status": "success", 
            "report": report_content
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/enhanced-brand-audit', methods=['POST'])
def enhanced_brand_audit():
    """Generate enhanced brand audit with detailed grid layout"""
    data = request.json
    urls = data.get('urls', [])
    
    if not urls:
        return jsonify({"error": "At least one URL is required"}), 400
    
    try:
        # Analyze brands using enhanced profiler
        brand_profiles = enhanced_profiler.analyze_competitor_brands(urls)
        
        if not brand_profiles:
            return jsonify({"error": "Failed to analyze any brands"}), 500
        
        # Generate enhanced report
        output_filename = f"enhanced_brand_audit_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        success = enhanced_generator.generate_report_from_profiles(brand_profiles, output_filename)
        
        if success:
            return jsonify({
                "status": "success",
                "message": f"Enhanced brand audit generated: {output_filename}",
                "filename": output_filename,
                "brands_analyzed": len(brand_profiles),
                "download_url": f"/download/{output_filename}"
            })
        else:
            return jsonify({"error": "Failed to generate report"}), 500
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/analyze-single-brand', methods=['POST'])
def analyze_single_brand():
    """Analyze a single brand and return detailed profile"""
    data = request.json
    url = data.get('url')
    
    if not url:
        return jsonify({"error": "URL is required"}), 400
    
    try:
        profiler = enhanced_profiler.EnhancedBrandProfiler()
        brand_profile = profiler.analyze_brand_comprehensive(url)
        
        if brand_profile:
            return jsonify({
                "status": "success",
                "brand_profile": brand_profile
            })
        else:
            return jsonify({"error": "Failed to analyze brand"}), 500
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/generate-grid-preview', methods=['POST'])
def generate_grid_preview():
    """Generate a preview of the competitive landscape grid"""
    data = request.json
    brand_profiles = data.get('brand_profiles', [])
    
    try:
        generator = enhanced_generator.EnhancedReportGenerator()
        grid_html = generator.generate_grid_html(brand_profiles)
        
        return jsonify({
            "status": "success",
            "grid_html": grid_html
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)