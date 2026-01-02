// ============================================
// NEURO VISION - TensorFlow.js Image Classifier
// ============================================

// --- STATE ---
let model = null;
let isModelLoaded = false;
let scanHistory = [];
let cameraStream = null;

// --- DOM ELEMENTS ---
const dropZone = document.getElementById('dropZone');
const fileInput = document.getElementById('fileInput');
const placeholder = document.getElementById('placeholder');
const previewImg = document.getElementById('previewImg');
const scannerOverlay = document.getElementById('scannerOverlay');
const statusPanel = document.getElementById('statusPanel');
const progressFill = document.getElementById('progressFill');
const processingText = document.getElementById('processingText');
const resultCard = document.getElementById('resultCard');
const predictionsList = document.getElementById('predictionsList');
const resultTime = document.getElementById('resultTime');
const historyList = document.getElementById('historyList');
const modelStatus = document.getElementById('modelStatus');
const statusText = document.getElementById('statusText');
const statusDot = modelStatus.querySelector('.status-dot');

// Buttons
const btnUpload = document.getElementById('btnUpload');
const btnCamera = document.getElementById('btnCamera');
const btnScanNew = document.getElementById('btnScanNew');
const btnExport = document.getElementById('btnExport');
const clearHistory = document.getElementById('clearHistory');

// Camera elements
const cameraModal = document.getElementById('cameraModal');
const cameraVideo = document.getElementById('cameraVideo');
const btnCapture = document.getElementById('btnCapture');
const closeCamera = document.getElementById('closeCamera');
const captureCanvas = document.getElementById('captureCanvas');

// --- INITIALIZATION ---
document.addEventListener('DOMContentLoaded', async () => {
    loadHistory();
    renderHistory();
    await loadModel();
    setupEventListeners();
});

// --- LOAD TENSORFLOW MODEL ---
async function loadModel() {
    try {
        statusText.textContent = 'Loading MobileNet...';
        model = await mobilenet.load({ version: 2, alpha: 1.0 });
        isModelLoaded = true;
        statusDot.classList.remove('loading');
        statusDot.classList.add('ready');
        statusText.textContent = 'Model Ready';
        console.log('MobileNet loaded successfully');
    } catch (error) {
        console.error('Error loading model:', error);
        statusDot.classList.remove('loading');
        statusDot.classList.add('error');
        statusText.textContent = 'Model Failed';
    }
}

// --- EVENT LISTENERS ---
function setupEventListeners() {
    // File input
    btnUpload.addEventListener('click', (e) => {
        e.stopPropagation();
        fileInput.click();
    });

    dropZone.addEventListener('click', () => {
        if (!placeholder.classList.contains('hidden')) {
            fileInput.click();
        }
    });

    fileInput.addEventListener('change', handleFile);

    // Drag and drop
    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('dragover');
    });

    dropZone.addEventListener('dragleave', (e) => {
        e.preventDefault();
        dropZone.classList.remove('dragover');
    });

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('dragover');
        const file = e.dataTransfer.files[0];
        if (file && file.type.startsWith('image/')) {
            processFile(file);
        }
    });

    // Camera
    btnCamera.addEventListener('click', (e) => {
        e.stopPropagation();
        openCamera();
    });

    closeCamera.addEventListener('click', closeModalCamera);
    btnCapture.addEventListener('click', capturePhoto);

    // Results actions
    btnScanNew.addEventListener('click', resetScanner);
    btnExport.addEventListener('click', exportResults);

    // History
    clearHistory.addEventListener('click', clearHistoryData);
}

// --- FILE HANDLING ---
function handleFile(e) {
    const file = e.target.files[0];
    if (file) processFile(file);
}

function processFile(file) {
    const reader = new FileReader();
    reader.onload = (e) => {
        previewImg.src = e.target.result;
        placeholder.classList.add('hidden');
        previewImg.classList.remove('hidden');
        startClassification();
    };
    reader.readAsDataURL(file);
}

// --- CLASSIFICATION ---
async function startClassification() {
    if (!isModelLoaded) {
        alert('Model is still loading. Please wait.');
        return;
    }

    resultCard.classList.add('hidden');
    scannerOverlay.classList.remove('hidden');
    statusPanel.classList.remove('hidden');
    progressFill.style.width = '0%';

    // Simulate scanning animation
    const stages = [
        'initializing tensors...',
        'extracting features...',
        'analyzing patterns...',
        'computing probabilities...',
        'finalizing results...'
    ];

    let progress = 0;
    let stageIndex = 0;

    const interval = setInterval(() => {
        progress += Math.random() * 15 + 5;
        if (progress > 95) progress = 95;

        progressFill.style.width = progress + '%';

        const newStage = Math.floor((progress / 100) * stages.length);
        if (newStage !== stageIndex && newStage < stages.length) {
            stageIndex = newStage;
            processingText.textContent = stages[stageIndex];
        }
    }, 150);

    try {
        // Wait for image to load
        await new Promise(resolve => {
            if (previewImg.complete) resolve();
            else previewImg.onload = resolve;
        });

        // Run classification
        const predictions = await model.classify(previewImg, 5);

        clearInterval(interval);
        progressFill.style.width = '100%';
        processingText.textContent = 'complete!';

        setTimeout(() => {
            scannerOverlay.classList.add('hidden');
            statusPanel.classList.add('hidden');
            showResults(predictions);
        }, 500);

    } catch (error) {
        console.error('Classification error:', error);
        clearInterval(interval);
        alert('Error during classification. Please try again.');
        resetScanner();
    }
}

// --- SHOW RESULTS ---
function showResults(predictions) {
    const timestamp = new Date().toLocaleTimeString();
    resultTime.textContent = timestamp;

    // Build predictions HTML
    predictionsList.innerHTML = predictions.map((pred, index) => {
        const confidence = (pred.probability * 100).toFixed(1);
        const label = formatLabel(pred.className);

        return `
            <div class="prediction-item" style="animation-delay: ${index * 0.1}s">
                <div class="prediction-rank">#${index + 1}</div>
                <div class="prediction-content">
                    <div class="prediction-label">${label}</div>
                    <div class="confidence-bar-container">
                        <div class="confidence-bar">
                            <div class="confidence-fill" style="width: ${confidence}%"></div>
                        </div>
                        <span class="confidence-value">${confidence}%</span>
                    </div>
                </div>
            </div>
        `;
    }).join('');

    resultCard.classList.remove('hidden');

    // Save to history
    addToHistory(predictions[0], previewImg.src);
}

function formatLabel(className) {
    // MobileNet returns comma-separated labels, take the first one
    const parts = className.split(',');
    return parts[0].trim().replace(/_/g, ' ');
}

// --- HISTORY MANAGEMENT ---
function addToHistory(topPrediction, imageSrc) {
    const entry = {
        id: Date.now(),
        label: formatLabel(topPrediction.className),
        confidence: (topPrediction.probability * 100).toFixed(1),
        timestamp: new Date().toLocaleString(),
        thumbnail: imageSrc
    };

    scanHistory.unshift(entry);
    if (scanHistory.length > 10) scanHistory.pop();

    saveHistory();
    renderHistory();
}

function renderHistory() {
    if (scanHistory.length === 0) {
        historyList.innerHTML = '<div class="history-empty">No scans yet</div>';
        return;
    }

    historyList.innerHTML = scanHistory.map(entry => `
        <div class="history-item" data-id="${entry.id}">
            <img src="${entry.thumbnail}" alt="Scan" class="history-thumb">
            <div class="history-info">
                <div class="history-label">${entry.label}</div>
                <div class="history-meta">${entry.confidence}% • ${entry.timestamp}</div>
            </div>
        </div>
    `).join('');
}

function saveHistory() {
    localStorage.setItem('neurovision_history', JSON.stringify(scanHistory));
}

function loadHistory() {
    const saved = localStorage.getItem('neurovision_history');
    scanHistory = saved ? JSON.parse(saved) : [];
}

function clearHistoryData() {
    scanHistory = [];
    saveHistory();
    renderHistory();
}

// --- CAMERA FUNCTIONS ---
async function openCamera() {
    try {
        cameraStream = await navigator.mediaDevices.getUserMedia({
            video: { facingMode: 'environment' }
        });
        cameraVideo.srcObject = cameraStream;
        cameraModal.classList.remove('hidden');
    } catch (error) {
        console.error('Camera error:', error);
        alert('Unable to access camera. Please check permissions.');
    }
}

function closeModalCamera() {
    if (cameraStream) {
        cameraStream.getTracks().forEach(track => track.stop());
        cameraStream = null;
    }
    cameraModal.classList.add('hidden');
}

function capturePhoto() {
    captureCanvas.width = cameraVideo.videoWidth;
    captureCanvas.height = cameraVideo.videoHeight;
    const ctx = captureCanvas.getContext('2d');
    ctx.drawImage(cameraVideo, 0, 0);

    const dataUrl = captureCanvas.toDataURL('image/jpeg');
    previewImg.src = dataUrl;
    placeholder.classList.add('hidden');
    previewImg.classList.remove('hidden');

    closeModalCamera();
    startClassification();
}

// --- EXPORT RESULTS ---
function exportResults() {
    const currentPredictions = [];
    predictionsList.querySelectorAll('.prediction-item').forEach(item => {
        const label = item.querySelector('.prediction-label').textContent;
        const conf = item.querySelector('.confidence-value').textContent;
        currentPredictions.push({ label, confidence: conf });
    });

    const exportData = {
        timestamp: new Date().toISOString(),
        predictions: currentPredictions
    };

    const blob = new Blob([JSON.stringify(exportData, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `neurovision_results_${Date.now()}.json`;
    a.click();
    URL.revokeObjectURL(url);
}

// --- RESET ---
function resetScanner() {
    resultCard.classList.add('hidden');
    placeholder.classList.remove('hidden');
    previewImg.classList.add('hidden');
    previewImg.src = '';
    fileInput.value = '';
}
