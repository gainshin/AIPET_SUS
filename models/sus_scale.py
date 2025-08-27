"""
SUS量表(System Usability Scale)評估模組 - 基於AIPET框架
實現標準化的可用性評估問卷和分析功能

改善建議基於AIPET代理式使用者體驗(Agentive UX)理論框架：
- A (Agency): 代理能力 - 定義AI代理人的能力邊界與自主性  
- I (Interaction): 互動模式 - 設計從手動到自動的光譜式控制體驗
- P (Privacy): 隱私增強 - 將隱私控制權內建於互動中
- E (Experience): 體驗連續性 - 確保跨設備、跨時間的無縫體驗  
- T (Trust): 信任建立 - 透過可恢復性與透明度建立深度信任

參考: improvement_recommendations_aipet_principles.py
"""

import numpy as np
import pandas as pd
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

class SUSGrade(Enum):
    """SUS評級"""
    A = "A"  # 90-100 points: Excellent
    B = "B"  # 80-89 points: Good
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
    acceptability: str  # Acceptability level

class SUSEvaluator:
    """SUS量表評估器"""
    
    def __init__(self):
        # SUS Standard Questions (English Version)
        self.questions = [
            {
                "id": "q1",
                "text": "I think that I would like to use this AI Agent system frequently",
                "positive": True
            },
            {
                "id": "q2", 
                "text": "I found the system unnecessarily complex",
                "positive": False
            },
            {
                "id": "q3",
                "text": "I thought the system was easy to use",
                "positive": True
            },
            {
                "id": "q4",
                "text": "I think that I would need the support of a technical person to be able to use this system",
                "positive": False
            },
            {
                "id": "q5",
                "text": "I found the various functions in this system were well integrated",
                "positive": True
            },
            {
                "id": "q6",
                "text": "I thought there was too much inconsistency in this system",
                "positive": False
            },
            {
                "id": "q7",
                "text": "I would imagine that most people would learn to use this system very quickly",
                "positive": True
            },
            {
                "id": "q8",
                "text": "I found the system very cumbersome to use",
                "positive": False
            },
            {
                "id": "q9",
                "text": "I felt very confident using the system",
                "positive": True
            },
            {
                "id": "q10",
                "text": "I needed to learn a lot of things before I could get going with this system",
                "positive": False
            }
        ]
        
        # Likert scale options
        self.likert_options = {
            1: "Strongly Disagree",
            2: "Disagree", 
            3: "Neutral",
            4: "Agree",
            5: "Strongly Agree"
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
        
        # Adjective rating mapping
        self.adjective_ratings = [
            (0, 25, "Awful"),
            (25, 39, "Poor"),
            (39, 52, "OK"),
            (52, 72, "Good"),
            (72, 85, "Excellent"),
            (85, 92, "Best Imaginable"),
            (92, 100, "Best Imaginable")
        ]
        
        # Acceptability levels
        self.acceptability_levels = [
            (0, 51, "Not Acceptable"),
            (51, 71, "Marginally Acceptable"),
            (71, 100, "Acceptable")
        ]
    
    def get_questions(self) -> List[Dict]:
        """Get SUS questionnaire questions"""
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
        """Get acceptability level"""
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
                
                # Performance assessment
                if normalized_score >= 3:
                    performance = "Excellent"
                elif normalized_score >= 2:
                    performance = "Good"
                elif normalized_score >= 1:
                    performance = "Average"
                else:
                    performance = "Needs Improvement"
                
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
        
        # 基於 AIPET 框架生成代理式使用者體驗改善建議
        # AIPET: Agency (代理能力), Interaction (互動模式), Privacy (隱私增強), Experience (體驗連續性), Trust (信任建立)
        suggestion_mapping = {
            "q1": {
                "area": "Agency - Agent Value Proposition",
                "aipet_dimension": "A - Agency (代理能力)",
                "suggestion": "Enhance AI Agent's autonomous capabilities and value delivery. Implement 'rules = behavior + triggers + exceptions' to define clear agent boundaries while enabling multi-modal interactions that provide genuine utility beyond traditional tools."
            },
            "q2": {
                "area": "Interaction - Complexity Reduction", 
                "aipet_dimension": "I - Interaction (互動模式)",
                "suggestion": "Implement spectrum control from 'fully manual' to 'fully automatic' like cruise control. Design guided intent declaration interfaces that replace open-ended prompts with structured components (buttons, forms, dropdowns) to reduce cognitive load."
            },
            "q3": {
                "area": "Interaction - Intuitive Collaboration",
                "aipet_dimension": "I - Interaction (互動模式)", 
                "suggestion": "Transition from 'chat interface' to 'contextual collaboration'. Design multi-modal, contextual interactions where AI acts directly on your workspace rather than through separate conversation windows."
            },
            "q4": {
                "area": "Trust - Transparent Autonomy",
                "aipet_dimension": "T - Trust (信任建立)",
                "suggestion": "Build trust through transparency and recoverability. Implement visible reasoning processes and one-click undo functionality. Ensure 'Human at the helm' principle with clear task logs and the ability to intervene at any step."
            },
            "q5": {
                "area": "Experience - Seamless Integration",
                "aipet_dimension": "E - Experience (體驗連續性)",
                "suggestion": "Create cross-device, cross-time memory for AI agents. Enable tasks started on mobile to continue seamlessly on laptop. Implement historical data reflection and dynamic contextual prompting for adaptive evolution."
            },
            "q6": {
                "area": "Experience - Consistency Across Modalities",
                "aipet_dimension": "E - Experience (體驗連續性)",
                "suggestion": "Ensure consistent experience across voice, visual, text, and touch interactions. Design for the continuous 'Sense-Think-Do' loop where AI maintains context and behavior consistency regardless of interaction mode."
            },
            "q7": {
                "area": "Interaction - Guided Learning",
                "aipet_dimension": "I - Interaction (互動模式)",
                "suggestion": "Replace static onboarding with dynamic learning mechanisms. Design hybrid UI that guides users to clearly 'declare' high-level goals through structured components rather than overwhelming them with open-ended possibilities."
            },
            "q8": {
                "area": "Agency - Capability Boundaries",
                "aipet_dimension": "A - Agency (代理能力)",
                "suggestion": "Clearly define agent capability boundaries using 'behavior + triggers + exceptions' patterns. Provide batch processing interfaces for repetitive tasks, allowing users to manage hundreds of AI-executed micro-tasks efficiently."
            },
            "q9": {
                "area": "Trust - Observability & Control",
                "aipet_dimension": "T - Trust (信任建立)", 
                "suggestion": "Implement observability and live feedback mechanisms. Visualize AI's action plans before execution, allowing users to review, modify, or reject plans. Build confidence through transparent decision-making processes and error recovery options."
            },
            "q10": {
                "area": "Privacy - Contextual Authorization",
                "aipet_dimension": "P - Privacy (隱私增強)",
                "suggestion": "Embed privacy controls within interactions. When AI needs permissions (calendar access, contacts), request authorization in context rather than in buried settings pages. Design 'just enough friction' for trust building."
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
            comparison["benchmark_category"] = "Top Tier (Top 10%)"
        elif percentile >= 75:
            comparison["benchmark_category"] = "Excellent (Top 25%)"
        elif percentile >= 50:
            comparison["benchmark_category"] = "Above Average (Top 50%)"
        elif percentile >= 25:
            comparison["benchmark_category"] = "Average (Top 75%)"
        else:
            comparison["benchmark_category"] = "Needs Improvement (Bottom 25%)"
        
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