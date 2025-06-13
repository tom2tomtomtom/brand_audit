#!/usr/bin/env python3
"""
Minimal health-only server for Railway deployment
Fast startup for health checks before loading the full system
"""

import os
from flask import Flask, jsonify
from datetime import datetime

app = Flask(__name__)

@app.route('/health')
def health():
    """Railway health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'mode': 'health_only',
        'message': 'Health check server ready - full system loading'
    }), 200

@app.route('/')
def index():
    """Basic index"""
    return jsonify({
        'status': 'loading',
        'message': 'Full competitive intelligence system is loading...'
    }), 503

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"🏥 Health-only server starting on port {port}")
    app.run(host='0.0.0.0', port=port)