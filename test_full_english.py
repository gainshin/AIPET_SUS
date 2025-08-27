#!/usr/bin/env python3
"""
Test complete English interface after fixing all Chinese text
"""
import requests
import json

# API Base URL
API_BASE = "http://localhost:5000/api"

# Test project info
project_info = {
    "name": "Voice Assistant Test",
    "description": "Smart voice-controlled AI assistant with natural language processing",
    "version": "3.1.0",
    "team": "Voice Technology Team"
}

# Test Kano responses
kano_responses = {
    "response_accuracy": {"functional": 2, "dysfunctional": 4},
    "response_speed": {"functional": 1, "dysfunctional": 5},
    "natural_conversation": {"functional": 1, "dysfunctional": 4},
    "context_memory": {"functional": 2, "dysfunctional": 5},
    "personalization": {"functional": 1, "dysfunctional": 3},
    "multi_modal": {"functional": 1, "dysfunctional": 3},
    "error_handling": {"functional": 2, "dysfunctional": 4},
    "learning_ability": {"functional": 1, "dysfunctional": 3},
    "privacy_security": {"functional": 2, "dysfunctional": 5},
    "integration": {"functional": 2, "dysfunctional": 4}
}

# Test SUS responses (good score)
sus_responses = {
    "q1": 4, "q2": 2, "q3": 5, "q4": 1, "q5": 4,
    "q6": 2, "q7": 4, "q8": 1, "q9": 5, "q10": 2
}

def test_full_english():
    print("🧪 Testing Complete English Interface (No Chinese Text)...")
    
    # Create evaluation
    evaluation_data = {
        "project_info": project_info,
        "kano_responses": kano_responses,
        "sus_responses": sus_responses
    }
    
    try:
        response = requests.post(f"{API_BASE}/evaluate", 
                               json=evaluation_data,
                               headers={'Content-Type': 'application/json'})
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                evaluation_id = result['data']['evaluation_id']
                print(f"✅ Test evaluation created: {evaluation_id}")
                
                # Check key result fields for English text
                sus_eval = result['data']['sus_evaluation']
                overall = result['data']['overall_assessment']
                kano_eval = result['data']['kano_evaluation']
                
                print(f"\n📊 Results Validation:")
                print(f"  • SUS Score: {sus_eval['score']:.1f}/100")
                print(f"  • Acceptability: '{sus_eval['acceptability']}'")
                print(f"  • Maturity Level: '{overall['maturity_level']}'")
                print(f"  • Overall Score: {overall['overall_score']:.1f}/100")
                
                # Validate English-only content
                chinese_indicators = ['良好', '具競爭力', '可接受', '不可接受', '基礎型', '期望型', '魅力型']
                english_found = True
                
                for indicator in chinese_indicators:
                    result_str = json.dumps(result, ensure_ascii=False)
                    if indicator in result_str:
                        print(f"❌ Found Chinese text: '{indicator}' in results")
                        english_found = False
                
                if english_found:
                    print("✅ No Chinese text found in API results!")
                
                print(f"\n🎯 Kano Categories (should be in English):")
                for category, percentage in kano_eval['summary']['category_percentages'].items():
                    if percentage > 0:
                        print(f"  • {category}: {percentage:.1f}%")
                
                print(f"\n🌐 Test Results Page:")
                print(f"🔗 http://localhost:5000?eval={evaluation_id}")
                print(f"📱 https://5000-i6tx75dds1e1esv6i13dp.e2b.dev?eval={evaluation_id}")
                
                print(f"\n✅ All Chinese text should now be converted to English!")
                return evaluation_id
                
            else:
                print(f"❌ Evaluation failed: {result.get('error')}")
                return None
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

if __name__ == "__main__":
    test_full_english()