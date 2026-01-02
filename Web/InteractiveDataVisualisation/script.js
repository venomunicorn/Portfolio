// ============================================
// INTERACTIVE DATA VISUALIZATION DASHBOARD
// ============================================

// --- DATASETS ---
const datasets = {
    population: {
        name: 'World Population',
        unit: 'billion',
        labels: ['1950', '1960', '1970', '1980', '1990', '2000', '2010', '2020'],
        data: [2.5, 3.0, 3.7, 4.4, 5.3, 6.1, 6.9, 7.8],
        colors: ['#4361ee', '#3a0ca3', '#7209b7', '#f72585', '#4cc9f0', '#4895ef', '#560bad', '#480ca8'],
        stats: {
            current: '7.8B',
            change: '+1.3%',
            positive: true,
            description: 'Global population growth rate'
        }
    },
    gdp: {
        name: 'World GDP',
        unit: 'trillion USD',
        labels: ['1960', '1970', '1980', '1990', '2000', '2010', '2020', '2023'],
        data: [1.4, 3.4, 11.2, 22.6, 33.8, 66.0, 84.7, 105.0],
        colors: ['#10b981', '#059669', '#047857', '#065f46', '#34d399', '#6ee7b7', '#a7f3d0', '#d1fae5'],
        stats: {
            current: '$105T',
            change: '+3.1%',
            positive: true,
            description: 'Gross Domestic Product'
        }
    },
    co2: {
        name: 'CO₂ Emissions',
        unit: 'billion tonnes',
        labels: ['1960', '1970', '1980', '1990', '2000', '2010', '2020', '2023'],
        data: [9.4, 14.9, 19.5, 22.7, 25.2, 33.4, 34.8, 37.1],
        colors: ['#ef4444', '#dc2626', '#b91c1c', '#991b1b', '#f87171', '#fca5a5', '#fecaca', '#fee2e2'],
        stats: {
            current: '37.1B',
            change: '+1.1%',
            positive: false,
            description: 'Annual carbon dioxide emissions'
        }
    },
    internet: {
        name: 'Internet Users',
        unit: '% of population',
        labels: ['1995', '2000', '2005', '2010', '2015', '2020', '2022', '2024'],
        data: [0.8, 6.8, 16.0, 30.0, 43.0, 60.0, 63.0, 67.0],
        colors: ['#f59e0b', '#d97706', '#b45309', '#92400e', '#fbbf24', '#fcd34d', '#fde68a', '#fef3c7'],
        stats: {
            current: '67%',
            change: '+4.0%',
            positive: true,
            description: 'Global internet penetration'
        }
    }
};

// --- STATE ---
let currentDataset = 'population';
let currentChartType = 'bar';
let chartInstance = null;

// --- DOM ELEMENTS ---
const chartCanvas = document.getElementById('mainChart');
const ctx = chartCanvas.getContext('2d');

// --- INITIALIZATION ---
document.addEventListener('DOMContentLoaded', () => {
    updateStats();
    renderChart();
    setupEventListeners();
});

function setupEventListeners() {
    // Dataset selector
    document.getElementById('datasetSelect').addEventListener('change', (e) => {
        currentDataset = e.target.value;
        updateStats();
        renderChart();
    });

    // Chart type buttons
    document.querySelectorAll('.chart-type-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.chart-type-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            currentChartType = btn.dataset.type;
            renderChart();
        });
    });

    // Download button
    document.getElementById('downloadBtn').addEventListener('click', downloadChart);
}

// --- UPDATE STATS ---
function updateStats() {
    const data = datasets[currentDataset];

    // Calculate derived stats
    const latest = data.data[data.data.length - 1];
    const previous = data.data[data.data.length - 2];
    const avg = (data.data.reduce((a, b) => a + b, 0) / data.data.length).toFixed(1);
    const max = Math.max(...data.data);
    const min = Math.min(...data.data);

    document.getElementById('stat-current').textContent = data.stats.current;
    document.getElementById('stat-current-change').textContent = data.stats.change;
    document.getElementById('stat-current-change').className =
        `stat-change ${data.stats.positive ? 'positive' : 'negative'}`;

    document.getElementById('stat-avg').textContent = avg + (data.unit === 'billion' || data.unit === 'billion tonnes' ? 'B' : data.unit === 'trillion USD' ? 'T' : '%');
    document.getElementById('stat-max').textContent = max + (data.unit === 'billion' || data.unit === 'billion tonnes' ? 'B' : data.unit === 'trillion USD' ? 'T' : '%');
    document.getElementById('stat-min').textContent = min + (data.unit === 'billion' || data.unit === 'billion tonnes' ? 'B' : data.unit === 'trillion USD' ? 'T' : '%');

    document.getElementById('chart-title').textContent = data.name + ' Over Time';
}

// --- RENDER CHART ---
function renderChart() {
    if (chartInstance) {
        chartInstance.destroy();
    }

    const data = datasets[currentDataset];

    const chartConfig = {
        type: currentChartType,
        data: {
            labels: data.labels,
            datasets: [{
                label: `${data.name} (${data.unit})`,
                data: data.data,
                backgroundColor: currentChartType === 'line'
                    ? createGradient(data.colors[0])
                    : data.colors.map(c => c + 'cc'),
                borderColor: data.colors[0],
                borderWidth: 2,
                fill: currentChartType === 'line',
                tension: 0.4,
                pointBackgroundColor: data.colors[0],
                pointBorderColor: '#fff',
                pointBorderWidth: 2,
                pointRadius: 5,
                pointHoverRadius: 8
            }]
        },
        options: getChartOptions(data)
    };

    chartInstance = new Chart(ctx, chartConfig);
}

function createGradient(color) {
    const gradient = ctx.createLinearGradient(0, 0, 0, 400);
    gradient.addColorStop(0, color + '80');
    gradient.addColorStop(1, color + '10');
    return gradient;
}

function getChartOptions(data) {
    const baseOptions = {
        responsive: true,
        maintainAspectRatio: false,
        animation: {
            duration: 1000,
            easing: 'easeOutQuart'
        },
        plugins: {
            legend: {
                display: true,
                position: 'top',
                labels: {
                    color: '#a0a0b0',
                    font: { size: 12 },
                    padding: 20
                }
            },
            tooltip: {
                backgroundColor: 'rgba(26, 26, 46, 0.95)',
                titleColor: '#fff',
                bodyColor: '#a0a0b0',
                borderColor: '#4361ee',
                borderWidth: 1,
                padding: 12,
                displayColors: false,
                callbacks: {
                    label: function (context) {
                        return `${context.parsed.y || context.parsed} ${data.unit}`;
                    }
                }
            }
        }
    };

    // Add scales for bar/line charts
    if (currentChartType === 'bar' || currentChartType === 'line') {
        baseOptions.scales = {
            x: {
                grid: {
                    color: 'rgba(255,255,255,0.05)'
                },
                ticks: {
                    color: '#a0a0b0'
                }
            },
            y: {
                beginAtZero: true,
                grid: {
                    color: 'rgba(255,255,255,0.05)'
                },
                ticks: {
                    color: '#a0a0b0',
                    callback: function (value) {
                        return value + (data.unit.includes('%') ? '%' : '');
                    }
                }
            }
        };
    }

    return baseOptions;
}

// --- DOWNLOAD CHART ---
function downloadChart() {
    const link = document.createElement('a');
    link.download = `${datasets[currentDataset].name.replace(/\s+/g, '_')}_chart.png`;
    link.href = chartCanvas.toDataURL('image/png');
    link.click();
}

// --- NAV ITEMS ---
document.querySelectorAll('.nav-item').forEach(item => {
    item.addEventListener('click', () => {
        document.querySelectorAll('.nav-item').forEach(i => i.classList.remove('active'));
        item.classList.add('active');
    });
});
