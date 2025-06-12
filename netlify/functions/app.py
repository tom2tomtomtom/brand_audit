import json
import os
from urllib.parse import parse_qs

def handler(event, context):
    """
    Netlify Function handler for Flask-like functionality
    """
    try:
        # Handle different HTTP methods
        http_method = event.get('httpMethod', 'GET')
        path = event.get('path', '/')
        query_params = event.get('queryStringParameters') or {}
        
        # Parse body for POST requests
        body = None
        if http_method == 'POST' and event.get('body'):
            try:
                body = json.loads(event['body'])
            except:
                body = parse_qs(event['body'])
        
        # Route handling
        if path == '/' or path == '/index.html':
            return serve_index()
        elif path.startswith('/api/analyze'):
            return handle_analyze(body)
        elif path.startswith('/api/status/'):
            job_id = path.split('/')[-1]
            return handle_status(job_id)
        elif path.startswith('/api/results/'):
            job_id = path.split('/')[-1]
            return handle_results(job_id)
        else:
            return {
                'statusCode': 404,
                'body': json.dumps({'error': 'Not found'})
            }
            
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'error': str(e)})
        }

def serve_index():
    """Serve the main HTML page"""
    try:
        # Read the HTML template
        with open('public/index.html', 'r') as f:
            html_content = f.read()
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'text/html',
                'Access-Control-Allow-Origin': '*'
            },
            'body': html_content
        }
    except FileNotFoundError:
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'text/html',
                'Access-Control-Allow-Origin': '*'
            },
            'body': '''
            <!DOCTYPE html>
            <html>
            <head>
                <title>Brand Audit Tool</title>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <script src="https://cdn.tailwindcss.com"></script>
            </head>
            <body class="bg-gray-50">
                <div class="min-h-screen py-12 px-4">
                    <div class="max-w-4xl mx-auto">
                        <div class="bg-white rounded-lg shadow-lg p-8">
                            <h1 class="text-3xl font-bold text-gray-900 mb-8 text-center">
                                Brand Competitor Analysis Tool
                            </h1>
                            
                            <div class="bg-yellow-50 border border-yellow-200 rounded-lg p-6 mb-8">
                                <h2 class="text-lg font-semibold text-yellow-800 mb-2">⚠️ Netlify Deployment Notice</h2>
                                <p class="text-yellow-700">
                                    This Flask application requires server-side processing for web scraping and AI analysis. 
                                    Netlify Functions have limitations that prevent full functionality:
                                </p>
                                <ul class="list-disc list-inside mt-3 text-yellow-700">
                                    <li>15-second execution timeout (analysis takes 5-10 minutes)</li>
                                    <li>No persistent storage for results</li>
                                    <li>Limited Python package support</li>
                                    <li>Cannot run Selenium WebDriver</li>
                                </ul>
                            </div>
                            
                            <div class="bg-blue-50 border border-blue-200 rounded-lg p-6 mb-8">
                                <h2 class="text-lg font-semibold text-blue-800 mb-2">🚀 Recommended Deployment</h2>
                                <p class="text-blue-700 mb-3">For full functionality, deploy on platforms that support long-running Python applications:</p>
                                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                                    <div class="bg-white rounded p-4 border">
                                        <h3 class="font-semibold text-gray-800">Docker Deployment</h3>
                                        <code class="text-sm text-gray-600">docker-compose up</code>
                                    </div>
                                    <div class="bg-white rounded p-4 border">
                                        <h3 class="font-semibold text-gray-800">Heroku</h3>
                                        <code class="text-sm text-gray-600">git push heroku main</code>
                                    </div>
                                    <div class="bg-white rounded p-4 border">
                                        <h3 class="font-semibold text-gray-800">Railway</h3>
                                        <code class="text-sm text-gray-600">railway up</code>
                                    </div>
                                    <div class="bg-white rounded p-4 border">
                                        <h3 class="font-semibold text-gray-800">DigitalOcean</h3>
                                        <code class="text-sm text-gray-600">Docker + droplet</code>
                                    </div>
                                </div>
                            </div>
                            
                            <div class="bg-gray-50 rounded-lg p-6">
                                <h2 class="text-lg font-semibold text-gray-800 mb-2">📋 Application Features</h2>
                                <ul class="list-disc list-inside text-gray-700 space-y-1">
                                    <li>Real website scraping using Selenium WebDriver</li>
                                    <li>AI-powered brand analysis with OpenAI GPT-4</li>
                                    <li>Professional PDF report generation</li>
                                    <li>Comprehensive competitive analysis</li>
                                    <li>Visual asset extraction (logos, colors, fonts)</li>
                                    <li>No dummy or fallback data generation</li>
                                </ul>
                            </div>
                            
                            <div class="mt-8 text-center">
                                <p class="text-gray-600">
                                    Repository: <a href="https://github.com/tom2tomtomtom/brand_audit" class="text-blue-600 hover:underline">github.com/tom2tomtomtom/brand_audit</a>
                                </p>
                            </div>
                        </div>
                    </div>
                </div>
            </body>
            </html>
            '''
        }

def handle_analyze(body):
    """Handle analysis request"""
    return {
        'statusCode': 501,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps({
            'error': 'Analysis not supported on Netlify',
            'message': 'This functionality requires long-running server processes. Please deploy on Docker, Heroku, or similar platform.',
            'deployment_instructions': 'See README.md for deployment options'
        })
    }

def handle_status(job_id):
    """Handle status request"""
    return {
        'statusCode': 501,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps({
            'error': 'Status checking not supported on Netlify',
            'message': 'Please deploy on a platform that supports persistent processes'
        })
    }

def handle_results(job_id):
    """Handle results request"""
    return {
        'statusCode': 501,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps({
            'error': 'Results download not supported on Netlify',
            'message': 'Please deploy on a platform with persistent storage'
        })
    }