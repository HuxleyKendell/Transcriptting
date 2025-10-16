// API base URL
const API_BASE = '/api';

// Current active transcript details
let currentTranscriptDetails = {};

// Tab switching
function showTab(tabName) {
    // Hide all tabs
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });
    
    // Remove active class from all buttons
    document.querySelectorAll('.tab-button').forEach(button => {
        button.classList.remove('active');
    });
    
    // Show selected tab
    document.getElementById(tabName).classList.add('active');
    
    // Add active class to clicked button
    event.target.classList.add('active');
    
    // Load data for the tab
    if (tabName === 'dashboard') {
        loadDashboard();
    } else if (tabName === 'transcripts') {
        loadTranscripts();
    } else if (tabName === 'insights') {
        loadInsights();
    }
}

// Load dashboard data
async function loadDashboard() {
    try {
        // Load transcripts count
        const transcriptsResponse = await fetch(`${API_BASE}/transcripts`);
        const transcriptsData = await transcriptsResponse.json();
        document.getElementById('totalTranscripts').textContent = transcriptsData.count || 0;
        
        // Load insights summary
        const summaryResponse = await fetch(`${API_BASE}/insights/summary`);
        const summaryData = await summaryResponse.json();
        
        document.getElementById('totalInsights').textContent = summaryData.total_insights || 0;
        
        // Update category counts
        const summary = summaryData.summary || {};
        document.getElementById('featureRequests').textContent = 
            summary.feature_request?.count || 0;
        document.getElementById('painPoints').textContent = 
            summary.pain_point?.count || 0;
        
        // Display detailed summary
        displaySummary(summary);
        
    } catch (error) {
        console.error('Error loading dashboard:', error);
        document.getElementById('summaryContent').innerHTML = 
            '<p class="error">Failed to load dashboard data</p>';
    }
}

// Display insights summary
function displaySummary(summary) {
    const summaryContent = document.getElementById('summaryContent');
    
    if (Object.keys(summary).length === 0) {
        summaryContent.innerHTML = '<p class="empty-state">No insights available yet. Upload some transcripts to get started!</p>';
        return;
    }
    
    let html = '';
    
    for (const [category, data] of Object.entries(summary)) {
        const categoryName = category.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase());
        
        html += `
            <div class="summary-category">
                <h3>${categoryName}</h3>
                <div class="summary-stats">
                    <div class="summary-stat">
                        <div class="summary-stat-label">Total</div>
                        <div class="summary-stat-value">${data.count}</div>
                    </div>
                    <div class="summary-stat">
                        <div class="summary-stat-label">High Priority</div>
                        <div class="summary-stat-value">${data.by_priority.high}</div>
                    </div>
                    <div class="summary-stat">
                        <div class="summary-stat-label">Positive</div>
                        <div class="summary-stat-value">${data.by_sentiment.positive}</div>
                    </div>
                    <div class="summary-stat">
                        <div class="summary-stat-label">Negative</div>
                        <div class="summary-stat-value">${data.by_sentiment.negative}</div>
                    </div>
                </div>
            </div>
        `;
    }
    
    summaryContent.innerHTML = html;
}

// Load transcripts list
async function loadTranscripts() {
    const listContainer = document.getElementById('transcriptsList');
    listContainer.innerHTML = '<div class="loading">Loading transcripts...</div>';
    
    try {
        const clientName = document.getElementById('searchClient').value;
        let url = `${API_BASE}/transcripts`;
        
        if (clientName) {
            url += `?client_name=${encodeURIComponent(clientName)}`;
        }
        
        const response = await fetch(url);
        const data = await response.json();
        
        if (data.transcripts.length === 0) {
            listContainer.innerHTML = `
                <div class="empty-state">
                    <div class="empty-state-icon">📄</div>
                    <p>No transcripts found</p>
                </div>
            `;
            return;
        }
        
        let html = '';
        
        for (const transcript of data.transcripts) {
            const callDate = new Date(transcript.call_date).toLocaleString();
            const statusBadge = transcript.processed 
                ? '<span class="badge processed">Processed</span>'
                : '<span class="badge pending">Pending</span>';
            
            html += `
                <div class="transcript-item">
                    <div class="transcript-header">
                        <div>
                            <div class="transcript-title">${transcript.title}</div>
                            <div class="transcript-meta">
                                ${transcript.client_name ? `Client: ${transcript.client_name} | ` : ''}
                                Date: ${callDate}
                                ${statusBadge}
                            </div>
                        </div>
                    </div>
                    ${transcript.insights.length > 0 ? `
                        <div class="insights-preview">
                            <h4>Extracted Insights (${transcript.insights.length}):</h4>
                            ${transcript.insights.slice(0, 3).map(insight => `
                                <div class="insight-preview-item">
                                    <span class="insight-category">${insight.category.replace('_', ' ')}:</span>
                                    ${insight.content.substring(0, 100)}${insight.content.length > 100 ? '...' : ''}
                                    <span class="badge ${insight.priority}">${insight.priority}</span>
                                    <span class="badge ${insight.sentiment}">${insight.sentiment}</span>
                                </div>
                            `).join('')}
                            ${transcript.insights.length > 3 ? `<p><em>+${transcript.insights.length - 3} more insights</em></p>` : ''}
                        </div>
                    ` : ''}
                    <div class="transcript-actions">
                        <button class="action-button view" onclick="viewTranscript(${transcript.id})">View Details</button>
                        ${!transcript.processed ? `<button class="action-button view" onclick="processTranscript(${transcript.id})">Process Now</button>` : ''}
                        <button class="action-button delete" onclick="deleteTranscript(${transcript.id})">Delete</button>
                    </div>
                </div>
            `;
        }
        
        listContainer.innerHTML = html;
        
    } catch (error) {
        console.error('Error loading transcripts:', error);
        listContainer.innerHTML = '<p class="error">Failed to load transcripts</p>';
    }
}

// View transcript details
async function viewTranscript(transcriptId) {
    try {
        const response = await fetch(`${API_BASE}/transcripts/${transcriptId}`);
        const data = await response.json();
        
        const transcript = data.transcript;
        
        alert(`Transcript: ${transcript.title}\n\nClient: ${transcript.client_name || 'N/A'}\n\nContent:\n${transcript.content.substring(0, 500)}...\n\nInsights: ${transcript.insights.length}`);
        
    } catch (error) {
        console.error('Error viewing transcript:', error);
        alert('Failed to load transcript details');
    }
}

// Process transcript
async function processTranscript(transcriptId) {
    if (!confirm('Process this transcript now? This will extract insights using Azure OpenAI.')) {
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE}/process/${transcriptId}`, {
            method: 'POST'
        });
        
        const data = await response.json();
        
        if (data.success) {
            alert(data.message);
            loadTranscripts();
        } else {
            alert('Failed to process transcript: ' + data.error);
        }
        
    } catch (error) {
        console.error('Error processing transcript:', error);
        alert('Failed to process transcript');
    }
}

// Delete transcript
async function deleteTranscript(transcriptId) {
    if (!confirm('Are you sure you want to delete this transcript?')) {
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE}/transcripts/${transcriptId}`, {
            method: 'DELETE'
        });
        
        const data = await response.json();
        
        if (data.success) {
            alert('Transcript deleted successfully');
            loadTranscripts();
            loadDashboard();
        } else {
            alert('Failed to delete transcript');
        }
        
    } catch (error) {
        console.error('Error deleting transcript:', error);
        alert('Failed to delete transcript');
    }
}

// Load insights
async function loadInsights() {
    const listContainer = document.getElementById('insightsList');
    listContainer.innerHTML = '<div class="loading">Loading insights...</div>';
    
    try {
        const category = document.getElementById('filterCategory').value;
        const sentiment = document.getElementById('filterSentiment').value;
        const priority = document.getElementById('filterPriority').value;
        
        let url = `${API_BASE}/insights?`;
        const params = [];
        
        if (category) params.push(`category=${category}`);
        if (sentiment) params.push(`sentiment=${sentiment}`);
        if (priority) params.push(`priority=${priority}`);
        
        url += params.join('&');
        
        const response = await fetch(url);
        const data = await response.json();
        
        if (data.insights.length === 0) {
            listContainer.innerHTML = `
                <div class="empty-state">
                    <div class="empty-state-icon">💡</div>
                    <p>No insights found</p>
                </div>
            `;
            return;
        }
        
        let html = '';
        
        for (const insight of data.insights) {
            const createdDate = new Date(insight.created_at).toLocaleString();
            
            html += `
                <div class="insight-item">
                    <div class="insight-category">${insight.category.replace('_', ' ')}</div>
                    <div class="insight-content">${insight.content}</div>
                    <div class="transcript-meta">
                        <span class="badge ${insight.priority}">${insight.priority} priority</span>
                        <span class="badge ${insight.sentiment}">${insight.sentiment}</span>
                        <span style="margin-left: 10px;">${createdDate}</span>
                    </div>
                </div>
            `;
        }
        
        listContainer.innerHTML = html;
        
    } catch (error) {
        console.error('Error loading insights:', error);
        listContainer.innerHTML = '<p class="error">Failed to load insights</p>';
    }
}

// Handle form submission
document.addEventListener('DOMContentLoaded', function() {
    const uploadForm = document.getElementById('uploadForm');
    
    uploadForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const statusDiv = document.getElementById('uploadStatus');
        statusDiv.className = 'status-message';
        statusDiv.textContent = 'Uploading and processing transcript...';
        statusDiv.style.display = 'block';
        
        const title = document.getElementById('transcriptTitle').value;
        const clientName = document.getElementById('clientName').value;
        const callDate = document.getElementById('callDate').value;
        const content = document.getElementById('transcriptContent').value;
        
        const payload = {
            title: title,
            content: content
        };
        
        if (clientName) {
            payload.client_name = clientName;
        }
        
        if (callDate) {
            payload.call_date = new Date(callDate).toISOString();
        }
        
        try {
            const response = await fetch(`${API_BASE}/transcripts`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(payload)
            });
            
            const data = await response.json();
            
            if (data.success) {
                statusDiv.className = 'status-message success';
                statusDiv.textContent = data.message || 'Transcript uploaded successfully!';
                
                // Reset form
                uploadForm.reset();
                
                // Reload dashboard
                setTimeout(() => {
                    loadDashboard();
                }, 1000);
            } else {
                statusDiv.className = 'status-message error';
                statusDiv.textContent = 'Error: ' + (data.error || 'Upload failed');
            }
            
        } catch (error) {
            console.error('Error uploading transcript:', error);
            statusDiv.className = 'status-message error';
            statusDiv.textContent = 'Error: Failed to upload transcript';
        }
    });
    
    // Load initial dashboard data
    loadDashboard();
});
