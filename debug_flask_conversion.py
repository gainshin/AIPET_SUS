#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Debug Flask Type Conversion
調試 Flask 類型轉換
"""

import json

def simulate_flask_conversion():
    """模擬 Flask 中的類型轉換邏輯"""
    
    # 模擬來自前端的原始數據
    sus_responses_raw = {f"q{i}": "3" for i in range(1, 11)}
    
    print("🔍 Simulating Flask app.py type conversion logic...")
    print(f"Original data: {list(sus_responses_raw.items())[:3]}...")
    
    # 執行類型轉換（模擬 app.py 中的邏輯）
    sus_responses = {}
    for key, value in sus_responses_raw.items():
        try:
            sus_responses[key] = int(value)
            print(f"✅ Converted {key}: '{value}' → {sus_responses[key]} ({type(sus_responses[key])})")
        except (ValueError, TypeError):
            print(f"❌ Conversion failed for {key}: {value}")
            return False
    
    print(f"\n📊 Converted data types: {[(k, type(v), v) for k, v in list(sus_responses.items())[:3]]}...")
    
    # 測試轉換後的數據是否工作
    try:
        from models.sus_scale import SUSEvaluator
        sus_evaluator = SUSEvaluator()
        
        print(f"\n🔍 Testing converted data with SUS evaluator...")
        result = sus_evaluator.evaluate(sus_responses)
        print(f"✅ SUS evaluation successful: {result.score}")
        
        detailed = sus_evaluator.generate_detailed_report(sus_responses)
        print(f"✅ Detailed report successful")
        
        return True
        
    except Exception as e:
        print(f"❌ Error with converted data: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Debugging Flask Type Conversion\n")
    
    success = simulate_flask_conversion()
    
    if success:
        print(f"\n🎉 Type conversion logic is working correctly!")
        print(f"💡 The error might be elsewhere in the Flask request handling.")
    else:
        print(f"\n❌ Type conversion logic needs fixing.")