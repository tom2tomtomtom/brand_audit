#!/usr/bin/env python3
"""
Railway Web Interface for Premium Competitive Intelligence
Safe deployment with defensive imports and robust fallbacks
"""

import os
import sys
import traceback
from flask import Flask, request, jsonify, render_template_string, send_file
from flask_cors import CORS
from dotenv import load_dotenv
import json
from datetime import datetime
import time

# Load environment variables first
load_dotenv()

app = Flask(__name__)
CORS(app)

# Global state for system availability
SYSTEM_AVAILABLE = False
STRATEGIC_SYSTEM = None
IMPORT_ERROR = None

def safe_import_strategic_system():
    """Safely import the strategic system with detailed error handling"""
    global SYSTEM_AVAILABLE, STRATEGIC_SYSTEM, IMPORT_ERROR
    
    try:
        print("🔄 Attempting to import strategic competitive intelligence system...")
        
        # Test basic dependencies first
        import requests
        import openai
        from openai import OpenAI
        print("✅ Basic dependencies available")
        
        # Test OpenAI configuration
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ImportError("OPENAI_API_KEY environment variable not set")
        print("✅ OpenAI API key configured")
        
        # Now try to import the strategic system
        from strategic_competitive_intelligence import StrategicCompetitiveIntelligence
        STRATEGIC_SYSTEM = StrategicCompetitiveIntelligence
        SYSTEM_AVAILABLE = True
        print("✅ Strategic competitive intelligence system loaded successfully")
        
    except Exception as e:
        IMPORT_ERROR = str(e)
        SYSTEM_AVAILABLE = False
        print(f"❌ Strategic system import failed: {e}")
        print(f"📋 Full traceback: {traceback.format_exc()}")

# Attempt to import the strategic system
safe_import_strategic_system()

# Fallback lightweight competitive intelligence for Railway
class RailwayCompetitiveIntelligence:
    """Lightweight competitive intelligence for Railway deployment"""
    
    def __init__(self):
        import requests
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def generate_strategic_intelligence_report(self, urls, report_title="Competitive Analysis", output_filename=None):
        """Generate a Railway demo report"""
        if not output_filename:
            output_filename = f"railway_demo_{int(time.time())}.html"
        
        # Generate demo HTML report
        html_content = self._generate_demo_report(urls, report_title)
        
        try:
            with open(output_filename, 'w', encoding='utf-8') as f:
                f.write(html_content)
            return output_filename
        except Exception as e:
            print(f"Error generating demo report: {e}")
            return None
    
    def _generate_demo_report(self, urls, title):
        """Generate Railway demo report"""
        brands_html = ""
        
        for i, url in enumerate(urls[:10], 1):
            domain = self._extract_domain(url)
            brands_html += f"""
            <div class="brand-card">
                <div class="brand-header">
                    <h3>🏢 {domain}</h3>
                    <div class="status-badge">Demo Ready</div>
                </div>
                <div class="brand-details">
                    <p><strong>URL:</strong> {url}</p>
                    <p><strong>Analysis Status:</strong> Available for full local deployment</p>
                </div>
                <div class="capabilities">
                    <div class="capability">🎨 Premium 6-row grid analysis</div>
                    <div class="capability">🧠 McKinsey-level AI insights</div>
                    <div class="capability">📊 Real data extraction</div>
                    <div class="capability">🔤 Typography analysis</div>
                </div>
            </div>
            """
        
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - Railway Demo</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
            color: #333;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 16px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 0 2px 4px rgba(0,0,0,0.3);
        }}
        
        .header p {{
            font-size: 1.2em;
            opacity: 0.9;
        }}
        
        .content {{
            padding: 40px;
        }}
        
        .demo-notice {{
            background: #e8f4fd;
            border: 2px solid #3498db;
            border-radius: 12px;
            padding: 30px;
            margin-bottom: 40px;
            text-align: center;
        }}
        
        .demo-notice h2 {{
            color: #2980b9;
            margin-bottom: 15px;
        }}
        
        .demo-notice p {{
            color: #34495e;
            margin-bottom: 10px;
        }}
        
        .github-link {{
            display: inline-block;
            background: #28a745;
            color: white;
            text-decoration: none;
            padding: 12px 24px;
            border-radius: 8px;
            font-weight: 600;
            margin-top: 20px;
            transition: background 0.3s ease;
        }}
        
        .github-link:hover {{
            background: #218838;
        }}
        
        .brands-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 25px;
            margin: 30px 0;
        }}
        
        .brand-card {{
            background: #f8f9fa;
            border: 1px solid #e9ecef;
            border-radius: 12px;
            padding: 25px;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }}
        
        .brand-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        }}
        
        .brand-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
        }}
        
        .brand-header h3 {{
            color: #2c3e50;
            font-size: 1.3em;
        }}
        
        .status-badge {{
            background: #28a745;
            color: white;
            padding: 5px 12px;
            border-radius: 15px;
            font-size: 0.8em;
            font-weight: 600;
        }}
        
        .brand-details {{
            margin-bottom: 20px;
        }}
        
        .brand-details p {{
            margin-bottom: 8px;
            color: #495057;
        }}
        
        .capabilities {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 8px;
        }}
        
        .capability {{
            background: #e7f3ff;
            color: #0066cc;
            padding: 8px 12px;
            border-radius: 6px;
            font-size: 0.85em;
            text-align: center;
        }}
        
        .footer {{
            background: #f8f9fa;
            padding: 30px;
            text-align: center;
            border-top: 1px solid #e9ecef;
            color: #6c757d;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎯 {title}</h1>
            <p>Railway Demo - Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
        </div>
        
        <div class="content">
            <div class="demo-notice">
                <h2>🚀 Railway Demo Environment</h2>
                <p>This Railway deployment demonstrates the web interface and system architecture.</p>
                <p><strong>The full competitive intelligence system includes:</strong></p>
                <ul style="text-align: left; display: inline-block; margin: 15px 0;">
                    <li>🎨 Premium 6-row brand grids with real logo extraction</li>
                    <li>🧠 McKinsey-level AI-powered strategic analysis</li>
                    <li>📊 Real web scraping with enhanced privacy handling</li>
                    <li>🔤 Typography analysis with actual font detection</li>
                    <li>🎭 Visual gallery capture from websites</li>
                    <li>📈 Comprehensive competitive positioning reports</li>
                </ul>
                <a href="https://github.com/tom2tomtomtom/brand_audit" class="github-link">
                    📂 Get Complete System on GitHub
                </a>
            </div>
            
            <h2 style="margin-bottom: 20px; color: #2c3e50;">Competitor Analysis Preview</h2>
            <div class="brands-grid">
                {brands_html}
            </div>
        </div>
        
        <div class="footer">
            <p><strong>Railway Deployment:</strong> Web interface and architecture demonstration</p>
            <p><strong>Full System:</strong> Available for local deployment with complete competitive intelligence capabilities</p>
        </div>
    </div>
</body>
</html>"""
    
    def _extract_domain(self, url):
        """Extract domain name from URL"""
        try:
            from urllib.parse import urlparse
            domain = urlparse(url).netloc
            domain = domain.replace('www.', '')
            return domain.split('.')[0].title()
        except:
            return "Company"

# HTML Template for the web interface
WEB_INTERFACE_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Premium Competitive Intelligence Generator</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            border-radius: 16px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }
        
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 0 2px 4px rgba(0,0,0,0.3);
        }
        
        .header p {
            font-size: 1.2em;
            opacity: 0.9;
        }
        
        .system-status {
            background: """ + ("#d4edda" if SYSTEM_AVAILABLE else "#fff3cd") + """;
            color: """ + ("#155724" if SYSTEM_AVAILABLE else "#856404") + """;
            padding: 15px;
            margin: 20px 40px;
            border-radius: 8px;
            border: 1px solid """ + ("#c3e6cb" if SYSTEM_AVAILABLE else "#ffeaa7") + """;
        }
        
        .content {
            padding: 40px;
        }
        
        .feature-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }
        
        .feature-card {
            background: #f8f9fa;
            padding: 25px;
            border-radius: 12px;
            text-align: center;
            border-left: 4px solid #667eea;
        }
        
        .feature-card h3 {
            color: #2c3e50;
            margin-bottom: 10px;
        }
        
        .feature-card p {
            color: #6c757d;
            font-size: 0.9em;
        }
        
        .url-form {
            background: #f8f9fa;
            padding: 30px;
            border-radius: 12px;
            margin-bottom: 30px;
        }
        
        .form-group {
            margin-bottom: 20px;
        }
        
        .form-group label {
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
            color: #2c3e50;
        }
        
        .url-input {
            width: 100%;
            padding: 12px;
            border: 2px solid #e9ecef;
            border-radius: 8px;
            font-size: 16px;
            margin-bottom: 10px;
            transition: border-color 0.3s ease;
        }
        
        .url-input:focus {
            border-color: #667eea;
            outline: none;
        }
        
        .add-url-btn {
            background: #28a745;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 14px;
        }
        
        .add-url-btn:hover {
            background: #218838;
        }
        
        .generate-btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 15px 40px;
            border-radius: 8px;
            font-size: 18px;
            font-weight: 600;
            cursor: pointer;
            width: 100%;
            transition: transform 0.2s ease;
        }
        
        .generate-btn:hover {
            transform: translateY(-2px);
        }
        
        .generate-btn:disabled {
            opacity: 0.6;
            cursor: not-allowed;
            transform: none;
        }
        
        .status {
            margin-top: 20px;
            padding: 15px;
            border-radius: 8px;
            display: none;
        }
        
        .status.loading {
            background: #d1ecf1;
            color: #0c5460;
            display: block;
        }
        
        .status.success {
            background: #d4edda;
            color: #155724;
            display: block;
        }
        
        .status.error {
            background: #f8d7da;
            color: #721c24;
            display: block;
        }
        
        .url-list {
            max-height: 200px;
            overflow-y: auto;
            border: 1px solid #e9ecef;
            border-radius: 8px;
            padding: 10px;
            background: white;
        }
        
        .url-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 8px;
            border-bottom: 1px solid #f1f3f4;
        }
        
        .url-item:last-child {
            border-bottom: none;
        }
        
        .remove-url {
            background: #dc3545;
            color: white;
            border: none;
            padding: 4px 8px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 12px;
        }
        
        .examples {
            background: #e7f3ff;
            padding: 20px;
            border-radius: 8px;
            margin-top: 20px;
        }
        
        .examples h4 {
            color: #0066cc;
            margin-bottom: 10px;
        }
        
        .examples ul {
            list-style: none;
            padding: 0;
        }
        
        .examples li {
            padding: 5px 0;
            color: #0066cc;
            cursor: pointer;
        }
        
        .examples li:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎯 Premium Competitive Intelligence</h1>
            <p>McKinsey-Level Analysis with 6-Row Brand Grid</p>
        </div>
        
        <div class="system-status">
            <strong>System Status:</strong> """ + ("✅ Full competitive intelligence system available" if SYSTEM_AVAILABLE else f"⚠️ Demo mode - Full system available for local deployment") + """
            """ + (f"<br><small>Import error: {IMPORT_ERROR}</small>" if IMPORT_ERROR else "") + """
        </div>
        
        <div class="content">
            <div class="feature-grid">
                <div class="feature-card">
                    <h3>🎨 Premium 6-Row Grid</h3>
                    <p>Logo, Brand Story, Personality, Colors, Typography, Visual Gallery</p>
                </div>
                <div class="feature-card">
                    <h3>🧠 AI-Powered Analysis</h3>
                    <p>McKinsey-level strategic insights and competitive positioning</p>
                </div>
                <div class="feature-card">
                    <h3>📊 Real Data Only</h3>
                    <p>100% scraped data with enhanced privacy dialog handling</p>
                </div>
                <div class="feature-card">
                    <h3>🔤 Typography Analysis</h3>
                    <p>Real font extraction from CSS and style sheets</p>
                </div>
            </div>
            
            <div class="url-form">
                <div class="form-group">
                    <label for="url-input">Add Competitor URLs (2-15 companies):</label>
                    <input type="url" id="url-input" class="url-input" placeholder="https://www.example.com" />
                    <button type="button" class="add-url-btn" onclick="addUrl()">Add URL</button>
                </div>
                
                <div class="form-group">
                    <label>URLs to Analyze:</label>
                    <div id="url-list" class="url-list">
                        <p style="color: #6c757d; text-align: center; padding: 20px;">No URLs added yet</p>
                    </div>
                </div>
                
                <button type="button" class="generate-btn" onclick="generateReport()" id="generate-btn">
                    """ + ("Generate Premium Competitive Intelligence Report" if SYSTEM_AVAILABLE else "Generate Demo Report") + """
                </button>
                
                <div id="status" class="status"></div>
            </div>
            
            <div class="examples">
                <h4>📝 Example URLs (click to add):</h4>
                <ul>
                    <li onclick="addExampleUrl('https://www.wolterskluwer.com')">• Wolters Kluwer (Medical AI)</li>
                    <li onclick="addExampleUrl('https://www.elsevier.com')">• Elsevier (Healthcare Publishing)</li>
                    <li onclick="addExampleUrl('https://www.openevidence.com')">• OpenEvidence (Medical Platform)</li>
                    <li onclick="addExampleUrl('https://www.apple.com')">• Apple (Technology)</li>
                    <li onclick="addExampleUrl('https://www.microsoft.com')">• Microsoft (Enterprise Software)</li>
                </ul>
            </div>
        </div>
    </div>
    
    <script>
        let urls = [];
        
        function addUrl() {
            const input = document.getElementById('url-input');
            const url = input.value.trim();
            
            if (!url) {
                alert('Please enter a URL');
                return;
            }
            
            if (!isValidUrl(url)) {
                alert('Please enter a valid URL (e.g., https://www.example.com)');
                return;
            }
            
            if (urls.includes(url)) {
                alert('This URL has already been added');
                return;
            }
            
            if (urls.length >= 15) {
                alert('Maximum 15 URLs allowed');
                return;
            }
            
            urls.push(url);
            input.value = '';
            updateUrlList();
        }
        
        function addExampleUrl(url) {
            if (urls.includes(url)) {
                alert('This URL has already been added');
                return;
            }
            
            if (urls.length >= 15) {
                alert('Maximum 15 URLs allowed');
                return;
            }
            
            urls.push(url);
            updateUrlList();
        }
        
        function removeUrl(index) {
            urls.splice(index, 1);
            updateUrlList();
        }
        
        function updateUrlList() {
            const listContainer = document.getElementById('url-list');
            
            if (urls.length === 0) {
                listContainer.innerHTML = '<p style="color: #6c757d; text-align: center; padding: 20px;">No URLs added yet</p>';
                return;
            }
            
            listContainer.innerHTML = urls.map((url, index) => `
                <div class="url-item">
                    <span>${url}</span>
                    <button class="remove-url" onclick="removeUrl(${index})">Remove</button>
                </div>
            `).join('');
        }
        
        function isValidUrl(string) {
            try {
                new URL(string);
                return string.startsWith('http://') || string.startsWith('https://');
            } catch (_) {
                return false;
            }
        }
        
        async function generateReport() {
            if (urls.length < 2) {
                alert('Please add at least 2 URLs for competitive analysis');
                return;
            }
            
            const btn = document.getElementById('generate-btn');
            const status = document.getElementById('status');
            
            btn.disabled = true;
            btn.textContent = 'Generating Report...';
            status.className = 'status loading';
            status.textContent = '🔄 Analyzing competitors and generating competitive intelligence report...';
            
            try {
                const response = await fetch('/api/generate-premium', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ urls: urls })
                });
                
                if (response.ok) {
                    const blob = await response.blob();
                    const url = window.URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = 'competitive_intelligence_report.html';
                    document.body.appendChild(a);
                    a.click();
                    window.URL.revokeObjectURL(url);
                    document.body.removeChild(a);
                    
                    status.className = 'status success';
                    status.textContent = '✅ Report generated successfully! Download should start automatically.';
                } else {
                    const error = await response.text();
                    throw new Error(error);
                }
                
            } catch (error) {
                status.className = 'status error';
                status.textContent = `❌ Error: ${error.message}`;
            } finally {
                btn.disabled = false;
                btn.textContent = """ + ("'Generate Premium Competitive Intelligence Report'" if SYSTEM_AVAILABLE else "'Generate Demo Report'") + """;
            }
        }
        
        // Handle Enter key in URL input
        document.getElementById('url-input').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                addUrl();
            }
        });
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """Main web interface"""
    return render_template_string(WEB_INTERFACE_TEMPLATE)

@app.route('/health')
def health():
    """Railway health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'system_available': SYSTEM_AVAILABLE,
        'import_error': IMPORT_ERROR
    }), 200

@app.route('/api/generate-premium', methods=['POST'])
def generate_premium():
    """Generate competitive intelligence report"""
    try:
        data = request.get_json()
        urls = data.get('urls', [])
        
        if len(urls) < 2:
            return jsonify({'error': 'At least 2 URLs required'}), 400
        
        if len(urls) > 15:
            return jsonify({'error': 'Maximum 15 URLs allowed'}), 400
        
        # Initialize the appropriate system
        if SYSTEM_AVAILABLE and STRATEGIC_SYSTEM:
            print("🚀 Using full strategic competitive intelligence system")
            generator = STRATEGIC_SYSTEM()
        else:
            print("🔄 Using Railway fallback system")
            generator = RailwayCompetitiveIntelligence()
        
        # Generate the report
        output_file = generator.generate_strategic_intelligence_report(
            urls=urls,
            report_title="Premium Competitive Intelligence Analysis",
            output_filename=f"report_{int(time.time())}.html"
        )
        
        if output_file and os.path.exists(output_file):
            return send_file(output_file, as_attachment=True, download_name='competitive_intelligence_report.html')
        else:
            return jsonify({'error': 'Failed to generate report'}), 500
            
    except Exception as e:
        print(f"Error in generate_premium: {e}")
        print(f"Traceback: {traceback.format_exc()}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/status')
def status():
    """Service status endpoint"""
    return jsonify({
        'status': 'running',
        'service': 'Premium Competitive Intelligence',
        'version': '2.1',
        'system_available': SYSTEM_AVAILABLE,
        'import_error': IMPORT_ERROR,
        'features': [
            'Premium web interface',
            'Defensive import handling',
            'Full system when available',
            'Railway fallback system',
            'Comprehensive error reporting'
        ],
        'endpoints': {
            'GET /': 'Web interface',
            'GET /health': 'Health check',
            'POST /api/generate-premium': 'Generate report',
            'GET /api/status': 'Service status'
        }
    })

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'error': 'Endpoint not found',
        'available_endpoints': [
            'GET /',
            'GET /health', 
            'POST /api/generate-premium',
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
    
    print(f"🚀 Starting Premium Competitive Intelligence on port {port}")
    print(f"🌍 Environment: {'Development' if debug_mode else 'Production'}")
    print(f"📡 Health check available at /health")
    print(f"🌐 Web interface available at /")
    print(f"🎯 Strategic system available: {SYSTEM_AVAILABLE}")
    if IMPORT_ERROR:
        print(f"⚠️ Import error: {IMPORT_ERROR}")
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug_mode
    )