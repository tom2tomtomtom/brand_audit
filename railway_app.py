#!/usr/bin/env python3
"""
Railway-compatible Flask app for Brand Audit Grid Generator
Simplified version without external dependencies
"""

import os
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from dotenv import load_dotenv
import json
from datetime import datetime
import time

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Simple in-memory storage for Railway deployment
analysis_jobs = {}

@app.route('/')
def index():
    """Health check and info endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Brand Audit Grid Generator',
        'version': '1.0',
        'timestamp': datetime.now().isoformat(),
        'endpoints': [
            'GET / - This health check',
            'POST /api/generate-grid - Generate competitive grid with URLs',
            'POST /api/quick-analysis - Quick brand analysis',
            'GET /api/status - Service status'
        ]
    })

@app.route('/health')
def health():
    """Railway health check endpoint"""
    return jsonify({'status': 'healthy'}), 200

@app.route('/api/status')
def status():
    """Service status endpoint"""
    return jsonify({
        'status': 'running',
        'active_jobs': len(analysis_jobs),
        'uptime': 'healthy',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/generate-grid', methods=['POST'])
def generate_grid():
    """Generate competitive landscape grid"""
    try:
        data = request.get_json()
        
        if not data or 'urls' not in data:
            return jsonify({'error': 'URLs array required'}), 400
        
        urls = data['urls']
        title = data.get('title', 'Competitive Landscape Analysis')
        
        if not isinstance(urls, list) or len(urls) == 0:
            return jsonify({'error': 'At least one URL required'}), 400
        
        # Create job ID
        job_id = f"grid_{int(time.time())}"
        
        # Store job info
        analysis_jobs[job_id] = {
            'status': 'started',
            'urls': urls,
            'title': title,
            'created_at': datetime.now().isoformat(),
            'progress': 0
        }
        
        # For Railway deployment, return immediately with job info
        # In production, this would trigger background processing
        analysis_jobs[job_id].update({
            'status': 'completed',
            'progress': 100,
            'message': 'Grid generation ready',
            'result_url': f'/api/download/{job_id}'
        })
        
        return jsonify({
            'job_id': job_id,
            'status': 'started',
            'message': 'Grid generation initiated',
            'estimated_time': '2-5 minutes',
            'status_url': f'/api/job/{job_id}',
            'urls_count': len(urls)
        })
        
    except Exception as e:
        return jsonify({'error': f'Failed to start grid generation: {str(e)}'}), 500

@app.route('/api/quick-analysis', methods=['POST'])  
def quick_analysis():
    """Quick brand analysis without full grid"""
    try:
        data = request.get_json()
        
        if not data or 'url' not in data:
            return jsonify({'error': 'URL required'}), 400
        
        url = data['url']
        
        # Simulate quick analysis
        mock_analysis = {
            'url': url,
            'brand_name': extract_domain_name(url),
            'status': 'analyzed',
            'analysis': {
                'domain': extract_domain_name(url),
                'platform_detected': True,
                'analysis_time': datetime.now().isoformat(),
                'basic_info': {
                    'reachable': True,
                    'domain_age': 'unknown',
                    'technology_stack': 'web_standard'
                }
            },
            'timestamp': datetime.now().isoformat()
        }
        
        return jsonify({
            'status': 'success',
            'analysis': mock_analysis
        })
        
    except Exception as e:
        return jsonify({'error': f'Analysis failed: {str(e)}'}), 500

@app.route('/api/job/<job_id>')
def get_job_status(job_id):
    """Get job status"""
    if job_id not in analysis_jobs:
        return jsonify({'error': 'Job not found'}), 404
    
    job = analysis_jobs[job_id]
    return jsonify(job)

@app.route('/api/download/<job_id>')
def download_result(job_id):
    """Download analysis result - placeholder for Railway"""
    if job_id not in analysis_jobs:
        return jsonify({'error': 'Job not found'}), 404
    
    job = analysis_jobs[job_id]
    
    # Generate simple HTML response for Railway demo
    html_content = generate_demo_grid_html(job.get('urls', []), job.get('title', 'Demo Grid'))
    
    # Create temporary file
    temp_filename = f"/tmp/grid_{job_id}.html"
    try:
        with open(temp_filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return send_file(
            temp_filename,
            as_attachment=True,
            download_name=f"competitive_grid_{job_id}.html",
            mimetype='text/html'
        )
    except Exception as e:
        return jsonify({'error': f'Failed to generate download: {str(e)}'}), 500

def extract_domain_name(url):
    """Extract clean domain name from URL"""
    try:
        from urllib.parse import urlparse
        domain = urlparse(url).netloc
        domain = domain.replace('www.', '')
        return domain.split('.')[0].title()
    except:
        return "Unknown"

def generate_demo_grid_html(urls, title):
    """Generate demo HTML grid for Railway deployment"""
    brands_html = ""
    
    for i, url in enumerate(urls[:10], 1):
        brand_name = extract_domain_name(url)
        brands_html += f"""
        <div class="brand-card">
            <div class="brand-header">
                <div class="brand-logo">{brand_name}</div>
            </div>
            <div class="brand-url">{url}</div>
            <div class="brand-status">Ready for analysis</div>
        </div>
        """
    
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - Railway Demo</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background: #f5f5f5;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }}
        .header {{
            text-align: center;
            margin-bottom: 40px;
        }}
        .title {{
            font-size: 2.5em;
            color: #2c3e50;
            margin-bottom: 10px;
        }}
        .subtitle {{
            color: #7f8c8d;
            font-size: 1.1em;
        }}
        .brands-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin: 40px 0;
        }}
        .brand-card {{
            border: 1px solid #e1e8ed;
            border-radius: 8px;
            padding: 20px;
            background: #fafafa;
        }}
        .brand-header {{
            display: flex;
            align-items: center;
            margin-bottom: 15px;
        }}
        .brand-logo {{
            font-size: 1.3em;
            font-weight: 600;
            color: #2c3e50;
            background: #ecf0f1;
            padding: 10px 15px;
            border-radius: 5px;
            margin-right: 15px;
        }}
        .brand-url {{
            font-size: 0.9em;
            color: #3498db;
            margin-bottom: 10px;
            word-break: break-all;
        }}
        .brand-status {{
            font-size: 0.8em;
            color: #27ae60;
            background: #e8f5e8;
            padding: 5px 10px;
            border-radius: 3px;
            display: inline-block;
        }}
        .info {{
            background: #e3f2fd;
            border: 1px solid #2196f3;
            border-radius: 5px;
            padding: 20px;
            margin: 30px 0;
            text-align: center;
        }}
        .footer {{
            text-align: center;
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #e1e8ed;
            color: #7f8c8d;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1 class="title">{title}</h1>
            <p class="subtitle">Railway Demo - Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
        </div>
        
        <div class="info">
            <strong>🚀 Railway Demo Version</strong><br>
            This is a simplified demonstration version running on Railway.<br>
            The full system includes real web scraping, AI analysis, and professional grid generation.
        </div>
        
        <div class="brands-grid">
            {brands_html}
        </div>
        
        <div class="footer">
            <p>Brand Audit Grid Generator - Railway Deployment</p>
            <p>Visit GitHub for the complete system: github.com/tom2tomtomtom/brand_audit</p>
        </div>
    </div>
</body>
</html>"""

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'error': 'Endpoint not found',
        'available_endpoints': [
            'GET /',
            'GET /health', 
            'POST /api/generate-grid',
            'POST /api/quick-analysis',
            'GET /api/status'
        ]
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # Railway deployment configuration
    port = int(os.environ.get('PORT', 5000))
    debug_mode = os.environ.get('FLASK_ENV') == 'development'
    
    print(f"🚀 Starting Brand Audit Grid Generator on port {port}")
    print(f"🌍 Environment: {'Development' if debug_mode else 'Production'}")
    print(f"📡 Health check available at /health")
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug_mode
    )