#!/usr/bin/env python3
"""
Test script to verify English interface functionality
"""
import requests
import json

# API Base URL
API_BASE = "http://localhost:5000/api"

def test_english_interface():
    print("🌐 Testing English Interface...")
    
    # Test Kano questions API
    try:
        response = requests.get(f"{API_BASE}/kano/questions")
        if response.status_code == 200:
            print("✅ Kano questions API working")
        else:
            print("❌ Kano questions API failed")
    except Exception as e:
        print(f"❌ Kano API error: {e}")
    
    # Test SUS questions API
    try:
        response = requests.get(f"{API_BASE}/sus/questions")
        if response.status_code == 200:
            print("✅ SUS questions API working")
        else:
            print("❌ SUS questions API failed")
    except Exception as e:
        print(f"❌ SUS API error: {e}")
    
    # Test main page access
    try:
        response = requests.get("http://localhost:5000/")
        if response.status_code == 200:
            content = response.text
            # Check for English content
            english_indicators = [
                'lang="en"',
                'Dashboard',
                'New Project',
                'History',
                'Settings',
                'Welcome back',
                'Processing...'
            ]
            
            english_found = sum(1 for indicator in english_indicators if indicator in content)
            print(f"✅ Main page accessible - English indicators found: {english_found}/{len(english_indicators)}")
            
            if english_found >= len(english_indicators) - 1:  # Allow for 1 missing
                print("✅ Interface successfully converted to English!")
            else:
                print("⚠️  Some English content may be missing")
        else:
            print("❌ Main page access failed")
    except Exception as e:
        print(f"❌ Main page error: {e}")
    
    print(f"\n🎯 English Interface Test Complete!")
    print(f"🔗 Access your English application at: http://localhost:5000")

if __name__ == "__main__":
    test_english_interface()