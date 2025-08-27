#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Debug SUS Detailed Report Generation
調試SUS詳細報告生成
"""

from models.sus_scale import SUSEvaluator

def debug_sus_detailed():
    """調試SUS詳細報告生成"""
    sus_evaluator = SUSEvaluator()
    
    # 測試數據 - 都是整數
    test_responses = {
        "q1": 3,  
        "q2": 3,  
        "q3": 3,  
        "q4": 3,  
        "q5": 3,  
        "q6": 3,  
        "q7": 3,  
        "q8": 3,  
        "q9": 3,  
        "q10": 3   
    }
    
    print("🔍 Testing SUS detailed report generation...")
    print(f"Test data types: {[(k, type(v), v) for k, v in test_responses.items()]}")
    
    try:
        # 測試基本評估
        result = sus_evaluator.evaluate(test_responses)
        print(f"✅ Basic evaluation successful! Score: {result.score}")
        
        # 測試個別問題分析
        print("🔍 Testing analyze_individual_questions...")
        analysis = sus_evaluator.analyze_individual_questions(test_responses)
        print(f"✅ Individual analysis successful! {len(analysis)} questions analyzed")
        
        # 測試改善建議
        print("🔍 Testing generate_improvement_suggestions...")
        suggestions = sus_evaluator.generate_improvement_suggestions(test_responses)
        print(f"✅ Improvement suggestions successful! {len(suggestions)} suggestions")
        
        # 測試詳細報告
        print("🔍 Testing generate_detailed_report...")
        detailed = sus_evaluator.generate_detailed_report(test_responses)
        print(f"✅ Detailed report successful!")
        
        # 檢查報告內容
        if 'improvement_suggestions' in detailed:
            print(f"📊 Report includes {len(detailed['improvement_suggestions'])} suggestions")
        
        return True
        
    except Exception as e:
        print(f"❌ Error in SUS detailed report: {e}")
        import traceback
        traceback.print_exc()
        return False

def debug_type_error():
    """嘗試重現類型錯誤"""
    sus_evaluator = SUSEvaluator()
    
    # 嘗試使用字符串響應
    string_responses = {f"q{i}": "3" for i in range(1, 11)}
    
    print("\n🔍 Testing with string responses (should cause type error)...")
    try:
        detailed = sus_evaluator.generate_detailed_report(string_responses)
        print("⚠️  No error with string responses - conversion working?")
        return False
    except Exception as e:
        print(f"❌ Expected error with strings: {e}")
        return True

if __name__ == "__main__":
    print("🧪 Debugging SUS Detailed Report Generation\n")
    
    # 測試整數響應
    int_ok = debug_sus_detailed()
    
    # 測試字符串響應
    string_error = debug_type_error()
    
    if int_ok:
        print(f"\n✅ SUS detailed report works with integers")
    else:
        print(f"\n❌ SUS detailed report fails with integers")
    
    if string_error:
        print(f"✅ String responses properly cause type error as expected")
    else:
        print(f"⚠️  String responses don't cause expected error")