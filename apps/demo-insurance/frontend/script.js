const API_URL = 'http://localhost:8000';

const loginForm = document.getElementById('login-form');
const dashboardScreen = document.getElementById('dashboard-screen');
const loginScreen = document.getElementById('login-screen');
const logoutBtn = document.getElementById('logout-btn');
const policyContainer = document.getElementById('policy-details');
const fileClaimBtn = document.getElementById('file-claim-btn');
const payPremiumBtn = document.getElementById('pay-premium-btn');
const activityList = document.getElementById('activity-list');

// --- EVENT LISTENERS ---

loginForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const btn = loginForm.querySelector('button');
    const originalText = btn.innerHTML;

    // Simulate loading state
    btn.innerHTML = '<div class="loader-mini"></div> Logging in...';

    try {
        const response = await fetch(`${API_URL}/login`, {
            method: 'POST'
        });

        if (response.ok) {
            showToast('Login Successful!', 'success');
            switchScreen('dashboard');
            loadDashboardData();
        } else {
            showToast('Login Failed. Please try again.', 'error');
        }
    } catch (err) {
        console.error(err);
        showToast('Connection Error. Is the backend running?', 'error');
    } finally {
        btn.innerHTML = originalText;
    }
});

logoutBtn.addEventListener('click', () => {
    switchScreen('login');
    showToast('Logged out successfully', 'info');
});

fileClaimBtn.addEventListener('click', async () => {
    try {
        const response = await fetch(`${API_URL}/claim`, { method: 'POST' });
        const data = await response.json();

        if (response.ok) {
            showToast(`Claim Submitted! ID: ${data.claim_id}`, 'warning');
            addActivity(`Files Claim: ${data.claim_id}`, 'Just now');
        }
    } catch (err) {
        showToast('Failed to file claim', 'error');
    }
});

payPremiumBtn.addEventListener('click', async () => {
    try {
        const response = await fetch(`${API_URL}/payment`, { method: 'POST' });
        const data = await response.json();

        if (response.ok) {
            showToast(`Premium Paid: ${data.payment}`, 'success');
            addActivity('Premium Payment Processed', 'Just now');
        }
    } catch (err) {
        showToast('Payment Failed', 'error');
    }
});

// --- FUNCTIONS ---

function switchScreen(screenName) {
    if (screenName === 'dashboard') {
        loginScreen.classList.add('hidden');
        loginScreen.classList.remove('active');
        dashboardScreen.classList.remove('hidden');
        dashboardScreen.classList.add('active');
    } else {
        dashboardScreen.classList.add('hidden');
        dashboardScreen.classList.remove('active');
        loginScreen.classList.remove('hidden');
        loginScreen.classList.add('active');
    }
}

async function loadDashboardData() {
    // 1. Get Policy
    try {
        // Using a hardcoded ID as per the backend demo
        const response = await fetch(`${API_URL}/policy/POL-8859`);
        const data = await response.json();

        policyContainer.innerHTML = `
            <div class="policy-detail-row">
                <span class="policy-label">Policy ID</span>
                <span class="policy-value">${data.policy_id}</span>
            </div>
            <div class="policy-detail-row">
                <span class="policy-label">Coverage</span>
                <span class="policy-value">$1,000,000</span>
            </div>
            <div class="policy-detail-row">
                <span class="policy-label">Plan Type</span>
                <span class="policy-value">Comprehensive Shield</span>
            </div>
        `;
    } catch (err) {
        policyContainer.innerHTML = '<p class="error">Failed to load policy.</p>';
    }
}

function showToast(message, type = 'info') {
    const container = document.getElementById('toast-container');
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;

    let icon = 'information-circle-outline';
    if (type === 'success') icon = 'checkmark-circle-outline';
    if (type === 'error') icon = 'alert-circle-outline';
    if (type === 'warning') icon = 'warning-outline';

    toast.innerHTML = `<ion-icon name="${icon}"></ion-icon> <span>${message}</span>`;

    container.appendChild(toast);

    setTimeout(() => {
        toast.style.opacity = '0';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

function addActivity(text, time) {
    const li = document.createElement('li');
    li.className = 'activity-item';
    li.innerHTML = `
        <div class="dot"></div>
        <div class="activity-text">
            <strong>${text}</strong>
            <small>${time}</small>
        </div>
    `;
    // Insert after the first item (System Online)
    const list = document.getElementById('activity-list');
    list.insertBefore(li, list.firstChild);
}
