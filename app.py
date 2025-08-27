"""
AI Agent Usability Evaluation Tool - Flask Application
Integrated evaluation system combining Kano Model and SUS Scale
"""

import json
import datetime
from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import os
import sys

# 添加當前目錄到路徑
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.kano_model import KanoModelEvaluator, KanoCategory
from models.sus_scale import SUSEvaluator, SUSGrade
from models.aipet_questions import AIPETQuestionnaire
from utils.report_generator import ReportGenerator
from utils.data_manager import DataManager

app = Flask(__name__)
CORS(app)  # 允許跨域請求

# 初始化評估器
kano_evaluator = KanoModelEvaluator()
sus_evaluator = SUSEvaluator()
aipet_evaluator = AIPETQuestionnaire()
data_manager = DataManager()

@app.route('/')
def index():
    """主頁面"""
    return render_template('index.html')

@app.route('/api/kano/questions')
def get_kano_questions():
    """獲取Kano模型問題"""
    try:
        questions = kano_evaluator.get_default_questions()
        answer_options = kano_evaluator.answer_mapping
        
        return jsonify({
            'success': True,
            'questions': questions,
            'answer_options': answer_options
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/sus/questions')
def get_sus_questions():
    """獲取SUS問題"""
    try:
        questions = sus_evaluator.get_questions()
        likert_options = sus_evaluator.likert_options
        
        return jsonify({
            'success': True,
            'questions': questions,
            'likert_options': likert_options
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/aipet/questions')
def get_aipet_questions():
    """獲取AIPET開放性問題"""
    try:
        questions = aipet_evaluator.get_questions()
        questions_by_dimension = aipet_evaluator.get_questions_by_dimension()
        dimension_stats = aipet_evaluator.get_dimension_statistics()
        
        return jsonify({
            'success': True,
            'questions': questions,
            'questions_by_dimension': questions_by_dimension,
            'dimension_statistics': dimension_stats,
            'total_questions': len(questions),
            'note': 'All AIPET questions are optional. Answer as many as you feel comfortable with.'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/evaluate', methods=['POST'])
def evaluate():
    """綜合評估API"""
    try:
        data = request.get_json()
        
        # 驗證輸入數據
        if not data:
            return jsonify({
                'success': False,
                'error': '缺少評估數據'
            }), 400
        
        project_info = data.get('project_info', {})
        kano_responses = data.get('kano_responses', {})
        sus_responses_raw = data.get('sus_responses', {})
        aipet_responses = data.get('aipet_responses', {})
        
        # 確保SUS響應為整數類型
        sus_responses = {}
        app.logger.info(f"DEBUG: sus_responses_raw type and content: {type(sus_responses_raw)} - {sus_responses_raw}")
        for key, value in sus_responses_raw.items():
            app.logger.info(f"DEBUG: Converting {key}: {value} (type: {type(value)})")
            try:
                sus_responses[key] = int(value)
                app.logger.info(f"DEBUG: Converted {key} to {sus_responses[key]} (type: {type(sus_responses[key])})")
            except (ValueError, TypeError):
                app.logger.error(f"DEBUG: Conversion failed for {key}: {value} (type: {type(value)})")
                return jsonify({
                    'success': False,
                    'error': f'SUS回答必須是數字，問題 {key} 的回答是 {value}'
                }), 400
        
        # 驗證必要字段
        if not kano_responses:
            return jsonify({
                'success': False,
                'error': '缺少Kano模型評估數據'
            }), 400
            
        if not sus_responses:
            return jsonify({
                'success': False,
                'error': '缺少SUS量表評估數據'
            }), 400
        
        # 執行Kano評估
        kano_results = kano_evaluator.analyze_responses(kano_responses)
        kano_summary = kano_evaluator.generate_summary_statistics(kano_results)
        kano_recommendations = kano_evaluator.generate_improvement_recommendations(
            kano_results, 
            kano_evaluator.get_default_questions()
        )
        
        # 執行SUS評估
        sus_result = sus_evaluator.evaluate(sus_responses)
        sus_detailed = sus_evaluator.generate_detailed_report(sus_responses)
        
        # 執行AIPET開放性問題分析 (可選)
        aipet_analysis = None
        aipet_validation = None
        if aipet_responses:
            aipet_validation = aipet_evaluator.validate_responses(aipet_responses)
            aipet_analysis = aipet_evaluator.analyze_responses(aipet_responses)
        
        # 生成綜合評估結果
        evaluation_result = {
            'project_info': project_info,
            'evaluation_date': datetime.datetime.now().isoformat(),
            'kano_evaluation': {
                'results': {qid: {
                    'category': result.category.value,
                    'satisfaction_impact': result.satisfaction_impact,
                    'dissatisfaction_impact': result.dissatisfaction_impact,
                    'better_coefficient': result.better_coefficient,
                    'worse_coefficient': result.worse_coefficient
                } for qid, result in kano_results.items()},
                'summary': kano_summary,
                'recommendations': kano_recommendations
            },
            'sus_evaluation': {
                'score': sus_result.score,
                'grade': sus_result.grade.value,
                'percentile': sus_result.percentile,
                'adjective_rating': sus_result.adjective_rating,
                'acceptability': sus_result.acceptability,
                'detailed_analysis': sus_detailed
            },
            'overall_assessment': generate_overall_assessment(kano_summary, sus_result, aipet_analysis)
        }
        
        # 添加AIPET評估結果（如果有的話）
        if aipet_analysis:
            evaluation_result['aipet_evaluation'] = {
                'analysis': aipet_analysis,
                'validation': aipet_validation,
                'responses_provided': len([r for r in aipet_responses.values() if r and r.strip()]),
                'total_questions': len(aipet_evaluator.get_questions())
            }
        
        # 保存評估結果
        evaluation_id = data_manager.save_evaluation(evaluation_result)
        evaluation_result['evaluation_id'] = evaluation_id
        
        return jsonify({
            'success': True,
            'data': evaluation_result
        })
        
    except Exception as e:
        app.logger.error(f"評估過程中發生錯誤: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'評估過程中發生錯誤: {str(e)}'
        }), 500

def generate_overall_assessment(kano_summary, sus_result, aipet_analysis=None):
    """生成綜合評估"""
    assessment = {
        'overall_score': 0,
        'maturity_level': '',
        'key_strengths': [],
        'critical_issues': [],
        'priority_actions': []
    }
    
    # 計算綜合分數 (SUS分數佔70%，Kano滿意度影響佔30%)
    sus_weight = 0.7
    kano_weight = 0.3
    
    # 標準化Kano滿意度影響 (轉換為0-100分)
    kano_satisfaction_normalized = max(0, min(100, 
        (kano_summary['average_satisfaction_impact'] + 1) * 50
    ))
    
    assessment['overall_score'] = (
        sus_result.score * sus_weight + 
        kano_satisfaction_normalized * kano_weight
    )
    
    # 確定成熟度等級
    if assessment['overall_score'] >= 85:
        assessment['maturity_level'] = 'Excellent - Market Leading'
    elif assessment['overall_score'] >= 75:
        assessment['maturity_level'] = 'Good - Competitive'
    elif assessment['overall_score'] >= 65:
        assessment['maturity_level'] = 'Average - Needs Improvement'
    elif assessment['overall_score'] >= 55:
        assessment['maturity_level'] = 'Poor - Requires Optimization'
    else:
        assessment['maturity_level'] = 'Very Poor - Critical Issues'
    
    # Identify key strengths
    if sus_result.score >= 80:
        assessment['key_strengths'].append('High user satisfaction')
    if kano_summary['category_percentages'].get('Attractive', 0) > 20:
        assessment['key_strengths'].append('Features with attractive qualities')
    if kano_summary['category_percentages'].get('Must-be', 0) < 30:
        assessment['key_strengths'].append('Stable basic functionality')
    
    # Identify critical issues
    if sus_result.score < 60:
        assessment['critical_issues'].append('Severely insufficient usability')
    if kano_summary['category_percentages'].get('Must-be', 0) > 50:
        assessment['critical_issues'].append('Too many unmet basic requirements')
    if kano_summary['average_dissatisfaction_impact'] > 0.6:
        assessment['critical_issues'].append('High risk of user dissatisfaction')
    
    # Determine priority actions
    if sus_result.score < 70:
        assessment['priority_actions'].append('Immediately improve system usability')
    if kano_summary['category_percentages'].get('Must-be', 0) > 40:
        assessment['priority_actions'].append('Prioritize meeting basic requirements')
    if kano_summary['category_percentages'].get('One-dimensional', 0) > 30:
        assessment['priority_actions'].append('Enhance performance of expected features')
    
    # Include AIPET insights if available
    if aipet_analysis:
        completion_rate = aipet_analysis['completion_rate']
        
        # Add AIPET-based strengths
        if completion_rate >= 75:
            assessment['key_strengths'].append('High engagement with Agentive UX feedback collection')
        
        # Add AIPET-based priority actions
        if completion_rate >= 50:
            assessment['priority_actions'].append('Leverage detailed user insights to implement AIPET framework recommendations')
        
        # Add dimension-specific insights
        high_coverage_dims = [dim for dim, data in aipet_analysis['dimension_coverage'].items() 
                             if data['percentage'] >= 75]
        if len(high_coverage_dims) >= 3:
            assessment['key_strengths'].append('Strong user feedback across multiple AIPET dimensions')
    
    return assessment

@app.route('/api/evaluation/<evaluation_id>')
def get_evaluation(evaluation_id):
    """Get evaluation results"""
    try:
        evaluation = data_manager.get_evaluation(evaluation_id)
        if not evaluation:
            return jsonify({
                'success': False,
                'error': '評估結果不存在'
            }), 404
        
        return jsonify({
            'success': True,
            'data': evaluation
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/evaluations')
def list_evaluations():
    """列出所有評估"""
    try:
        evaluations = data_manager.list_evaluations()
        return jsonify({
            'success': True,
            'data': evaluations
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/report/<evaluation_id>')
def generate_report(evaluation_id):
    """生成PDF報告"""
    try:
        evaluation = data_manager.get_evaluation(evaluation_id)
        if not evaluation:
            return jsonify({
                'success': False,
                'error': '評估結果不存在'
            }), 404
        
        # 生成報告
        report_generator = ReportGenerator()
        report_path = report_generator.generate_pdf_report(evaluation, evaluation_id)
        
        # Generate filename: ProjectName_version_ddmmyyyy.pdf
        project_info = evaluation.get('project_info', {})
        project_name = project_info.get('name', 'UnknownProject').replace(' ', '_')
        version = project_info.get('version', '').strip()
        if not version:
            version = '1.0'
        version = version.replace(' ', '_')
        
        # Generate date in ddmmyyyy format
        created_at = evaluation.get('created_at', '')
        try:
            if created_at:
                date_obj = datetime.datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                date_str = date_obj.strftime('%d%m%Y')
            else:
                date_str = datetime.datetime.now().strftime('%d%m%Y')
        except:
            date_str = datetime.datetime.now().strftime('%d%m%Y')
        
        # Clean project name to remove special characters
        import re
        clean_project_name = re.sub(r'[^\w\-_]', '', project_name)[:30]  # Limit length
        clean_version = re.sub(r'[^\w\-_\.]', '', version)[:10]  # Limit length
        
        filename = f'{clean_project_name}_{clean_version}_{date_str}.pdf'
        
        return send_file(
            report_path,
            as_attachment=True,
            download_name=filename,
            mimetype='application/pdf'
        )
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/evaluation/<evaluation_id>', methods=['DELETE'])
def delete_evaluation(evaluation_id):
    """Delete evaluation"""
    try:
        # Check if evaluation exists
        evaluation = data_manager.get_evaluation(evaluation_id)
        if not evaluation:
            return jsonify({
                'success': False,
                'error': 'Evaluation not found'
            }), 404
        
        # Delete the evaluation
        success = data_manager.delete_evaluation(evaluation_id)
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Evaluation deleted successfully'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to delete evaluation'
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/health')
def health_check():
    """健康檢查"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.datetime.now().isoformat(),
        'version': '1.0.0'
    })

@app.errorhandler(404)
def not_found(error):
    """404錯誤處理"""
    return jsonify({
        'success': False,
        'error': '請求的資源不存在'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """500錯誤處理"""
    return jsonify({
        'success': False,
        'error': '伺服器內部錯誤'
    }), 500

if __name__ == '__main__':
    # Create necessary directories
    os.makedirs('data', exist_ok=True)
    os.makedirs('reports', exist_ok=True)
    
    # Start development server
    print("Starting AI Agent Usability Evaluation Tool...")
    print("Visit http://localhost:5000 to begin")
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )