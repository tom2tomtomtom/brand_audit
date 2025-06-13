#!/usr/bin/env python3
"""
Railway Web Interface for Premium Competitive Intelligence
Complete web interface with premium 6-row grid system
"""

import os
from flask import Flask, request, jsonify, render_template_string, send_file
from flask_cors import CORS
from dotenv import load_dotenv
import json
from datetime import datetime
import time

# Import our premium competitive intelligence system
IMPORT_ERROR = None
SYSTEM_AVAILABLE = False
StrategicCompetitiveIntelligence = None

# Try to load the system at startup
try:
    from strategic_competitive_intelligence import StrategicCompetitiveIntelligence
    SYSTEM_AVAILABLE = True
    print("Strategic competitive intelligence system loaded successfully")
except ImportError as e:
    print(f"Strategic system not available - ImportError: {e}")
    IMPORT_ERROR = f"ImportError: {str(e)}"
    SYSTEM_AVAILABLE = False
except Exception as e:
    print(f"Error loading strategic system - {type(e).__name__}: {e}")
    import traceback
    IMPORT_ERROR = f"{type(e).__name__}: {str(e)}\n{traceback.format_exc()}"
    SYSTEM_AVAILABLE = False

# NO DEMO SYSTEM - REAL DATA ONLY

# Load environment variables
load_dotenv()

# Verify critical environment variables
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
if not OPENAI_API_KEY:
    print("⚠️  WARNING: OPENAI_API_KEY not found in environment variables")
    print("   The system will not be able to perform AI analysis")
else:
    print(f"OpenAI API key loaded ({len(OPENAI_API_KEY)} chars)")

app = Flask(__name__)
CORS(app)

# HTML Template for the web interface
WEB_INTERFACE_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Brandintell - Comprehensive Competitive Intelligence</title>
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
        
        /* Progress Bar Styles */
        .progress-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
            font-weight: 600;
            color: #333;
        }
        
        .progress-bar {
            width: 100%;
            height: 20px;
            background-color: #e9ecef;
            border-radius: 10px;
            overflow: hidden;
            margin-bottom: 15px;
        }
        
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            width: 0%;
            transition: width 0.3s ease;
            border-radius: 10px;
        }
        
        .progress-details {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
            font-size: 14px;
            color: #666;
            background: #f8f9fa;
            padding: 10px;
            border-radius: 6px;
        }
        
        .examples li:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Brandintell</h1>
            <p>Comprehensive Competitive Intelligence Analysis</p>
        </div>
        
        <div class="content">
            <div class="feature-grid">
                <div class="feature-card">
                    <h3>Comprehensive Brand Analysis</h3>
                    <p>Logo, Brand Story, Personality, Colors, Typography, Visual Gallery</p>
                </div>
                <div class="feature-card">
                    <h3>🧠 AI-Powered Analysis</h3>
                    <p>McKinsey-level strategic insights and competitive positioning</p>
                </div>
                <div class="feature-card">
                    <h3>Real Data Only</h3>
                    <p>100% scraped data with enhanced privacy dialog handling</p>
                </div>
                <div class="feature-card">
                    <h3>🔤 Typography Analysis</h3>
                    <p>Real font extraction from CSS and style sheets</p>
                </div>
            </div>
            
            <div class="url-form">
                <div class="form-group">
                    <label for="url-input">Add Competitor URLs (3-15 companies):</label>
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
                    Generate Comprehensive Intelligence Report
                </button>
                
                <div id="status" class="status"></div>
                
                <!-- Progress Bar -->
                <div id="progress-container" style="display: none; margin-top: 20px;">
                    <div class="progress-header">
                        <span id="progress-text">Initializing analysis...</span>
                        <span id="progress-percent">0%</span>
                    </div>
                    <div class="progress-bar">
                        <div id="progress-fill" class="progress-fill"></div>
                    </div>
                    <div id="progress-details" class="progress-details">
                        <div>Current: <span id="current-task">Starting up...</span></div>
                        <div>Completed: <span id="completed-count">0</span> / <span id="total-count">0</span> brands</div>
                    </div>
                </div>
            </div>
            
            <div class="examples">
                <h4>Example URLs (click to add):</h4>
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
            
            // Calculate estimated time
            const estimatedMinutes = urls.length * 8; // 8 minutes per brand for deep analysis
            const timeMessage = estimatedMinutes > 60 ? 
                `${Math.floor(estimatedMinutes/60)}h ${estimatedMinutes%60}m` : 
                `${estimatedMinutes} minutes`;
            
            btn.disabled = true;
            btn.textContent = 'Starting Deep Analysis...';
            status.className = 'status loading';
            status.textContent = `Deep analysis in progress - estimated time: ${timeMessage}. Perfect time for a coffee break!`;
            
            // Show progress bar
            document.getElementById('progress-container').style.display = 'block';
            
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
                    a.download = 'premium_competitive_intelligence_report.html';
                    document.body.appendChild(a);
                    a.click();
                    window.URL.revokeObjectURL(url);
                    document.body.removeChild(a);
                    
                    status.className = 'status success';
                    status.textContent = 'Report generated successfully! Download should start automatically.';
                } else {
                    const error = await response.text();
                    throw new Error(error);
                }
                
            } catch (error) {
                status.className = 'status error';
                status.textContent = `❌ Error: ${error.message}`;
            } finally {
                btn.disabled = false;
                btn.textContent = 'Generate Comprehensive Intelligence Report';
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
    """Railway health check endpoint - simple and fast"""
    return 'OK', 200

@app.route('/api/status')
def api_status():
    """Simple status check"""
    return jsonify({
        'status': 'online',
        'app': 'Brandintell',
        'version': '1.0',
        'endpoints': ['/health', '/api/status', '/debug', '/api/generate-premium'],
        'system_loaded': SYSTEM_AVAILABLE
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
        from strategic_competitive_intelligence import StrategicCompetitiveIntelligence
        debug_info['import_status'] = 'Success'
    except Exception as e:
        debug_info['import_error'] = str(e)
        debug_info['import_traceback'] = traceback.format_exc()
    
    # Check dependencies
    try:
        import openai
        debug_info['openai_module'] = 'Loaded'
    except:
        debug_info['openai_module'] = 'Failed'
        
    try:
        import selenium
        debug_info['selenium_module'] = 'Loaded'
    except:
        debug_info['selenium_module'] = 'Failed'
        
    try:
        import pandas
        debug_info['pandas_module'] = 'Loaded'
    except:
        debug_info['pandas_module'] = 'Failed'
    
    return jsonify(debug_info)

@app.route('/api/generate-premium', methods=['POST'])
def generate_premium():
    """Generate premium competitive intelligence report"""
    # Check if system is available
    if not SYSTEM_AVAILABLE or not StrategicCompetitiveIntelligence:
        return jsonify({
            'error': 'Full competitive intelligence system required. No demo or fake data allowed.',
            'details': 'Strategic competitive intelligence system not available',
            'import_error': IMPORT_ERROR
        }), 503
    
    try:
        data = request.get_json()
        urls = data.get('urls', [])
        
        if len(urls) < 2:
            return jsonify({'error': 'At least 2 URLs required'}), 400
        
        if len(urls) > 15:
            return jsonify({'error': 'Maximum 15 URLs allowed'}), 400
        
        # ONLY use the full strategic competitive intelligence system
        generator = StrategicCompetitiveIntelligence()
        
        # Progress tracking (simplified for this implementation)
        progress_data = {
            'current_step': 0,
            'total_steps': len(urls) * 8,  # Approximate steps per brand
            'current_task': 'Starting analysis...',
            'brand_count': len(urls)
        }
        
        def progress_callback(message):
            progress_data['current_step'] += 1
            progress_data['current_task'] = message
            print(f"Progress: {message}")
        
        # Generate the FULL report with real data only
        # Use /tmp directory for Railway compatibility
        import tempfile
        
        temp_dir = tempfile.gettempdir()
        output_filename = os.path.join(temp_dir, f"brandintell_report_{int(time.time())}.html")
        
        print(f"Starting analysis with output to: {output_filename}")
        print(f"Analyzing {len(urls)} URLs: {urls}")
        
        output_file = generator.generate_strategic_intelligence_report(
            urls=urls,
            report_title="Brandintell Comprehensive Intelligence Analysis",
            output_filename=output_filename,
            progress_callback=progress_callback
        )
        
        if output_file and os.path.exists(output_file):
            return send_file(output_file, as_attachment=True, download_name='brandintell_comprehensive_report.html')
        else:
            return jsonify({'error': 'Failed to generate report'}), 500
            
    except Exception as e:
        import traceback
        error_details = {
            'error': str(e),
            'type': type(e).__name__,
            'traceback': traceback.format_exc()
        }
        print(f"Error in generate_premium: {error_details}")
        return jsonify(error_details), 500

@app.route('/api/status')
def status():
    """Service status endpoint"""
    return jsonify({
        'status': 'running',
        'service': 'Premium Competitive Intelligence',
        'version': '2.0',
        'features': [
            'Premium 6-row grid system',
            'Real typography analysis',
            'Visual gallery capture',
            'Privacy dialog mitigation',
            'McKinsey-level AI analysis',
            'Real brand color extraction'
        ],
        'system_available': SYSTEM_AVAILABLE,
        'endpoints': {
            'GET /': 'Web interface',
            'GET /health': 'Health check',
            'POST /api/generate-premium': 'Generate premium report',
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
    print(f"System available: {SYSTEM_AVAILABLE}")
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug_mode
    )