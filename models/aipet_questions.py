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
    kano_question_id: str
    is_required: bool = False  # All AIPET questions are optional

class AIPETQuestionnaire:
    """AIPET 開放性問卷評估器"""
    
    def __init__(self):
        self.questions = self._initialize_questions()
    
    def _initialize_questions(self) -> List[AIPETQuestion]:
        """初始化 AIPET 開放性問題 - 與 Kano 問題建立對應關係"""
        return [
            AIPETQuestion(
                id="response_accuracy",  # 對應 Kano: Response Accuracy
                text="When an AI Agent gives you inaccurate responses, what specific feedback mechanisms would help you correct it most effectively? What transparency about its confidence levels or reasoning would you want to see?",
                dimension=AIPETDimension.TRUST,
                sub_category="Response Accuracy & Trust",
                kano_question_id="response_accuracy"
            ),
            AIPETQuestion(
                id="response_speed",  # 對應 Kano: Response Speed  
                text="How would you prefer an AI Agent to manage your expectations during processing delays? Should it show progress indicators, offer interim responses, or give you control over speed vs quality trade-offs?",
                dimension=AIPETDimension.INTERACTION,
                sub_category="Response Timing & Control",
                kano_question_id="response_speed"
            ),
            AIPETQuestion(
                id="natural_conversation",  # 對應 Kano: Natural Conversation
                text="Describe your ideal balance between natural conversation flow and structured interaction with an AI Agent. When would you prefer guided prompts vs free-form dialogue? What makes conversation feel authentic to you?",
                dimension=AIPETDimension.INTERACTION,
                sub_category="Conversational Preferences", 
                kano_question_id="natural_conversation"
            ),
            AIPETQuestion(
                id="context_memory",  # 對應 Kano: Context Memory
                text="What information should an AI Agent remember about your conversations across sessions? How would you want to control what it remembers vs forgets? What memory capabilities would enhance vs concern you?",
                dimension=AIPETDimension.EXPERIENCE,
                sub_category="Context & Memory Management",
                kano_question_id="context_memory"
            ),
            AIPETQuestion(
                id="personalization",  # 對應 Kano: Personalization Service
                text="How would you want an AI Agent to learn your preferences without feeling invasive? What kind of personalization would enhance your experience, and what boundaries should it never cross?",
                dimension=AIPETDimension.EXPERIENCE,
                sub_category="Personalization & Boundaries",
                kano_question_id="personalization"
            ),
            AIPETQuestion(
                id="multi_modal",  # 對應 Kano: Multi-modal Interaction
                text="When interacting with an AI Agent across different modes (text, voice, images), how should it maintain consistency? What control would you want over switching between interaction modes?",
                dimension=AIPETDimension.INTERACTION,
                sub_category="Multi-modal Control",
                kano_question_id="multi_modal"
            ),
            AIPETQuestion(
                id="error_handling",  # 對應 Kano: Error Handling
                text="When an AI Agent makes mistakes, what recovery process would rebuild your trust? How should it acknowledge errors, and what control should you have over correcting its understanding?",
                dimension=AIPETDimension.TRUST,
                sub_category="Error Recovery & Trust",
                kano_question_id="error_handling"
            ),
            AIPETQuestion(
                id="learning_ability",  # 對應 Kano: Learning Ability
                text="How would you want to be involved in an AI Agent's learning process? What feedback mechanisms would feel natural to you, and how should the agent show it's incorporating your input?",
                dimension=AIPETDimension.AGENCY,
                sub_category="Collaborative Learning",
                kano_question_id="learning_ability"
            ),
            AIPETQuestion(
                id="emotional_intelligence",  # 對應 Kano: Emotional Intelligence  
                text="How should an AI Agent respond to your emotional state? What boundaries should it maintain, and what level of emotional recognition vs response would feel appropriate vs intrusive?",
                dimension=AIPETDimension.AGENCY,
                sub_category="Emotional Boundaries",
                kano_question_id="emotional_intelligence"
            ),
            AIPETQuestion(
                id="privacy_protection",  # 對應 Kano: Privacy Protection
                text="How would you want an AI Agent to request and manage access to your personal data? What transparency about data usage would make you comfortable, and what controls should always remain in your hands?",
                dimension=AIPETDimension.PRIVACY,
                sub_category="Data Privacy & Control",
                kano_question_id="privacy_protection"
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
                "kano_question_id": q.kano_question_id,
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