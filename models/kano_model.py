"""
Kano Model Evaluation Module
Implements Kano model questionnaire design, data analysis and result classification
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

class KanoCategory(Enum):
    """Kano Model Categories"""
    MUST_BE = "Must-be"  # Basic needs
    ONE_DIMENSIONAL = "One-dimensional"  # Performance needs
    ATTRACTIVE = "Attractive"  # Excitement needs
    INDIFFERENT = "Indifferent"  # Indifferent needs
    REVERSE = "Reverse"  # Reverse needs
    QUESTIONABLE = "Questionable"  # Questionable needs

@dataclass
class KanoResult:
    """Kano Evaluation Result"""
    category: KanoCategory
    satisfaction_impact: float  # Satisfaction impact coefficient
    dissatisfaction_impact: float  # Dissatisfaction impact coefficient
    better_coefficient: float  # Better coefficient
    worse_coefficient: float  # Worse coefficient

class KanoModelEvaluator:
    """Kano Model Evaluator"""
    
    def __init__(self):
        # Kano classification decision table
        self.kano_table = {
            # (functional answer, dysfunctional answer) -> category
            (1, 1): KanoCategory.QUESTIONABLE,  # 喜歡-喜歡
            (1, 2): KanoCategory.ATTRACTIVE,    # 喜歡-理所當然
            (1, 3): KanoCategory.ATTRACTIVE,    # 喜歡-無所謂
            (1, 4): KanoCategory.ATTRACTIVE,    # 喜歡-勉強接受
            (1, 5): KanoCategory.ONE_DIMENSIONAL, # 喜歡-不喜歡
            
            (2, 1): KanoCategory.REVERSE,       # 理所當然-喜歡
            (2, 2): KanoCategory.INDIFFERENT,   # 理所當然-理所當然
            (2, 3): KanoCategory.INDIFFERENT,   # 理所當然-無所謂
            (2, 4): KanoCategory.INDIFFERENT,   # 理所當然-勉強接受
            (2, 5): KanoCategory.MUST_BE,       # 理所當然-不喜歡
            
            (3, 1): KanoCategory.REVERSE,       # 無所謂-喜歡
            (3, 2): KanoCategory.INDIFFERENT,   # 無所謂-理所當然
            (3, 3): KanoCategory.INDIFFERENT,   # 無所謂-無所謂
            (3, 4): KanoCategory.INDIFFERENT,   # 無所謂-勉強接受
            (3, 5): KanoCategory.MUST_BE,       # 無所謂-不喜歡
            
            (4, 1): KanoCategory.REVERSE,       # 勉強接受-喜歡
            (4, 2): KanoCategory.INDIFFERENT,   # 勉強接受-理所當然
            (4, 3): KanoCategory.INDIFFERENT,   # 勉強接受-無所謂
            (4, 4): KanoCategory.INDIFFERENT,   # 勉強接受-勉強接受
            (4, 5): KanoCategory.MUST_BE,       # 勉強接受-不喜歡
            
            (5, 1): KanoCategory.REVERSE,       # 不喜歡-喜歡
            (5, 2): KanoCategory.REVERSE,       # 不喜歡-理所當然
            (5, 3): KanoCategory.REVERSE,       # 不喜歡-無所謂
            (5, 4): KanoCategory.REVERSE,       # 不喜歡-勉強接受
            (5, 5): KanoCategory.QUESTIONABLE,  # 不喜歡-不喜歡
        }
        
        # 答案選項映射
        self.answer_mapping = {
            1: "I like it that way",
            2: "It must be that way", 
            3: "I am neutral",
            4: "I can live with it that way",
            5: "I dislike it that way"
        }
    
    def get_default_questions(self) -> List[Dict]:
        """Get default AI Agent evaluation questions"""
        return [
            {
                "id": "response_accuracy",
                "title": "回應準確性",
                "functional": "如果AI Agent總是能準確理解您的問題並給出正確答案，您的感受如何？",
                "dysfunctional": "如果AI Agent經常誤解您的問題或給出錯誤答案，您的感受如何？"
            },
            {
                "id": "response_speed",
                "title": "回應速度",
                "functional": "如果AI Agent能在1秒內回應您的問題，您的感受如何？",
                "dysfunctional": "如果AI Agent需要超過10秒才能回應您的問題，您的感受如何？"
            },
            {
                "id": "natural_conversation",
                "title": "自然對話",
                "functional": "如果AI Agent能像人類一樣進行自然流暢的對話，您的感受如何？",
                "dysfunctional": "如果AI Agent的回應生硬且不自然，您的感受如何？"
            },
            {
                "id": "context_memory",
                "title": "上下文記憶",
                "functional": "如果AI Agent能記住整個對話歷史並保持上下文連貫，您的感受如何？",
                "dysfunctional": "如果AI Agent無法記住之前的對話內容，每次都要重新解釋，您的感受如何？"
            },
            {
                "id": "personalization",
                "title": "個人化服務",
                "functional": "如果AI Agent能根據您的偏好和歷史記錄提供個人化服務，您的感受如何？",
                "dysfunctional": "如果AI Agent無法提供任何個人化服務，對所有人都是相同回應，您的感受如何？"
            },
            {
                "id": "multi_modal",
                "title": "多模態互動",
                "functional": "如果AI Agent能處理文字、圖片、語音等多種輸入方式，您的感受如何？",
                "dysfunctional": "如果AI Agent只能處理純文字輸入，您的感受如何？"
            },
            {
                "id": "error_handling",
                "title": "錯誤處理",
                "functional": "如果AI Agent在出錯時能主動道歉並提供解決方案，您的感受如何？",
                "dysfunctional": "如果AI Agent出錯時不承認錯誤，繼續堅持錯誤回答，您的感受如何？"
            },
            {
                "id": "learning_ability",
                "title": "學習能力",
                "functional": "如果AI Agent能從與您的互動中學習並逐漸改善服務品質，您的感受如何？",
                "dysfunctional": "如果AI Agent完全無法學習改進，重複犯同樣的錯誤，您的感受如何？"
            },
            {
                "id": "emotional_intelligence",
                "title": "情感智慧",
                "functional": "如果AI Agent能理解您的情感並給予適當的情感回應，您的感受如何？",
                "dysfunctional": "如果AI Agent完全無法理解情感，對情緒化的問題給出冷漠回應，您的感受如何？"
            },
            {
                "id": "privacy_protection",
                "title": "隱私保護",
                "functional": "如果AI Agent能嚴格保護您的隱私資訊並透明說明數據使用方式，您的感受如何？",
                "dysfunctional": "如果AI Agent可能洩露您的隱私資訊且不說明數據如何使用，您的感受如何？"
            }
        ]
    
    def classify_single_response(self, functional_answer: int, dysfunctional_answer: int) -> KanoCategory:
        """分類單個問題的回應"""
        return self.kano_table.get((functional_answer, dysfunctional_answer), KanoCategory.QUESTIONABLE)
    
    def analyze_responses(self, responses: Dict[str, Dict]) -> Dict[str, KanoResult]:
        """
        分析Kano問卷回應
        
        Args:
            responses: {question_id: {functional: int, dysfunctional: int}}
            
        Returns:
            Dict[question_id, KanoResult]
        """
        results = {}
        
        for question_id, answer in responses.items():
            functional = answer['functional']
            dysfunctional = answer['dysfunctional']
            
            category = self.classify_single_response(functional, dysfunctional)
            
            # 計算Better和Worse係數
            better_coeff = self._calculate_better_coefficient(functional, dysfunctional)
            worse_coeff = self._calculate_worse_coefficient(functional, dysfunctional)
            
            # 計算滿意度影響係數
            satisfaction_impact = self._calculate_satisfaction_impact(category, better_coeff)
            dissatisfaction_impact = self._calculate_dissatisfaction_impact(category, worse_coeff)
            
            results[question_id] = KanoResult(
                category=category,
                satisfaction_impact=satisfaction_impact,
                dissatisfaction_impact=dissatisfaction_impact,
                better_coefficient=better_coeff,
                worse_coefficient=worse_coeff
            )
        
        return results
    
    def _calculate_better_coefficient(self, functional: int, dysfunctional: int) -> float:
        """計算Better係數（滿意度提升係數）"""
        if functional <= 2:  # 喜歡或理所當然
            return 1.0
        elif functional == 3:  # 無所謂
            return 0.5
        else:  # 勉強接受或不喜歡
            return 0.0
    
    def _calculate_worse_coefficient(self, functional: int, dysfunctional: int) -> float:
        """計算Worse係數（不滿意度降低係數）"""
        if dysfunctional >= 4:  # 勉強接受或不喜歡
            return 1.0
        elif dysfunctional == 3:  # 無所謂
            return 0.5
        else:  # 喜歡或理所當然
            return 0.0
    
    def _calculate_satisfaction_impact(self, category: KanoCategory, better_coeff: float) -> float:
        """計算滿意度影響係數"""
        multipliers = {
            KanoCategory.ATTRACTIVE: 1.0,
            KanoCategory.ONE_DIMENSIONAL: 0.8,
            KanoCategory.MUST_BE: 0.2,
            KanoCategory.INDIFFERENT: 0.0,
            KanoCategory.REVERSE: -0.5,
            KanoCategory.QUESTIONABLE: 0.0
        }
        return multipliers.get(category, 0.0) * better_coeff
    
    def _calculate_dissatisfaction_impact(self, category: KanoCategory, worse_coeff: float) -> float:
        """計算不滿意度影響係數"""
        multipliers = {
            KanoCategory.MUST_BE: 1.0,
            KanoCategory.ONE_DIMENSIONAL: 0.8,
            KanoCategory.ATTRACTIVE: 0.2,
            KanoCategory.INDIFFERENT: 0.0,
            KanoCategory.REVERSE: -0.5,
            KanoCategory.QUESTIONABLE: 0.0
        }
        return multipliers.get(category, 0.0) * worse_coeff
    
    def generate_summary_statistics(self, results: Dict[str, KanoResult]) -> Dict:
        """生成統計摘要"""
        categories = [result.category for result in results.values()]
        category_counts = {}
        
        for category in KanoCategory:
            category_counts[category.value] = categories.count(category)
        
        total_questions = len(results)
        category_percentages = {
            cat: (count / total_questions * 100) if total_questions > 0 else 0
            for cat, count in category_counts.items()
        }
        
        avg_satisfaction = np.mean([r.satisfaction_impact for r in results.values()])
        avg_dissatisfaction = np.mean([r.dissatisfaction_impact for r in results.values()])
        
        return {
            "category_counts": category_counts,
            "category_percentages": category_percentages,
            "total_questions": total_questions,
            "average_satisfaction_impact": avg_satisfaction,
            "average_dissatisfaction_impact": avg_dissatisfaction,
            "priority_features": self._identify_priority_features(results)
        }
    
    def _identify_priority_features(self, results: Dict[str, KanoResult]) -> Dict[str, List[str]]:
        """識別優先級特性"""
        must_be = []
        attractive = []
        one_dimensional = []
        
        for question_id, result in results.items():
            if result.category == KanoCategory.MUST_BE:
                must_be.append(question_id)
            elif result.category == KanoCategory.ATTRACTIVE:
                attractive.append(question_id)
            elif result.category == KanoCategory.ONE_DIMENSIONAL:
                one_dimensional.append(question_id)
        
        # 按影響係數排序
        must_be.sort(key=lambda x: results[x].dissatisfaction_impact, reverse=True)
        attractive.sort(key=lambda x: results[x].satisfaction_impact, reverse=True)
        one_dimensional.sort(key=lambda x: results[x].satisfaction_impact + results[x].dissatisfaction_impact, reverse=True)
        
        return {
            "must_be_features": must_be[:3],  # Top 3 most important must-be needs
            "attractive_features": attractive[:3],  # Top 3 most important attractive needs
            "one_dimensional_features": one_dimensional[:3]  # Top 3 most important one-dimensional needs
        }
    
    def generate_improvement_recommendations(self, results: Dict[str, KanoResult], questions: List[Dict]) -> List[Dict]:
        """Generate improvement recommendations"""
        recommendations = []
        questions_dict = {q["id"]: q for q in questions}
        
        # Must-be needs recommendations (must be satisfied first)
        must_be_features = [qid for qid, result in results.items() 
                           if result.category == KanoCategory.MUST_BE]
        if must_be_features:
            must_be_features.sort(key=lambda x: results[x].dissatisfaction_impact, reverse=True)
            top_must_be = must_be_features[0] if must_be_features else None
            if top_must_be:
                recommendations.append({
                    "priority": "High",
                    "category": "Must-be Needs",
                    "feature": questions_dict[top_must_be]["title"],
                    "description": f"Users consider {questions_dict[top_must_be]['title']} as a basic requirement, must prioritize ensuring its stability and reliability.",
                    "action": "Immediate improvement and ensure 100% reliability"
                })
        
        # One-dimensional needs recommendations (directly affect satisfaction)
        one_dim_features = [qid for qid, result in results.items() 
                           if result.category == KanoCategory.ONE_DIMENSIONAL]
        if one_dim_features:
            one_dim_features.sort(key=lambda x: results[x].satisfaction_impact, reverse=True)
            top_one_dim = one_dim_features[0] if one_dim_features else None
            if top_one_dim:
                recommendations.append({
                    "priority": "Medium",
                    "category": "One-dimensional Needs", 
                    "feature": questions_dict[top_one_dim]["title"],
                    "description": f"Improving {questions_dict[top_one_dim]['title']} directly enhances user satisfaction.",
                    "action": "Continuously optimize performance and user experience"
                })
        
        # Attractive needs recommendations (create delight)
        attractive_features = [qid for qid, result in results.items() 
                              if result.category == KanoCategory.ATTRACTIVE]
        if attractive_features:
            attractive_features.sort(key=lambda x: results[x].satisfaction_impact, reverse=True)
            top_attractive = attractive_features[0] if attractive_features else None
            if top_attractive:
                recommendations.append({
                    "priority": "Low",
                    "category": "Attractive Needs",
                    "feature": questions_dict[top_attractive]["title"],
                    "description": f"{questions_dict[top_attractive]['title']} is a feature that can create user delight.",
                    "action": "Invest in development when resources allow"
                })
        
        return recommendations