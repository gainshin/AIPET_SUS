#!/usr/bin/env python3
"""
測試 Kano Matrix 可視化的腳本
"""
import requests
import json

# API 基礎 URL
API_BASE = "http://localhost:5000/api"

# 測試項目信息
project_info = {
    "name": "AI Assistant Demo",
    "description": "測試用 AI 助手系統",
    "version": "1.0.0",
    "team": "測試團隊"
}

# 模擬 Kano 回答
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
    "integration": {"functional": 1, "dysfunctional": 3}
}

# 模擬 SUS 回答
sus_responses = {
    "q1": 4, "q2": 2, "q3": 4, "q4": 2, "q5": 4,
    "q6": 2, "q7": 4, "q8": 2, "q9": 4, "q10": 2
}

def test_evaluation():
    print("開始測試 Kano Matrix 可視化...")
    
    # 準備評估數據
    evaluation_data = {
        "project_info": project_info,
        "kano_responses": kano_responses,
        "sus_responses": sus_responses
    }
    
    try:
        # 發送評估請求
        response = requests.post(f"{API_BASE}/evaluate", 
                               json=evaluation_data,
                               headers={'Content-Type': 'application/json'})
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                evaluation_id = result['data']['evaluation_id']
                print(f"✅ 評估成功創建！ID: {evaluation_id}")
                print(f"🌐 請訪問：http://localhost:5000?eval={evaluation_id}")
                print(f"📊 您可以看到新的 Kano Matrix 散點圖可視化")
                
                # 打印 Kano 分析結果
                kano_eval = result['data']['kano_evaluation']
                print(f"\n📈 Kano 分析結果:")
                for category, percentage in kano_eval['summary']['category_percentages'].items():
                    if percentage > 0:
                        print(f"  {category}: {percentage:.1f}%")
                        
            else:
                print(f"❌ 評估失敗: {result.get('error')}")
        else:
            print(f"❌ HTTP 錯誤: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ 無法連接到服務器，請確保服務正在運行")
    except Exception as e:
        print(f"❌ 發生錯誤: {e}")

if __name__ == "__main__":
    test_evaluation()