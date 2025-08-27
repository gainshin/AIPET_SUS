#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Basic Evaluation (without AIPET)
測試基礎評估（不包含 AIPET）
"""

import requests
import json

def test_basic_evaluation():
    """測試基礎評估 API"""
    try:
        # 只包含基本的 Kano 和 SUS 數據
        evaluation_data = {
            "project_info": {"name": "Basic Test Project"},
            "kano_responses": {
                "response_accuracy": {"functional": "like", "dysfunctional": "dislike"}
            },
            "sus_responses": {f"q{i}": 3 for i in range(1, 11)}  # 整數格式
        }
        
        print("🧪 Testing basic evaluation (Kano + SUS only)...")
        print(f"📊 SUS data types: {[(k, type(v)) for k, v in list(evaluation_data['sus_responses'].items())[:3]]}...")
        
        response = requests.post(
            "http://localhost:5000/api/evaluate",
            json=evaluation_data,
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("✅ Basic evaluation successful")
                
                # 檢查基本結果
                data = result['data']
                sus_eval = data.get('sus_evaluation')
                if sus_eval:
                    print(f"📊 SUS Score: {sus_eval['score']}")
                    print(f"📊 SUS Grade: {sus_eval['grade']}")
                
                kano_eval = data.get('kano_evaluation')
                if kano_eval:
                    print(f"📊 Kano Categories: {len(kano_eval['results'])} analyzed")
                
                return True
            else:
                print(f"❌ Evaluation failed: {result.get('error')}")
                return False
        else:
            print(f"❌ HTTP Error {response.status_code}: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Basic evaluation error: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing Basic Evaluation API\n")
    
    success = test_basic_evaluation()
    
    if success:
        print(f"\n🎉 Basic evaluation works! The error is likely in AIPET integration.")
    else:
        print(f"\n❌ Basic evaluation fails - need to fix core evaluation logic.")