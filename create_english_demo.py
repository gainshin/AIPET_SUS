#!/usr/bin/env python3
"""
Create a demo evaluation to showcase the English interface
"""
import requests
import json

# API Base URL
API_BASE = "http://localhost:5000/api"

# English demo project info
project_info = {
    "name": "ChatGPT Assistant Demo",
    "description": "AI-powered conversational assistant for customer service",
    "version": "2.0.1", 
    "team": "AI Innovation Team"
}

# Sample Kano responses (simulating user evaluation)
kano_responses = {
    "response_accuracy": {"functional": 1, "dysfunctional": 5},  # Attractive
    "response_speed": {"functional": 2, "dysfunctional": 4},     # Must-be  
    "natural_conversation": {"functional": 1, "dysfunctional": 4}, # Attractive
    "context_memory": {"functional": 2, "dysfunctional": 5},     # Must-be
    "personalization": {"functional": 1, "dysfunctional": 3},   # Attractive
    "multi_modal": {"functional": 1, "dysfunctional": 3},       # Attractive
    "error_handling": {"functional": 2, "dysfunctional": 4},    # Must-be
    "learning_ability": {"functional": 1, "dysfunctional": 3},  # Attractive
    "privacy_security": {"functional": 2, "dysfunctional": 5},  # Must-be
    "integration": {"functional": 4, "dysfunctional": 2}        # One-dimensional
}

# Sample SUS responses (favorable ratings)
sus_responses = {
    "q1": 4, "q2": 2, "q3": 4, "q4": 2, "q5": 4,
    "q6": 2, "q7": 4, "q8": 2, "q9": 4, "q10": 2
}

def create_english_demo():
    print("🚀 Creating English Interface Demo Evaluation...")
    
    # Prepare evaluation data
    evaluation_data = {
        "project_info": project_info,
        "kano_responses": kano_responses,
        "sus_responses": sus_responses
    }
    
    try:
        # Send evaluation request
        response = requests.post(f"{API_BASE}/evaluate", 
                               json=evaluation_data,
                               headers={'Content-Type': 'application/json'})
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                evaluation_id = result['data']['evaluation_id']
                print(f"✅ Demo evaluation created successfully!")
                print(f"📋 Evaluation ID: {evaluation_id}")
                print(f"🎯 Project: {project_info['name']}")
                
                # Display key results
                sus_eval = result['data']['sus_evaluation']
                overall = result['data']['overall_assessment']
                kano_eval = result['data']['kano_evaluation']
                
                print(f"\n📊 Quick Results Preview:")
                print(f"  • SUS Score: {sus_eval['score']:.1f}/100")
                print(f"  • Overall Score: {overall['overall_score']:.1f}/100") 
                print(f"  • Maturity Level: {overall['maturity_level']}")
                
                print(f"\n🎨 Kano Category Distribution:")
                for category, percentage in kano_eval['summary']['category_percentages'].items():
                    if percentage > 0:
                        print(f"  • {category}: {percentage:.1f}%")
                
                print(f"\n🌐 Access the English Demo Results:")
                print(f"🔗 Direct Link: http://localhost:5000?eval={evaluation_id}")
                print(f"📱 Public URL: https://5000-i6tx75dds1e1esv6i13dp.e2b.dev?eval={evaluation_id}")
                
                print(f"\n✨ Features to test in English interface:")
                print(f"  • Dashboard navigation and statistics")
                print(f"  • New project creation form")  
                print(f"  • Kano Model assessment with English options")
                print(f"  • SUS Scale evaluation with English labels")
                print(f"  • Results analysis with English descriptions")
                print(f"  • Kano Matrix scatter plot visualization")
                print(f"  • PDF report generation")
                print(f"  • Assessment history viewing")
                        
            else:
                print(f"❌ Evaluation failed: {result.get('error')}")
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Unable to connect to server. Please ensure service is running.")
    except Exception as e:
        print(f"❌ Error occurred: {e}")

if __name__ == "__main__":
    create_english_demo()