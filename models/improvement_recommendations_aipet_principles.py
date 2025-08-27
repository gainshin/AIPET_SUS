# -*- coding: utf-8 -*-
"""
AIPET Framework: Improvement Recommendations Principles
基於代理式使用者體驗(Agentive UX)理論框架的改善建議原則

從「UI Drawer」到「Agent Choreographer」的轉變，與產業專家的觀察高度一致。
Jakob Nielsen 最近指出：
"We'll still craft humane experiences, but increasingly through policies, protocols, 
and orchestrations rather than panels and palettes."

本文件定義代理式使用者體驗 (Agentive UX) 的演化路徑，並提供一套系統化的實踐框架 (AIPET)，
最終聚焦於設計師在「提示到介面 (Prompt-to-UI)」時代所需的核心技能：脈絡工程 (Context Engineering)。
"""

class AIPETFramework:
    """
    AIPET實踐框架：整合業界智慧
    
    AIPET框架為設計Agentive UX提供了五個關鍵支柱，
    整合了Microsoft與Salesforce的觀點後，此框架變得更加完整。
    """
    
    @staticmethod
    def get_framework_principles():
        """獲取AIPET框架的五大核心原則"""
        return {
            "A": {
                "name": "Agency (代理能力)",
                "description": "定義AI代理人的能力邊界與自主性",
                "design_strategy": """
                不僅要使用「規則 = 行為 + 觸發器 + 例外」的模式來定義能力邊界，
                更要如Microsoft所強調，讓代理人具備多模態輸入與輸出的能力，
                能跨越聲音、語音、文字、圖像等多種模態進行理解與回應。
                """,
                "key_concepts": [
                    "多模態輸入輸出能力",
                    "明確的能力邊界定義",
                    "規則化行為模式",
                    "自主決策機制",
                    "例外處理能力"
                ]
            },
            "I": {
                "name": "Interaction (互動模式)",
                "description": "設計從手動到自動的光譜式控制體驗",
                "design_strategy": """
                提供從「全手動」到「全自動」的光譜式控制，如同汽車的「巡航模式」，
                讓使用者可以隨時無縫接管或放權。同時，對於重複性任務，應採用「批次處理」
                的介面模式，讓使用者能一次管理數百個由AI執行的微任務。
                """,
                "key_concepts": [
                    "光譜式控制 (全手動到全自動)",
                    "無縫接管與放權機制",
                    "批次處理介面模式",
                    "引導式意圖宣告",
                    "混合式介面設計"
                ]
            },
            "P": {
                "name": "Privacy (隱私增強)",
                "description": "將隱私控制權內建於互動中",
                "design_strategy": """
                將隱私控制權內建於互動中。當AI需要更多權限時，它必須在當下情境中
                明確請求授權，而不是讓使用者在深埋的設定頁面中尋找選項。
                這種「剛剛好的摩擦力」是建立信任的關鍵。
                """,
                "key_concepts": [
                    "情境內即時授權",
                    "適度摩擦力設計",
                    "透明的權限請求",
                    "使用者資料控制權",
                    "隱私設定可見性"
                ]
            },
            "E": {
                "name": "Experience (體驗連續性)",
                "description": "確保跨設備、跨時間的無縫體驗",
                "design_strategy": """
                確保AI代理擁有跨設備、跨時間的記憶。這不僅是讓使用者在手機上開始的任務
                能在筆電上無縫接續，更是利用歷史資料來「反思過去」，並根據當下情境
                「動態提示」，最終實現跨時間的「自適應演進」。
                """,
                "key_concepts": [
                    "跨設備無縫體驗",
                    "跨時間記憶能力",
                    "歷史資料反思",
                    "動態情境提示",
                    "自適應演進機制"
                ]
            },
            "T": {
                "name": "Trust (信任建立)",
                "description": "透過可恢復性與透明度建立深度信任",
                "design_strategy": """
                信任的雙支柱是可恢復性(Recoverability)與透明度(Transparency)。
                可恢復性確保當AI犯錯時，使用者可以輕鬆撤銷；而透明度則是在AI行動前
                就建立信任。一個清晰、可互動的任務日誌和一鍵撤銷功能，是實現這兩點的關鍵。
                """,
                "key_concepts": [
                    "可恢復性機制",
                    "透明度設計",
                    "人類掌舵原則",
                    "可見的推理過程",
                    "一鍵撤銷功能"
                ]
            }
        }
    
    @staticmethod
    def get_maturity_model():
        """獲取Salesforce提出的五級代理人成熟度模型"""
        return {
            "Level 0-1": {
                "name": "規則與檢索",
                "description": "設計師為代理人設定固定的規則和知識庫"
            },
            "Level 2": {
                "name": "簡單編排",
                "description": "設計師開始設計單一領域內的任務流程"
            },
            "Level 3": {
                "name": "複雜編排",
                "description": "設計師需要處理跨越多個領域的任務"
            },
            "Level 4": {
                "name": "多代理人編排",
                "description": "設計的終極目標是設計一個生態系，讓多個自主代理人協商與合作"
            }
        }
    
    @staticmethod
    def get_context_engineering_strategies():
        """獲取脈絡工程的實踐策略"""
        return {
            "guided_intent_declaration": {
                "challenge": "開放式的prompt輸入框常讓使用者感到迷茫",
                "strategy": "設計混合式介面，透過結構化元件引導使用者清晰地「宣告」高層次目標"
            },
            "dynamic_learning": {
                "challenge": "AI不知道使用者的個人偏好和工作流程，且這些偏好會隨時間演化",
                "strategy": "設計一個讓AI能從使用者反饋中持續學習和適應的機制"
            },
            "observability_feedback": {
                "challenge": "AI的「思考」過程是一個黑盒子，使用者在等待時會感到焦慮和失控",
                "strategy": "將AI的行動計畫視覺化，使用者可以在AI執行前就審核、修改或否決計畫"
            }
        }

class AgentiveUXPrinciples:
    """
    代理式使用者體驗的核心原則
    
    從「打造更有效率的工具」轉向「設計更智慧的合作夥伴」
    """
    
    @staticmethod
    def get_paradigm_shift():
        """獲取典範演進的四個階段"""
        return {
            "tool_to_partner": {
                "from": "附加功能",
                "to": "代理人階段", 
                "description": "AI從被動工具轉向能主動執行多步驟、跨應用複雜任務的代理人"
            },
            "task_to_goal": {
                "from": "任務指導",
                "to": "目標達成",
                "description": "使用者不再需要告訴系統「如何做」，只需表達「想要什麼」"
            },
            "chat_to_context": {
                "from": "聊天介面", 
                "to": "情境化協作",
                "description": "未來的互動將是多模態、情境化的，聊天退居二線成為備用選項"
            },
            "request_to_loop": {
                "from": "單次請求",
                "to": "持續性循環",
                "description": "AI代理人運作模式是持續的「感知-思考-行動」循環"
            }
        }

class IndustryFrameworks:
    """
    業界框架：Microsoft與Salesforce的雙重視角
    """
    
    @staticmethod
    def get_microsoft_framework():
        """Microsoft Agent UX：時空三維框架"""
        return {
            "space": {
                "name": "空間 (Space)",
                "description": "代理人運作的環境",
                "principles": [
                    "連結而非瓦解人與知識",
                    "易於訪問但適時無形",
                    "在背景運作，僅在關鍵時刻出現"
                ]
            },
            "time": {
                "name": "時間 (Time)", 
                "description": "跨時間的記憶與演進能力",
                "principles": [
                    "反思過去 (Past)",
                    "動態提示現在 (Now)", 
                    "適應未來 (Future)"
                ]
            },
            "core": {
                "name": "核心 (Core)",
                "description": "設計的基礎原則",
                "principles": [
                    "擁抱不確定性",
                    "透明度建立信任",
                    "使用者控制權",
                    "體驗一致性"
                ]
            }
        }
    
    @staticmethod
    def get_salesforce_framework():
        """Salesforce Agent Experience (AX) Design：雙重視角"""
        return {
            "design_for_agents": {
                "name": "為代理人設計",
                "description": "優化AI代理人運作的數位環境",
                "includes": [
                    "高品質的API",
                    "良好的知識管理系統",
                    "標準化的代理人間通訊協定"
                ]
            },
            "design_of_agents": {
                "name": "設計代理人",
                "description": "設計AI代理人本身的行為模式", 
                "includes": [
                    "對話設計",
                    "提示工程",
                    "結構化本體論定義",
                    "人類在環 (Human at the helm)",
                    "透過透明度建立信任"
                ]
            }
        }

# 使用範例
if __name__ == "__main__":
    # 獲取AIPET框架原則
    aipet = AIPETFramework()
    principles = aipet.get_framework_principles()
    
    print("AIPET Framework Principles:")
    for key, principle in principles.items():
        print(f"\n{key} - {principle['name']}")
        print(f"描述: {principle['description']}")
        print(f"關鍵概念: {', '.join(principle['key_concepts'])}")
    
    # 獲取成熟度模型
    maturity = aipet.get_maturity_model()
    print("\n\nAgent Maturity Model:")
    for level, info in maturity.items():
        print(f"{level}: {info['name']} - {info['description']}")