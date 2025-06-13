#!/usr/bin/env python3
"""
Railway Web Interface with Async Job Processing
Handles long-running analysis tasks without timeouts
"""

import os
import json
import time
import uuid
from flask import Flask, request, jsonify, render_template_string, send_file
from flask_cors import CORS
from dotenv import load_dotenv
from datetime import datetime
import threading
from collections import defaultdict

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

# Load environment variables
load_dotenv()

# Verify critical environment variables
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
if not OPENAI_API_KEY:
    print("⚠️  WARNING: OPENAI_API_KEY not found in environment variables")
else:
    print(f"OpenAI API key loaded ({len(OPENAI_API_KEY)} chars)")

app = Flask(__name__)
CORS(app)

# Job storage (in-memory for simplicity, could use Redis in production)
jobs = defaultdict(dict)
job_lock = threading.Lock()

def run_analysis_job(job_id, urls):
    """Run analysis in background thread"""
    with job_lock:
        jobs[job_id]['status'] = 'running'
        jobs[job_id]['started_at'] = datetime.now().isoformat()
        jobs[job_id]['progress'] = 0
        jobs[job_id]['message'] = 'Initializing analysis...'
    
    try:
        generator = StrategicCompetitiveIntelligence()
        
        def progress_callback(message):
            with job_lock:
                jobs[job_id]['progress'] += 1
                jobs[job_id]['message'] = message
                jobs[job_id]['last_update'] = datetime.now().isoformat()
            print(f"Job {job_id}: {message}")
        
        # Use temp directory
        import tempfile
        temp_dir = tempfile.gettempdir()
        output_filename = os.path.join(temp_dir, f"brandintell_{job_id}.html")
        
        output_file = generator.generate_strategic_intelligence_report(
            urls=urls,
            report_title="Brandintell Comprehensive Intelligence Analysis",
            output_filename=output_filename,
            progress_callback=progress_callback
        )
        
        with job_lock:
            jobs[job_id]['status'] = 'completed'
            jobs[job_id]['output_file'] = output_file
            jobs[job_id]['completed_at'] = datetime.now().isoformat()
            
    except Exception as e:
        import traceback
        with job_lock:
            jobs[job_id]['status'] = 'failed'
            jobs[job_id]['error'] = str(e)
            jobs[job_id]['traceback'] = traceback.format_exc()
            jobs[job_id]['failed_at'] = datetime.now().isoformat()
        print(f"Job {job_id} failed: {e}")

# HTML Template (simplified for async)
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
        
        .progress-container {
            margin-top: 20px;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 8px;
        }
        
        .progress-bar {
            width: 100%;
            height: 20px;
            background-color: #e9ecef;
            border-radius: 10px;
            overflow: hidden;
            margin-bottom: 10px;
        }
        
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            width: 0%;
            transition: width 0.3s ease;
            border-radius: 10px;
        }
        
        .progress-message {
            font-size: 14px;
            color: #666;
            margin-top: 10px;
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
                    Generate Comprehensive Intelligence Report
                </button>
                
                <div id="status" class="status"></div>
                
                <div id="progress-container" class="progress-container" style="display: none;">
                    <div class="progress-bar">
                        <div id="progress-fill" class="progress-fill"></div>
                    </div>
                    <div id="progress-message" class="progress-message">Starting analysis...</div>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        let urls = [];
        let currentJobId = null;
        let pollInterval = null;
        
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
            const progressContainer = document.getElementById('progress-container');
            
            btn.disabled = true;
            btn.textContent = 'Starting Analysis...';
            status.className = 'status loading';
            status.textContent = 'Initiating analysis job...';
            progressContainer.style.display = 'block';
            
            try {
                // Start the job
                const response = await fetch('/api/start-analysis', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ urls: urls })
                });
                
                if (!response.ok) {
                    const error = await response.json();
                    throw new Error(error.error || 'Failed to start analysis');
                }
                
                const data = await response.json();
                currentJobId = data.job_id;
                
                status.textContent = `Analysis started. Job ID: ${currentJobId}`;
                
                // Start polling for status
                pollJobStatus();
                
            } catch (error) {
                status.className = 'status error';
                status.textContent = `Error: ${error.message}`;
                btn.disabled = false;
                btn.textContent = 'Generate Comprehensive Intelligence Report';
                progressContainer.style.display = 'none';
            }
        }
        
        async function pollJobStatus() {
            if (!currentJobId) return;
            
            try {
                const response = await fetch(`/api/job-status/${currentJobId}`);
                const data = await response.json();
                
                const progressFill = document.getElementById('progress-fill');
                const progressMessage = document.getElementById('progress-message');
                const status = document.getElementById('status');
                const btn = document.getElementById('generate-btn');
                
                if (data.status === 'running') {
                    // Update progress
                    const progress = Math.min((data.progress || 0) * 5, 95); // Rough estimate
                    progressFill.style.width = progress + '%';
                    progressMessage.textContent = data.message || 'Processing...';
                    
                    // Continue polling
                    pollInterval = setTimeout(pollJobStatus, 2000);
                    
                } else if (data.status === 'completed') {
                    // Job completed successfully
                    progressFill.style.width = '100%';
                    progressMessage.textContent = 'Analysis complete!';
                    status.className = 'status success';
                    status.textContent = 'Report generated successfully! Downloading...';
                    
                    // Download the report
                    window.location.href = `/api/download-report/${currentJobId}`;
                    
                    // Reset UI
                    btn.disabled = false;
                    btn.textContent = 'Generate Comprehensive Intelligence Report';
                    setTimeout(() => {
                        document.getElementById('progress-container').style.display = 'none';
                    }, 3000);
                    
                } else if (data.status === 'failed') {
                    // Job failed
                    status.className = 'status error';
                    status.textContent = `Analysis failed: ${data.error}`;
                    btn.disabled = false;
                    btn.textContent = 'Generate Comprehensive Intelligence Report';
                    document.getElementById('progress-container').style.display = 'none';
                }
                
            } catch (error) {
                console.error('Error polling job status:', error);
                // Continue polling even on error
                pollInterval = setTimeout(pollJobStatus, 2000);
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

@app.route('/api/start-analysis', methods=['POST'])
def start_analysis():
    """Start analysis job in background"""
    if not SYSTEM_AVAILABLE or not StrategicCompetitiveIntelligence:
        return jsonify({
            'error': 'Strategic competitive intelligence system not available',
            'import_error': IMPORT_ERROR
        }), 503
    
    try:
        data = request.get_json()
        urls = data.get('urls', [])
        
        if len(urls) < 2:
            return jsonify({'error': 'At least 2 URLs required'}), 400
        
        if len(urls) > 15:
            return jsonify({'error': 'Maximum 15 URLs allowed'}), 400
        
        # Create job ID
        job_id = str(uuid.uuid4())
        
        # Initialize job
        with job_lock:
            jobs[job_id] = {
                'id': job_id,
                'status': 'pending',
                'urls': urls,
                'created_at': datetime.now().isoformat(),
                'progress': 0
            }
        
        # Start background thread
        thread = threading.Thread(target=run_analysis_job, args=(job_id, urls))
        thread.daemon = True
        thread.start()
        
        return jsonify({
            'job_id': job_id,
            'status': 'started',
            'message': f'Analysis started for {len(urls)} URLs'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/job-status/<job_id>')
def job_status(job_id):
    """Get job status"""
    with job_lock:
        job = jobs.get(job_id)
    
    if not job:
        return jsonify({'error': 'Job not found'}), 404
    
    return jsonify(job)

@app.route('/api/download-report/<job_id>')
def download_report(job_id):
    """Download completed report"""
    with job_lock:
        job = jobs.get(job_id)
    
    if not job:
        return jsonify({'error': 'Job not found'}), 404
    
    if job['status'] != 'completed':
        return jsonify({'error': 'Job not completed'}), 400
    
    output_file = job.get('output_file')
    if output_file and os.path.exists(output_file):
        return send_file(output_file, as_attachment=True, 
                        download_name='brandintell_comprehensive_report.html')
    else:
        return jsonify({'error': 'Report file not found'}), 404

@app.route('/api/status')
def api_status():
    """Service status endpoint"""
    return jsonify({
        'status': 'running',
        'service': 'Brandintell Async',
        'version': '2.1',
        'system_available': SYSTEM_AVAILABLE,
        'endpoints': {
            'GET /': 'Web interface',
            'GET /health': 'Health check',
            'POST /api/start-analysis': 'Start analysis job',
            'GET /api/job-status/<id>': 'Get job status',
            'GET /api/download-report/<id>': 'Download report'
        }
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug_mode = os.environ.get('FLASK_ENV') == 'development'
    
    print(f"🚀 Starting Brandintell Async on port {port}")
    print(f"System available: {SYSTEM_AVAILABLE}")
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug_mode
    )