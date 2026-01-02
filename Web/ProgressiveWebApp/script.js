// ============================================
// MULTICONVERT - Progressive Web App
// ============================================

// --- CONVERSION DATA ---
const units = {
    length: {
        meters: { name: 'Meters', symbol: 'm', toBase: 1 },
        kilometers: { name: 'Kilometers', symbol: 'km', toBase: 1000 },
        centimeters: { name: 'Centimeters', symbol: 'cm', toBase: 0.01 },
        millimeters: { name: 'Millimeters', symbol: 'mm', toBase: 0.001 },
        feet: { name: 'Feet', symbol: 'ft', toBase: 0.3048 },
        inches: { name: 'Inches', symbol: 'in', toBase: 0.0254 },
        yards: { name: 'Yards', symbol: 'yd', toBase: 0.9144 },
        miles: { name: 'Miles', symbol: 'mi', toBase: 1609.344 }
    },
    weight: {
        kilograms: { name: 'Kilograms', symbol: 'kg', toBase: 1 },
        grams: { name: 'Grams', symbol: 'g', toBase: 0.001 },
        milligrams: { name: 'Milligrams', symbol: 'mg', toBase: 0.000001 },
        pounds: { name: 'Pounds', symbol: 'lb', toBase: 0.453592 },
        ounces: { name: 'Ounces', symbol: 'oz', toBase: 0.0283495 },
        tons: { name: 'Metric Tons', symbol: 't', toBase: 1000 }
    },
    temperature: {
        celsius: { name: 'Celsius', symbol: '°C' },
        fahrenheit: { name: 'Fahrenheit', symbol: '°F' },
        kelvin: { name: 'Kelvin', symbol: 'K' }
    }
};

// Quick reference data
const quickRef = {
    length: [
        { from: '1 km', to: '0.621 mi' },
        { from: '1 m', to: '3.281 ft' },
        { from: '1 inch', to: '2.54 cm' }
    ],
    weight: [
        { from: '1 kg', to: '2.205 lb' },
        { from: '1 lb', to: '453.6 g' },
        { from: '1 oz', to: '28.35 g' }
    ],
    temperature: [
        { from: '0°C', to: '32°F' },
        { from: '100°C', to: '212°F' },
        { from: '0 K', to: '-273.15°C' }
    ]
};

// --- STATE ---
let currentCategory = 'length';
let history = [];
let isDarkMode = false;
let deferredPrompt = null;

// --- DOM ELEMENTS ---
const fromUnitSelect = document.getElementById('fromUnit');
const toUnitSelect = document.getElementById('toUnit');
const fromValue = document.getElementById('fromValue');
const toValue = document.getElementById('toValue');
const swapBtn = document.getElementById('swapBtn');
const tabBtns = document.querySelectorAll('.tab-btn');
const referenceGrid = document.getElementById('referenceGrid');
const historyList = document.getElementById('historyList');
const clearHistoryBtn = document.getElementById('clearHistory');
const themeToggle = document.getElementById('themeToggle');
const installBtn = document.getElementById('installBtn');
const offlineBanner = document.getElementById('offlineBanner');

// --- INITIALIZATION ---
document.addEventListener('DOMContentLoaded', () => {
    loadTheme();
    loadHistory();
    setupEventListeners();
    loadCategory('length');
    setupPWA();
    checkOnlineStatus();
});

// --- EVENT LISTENERS ---
function setupEventListeners() {
    // Tabs
    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            tabBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            loadCategory(btn.dataset.category);
        });
    });

    // Conversion
    fromValue.addEventListener('input', convert);
    fromUnitSelect.addEventListener('change', convert);
    toUnitSelect.addEventListener('change', convert);

    // Swap
    swapBtn.addEventListener('click', swapUnits);

    // History
    clearHistoryBtn.addEventListener('click', clearHistory);

    // Theme
    themeToggle.addEventListener('click', toggleTheme);

    // Install
    installBtn.addEventListener('click', installApp);

    // Online/Offline
    window.addEventListener('online', checkOnlineStatus);
    window.addEventListener('offline', checkOnlineStatus);
}

// --- CATEGORY LOADING ---
function loadCategory(category) {
    currentCategory = category;
    const categoryUnits = units[category];

    // Clear and populate selects
    fromUnitSelect.innerHTML = '';
    toUnitSelect.innerHTML = '';

    Object.entries(categoryUnits).forEach(([key, unit], index) => {
        const option1 = new Option(`${unit.name} (${unit.symbol})`, key);
        const option2 = new Option(`${unit.name} (${unit.symbol})`, key);
        fromUnitSelect.add(option1);
        toUnitSelect.add(option2);

        // Default second option selected for 'to'
        if (index === 1) toUnitSelect.value = key;
    });

    // Update quick reference
    loadQuickReference(category);

    // Clear values
    fromValue.value = '';
    toValue.value = '';
}

function loadQuickReference(category) {
    const refs = quickRef[category];
    referenceGrid.innerHTML = refs.map(ref => `
        <div class="ref-item">
            <span class="ref-from">${ref.from}</span>
            <i class="fas fa-arrow-right"></i>
            <span class="ref-to">${ref.to}</span>
        </div>
    `).join('');
}

// --- CONVERSION ---
function convert() {
    const value = parseFloat(fromValue.value);
    if (isNaN(value)) {
        toValue.value = '';
        return;
    }

    const from = fromUnitSelect.value;
    const to = toUnitSelect.value;

    let result;

    if (currentCategory === 'temperature') {
        result = convertTemperature(value, from, to);
    } else {
        const fromUnit = units[currentCategory][from];
        const toUnit = units[currentCategory][to];
        const baseValue = value * fromUnit.toBase;
        result = baseValue / toUnit.toBase;
    }

    // Format result
    toValue.value = formatNumber(result);

    // Add to history
    addToHistory(value, from, result, to);
}

function convertTemperature(value, from, to) {
    // Convert to Celsius first
    let celsius;
    switch (from) {
        case 'celsius': celsius = value; break;
        case 'fahrenheit': celsius = (value - 32) * 5 / 9; break;
        case 'kelvin': celsius = value - 273.15; break;
    }

    // Convert from Celsius to target
    switch (to) {
        case 'celsius': return celsius;
        case 'fahrenheit': return celsius * 9 / 5 + 32;
        case 'kelvin': return celsius + 273.15;
    }
}

function formatNumber(num) {
    if (Math.abs(num) >= 1000000 || (Math.abs(num) < 0.001 && num !== 0)) {
        return num.toExponential(4);
    }
    return parseFloat(num.toPrecision(8)).toString();
}

// --- SWAP UNITS ---
function swapUnits() {
    const tempUnit = fromUnitSelect.value;
    fromUnitSelect.value = toUnitSelect.value;
    toUnitSelect.value = tempUnit;

    // Also swap values
    const tempValue = fromValue.value;
    fromValue.value = toValue.value;
    toValue.value = tempValue;

    // Animate button
    swapBtn.classList.add('spinning');
    setTimeout(() => swapBtn.classList.remove('spinning'), 300);

    convert();
}

// --- HISTORY ---
function addToHistory(fromVal, fromUnit, toVal, toUnit) {
    const fromSymbol = units[currentCategory][fromUnit].symbol;
    const toSymbol = units[currentCategory][toUnit].symbol;

    const entry = {
        id: Date.now(),
        text: `${fromVal} ${fromSymbol} = ${formatNumber(toVal)} ${toSymbol}`,
        category: currentCategory,
        timestamp: new Date().toLocaleTimeString()
    };

    // Avoid duplicates
    if (history.length > 0 && history[0].text === entry.text) return;

    history.unshift(entry);
    if (history.length > 10) history.pop();

    saveHistory();
    renderHistory();
}

function renderHistory() {
    if (history.length === 0) {
        historyList.innerHTML = '<p class="history-empty">No conversions yet</p>';
        return;
    }

    historyList.innerHTML = history.map(entry => `
        <div class="history-item">
            <span class="history-text">${entry.text}</span>
            <span class="history-time">${entry.timestamp}</span>
        </div>
    `).join('');
}

function clearHistory() {
    history = [];
    saveHistory();
    renderHistory();
}

function saveHistory() {
    localStorage.setItem('multiconvert_history', JSON.stringify(history));
}

function loadHistory() {
    const saved = localStorage.getItem('multiconvert_history');
    history = saved ? JSON.parse(saved) : [];
    renderHistory();
}

// --- THEME ---
function toggleTheme() {
    isDarkMode = !isDarkMode;
    document.body.classList.toggle('dark-mode', isDarkMode);
    themeToggle.innerHTML = isDarkMode ? '<i class="fas fa-sun"></i>' : '<i class="fas fa-moon"></i>';
    localStorage.setItem('multiconvert_theme', isDarkMode ? 'dark' : 'light');
}

function loadTheme() {
    const saved = localStorage.getItem('multiconvert_theme');
    if (saved === 'dark') {
        isDarkMode = true;
        document.body.classList.add('dark-mode');
        themeToggle.innerHTML = '<i class="fas fa-sun"></i>';
    }
}

// --- PWA ---
function setupPWA() {
    // Register service worker
    if ('serviceWorker' in navigator) {
        navigator.serviceWorker.register('sw.js')
            .then(reg => {
                console.log('Service Worker registered');

                // Check for updates
                reg.addEventListener('updatefound', () => {
                    const newWorker = reg.installing;
                    newWorker.addEventListener('statechange', () => {
                        if (newWorker.state === 'installed' && navigator.serviceWorker.controller) {
                            showUpdateNotification();
                        }
                    });
                });
            })
            .catch(err => console.error('SW registration failed:', err));
    }

    // Install prompt
    window.addEventListener('beforeinstallprompt', (e) => {
        e.preventDefault();
        deferredPrompt = e;
        installBtn.classList.remove('hidden');
    });

    window.addEventListener('appinstalled', () => {
        installBtn.classList.add('hidden');
        deferredPrompt = null;
    });
}

function installApp() {
    if (deferredPrompt) {
        deferredPrompt.prompt();
        deferredPrompt.userChoice.then(choice => {
            if (choice.outcome === 'accepted') {
                console.log('App installed');
            }
            deferredPrompt = null;
            installBtn.classList.add('hidden');
        });
    }
}

function showUpdateNotification() {
    const banner = document.createElement('div');
    banner.className = 'update-banner';
    banner.innerHTML = `
        <span>New version available!</span>
        <button onclick="location.reload()">Update</button>
    `;
    document.body.prepend(banner);
}

function checkOnlineStatus() {
    if (navigator.onLine) {
        offlineBanner.classList.remove('visible');
    } else {
        offlineBanner.classList.add('visible');
    }
}
