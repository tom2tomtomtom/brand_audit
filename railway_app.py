#!/usr/bin/env python3
"""
Railway Web Interface for Competitive Intelligence V2
Using the improved V2 system with real data only
"""

import os
from flask import Flask, request, jsonify, render_template_string, send_file
from flask_cors import CORS
from dotenv import load_dotenv
import json
from datetime import datetime
import time
import tempfile

# Import our V2 competitive intelligence system
IMPORT_ERROR = None
SYSTEM_AVAILABLE = False

try:
    from competitive_grid_generator_v2 import CompetitiveGridGeneratorV2
    SYSTEM_AVAILABLE = True
    print("✅ V2 Competitive Intelligence System loaded successfully")
except ImportError as e:
    print(f"❌ V2 System not available - ImportError: {e}")
    IMPORT_ERROR = f"ImportError: {str(e)}"
    SYSTEM_AVAILABLE = False
except Exception as e:
    print(f"❌ Error loading V2 system - {type(e).__name__}: {e}")
    import traceback
    IMPORT_ERROR = f"{type(e).__name__}: {str(e)}\n{traceback.format_exc()}"
    SYSTEM_AVAILABLE = False

# Load environment variables
load_dotenv()

# Verify critical environment variables
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
if not OPENAI_API_KEY:
    print("⚠️  WARNING: OPENAI_API_KEY not found in environment variables")
    print("   The system will not be able to perform AI analysis")
else:
    print(f"✅ OpenAI API key loaded ({len(OPENAI_API_KEY)} chars)")

app = Flask(__name__)
CORS(app)

# HTML Template for the web interface
WEB_INTERFACE_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Brandintell V2 - Real Data Competitive Intelligence</title>
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
        
        .v2-badge {
            display: inline-block;
            background: #28a745;
            color: white;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.8em;
            font-weight: 600;
            margin-left: 10px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Brandintell <span class="v2-badge">V2</span></h1>
            <p>Real Data Competitive Intelligence Analysis</p>
        </div>
        
        <div class="content">
            <div class="feature-grid">
                <div class="feature-card">
                    <h3>🚀 V2 Enhanced System</h3>
                    <p>Multi-strategy extraction with BeautifulSoup, Selenium, and Playwright</p>
                </div>
                <div class="feature-card">
                    <h3>💯 Real Data Only</h3>
                    <p>No placeholders or fallbacks - transparent failure reporting</p>
                </div>
                <div class="feature-card">
                    <h3>🔍 Industry Agnostic</h3>
                    <p>Dynamic industry detection with no hardcoded assumptions</p>
                </div>
                <div class="feature-card">
                    <h3>🧠 Intelligent Analysis</h3>
                    <p>3 retry strategies with GPT-4 chain-of-thought reasoning</p>
                </div>
            </div>
            
            <div class="url-form">
                <div class="form-group">
                    <label for="url-input">Add Competitor URLs (2-10 companies):</label>
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
                    Generate V2 Intelligence Report
                </button>
                
                <div id="status" class="status"></div>
            </div>
            
            <div class="examples">
                <h4>Example URLs (click to add):</h4>
                <ul>
                    <li onclick="addExampleUrl('https://stripe.com')">• Stripe (Payments)</li>
                    <li onclick="addExampleUrl('https://square.com')">• Square (Commerce)</li>
                    <li onclick="addExampleUrl('https://paypal.com')">• PayPal (Digital Payments)</li>
                    <li onclick="addExampleUrl('https://shopify.com')">• Shopify (E-commerce)</li>
                    <li onclick="addExampleUrl('https://woocommerce.com')">• WooCommerce (E-commerce)</li>
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
            
            if (urls.length >= 10) {
                alert('Maximum 10 URLs allowed');
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
            
            if (urls.length >= 10) {
                alert('Maximum 10 URLs allowed');
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
            btn.textContent = 'Generating V2 Report...';
            status.className = 'status loading';
            status.textContent = 'V2 analysis in progress - this may take a few minutes...';
            
            try {
                const response = await fetch('/api/generate-v2', {
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
                    a.download = 'brandintell_v2_report.html';
                    document.body.appendChild(a);
                    a.click();
                    window.URL.revokeObjectURL(url);
                    document.body.removeChild(a);
                    
                    status.className = 'status success';
                    status.textContent = 'V2 report generated successfully! Download should start automatically.';
                } else {
                    const error = await response.text();
                    throw new Error(error);
                }
                
            } catch (error) {
                status.className = 'status error';
                status.textContent = `❌ Error: ${error.message}`;
            } finally {
                btn.disabled = false;
                btn.textContent = 'Generate V2 Intelligence Report';
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
    return 'OK', 200

@app.route('/api/status')
def api_status():
    """Simple status check"""
    return jsonify({
        'status': 'online',
        'app': 'Brandintell V2',
        'version': '2.0',
        'endpoints': ['/health', '/api/status', '/debug', '/api/generate-v2'],
        'system_loaded': SYSTEM_AVAILABLE,
        'features': [
            'Multi-strategy extraction (BeautifulSoup, Selenium, Playwright)',
            'Real data only - no fallbacks',
            'Industry agnostic analysis',
            'Intelligent retry logic',
            'Quality scoring and confidence metrics'
        ]
    })

@app.route('/debug')
def debug():
    """Debug endpoint to check system status"""
    import sys
    import traceback
    
    debug_info = {
        'system_available': SYSTEM_AVAILABLE,
        'python_version': sys.version,
        'openai_key_present': bool(os.environ.get('OPENAI_API_KEY')),
        'initial_import_error': IMPORT_ERROR,
        'import_error': None,
        'modules_loaded': list(sys.modules.keys())
    }
    
    # Try importing again to get the actual error
    try:
        from competitive_grid_generator_v2 import CompetitiveGridGeneratorV2
        debug_info['import_status'] = 'Success'
    except Exception as e:
        debug_info['import_error'] = str(e)
        debug_info['import_traceback'] = traceback.format_exc()
    
    # Check dependencies
    dependencies = {
        'openai': False,
        'selenium': False,
        'pandas': False,
        'beautifulsoup4': False,
        'playwright': False,
        'requests': False
    }
    
    for module_name in dependencies:
        try:
            __import__(module_name)
            dependencies[module_name] = True
        except:
            dependencies[module_name] = False
    
    debug_info['dependencies'] = dependencies
    
    return jsonify(debug_info)

@app.route('/api/generate-v2', methods=['POST'])
def generate_v2():
    """Generate V2 competitive intelligence report"""
    # Check if system is available
    if not SYSTEM_AVAILABLE:
        return jsonify({
            'error': 'V2 competitive intelligence system not available',
            'details': 'CompetitiveGridGeneratorV2 could not be loaded',
            'import_error': IMPORT_ERROR
        }), 503
    
    try:
        data = request.get_json()
        urls = data.get('urls', [])
        
        if len(urls) < 2:
            return jsonify({'error': 'At least 2 URLs required'}), 400
        
        if len(urls) > 10:
            return jsonify({'error': 'Maximum 10 URLs allowed'}), 400
        
        # Use the V2 system
        generator = CompetitiveGridGeneratorV2()
        
        # Generate the report
        print(f"Starting V2 analysis for {len(urls)} URLs: {urls}")
        
        # Use temp directory for Railway compatibility
        temp_dir = tempfile.gettempdir()
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_filename = os.path.join(temp_dir, f"brandintell_v2_{timestamp}.html")
        
        # Generate report with V2 system
        result = generator.generate_report(
            urls=urls,
            report_title="Brandintell V2 Competitive Intelligence Analysis",
            output_filename=output_filename
        )
        
        if result['success'] and os.path.exists(result['output_file']):
            return send_file(
                result['output_file'], 
                as_attachment=True, 
                download_name='brandintell_v2_report.html'
            )
        else:
            return jsonify({
                'error': 'Failed to generate report',
                'details': result.get('errors', [])
            }), 500
            
    except Exception as e:
        import traceback
        error_details = {
            'error': str(e),
            'type': type(e).__name__,
            'traceback': traceback.format_exc()
        }
        print(f"Error in generate_v2: {error_details}")
        return jsonify(error_details), 500

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'error': 'Endpoint not found',
        'available_endpoints': [
            'GET /',
            'GET /health', 
            'POST /api/generate-v2',
            'GET /api/status',
            'GET /debug'
        ]
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # Railway deployment configuration
    port = int(os.environ.get('PORT', 5000))
    debug_mode = os.environ.get('FLASK_ENV') == 'development'
    
    print(f"🚀 Starting Brandintell V2 on port {port}")
    print(f"🌍 Environment: {'Development' if debug_mode else 'Production'}")
    print(f"📡 Health check available at /health")
    print(f"🌐 Web interface available at /")
    print(f"✅ System available: {SYSTEM_AVAILABLE}")
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug_mode
    )
