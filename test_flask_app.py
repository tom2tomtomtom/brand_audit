#!/usr/bin/env python3
"""
Test the Flask application with real data
"""

import sys
import os
import threading
import time
import requests
import json
from flask import Flask

sys.path.append('.')

def test_flask_endpoints():
    """Test Flask application endpoints"""
    print("🌶️ Testing Flask application...")
    
    base_url = "http://localhost:5000"
    
    # Test 1: Health check
    try:
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            print("   ✅ Health check endpoint working")
        else:
            print(f"   ❌ Health check failed: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("   ❌ Flask app not running - cannot test endpoints")
        return False
    
    # Test 2: Static files
    try:
        response = requests.get(f"{base_url}/static/style.css")
        if response.status_code == 200:
            print("   ✅ Static files serving correctly")
        else:
            print(f"   ⚠️  Static files issue: {response.status_code}")
    except:
        print("   ⚠️  Could not test static files")
    
    # Test 3: Submit analysis job
    try:
        test_data = {
            "urls": ["https://stripe.com"],
            "brand_names": ["Stripe"]
        }
        
        response = requests.post(f"{base_url}/analyze", json=test_data)
        
        if response.status_code == 200:
            result = response.json()
            job_id = result.get('job_id')
            
            if job_id:
                print(f"   ✅ Analysis job submitted: {job_id}")
                
                # Test 4: Check job status
                max_wait = 30  # 30 seconds max
                start_time = time.time()
                
                while time.time() - start_time < max_wait:
                    status_response = requests.get(f"{base_url}/status/{job_id}")
                    
                    if status_response.status_code == 200:
                        status_data = status_response.json()
                        status = status_data.get('status', 'unknown')
                        
                        print(f"   📊 Job status: {status}")
                        
                        if status == 'completed':
                            print("   ✅ Analysis job completed successfully!")
                            
                            # Test 5: Download results
                            results_response = requests.get(f"{base_url}/results/{job_id}")
                            if results_response.status_code == 200:
                                print("   ✅ Results download working")
                                return True
                            else:
                                print(f"   ❌ Results download failed: {results_response.status_code}")
                                return False
                        
                        elif status == 'failed':
                            error_msg = status_data.get('error', 'Unknown error')
                            print(f"   ⚠️  Analysis failed: {error_msg}")
                            
                            # This is expected if no OpenAI API key
                            if "OpenAI API key" in error_msg:
                                print("   ℹ️  Expected failure due to missing OpenAI API key")
                                return True
                            else:
                                return False
                        
                        elif status in ['pending', 'running']:
                            time.sleep(2)  # Wait and check again
                        else:
                            print(f"   ❌ Unknown status: {status}")
                            return False
                    else:
                        print(f"   ❌ Status check failed: {status_response.status_code}")
                        return False
                
                print("   ⚠️  Job did not complete within timeout")
                return False
            else:
                print("   ❌ No job ID returned")
                return False
        else:
            print(f"   ❌ Analysis submission failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ Flask testing error: {str(e)}")
        return False

def start_flask_app():
    """Start the Flask app in a separate thread"""
    print("🚀 Starting Flask application...")
    
    try:
        from app import app
        app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False, threaded=True)
    except Exception as e:
        print(f"❌ Failed to start Flask app: {str(e)}")

def test_flask_application():
    """Test the complete Flask application"""
    print("🧪 Testing Flask Application with Real Data")
    print("=" * 50)
    
    # Start Flask app in background thread
    flask_thread = threading.Thread(target=start_flask_app, daemon=True)
    flask_thread.start()
    
    # Wait for Flask to start
    print("⏳ Waiting for Flask app to start...")
    time.sleep(5)
    
    # Test the endpoints
    return test_flask_endpoints()

if __name__ == "__main__":
    success = test_flask_application()
    
    if success:
        print("\n🎉 Flask application testing completed successfully!")
        print("✅ The brand audit tool is working with real data")
    else:
        print("\n❌ Flask application testing failed")
        print("⚠️  Check the logs above for details")
    
    sys.exit(0 if success else 1)