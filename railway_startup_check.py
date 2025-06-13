#!/usr/bin/env python3
"""
Railway startup verification script
"""
import os
import sys
import subprocess

def check_chrome():
    """Check if Chrome is properly installed"""
    try:
        result = subprocess.run(['google-chrome', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Chrome installed: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ Chrome error: {result.stderr}")
            return False
    except FileNotFoundError:
        print("❌ Chrome not found in PATH")
        return False

def check_chromedriver():
    """Check if ChromeDriver is available"""
    try:
        result = subprocess.run(['chromedriver', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ ChromeDriver installed: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ ChromeDriver error: {result.stderr}")
            return False
    except FileNotFoundError:
        print("❌ ChromeDriver not found in PATH")
        return False

def check_display():
    """Check if DISPLAY is set for headless Chrome"""
    display = os.environ.get('DISPLAY')
    if display:
        print(f"✅ DISPLAY set: {display}")
        return True
    else:
        print("❌ DISPLAY not set - Chrome may fail")
        return False

def check_openai_key():
    """Check if OpenAI API key is available"""
    key = os.environ.get('OPENAI_API_KEY')
    if key:
        print(f"✅ OpenAI API key found ({len(key)} chars)")
        return True
    else:
        print("❌ OpenAI API key not found")
        return False

def main():
    """Run all startup checks"""
    print("=== Railway Startup Verification ===")
    print(f"Working directory: {os.getcwd()}")
    print(f"Python version: {sys.version}")
    print(f"PORT: {os.environ.get('PORT', 'NOT SET')}")
    print("")
    
    checks = [
        ("Chrome", check_chrome()),
        ("ChromeDriver", check_chromedriver()),
        ("Display", check_display()),
        ("OpenAI API Key", check_openai_key())
    ]
    
    failed = [name for name, result in checks if not result]
    
    if failed:
        print(f"\n⚠️  Failed checks: {', '.join(failed)}")
        print("The application may not function properly.")
    else:
        print("\n✅ All checks passed! Ready to start.")
    
    return len(failed) == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)