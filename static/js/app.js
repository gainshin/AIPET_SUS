/**
 * AI Agent Usability Evaluation Tool - Frontend Application
 */

// 全局變量
let currentStep = 'dashboard';
let projectInfo = {};
let kanoQuestions = [];
let susQuestions = [];
let aipetQuestions = [];
let kanoResponses = {};
let susResponses = {};
let aipetResponses = {};
let evaluationResult = null;

// API Base URL
const API_BASE = '/api';

// Page initialization
document.addEventListener('DOMContentLoaded', function() {
    showDashboard();
    loadKanoQuestions();
    loadSUSQuestions();
    loadAIPETQuestions();
    loadDashboardStats();
    
    // 綁定表單事件
    const form = document.getElementById('projectInfoForm');
    if (form) {
        form.addEventListener('submit', handleProjectInfoSubmit);
    }
    
    // Update navigation state
    updateNavigation('dashboard');
});

// Show Dashboard
function showDashboard() {
    hideAllSections();
    const dashboardSection = document.getElementById('dashboardSection');
    if (dashboardSection) {
        dashboardSection.style.display = 'block';
    }
    currentStep = 'dashboard';
    updateNavigation('dashboard');
    loadProjects();
    loadDashboardStats();
}

// Show new project form
function showNewProject() {
    hideAllSections();
    const newProjectSection = document.getElementById('newProjectSection');
    if (newProjectSection) {
        newProjectSection.style.display = 'block';
    }
    currentStep = 'new-project';
    updateNavigation('new-project');
}

// Update navigation state
function updateNavigation(activeItem) {
    document.querySelectorAll('.nav-item').forEach(item => {
        item.classList.remove('active');
    });
    
    const navItems = document.querySelectorAll('.nav-item');
    const navMapping = {
        'dashboard': 0,
        'new-project': 1,
        'history': 2
    };
    
    if (navMapping[activeItem] !== undefined && navItems[navMapping[activeItem]]) {
        navItems[navMapping[activeItem]].classList.add('active');
    }
}

// Handle project info submission
function handleProjectInfoSubmit(e) {
    e.preventDefault();
    
    const name = document.getElementById('projectName').value.trim();
    if (!name) {
        showAlert('Please enter project name', 'warning');
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

// Show Kano evaluation
function showKanoEvaluation() {
    hideAllSections();
    document.getElementById('kanoEvaluationSection').style.display = 'block';
    currentStep = 'kano-evaluation';
    renderKanoQuestions();
}

// Load Kano questions
async function loadKanoQuestions() {
    try {
        const response = await fetch(`${API_BASE}/kano/questions`);
        const data = await response.json();
        
        if (data.success) {
            kanoQuestions = data.questions;
        } else {
            showAlert('Failed to load Kano questions: ' + data.error, 'error');
        }
    } catch (error) {
        showAlert('Network error: ' + error.message, 'error');
    }
}

// Render Kano questions
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
                <h6><i class="bi bi-plus-circle text-success"></i> Functional Question</h6>
                <p class="question-text">${question.functional}</p>
                <div class="option-group" id="functional-${question.id}">
                    ${renderKanoOptions(question.id, 'functional')}
                </div>
            </div>
            
            <div class="question-section">
                <h6><i class="bi bi-dash-circle text-danger"></i> Dysfunctional Question</h6>
                <p class="question-text">${question.dysfunctional}</p>
                <div class="option-group" id="dysfunctional-${question.id}">
                    ${renderKanoOptions(question.id, 'dysfunctional')}
                </div>
            </div>
        `;
        container.appendChild(questionDiv);
    });
}

// Render Kano options
function renderKanoOptions(questionId, type) {
    const options = [
        { value: 1, text: 'I like it that way' },
        { value: 2, text: 'It must be that way' },
        { value: 3, text: 'I am neutral' },
        { value: 4, text: 'I can live with it that way' },
        { value: 5, text: 'I dislike it that way' }
    ];
    
    return options.map(option => `
        <button type="button" class="option-btn" 
                onclick="selectKanoOption('${questionId}', '${type}', ${option.value}, this)">
            ${option.text}
        </button>
    `).join('');
}

// Select Kano option
function selectKanoOption(questionId, type, value, element) {
    // Remove selected state from other options in the same group
    const group = element.parentNode;
    group.querySelectorAll('.option-btn').forEach(btn => btn.classList.remove('selected'));
    
    // Set current option as selected
    element.classList.add('selected');
    
    // Save response
    if (!kanoResponses[questionId]) {
        kanoResponses[questionId] = {};
    }
    kanoResponses[questionId][type] = value;
    
    // Check progress
    updateKanoProgress();
}

// Update Kano progress
function updateKanoProgress() {
    const totalQuestions = kanoQuestions.length * 2; // Each question has two sub-questions
    let answeredCount = 0;
    
    Object.values(kanoResponses).forEach(response => {
        if (response.functional !== undefined) answeredCount++;
        if (response.dysfunctional !== undefined) answeredCount++;
    });
    
    const progress = (answeredCount / totalQuestions) * 100;
    console.log(`Kano progress: ${answeredCount}/${totalQuestions} (${progress.toFixed(1)}%)`);
}

// Submit Kano evaluation
function submitKanoEvaluation() {
    // 檢查是否所有問題都已回答
    const incompleteQuestions = kanoQuestions.filter(q => 
        !kanoResponses[q.id] || 
        kanoResponses[q.id].functional === undefined || 
        kanoResponses[q.id].dysfunctional === undefined
    );
    
    if (incompleteQuestions.length > 0) {
        showAlert(`${incompleteQuestions.length} questions are still incomplete`, 'warning');
        return;
    }
    
    showSUSEvaluation();
}

// Show SUS evaluation
function showSUSEvaluation() {
    hideAllSections();
    const susSection = document.getElementById('susEvaluationSection');
    if (susSection) {
        susSection.style.display = 'block';
    }
    currentStep = 'sus-evaluation';
    renderSUSQuestions();
}

// Load SUS questions
async function loadSUSQuestions() {
    try {
        const response = await fetch(`${API_BASE}/sus/questions`);
        const data = await response.json();
        
        if (data.success) {
            susQuestions = data.questions;
        } else {
            showAlert('Failed to load SUS questions: ' + data.error, 'error');
        }
    } catch (error) {
        showAlert('Network error: ' + error.message, 'error');
    }
}

// Load AIPET questions
async function loadAIPETQuestions() {
    try {
        const response = await fetch(`${API_BASE}/aipet/questions`);
        const data = await response.json();
        
        if (data.success) {
            aipetQuestions = data.questions;
        } else {
            showAlert('Failed to load AIPET questions: ' + data.error, 'error');
        }
    } catch (error) {
        showAlert('Network error: ' + error.message, 'error');
    }
}

// Render AIPET questions
function renderAIPETQuestions() {
    const container = document.getElementById('aipetQuestions');
    if (!container) return;
    
    container.innerHTML = '';
    
    // Filter AIPET questions based on Kano responses
    // Only show AIPET questions where corresponding Kano response is "neutral" (value 3)
    const conditionalQuestions = aipetQuestions.filter(question => {
        const kanoQuestionId = question.kano_question_id;
        const kanoResponse = kanoResponses[kanoQuestionId];
        
        // Show question if either functional or dysfunctional response is neutral (3)
        return kanoResponse && (kanoResponse.functional === 3 || kanoResponse.dysfunctional === 3);
    });
    
    if (conditionalQuestions.length === 0) {
        container.innerHTML = `
            <div class="alert alert-info">
                <i class="bi bi-info-circle"></i>
                <strong>No AIPET Questions Available</strong><br>
                AIPET questions appear only when you select "I am neutral" for corresponding Kano Model questions. 
                Your responses indicate clear preferences, which means no additional deep-dive questions are needed at this time.
            </div>
        `;
        return;
    }
    
    // Group questions by dimension for better organization
    const dimensionGroups = {
        'A': { name: 'Agency', questions: [] },
        'I': { name: 'Interaction', questions: [] },
        'P': { name: 'Privacy', questions: [] },
        'E': { name: 'Experience', questions: [] },
        'T': { name: 'Trust', questions: [] }
    };
    
    conditionalQuestions.forEach(question => {
        dimensionGroups[question.dimension].questions.push(question);
    });
    
    // Add introduction text
    const introDiv = document.createElement('div');
    introDiv.className = 'alert alert-primary mb-4';
    introDiv.innerHTML = `
        <i class="bi bi-lightbulb"></i>
        <strong>Personalized AIPET Questions</strong><br>
        These questions appear because you selected "I am neutral" for related features. Your insights will help us understand your specific needs and preferences for AI agent interaction design.
    `;
    container.appendChild(introDiv);
    
    // Render each dimension group
    Object.keys(dimensionGroups).forEach(dimension => {
        const group = dimensionGroups[dimension];
        if (group.questions.length === 0) return;
        
        const dimensionDiv = document.createElement('div');
        dimensionDiv.className = 'aipet-dimension-group';
        dimensionDiv.innerHTML = `
            <div class="dimension-header">
                <h5><i class="bi bi-tag"></i> ${group.name}</h5>
            </div>
        `;
        
        group.questions.forEach((question, index) => {
            const kanoQuestionId = question.kano_question_id;
            const kanoResponse = kanoResponses[kanoQuestionId];
            
            // Determine which Kano response triggered this question
            let triggerReason = '';
            if (kanoResponse.functional === 3 && kanoResponse.dysfunctional === 3) {
                triggerReason = 'Both functional and dysfunctional responses were neutral';
            } else if (kanoResponse.functional === 3) {
                triggerReason = 'Functional response was neutral';
            } else if (kanoResponse.dysfunctional === 3) {
                triggerReason = 'Dysfunctional response was neutral';
            }
            
            const questionDiv = document.createElement('div');
            questionDiv.className = 'question-card aipet-question';
            questionDiv.innerHTML = `
                <div class="question-title">
                    <i class="bi bi-chat-dots"></i>
                    ${question.text}
                </div>
                <div class="question-meta">
                    <small class="text-muted">
                        Category: ${question.sub_category} | 
                        Triggered by: ${triggerReason} | Optional
                    </small>
                </div>
                <div class="aipet-textarea-wrapper">
                    <textarea 
                        id="aipet-${question.id}" 
                        class="aipet-textarea" 
                        placeholder="Share your thoughts here... This question appeared because you were neutral about this feature."
                        rows="4"
                        onchange="updateAIPETResponse('${question.id}', this.value)"
                    ></textarea>
                    <div class="textarea-helper">
                        <small class="text-muted">Help us understand your specific preferences and requirements</small>
                    </div>
                </div>
            `;
            dimensionDiv.appendChild(questionDiv);
        });
        
        container.appendChild(dimensionDiv);
    });
    
    // Add progress indicator
    const progressDiv = document.createElement('div');
    progressDiv.className = 'aipet-progress mt-3';
    progressDiv.innerHTML = `
        <div class="d-flex justify-content-between align-items-center">
            <span id="aipetProgress">0 of ${conditionalQuestions.length} questions answered</span>
            <span class="text-muted">Complete as many as you'd like</span>
        </div>
    `;
    container.appendChild(progressDiv);
}

// Update AIPET response
function updateAIPETResponse(questionId, value) {
    if (value && value.trim()) {
        aipetResponses[questionId] = value.trim();
    } else {
        delete aipetResponses[questionId];
    }
    
    // Update progress
    updateAIPETProgress();
}

// Update AIPET progress indicator
function updateAIPETProgress() {
    const progressElement = document.getElementById('aipetProgress');
    if (progressElement) {
        // Calculate available questions based on Kano responses
        const conditionalQuestions = aipetQuestions.filter(question => {
            const kanoQuestionId = question.kano_question_id;
            const kanoResponse = kanoResponses[kanoQuestionId];
            return kanoResponse && (kanoResponse.functional === 3 || kanoResponse.dysfunctional === 3);
        });
        
        const answered = Object.keys(aipetResponses).length;
        const total = conditionalQuestions.length;
        progressElement.textContent = `${answered} of ${total} questions answered`;
    }
}

// Render SUS questions
function renderSUSQuestions() {
    const container = document.getElementById('susQuestions');
    if (!container) return;
    
    container.innerHTML = '';
    
    susQuestions.forEach((question, index) => {
        const questionDiv = document.createElement('div');
        questionDiv.className = 'question-card';
        questionDiv.innerHTML = `
            <div class="question-title">
                <i class="bi bi-speedometer2"></i>
                ${index + 1}. ${question.text}
            </div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 5px; font-size: 12px; color: #6c757d;">
                <span>Strongly Disagree</span>
                <span>Disagree</span>
                <span>Neutral</span>
                <span>Agree</span>
                <span>Strongly Agree</span>
            </div>
            <div class="option-group" id="sus-${question.id}">
                ${renderSUSOptions(question.id)}
            </div>
        `;
        container.appendChild(questionDiv);
    });
}

// Render SUS options
function renderSUSOptions(questionId) {
    return [1, 2, 3, 4, 5].map(value => `
        <button type="button" class="option-btn" 
                onclick="selectSUSOption('${questionId}', ${value}, this)">
            ${value}
        </button>
    `).join('');
}

// Select SUS option
function selectSUSOption(questionId, value, element) {
    // Remove selected state from other options in the same group
    const group = element.parentNode;
    group.querySelectorAll('.option-btn').forEach(btn => btn.classList.remove('selected'));
    
    // Set current option as selected
    element.classList.add('selected');
    
    // Save response
    susResponses[questionId] = value;
    
    // Check progress
    updateSUSProgress();
}

// Update SUS progress
function updateSUSProgress() {
    const totalQuestions = susQuestions.length;
    const answeredCount = Object.keys(susResponses).length;
    const progress = (answeredCount / totalQuestions) * 100;
    console.log(`SUS progress: ${answeredCount}/${totalQuestions} (${progress.toFixed(1)}%)`);
}

// Submit SUS evaluation
async function submitSUSEvaluation() {
    // 檢查是否所有問題都已回答
    if (Object.keys(susResponses).length < susQuestions.length) {
        const unanswered = susQuestions.length - Object.keys(susResponses).length;
        showAlert(`${unanswered} questions remain unanswered`, 'warning');
        return;
    }
    
    // Instead of submitting immediately, go to AIPET questions
    showAIPETQuestions();
}

// Show AIPET Questions section
function showAIPETQuestions() {
    hideAllSections();
    const aipetSection = document.getElementById('aipetQuestionsSection');
    if (aipetSection) {
        aipetSection.style.display = 'block';
        renderAIPETQuestions();
        currentStep = 'aipet-questions';
        updateNavigation('new-project'); // Keep new-project nav active
    }
}

// Skip AIPET questions and go directly to results
function skipAIPETQuestions() {
    submitFinalEvaluation();
}

// Submit AIPET responses and complete evaluation
function submitAIPETResponses() {
    submitFinalEvaluation();
}

// Submit final evaluation with all data
async function submitFinalEvaluation() {
    // Show loading animation
    showLoading(true);
    
    try {
        // Prepare evaluation data
        const evaluationData = {
            project_info: projectInfo,
            kano_responses: kanoResponses,
            sus_responses: susResponses,
            aipet_responses: aipetResponses
        };
        
        // Send evaluation request
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
            showAlert('Evaluation failed: ' + result.error, 'error');
        }
    } catch (error) {
        showAlert('Network error: ' + error.message, 'error');
    } finally {
        showLoading(false);
    }
}

// Show results
function showResults() {
    hideAllSections();
    document.getElementById('resultsSection').style.display = 'block';
    currentStep = 'results';
    renderResults();
}

// Render results
function renderResults() {
    const container = document.getElementById('evaluationResults');
    const sus = evaluationResult.sus_evaluation;
    const overall = evaluationResult.overall_assessment;
    
    container.innerHTML = `
        <!-- Results Summary -->
        <div class="result-summary">
            <h2><i class="bi bi-trophy"></i> ${projectInfo.name} Assessment Results</h2>
            <div class="row mt-4">
                <div class="col-md-6">
                    <div class="score-display">${sus.score.toFixed(1)}</div>
                    <div class="score-subtitle">SUS Usability Score</div>
                </div>
                <div class="col-md-6">
                    <div class="score-display">${overall.overall_score.toFixed(1)}</div>
                    <div class="score-subtitle">Overall Assessment Score</div>
                </div>
            </div>
            <div class="mt-3">
                <h4>Maturity Level: ${overall.maturity_level}</h4>
                <p>System Acceptability: ${sus.acceptability} | User Satisfaction: ${sus.adjective_rating}</p>
            </div>
        </div>

        <!-- Detailed Results Grid -->
        <div class="result-grid">
            ${renderSUSResults(sus)}
            ${renderKanoResults(evaluationResult.kano_evaluation)}
            ${evaluationResult.aipet_evaluation ? renderAIPETResults(evaluationResult.aipet_evaluation) : ''}
            ${renderRecommendations(evaluationResult)}
            ${renderOverallAssessment(overall)}
        </div>
    `;
    
    // 渲染圖表
    setTimeout(() => {
        renderCharts();
    }, 100);
}

// Render SUS results
function renderSUSResults(sus) {
    return `
        <div class="result-card">
            <h4><i class="bi bi-speedometer2 text-warning"></i> SUS Scale Analysis</h4>
            <div class="mb-3">
                <div class="progress-item">
                    <div class="progress-label">
                        <span>SUS Score</span>
                        <span>${sus.score.toFixed(1)}/100</span>
                    </div>
                    <div class="progress">
                        <div class="progress-bar ${getSUSProgressColor(sus.score)}" 
                             style="width: ${sus.score}%"></div>
                    </div>
                </div>

            </div>
            <div class="mt-3">
                <p><strong>Grade:</strong> <span class="badge bg-${getGradeBadgeColor(sus.grade)}">${sus.grade}</span></p>
                <p><strong>Acceptability:</strong> ${sus.acceptability}</p>
                <p><strong>User Rating:</strong> ${sus.adjective_rating}</p>
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
            <h4><i class="bi bi-diagram-3 text-success"></i> Kano Model Matrix Analysis</h4>
            <p class="text-muted mb-3">
                <small>Bubble size represents category proportion, position reflects relationship between implementation level and satisfaction impact</small>
            </p>
            <div class="chart-container" style="height: 400px;">
                <canvas id="kanoChart"></canvas>
            </div>
            <div class="mt-3">
                <h6>Category Distribution Statistics</h6>
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
            <div class="mt-3">
                <small class="text-muted">
                    <strong>Interpretation Guide:</strong><br>
                    • <strong>Must-be:</strong> Essential features that cause dissatisfaction when missing<br>
                    • <strong>One-dimensional:</strong> Performance features where more is better<br>
                    • <strong>Attractive:</strong> Delighter features that greatly boost satisfaction<br>
                    • <strong>Indifferent:</strong> Features with minimal impact on satisfaction
                </small>
            </div>
        </div>
    `;
}

// Render AIPET Results
function renderAIPETResults(aipet) {
    const analysis = aipet.analysis;
    const completionRate = analysis.completion_rate;
    
    if (completionRate === 0) {
        return `
            <div class="result-card">
                <h4><i class="bi bi-chat-dots text-purple"></i> AIPET Insights</h4>
                <div class="alert alert-info">
                    <i class="bi bi-info-circle"></i>
                    No AIPET responses were provided. Consider filling out the open-ended questions in future evaluations for personalized Agentive UX insights.
                </div>
            </div>
        `;
    }
    
    return `
        <div class="result-card">
            <h4><i class="bi bi-chat-dots text-purple"></i> AIPET Framework Insights</h4>
            <p class="text-muted mb-3">
                <small>Responses analyzed through the AIPET framework for Agentive UX design</small>
            </p>
            
            <div class="mb-4">
                <div class="progress-item">
                    <div class="progress-label">
                        <span>Participation Rate</span>
                        <span>${analysis.answered_questions}/${analysis.total_questions} questions (${completionRate.toFixed(1)}%)</span>
                    </div>
                    <div class="progress">
                        <div class="progress-bar bg-purple" style="width: ${completionRate}%"></div>
                    </div>
                </div>
            </div>
            
            <div class="dimension-coverage">
                ${Object.entries(analysis.dimension_coverage).map(([dim, data]) => `
                    <div class="coverage-item">
                        <div class="coverage-percentage">${data.percentage.toFixed(0)}%</div>
                        <div class="coverage-label">${dim} - ${data.name.split('(')[0].trim()}</div>
                        <div class="text-muted" style="font-size: 11px;">${data.answered}/${data.total} questions</div>
                    </div>
                `).join('')}
            </div>
            
            ${analysis.insights.length > 0 ? `
                <div class="aipet-insights mt-4">
                    <h6>Key Insights</h6>
                    ${analysis.insights.map(insight => `
                        <div class="insight-card ${insight.type}">
                            <div class="insight-title">
                                <i class="bi bi-${getInsightIcon(insight.type)}"></i>
                                ${insight.title}
                            </div>
                            <p class="mb-0">${insight.description}</p>
                        </div>
                    `).join('')}
                </div>
            ` : ''}
            
            <div class="mt-3">
                <small class="text-muted">
                    <strong>AIPET Framework:</strong> Agency (A), Interaction (I), Privacy (P), Experience (E), Trust (T)<br>
                    These insights help guide the transition from traditional UI design to Agentive UX design.
                </small>
            </div>
        </div>
    `;
}

// Helper function for AIPET insight icons
function getInsightIcon(type) {
    switch (type) {
        case 'positive': return 'check-circle';
        case 'neutral': return 'info-circle';
        case 'suggestion': return 'lightbulb';
        default: return 'chat-dots';
    }
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
            <h4><i class="bi bi-lightbulb text-primary"></i> Improvement Recommendations</h4>
            <ul class="recommendation-list">
                ${allRecommendations.slice(0, 6).map(rec => `
                    <li class="recommendation-item ${rec.priority.toLowerCase()}-priority">
                        <div class="d-flex justify-content-between align-items-start mb-2">
                            <strong>${rec.area || rec.feature}</strong>
                            <span class="badge bg-${getPriorityBadgeColor(rec.priority)}">${rec.priority}優先級</span>
                        </div>
                        <p class="mb-1">${rec.suggestion || rec.description}</p>
                        ${rec.action ? `<small class="text-muted">Recommended Action: ${rec.action}</small>` : ''}
                    </li>
                `).join('')}
            </ul>
        </div>
    `;
}

// Render overall assessment
function renderOverallAssessment(overall) {
    return `
        <div class="result-card">
            <h4><i class="bi bi-graph-up text-info"></i> Overall Assessment</h4>
            <div class="mb-3">
                <h5>Maturity Level</h5>
                <div class="alert alert-${getMaturityAlertColor(overall.overall_score)}">
                    <strong>${overall.maturity_level}</strong><br>
                    Overall Score: ${overall.overall_score.toFixed(1)}/100
                </div>
            </div>
            
            ${overall.key_strengths.length > 0 ? `
                <div class="mb-3">
                    <h6><i class="bi bi-check-circle text-success"></i> Key Strengths</h6>
                    <ul class="list-unstyled">
                        ${overall.key_strengths.map(strength => `<li>✓ ${strength}</li>`).join('')}
                    </ul>
                </div>
            ` : ''}
            
            ${overall.critical_issues.length > 0 ? `
                <div class="mb-3">
                    <h6><i class="bi bi-exclamation-triangle text-danger"></i> Critical Issues</h6>
                    <ul class="list-unstyled">
                        ${overall.critical_issues.map(issue => `<li>⚠ ${issue}</li>`).join('')}
                    </ul>
                </div>
            ` : ''}
            
            ${overall.priority_actions.length > 0 ? `
                <div>
                    <h6><i class="bi bi-list-check text-primary"></i> Priority Actions</h6>
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
    const results = kano.results || {};
    
    // Prepare scatter plot data
    const scatterData = [];
    const categoryColors = {
        'Must-be': '#dc3545',
        'One-dimensional': '#007bff', 
        'Attractive': '#28a745',
        'Indifferent': '#6c757d',
        'Reverse': '#6f42c1',
        'Questionable': '#fd7e14'
    };
    
    // 為每個類別創建數據點
    Object.entries(categories).forEach(([category, percentage]) => {
        if (percentage > 0) {
            // 根據類別設置在矩陣中的位置
            let x, y;
            switch(category) {
                case 'Must-be':
                    x = 0.8; y = 0.2; // 右下：高實現度，低滿意度變化
                    break;
                case 'One-dimensional':
                    x = 0.8; y = 0.8; // 右上：高實現度，高滿意度
                    break;
                case 'Attractive':
                    x = 0.2; y = 0.8; // 左上：低實現度，高滿意度變化
                    break;
                case 'Indifferent':
                    x = 0.5; y = 0.2; // 中下：中等實現度，低滿意度變化
                    break;
                case 'Reverse':
                    x = 0.2; y = 0.2; // 左下：低實現度，低滿意度
                    break;
                case 'Questionable':
                    x = 0.5; y = 0.5; // 中心：需要重新評估
                    break;
                default:
                    x = 0.5; y = 0.5;
            }
            
            scatterData.push({
                x: x,
                y: y,
                r: Math.sqrt(percentage) * 3, // Bubble size reflects proportion
                category: category,
                percentage: percentage
            });
        }
    });
    
    new Chart(canvas, {
        type: 'scatter',
        data: {
            datasets: scatterData.map(point => ({
                label: getKanoCategoryName(point.category),
                data: [{
                    x: point.x,
                    y: point.y,
                    r: point.r
                }],
                backgroundColor: categoryColors[point.category] + '80', // 半透明
                borderColor: categoryColors[point.category],
                borderWidth: 2,
                pointRadius: point.r,
                showLine: false
            }))
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: {
                    type: 'linear',
                    position: 'bottom',
                    min: 0,
                    max: 1,
                    title: {
                        display: true,
                        text: 'Implementation Level (Well Implemented)',
                        font: { size: 12 }
                    },
                    grid: {
                        display: true,
                        color: '#e9ecef'
                    },
                    ticks: {
                        callback: function(value) {
                            if (value === 0) return '低';
                            if (value === 0.5) return '中';
                            if (value === 1) return '高';
                            return '';
                        }
                    }
                },
                y: {
                    min: 0,
                    max: 1,
                    title: {
                        display: true,
                        text: 'Satisfaction Impact (High Satisfaction)',
                        font: { size: 12 }
                    },
                    grid: {
                        display: true,
                        color: '#e9ecef'
                    },
                    ticks: {
                        callback: function(value) {
                            if (value === 0) return '低';
                            if (value === 0.5) return '中'; 
                            if (value === 1) return '高';
                            return '';
                        }
                    }
                }
            },
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        usePointStyle: true,
                        padding: 15,
                        font: { size: 11 }
                    }
                },
                tooltip: {
                    callbacks: {
                        title: function() {
                            return 'Kano 模型分析';
                        },
                        label: function(context) {
                            const dataset = context.dataset;
                            const point = scatterData.find(p => 
                                getKanoCategoryName(p.category) === dataset.label
                            );
                            return `${dataset.label}: ${point?.percentage.toFixed(1)}%`;
                        }
                    }
                },
                annotation: {
                    annotations: {
                        // 添加象限分割線
                        line1: {
                            type: 'line',
                            xMin: 0.5,
                            xMax: 0.5,
                            yMin: 0,
                            yMax: 1,
                            borderColor: '#dee2e6',
                            borderWidth: 1,
                            borderDash: [5, 5]
                        },
                        line2: {
                            type: 'line',
                            xMin: 0,
                            xMax: 1,
                            yMin: 0.5,
                            yMax: 0.5,
                            borderColor: '#dee2e6',
                            borderWidth: 1,
                            borderDash: [5, 5]
                        }
                    }
                }
            },
            elements: {
                point: {
                    hoverRadius: 8
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
        'Must-be': 'Must-be',
        'One-dimensional': 'One-dimensional',
        'Attractive': 'Attractive',
        'Indifferent': 'Indifferent',
        'Reverse': 'Reverse',
        'Questionable': 'Questionable'
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
        showAlert('No report available for download', 'warning');
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
            
            showAlert('Report downloaded successfully', 'success');
        } else {
            const error = await response.json();
            showAlert('Report generation failed: ' + error.error, 'error');
        }
    } catch (error) {
        showAlert('Network error: ' + error.message, 'error');
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
    
    // Clear form
    document.getElementById('projectInfoForm').reset();
    
    // 顯示歡迎頁面
    showWelcome();
}

// 顯示歷史記錄
async function showHistory() {
    hideAllSections();
    const historySection = document.getElementById('historySection');
    if (historySection) {
        historySection.style.display = 'block';
    }
    currentStep = 'history';
    updateNavigation('history');
    
    showLoading(true, 'Loading evaluation records...');
    
    try {
        const response = await fetch(`${API_BASE}/evaluations`);
        const result = await response.json();
        
        if (result.success) {
            renderHistory(result.data);
        } else {
            showAlert('Failed to load history: ' + result.error, 'error');
        }
    } catch (error) {
        showAlert('Network error: ' + error.message, 'error');
    } finally {
        showLoading(false);
    }
}

// This function has been replaced by renderHistoryTable, kept for backwards compatibility
function renderHistory(evaluations) {
    renderHistoryTable(evaluations);
}

// 查看評估詳情
async function viewEvaluation(evaluationId) {
    showLoading(true, 'Loading evaluation details...');
    
    try {
        const response = await fetch(`${API_BASE}/evaluation/${evaluationId}`);
        const result = await response.json();
        
        if (result.success) {
            evaluationResult = result.data;
            projectInfo = result.data.project_info || {};
            showResults();
        } else {
            showAlert('Failed to load evaluation details: ' + result.error, 'error');
        }
    } catch (error) {
        showAlert('Network error: ' + error.message, 'error');
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
    document.querySelectorAll('.dashboard-section').forEach(section => {
        section.style.display = 'none';
    });
}

// 加載Dashboard統計數據
async function loadDashboardStats() {
    try {
        const response = await fetch(`${API_BASE}/evaluations`);
        const result = await response.json();
        
        if (result.success) {
            const evaluations = result.data;
            const totalAssessments = evaluations.length;
            
            // 計算平均SUS分數
            let totalSUS = 0;
            let validScores = 0;
            evaluations.forEach(evaluation => {
                const susScore = evaluation.sus_evaluation?.score;
                if (susScore && susScore > 0) {
                    totalSUS += susScore;
                    validScores++;
                }
            });
            
            const avgSUS = validScores > 0 ? (totalSUS / validScores).toFixed(1) : 'N/A';
            
            // 更新統計卡片
            const totalElement = document.getElementById('totalAssessments');
            const avgElement = document.getElementById('avgSusScore');
            const activeElement = document.getElementById('activeProjects');
            
            if (totalElement) totalElement.textContent = totalAssessments;
            if (avgElement) avgElement.textContent = avgSUS;
            if (activeElement) {
                const uniqueProjects = new Set(evaluations.map(e => e.project_info?.name || 'Unknown')).size;
                activeElement.textContent = Math.max(uniqueProjects, 1);
            }
        }
    } catch (error) {
        console.error('Failed to load statistics:', error);
    }
}

// 加載項目列表
async function loadProjects() {
    try {
        const response = await fetch(`${API_BASE}/evaluations`);
        const result = await response.json();
        
        if (result.success) {
            renderProjectsTable(result.data);
        }
    } catch (error) {
        console.error('Failed to load projects:', error);
    }
}

// 渲染項目表格
function renderProjectsTable(evaluations) {
    const tbody = document.getElementById('projectsTableBody');
    if (!tbody) return;
    
    if (!evaluations || evaluations.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="4" style="text-align: center; padding: 40px; color: #6B7280;">
                    <i class="bi bi-inbox" style="font-size: 48px; display: block; margin-bottom: 16px;"></i>
                    No projects yet. Create your first AI agent assessment!
                </td>
            </tr>
        `;
        return;
    }
    
    // 按項目名稱分組
    const projectGroups = {};
    evaluations.forEach(evaluation => {
        const projectName = evaluation.project_info?.name || 'Unnamed Project';
        if (!projectGroups[projectName]) {
            projectGroups[projectName] = [];
        }
        projectGroups[projectName].push(evaluation);
    });
    
    tbody.innerHTML = Object.entries(projectGroups).map(([projectName, projectEvals]) => {
        const latestEval = projectEvals[0]; // 最新的評估
        const createdDate = new Date(latestEval.created_at).toLocaleDateString();
        const assessmentCount = projectEvals.length;
        
        return `
            <tr>
                <td>
                    <strong>${projectName}</strong><br>
                    <small style="color: #6B7280;">${latestEval.project_info?.description || 'No description'}</small>
                </td>
                <td>${createdDate}</td>
                <td>${assessmentCount}</td>
                <td>
                    <div class="project-actions">
                        <button class="action-btn" onclick="viewProject('${latestEval.id}')" title="View Details">
                            <i class="bi bi-graph-up"></i>
                        </button>
                        <button class="action-btn" onclick="shareProject('${latestEval.id}')" title="Share">
                            <i class="bi bi-share"></i>
                        </button>
                        <button class="action-btn" onclick="downloadReport('${latestEval.id}')" title="Download Report">
                            <i class="bi bi-download"></i>
                        </button>
                    </div>
                </td>
            </tr>
        `;
    }).join('');
}

// 查看項目詳情
function viewProject(evaluationId) {
    viewEvaluation(evaluationId);
}

// 分享項目
function shareProject(evaluationId) {
    const url = `${window.location.origin}?eval=${evaluationId}`;
    if (navigator.share) {
        navigator.share({
            title: 'AI Agent Assessment Results',
            url: url
        });
    } else {
        navigator.clipboard.writeText(url).then(() => {
            showAlert('Link copied to clipboard', 'success');
        });
    }
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
            case 'new-project':
                showDashboard();
                break;
            case 'kano-evaluation':
                showNewProject();
                break;
            case 'sus-evaluation':
                showKanoEvaluation();
                break;
            case 'results':
            case 'history':
                showDashboard();
                break;
        }
    }
});

// 顯示設置頁面 (placeholder)
function showSettings() {
    showAlert('Settings feature under development...', 'info');
}

// 渲染歷史記錄表格
function renderHistoryTable(evaluations) {
    const tbody = document.getElementById('historyTableBody');
    if (!tbody) return;
    
    if (!evaluations || evaluations.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="5" style="text-align: center; padding: 40px; color: #6B7280;">
                    <i class="bi bi-inbox" style="font-size: 48px; display: block; margin-bottom: 16px;"></i>
                    No assessment history available
                </td>
            </tr>
        `;
        return;
    }
    
    tbody.innerHTML = evaluations.map(evaluation => {
        const createdDate = new Date(evaluation.created_at).toLocaleDateString();
        const susScore = evaluation.sus_evaluation?.score || 'N/A';
        const overallScore = evaluation.overall_assessment?.overall_score || 'N/A';
        
        return `
            <tr>
                <td>
                    <strong>${evaluation.project_info?.name || 'Unnamed Project'}</strong><br>
                    <small style="color: #6B7280;">${evaluation.project_info?.description || 'No description'}</small>
                </td>
                <td>${createdDate}</td>
                <td><span class="badge ${getScoreBadgeClass(susScore)}">${typeof susScore === 'number' ? susScore.toFixed(1) : susScore}</span></td>
                <td><span class="badge ${getScoreBadgeClass(overallScore)}">${typeof overallScore === 'number' ? overallScore.toFixed(1) : overallScore}</span></td>
                <td>
                    <div class="project-actions">
                        <button class="action-btn" onclick="viewEvaluation('${evaluation.id}')" title="View Details">
                            <i class="bi bi-eye"></i>
                        </button>
                        <button class="action-btn" onclick="downloadReport('${evaluation.id}')" title="Download Report">
                            <i class="bi bi-download"></i>
                        </button>
                    </div>
                </td>
            </tr>
        `;
    }).join('');
}