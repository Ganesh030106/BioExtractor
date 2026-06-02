// ============================
// BioExtractor — Frontend Logic
// ============================

const API_BASE = '';

// --- Example Data ---
const EXAMPLES = {
    bio: `My name is Ganesh Kumar, I'm a Full Stack Developer based in Chennai. I have 7 years of experience working at TCS. I know Python, Java, React, Node.js, and Docker. I completed my B.Tech in Computer Science. My email is ganesh.kumar@email.com and you can find me on linkedin.com/in/ganeshkumar. I'm passionate about building scalable web applications and machine learning.`,
    developer: `Hi, I'm Priya Sharma. I work as a Backend Developer at Infosys with 4 years of experience. My tech stack includes Python, Django, Flask, PostgreSQL, Redis, Docker, and AWS. I'm based in Bangalore and hold an M.Tech in Information Technology. My GitHub is github.com/priyasharma-dev. I'm interested in microservices architecture and cloud computing.`,
    designer: `I am Arjun Menon, a UI/UX Designer from Kochi with 5 years of experience. I currently work at Zoho. I'm skilled in Figma, Adobe XD, Photoshop, Illustrator, HTML, CSS, JavaScript, and React. I have a Diploma in Visual Communication. You can reach me at arjun.menon@email.com or check my portfolio at linkedin.com/in/arjunmenon.`,
    manager: `Hello, this is Sneha Reddy. I am a Project Manager at Wipro based in Hyderabad with over 10 years of experience in the IT industry. I have expertise in Jira, Confluence, Slack, Power BI, and Tableau. I hold an MBA from IIM. My hobbies include reading, traveling, and mentoring. Contact me at sneha.reddy@email.com.`,
};

// --- Field Config ---
const FIELD_CONFIG = {
    name: {
        label: 'Name',
        icon: '👤',
        iconClass: 'icon-name',
    },
    role: {
        label: 'Role / Designation',
        icon: '💼',
        iconClass: 'icon-role',
    },
    experience: {
        label: 'Experience',
        icon: '⏱️',
        iconClass: 'icon-exp',
    },
    company: {
        label: 'Company',
        icon: '🏢',
        iconClass: 'icon-company',
    },
    tech_stacks: {
        label: 'Tech Stacks',
        icon: '🛠️',
        iconClass: 'icon-tech',
    },
    education: {
        label: 'Education',
        icon: '🎓',
        iconClass: 'icon-edu',
    },
    location: {
        label: 'Location',
        icon: '📍',
        iconClass: 'icon-location',
    },
    email: {
        label: 'Email',
        icon: '📧',
        iconClass: 'icon-email',
    },
    phone: {
        label: 'Phone',
        icon: '📱',
        iconClass: 'icon-phone',
    },
    linkedin: {
        label: 'LinkedIn',
        icon: '🔗',
        iconClass: 'icon-linkedin',
    },
    github: {
        label: 'GitHub',
        icon: '🐙',
        iconClass: 'icon-github',
    },
    interests: {
        label: 'Interests',
        icon: '✨',
        iconClass: 'icon-interests',
    },
};

// --- DOM Refs ---
const $ = (sel) => document.querySelector(sel);
const $$ = (sel) => document.querySelectorAll(sel);

const textInput = $('#text-input');
const charCount = $('#char-count');
const btnExtract = $('#btn-extract');
const btnExtractText = $('#btn-extract-text');
const spinner = $('#spinner');
const btnClearInput = $('#btn-clear-input');
const btnExport = $('#btn-export');
const btnClearAll = $('#btn-clear-all');
const btnCopyJson = $('#btn-copy-json');
const resultSection = $('#result-section');
const profileGrid = $('#profile-grid');
const jsonOutput = $('#json-output');
const historyList = $('#history-list');
const historyCount = $('#history-count');
const toastContainer = $('#toast-container');

// Settings Drawer Refs
const btnSettings = $('#btn-settings');
const btnCloseSettings = $('#btn-close-settings');
const settingsDrawer = $('#settings-drawer');
const geminiApiKeyInput = $('#gemini-api-key');
const settingsToggleVisibility = $('#settings-toggle-visibility');
const btnClearSettings = $('#btn-clear-settings');
const btnSaveSettings = $('#btn-save-settings');

// --- State ---
let currentExtracted = null;
let geminiConfigured = false;

// --- Init ---
document.addEventListener('DOMContentLoaded', () => {
    checkEngineStatus();
    loadHistory();
    setupTabs();
    setupListeners();
});

// --- Engine Status ---
async function checkEngineStatus() {
    try {
        const localKey = localStorage.getItem('gemini_api_key');
        geminiConfigured = !!(localKey && localKey.trim());
        
        const badge = document.querySelector('.hero-badge');
        if (badge) {
            if (geminiConfigured) {
                badge.innerHTML = `
                    <span class="pulse-dot" style="background: #34d399"></span>
                    ✨ Gemini AI Connected (User Key)
                `;
                badge.className = 'hero-badge badge-gemini';
            } else {
                badge.innerHTML = `
                    <span class="pulse-dot" style="background: #fb7185"></span>
                    ⚠️ API Key Required — Configure in Settings
                `;
                badge.className = 'hero-badge badge-not-configured';
            }
        }
    } catch (err) {
        console.error('Failed to check engine status:', err);
    }
}

// --- Tab Switching ---
function setupTabs() {
    $$('.nav-tab').forEach((tab) => {
        tab.addEventListener('click', () => {
            const target = tab.dataset.tab;
            $$('.nav-tab').forEach((t) => t.classList.remove('active'));
            tab.classList.add('active');
            $$('.tab-content').forEach((c) => c.classList.remove('active'));
            $(`#content-${target}`).classList.add('active');

            if (target === 'history') loadHistory();
        });
    });
}

// --- Event Listeners ---
function setupListeners() {
    // Character count
    textInput.addEventListener('input', () => {
        const len = textInput.value.length;
        charCount.textContent = `${len} character${len !== 1 ? 's' : ''}`;
    });

    // Extract
    btnExtract.addEventListener('click', handleExtract);

    // Keyboard shortcut
    textInput.addEventListener('keydown', (e) => {
        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
            handleExtract();
        }
    });

    // Clear input
    btnClearInput.addEventListener('click', () => {
        textInput.value = '';
        charCount.textContent = '0 characters';
        resultSection.style.display = 'none';
        textInput.focus();
    });

    // Copy JSON
    btnCopyJson.addEventListener('click', () => {
        if (currentExtracted) {
            const cleanData = { ...currentExtracted };
            delete cleanData.raw_text;
            navigator.clipboard.writeText(JSON.stringify(cleanData, null, 2));
            showToast('JSON copied to clipboard!', 'success');
        }
    });

    // Export
    btnExport.addEventListener('click', handleExport);

    // Clear All
    btnClearAll.addEventListener('click', handleClearAll);

    // Example chips
    $$('.chip').forEach((chip) => {
        chip.addEventListener('click', () => {
            const key = chip.dataset.example;
            textInput.value = EXAMPLES[key] || '';
            const len = textInput.value.length;
            charCount.textContent = `${len} characters`;
            textInput.focus();
            showToast('Example loaded! Click Extract Data.', 'success');
        });
    });

    // Settings Toggle Drawer
    btnSettings.addEventListener('click', () => {
        settingsDrawer.classList.toggle('open');
        if (settingsDrawer.classList.contains('open')) {
            const savedKey = localStorage.getItem('gemini_api_key') || '';
            geminiApiKeyInput.value = savedKey;
            geminiApiKeyInput.focus();
        }
    });

    // Close Settings Drawer
    btnCloseSettings.addEventListener('click', () => {
        settingsDrawer.classList.remove('open');
    });

    // Toggle API Key Input type visibility
    settingsToggleVisibility.addEventListener('click', () => {
        const type = geminiApiKeyInput.getAttribute('type') === 'password' ? 'text' : 'password';
        geminiApiKeyInput.setAttribute('type', type);
        settingsToggleVisibility.textContent = type === 'password' ? '👁️' : '🔒';
    });

    // Save Settings
    btnSaveSettings.addEventListener('click', () => {
        const key = geminiApiKeyInput.value.trim();
        if (!key) {
            showToast('Please enter an API Key first or clear settings.', 'error');
            return;
        }
        localStorage.setItem('gemini_api_key', key);
        settingsDrawer.classList.remove('open');
        showToast('Settings saved successfully!', 'success');
        checkEngineStatus();
    });

    // Clear Settings
    btnClearSettings.addEventListener('click', () => {
        geminiApiKeyInput.value = '';
        localStorage.removeItem('gemini_api_key');
        settingsDrawer.classList.remove('open');
        showToast('API Key removed.', 'success');
        checkEngineStatus();
    });
}

// --- Extract Handler ---
async function handleExtract() {
    const text = textInput.value.trim();
    if (!text) {
        showToast('Please enter some text first.', 'error');
        textInput.focus();
        return;
    }

    const localKey = localStorage.getItem('gemini_api_key');
    if (!localKey || !localKey.trim()) {
        showToast('⚠️ API Key Required. Please set it in Settings (top-right).', 'error');
        settingsDrawer.classList.add('open');
        geminiApiKeyInput.focus();
        return;
    }

    setLoading(true);

    try {
        const resp = await fetch(`${API_BASE}/api/extract`, {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json',
                'X-Gemini-API-Key': localKey.trim()
            },
            body: JSON.stringify({ text }),
        });

        const data = await resp.json();

        if (!resp.ok) {
            throw new Error(data.error || 'Extraction failed.');
        }

        currentExtracted = data.extracted;
        renderResult(data.extracted);
        updateHistoryCount(data.total_entries);
        
        const extractedBy = data.extracted.extracted_by === 'gemini' ? 'Gemini AI' : 'Regex Fallback';
        showToast(`✨ Profile extracted via ${extractedBy}!`, 'success');
    } catch (err) {
        showToast(err.message || 'Something went wrong.', 'error');
    } finally {
        setLoading(false);
    }
}

// --- Render Result ---
function renderResult(data) {
    resultSection.style.display = 'block';

    // Profile cards
    profileGrid.innerHTML = '';
    const displayFields = Object.keys(FIELD_CONFIG);

    displayFields.forEach((key, idx) => {
        const config = FIELD_CONFIG[key];
        const value = data[key];
        const card = document.createElement('div');
        card.className = 'profile-card';
        card.style.animationDelay = `${idx * 0.05}s`;

        let valueHtml;
        if (value === null || value === undefined) {
            valueHtml = `<div class="profile-card-value null-val">Not detected</div>`;
        } else if (Array.isArray(value)) {
            if (key === 'tech_stacks') {
                valueHtml = `<div class="profile-card-value">${value
                    .map((t) => `<span class="tech-tag">${escapeHtml(t)}</span>`)
                    .join('')}</div>`;
            } else {
                valueHtml = `<div class="profile-card-value">${value
                    .map((v) => escapeHtml(v))
                    .join(', ')}</div>`;
            }
        } else {
            valueHtml = `<div class="profile-card-value">${escapeHtml(String(value))}</div>`;
        }

        card.innerHTML = `
            <div class="profile-card-icon ${config.iconClass}">${config.icon}</div>
            <div class="profile-card-label">${config.label}</div>
            ${valueHtml}
        `;

        profileGrid.appendChild(card);
    });

    // JSON output with syntax highlighting
    const cleanData = { ...data };
    delete cleanData.raw_text;
    jsonOutput.innerHTML = syntaxHighlight(JSON.stringify(cleanData, null, 2));

    // Smooth scroll to result
    resultSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// --- JSON Syntax Highlighting ---
function syntaxHighlight(json) {
    return json.replace(
        /("(\\u[\da-fA-F]{4}|\\[^u]|[^\\"])*"(\s*:)?|\b(true|false|null)\b|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?)/g,
        (match) => {
            let cls = 'json-number';
            if (/^"/.test(match)) {
                if (/:$/.test(match)) {
                    cls = 'json-key';
                    // Remove the colon for wrapping, add it back
                    return `<span class="${cls}">${escapeHtml(match.slice(0, -1))}</span>:`;
                } else {
                    cls = 'json-string';
                }
            } else if (/true|false/.test(match)) {
                cls = 'json-bool';
            } else if (/null/.test(match)) {
                cls = 'json-null';
            }
            return `<span class="${cls}">${escapeHtml(match)}</span>`;
        }
    );
}

// --- History ---
async function loadHistory() {
    try {
        const resp = await fetch(`${API_BASE}/api/history`);
        const data = await resp.json();
        renderHistory(data.entries);
        updateHistoryCount(data.total);
    } catch (err) {
        console.error('Failed to load history:', err);
    }
}

function renderHistory(entries) {
    if (!entries || entries.length === 0) {
        historyList.innerHTML = `
            <div class="empty-state" id="empty-state">
                <div class="empty-icon">
                    <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                        <polyline points="14 2 14 8 20 8"/>
                    </svg>
                </div>
                <h3>No extractions yet</h3>
                <p>Start by entering a text description to extract structured data.</p>
            </div>
        `;
        return;
    }

    historyList.innerHTML = '';
    const GRADIENTS = [
        'linear-gradient(135deg, #818cf8, #6366f1)',
        'linear-gradient(135deg, #c084fc, #a855f7)',
        'linear-gradient(135deg, #f472b6, #ec4899)',
        'linear-gradient(135deg, #34d399, #10b981)',
        'linear-gradient(135deg, #22d3ee, #06b6d4)',
        'linear-gradient(135deg, #fbbf24, #f59e0b)',
    ];

    // Render newest first
    entries
        .slice()
        .reverse()
        .forEach((entry, i) => {
            const realIndex = entries.length - 1 - i;
            const name = entry.name || 'Unknown';
            const initials = name
                .split(' ')
                .map((n) => n[0])
                .join('')
                .slice(0, 2)
                .toUpperCase();
            const gradient = GRADIENTS[i % GRADIENTS.length];
            const techs = entry.tech_stacks
                ? entry.tech_stacks.slice(0, 5).map((t) => `<span class="tech-tag">${escapeHtml(t)}</span>`).join('')
                : '';

            const el = document.createElement('div');
            el.className = 'history-entry';
            el.style.animationDelay = `${i * 0.05}s`;
            el.innerHTML = `
                <div class="history-entry-header" data-idx="${realIndex}">
                    <div class="history-entry-info">
                        <div class="history-avatar" style="background: ${gradient}">${initials}</div>
                        <div>
                            <div class="history-name">${escapeHtml(name)}</div>
                            <div class="history-meta">
                                ${entry.role ? `<span class="history-meta-item">💼 ${escapeHtml(entry.role)}</span>` : ''}
                                ${entry.experience ? `<span class="history-meta-item">⏱️ ${escapeHtml(entry.experience)}</span>` : ''}
                                <span class="history-meta-item">🕐 ${escapeHtml(entry.timestamp)}</span>
                            </div>
                        </div>
                    </div>
                    <div class="history-entry-actions">
                        <button class="btn-sm btn-delete-entry" data-idx="${realIndex}" title="Delete entry">
                            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                <polyline points="3,6 5,6 21,6"/>
                                <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>
                            </svg>
                        </button>
                    </div>
                </div>
                <div class="history-entry-body" id="history-body-${realIndex}">
                    ${techs ? `<div class="history-tags">${techs}</div>` : ''}
                    <div class="history-raw-text">${escapeHtml(entry.raw_text || '')}</div>
                </div>
            `;
            historyList.appendChild(el);
        });

    // Toggle body
    $$('.history-entry-header').forEach((header) => {
        header.addEventListener('click', (e) => {
            if (e.target.closest('.btn-delete-entry')) return;
            const idx = header.dataset.idx;
            const body = $(`#history-body-${idx}`);
            body.classList.toggle('open');
        });
    });

    // Delete buttons
    $$('.btn-delete-entry').forEach((btn) => {
        btn.addEventListener('click', (e) => {
            e.stopPropagation();
            handleDeleteEntry(parseInt(btn.dataset.idx));
        });
    });
}

function updateHistoryCount(count) {
    historyCount.textContent = count;
}

// --- Delete Entry ---
async function handleDeleteEntry(index) {
    try {
        const resp = await fetch(`${API_BASE}/api/delete/${index}`, {
            method: 'DELETE',
        });
        const data = await resp.json();
        if (data.success) {
            loadHistory();
            showToast('Entry deleted.', 'success');
        }
    } catch (err) {
        showToast('Failed to delete entry.', 'error');
    }
}

// --- Clear All ---
async function handleClearAll() {
    if (!confirm('Are you sure you want to clear all extracted data?')) return;
    try {
        const resp = await fetch(`${API_BASE}/api/clear`, { method: 'DELETE' });
        const data = await resp.json();
        if (data.success) {
            loadHistory();
            showToast('All data cleared.', 'success');
        }
    } catch (err) {
        showToast('Failed to clear data.', 'error');
    }
}

// --- Export ---
async function handleExport() {
    try {
        const resp = await fetch(`${API_BASE}/api/export`);
        const data = await resp.json();
        if (data.length === 0) {
            showToast('No data to export.', 'error');
            return;
        }
        const blob = new Blob([JSON.stringify(data, null, 2)], {
            type: 'application/json',
        });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `bioextractor_profiles_${new Date().toISOString().slice(0, 10)}.json`;
        a.click();
        URL.revokeObjectURL(url);
        showToast('Data exported successfully!', 'success');
    } catch (err) {
        showToast('Export failed.', 'error');
    }
}

// --- Loading State ---
function setLoading(loading) {
    if (loading) {
        btnExtract.disabled = true;
        btnExtractText.textContent = 'Extracting...';
        spinner.style.display = 'block';
    } else {
        btnExtract.disabled = false;
        btnExtractText.textContent = 'Extract Data';
        spinner.style.display = 'none';
    }
}

// --- Toast ---
function showToast(message, type = 'success') {
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    const icon =
        type === 'success'
            ? '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#34d399" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20,6 9,17 4,12"/></svg>'
            : '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#fb7185" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/></svg>';
    toast.innerHTML = `${icon}<span>${escapeHtml(message)}</span>`;
    toastContainer.appendChild(toast);

    setTimeout(() => {
        toast.classList.add('toast-out');
        toast.addEventListener('animationend', () => toast.remove());
    }, 3000);
}

// --- Utilities ---
function escapeHtml(str) {
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
}
