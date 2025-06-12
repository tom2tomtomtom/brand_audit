#!/usr/bin/env python3
"""
Development server runner for Brand Audit Tool
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import the Flask app
from app import app

if __name__ == '__main__':
    print("🚀 Starting Brand Audit Tool Development Server...")
    print("📊 Visit http://localhost:5000 to use the application")
    print("🛑 Press Ctrl+C to stop the server")
    print("")
    
    # Run in development mode
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
        threaded=True
    )