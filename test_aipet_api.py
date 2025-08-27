#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test AIPET Questions API
測試 AIPET 問題 API
"""

import requests
import json

def test_aipet_api():
    """測試 AIPET API 端點"""
    try:
        # 測試 AIPET 問題端點
        response = requests.get("http://localhost:5000/api/aipet/questions", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print("✅ AIPET Questions API working")
                print(f"📋 Total questions: {data['total_questions']}")
                
                # 顯示維度分布
                stats = data.get('dimension_statistics', {})
                print("\n📊 Dimension Distribution:")
                for dim, count in stats.items():
                    print(f"   {dim}: {count} questions")
                
                # 顯示幾個範例問題
                questions = data.get('questions', [])
                print(f"\n💡 Sample Questions (first 2):")
                for i, q in enumerate(questions[:2], 1):
                    print(f"\n   {i}. ID: {q['id']}")
                    print(f"      Dimension: {q['dimension']} - {q['dimension_name']}")
                    print(f"      Text: {q['text'][:80]}...")
                
                return True
            else:
                print(f"❌ API returned error: {data.get('error')}")
                return False
        else:
            print(f"❌ HTTP Error {response.status_code}: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed - Flask server may not be running")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_complete_evaluation():
    """測試完整的評估流程包含 AIPET"""
    try:
        # 準備測試數據
        evaluation_data = {
            "project_info": {"name": "AIPET Test Project"},
            "kano_responses": {
                "response_accuracy": {"functional": "like", "dysfunctional": "dislike"}
            },
            "sus_responses": {f"q{i}": 3 for i in range(1, 11)},  # 中性回答（整數格式）
            "aipet_responses": {}
        }
        
        response = requests.post(
            "http://localhost:5000/api/evaluate",
            json=evaluation_data,
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("✅ Complete evaluation with AIPET working")
                
                # 檢查 AIPET 結果
                aipet_eval = result.get('data', {}).get('aipet_evaluation')
                if aipet_eval:
                    analysis = aipet_eval['analysis']
                    print(f"📊 AIPET Analysis:")
                    print(f"   Completion Rate: {analysis['completion_rate']:.1f}%")
                    print(f"   Questions Answered: {analysis['answered_questions']}/{analysis['total_questions']}")
                    
                    # 顯示維度覆蓋
                    print(f"\n📈 Dimension Coverage:")
                    for dim, data in analysis['dimension_coverage'].items():
                        print(f"   {dim}: {data['percentage']:.0f}% ({data['answered']}/{data['total']})")
                    
                    # 顯示見解
                    insights = analysis.get('insights', [])
                    if insights:
                        print(f"\n💡 Insights ({len(insights)}):")
                        for insight in insights[:2]:
                            print(f"   • {insight['title']}: {insight['description'][:60]}...")
                else:
                    print("⚠️  No AIPET evaluation found in results")
                
                return True
            else:
                print(f"❌ Evaluation failed: {result.get('error')}")
                return False
        else:
            print(f"❌ HTTP Error {response.status_code}: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Evaluation test error: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing AIPET Questions Integration\n")
    
    # 測試 API 端點
    api_ok = test_aipet_api()
    
    if api_ok:
        print("\n" + "="*50)
        # 測試完整評估
        eval_ok = test_complete_evaluation()
        
        if eval_ok:
            print(f"\n🎉 All AIPET integration tests passed!")
            print(f"🌐 Access system: https://5000-i6tx75dds1e1esv6i13dp.e2b.dev/")
        else:
            print(f"\n⚠️  AIPET API works but evaluation integration needs fixing")
    else:
        print(f"\n❌ AIPET API endpoint not working")