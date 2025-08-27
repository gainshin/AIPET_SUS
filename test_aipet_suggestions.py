#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test AIPET-based SUS Improvement Suggestions
測試基於AIPET框架的SUS改善建議功能
"""

import requests
import json

def test_aipet_sus_suggestions():
    """測試AIPET框架的SUS改善建議"""
    print("🧪 Testing AIPET-based SUS Improvement Suggestions...")
    
    # 模擬一個評估回應，其中某些問題得分較低，需要改善建議
    sus_responses = [
        {"question": "q1", "score": 2},  # Low score - needs improvement
        {"question": "q2", "score": 4},  # High score - good
        {"question": "q3", "score": 2},  # Low score - needs improvement  
        {"question": "q4", "score": 1},  # Very low score - needs improvement
        {"question": "q5", "score": 3},  # Medium score
        {"question": "q6", "score": 2},  # Low score - needs improvement
        {"question": "q7", "score": 1},  # Very low score - needs improvement
        {"question": "q8", "score": 4},  # High score - good
        {"question": "q9", "score": 2},  # Low score - needs improvement
        {"question": "q10", "score": 1}  # Very low score - needs improvement
    ]
    
    # 發送評估請求
    try:
        url = "http://localhost:5001/api/evaluate"
        # 添加基本的Kano數據以滿足API要求
        basic_kano_responses = {
            "response_accuracy": {"functional": "like", "dysfunctional": "dislike"},
            "response_speed": {"functional": "expect", "dysfunctional": "tolerate"},
            "understanding_ability": {"functional": "like", "dysfunctional": "dislike"}
        }
        
        payload = {
            "project_name": "test_aipet_framework",
            "kano_responses": basic_kano_responses,
            "sus_responses": {f"q{i+1}": resp["score"] for i, resp in enumerate(sus_responses)}
        }
        
        response = requests.post(url, json=payload, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ SUS evaluation API working")
            
            # 檢查AIPET建議
            if 'improvement_recommendations' in result:
                recommendations = result['improvement_recommendations']
                print(f"\n📋 AIPET-based Improvement Recommendations ({len(recommendations)} items):")
                
                # 統計AIPET維度分布
                aipet_dimensions = {}
                for rec in recommendations:
                    if 'aipet_dimension' in rec:
                        dimension = rec['aipet_dimension'].split(' - ')[0]  # 提取維度字母
                        aipet_dimensions[dimension] = aipet_dimensions.get(dimension, 0) + 1
                
                print(f"\n🔍 AIPET Dimensions Coverage:")
                for dim, count in sorted(aipet_dimensions.items()):
                    print(f"   {dim}: {count} recommendations")
                
                # 顯示範例建議
                print(f"\n💡 Sample AIPET Recommendations:")
                for i, rec in enumerate(recommendations[:3], 1):
                    print(f"\n   {i}. Area: {rec['area']}")
                    print(f"      Framework: {rec.get('aipet_dimension', 'N/A')}")
                    print(f"      Priority: {rec['priority']}")
                    print(f"      Suggestion: {rec['suggestion'][:100]}...")
                
                print(f"\n🎯 AIPET Framework Integration Complete!")
                return True
            else:
                print("❌ No improvement recommendations found")
                return False
                
        else:
            print(f"❌ API request failed with status {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Network error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_aipet_principles_import():
    """測試AIPET原則模組導入"""
    print("\n🔧 Testing AIPET Principles Module...")
    
    try:
        from models.improvement_recommendations_aipet_principles import AIPETFramework, AgentiveUXPrinciples
        
        # 測試AIPET框架
        framework = AIPETFramework()
        principles = framework.get_framework_principles()
        
        print("✅ AIPET Framework imported successfully")
        print(f"📊 Framework includes {len(principles)} core principles:")
        
        for key, principle in principles.items():
            print(f"   {key} - {principle['name']}")
        
        # 測試成熟度模型
        maturity = framework.get_maturity_model()
        print(f"\n📈 Maturity Model includes {len(maturity)} levels:")
        for level, info in maturity.items():
            print(f"   {level}: {info['name']}")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 AIPET Framework Integration Test\n")
    
    # 測試原則模組
    principles_ok = test_aipet_principles_import()
    
    # 測試SUS建議功能
    suggestions_ok = test_aipet_sus_suggestions()
    
    if principles_ok and suggestions_ok:
        print("\n🎉 All AIPET integration tests passed!")
        print("🌐 Access the system at: https://5000-i6tx75dds1e1esv6i13dp.e2b.dev/")
        print("   • Create new evaluation to test AIPET-based recommendations")
        print("   • Look for Agentive UX improvement suggestions")
    else:
        print("\n⚠️  Some tests failed. Please check the implementation.")