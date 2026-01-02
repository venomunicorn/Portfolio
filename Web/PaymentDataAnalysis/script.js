// FIXED: Wait for DOM and Chart.js to be fully loaded
document.addEventListener('DOMContentLoaded', function () {
    // Check if Chart.js is loaded
    if (typeof Chart === 'undefined') {
        showNotification('Chart.js library failed to load. Please check your internet connection.', 'error');
        return;
    }

    console.log('Chart.js loaded successfully, version:', Chart.version);
    initializeApp();
});

// Global variables
let currentData = null;
let categoryChart = null;
let trendsChart = null;

// Pastel color palette for charts
const pastelColors = [
    '#ff9aa2', '#ffdac1', '#e2f0cb', '#a1c4fd',
    '#c2e9fb', '#fbc2eb', '#a6c1ee', '#d4fc79',
    '#96e6a1', '#fddb92', '#d1fdff', '#8a84e2'
];

// DOM Elements
let fileInput, uploadArea, uploadBtn, loadingSpinner;
let totalSpentEl, totalReceivedEl, transactionCountEl, largestAmountEl, netBalanceEl, avgAmountEl;
let minAmountEl, maxAmountEl, startDateEl, endDateEl, categoryFilterEl, keywordSearchEl;
let applyFiltersBtn, resetFiltersBtn, trendBtns;
let exportCSVBtn, printReportBtn, themeToggleBtn;
let isDarkMode = false;

function initializeApp() {
    try {
        // Initialize DOM elements
        fileInput = document.getElementById('fileInput');
        uploadArea = document.getElementById('uploadArea');
        uploadBtn = document.getElementById('uploadBtn');
        loadingSpinner = document.getElementById('loadingSpinner');

        // Stats elements
        totalSpentEl = document.getElementById('totalSpent');
        totalReceivedEl = document.getElementById('totalReceived');
        transactionCountEl = document.getElementById('transactionCount');
        largestAmountEl = document.getElementById('largestAmount');
        netBalanceEl = document.getElementById('netBalance');
        avgAmountEl = document.getElementById('avgAmount');

        // Filter elements
        minAmountEl = document.getElementById('minAmount');
        maxAmountEl = document.getElementById('maxAmount');
        startDateEl = document.getElementById('startDate');
        endDateEl = document.getElementById('endDate');
        categoryFilterEl = document.getElementById('categoryFilter');
        keywordSearchEl = document.getElementById('keywordSearch');
        applyFiltersBtn = document.getElementById('applyFilters');
        resetFiltersBtn = document.getElementById('resetFilters');

        // Chart elements
        trendBtns = document.querySelectorAll('.trend-btn');

        // Export and theme elements
        exportCSVBtn = document.getElementById('exportCSV');
        printReportBtn = document.getElementById('printReport');
        themeToggleBtn = document.getElementById('themeToggle');

        // Load saved theme
        loadTheme();

        // Initialize event listeners
        initializeEventListeners();

        // Load initial data
        loadInitialData();

        console.log('App initialized successfully');
    } catch (error) {
        console.error('Error initializing app:', error);
        showNotification('Failed to initialize application', 'error');
    }
}

function initializeEventListeners() {
    try {
        // File upload events
        if (uploadArea && fileInput) {
            uploadArea.addEventListener('click', () => fileInput.click());
            uploadArea.addEventListener('dragover', handleDragOver);
            uploadArea.addEventListener('dragleave', handleDragLeave);
            uploadArea.addEventListener('drop', handleDrop);
            fileInput.addEventListener('change', handleFileSelect);
        }

        if (uploadBtn) {
            uploadBtn.addEventListener('click', handleUpload);
        }

        // Filter events
        if (applyFiltersBtn) {
            applyFiltersBtn.addEventListener('click', applyFilters);
        }
        if (resetFiltersBtn) {
            resetFiltersBtn.addEventListener('click', resetFilters);
        }

        // Trend button events
        if (trendBtns) {
            trendBtns.forEach(btn => {
                btn.addEventListener('click', (e) => {
                    trendBtns.forEach(b => b.classList.remove('active'));
                    e.target.classList.add('active');
                    updateTrendsChart(e.target.dataset.period);
                });
            });
        }

        // Export and theme events
        if (exportCSVBtn) {
            exportCSVBtn.addEventListener('click', exportToCSV);
        }
        if (printReportBtn) {
            printReportBtn.addEventListener('click', printReport);
        }
        if (themeToggleBtn) {
            themeToggleBtn.addEventListener('click', toggleTheme);
        }

        console.log('Event listeners initialized');
    } catch (error) {
        console.error('Error setting up event listeners:', error);
    }
}

function handleDragOver(e) {
    e.preventDefault();
    uploadArea.classList.add('dragover');
}

function handleDragLeave(e) {
    e.preventDefault();
    uploadArea.classList.remove('dragover');
}

function handleDrop(e) {
    e.preventDefault();
    uploadArea.classList.remove('dragover');
    const files = e.dataTransfer.files;
    if (files.length > 0 && (files[0].name.endsWith('.xlsx') || files[0].name.endsWith('.xls'))) {
        fileInput.files = files;
        handleFileSelect();
    } else {
        showNotification('Please select a valid .xlsx or .xls file', 'error');
    }
}

function handleFileSelect() {
    const file = fileInput.files[0];
    if (file) {
        document.querySelector('.upload-content p').textContent = `Selected: ${file.name}`;
    }
}

async function handleUpload() {
    const file = fileInput.files[0];
    if (!file) {
        showNotification('Please select a file first', 'error');
        return;
    }

    showLoading(true);
    updateStatus('Uploading file...');

    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });

        const result = await response.json();

        if (response.ok) {
            showNotification('File uploaded successfully!', 'success');
            updateStatus('File uploaded. Loading analysis...');
            await loadInitialData();
        } else {
            showNotification(`Upload failed: ${result.error}`, 'error');
            updateStatus('Upload failed. Please try again.');
        }
    } catch (error) {
        console.error('Upload error:', error);
        showNotification(`Upload failed: ${error.message}`, 'error');
        updateStatus('Upload failed due to network error.');
    } finally {
        showLoading(false);
    }
}

async function loadInitialData() {
    showLoading(true);
    updateStatus('Loading transaction data...');

    try {
        const response = await fetch('/analyze');

        if (response.ok) {
            currentData = await response.json();
            console.log('Data loaded successfully:', currentData);
            updateDashboard(currentData);
            updateStatus(`Loaded ${currentData.transaction_count || 0} transactions successfully.`);
        } else {
            const error = await response.json();
            console.error('Failed to load data:', error);
            showNotification(`Failed to load data: ${error.error}`, 'error');
            updateStatus('No data available. Please upload a transaction file.');
        }
    } catch (error) {
        console.error('Network error:', error);
        showNotification(`Failed to load data: ${error.message}`, 'error');
        updateStatus('Network error. Please check your connection and try again.');
    } finally {
        showLoading(false);
    }
}

function updateDashboard(data) {
    try {
        console.log('Updating dashboard with data:', data);
        updateStats(data);
        updateCategoryFilter(data.categories || {});
        updateCharts(data);
        updateTransactionsTable(data.filtered_data || []);
    } catch (error) {
        console.error('Error updating dashboard:', error);
        showNotification('Error updating dashboard display', 'error');
    }
}

function updateStats(data) {
    try {
        const { totals = {}, transaction_count = 0, largest_transaction = {} } = data;

        const spent = totals.spent || 0;
        const received = totals.received || 0;
        const netBalance = received - spent;
        const avgAmount = transaction_count > 0 ? (spent + received) / transaction_count : 0;

        if (totalSpentEl) totalSpentEl.textContent = `₹${formatNumber(spent)}`;
        if (totalReceivedEl) totalReceivedEl.textContent = `₹${formatNumber(received)}`;
        if (netBalanceEl) {
            netBalanceEl.textContent = `₹${formatNumber(Math.abs(netBalance))}`;
            netBalanceEl.style.color = netBalance >= 0 ? '#10b981' : '#ef4444';
        }
        if (transactionCountEl) transactionCountEl.textContent = formatNumber(transaction_count);
        if (avgAmountEl) avgAmountEl.textContent = `₹${formatNumber(avgAmount)}`;
        if (largestAmountEl) largestAmountEl.textContent = `₹${formatNumber(Math.abs(largest_transaction.amount || 0))}`;

        console.log('Stats updated');
    } catch (error) {
        console.error('Error updating stats:', error);
    }
}

function updateCategoryFilter(categories) {
    try {
        if (!categoryFilterEl) return;

        categoryFilterEl.innerHTML = '<option value="All">All Categories</option>';
        Object.keys(categories).forEach(category => {
            const option = document.createElement('option');
            option.value = category;
            option.textContent = category;
            categoryFilterEl.appendChild(option);
        });

        console.log('Category filter updated');
    } catch (error) {
        console.error('Error updating category filter:', error);
    }
}

function updateCharts(data) {
    try {
        console.log('Updating charts...');
        updateCategoryChart(data.categories || {});
        updateTrendsChart('daily', data.trends);
    } catch (error) {
        console.error('Error updating charts:', error);
    }
}

function updateCategoryChart(categories) {
    try {
        const canvas = document.getElementById('categoryChart');
        const messageEl = document.getElementById('categoryChartMessage');

        if (!canvas) {
            console.error('Category chart canvas not found');
            return;
        }

        // FIXED: Destroy existing chart properly
        if (categoryChart && typeof categoryChart.destroy === 'function') {
            categoryChart.destroy();
            categoryChart = null;
        }

        const labels = Object.keys(categories);
        const values = Object.values(categories);

        if (labels.length === 0) {
            if (messageEl) messageEl.textContent = 'No category data available';
            return;
        }

        if (messageEl) messageEl.style.display = 'none';

        const ctx = canvas.getContext('2d');

        // FIXED: Use proper Chart.js v4 syntax
        categoryChart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: labels,
                datasets: [{
                    data: values,
                    backgroundColor: pastelColors.slice(0, labels.length),
                    borderWidth: 0,
                    hoverBorderWidth: 3,
                    hoverBorderColor: '#fff'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            padding: 15,
                            usePointStyle: true,
                            font: {
                                size: 11
                            }
                        }
                    },
                    tooltip: {
                        callbacks: {
                            label: function (context) {
                                const value = context.parsed;
                                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                const percentage = ((value / total) * 100).toFixed(1);
                                return `${context.label}: ₹${formatNumber(value)} (${percentage}%)`;
                            }
                        }
                    }
                },
                cutout: '60%'
            }
        });

        console.log('Category chart updated successfully');
    } catch (error) {
        console.error('Error updating category chart:', error);
        const messageEl = document.getElementById('categoryChartMessage');
        if (messageEl) messageEl.textContent = 'Error loading chart';
    }
}

function updateTrendsChart(period = 'daily', trends = null) {
    try {
        const canvas = document.getElementById('trendsChart');
        const messageEl = document.getElementById('trendsChartMessage');

        if (!canvas) {
            console.error('Trends chart canvas not found');
            return;
        }

        // FIXED: Destroy existing chart properly
        if (trendsChart && typeof trendsChart.destroy === 'function') {
            trendsChart.destroy();
            trendsChart = null;
        }

        if (!trends && currentData) {
            trends = currentData.trends;
        }

        if (!trends || !trends[period] || trends[period].length === 0) {
            if (messageEl) messageEl.textContent = `No ${period} trend data available`;
            return;
        }

        if (messageEl) messageEl.style.display = 'none';

        const data = trends[period];
        const labels = data.map(item => {
            if (period === 'daily') {
                return item.Period ? new Date(item.Period).toLocaleDateString() : 'Unknown';
            } else {
                return item.Period || 'Unknown';
            }
        });
        const values = data.map(item => Math.abs(item.Amount || 0));

        const ctx = canvas.getContext('2d');

        // FIXED: Use proper Chart.js v4 syntax
        trendsChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Spending (₹)',
                    data: values,
                    borderColor: pastelColors[0],
                    backgroundColor: pastelColors[0] + '20',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4,
                    pointBackgroundColor: pastelColors[0],
                    pointBorderColor: '#fff',
                    pointBorderWidth: 2,
                    pointRadius: 5,
                    pointHoverRadius: 7
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        callbacks: {
                            label: function (context) {
                                return `₹${formatNumber(context.parsed.y)}`;
                            }
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            callback: function (value) {
                                return '₹' + formatNumber(value);
                            }
                        },
                        grid: {
                            color: 'rgba(0,0,0,0.1)'
                        }
                    },
                    x: {
                        grid: {
                            color: 'rgba(0,0,0,0.1)'
                        }
                    }
                }
            }
        });

        console.log(`${period} trends chart updated successfully`);
    } catch (error) {
        console.error('Error updating trends chart:', error);
        const messageEl = document.getElementById('trendsChartMessage');
        if (messageEl) messageEl.textContent = 'Error loading chart';
    }
}

function updateTransactionsTable(transactions) {
    try {
        const tbody = document.querySelector('#transactionsTable tbody');
        if (!tbody) return;

        if (!transactions || transactions.length === 0) {
            tbody.innerHTML = '<tr><td colspan="5" class="no-data">No transactions to display</td></tr>';
            return;
        }

        tbody.innerHTML = transactions.slice(0, 100).map(transaction => `
            <tr>
                <td>${formatDate(transaction.DateTime) || 'N/A'}</td>
                <td>${transaction['Transaction Details'] || 'N/A'}</td>
                <td>${transaction.Category || 'N/A'}</td>
                <td class="${(transaction.Amount < 0) ? 'amount-debit' : 'amount-credit'}">
                    ₹${formatNumber(Math.abs(transaction.Amount || 0))}
                </td>
                <td>
                    <span class="badge ${transaction.Type === 'Credit' ? 'badge-success' : 'badge-danger'}">
                        ${transaction.Type || 'Unknown'}
                    </span>
                </td>
            </tr>
        `).join('');

        console.log('Transactions table updated');
    } catch (error) {
        console.error('Error updating transactions table:', error);
    }
}

async function applyFilters() {
    if (!currentData) {
        showNotification('No data loaded. Please load data first.', 'error');
        return;
    }

    showLoading(true);
    updateStatus('Applying filters...');

    const filters = {
        min_amount: minAmountEl?.value || null,
        max_amount: maxAmountEl?.value || null,
        start_date: startDateEl?.value || null,
        end_date: endDateEl?.value || null,
        category: categoryFilterEl?.value === 'All' ? null : categoryFilterEl?.value,
        keyword: keywordSearchEl?.value || null
    };

    try {
        const response = await fetch('/filter', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(filters)
        });

        if (response.ok) {
            const filteredData = await response.json();
            updateDashboard(filteredData);
            showNotification('Filters applied successfully!', 'success');
            updateStatus(`Filters applied. Showing ${filteredData.transaction_count || 0} transactions.`);
        } else {
            const error = await response.json();
            showNotification(`Filter failed: ${error.error}`, 'error');
            updateStatus('Filter failed. Please try again.');
        }
    } catch (error) {
        console.error('Filter error:', error);
        showNotification(`Filter failed: ${error.message}`, 'error');
        updateStatus('Filter failed due to network error.');
    } finally {
        showLoading(false);
    }
}

function resetFilters() {
    try {
        if (minAmountEl) minAmountEl.value = '';
        if (maxAmountEl) maxAmountEl.value = '';
        if (startDateEl) startDateEl.value = '';
        if (endDateEl) endDateEl.value = '';
        if (categoryFilterEl) categoryFilterEl.value = 'All';
        if (keywordSearchEl) keywordSearchEl.value = '';

        if (currentData) {
            updateDashboard(currentData);
            showNotification('Filters reset!', 'success');
            updateStatus('Filters cleared. Showing all transactions.');
        }
    } catch (error) {
        console.error('Error resetting filters:', error);
    }
}

// Utility functions
function formatNumber(num) {
    if (typeof num !== 'number' || isNaN(num)) return '0';
    return num.toLocaleString('en-IN');
}

function formatDate(dateString) {
    if (!dateString) return 'N/A';
    try {
        const date = new Date(dateString);
        if (isNaN(date.getTime())) return 'N/A';
        return date.toLocaleDateString('en-IN') + ' ' + date.toLocaleTimeString('en-IN', {
            hour: '2-digit',
            minute: '2-digit'
        });
    } catch (error) {
        return 'N/A';
    }
}

function showLoading(show) {
    if (loadingSpinner) {
        loadingSpinner.style.display = show ? 'flex' : 'none';
    }
}

function updateStatus(message) {
    const statusEl = document.getElementById('statusMessage');
    if (statusEl) {
        statusEl.innerHTML = `<p>${message}</p>`;
        statusEl.style.display = 'block';
        setTimeout(() => {
            statusEl.style.display = 'none';
        }, 3000);
    }
}

function showNotification(message, type = 'info') {
    console.log(`${type.toUpperCase()}: ${message}`);

    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <div class="notification-content">
            <span>${message}</span>
            <button class="notification-close">&times;</button>
        </div>
    `;

    // Add notification styles if not present
    if (!document.querySelector('#notification-styles')) {
        const style = document.createElement('style');
        style.id = 'notification-styles';
        style.textContent = `
            .notification {
                position: fixed;
                top: 20px;
                right: 20px;
                padding: 1rem 1.5rem;
                border-radius: 0.5rem;
                box-shadow: 0 4px 12px rgba(0,0,0,0.15);
                z-index: 1000;
                max-width: 400px;
                animation: slideIn 0.3s ease;
            }
            .notification-success {
                background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
                color: #155724;
                border: 1px solid #c3e6cb;
            }
            .notification-error {
                background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);
                color: #721c24;
                border: 1px solid #f5c6cb;
            }
            .notification-info {
                background: linear-gradient(135deg, #a1c4fd 0%, #c2e9fb 100%);
                color: #0c5460;
                border: 1px solid #bee5eb;
            }
            .notification-content {
                display: flex;
                justify-content: space-between;
                align-items: center;
            }
            .notification-close {
                background: none;
                border: none;
                font-size: 1.5rem;
                cursor: pointer;
                margin-left: 1rem;
                opacity: 0.7;
            }
            .notification-close:hover {
                opacity: 1;
            }
            @keyframes slideIn {
                from { transform: translateX(100%); opacity: 0; }
                to { transform: translateX(0); opacity: 1; }
            }
            .chart-message {
                text-align: center;
                color: #666;
                font-style: italic;
                padding: 2rem;
            }
            .status-message {
                position: fixed;
                bottom: 20px;
                left: 50%;
                transform: translateX(-50%);
                background: rgba(255, 255, 255, 0.9);
                padding: 0.5rem 1rem;
                border-radius: 0.5rem;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                display: none;
                z-index: 999;
            }
            .badge {
                padding: 0.25rem 0.5rem;
                border-radius: 0.25rem;
                font-size: 0.75rem;
                font-weight: 600;
                text-transform: uppercase;
            }
            .badge-success {
                background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
                color: #155724;
            }
            .badge-danger {
                background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);
                color: #721c24;
            }
        `;
        document.head.appendChild(style);
    }

    document.body.appendChild(notification);

    // Auto remove after 5 seconds
    setTimeout(() => {
        if (notification.parentElement) {
            notification.remove();
        }
    }, 5000);

    // Manual close
    notification.querySelector('.notification-close').addEventListener('click', () => {
        notification.remove();
    });
}

// =============================================
// EXPORT, PRINT, AND THEME FUNCTIONS
// =============================================

function exportToCSV() {
    if (!currentData || !currentData.filtered_data || currentData.filtered_data.length === 0) {
        showNotification('No data to export. Please load transactions first.', 'error');
        return;
    }

    const transactions = currentData.filtered_data;
    const headers = ['Date', 'Details', 'Category', 'Amount', 'Type'];

    const csvRows = [
        headers.join(','),
        ...transactions.map(t => [
            `"${formatDate(t.DateTime) || 'N/A'}"`,
            `"${(t['Transaction Details'] || 'N/A').replace(/"/g, '""')}"`,
            `"${t.Category || 'N/A'}"`,
            Math.abs(t.Amount || 0),
            t.Type || 'Unknown'
        ].join(','))
    ];

    const csvContent = csvRows.join('\n');
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);

    const a = document.createElement('a');
    a.href = url;
    a.download = `transactions_${new Date().toISOString().split('T')[0]}.csv`;
    a.click();

    URL.revokeObjectURL(url);
    showNotification('CSV file downloaded successfully!', 'success');
}

function printReport() {
    if (!currentData) {
        showNotification('No data to print. Please load transactions first.', 'error');
        return;
    }

    // Create print-friendly content
    const printWindow = window.open('', '_blank');
    const totals = currentData.totals || {};
    const spent = totals.spent || 0;
    const received = totals.received || 0;

    printWindow.document.write(`
        <!DOCTYPE html>
        <html>
        <head>
            <title>Transaction Report</title>
            <style>
                body { font-family: Arial, sans-serif; padding: 20px; }
                h1 { color: #333; border-bottom: 2px solid #6366f1; padding-bottom: 10px; }
                .stats { display: flex; gap: 20px; margin: 20px 0; flex-wrap: wrap; }
                .stat-box { background: #f3f4f6; padding: 15px; border-radius: 8px; min-width: 150px; }
                .stat-value { font-size: 1.5rem; font-weight: bold; color: #6366f1; }
                .stat-label { color: #666; font-size: 0.9rem; }
                table { width: 100%; border-collapse: collapse; margin-top: 20px; }
                th, td { border: 1px solid #ddd; padding: 10px; text-align: left; }
                th { background: #6366f1; color: white; }
                tr:nth-child(even) { background: #f9f9f9; }
                .credit { color: #10b981; }
                .debit { color: #ef4444; }
                .footer { margin-top: 30px; color: #888; font-size: 0.8rem; }
            </style>
        </head>
        <body>
            <h1>💳 Transaction Report</h1>
            <p>Generated on ${new Date().toLocaleString()}</p>
            
            <div class="stats">
                <div class="stat-box">
                    <div class="stat-value">₹${formatNumber(spent)}</div>
                    <div class="stat-label">Total Spent</div>
                </div>
                <div class="stat-box">
                    <div class="stat-value">₹${formatNumber(received)}</div>
                    <div class="stat-label">Total Received</div>
                </div>
                <div class="stat-box">
                    <div class="stat-value">${currentData.transaction_count || 0}</div>
                    <div class="stat-label">Transactions</div>
                </div>
            </div>
            
            <table>
                <thead>
                    <tr>
                        <th>Date</th>
                        <th>Details</th>
                        <th>Category</th>
                        <th>Amount</th>
                        <th>Type</th>
                    </tr>
                </thead>
                <tbody>
                    ${(currentData.filtered_data || []).slice(0, 50).map(t => `
                        <tr>
                            <td>${formatDate(t.DateTime) || 'N/A'}</td>
                            <td>${t['Transaction Details'] || 'N/A'}</td>
                            <td>${t.Category || 'N/A'}</td>
                            <td class="${t.Type === 'Credit' ? 'credit' : 'debit'}">₹${formatNumber(Math.abs(t.Amount || 0))}</td>
                            <td>${t.Type || 'Unknown'}</td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
            
            <div class="footer">
                <p>Transaction Analyzer Report • ${currentData.transaction_count || 0} total transactions (showing first 50)</p>
            </div>
        </body>
        </html>
    `);

    printWindow.document.close();
    printWindow.print();
}

function toggleTheme() {
    isDarkMode = !isDarkMode;
    document.body.classList.toggle('dark-mode', isDarkMode);

    if (themeToggleBtn) {
        themeToggleBtn.textContent = isDarkMode ? '☀️' : '🌙';
    }

    localStorage.setItem('payment_analyzer_theme', isDarkMode ? 'dark' : 'light');
}

function loadTheme() {
    const savedTheme = localStorage.getItem('payment_analyzer_theme');
    if (savedTheme === 'dark') {
        isDarkMode = true;
        document.body.classList.add('dark-mode');
        if (themeToggleBtn) {
            themeToggleBtn.textContent = '☀️';
        }
    }
}
