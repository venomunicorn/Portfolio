// ============================================
// ATMOSPHERE - Weather App
// ============================================

// --- STATE ---
let isCelsius = true;
let currentCity = 'San Francisco';

// --- DOM ELEMENTS ---
const elements = {
    searchBtn: document.getElementById('searchBtn'),
    cityInput: document.getElementById('cityInput'),
    geoBtn: document.getElementById('geoBtn'),
    unitToggle: document.getElementById('unitToggle'),
    loading: document.getElementById('loading'),
    weatherContent: document.getElementById('weatherContent'),
    recentSearches: document.getElementById('recentSearches'),

    // Weather display
    weatherIcon: document.getElementById('weatherIcon'),
    tempValue: document.getElementById('tempValue'),
    unitLabel: document.getElementById('unitLabel'),
    condition: document.getElementById('condition'),
    locationName: document.getElementById('locationName'),
    dateTime: document.getElementById('dateTime'),

    // Details
    feelsLike: document.getElementById('feelsLike'),
    humidity: document.getElementById('humidity'),
    wind: document.getElementById('wind'),
    pressure: document.getElementById('pressure'),
    visibility: document.getElementById('visibility'),
    clouds: document.getElementById('clouds'),

    // Forecasts
    hourlyForecast: document.getElementById('hourlyForecast'),
    dailyForecast: document.getElementById('dailyForecast'),

    // Sun times
    sunrise: document.getElementById('sunrise'),
    sunset: document.getElementById('sunset'),
    sunPosition: document.getElementById('sunPosition')
};

// --- MOCK WEATHER DATA ---
const weatherDatabase = {
    'san francisco': {
        temp: 18, feelsLike: 16, humidity: 72, wind: 15, pressure: 1015, visibility: 12, clouds: 45,
        condition: 'Partly Cloudy', icon: 'fa-cloud-sun',
        sunrise: '6:52 AM', sunset: '4:54 PM',
        hourly: [18, 17, 16, 15, 14, 14, 15, 17, 19, 21, 22, 22],
        daily: [
            { day: 'Mon', high: 19, low: 12, icon: 'fa-cloud-sun' },
            { day: 'Tue', high: 21, low: 13, icon: 'fa-sun' },
            { day: 'Wed', high: 18, low: 11, icon: 'fa-cloud' },
            { day: 'Thu', high: 16, low: 10, icon: 'fa-cloud-rain' },
            { day: 'Fri', high: 17, low: 11, icon: 'fa-cloud-sun' }
        ]
    },
    'london': {
        temp: 8, feelsLike: 5, humidity: 85, wind: 22, pressure: 1008, visibility: 8, clouds: 90,
        condition: 'Rainy', icon: 'fa-cloud-showers-heavy',
        sunrise: '8:02 AM', sunset: '3:53 PM',
        hourly: [8, 7, 7, 6, 6, 5, 5, 6, 7, 8, 9, 9],
        daily: [
            { day: 'Mon', high: 9, low: 4, icon: 'fa-cloud-rain' },
            { day: 'Tue', high: 7, low: 3, icon: 'fa-cloud-showers-heavy' },
            { day: 'Wed', high: 8, low: 4, icon: 'fa-cloud' },
            { day: 'Thu', high: 10, low: 5, icon: 'fa-cloud-sun' },
            { day: 'Fri', high: 11, low: 6, icon: 'fa-sun' }
        ]
    },
    'new york': {
        temp: 2, feelsLike: -2, humidity: 55, wind: 18, pressure: 1022, visibility: 15, clouds: 20,
        condition: 'Clear & Cold', icon: 'fa-snowflake',
        sunrise: '7:16 AM', sunset: '4:32 PM',
        hourly: [2, 1, 0, -1, -2, -2, -1, 1, 3, 5, 6, 6],
        daily: [
            { day: 'Mon', high: 4, low: -2, icon: 'fa-snowflake' },
            { day: 'Tue', high: 6, low: 0, icon: 'fa-sun' },
            { day: 'Wed', high: 8, low: 2, icon: 'fa-cloud-sun' },
            { day: 'Thu', high: 5, low: -1, icon: 'fa-cloud' },
            { day: 'Fri', high: 3, low: -3, icon: 'fa-snowflake' }
        ]
    },
    'tokyo': {
        temp: 12, feelsLike: 10, humidity: 60, wind: 10, pressure: 1018, visibility: 14, clouds: 30,
        condition: 'Mostly Clear', icon: 'fa-moon',
        sunrise: '6:47 AM', sunset: '4:32 PM',
        hourly: [12, 11, 10, 9, 9, 8, 9, 11, 13, 15, 16, 15],
        daily: [
            { day: 'Mon', high: 14, low: 8, icon: 'fa-sun' },
            { day: 'Tue', high: 15, low: 9, icon: 'fa-cloud-sun' },
            { day: 'Wed', high: 13, low: 7, icon: 'fa-cloud' },
            { day: 'Thu', high: 12, low: 6, icon: 'fa-cloud-sun' },
            { day: 'Fri', high: 14, low: 8, icon: 'fa-sun' }
        ]
    },
    'dubai': {
        temp: 28, feelsLike: 30, humidity: 45, wind: 12, pressure: 1012, visibility: 20, clouds: 5,
        condition: 'Sunny', icon: 'fa-sun',
        sunrise: '6:58 AM', sunset: '5:35 PM',
        hourly: [28, 27, 26, 25, 24, 24, 25, 27, 30, 32, 33, 32],
        daily: [
            { day: 'Mon', high: 30, low: 22, icon: 'fa-sun' },
            { day: 'Tue', high: 31, low: 23, icon: 'fa-sun' },
            { day: 'Wed', high: 29, low: 21, icon: 'fa-cloud-sun' },
            { day: 'Thu', high: 28, low: 20, icon: 'fa-sun' },
            { day: 'Fri', high: 30, low: 22, icon: 'fa-sun' }
        ]
    },
    'mumbai': {
        temp: 32, feelsLike: 36, humidity: 78, wind: 8, pressure: 1010, visibility: 10, clouds: 40,
        condition: 'Hot & Humid', icon: 'fa-cloud-sun',
        sunrise: '6:58 AM', sunset: '6:05 PM',
        hourly: [32, 31, 30, 29, 28, 28, 29, 31, 33, 34, 35, 34],
        daily: [
            { day: 'Mon', high: 33, low: 26, icon: 'fa-cloud-sun' },
            { day: 'Tue', high: 34, low: 27, icon: 'fa-sun' },
            { day: 'Wed', high: 32, low: 25, icon: 'fa-cloud' },
            { day: 'Thu', high: 31, low: 24, icon: 'fa-cloud-rain' },
            { day: 'Fri', high: 33, low: 26, icon: 'fa-cloud-sun' }
        ]
    },
    'sydney': {
        temp: 26, feelsLike: 28, humidity: 65, wind: 14, pressure: 1014, visibility: 18, clouds: 25,
        condition: 'Warm & Clear', icon: 'fa-sun',
        sunrise: '5:39 AM', sunset: '8:06 PM',
        hourly: [26, 25, 24, 23, 22, 22, 23, 25, 27, 29, 30, 29],
        daily: [
            { day: 'Mon', high: 28, low: 20, icon: 'fa-sun' },
            { day: 'Tue', high: 30, low: 22, icon: 'fa-sun' },
            { day: 'Wed', high: 27, low: 19, icon: 'fa-cloud-sun' },
            { day: 'Thu', high: 25, low: 18, icon: 'fa-cloud' },
            { day: 'Fri', high: 26, low: 19, icon: 'fa-cloud-sun' }
        ]
    }
};

// Default weather
const defaultWeather = {
    temp: 24, feelsLike: 22, humidity: 48, wind: 12, pressure: 1013, visibility: 10, clouds: 35,
    condition: 'Partly Cloudy', icon: 'fa-cloud-sun',
    sunrise: '6:45 AM', sunset: '5:30 PM',
    hourly: [24, 23, 22, 21, 20, 19, 20, 22, 25, 27, 28, 27],
    daily: [
        { day: 'Mon', high: 26, low: 18, icon: 'fa-sun' },
        { day: 'Tue', high: 24, low: 17, icon: 'fa-cloud-sun' },
        { day: 'Wed', high: 22, low: 15, icon: 'fa-cloud' },
        { day: 'Thu', high: 23, low: 16, icon: 'fa-cloud-sun' },
        { day: 'Fri', high: 25, low: 17, icon: 'fa-sun' }
    ]
};

// --- INITIALIZATION ---
document.addEventListener('DOMContentLoaded', () => {
    setupEventListeners();
    loadRecentSearches();
    updateDateTime();
    fetchWeather('San Francisco');

    // Update time every minute
    setInterval(updateDateTime, 60000);
});

// --- EVENT LISTENERS ---
function setupEventListeners() {
    elements.searchBtn?.addEventListener('click', handleSearch);
    elements.cityInput?.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') handleSearch();
    });
    elements.geoBtn?.addEventListener('click', handleGeolocation);
    elements.unitToggle?.addEventListener('click', toggleUnit);

    // Recent search tags
    elements.recentSearches?.addEventListener('click', (e) => {
        if (e.target.classList.contains('recent-tag')) {
            const city = e.target.dataset.city;
            elements.cityInput.value = city;
            fetchWeather(city);
        }
    });
}

// --- SEARCH HANDLING ---
function handleSearch() {
    const city = elements.cityInput.value.trim();
    if (city) {
        fetchWeather(city);
        addToRecentSearches(city);
    }
}

function handleGeolocation() {
    if (navigator.geolocation) {
        showLoading();
        navigator.geolocation.getCurrentPosition(
            (position) => {
                // For demo, just show a random city
                const cities = ['San Francisco', 'New York', 'London', 'Tokyo', 'Dubai'];
                const randomCity = cities[Math.floor(Math.random() * cities.length)];
                fetchWeather(randomCity);
            },
            (error) => {
                hideLoading();
                alert('Unable to get location. Please search for a city.');
            }
        );
    }
}

// --- FETCH & DISPLAY WEATHER ---
function fetchWeather(city) {
    showLoading();
    currentCity = city;

    // Simulate API delay
    setTimeout(() => {
        const cityLower = city.toLowerCase();
        const data = weatherDatabase[cityLower] || defaultWeather;

        updateWeatherDisplay(data, city);
        updateHourlyForecast(data.hourly);
        updateDailyForecast(data.daily);

        hideLoading();
    }, 800);
}

function updateWeatherDisplay(data, city) {
    // Temperature
    const temp = isCelsius ? data.temp : celsiusToFahrenheit(data.temp);
    const feelsLike = isCelsius ? data.feelsLike : celsiusToFahrenheit(data.feelsLike);

    elements.tempValue.textContent = Math.round(temp);
    elements.unitLabel.textContent = isCelsius ? 'C' : 'F';
    elements.condition.textContent = data.condition;
    elements.locationName.textContent = formatCityName(city);

    // Icon
    elements.weatherIcon.innerHTML = `<i class="fas ${data.icon}"></i>`;

    // Details
    elements.feelsLike.textContent = `${Math.round(feelsLike)}°`;
    elements.humidity.textContent = `${data.humidity}%`;
    elements.wind.textContent = `${data.wind} km/h`;
    elements.pressure.textContent = `${data.pressure} hPa`;
    elements.visibility.textContent = `${data.visibility} km`;
    elements.clouds.textContent = `${data.clouds}%`;

    // Sun times
    elements.sunrise.textContent = data.sunrise;
    elements.sunset.textContent = data.sunset;

    // Update sun position (simplified)
    updateSunPosition();
}

function updateHourlyForecast(hourlyData) {
    const hours = ['Now', '1h', '2h', '3h', '4h', '5h', '6h', '7h', '8h', '9h', '10h', '11h'];
    const icons = ['fa-cloud-sun', 'fa-cloud', 'fa-cloud-sun', 'fa-moon', 'fa-moon', 'fa-moon',
        'fa-sun', 'fa-sun', 'fa-cloud-sun', 'fa-sun', 'fa-cloud-sun', 'fa-cloud'];

    let html = '';
    hourlyData.forEach((temp, index) => {
        const displayTemp = isCelsius ? temp : celsiusToFahrenheit(temp);
        html += `
            <div class="hourly-item ${index === 0 ? 'active' : ''}">
                <span class="hour">${hours[index]}</span>
                <i class="fas ${icons[index]}"></i>
                <span class="hourly-temp">${Math.round(displayTemp)}°</span>
            </div>
        `;
    });
    elements.hourlyForecast.innerHTML = html;
}

function updateDailyForecast(dailyData) {
    let html = '';
    dailyData.forEach((day, index) => {
        const high = isCelsius ? day.high : celsiusToFahrenheit(day.high);
        const low = isCelsius ? day.low : celsiusToFahrenheit(day.low);

        html += `
            <div class="daily-item" style="animation-delay: ${index * 0.1}s">
                <span class="day-name">${day.day}</span>
                <i class="fas ${day.icon}"></i>
                <div class="temp-range">
                    <span class="high">${Math.round(high)}°</span>
                    <div class="temp-bar">
                        <div class="temp-fill" style="width: ${((high - low) / 20) * 100}%"></div>
                    </div>
                    <span class="low">${Math.round(low)}°</span>
                </div>
            </div>
        `;
    });
    elements.dailyForecast.innerHTML = html;
}

function updateSunPosition() {
    const now = new Date();
    const hours = now.getHours();
    // Simplified calculation (assumes 6am sunrise, 6pm sunset)
    const progress = Math.max(0, Math.min(100, ((hours - 6) / 12) * 100));
    elements.sunPosition.style.left = `${progress}%`;
}

// --- UNIT TOGGLE ---
function toggleUnit() {
    isCelsius = !isCelsius;
    elements.unitToggle.textContent = isCelsius ? '°C' : '°F';

    // Refresh display
    const cityLower = currentCity.toLowerCase();
    const data = weatherDatabase[cityLower] || defaultWeather;
    updateWeatherDisplay(data, currentCity);
    updateHourlyForecast(data.hourly);
    updateDailyForecast(data.daily);
}

function celsiusToFahrenheit(celsius) {
    return (celsius * 9 / 5) + 32;
}

// --- RECENT SEARCHES ---
function loadRecentSearches() {
    const saved = localStorage.getItem('recentSearches');
    if (saved) {
        const searches = JSON.parse(saved);
        renderRecentSearches(searches);
    }
}

function addToRecentSearches(city) {
    let searches = JSON.parse(localStorage.getItem('recentSearches') || '[]');

    // Remove if exists and add to front
    searches = searches.filter(s => s.toLowerCase() !== city.toLowerCase());
    searches.unshift(city);

    // Keep max 5
    searches = searches.slice(0, 5);

    localStorage.setItem('recentSearches', JSON.stringify(searches));
    renderRecentSearches(searches);
}

function renderRecentSearches(searches) {
    let html = '';
    searches.forEach(city => {
        html += `<span class="recent-tag" data-city="${city}">${city}</span>`;
    });
    elements.recentSearches.innerHTML = html;
}

// --- UTILITIES ---
function showLoading() {
    elements.loading.style.display = 'flex';
    elements.weatherContent.style.opacity = '0.3';
}

function hideLoading() {
    elements.loading.style.display = 'none';
    elements.weatherContent.style.opacity = '1';
}

function updateDateTime() {
    const now = new Date();
    const options = { weekday: 'long', month: 'short', day: 'numeric' };
    elements.dateTime.textContent = now.toLocaleDateString('en-US', options);
}

function formatCityName(city) {
    return city.split(' ').map(word =>
        word.charAt(0).toUpperCase() + word.slice(1).toLowerCase()
    ).join(' ');
}
