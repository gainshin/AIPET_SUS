"""
報告生成器
生成PDF格式的評估報告
"""

import os
import datetime
from typing import Dict, List
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.lib.colors import Color, black, blue, red, green, orange
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.platypus import Image as RLImage
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import io
import base64

# 設置matplotlib使用非互動後端
matplotlib.use('Agg')

class ReportGenerator:
    """PDF報告生成器"""
    
    def __init__(self):
        self.setup_fonts()
        self.setup_styles()
        self.setup_colors()
    
    def setup_fonts(self):
        """設置字體"""
        # 註冊中文字體（這裡使用系統默認字體）
        try:
            # 嘗試註冊中文字體
            font_paths = [
                '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
                '/System/Library/Fonts/Helvetica.ttc',
                'C:/Windows/Fonts/msyh.ttc'  # Windows微軟雅黑
            ]
            
            for font_path in font_paths:
                if os.path.exists(font_path):
                    pdfmetrics.registerFont(TTFont('Chinese', font_path))
                    break
            else:
                # 如果沒有找到中文字體，使用默認字體
                self.chinese_font = 'Helvetica'
        except:
            self.chinese_font = 'Helvetica'
    
    def setup_styles(self):
        """設置樣式"""
        self.styles = getSampleStyleSheet()
        
        # 標題樣式
        self.styles.add(ParagraphStyle(
            name='ChineseTitle',
            fontName='Helvetica-Bold',
            fontSize=24,
            alignment=TA_CENTER,
            spaceAfter=30,
            textColor=blue
        ))
        
        # 二級標題樣式
        self.styles.add(ParagraphStyle(
            name='ChineseHeading2',
            fontName='Helvetica-Bold',
            fontSize=18,
            spaceBefore=20,
            spaceAfter=10,
            textColor=black
        ))
        
        # 三級標題樣式
        self.styles.add(ParagraphStyle(
            name='ChineseHeading3',
            fontName='Helvetica-Bold',
            fontSize=14,
            spaceBefore=15,
            spaceAfter=8,
            textColor=black
        ))
        
        # 正文樣式
        self.styles.add(ParagraphStyle(
            name='ChineseBody',
            fontName='Helvetica',
            fontSize=12,
            spaceBefore=6,
            spaceAfter=6,
            alignment=TA_LEFT
        ))
        
        # 重要信息樣式
        self.styles.add(ParagraphStyle(
            name='ChineseImportant',
            fontName='Helvetica-Bold',
            fontSize=12,
            spaceBefore=6,
            spaceAfter=6,
            textColor=red
        ))
    
    def setup_colors(self):
        """設置顏色"""
        self.colors = {
            'excellent': Color(0.2, 0.8, 0.2),    # 綠色
            'good': Color(0.2, 0.6, 0.8),         # 藍色
            'average': Color(0.8, 0.8, 0.2),      # 黃色
            'poor': Color(0.8, 0.4, 0.2),         # 橙色
            'very_poor': Color(0.8, 0.2, 0.2),    # 紅色
            'kano_must_be': Color(0.8, 0.2, 0.2), # 基礎型-紅色
            'kano_one_dim': Color(0.2, 0.6, 0.8), # 期望型-藍色
            'kano_attractive': Color(0.2, 0.8, 0.2), # 魅力型-綠色
            'kano_indifferent': Color(0.7, 0.7, 0.7), # 無差異-灰色
            'kano_reverse': Color(0.5, 0.2, 0.8)   # 反向-紫色
        }
    
    def generate_pdf_report(self, evaluation_data: Dict, evaluation_id: str) -> str:
        """
        生成PDF報告
        
        Args:
            evaluation_data: 評估數據
            evaluation_id: 評估ID
            
        Returns:
            PDF文件路徑
        """
        # 創建報告目錄
        os.makedirs('reports', exist_ok=True)
        
        # 生成文件名
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'AI_Agent_評估報告_{evaluation_id}_{timestamp}.pdf'
        filepath = os.path.join('reports', filename)
        
        # 創建PDF文檔
        doc = SimpleDocTemplate(
            filepath,
            pagesize=A4,
            rightMargin=2*cm,
            leftMargin=2*cm,
            topMargin=2*cm,
            bottomMargin=2*cm
        )
        
        # 構建報告內容
        story = []
        
        # 添加標題頁
        story.extend(self._build_title_page(evaluation_data))
        story.append(PageBreak())
        
        # 添加執行摘要
        story.extend(self._build_executive_summary(evaluation_data))
        story.append(PageBreak())
        
        # 添加SUS評估結果
        story.extend(self._build_sus_section(evaluation_data))
        story.append(PageBreak())
        
        # 添加Kano模型分析
        story.extend(self._build_kano_section(evaluation_data))
        story.append(PageBreak())
        
        # 添加綜合分析
        story.extend(self._build_overall_analysis(evaluation_data))
        story.append(PageBreak())
        
        # 添加改進建議
        story.extend(self._build_recommendations(evaluation_data))
        
        # 生成PDF
        doc.build(story)
        
        return filepath
    
    def _build_title_page(self, data: Dict) -> List:
        """構建標題頁"""
        story = []
        
        # 主標題
        story.append(Paragraph("AI Agent 可用性評估報告", self.styles['ChineseTitle']))
        story.append(Spacer(1, 50))
        
        # 項目信息
        project_info = data.get('project_info', {})
        
        project_table_data = [
            ['項目名稱', project_info.get('name', 'N/A')],
            ['項目描述', project_info.get('description', 'N/A')],
            ['版本', project_info.get('version', 'N/A')],
            ['開發團隊', project_info.get('team', 'N/A')],
            ['評估日期', data.get('evaluation_date', 'N/A')[:10]],
            ['評估ID', data.get('evaluation_id', 'N/A')]
        ]
        
        project_table = Table(project_table_data, colWidths=[3*cm, 10*cm])
        project_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('GRID', (0, 0), (-1, -1), 1, black),
            ('BACKGROUND', (0, 0), (0, -1), Color(0.9, 0.9, 0.9))
        ]))
        
        story.append(project_table)
        story.append(Spacer(1, 100))
        
        # 評估摘要
        overall = data.get('overall_assessment', {})
        
        story.append(Paragraph("評估摘要", self.styles['ChineseHeading2']))
        
        summary_data = [
            ['綜合分數', f"{overall.get('overall_score', 0):.1f}/100"],
            ['成熟度等級', overall.get('maturity_level', 'N/A')],
            ['SUS分數', f"{data.get('sus_evaluation', {}).get('score', 0):.1f}/100"],
            ['SUS等級', data.get('sus_evaluation', {}).get('grade', 'N/A')],
        ]
        
        summary_table = Table(summary_data, colWidths=[4*cm, 6*cm])
        summary_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 14),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 2, black),
            ('BACKGROUND', (0, 0), (-1, -1), Color(0.95, 0.95, 0.95))
        ]))
        
        story.append(summary_table)
        
        return story
    
    def _build_executive_summary(self, data: Dict) -> List:
        """構建執行摘要"""
        story = []
        
        story.append(Paragraph("執行摘要", self.styles['ChineseTitle']))
        story.append(Spacer(1, 20))
        
        # 總體評估
        overall = data.get('overall_assessment', {})
        sus_data = data.get('sus_evaluation', {})
        
        summary_text = f"""
        本次評估針對 {data.get('project_info', {}).get('name', 'AI Agent系統')} 進行了全面的可用性分析，
        結合了SUS量表和Kano模型兩種科學的評估方法。
        
        <b>主要發現：</b>
        • 綜合評估分數：{overall.get('overall_score', 0):.1f}/100 ({overall.get('maturity_level', 'N/A')})
        • SUS可用性分數：{sus_data.get('score', 0):.1f}/100 ({sus_data.get('grade', 'N/A')}等級)
        • 系統可接受性：{sus_data.get('acceptability', 'N/A')}
        • 用戶滿意度：{sus_data.get('adjective_rating', 'N/A')}
        """
        
        story.append(Paragraph(summary_text, self.styles['ChineseBody']))
        story.append(Spacer(1, 20))
        
        # 關鍵優勢
        strengths = overall.get('key_strengths', [])
        if strengths:
            story.append(Paragraph("關鍵優勢", self.styles['ChineseHeading3']))
            for strength in strengths:
                story.append(Paragraph(f"• {strength}", self.styles['ChineseBody']))
            story.append(Spacer(1, 15))
        
        # 關鍵問題
        issues = overall.get('critical_issues', [])
        if issues:
            story.append(Paragraph("關鍵問題", self.styles['ChineseHeading3']))
            for issue in issues:
                story.append(Paragraph(f"• {issue}", self.styles['ChineseImportant']))
            story.append(Spacer(1, 15))
        
        # 優先行動
        actions = overall.get('priority_actions', [])
        if actions:
            story.append(Paragraph("優先行動建議", self.styles['ChineseHeading3']))
            for i, action in enumerate(actions, 1):
                story.append(Paragraph(f"{i}. {action}", self.styles['ChineseBody']))
        
        return story
    
    def _build_sus_section(self, data: Dict) -> List:
        """構建SUS評估部分"""
        story = []
        
        story.append(Paragraph("SUS量表評估結果", self.styles['ChineseTitle']))
        story.append(Spacer(1, 20))
        
        sus_data = data.get('sus_evaluation', {})
        detailed = sus_data.get('detailed_analysis', {})
        
        # SUS分數概覽
        story.append(Paragraph("評估概覽", self.styles['ChineseHeading2']))
        
        sus_overview_data = [
            ['指標', '結果', '說明'],
            ['SUS分數', f"{sus_data.get('score', 0):.1f}/100", '標準化可用性分數'],
            ['等級', sus_data.get('grade', 'N/A'), 'A-F等級評定'],
            ['百分位數', f"{sus_data.get('percentile', 0):.1f}%", '在所有系統中的排名'],
            ['形容詞評級', sus_data.get('adjective_rating', 'N/A'), '主觀感受描述'],
            ['可接受性', sus_data.get('acceptability', 'N/A'), '是否達到可用標準']
        ]
        
        sus_table = Table(sus_overview_data, colWidths=[3*cm, 3*cm, 7*cm])
        sus_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 1, black),
            ('BACKGROUND', (0, 0), (-1, 0), Color(0.8, 0.8, 0.8))
        ]))
        
        story.append(sus_table)
        story.append(Spacer(1, 20))
        
        # 基準比較
        benchmark = detailed.get('benchmark_comparison', {})
        if benchmark:
            story.append(Paragraph("行業基準比較", self.styles['ChineseHeading2']))
            
            benchmark_text = f"""
            您的系統得分 {benchmark.get('your_score', 0):.1f}，
            {"高於" if benchmark.get('difference_from_average', 0) > 0 else "低於"}行業平均分 {benchmark.get('industry_average', 0):.1f} 約 {abs(benchmark.get('difference_from_average', 0)):.1f}分。
            
            在所有參與評估的系統中，您的系統表現超越了 {benchmark.get('percentile', 0):.1f}% 的系統，
            屬於 {benchmark.get('benchmark_category', 'N/A')} 範圍。
            """
            
            story.append(Paragraph(benchmark_text, self.styles['ChineseBody']))
            story.append(Spacer(1, 20))
        
        # 優勢和劣勢分析
        strengths = detailed.get('strengths', [])
        weaknesses = detailed.get('weaknesses', [])
        
        if strengths or weaknesses:
            story.append(Paragraph("詳細分析", self.styles['ChineseHeading2']))
            
            if strengths:
                story.append(Paragraph("系統優勢：", self.styles['ChineseHeading3']))
                for strength in strengths:
                    story.append(Paragraph(f"✓ {strength}", self.styles['ChineseBody']))
                story.append(Spacer(1, 10))
            
            if weaknesses:
                story.append(Paragraph("需要改進的領域：", self.styles['ChineseHeading3']))
                for weakness in weaknesses:
                    story.append(Paragraph(f"⚠ {weakness}", self.styles['ChineseImportant']))
        
        return story
    
    def _build_kano_section(self, data: Dict) -> List:
        """構建Kano模型分析部分"""
        story = []
        
        story.append(Paragraph("Kano模型分析結果", self.styles['ChineseTitle']))
        story.append(Spacer(1, 20))
        
        kano_data = data.get('kano_evaluation', {})
        summary = kano_data.get('summary', {})
        
        # Kano分類統計
        story.append(Paragraph("需求類型分佈", self.styles['ChineseHeading2']))
        
        category_percentages = summary.get('category_percentages', {})
        
        kano_distribution_data = [['需求類型', '數量', '百分比', '說明']]
        
        category_descriptions = {
            'Must-be': '基礎型需求 - 必須滿足的基本功能',
            'One-dimensional': '期望型需求 - 性能越好滿意度越高',
            'Attractive': '魅力型需求 - 能創造驚喜的功能',
            'Indifferent': '無差異需求 - 用戶不關心的功能',
            'Reverse': '反向需求 - 用戶不希望的功能',
            'Questionable': '有疑問需求 - 回答矛盾需要重新評估'
        }
        
        for category, percentage in category_percentages.items():
            count = summary.get('category_counts', {}).get(category, 0)
            description = category_descriptions.get(category, '')
            kano_distribution_data.append([category, str(count), f"{percentage:.1f}%", description])
        
        kano_table = Table(kano_distribution_data, colWidths=[2.5*cm, 1.5*cm, 2*cm, 7*cm])
        kano_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('ALIGN', (0, 0), (2, -1), 'CENTER'),
            ('ALIGN', (3, 0), (3, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 1, black),
            ('BACKGROUND', (0, 0), (-1, 0), Color(0.8, 0.8, 0.8))
        ]))
        
        story.append(kano_table)
        story.append(Spacer(1, 20))
        
        # 影響係數分析
        story.append(Paragraph("滿意度影響分析", self.styles['ChineseHeading2']))
        
        impact_text = f"""
        <b>平均滿意度影響係數：</b> {summary.get('average_satisfaction_impact', 0):.3f}
        <b>平均不滿意度影響係數：</b> {summary.get('average_dissatisfaction_impact', 0):.3f}
        
        滿意度影響係數反映功能改進對用戶滿意度的正面提升程度。
        不滿意度影響係數反映功能缺失對用戶滿意度的負面影響程度。
        """
        
        story.append(Paragraph(impact_text, self.styles['ChineseBody']))
        story.append(Spacer(1, 20))
        
        # 優先級功能
        priority_features = summary.get('priority_features', {})
        if priority_features:
            story.append(Paragraph("功能優先級建議", self.styles['ChineseHeading2']))
            
            feature_types = [
                ('must_be_features', '優先滿足 - 基礎型需求'),
                ('one_dimensional_features', '重點提升 - 期望型需求'),
                ('attractive_features', '創新投入 - 魅力型需求')
            ]
            
            for feature_key, title in feature_types:
                features = priority_features.get(feature_key, [])
                if features:
                    story.append(Paragraph(title, self.styles['ChineseHeading3']))
                    for i, feature_id in enumerate(features, 1):
                        # 這裡可以根據feature_id獲取具體的功能描述
                        story.append(Paragraph(f"{i}. {feature_id.replace('_', ' ').title()}", self.styles['ChineseBody']))
                    story.append(Spacer(1, 10))
        
        return story
    
    def _build_overall_analysis(self, data: Dict) -> List:
        """構建綜合分析部分"""
        story = []
        
        story.append(Paragraph("綜合分析與建議", self.styles['ChineseTitle']))
        story.append(Spacer(1, 20))
        
        overall = data.get('overall_assessment', {})
        
        # 成熟度評估
        story.append(Paragraph("系統成熟度評估", self.styles['ChineseHeading2']))
        
        maturity_text = f"""
        根據SUS量表和Kano模型的綜合分析，您的AI Agent系統當前的成熟度等級為：
        <b>{overall.get('maturity_level', 'N/A')}</b>
        
        綜合評分：<b>{overall.get('overall_score', 0):.1f}/100</b>
        
        該評分結合了用戶可用性體驗（SUS分數佔70%權重）和功能需求滿足度（Kano分析佔30%權重）。
        """
        
        story.append(Paragraph(maturity_text, self.styles['ChineseBody']))
        story.append(Spacer(1, 20))
        
        # 競爭力分析
        story.append(Paragraph("市場競爭力分析", self.styles['ChineseHeading2']))
        
        sus_score = data.get('sus_evaluation', {}).get('score', 0)
        
        if sus_score >= 85:
            competitiveness = "您的系統在市場中具有強競爭優勢，用戶滿意度很高。"
        elif sus_score >= 75:
            competitiveness = "您的系統具有良好的市場競爭力，但仍有進一步提升的空間。"
        elif sus_score >= 65:
            competitiveness = "您的系統達到了基本的可用標準，但需要重點改進以提升競爭力。"
        else:
            competitiveness = "您的系統在市場競爭中處於劣勢，急需進行全面的可用性改進。"
        
        story.append(Paragraph(competitiveness, self.styles['ChineseBody']))
        story.append(Spacer(1, 20))
        
        # 風險評估
        story.append(Paragraph("潛在風險評估", self.styles['ChineseHeading2']))
        
        kano_summary = data.get('kano_evaluation', {}).get('summary', {})
        must_be_percentage = kano_summary.get('category_percentages', {}).get('Must-be', 0)
        
        risks = []
        if sus_score < 60:
            risks.append("用戶流失風險：可用性分數過低可能導致用戶放棄使用")
        if must_be_percentage > 40:
            risks.append("基礎功能風險：過多基礎需求未滿足會嚴重影響用戶體驗")
        
        avg_dissatisfaction = kano_summary.get('average_dissatisfaction_impact', 0)
        if avg_dissatisfaction > 0.6:
            risks.append("用戶不滿風險：功能缺失會顯著降低用戶滿意度")
        
        if risks:
            for risk in risks:
                story.append(Paragraph(f"⚠ {risk}", self.styles['ChineseImportant']))
        else:
            story.append(Paragraph("✓ 當前系統風險較低，整體表現良好", self.styles['ChineseBody']))
        
        return story
    
    def _build_recommendations(self, data: Dict) -> List:
        """構建改進建議部分"""
        story = []
        
        story.append(Paragraph("詳細改進建議", self.styles['ChineseTitle']))
        story.append(Spacer(1, 20))
        
        # SUS改進建議
        sus_suggestions = data.get('sus_evaluation', {}).get('detailed_analysis', {}).get('improvement_suggestions', [])
        
        if sus_suggestions:
            story.append(Paragraph("可用性改進建議（基於SUS分析）", self.styles['ChineseHeading2']))
            
            for i, suggestion in enumerate(sus_suggestions, 1):
                priority = suggestion.get('priority', '中')
                area = suggestion.get('area', 'N/A')
                desc = suggestion.get('suggestion', 'N/A')
                
                story.append(Paragraph(f"{i}. {area} [{priority}優先級]", self.styles['ChineseHeading3']))
                story.append(Paragraph(desc, self.styles['ChineseBody']))
                story.append(Spacer(1, 10))
            
            story.append(Spacer(1, 20))
        
        # Kano改進建議
        kano_recommendations = data.get('kano_evaluation', {}).get('recommendations', [])
        
        if kano_recommendations:
            story.append(Paragraph("功能需求改進建議（基於Kano分析）", self.styles['ChineseHeading2']))
            
            for i, recommendation in enumerate(kano_recommendations, 1):
                priority = recommendation.get('priority', '中')
                category = recommendation.get('category', 'N/A')
                feature = recommendation.get('feature', 'N/A')
                desc = recommendation.get('description', 'N/A')
                action = recommendation.get('action', 'N/A')
                
                story.append(Paragraph(f"{i}. {feature} [{priority}優先級 - {category}]", self.styles['ChineseHeading3']))
                story.append(Paragraph(f"分析：{desc}", self.styles['ChineseBody']))
                story.append(Paragraph(f"建議行動：{action}", self.styles['ChineseBody']))
                story.append(Spacer(1, 10))
        
        # 實施路線圖
        story.append(Spacer(1, 20))
        story.append(Paragraph("實施路線圖建議", self.styles['ChineseHeading2']))
        
        overall = data.get('overall_assessment', {})
        priority_actions = overall.get('priority_actions', [])
        
        roadmap_text = """
        基於本次評估結果，建議按以下順序實施改進：
        
        <b>短期目標（1-3個月）：</b>
        • 修復所有基礎型需求問題
        • 解決嚴重的可用性問題
        • 提升系統穩定性和可靠性
        
        <b>中期目標（3-6個月）：</b>
        • 優化期望型功能的性能
        • 改善用戶界面和交互體驗
        • 完善幫助文檔和用戶引導
        
        <b>長期目標（6-12個月）：</b>
        • 開發魅力型功能創造差異化優勢
        • 持續收集用戶反饋並迭代改進
        • 建立完善的可用性監控體系
        """
        
        story.append(Paragraph(roadmap_text, self.styles['ChineseBody']))
        
        return story