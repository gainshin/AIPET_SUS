/**
 * AI Agent 可用性評估工具 - 前端應用程式
 */

// 全局變量
let currentStep = 'welcome';
let projectInfo = {};
let kanoQuestions = [];
let susQuestions = [];
let kanoResponses = {};
let susResponses = {};
let evaluationResult = null;

// API基礎URL
const API_BASE = '/api';

// 頁面初始化
document.addEventListener('DOMContentLoaded', function() {
    showWelcome();
    loadKanoQuestions();
    loadSUSQuestions();
    
    // 綁定表單事件
    document.getElementById('projectInfoForm').addEventListener('submit', handleProjectInfoSubmit);
});

// 顯示歡迎頁面
function showWelcome() {
    hideAllSections();
    document.getElementById('welcomeSection').style.display = 'block';
    currentStep = 'welcome';
}

// 開始評估
function startEvaluation() {
    showProjectInfo();
}

// 顯示項目信息表單
function showProjectInfo() {
    hideAllSections();
    document.getElementById('projectInfoSection').style.display = 'block';
    currentStep = 'project-info';
}

// 處理項目信息提交
function handleProjectInfoSubmit(e) {
    e.preventDefault();
    
    const name = document.getElementById('projectName').value.trim();
    if (!name) {
        showAlert('請輸入項目名稱', 'warning');
        return;
    }
    
    projectInfo = {
        name: name,
        description: document.getElementById('projectDescription').value.trim(),
        version: document.getElementById('projectVersion').value.trim(),
        team: document.getElementById('projectTeam').value.trim()
    };
    
    showKanoEvaluation();
}

// 顯示Kano評估
function showKanoEvaluation() {
    hideAllSections();
    document.getElementById('kanoEvaluationSection').style.display = 'block';
    currentStep = 'kano-evaluation';
    renderKanoQuestions();
}

// 加載Kano問題
async function loadKanoQuestions() {
    try {
        const response = await fetch(`${API_BASE}/kano/questions`);
        const data = await response.json();
        
        if (data.success) {
            kanoQuestions = data.questions;
        } else {
            showAlert('加載Kano問題失敗: ' + data.error, 'error');
        }
    } catch (error) {
        showAlert('網絡錯誤: ' + error.message, 'error');
    }
}

// 渲染Kano問題
function renderKanoQuestions() {
    const container = document.getElementById('kanoQuestions');
    container.innerHTML = '';
    
    kanoQuestions.forEach((question, index) => {
        const questionDiv = document.createElement('div');
        questionDiv.className = 'question-card';
        questionDiv.innerHTML = `
            <div class="question-title">
                <i class="bi bi-patch-question"></i>
                ${index + 1}. ${question.title}
            </div>
            
            <div class="question-section">
                <h6><i class="bi bi-plus-circle text-success"></i> 功能性問題</h6>
                <p class="question-text">${question.functional}</p>
                <div class="option-group" id="functional-${question.id}">
                    ${renderKanoOptions(question.id, 'functional')}
                </div>
            </div>
            
            <div class="question-section">
                <h6><i class="bi bi-dash-circle text-danger"></i> 失功能性問題</h6>
                <p class="question-text">${question.dysfunctional}</p>
                <div class="option-group" id="dysfunctional-${question.id}">
                    ${renderKanoOptions(question.id, 'dysfunctional')}
                </div>
            </div>
        `;
        container.appendChild(questionDiv);
    });
}

// 渲染Kano選項
function renderKanoOptions(questionId, type) {
    const options = [
        { value: 1, text: '我喜歡這樣' },
        { value: 2, text: '理所當然應該這樣' },
        { value: 3, text: '我無所謂' },
        { value: 4, text: '我勉強可以接受' },
        { value: 5, text: '我不喜歡這樣' }
    ];
    
    return options.map(option => `
        <button type="button" class="option-btn" 
                onclick="selectKanoOption('${questionId}', '${type}', ${option.value}, this)">
            ${option.text}
        </button>
    `).join('');
}

// 選擇Kano選項
function selectKanoOption(questionId, type, value, element) {
    // 移除同組其他選項的選中狀態
    const group = element.parentNode;
    group.querySelectorAll('.option-btn').forEach(btn => btn.classList.remove('selected'));
    
    // 設置當前選項為選中
    element.classList.add('selected');
    
    // 保存回答
    if (!kanoResponses[questionId]) {
        kanoResponses[questionId] = {};
    }
    kanoResponses[questionId][type] = value;
    
    // 檢查進度
    updateKanoProgress();
}

// 更新Kano進度
function updateKanoProgress() {
    const totalQuestions = kanoQuestions.length * 2; // 每個問題有兩個子問題
    let answeredCount = 0;
    
    Object.values(kanoResponses).forEach(response => {
        if (response.functional !== undefined) answeredCount++;
        if (response.dysfunctional !== undefined) answeredCount++;
    });
    
    const progress = (answeredCount / totalQuestions) * 100;
    console.log(`Kano進度: ${answeredCount}/${totalQuestions} (${progress.toFixed(1)}%)`);
}

// 提交Kano評估
function submitKanoEvaluation() {
    // 檢查是否所有問題都已回答
    const incompleteQuestions = kanoQuestions.filter(q => 
        !kanoResponses[q.id] || 
        kanoResponses[q.id].functional === undefined || 
        kanoResponses[q.id].dysfunctional === undefined
    );
    
    if (incompleteQuestions.length > 0) {
        showAlert(`還有 ${incompleteQuestions.length} 個問題未完成回答`, 'warning');
        return;
    }
    
    showSUSEvaluation();
}

// 顯示SUS評估
function showSUSEvaluation() {
    hideAllSections();
    document.getElementById('susEvaluationSection').style.display = 'block';
    currentStep = 'sus-evaluation';
    renderSUSQuestions();
}

// 加載SUS問題
async function loadSUSQuestions() {
    try {
        const response = await fetch(`${API_BASE}/sus/questions`);
        const data = await response.json();
        
        if (data.success) {
            susQuestions = data.questions;
        } else {
            showAlert('加載SUS問題失敗: ' + data.error, 'error');
        }
    } catch (error) {
        showAlert('網絡錯誤: ' + error.message, 'error');
    }
}

// 渲染SUS問題
function renderSUSQuestions() {
    const container = document.getElementById('susQuestions');
    container.innerHTML = '';
    
    susQuestions.forEach((question, index) => {
        const questionDiv = document.createElement('div');
        questionDiv.className = 'question-card';
        questionDiv.innerHTML = `
            <div class="question-title">
                <i class="bi bi-speedometer2"></i>
                ${index + 1}. ${question.text}
            </div>
            <div class="sus-scale-labels">
                <span>強烈不同意</span>
                <span>不同意</span>
                <span>普通</span>
                <span>同意</span>
                <span>強烈同意</span>
            </div>
            <div class="sus-option-group" id="sus-${question.id}">
                ${renderSUSOptions(question.id)}
            </div>
        `;
        container.appendChild(questionDiv);
    });
}

// 渲染SUS選項
function renderSUSOptions(questionId) {
    return [1, 2, 3, 4, 5].map(value => `
        <button type="button" class="sus-option" 
                onclick="selectSUSOption('${questionId}', ${value}, this)">
            ${value}
        </button>
    `).join('');
}

// 選擇SUS選項
function selectSUSOption(questionId, value, element) {
    // 移除同組其他選項的選中狀態
    const group = element.parentNode;
    group.querySelectorAll('.sus-option').forEach(btn => btn.classList.remove('selected'));
    
    // 設置當前選項為選中
    element.classList.add('selected');
    
    // 保存回答
    susResponses[questionId] = value;
    
    // 檢查進度
    updateSUSProgress();
}

// 更新SUS進度
function updateSUSProgress() {
    const totalQuestions = susQuestions.length;
    const answeredCount = Object.keys(susResponses).length;
    const progress = (answeredCount / totalQuestions) * 100;
    console.log(`SUS進度: ${answeredCount}/${totalQuestions} (${progress.toFixed(1)}%)`);
}

// 提交SUS評估
async function submitSUSEvaluation() {
    // 檢查是否所有問題都已回答
    if (Object.keys(susResponses).length < susQuestions.length) {
        const unanswered = susQuestions.length - Object.keys(susResponses).length;
        showAlert(`還有 ${unanswered} 個問題未回答`, 'warning');
        return;
    }
    
    // 顯示加載動畫
    showLoading(true);
    
    try {
        // 準備評估數據
        const evaluationData = {
            project_info: projectInfo,
            kano_responses: kanoResponses,
            sus_responses: susResponses
        };
        
        // 發送評估請求
        const response = await fetch(`${API_BASE}/evaluate`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(evaluationData)
        });
        
        const result = await response.json();
        
        if (result.success) {
            evaluationResult = result.data;
            showResults();
        } else {
            showAlert('評估失敗: ' + result.error, 'error');
        }
    } catch (error) {
        showAlert('網絡錯誤: ' + error.message, 'error');
    } finally {
        showLoading(false);
    }
}

// 顯示結果
function showResults() {
    hideAllSections();
    document.getElementById('resultsSection').style.display = 'block';
    currentStep = 'results';
    renderResults();
}

// 渲染結果
function renderResults() {
    const container = document.getElementById('evaluationResults');
    const sus = evaluationResult.sus_evaluation;
    const overall = evaluationResult.overall_assessment;
    
    container.innerHTML = `
        <!-- 結果摘要 -->
        <div class="result-summary">
            <h2><i class="bi bi-trophy"></i> ${projectInfo.name} 評估結果</h2>
            <div class="row mt-4">
                <div class="col-md-6">
                    <div class="score-display">${sus.score.toFixed(1)}</div>
                    <div class="score-subtitle">SUS可用性分數</div>
                </div>
                <div class="col-md-6">
                    <div class="score-display">${overall.overall_score.toFixed(1)}</div>
                    <div class="score-subtitle">綜合評估分數</div>
                </div>
            </div>
            <div class="mt-3">
                <h4>成熟度等級: ${overall.maturity_level}</h4>
                <p>系統可接受性: ${sus.acceptability} | 用戶滿意度: ${sus.adjective_rating}</p>
            </div>
        </div>

        <!-- 詳細結果網格 -->
        <div class="result-grid">
            ${renderSUSResults(sus)}
            ${renderKanoResults(evaluationResult.kano_evaluation)}
            ${renderRecommendations(evaluationResult)}
            ${renderOverallAssessment(overall)}
        </div>
    `;
    
    // 渲染圖表
    setTimeout(() => {
        renderCharts();
    }, 100);
}

// 渲染SUS結果
function renderSUSResults(sus) {
    return `
        <div class="result-card">
            <h4><i class="bi bi-speedometer2 text-warning"></i> SUS量表分析</h4>
            <div class="mb-3">
                <div class="progress-item">
                    <div class="progress-label">
                        <span>SUS分數</span>
                        <span>${sus.score.toFixed(1)}/100</span>
                    </div>
                    <div class="progress">
                        <div class="progress-bar ${getSUSProgressColor(sus.score)}" 
                             style="width: ${sus.score}%"></div>
                    </div>
                </div>
                <div class="progress-item">
                    <div class="progress-label">
                        <span>行業排名</span>
                        <span>前${(100 - sus.percentile).toFixed(1)}%</span>
                    </div>
                    <div class="progress">
                        <div class="progress-bar bg-info" 
                             style="width: ${sus.percentile}%"></div>
                    </div>
                </div>
            </div>
            <div class="mt-3">
                <p><strong>等級:</strong> <span class="badge bg-${getGradeBadgeColor(sus.grade)}">${sus.grade}</span></p>
                <p><strong>可接受性:</strong> ${sus.acceptability}</p>
                <p><strong>用戶感受:</strong> ${sus.adjective_rating}</p>
            </div>
        </div>
    `;
}

// 渲染Kano結果
function renderKanoResults(kano) {
    const summary = kano.summary;
    const categories = summary.category_percentages;
    
    return `
        <div class="result-card">
            <h4><i class="bi bi-diagram-3 text-success"></i> Kano模型分析</h4>
            <div class="chart-container">
                <canvas id="kanoChart"></canvas>
            </div>
            <div class="mt-3">
                ${Object.entries(categories).map(([category, percentage]) => `
                    <div class="progress-item">
                        <div class="progress-label">
                            <span>${getKanoCategoryName(category)}</span>
                            <span>${percentage.toFixed(1)}%</span>
                        </div>
                        <div class="progress">
                            <div class="progress-bar ${getKanoProgressColor(category)}" 
                                 style="width: ${percentage}%"></div>
                        </div>
                    </div>
                `).join('')}
            </div>
        </div>
    `;
}

// 渲染建議
function renderRecommendations(evaluation) {
    const susRecommendations = evaluation.sus_evaluation.detailed_analysis.improvement_suggestions || [];
    const kanoRecommendations = evaluation.kano_evaluation.recommendations || [];
    
    const allRecommendations = [
        ...susRecommendations.map(r => ({...r, source: 'SUS'})),
        ...kanoRecommendations.map(r => ({...r, source: 'Kano'}))
    ].sort((a, b) => {
        const priorityOrder = {'高': 3, '中': 2, '低': 1};
        return priorityOrder[b.priority] - priorityOrder[a.priority];
    });
    
    return `
        <div class="result-card">
            <h4><i class="bi bi-lightbulb text-primary"></i> 改進建議</h4>
            <ul class="recommendation-list">
                ${allRecommendations.slice(0, 6).map(rec => `
                    <li class="recommendation-item ${rec.priority.toLowerCase()}-priority">
                        <div class="d-flex justify-content-between align-items-start mb-2">
                            <strong>${rec.area || rec.feature}</strong>
                            <span class="badge bg-${getPriorityBadgeColor(rec.priority)}">${rec.priority}優先級</span>
                        </div>
                        <p class="mb-1">${rec.suggestion || rec.description}</p>
                        ${rec.action ? `<small class="text-muted">建議行動: ${rec.action}</small>` : ''}
                    </li>
                `).join('')}
            </ul>
        </div>
    `;
}

// 渲染綜合評估
function renderOverallAssessment(overall) {
    return `
        <div class="result-card">
            <h4><i class="bi bi-graph-up text-info"></i> 綜合評估</h4>
            <div class="mb-3">
                <h5>成熟度等級</h5>
                <div class="alert alert-${getMaturityAlertColor(overall.overall_score)}">
                    <strong>${overall.maturity_level}</strong><br>
                    綜合分數: ${overall.overall_score.toFixed(1)}/100
                </div>
            </div>
            
            ${overall.key_strengths.length > 0 ? `
                <div class="mb-3">
                    <h6><i class="bi bi-check-circle text-success"></i> 關鍵優勢</h6>
                    <ul class="list-unstyled">
                        ${overall.key_strengths.map(strength => `<li>✓ ${strength}</li>`).join('')}
                    </ul>
                </div>
            ` : ''}
            
            ${overall.critical_issues.length > 0 ? `
                <div class="mb-3">
                    <h6><i class="bi bi-exclamation-triangle text-danger"></i> 關鍵問題</h6>
                    <ul class="list-unstyled">
                        ${overall.critical_issues.map(issue => `<li>⚠ ${issue}</li>`).join('')}
                    </ul>
                </div>
            ` : ''}
            
            ${overall.priority_actions.length > 0 ? `
                <div>
                    <h6><i class="bi bi-list-check text-primary"></i> 優先行動</h6>
                    <ol>
                        ${overall.priority_actions.map(action => `<li>${action}</li>`).join('')}
                    </ol>
                </div>
            ` : ''}
        </div>
    `;
}

// 渲染圖表
function renderCharts() {
    renderKanoChart();
}

// 渲染Kano圖表
function renderKanoChart() {
    const canvas = document.getElementById('kanoChart');
    if (!canvas) return;
    
    const kano = evaluationResult.kano_evaluation;
    const categories = kano.summary.category_percentages;
    
    new Chart(canvas, {
        type: 'doughnut',
        data: {
            labels: Object.keys(categories).map(getKanoCategoryName),
            datasets: [{
                data: Object.values(categories),
                backgroundColor: [
                    '#dc3545', // Must-be (紅色)
                    '#007bff', // One-dimensional (藍色)
                    '#28a745', // Attractive (綠色)
                    '#6c757d', // Indifferent (灰色)
                    '#6f42c1', // Reverse (紫色)
                    '#fd7e14'  // Questionable (橙色)
                ],
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom'
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return context.label + ': ' + context.parsed.toFixed(1) + '%';
                        }
                    }
                }
            }
        }
    });
}

// 工具函數
function getSUSProgressColor(score) {
    if (score >= 90) return 'bg-success';
    if (score >= 80) return 'bg-primary';
    if (score >= 70) return 'bg-warning';
    if (score >= 60) return 'bg-orange';
    return 'bg-danger';
}

function getGradeBadgeColor(grade) {
    const colors = { A: 'success', B: 'primary', C: 'warning', D: 'orange', F: 'danger' };
    return colors[grade] || 'secondary';
}

function getKanoCategoryName(category) {
    const names = {
        'Must-be': '基礎型',
        'One-dimensional': '期望型',
        'Attractive': '魅力型',
        'Indifferent': '無差異',
        'Reverse': '反向',
        'Questionable': '有疑問'
    };
    return names[category] || category;
}

function getKanoProgressColor(category) {
    const colors = {
        'Must-be': 'bg-danger',
        'One-dimensional': 'bg-primary',
        'Attractive': 'bg-success',
        'Indifferent': 'bg-secondary',
        'Reverse': 'bg-dark',
        'Questionable': 'bg-warning'
    };
    return colors[category] || 'bg-info';
}

function getPriorityBadgeColor(priority) {
    const colors = { '高': 'danger', '中': 'warning', '低': 'success' };
    return colors[priority] || 'secondary';
}

function getMaturityAlertColor(score) {
    if (score >= 85) return 'success';
    if (score >= 75) return 'primary';
    if (score >= 65) return 'warning';
    if (score >= 55) return 'orange';
    return 'danger';
}

// 下載報告
async function downloadReport() {
    if (!evaluationResult || !evaluationResult.evaluation_id) {
        showAlert('沒有可下載的報告', 'warning');
        return;
    }
    
    showLoading(true, '正在生成PDF報告...');
    
    try {
        const response = await fetch(`${API_BASE}/report/${evaluationResult.evaluation_id}`);
        
        if (response.ok) {
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.style.display = 'none';
            a.href = url;
            a.download = `AI_Agent_評估報告_${evaluationResult.evaluation_id}.pdf`;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
            
            showAlert('報告下載成功', 'success');
        } else {
            const error = await response.json();
            showAlert('報告生成失敗: ' + error.error, 'error');
        }
    } catch (error) {
        showAlert('網絡錯誤: ' + error.message, 'error');
    } finally {
        showLoading(false);
    }
}

// 開始新評估
function startNewEvaluation() {
    // 重置所有數據
    projectInfo = {};
    kanoResponses = {};
    susResponses = {};
    evaluationResult = null;
    currentStep = 'welcome';
    
    // 清空表單
    document.getElementById('projectInfoForm').reset();
    
    // 顯示歡迎頁面
    showWelcome();
}

// 顯示歷史記錄
async function showHistory() {
    hideAllSections();
    document.getElementById('historySection').style.display = 'block';
    currentStep = 'history';
    
    showLoading(true, '正在加載評估記錄...');
    
    try {
        const response = await fetch(`${API_BASE}/evaluations`);
        const result = await response.json();
        
        if (result.success) {
            renderHistory(result.data);
        } else {
            showAlert('加載歷史記錄失敗: ' + result.error, 'error');
        }
    } catch (error) {
        showAlert('網絡錯誤: ' + error.message, 'error');
    } finally {
        showLoading(false);
    }
}

// 這個函數已經被 renderHistoryTable 替代，保留以防向後兼容
function renderHistory(evaluations) {
    renderHistoryTable(evaluations);
}

// 查看評估詳情
async function viewEvaluation(evaluationId) {
    showLoading(true, '正在加載評估詳情...');
    
    try {
        const response = await fetch(`${API_BASE}/evaluation/${evaluationId}`);
        const result = await response.json();
        
        if (result.success) {
            evaluationResult = result.data;
            projectInfo = result.data.project_info || {};
            showResults();
        } else {
            showAlert('加載評估詳情失敗: ' + result.error, 'error');
        }
    } catch (error) {
        showAlert('網絡錯誤: ' + error.message, 'error');
    } finally {
        showLoading(false);
    }
}

// 獲取分數徽章類別
function getScoreBadgeClass(score) {
    if (!score) return 'bg-secondary';
    if (score >= 90) return 'excellent';
    if (score >= 80) return 'good';
    if (score >= 70) return 'average';
    if (score >= 60) return 'poor';
    return 'very-poor';
}

// 隱藏所有區域
function hideAllSections() {
    document.querySelectorAll('.evaluation-section, #welcomeSection').forEach(section => {
        section.style.display = 'none';
    });
}

// 顯示加載動畫
function showLoading(show, message = '處理中...') {
    const overlay = document.getElementById('loadingOverlay');
    if (show) {
        overlay.querySelector('p').textContent = message;
        overlay.style.display = 'flex';
    } else {
        overlay.style.display = 'none';
    }
}

// 顯示提示訊息
function showAlert(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type === 'error' ? 'danger' : type} alert-dismissible fade show position-fixed`;
    alertDiv.style.cssText = 'top: 20px; right: 20px; z-index: 10000; min-width: 300px;';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(alertDiv);
    
    // 自動移除提示
    setTimeout(() => {
        if (alertDiv.parentNode) {
            alertDiv.parentNode.removeChild(alertDiv);
        }
    }, 5000);
}

// 鍵盤快捷鍵支援
document.addEventListener('keydown', function(e) {
    // Ctrl+Enter 或 Cmd+Enter 快速提交當前步驟
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        e.preventDefault();
        
        switch (currentStep) {
            case 'project-info':
                document.getElementById('projectInfoForm').dispatchEvent(new Event('submit'));
                break;
            case 'kano-evaluation':
                submitKanoEvaluation();
                break;
            case 'sus-evaluation':
                submitSUSEvaluation();
                break;
        }
    }
    
    // ESC 返回上一步
    if (e.key === 'Escape') {
        e.preventDefault();
        
        switch (currentStep) {
            case 'project-info':
                showWelcome();
                break;
            case 'kano-evaluation':
                showProjectInfo();
                break;
            case 'sus-evaluation':
                showKanoEvaluation();
                break;
            case 'results':
            case 'history':
                showWelcome();
                break;
        }
    }
});