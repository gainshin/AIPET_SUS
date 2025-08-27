# AI Agent 可用性評估工具 - API 文檔

## 基礎信息

- **基礎URL**: https://5000-i6tx75dds1e1esv6i13dp.e2b.dev/api
- **協議**: HTTPS  
- **數據格式**: JSON
- **字符編碼**: UTF-8

## 通用響應格式

### 成功響應
```json
{
    "success": true,
    "data": {
        // 具體數據內容
    }
}
```

### 錯誤響應
```json
{
    "success": false,
    "error": "錯誤描述信息"
}
```

## API 端點

### 1. 健康檢查

檢查服務狀態

**端點**: `GET /health`

**響應示例**:
```json
{
    "status": "healthy",
    "timestamp": "2025-08-27T14:01:50.097284",
    "version": "1.0.0"
}
```

### 2. 獲取Kano模型問題

獲取預設的Kano評估問題列表

**端點**: `GET /kano/questions`

**響應示例**:
```json
{
    "success": true,
    "questions": [
        {
            "id": "response_accuracy",
            "title": "回應準確性",
            "functional": "如果AI Agent總是能準確理解您的問題並給出正確答案，您的感受如何？",
            "dysfunctional": "如果AI Agent經常誤解您的問題或給出錯誤答案，您的感受如何？"
        }
        // ... 更多問題
    ],
    "answer_options": {
        "1": "我喜歡這樣",
        "2": "理所當然應該這樣",
        "3": "我無所謂", 
        "4": "我勉強可以接受",
        "5": "我不喜歡這樣"
    }
}
```

### 3. 獲取SUS量表問題

獲取標準SUS評估問題

**端點**: `GET /sus/questions`

**響應示例**:
```json
{
    "success": true,
    "questions": [
        {
            "id": "q1",
            "text": "我想要經常使用這個AI Agent系統",
            "positive": true
        }
        // ... 更多問題
    ],
    "likert_options": {
        "1": "強烈不同意",
        "2": "不同意",
        "3": "普通",
        "4": "同意", 
        "5": "強烈同意"
    }
}
```

### 4. 提交評估

執行完整的可用性評估

**端點**: `POST /evaluate`

**請求格式**:
```json
{
    "project_info": {
        "name": "我的AI助手",
        "description": "智能客服機器人",
        "version": "v1.0.0",
        "team": "開發團隊"
    },
    "kano_responses": {
        "response_accuracy": {
            "functional": 2,
            "dysfunctional": 5
        }
        // ... 更多回應
    },
    "sus_responses": {
        "q1": 4,
        "q2": 2,
        "q3": 4
        // ... 更多回應
    }
}
```

**響應示例**:
```json
{
    "success": true,
    "data": {
        "evaluation_id": "abc12345",
        "project_info": {
            "name": "我的AI助手",
            "description": "智能客服機器人",
            "version": "v1.0.0",
            "team": "開發團隊"
        },
        "evaluation_date": "2025-08-27T14:01:50.097284",
        "kano_evaluation": {
            "results": {
                "response_accuracy": {
                    "category": "Must-be",
                    "satisfaction_impact": 0.2,
                    "dissatisfaction_impact": 1.0,
                    "better_coefficient": 1.0,
                    "worse_coefficient": 1.0
                }
            },
            "summary": {
                "category_counts": {
                    "Must-be": 3,
                    "One-dimensional": 2,
                    "Attractive": 4,
                    "Indifferent": 1,
                    "Reverse": 0,
                    "Questionable": 0
                },
                "category_percentages": {
                    "Must-be": 30.0,
                    "One-dimensional": 20.0,
                    "Attractive": 40.0,
                    "Indifferent": 10.0,
                    "Reverse": 0.0,
                    "Questionable": 0.0
                },
                "total_questions": 10,
                "average_satisfaction_impact": 0.65,
                "average_dissatisfaction_impact": 0.45,
                "priority_features": {
                    "must_be_features": ["response_accuracy", "privacy_protection"],
                    "attractive_features": ["emotional_intelligence", "personalization"],
                    "one_dimensional_features": ["response_speed", "natural_conversation"]
                }
            },
            "recommendations": [
                {
                    "priority": "高",
                    "category": "基礎型需求",
                    "feature": "回應準確性",
                    "description": "用戶認為回應準確性是基礎需求，必須優先確保其穩定性和可靠性。",
                    "action": "立即改進並確保100%可靠性"
                }
            ]
        },
        "sus_evaluation": {
            "score": 72.5,
            "grade": "C", 
            "percentile": 65.2,
            "adjective_rating": "好",
            "acceptability": "可接受",
            "detailed_analysis": {
                "overall_result": {
                    "score": 72.5,
                    "grade": "C",
                    "percentile": 65.2,
                    "adjective_rating": "好",
                    "acceptability": "可接受"
                },
                "question_analysis": {
                    "q1": {
                        "question": "我想要經常使用這個AI Agent系統",
                        "response": 4,
                        "normalized_score": 3,
                        "performance": "優秀",
                        "is_positive": true
                    }
                },
                "improvement_suggestions": [
                    {
                        "priority": "中",
                        "area": "系統複雜性",
                        "current_score": 1,
                        "suggestion": "簡化用戶界面和交互流程，降低系統複雜度",
                        "question": "我覺得這個系統過於複雜"
                    }
                ],
                "benchmark_comparison": {
                    "your_score": 72.5,
                    "industry_average": 68.0,
                    "difference_from_average": 4.5,
                    "percentile": 65.2,
                    "better_than_percent": 65.2,
                    "benchmark_category": "中上 (前50%)"
                },
                "strengths": ["容易使用", "用戶參與度高"],
                "weaknesses": ["系統過於複雜", "需要技術支援"]
            }
        },
        "overall_assessment": {
            "overall_score": 73.8,
            "maturity_level": "良好 - 具競爭力",
            "key_strengths": ["用戶滿意度高", "具備魅力型功能"],
            "critical_issues": [],
            "priority_actions": ["提升期望型功能性能", "改善用戶界面和交互體驗"]
        }
    }
}
```

### 5. 獲取評估結果

根據評估ID獲取詳細結果

**端點**: `GET /evaluation/{evaluation_id}`

**響應**: 與評估提交時相同的數據結構

### 6. 評估記錄列表

獲取所有評估記錄

**端點**: `GET /evaluations`

**查詢參數**:
- `limit` (可選): 返回數量限制，默認50
- `offset` (可選): 偏移量，默認0

**響應示例**:
```json
{
    "success": true,
    "data": [
        {
            "id": "abc12345",
            "project_info": {
                "name": "我的AI助手",
                "description": "智能客服機器人"
            },
            "sus_evaluation": {
                "score": 72.5,
                "grade": "C"
            },
            "overall_assessment": {
                "overall_score": 73.8,
                "maturity_level": "良好 - 具競爭力"
            },
            "created_at": "2025-08-27T14:01:50.097284"
        }
    ]
}
```

### 7. 生成PDF報告

下載評估結果的PDF報告

**端點**: `GET /report/{evaluation_id}`

**響應**: PDF文件下載

**響應頭**:
```
Content-Type: application/pdf
Content-Disposition: attachment; filename="AI_Agent_評估報告_{evaluation_id}.pdf"
```

## 錯誤代碼

| 狀態碼 | 描述 | 示例 |
|--------|------|------|
| 200 | 成功 | 請求處理成功 |
| 400 | 請求錯誤 | 缺少必要參數或參數格式錯誤 |
| 404 | 資源不存在 | 評估ID不存在 |  
| 500 | 服務器錯誤 | 內部處理錯誤 |

## 數據類型說明

### Kano分類類型
- `Must-be`: 基礎型需求
- `One-dimensional`: 期望型需求  
- `Attractive`: 魅力型需求
- `Indifferent`: 無差異需求
- `Reverse`: 反向需求
- `Questionable`: 有疑問需求

### SUS評級
- `A`: 90-100分，優秀
- `B`: 80-89分，良好
- `C`: 70-79分，中等
- `D`: 60-69分，較差
- `F`: 0-59分，極差

## 使用示例

### JavaScript (Fetch API)

```javascript
// 獲取Kano問題
const getKanoQuestions = async () => {
    const response = await fetch('/api/kano/questions');
    const data = await response.json();
    return data;
};

// 提交評估
const submitEvaluation = async (evaluationData) => {
    const response = await fetch('/api/evaluate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(evaluationData)
    });
    const result = await response.json();
    return result;
};

// 下載報告
const downloadReport = async (evaluationId) => {
    const response = await fetch(`/api/report/${evaluationId}`);
    const blob = await response.blob();
    
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `AI_Agent_評估報告_${evaluationId}.pdf`;
    a.click();
    window.URL.revokeObjectURL(url);
};
```

### Python (requests)

```python
import requests
import json

# 基礎URL
BASE_URL = 'https://5000-i6tx75dds1e1esv6i13dp.e2b.dev/api'

# 獲取SUS問題
def get_sus_questions():
    response = requests.get(f'{BASE_URL}/sus/questions')
    return response.json()

# 提交評估
def submit_evaluation(evaluation_data):
    response = requests.post(
        f'{BASE_URL}/evaluate',
        headers={'Content-Type': 'application/json'},
        data=json.dumps(evaluation_data)
    )
    return response.json()

# 獲取評估記錄
def get_evaluations():
    response = requests.get(f'{BASE_URL}/evaluations')
    return response.json()
```

### cURL

```bash
# 健康檢查
curl -X GET "https://5000-i6tx75dds1e1esv6i13dp.e2b.dev/api/health"

# 獲取Kano問題
curl -X GET "https://5000-i6tx75dds1e1esv6i13dp.e2b.dev/api/kano/questions"

# 提交評估
curl -X POST "https://5000-i6tx75dds1e1esv6i13dp.e2b.dev/api/evaluate" \
  -H "Content-Type: application/json" \
  -d '{
    "project_info": {
      "name": "測試AI助手",
      "description": "用於測試的AI助手"
    },
    "kano_responses": {
      "response_accuracy": {"functional": 2, "dysfunctional": 5}
    },
    "sus_responses": {
      "q1": 4, "q2": 2, "q3": 4, "q4": 2, "q5": 4,
      "q6": 2, "q7": 4, "q8": 2, "q9": 4, "q10": 2
    }
  }'

# 下載報告
curl -X GET "https://5000-i6tx75dds1e1esv6i13dp.e2b.dev/api/report/{evaluation_id}" \
  -o "evaluation_report.pdf"
```

## 速率限制

目前未設置速率限制，但建議：
- 避免過於頻繁的請求
- 合理使用評估功能
- 批量操作時適當添加延遲

## 注意事項

1. **數據持久化**: 評估數據存儲在本地文件系統中
2. **並發處理**: 支持多用戶同時使用
3. **文件大小**: PDF報告大小通常在1-5MB之間
4. **瀏覽器兼容**: 建議使用現代瀏覽器以獲得最佳體驗
5. **網絡要求**: 需要穩定的網絡連接以確保評估過程不中斷

## 技術支援

如有API使用問題，請檢查：
1. 請求格式是否正確
2. 必要參數是否都已提供
3. 數據類型是否符合要求
4. 網絡連接是否正常