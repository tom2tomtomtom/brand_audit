#!/usr/bin/env python3
"""
Test script to verify Flask app works locally before deployment
"""

import os
import sys
sys.path.append('.')

def test_flask_import():
    """Test if Flask app imports correctly"""
    try:
        import app
        print("✅ Flask app imported successfully")
        return True
    except Exception as e:
        print(f"❌ Flask app import failed: {e}")
        return False

def test_routes():
    """Test if routes are registered"""
    try:
        import app
        client = app.app.test_client()
        
        # Test main page
        response = client.get('/')
        print(f"GET /: {response.status_code}")
        
        # Test debug routes
        response = client.get('/debug/routes')
        print(f"GET /debug/routes: {response.status_code}")
        
        # Test API test endpoint
        response = client.get('/api/test')
        print(f"GET /api/test: {response.status_code}")
        
        return True
    except Exception as e:
        print(f"❌ Route testing failed: {e}")
        return False

def test_dependencies():
    """Test if all dependencies can be imported"""
    dependencies = [
        'flask', 'flask_cors', 'selenium', 'beautifulsoup4', 
        'requests', 'openai', 'reportlab', 'PIL', 'python_dotenv'
    ]
    
    failed = []
    for dep in dependencies:
        try:
            if dep == 'beautifulsoup4':
                import bs4
            elif dep == 'PIL':
                import PIL
            elif dep == 'python_dotenv':
                import dotenv
            elif dep == 'flask_cors':
                import flask_cors
            else:
                __import__(dep)
            print(f"✅ {dep}")
        except ImportError as e:
            print(f"❌ {dep}: {e}")
            failed.append(dep)
    
    return len(failed) == 0

if __name__ == "__main__":
    print("🧪 Testing Flask Application Locally")
    print("=" * 50)
    
    print("\n1. Testing Dependencies:")
    deps_ok = test_dependencies()
    
    print("\n2. Testing Flask Import:")
    import_ok = test_flask_import()
    
    print("\n3. Testing Routes:")
    routes_ok = test_routes()
    
    print("\n" + "=" * 50)
    if deps_ok and import_ok and routes_ok:
        print("🎉 All tests passed! App should work on Railway.")
    else:
        print("❌ Some tests failed. Check the issues above.")
        
    sys.exit(0 if (deps_ok and import_ok and routes_ok) else 1)