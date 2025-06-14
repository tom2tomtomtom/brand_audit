#!/usr/bin/env python3
"""
Flask API for Brand Audit V2
Real data only - no fallbacks or defaults
"""

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import json
from datetime import datetime
from enhanced_brand_profiler_v2 import EnhancedBrandProfilerV2
from competitive_grid_generator_v2 import CompetitiveGridGeneratorV2
from ai_powered_competitive_intelligence_v2 import AIPoweredCompetitiveIntelligenceV2

app = Flask(__name__)
CORS(app)

# Initialize V2 components
brand_profiler = EnhancedBrandProfilerV2()
grid_generator = CompetitiveGridGeneratorV2()
ai_intelligence = AIPoweredCompetitiveIntelligenceV2()

@app.route('/')
def home():
    """API documentation"""
    return jsonify({
        "name": "Brand Audit API V2",
        "version": "2.0.0",
        "description": "Real data only - no fallbacks or defaults",
        "endpoints": {
            "/api/v2/analyze-brand": {
                "method": "POST",
                "description": "Analyze a single brand",
                "params": {"url": "Brand website URL"}
            },
            "/api/v2/competitive-grid": {
                "method": "POST",
                "description": "Generate competitive landscape grid",
                "params": {
                    "urls": "List of brand URLs",
                    "title": "Report title (optional)"
                }
            },
            "/api/v2/ai-intelligence": {
                "method": "POST",
                "description": "Generate AI-powered competitive intelligence",
                "params": {
                    "urls": "List of brand URLs",
                    "title": "Report title (optional)"
                }
            },
            "/api/v2/health": {
                "method": "GET",
                "description": "Check API health"
            }
        }
    })

@app.route('/api/v2/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "2.0.0",
        "openai_configured": bool(os.getenv("OPENAI_API_KEY"))
    })

@app.route('/api/v2/analyze-brand', methods=['POST'])
def analyze_brand():
    """Analyze a single brand - real data only"""
    try:
        data = request.get_json()
        url = data.get('url')
        
        if not url:
            return jsonify({
                "error": "URL parameter is required"
            }), 400
        
        # Analyze brand
        result = brand_profiler.analyze_brand(url)
        
        # Return result as-is (success or failure)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            "error": f"Analysis failed: {str(e)}",
            "status": "error"
        }), 500

@app.route('/api/v2/competitive-grid', methods=['POST'])
def generate_competitive_grid():
    """Generate competitive grid - real data only"""
    try:
        data = request.get_json()
        urls = data.get('urls', [])
        title = data.get('title', 'Competitive Landscape Analysis')
        
        if not urls or not isinstance(urls, list):
            return jsonify({
                "error": "URLs parameter must be a non-empty list"
            }), 400
        
        # Generate timestamp filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"grid_v2_{timestamp}.html"
        
        # Generate grid
        result = grid_generator.generate_report(
            urls=urls,
            report_title=title,
            output_filename=filename
        )
        
        if result:
            # Return success with file info
            response = {
                "status": "success",
                "filename": result['filename'],
                "successful_count": result['successful_count'],
                "failed_count": result['failed_count'],
                "brands": []
            }
            
            # Include brand summaries
            for brand in result.get('brands', []):
                response['brands'].append({
                    "company_name": brand['company_name'],
                    "url": brand['url'],
                    "extraction_quality": brand['extraction_quality'],
                    "has_logo": bool(brand.get('logo_url')),
                    "color_count": len(brand.get('color_palette', [])),
                    "personality_count": len(brand.get('personality_descriptors', []))
                })
            
            # Also return failed URLs
            if 'failed' in grid_generator.__dict__:
                response['failed_urls'] = grid_generator.failed_extractions
            
            return jsonify(response)
        else:
            return jsonify({
                "error": "Grid generation failed",
                "status": "failed"
            }), 500
            
    except Exception as e:
        return jsonify({
            "error": f"Grid generation failed: {str(e)}",
            "status": "error"
        }), 500

@app.route('/api/v2/ai-intelligence', methods=['POST'])
def generate_ai_intelligence():
    """Generate AI-powered competitive intelligence - real data only"""
    try:
        data = request.get_json()
        urls = data.get('urls', [])
        title = data.get('title', 'Competitive Intelligence Report')
        
        if not urls or not isinstance(urls, list):
            return jsonify({
                "error": "URLs parameter must be a non-empty list"
            }), 400
        
        # Generate timestamp filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"intelligence_v2_{timestamp}.html"
        
        # Generate intelligence report
        result = ai_intelligence.generate_report(
            urls=urls,
            report_title=title,
            output_filename=filename
        )
        
        if result:
            # Return success with analysis summary
            response = {
                "status": "success",
                "filename": result['filename'],
                "successful_count": result['successful_count'],
                "failed_count": result['failed_count'],
                "has_cross_brand_insights": result['has_insights'],
                "brands": []
            }
            
            # Include AI analysis summaries
            for brand in ai_intelligence.brand_profiles:
                analyses = brand.get('ai_analyses', {})
                
                brand_summary = {
                    "company_name": brand['company_name'],
                    "url": brand['url'],
                    "extraction_quality": brand.get('extraction_quality', 0),
                    "analyses_completed": list(analyses.keys()),
                    "health_score": analyses.get('health', {}).get('overall_score', 0),
                    "threat_level": analyses.get('health', {}).get('competitive_threat', {}).get('level', 'Unknown'),
                    "positioning_type": analyses.get('positioning', {}).get('positioning_strategy', {}).get('type', 'Unknown')
                }
                
                response['brands'].append(brand_summary)
            
            # Include failed URLs
            response['failed_urls'] = ai_intelligence.failed_brands
            
            return jsonify(response)
        else:
            return jsonify({
                "error": "Intelligence generation failed",
                "status": "failed"
            }), 500
            
    except Exception as e:
        return jsonify({
            "error": f"Intelligence generation failed: {str(e)}",
            "status": "error"
        }), 500

@app.route('/api/v2/download/<filename>', methods=['GET'])
def download_report(filename):
    """Download generated report"""
    try:
        # Security check - only allow specific file patterns
        if not (filename.startswith('grid_v2_') or filename.startswith('intelligence_v2_')):
            return jsonify({"error": "Invalid filename"}), 400
        
        if not filename.endswith('.html'):
            return jsonify({"error": "Invalid file type"}), 400
        
        # Check if file exists
        if os.path.exists(filename):
            return send_file(filename, as_attachment=True)
        else:
            return jsonify({"error": "File not found"}), 404
            
    except Exception as e:
        return jsonify({"error": f"Download failed: {str(e)}"}), 500

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        "error": "Endpoint not found",
        "status": 404
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        "error": "Internal server error",
        "status": 500
    }), 500

if __name__ == '__main__':
    # Check for required environment variables
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  Warning: OPENAI_API_KEY not set!")
        print("AI analysis features will not work without it.")
    
    # Run the app
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    print(f"🚀 Starting Brand Audit API V2 on port {port}")
    print(f"📋 Real data only - no fallbacks or defaults")
    print(f"🔗 API documentation: http://localhost:{port}/")
    
    app.run(host='0.0.0.0', port=port, debug=debug)
