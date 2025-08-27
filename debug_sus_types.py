#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Debug SUS Type Issues
調試SUS類型問題
"""

from models.sus_scale import SUSEvaluator

def debug_sus_evaluation():
    """調試SUS評估中的類型問題"""
    sus_evaluator = SUSEvaluator()
    
    # 測試數據，確保都是整數
    test_responses = {
        "q1": 2,  
        "q2": 4,  
        "q3": 2,  
        "q4": 1,  
        "q5": 3,  
        "q6": 2,  
        "q7": 1,  
        "q8": 4,  
        "q9": 2,  
        "q10": 1   
    }
    
    print("🔍 Testing SUS evaluation with integer responses...")
    print(f"Test data types: {[(k, type(v), v) for k, v in test_responses.items()]}")
    
    try:
        result = sus_evaluator.evaluate(test_responses)
        print(f"✅ SUS evaluation successful! Score: {result.score}")
        
        # 測試詳細報告
        detailed = sus_evaluator.generate_detailed_report(test_responses)
        print(f"✅ Detailed report generated")
        
        # 檢查改善建議
        if 'improvement_recommendations' in detailed:
            recommendations = detailed['improvement_recommendations']
            print(f"✅ Found {len(recommendations)} improvement recommendations")
            
            for i, rec in enumerate(recommendations[:2], 1):
                print(f"\n   {i}. {rec.get('area', 'N/A')}")
                print(f"      AIPET: {rec.get('aipet_dimension', 'N/A')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error in SUS evaluation: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    debug_sus_evaluation()