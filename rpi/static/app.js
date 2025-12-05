// RPi Answer Sheet Checker - Frontend

// DOM elements
const uploadArea = document.getElementById('uploadArea');
const imageInput = document.getElementById('imageInput');
const uploadProgress = document.getElementById('uploadProgress');
const uploadStatus = document.getElementById('uploadStatus');
const answerKeyContainer = document.getElementById('answerKeyContainer');
const addAnswerBtn = document.getElementById('addAnswerBtn');
const gradeBtn = document.getElementById('gradeBtn');
const clearBtn = document.getElementById('clearBtn');
const thresholdInput = document.getElementById('threshold');
const thresholdValue = document.getElementById('thresholdValue');
const resultsSection = document.getElementById('resultsSection');
const resultsSummary = document.getElementById('resultsSummary');
const resultsDetails = document.getElementById('resultsDetails');
const historyList = document.getElementById('historyList');

// State
let uploadedImagePath = null;
let gradingHistory = [];

// Upload Area Events
uploadArea.addEventListener('click', () => imageInput.click());
uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadArea.classList.add('dragover');
});
uploadArea.addEventListener('dragleave', () => {
    uploadArea.classList.remove('dragover');
});
uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadArea.classList.remove('dragover');
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        uploadImage(files[0]);
    }
});

imageInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
        uploadImage(e.target.files[0]);
    }
});

// Upload Image
async function uploadImage(file) {
    if (!isValidImageFile(file)) {
        showStatus('Invalid file type. Use JPG, PNG, or BMP.', 'error');
        return;
    }
    
    if (file.size > 50 * 1024 * 1024) {
        showStatus('File too large. Maximum 50MB.', 'error');
        return;
    }
    
    uploadProgress.classList.remove('hidden');
    showStatus('Uploading...', 'info');
    gradeBtn.disabled = true;
    
    const formData = new FormData();
    formData.append('image', file);
    
    try {
        const response = await fetch('/api/upload', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (response.ok) {
            uploadedImagePath = data.path;
            showStatus(`✓ Image uploaded: ${file.name}`, 'success');
            gradeBtn.disabled = false;
        } else {
            showStatus(`Upload failed: ${data.error}`, 'error');
        }
    } catch (error) {
        showStatus(`Upload error: ${error.message}`, 'error');
    } finally {
        uploadProgress.classList.add('hidden');
    }
}

// Validate image file
function isValidImageFile(file) {
    const validTypes = ['image/jpeg', 'image/png', 'image/bmp'];
    return validTypes.includes(file.type);
}

// Answer Key Management
let answerCount = 1;

addAnswerBtn.addEventListener('click', () => {
    answerCount++;
    addAnswerField(answerCount);
});

function addAnswerField(number) {
    const div = document.createElement('div');
    div.className = 'answer-input';
    div.innerHTML = `
        <label>Q${number}</label>
        <input type="text" class="answer-field" placeholder="Answer ${number}">
        <button type="button" class="remove-btn">×</button>
    `;
    
    div.querySelector('.remove-btn').addEventListener('click', () => {
        div.remove();
    });
    
    answerKeyContainer.appendChild(div);
}

// Get Answer Key
function getAnswerKey() {
    const fields = document.querySelectorAll('.answer-field');
    return Array.from(fields).map(field => field.value).filter(v => v.trim());
}

// Threshold
thresholdInput.addEventListener('input', (e) => {
    thresholdValue.textContent = Math.round(e.target.value * 100) + '%';
});

// Grade Button
gradeBtn.addEventListener('click', async () => {
    if (!uploadedImagePath) {
        showStatus('Please upload an image first', 'error');
        return;
    }
    
    const answerKey = getAnswerKey();
    if (answerKey.length === 0) {
        showStatus('Please add at least one answer', 'error');
        return;
    }
    
    gradeBtn.disabled = true;
    showStatus('Grading... Please wait', 'info');
    
    try {
        const response = await fetch('/api/grade', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                image_path: uploadedImagePath,
                answer_key: answerKey,
                threshold: parseFloat(thresholdInput.value)
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            displayResults(data.results);
            addToHistory(data.results);
            showStatus('✓ Grading complete!', 'success');
        } else {
            showStatus(`Grading failed: ${data.error}`, 'error');
        }
    } catch (error) {
        showStatus(`Error: ${error.message}`, 'error');
    } finally {
        gradeBtn.disabled = false;
    }
});

// Display Results
function displayResults(results) {
    if (!results.success) {
        showStatus('Error processing image', 'error');
        return;
    }
    
    resultsSection.classList.remove('hidden');
    resultsSummary.innerHTML = '';
    resultsDetails.innerHTML = '';
    
    const summary = results.summary;
    
    // Summary
    const summaryHTML = `
        <h3>📊 Summary</h3>
        <div class="summary-stat">
            <span>Passed:</span>
            <span>${summary.passed}/${summary.total_questions}</span>
        </div>
        <div class="summary-stat">
            <span>Percentage:</span>
            <span>${summary.percentage.toFixed(1)}%</span>
        </div>
        <div class="summary-stat">
            <span>Threshold:</span>
            <span>${(summary.threshold * 100).toFixed(0)}%</span>
        </div>
    `;
    resultsSummary.innerHTML = summaryHTML;
    
    // Details
    let detailsHTML = '';
    for (let i = 1; i <= summary.total_questions; i++) {
        if (results[i]) {
            const result = results[i];
            const isPassed = result.similarity >= summary.threshold;
            const className = isPassed ? 'pass' : 'fail';
            const icon = isPassed ? '✅' : '❌';
            
            detailsHTML += `
                <div class="question-result ${className}">
                    <h4>${icon} Question ${i}</h4>
                    <p><strong>Similarity:</strong> <span class="similarity">${(result.similarity * 100).toFixed(1)}%</span></p>
                    <p><strong>Expected:</strong> ${escapeHtml(result.expected)}</p>
                    <p><strong>Student:</strong> ${escapeHtml(result.student)}</p>
                </div>
            `;
        }
    }
    
    resultsDetails.innerHTML = detailsHTML;
}

// History
function addToHistory(results) {
    const summary = results.summary;
    const timestamp = new Date().toLocaleString();
    
    gradingHistory.unshift({
        timestamp,
        percentage: summary.percentage,
        passed: summary.passed,
        total: summary.total_questions
    });
    
    updateHistoryDisplay();
}

function updateHistoryDisplay() {
    if (gradingHistory.length === 0) {
        historyList.innerHTML = '<p class="placeholder">No grading history yet</p>';
        return;
    }
    
    historyList.innerHTML = gradingHistory.map((item, index) => `
        <div class="history-item">
            <div class="history-item-header">
                <strong>${item.passed}/${item.total} passed</strong>
                <span>${item.percentage.toFixed(1)}%</span>
            </div>
            <div class="history-item-meta">${item.timestamp}</div>
        </div>
    `).join('');
}

// Clear All
clearBtn.addEventListener('click', () => {
    if (confirm('Clear all data? This cannot be undone.')) {
        uploadedImagePath = null;
        imageInput.value = '';
        answerKeyContainer.innerHTML = '';
        addAnswerField(1);
        resultsSection.classList.add('hidden');
        showStatus('', '');
        document.querySelectorAll('.answer-field').forEach(f => f.value = '');
    }
});

// Utility Functions
function showStatus(message, type) {
    uploadStatus.textContent = message;
    uploadStatus.className = `status ${type}`;
}

function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    addAnswerField(1);
    loadHistoryFromServer();
});

async function loadHistoryFromServer() {
    try {
        const response = await fetch('/api/results');
        const data = await response.json();
        
        if (data.success && data.results) {
            gradingHistory = data.results.map(r => ({
                timestamp: new Date(r.timestamp * 1000).toLocaleString(),
                percentage: r.summary.percentage,
                passed: r.summary.passed,
                total: r.summary.total_questions
            }));
            updateHistoryDisplay();
        }
    } catch (error) {
        console.error('Failed to load history:', error);
    }
}
