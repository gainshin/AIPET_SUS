# -*- coding: utf-8 -*-
"""
AIPET Open-ended Questions Module
AIPET 開放性問題模組

Based on AIPET Framework (Agency, Interaction, Privacy, Experience, Trust)
基於 AIPET 框架的開放性問題評估
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum

class AIPETDimension(Enum):
    """AIPET 框架維度"""
    AGENCY = "A"          # 代理能力
    INTERACTION = "I"     # 互動模式 
    PRIVACY = "P"         # 隱私增強
    EXPERIENCE = "E"      # 體驗連續性
    TRUST = "T"          # 信任建立

@dataclass
class AIPETQuestion:
    """AIPET 問題結構"""
    id: str
    text: str
    dimension: AIPETDimension
    sub_category: str
    is_required: bool = False  # All AIPET questions are optional

class AIPETQuestionnaire:
    """AIPET 開放性問卷評估器"""
    
    def __init__(self):
        self.questions = self._initialize_questions()
    
    def _initialize_questions(self) -> List[AIPETQuestion]:
        """初始化 AIPET 開放性問題"""
        return [
            AIPETQuestion(
                id="I1",
                text="Describe your preferred way to communicate your interview intentions to an AI system. Would you rather use structured forms, natural conversation, voice commands, or a combination? What would make you feel most understood?",
                dimension=AIPETDimension.INTERACTION,
                sub_category="Communication Preferences"
            ),
            AIPETQuestion(
                id="P2", 
                text="What are your biggest privacy concerns when interacting with an AI interviewing system? How would you want the system to address these concerns throughout the interview process?",
                dimension=AIPETDimension.PRIVACY,
                sub_category="Privacy Concerns"
            ),
            AIPETQuestion(
                id="T1",
                text="Think about a time when you might disagree with an AI interviewer's assessment or decision. How would you want the system to handle this situation? What would need to happen for you to trust the process again?",
                dimension=AIPETDimension.TRUST,
                sub_category="Conflict Resolution"
            ),
            AIPETQuestion(
                id="A1",
                text="When the AI interviewer makes autonomous decisions during your interview (such as adjusting question difficulty or focus areas), what level of control would you prefer to maintain? Describe your ideal balance between AI autonomy and your oversight.",
                dimension=AIPETDimension.AGENCY,
                sub_category="Autonomy Balance"
            ),
            AIPETQuestion(
                id="E1",
                text="If you started an interview process on your phone and needed to continue on your laptop, or came back to it days later, what information should the AI remember about you? What should it \"forget\" to respect your privacy?",
                dimension=AIPETDimension.EXPERIENCE,
                sub_category="Cross-device Continuity"
            ),
            AIPETQuestion(
                id="T2",
                text="What would an AI interviewing system need to show or tell you during the process to make you feel confident that it's making fair and accurate evaluations? Describe the transparency you need to trust the system.",
                dimension=AIPETDimension.TRUST,
                sub_category="Transparency Requirements"
            ),
            AIPETQuestion(
                id="A2", 
                text="Think about a scenario where the AI interviewer needs to handle an unexpected situation (like technical difficulties or unclear responses). What boundaries should the AI have, and when should it escalate to human intervention?",
                dimension=AIPETDimension.AGENCY,
                sub_category="Capability Boundaries"
            ),
            AIPETQuestion(
                id="P1",
                text="When an AI interviewer needs access to your personal information (resume, portfolio, previous interview records), how would you want to be asked for permission? Describe the approach that would make you feel most comfortable and in control.",
                dimension=AIPETDimension.PRIVACY,
                sub_category="Permission Management"
            ),
            AIPETQuestion(
                id="I2",
                text="Imagine you could customize how much the AI interviewer controls versus how much you control during the interview process. Walk us through your ideal \"control spectrum\" - when would you want full automation versus manual control?",
                dimension=AIPETDimension.INTERACTION,
                sub_category="Control Spectrum"
            ),
            AIPETQuestion(
                id="E2",
                text="Describe how you would want an AI interviewer to learn and adapt from your previous interactions. What kind of personalization would enhance your experience versus what might feel intrusive?",
                dimension=AIPETDimension.EXPERIENCE,
                sub_category="Adaptive Learning"
            )
        ]
    
    def get_questions(self) -> List[Dict]:
        """獲取所有 AIPET 問題"""
        return [
            {
                "id": q.id,
                "text": q.text,
                "dimension": q.dimension.value,
                "dimension_name": self._get_dimension_name(q.dimension),
                "sub_category": q.sub_category,
                "is_required": q.is_required
            }
            for q in self.questions
        ]
    
    def get_questions_by_dimension(self) -> Dict[str, List[Dict]]:
        """按維度分組獲取問題"""
        grouped = {
            "A": [], "I": [], "P": [], "E": [], "T": []
        }
        
        for q in self.questions:
            grouped[q.dimension.value].append({
                "id": q.id,
                "text": q.text,
                "sub_category": q.sub_category,
                "is_required": q.is_required
            })
        
        return grouped
    
    def _get_dimension_name(self, dimension: AIPETDimension) -> str:
        """獲取維度名稱"""
        dimension_names = {
            AIPETDimension.AGENCY: "Agency (代理能力)",
            AIPETDimension.INTERACTION: "Interaction (互動模式)",
            AIPETDimension.PRIVACY: "Privacy (隱私增強)",
            AIPETDimension.EXPERIENCE: "Experience (體驗連續性)",
            AIPETDimension.TRUST: "Trust (信任建立)"
        }
        return dimension_names.get(dimension, "Unknown")
    
    def validate_responses(self, responses: Dict[str, str]) -> Dict[str, List[str]]:
        """驗證回答（由於都是選填，主要檢查格式）"""
        errors = {
            "validation_errors": [],
            "warnings": []
        }
        
        # 檢查是否有無效的問題 ID
        valid_question_ids = {q.id for q in self.questions}
        for question_id in responses.keys():
            if question_id not in valid_question_ids:
                errors["validation_errors"].append(f"Invalid question ID: {question_id}")
        
        # 檢查回答長度（建議性檢查）
        for question_id, response in responses.items():
            if response and len(response.strip()) > 2000:
                errors["warnings"].append(f"Response to {question_id} is quite long ({len(response)} characters). Consider being more concise.")
            elif response and len(response.strip()) < 10:
                errors["warnings"].append(f"Response to {question_id} seems quite brief. Consider providing more detail if possible.")
        
        return errors
    
    def analyze_responses(self, responses: Dict[str, str]) -> Dict:
        """分析 AIPET 問題回答"""
        analysis = {
            "total_questions": len(self.questions),
            "answered_questions": len([r for r in responses.values() if r and r.strip()]),
            "completion_rate": 0,
            "dimension_coverage": {},
            "insights": []
        }
        
        # 計算完成率
        if analysis["total_questions"] > 0:
            analysis["completion_rate"] = analysis["answered_questions"] / analysis["total_questions"] * 100
        
        # 分析各維度覆蓋情況
        dimension_counts = {"A": 0, "I": 0, "P": 0, "E": 0, "T": 0}
        dimension_totals = {"A": 0, "I": 0, "P": 0, "E": 0, "T": 0}
        
        for question in self.questions:
            dim = question.dimension.value
            dimension_totals[dim] += 1
            
            if question.id in responses and responses[question.id] and responses[question.id].strip():
                dimension_counts[dim] += 1
        
        for dim in dimension_counts:
            analysis["dimension_coverage"][dim] = {
                "answered": dimension_counts[dim],
                "total": dimension_totals[dim],
                "percentage": (dimension_counts[dim] / dimension_totals[dim] * 100) if dimension_totals[dim] > 0 else 0,
                "name": self._get_dimension_name(AIPETDimension(dim))
            }
        
        # 生成見解
        analysis["insights"] = self._generate_insights(analysis, responses)
        
        return analysis
    
    def _generate_insights(self, analysis: Dict, responses: Dict[str, str]) -> List[Dict]:
        """基於回答生成見解"""
        insights = []
        
        # 完成率見解
        completion_rate = analysis["completion_rate"]
        if completion_rate >= 80:
            insights.append({
                "type": "positive",
                "title": "High Engagement",
                "description": f"Excellent participation with {completion_rate:.0f}% completion rate. This comprehensive feedback will help improve Agentive UX design."
            })
        elif completion_rate >= 50:
            insights.append({
                "type": "neutral", 
                "title": "Moderate Engagement",
                "description": f"Good participation with {completion_rate:.0f}% completion rate. Consider answering additional questions for more personalized insights."
            })
        else:
            insights.append({
                "type": "suggestion",
                "title": "Low Participation",
                "description": f"Only {completion_rate:.0f}% questions answered. Your additional insights would be valuable for improving AI-human interaction design."
            })
        
        # 維度覆蓋見解
        high_coverage_dims = [dim for dim, data in analysis["dimension_coverage"].items() 
                             if data["percentage"] >= 75]
        low_coverage_dims = [dim for dim, data in analysis["dimension_coverage"].items() 
                            if data["percentage"] < 25]
        
        if high_coverage_dims:
            dim_names = [analysis["dimension_coverage"][dim]["name"].split("(")[0].strip() 
                        for dim in high_coverage_dims]
            insights.append({
                "type": "positive",
                "title": "Strong Domain Focus", 
                "description": f"Excellent coverage in {', '.join(dim_names)} dimensions. Your insights will contribute to these specific areas of Agentive UX research."
            })
        
        if low_coverage_dims and len(low_coverage_dims) < 3:
            dim_names = [analysis["dimension_coverage"][dim]["name"].split("(")[0].strip() 
                        for dim in low_coverage_dims]
            insights.append({
                "type": "suggestion",
                "title": "Opportunity for Additional Insights",
                "description": f"Consider sharing thoughts on {', '.join(dim_names)} to provide a more complete perspective on AI interaction design."
            })
        
        return insights
    
    def get_dimension_statistics(self) -> Dict[str, int]:
        """獲取各維度問題統計"""
        stats = {"A": 0, "I": 0, "P": 0, "E": 0, "T": 0}
        
        for question in self.questions:
            stats[question.dimension.value] += 1
        
        return stats

# 使用範例
if __name__ == "__main__":
    aipet = AIPETQuestionnaire()
    
    print("AIPET Open-ended Questions:")
    questions = aipet.get_questions()
    
    for i, q in enumerate(questions, 1):
        print(f"\nQ{i}. {q['text']} ({q['id']})")
        print(f"   Dimension: {q['dimension_name']}")
        print(f"   Category: {q['sub_category']}")
    
    print(f"\n📊 Dimension Distribution:")
    stats = aipet.get_dimension_statistics()
    for dim, count in stats.items():
        dim_name = aipet._get_dimension_name(AIPETDimension(dim))
        print(f"   {dim} ({dim_name.split('(')[0].strip()}): {count} questions")