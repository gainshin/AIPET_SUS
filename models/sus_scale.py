"""
SUS量表(System Usability Scale)評估模組
實現標準化的可用性評估問卷和分析功能
"""

import numpy as np
import pandas as pd
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

class SUSGrade(Enum):
    """SUS評級"""
    A = "A"  # 90-100分：優秀
    B = "B"  # 80-89分：良好
    C = "C"  # 70-79分：中等
    D = "D"  # 60-69分：較差
    F = "F"  # 0-59分：極差

@dataclass
class SUSResult:
    """SUS評估結果"""
    score: float  # SUS分數 (0-100)
    grade: SUSGrade  # 評級
    percentile: float  # 百分位數
    adjective_rating: str  # 形容詞評級
    acceptability: str  # 可接受性

class SUSEvaluator:
    """SUS量表評估器"""
    
    def __init__(self):
        # SUS標準問題（繁體中文版）
        self.questions = [
            {
                "id": "q1",
                "text": "我想要經常使用這個AI Agent系統",
                "positive": True
            },
            {
                "id": "q2", 
                "text": "我覺得這個系統過於複雜",
                "positive": False
            },
            {
                "id": "q3",
                "text": "我覺得這個系統很容易使用",
                "positive": True
            },
            {
                "id": "q4",
                "text": "我需要技術人員的協助才能使用這個系統",
                "positive": False
            },
            {
                "id": "q5",
                "text": "我覺得這個系統的各項功能整合得很好",
                "positive": True
            },
            {
                "id": "q6",
                "text": "我覺得這個系統有太多不一致的地方",
                "positive": False
            },
            {
                "id": "q7",
                "text": "我想大部分的人能很快學會使用這個系統",
                "positive": True
            },
            {
                "id": "q8",
                "text": "我覺得這個系統很難使用",
                "positive": False
            },
            {
                "id": "q9",
                "text": "我對使用這個系統感到很有信心",
                "positive": True
            },
            {
                "id": "q10",
                "text": "在使用這個系統之前，我需要先學習很多東西",
                "positive": False
            }
        ]
        
        # Likert量表選項
        self.likert_options = {
            1: "強烈不同意",
            2: "不同意", 
            3: "普通",
            4: "同意",
            5: "強烈同意"
        }
        
        # 行業基準數據 (基於大量SUS研究)
        self.benchmarks = {
            "average": 68.0,
            "std": 12.5,
            "percentiles": {
                10: 51.7,
                25: 62.7,
                50: 72.6,
                75: 78.9,
                90: 85.5,
                95: 91.0
            }
        }
        
        # 形容詞評級映射
        self.adjective_ratings = [
            (0, 25, "極差"),
            (25, 39, "很差"),
            (39, 52, "差"),
            (52, 72, "尚可"),
            (72, 85, "好"),
            (85, 92, "優秀"),
            (92, 100, "最佳")
        ]
        
        # 可接受性等級
        self.acceptability_levels = [
            (0, 51, "不可接受"),
            (51, 71, "邊際可接受"),
            (71, 100, "可接受")
        ]
    
    def get_questions(self) -> List[Dict]:
        """獲取SUS問卷問題"""
        return self.questions
    
    def calculate_sus_score(self, responses: Dict[str, int]) -> float:
        """
        計算SUS分數
        
        Args:
            responses: {question_id: likert_response (1-5)}
            
        Returns:
            SUS分數 (0-100)
        """
        if len(responses) != 10:
            raise ValueError("SUS問卷必須包含所有10個問題的回答")
        
        total_score = 0
        
        for i, question in enumerate(self.questions, 1):
            question_id = f"q{i}"
            if question_id not in responses:
                raise ValueError(f"缺少問題 {question_id} 的回答")
            
            response = responses[question_id]
            if not 1 <= response <= 5:
                raise ValueError(f"回答必須在1-5之間，問題 {question_id} 的回答是 {response}")
            
            # 計算分數貢獻
            if question["positive"]:
                # 正向問題：分數 = 回答 - 1
                score_contribution = response - 1
            else:
                # 負向問題：分數 = 5 - 回答
                score_contribution = 5 - response
            
            total_score += score_contribution
        
        # SUS分數 = 總分 * 2.5
        sus_score = total_score * 2.5
        return min(100, max(0, sus_score))  # 確保分數在0-100範圍內
    
    def get_grade(self, score: float) -> SUSGrade:
        """根據分數獲取評級"""
        if score >= 90:
            return SUSGrade.A
        elif score >= 80:
            return SUSGrade.B
        elif score >= 70:
            return SUSGrade.C
        elif score >= 60:
            return SUSGrade.D
        else:
            return SUSGrade.F
    
    def get_percentile(self, score: float) -> float:
        """計算分數的百分位數"""
        # 使用正態分佈近似
        z_score = (score - self.benchmarks["average"]) / self.benchmarks["std"]
        # 轉換為百分位數
        from scipy.stats import norm
        try:
            percentile = norm.cdf(z_score) * 100
        except ImportError:
            # 如果沒有scipy，使用簡化計算
            if score <= self.benchmarks["percentiles"][10]:
                percentile = 10
            elif score <= self.benchmarks["percentiles"][25]:
                percentile = 25
            elif score <= self.benchmarks["percentiles"][50]:
                percentile = 50
            elif score <= self.benchmarks["percentiles"][75]:
                percentile = 75
            elif score <= self.benchmarks["percentiles"][90]:
                percentile = 90
            else:
                percentile = 95
        
        return min(100, max(0, percentile))
    
    def get_adjective_rating(self, score: float) -> str:
        """獲取形容詞評級"""
        for min_score, max_score, rating in self.adjective_ratings:
            if min_score <= score < max_score:
                return rating
        return self.adjective_ratings[-1][2]  # 返回最高評級
    
    def get_acceptability(self, score: float) -> str:
        """獲取可接受性等級"""
        for min_score, max_score, level in self.acceptability_levels:
            if min_score <= score < max_score:
                return level
        return self.acceptability_levels[-1][2]  # 返回最高等級
    
    def evaluate(self, responses: Dict[str, int]) -> SUSResult:
        """
        完整的SUS評估
        
        Args:
            responses: {question_id: likert_response (1-5)}
            
        Returns:
            SUSResult對象
        """
        score = self.calculate_sus_score(responses)
        grade = self.get_grade(score)
        percentile = self.get_percentile(score)
        adjective_rating = self.get_adjective_rating(score)
        acceptability = self.get_acceptability(score)
        
        return SUSResult(
            score=score,
            grade=grade,
            percentile=percentile,
            adjective_rating=adjective_rating,
            acceptability=acceptability
        )
    
    def analyze_individual_questions(self, responses: Dict[str, int]) -> Dict[str, Dict]:
        """分析個別問題的表現"""
        analysis = {}
        
        for i, question in enumerate(self.questions, 1):
            question_id = f"q{i}"
            if question_id in responses:
                response = responses[question_id]
                
                # 標準化分數 (0-4)
                if question["positive"]:
                    normalized_score = response - 1
                else:
                    normalized_score = 5 - response
                
                # 表現評估
                if normalized_score >= 3:
                    performance = "優秀"
                elif normalized_score >= 2:
                    performance = "良好"
                elif normalized_score >= 1:
                    performance = "普通"
                else:
                    performance = "需要改進"
                
                analysis[question_id] = {
                    "question": question["text"],
                    "response": response,
                    "normalized_score": normalized_score,
                    "performance": performance,
                    "is_positive": question["positive"]
                }
        
        return analysis
    
    def generate_improvement_suggestions(self, responses: Dict[str, int]) -> List[Dict]:
        """生成改進建議"""
        suggestions = []
        analysis = self.analyze_individual_questions(responses)
        
        # 找出表現不佳的問題
        poor_performers = []
        for question_id, data in analysis.items():
            if data["normalized_score"] <= 1:
                poor_performers.append((question_id, data))
        
        # 根據問題類型生成建議
        suggestion_mapping = {
            "q1": {
                "area": "用戶參與度",
                "suggestion": "提升AI Agent的實用性和價值，讓用戶更願意經常使用"
            },
            "q2": {
                "area": "系統複雜性",
                "suggestion": "簡化用戶界面和交互流程，降低系統複雜度"
            },
            "q3": {
                "area": "易用性",
                "suggestion": "改善用戶體驗設計，提供更直觀的操作方式"
            },
            "q4": {
                "area": "獨立使用性",
                "suggestion": "完善幫助文檔和引導功能，降低技術門檻"
            },
            "q5": {
                "area": "功能整合",
                "suggestion": "優化功能間的連接和協調，提供更統一的體驗"
            },
            "q6": {
                "area": "一致性",
                "suggestion": "建立清晰的設計規範，確保界面和交互的一致性"
            },
            "q7": {
                "area": "學習曲線",
                "suggestion": "優化新手引導流程，提供更好的學習體驗"
            },
            "q8": {
                "area": "使用難度",
                "suggestion": "重新設計複雜的功能，提供更簡單的替代方案"
            },
            "q9": {
                "area": "用戶信心",
                "suggestion": "增加反饋機制和錯誤預防，提升用戶使用信心"
            },
            "q10": {
                "area": "學習成本",
                "suggestion": "減少預備知識要求，提供更好的上手體驗"
            }
        }
        
        for question_id, data in poor_performers:
            if question_id in suggestion_mapping:
                suggestion_info = suggestion_mapping[question_id]
                suggestions.append({
                    "priority": "高" if data["normalized_score"] == 0 else "中",
                    "area": suggestion_info["area"],
                    "current_score": data["normalized_score"],
                    "suggestion": suggestion_info["suggestion"],
                    "question": data["question"]
                })
        
        return suggestions
    
    def compare_with_benchmarks(self, score: float) -> Dict:
        """與行業基準比較"""
        percentile = self.get_percentile(score)
        
        comparison = {
            "your_score": score,
            "industry_average": self.benchmarks["average"],
            "difference_from_average": score - self.benchmarks["average"],
            "percentile": percentile,
            "better_than_percent": percentile,
            "benchmark_category": ""
        }
        
        if percentile >= 90:
            comparison["benchmark_category"] = "頂尖 (前10%)"
        elif percentile >= 75:
            comparison["benchmark_category"] = "優秀 (前25%)"
        elif percentile >= 50:
            comparison["benchmark_category"] = "中上 (前50%)"
        elif percentile >= 25:
            comparison["benchmark_category"] = "中等 (前75%)"
        else:
            comparison["benchmark_category"] = "需要改進 (後25%)"
        
        return comparison
    
    def generate_detailed_report(self, responses: Dict[str, int]) -> Dict:
        """生成詳細報告"""
        result = self.evaluate(responses)
        question_analysis = self.analyze_individual_questions(responses)
        suggestions = self.generate_improvement_suggestions(responses)
        benchmark_comparison = self.compare_with_benchmarks(result.score)
        
        return {
            "overall_result": {
                "score": result.score,
                "grade": result.grade.value,
                "percentile": result.percentile,
                "adjective_rating": result.adjective_rating,
                "acceptability": result.acceptability
            },
            "question_analysis": question_analysis,
            "improvement_suggestions": suggestions,
            "benchmark_comparison": benchmark_comparison,
            "strengths": self._identify_strengths(question_analysis),
            "weaknesses": self._identify_weaknesses(question_analysis)
        }
    
    def _identify_strengths(self, analysis: Dict) -> List[str]:
        """識別強項"""
        strengths = []
        for question_id, data in analysis.items():
            if data["normalized_score"] >= 3:
                area_map = {
                    "q1": "用戶參與度高",
                    "q2": "系統複雜度適中",
                    "q3": "容易使用",
                    "q4": "獨立使用性佳",
                    "q5": "功能整合良好",
                    "q6": "系統一致性佳",
                    "q7": "容易學習",
                    "q8": "使用簡單",
                    "q9": "用戶信心足",
                    "q10": "學習成本低"
                }
                if question_id in area_map:
                    strengths.append(area_map[question_id])
        return strengths
    
    def _identify_weaknesses(self, analysis: Dict) -> List[str]:
        """識別弱項"""
        weaknesses = []
        for question_id, data in analysis.items():
            if data["normalized_score"] <= 1:
                area_map = {
                    "q1": "用戶參與度不足",
                    "q2": "系統過於複雜",
                    "q3": "使用困難",
                    "q4": "需要技術支援",
                    "q5": "功能整合不佳",
                    "q6": "系統不一致",
                    "q7": "學習困難",
                    "q8": "使用複雜",
                    "q9": "用戶缺乏信心",
                    "q10": "學習成本高"
                }
                if question_id in area_map:
                    weaknesses.append(area_map[question_id])
        return weaknesses