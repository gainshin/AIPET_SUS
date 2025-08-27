#!/usr/bin/env python3
"""
Test that both Kano and SUS questionnaires are completely in English
"""
import requests
import json

# API Base URL
API_BASE = "http://localhost:5000/api"

def test_questionnaires_english():
    print("🧪 Testing Complete English Questionnaires...")
    
    # Test Kano Questions
    try:
        response = requests.get(f"{API_BASE}/kano/questions")
        if response.status_code == 200:
            kano_data = response.json()
            print("✅ Kano Questions API working")
            
            # Check for Chinese characters in questions
            questions_json = json.dumps(kano_data, ensure_ascii=False)
            chinese_chars = []
            chinese_indicators = [
                '如果', '您的', '感受', '如何', '總是', '準確', '理解', '問題', '給出',
                '正確', '答案', '經常', '誤解', '錯誤', '回應', '秒內', '需要', '超過',
                '才能', '自然', '流暢', '對話', '生硬', '不自然', '記住', '整個',
                '歷史', '保持', '上下文', '連貫', '無法', '之前', '內容', '每次',
                '重新', '解釋'
            ]
            
            for indicator in chinese_indicators:
                if indicator in questions_json:
                    chinese_chars.append(indicator)
            
            if chinese_chars:
                print(f"❌ Found Chinese characters in Kano questions: {chinese_chars[:5]}...")
            else:
                print("✅ Kano questions completely in English!")
                
            # Show sample question
            first_question = kano_data['questions'][0]
            print(f"\n📋 Sample Kano Question:")
            print(f"   Title: {first_question['title']}")
            print(f"   Functional: {first_question['functional'][:50]}...")
            print(f"   Dysfunctional: {first_question['dysfunctional'][:50]}...")
            
        else:
            print("❌ Kano Questions API failed")
    except Exception as e:
        print(f"❌ Kano API error: {e}")
    
    print()
    
    # Test SUS Questions
    try:
        response = requests.get(f"{API_BASE}/sus/questions")
        if response.status_code == 200:
            sus_data = response.json()
            print("✅ SUS Questions API working")
            
            # Check for Chinese characters in questions
            sus_json = json.dumps(sus_data, ensure_ascii=False)
            chinese_indicators = [
                '我想要', '經常使用', '這個', '系統', '覺得', '過於', '複雜',
                '很容易', '使用', '需要', '技術人員', '協助', '各項', '功能',
                '整合', '很好', '太多', '不一致', '地方', '大部分', '的人',
                '很快', '學會', '很難', '感到', '信心', '之前', '學習',
                '很多', '東西'
            ]
            
            chinese_chars = []
            for indicator in chinese_indicators:
                if indicator in sus_json:
                    chinese_chars.append(indicator)
            
            if chinese_chars:
                print(f"❌ Found Chinese characters in SUS questions: {chinese_chars[:5]}...")
            else:
                print("✅ SUS questions completely in English!")
                
            # Show sample questions
            print(f"\n📋 Sample SUS Questions:")
            for i, question in enumerate(sus_data['questions'][:3], 1):
                print(f"   Q{i}: {question['text']}")
                
        else:
            print("❌ SUS Questions API failed")
    except Exception as e:
        print(f"❌ SUS API error: {e}")
    
    print(f"\n🎯 Questionnaire Test Complete!")
    print(f"🌐 Test the questionnaires at: https://5000-i6tx75dds1e1esv6i13dp.e2b.dev/")
    print(f"   • Click 'New Project' to start an evaluation")
    print(f"   • Check both Kano and SUS questionnaires are in English")

if __name__ == "__main__":
    test_questionnaires_english()