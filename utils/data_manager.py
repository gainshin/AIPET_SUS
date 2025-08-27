"""
數據管理器
處理評估結果的保存、讀取和管理
"""

import json
import os
import uuid
import datetime
from typing import Dict, List, Optional
import pandas as pd

class DataManager:
    """數據管理器"""
    
    def __init__(self, data_dir: str = 'data'):
        self.data_dir = data_dir
        self.evaluations_file = os.path.join(data_dir, 'evaluations.json')
        self._ensure_data_dir()
    
    def _ensure_data_dir(self):
        """確保數據目錄存在"""
        os.makedirs(self.data_dir, exist_ok=True)
        
        # 如果評估文件不存在，創建空文件
        if not os.path.exists(self.evaluations_file):
            with open(self.evaluations_file, 'w', encoding='utf-8') as f:
                json.dump({}, f, ensure_ascii=False, indent=2)
    
    def save_evaluation(self, evaluation_data: Dict) -> str:
        """
        保存評估結果
        
        Args:
            evaluation_data: 評估數據
            
        Returns:
            評估ID
        """
        # 生成唯一ID
        evaluation_id = str(uuid.uuid4())[:8]
        
        # 添加元數據
        evaluation_data['id'] = evaluation_id
        evaluation_data['created_at'] = datetime.datetime.now().isoformat()
        evaluation_data['updated_at'] = evaluation_data['created_at']
        
        # 讀取現有數據
        evaluations = self._load_evaluations()
        
        # 添加新評估
        evaluations[evaluation_id] = evaluation_data
        
        # 保存到文件
        with open(self.evaluations_file, 'w', encoding='utf-8') as f:
            json.dump(evaluations, f, ensure_ascii=False, indent=2)
        
        return evaluation_id
    
    def get_evaluation(self, evaluation_id: str) -> Optional[Dict]:
        """
        獲取評估結果
        
        Args:
            evaluation_id: 評估ID
            
        Returns:
            評估數據或None
        """
        evaluations = self._load_evaluations()
        return evaluations.get(evaluation_id)
    
    def update_evaluation(self, evaluation_id: str, update_data: Dict) -> bool:
        """
        更新評估結果
        
        Args:
            evaluation_id: 評估ID
            update_data: 更新數據
            
        Returns:
            是否成功
        """
        evaluations = self._load_evaluations()
        
        if evaluation_id not in evaluations:
            return False
        
        # 更新數據
        evaluations[evaluation_id].update(update_data)
        evaluations[evaluation_id]['updated_at'] = datetime.datetime.now().isoformat()
        
        # 保存到文件
        with open(self.evaluations_file, 'w', encoding='utf-8') as f:
            json.dump(evaluations, f, ensure_ascii=False, indent=2)
        
        return True
    
    def delete_evaluation(self, evaluation_id: str) -> bool:
        """
        刪除評估結果
        
        Args:
            evaluation_id: 評估ID
            
        Returns:
            是否成功
        """
        evaluations = self._load_evaluations()
        
        if evaluation_id not in evaluations:
            return False
        
        del evaluations[evaluation_id]
        
        # 保存到文件
        with open(self.evaluations_file, 'w', encoding='utf-8') as f:
            json.dump(evaluations, f, ensure_ascii=False, indent=2)
        
        return True
    
    def list_evaluations(self, limit: int = 50, offset: int = 0) -> List[Dict]:
        """
        列出評估結果
        
        Args:
            limit: 限制數量
            offset: 偏移量
            
        Returns:
            評估列表
        """
        evaluations = self._load_evaluations()
        
        # 轉換為列表並按創建時間排序
        evaluation_list = list(evaluations.values())
        evaluation_list.sort(key=lambda x: x.get('created_at', ''), reverse=True)
        
        # 分頁
        start = offset
        end = offset + limit
        
        return evaluation_list[start:end]
    
    def search_evaluations(self, query: str, field: str = 'project_name') -> List[Dict]:
        """
        搜索評估結果
        
        Args:
            query: 搜索關鍵詞
            field: 搜索字段
            
        Returns:
            匹配的評估列表
        """
        evaluations = self._load_evaluations()
        results = []
        
        for evaluation in evaluations.values():
            # 搜索項目信息
            project_info = evaluation.get('project_info', {})
            
            if field == 'project_name':
                if query.lower() in project_info.get('name', '').lower():
                    results.append(evaluation)
            elif field == 'description':
                if query.lower() in project_info.get('description', '').lower():
                    results.append(evaluation)
            elif field == 'all':
                # 在所有文本字段中搜索
                searchable_text = ' '.join([
                    project_info.get('name', ''),
                    project_info.get('description', ''),
                    project_info.get('version', ''),
                    project_info.get('team', '')
                ]).lower()
                
                if query.lower() in searchable_text:
                    results.append(evaluation)
        
        # 按創建時間排序
        results.sort(key=lambda x: x.get('created_at', ''), reverse=True)
        
        return results
    
    def get_evaluation_statistics(self) -> Dict:
        """
        獲取評估統計信息
        
        Returns:
            統計數據
        """
        evaluations = self._load_evaluations()
        
        if not evaluations:
            return {
                'total_evaluations': 0,
                'average_sus_score': 0,
                'sus_score_distribution': {},
                'kano_category_distribution': {},
                'evaluation_trend': []
            }
        
        # 提取SUS分數
        sus_scores = []
        kano_categories = []
        evaluation_dates = []
        
        for evaluation in evaluations.values():
            sus_data = evaluation.get('sus_evaluation', {})
            sus_score = sus_data.get('score', 0)
            sus_scores.append(sus_score)
            
            # 提取Kano類別
            kano_data = evaluation.get('kano_evaluation', {})
            kano_results = kano_data.get('results', {})
            for result in kano_results.values():
                category = result.get('category', 'Unknown')
                kano_categories.append(category)
            
            # 提取評估日期
            created_at = evaluation.get('created_at', '')
            if created_at:
                try:
                    date = datetime.datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                    evaluation_dates.append(date.strftime('%Y-%m'))
                except:
                    pass
        
        # 計算統計數據
        stats = {
            'total_evaluations': len(evaluations),
            'average_sus_score': sum(sus_scores) / len(sus_scores) if sus_scores else 0,
            'sus_score_distribution': self._calculate_sus_distribution(sus_scores),
            'kano_category_distribution': self._calculate_category_distribution(kano_categories),
            'evaluation_trend': self._calculate_evaluation_trend(evaluation_dates)
        }
        
        return stats
    
    def _calculate_sus_distribution(self, scores: List[float]) -> Dict:
        """計算SUS分數分佈"""
        if not scores:
            return {}
        
        ranges = [
            (90, 100, 'A (優秀)'),
            (80, 89, 'B (良好)'),
            (70, 79, 'C (中等)'),
            (60, 69, 'D (較差)'),
            (0, 59, 'F (極差)')
        ]
        
        distribution = {}
        
        for min_score, max_score, label in ranges:
            count = sum(1 for score in scores if min_score <= score <= max_score)
            percentage = (count / len(scores)) * 100 if scores else 0
            distribution[label] = {
                'count': count,
                'percentage': round(percentage, 1)
            }
        
        return distribution
    
    def _calculate_category_distribution(self, categories: List[str]) -> Dict:
        """計算Kano類別分佈"""
        if not categories:
            return {}
        
        distribution = {}
        unique_categories = set(categories)
        
        for category in unique_categories:
            count = categories.count(category)
            percentage = (count / len(categories)) * 100
            distribution[category] = {
                'count': count,
                'percentage': round(percentage, 1)
            }
        
        return distribution
    
    def _calculate_evaluation_trend(self, dates: List[str]) -> List[Dict]:
        """計算評估趨勢"""
        if not dates:
            return []
        
        # 統計每月評估數量
        monthly_counts = {}
        for date in dates:
            monthly_counts[date] = monthly_counts.get(date, 0) + 1
        
        # 轉換為列表並排序
        trend = [
            {'month': month, 'count': count}
            for month, count in sorted(monthly_counts.items())
        ]
        
        return trend
    
    def _load_evaluations(self) -> Dict:
        """加載評估數據"""
        try:
            with open(self.evaluations_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}
    
    def export_evaluations_csv(self, output_path: str = None) -> str:
        """
        導出評估數據為CSV格式
        
        Args:
            output_path: 輸出路徑
            
        Returns:
            CSV文件路徑
        """
        if output_path is None:
            timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            output_path = os.path.join(self.data_dir, f'evaluations_export_{timestamp}.csv')
        
        evaluations = self._load_evaluations()
        
        # 準備CSV數據
        csv_data = []
        
        for evaluation in evaluations.values():
            project_info = evaluation.get('project_info', {})
            sus_data = evaluation.get('sus_evaluation', {})
            kano_data = evaluation.get('kano_evaluation', {})
            overall_data = evaluation.get('overall_assessment', {})
            
            row = {
                '評估ID': evaluation.get('id', ''),
                '項目名稱': project_info.get('name', ''),
                '項目描述': project_info.get('description', ''),
                '版本': project_info.get('version', ''),
                '團隊': project_info.get('team', ''),
                '評估日期': evaluation.get('created_at', ''),
                'SUS分數': sus_data.get('score', 0),
                'SUS等級': sus_data.get('grade', ''),
                '百分位數': sus_data.get('percentile', 0),
                '形容詞評級': sus_data.get('adjective_rating', ''),
                'Acceptability': sus_data.get('acceptability', ''),
                '綜合分數': overall_data.get('overall_score', 0),
                '成熟度等級': overall_data.get('maturity_level', ''),
                'Kano平均滿意度影響': kano_data.get('summary', {}).get('average_satisfaction_impact', 0),
                'Kano平均不滿意度影響': kano_data.get('summary', {}).get('average_dissatisfaction_impact', 0)
            }
            
            csv_data.append(row)
        
        # 寫入CSV文件
        if csv_data:
            df = pd.DataFrame(csv_data)
            df.to_csv(output_path, index=False, encoding='utf-8-sig')
        
        return output_path
    
    def backup_data(self, backup_path: str = None) -> str:
        """
        備份數據
        
        Args:
            backup_path: 備份路徑
            
        Returns:
            備份文件路徑
        """
        if backup_path is None:
            timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_path = os.path.join(self.data_dir, f'backup_{timestamp}.json')
        
        evaluations = self._load_evaluations()
        
        backup_data = {
            'backup_date': datetime.datetime.now().isoformat(),
            'total_evaluations': len(evaluations),
            'evaluations': evaluations
        }
        
        with open(backup_path, 'w', encoding='utf-8') as f:
            json.dump(backup_data, f, ensure_ascii=False, indent=2)
        
        return backup_path
    
    def restore_data(self, backup_path: str) -> bool:
        """
        恢復數據
        
        Args:
            backup_path: 備份文件路徑
            
        Returns:
            是否成功
        """
        try:
            with open(backup_path, 'r', encoding='utf-8') as f:
                backup_data = json.load(f)
            
            evaluations = backup_data.get('evaluations', {})
            
            # 保存恢復的數據
            with open(self.evaluations_file, 'w', encoding='utf-8') as f:
                json.dump(evaluations, f, ensure_ascii=False, indent=2)
            
            return True
        except Exception as e:
            print(f"恢復數據時發生錯誤: {e}")
            return False