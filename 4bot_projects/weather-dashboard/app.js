// Weather Dashboard App - Main JavaScript File
// Handles API integration, geolocation, and DOM manipulation

class WeatherDashboard {
    constructor() {
        this.apiKey = window.CONFIG?.API_KEY || 'demo-key';
        this.apiUrl = 'https://api.openweathermap.org/data/2.5';
        this.currentLocationData = null;
        this.init();
    }

    // Initialize the application
    init() {
        this.bindEvents();
        this.loadWeatherData();
    }

    // Bind event listeners
    bindEvents() {
        const refreshBtn = document.getElementById('refresh-btn');
        const locationBtn = document.getElementById('location-btn');
        
        if (refreshBtn) {
            refreshBtn.addEventListener('click', () => this.loadWeatherData());
        }
        
        if (locationBtn) {
            locationBtn.addEventListener('click', () => this.getCurrentLocation());
        }

        // Handle window resize for responsive updates
        window.addEventListener('resize', this.debounce(() => {
            this.updateLayout();
        }, 250));
    }

    // Load weather data - try cached location first, then geolocation
    async loadWeatherData() {
        this.showLoading();
        
        try {
            // Try to get cached location first
            const cachedLocation = this.getCachedLocation();
            
            if (cachedLocation) {
                await this.fetchWeatherByCoords(cachedLocation.lat, cachedLocation.lon);
            } else {
                await this.getCurrentLocation();
            }
        } catch (error) {
            this.handleError('Failed to load weather data', error);
        }
    }

    // Get user's current location using geolocation API
    getCurrentLocation() {
        return new Promise((resolve, reject) => {
            if (!navigator.geolocation) {
                reject(new Error('Geolocation is not supported by this browser'));
                return;
            }

            const options = {
                enableHighAccuracy: true,
                timeout: 10000,
                maximumAge: 300000 // 5 minutes
            };

            navigator.geolocation.getCurrentPosition(
                async (position) => {
                    const { latitude, longitude } = position.coords;
                    
                    // Cache the location
                    this.cacheLocation(latitude, longitude);
                    
                    try {
                        await this.fetchWeatherByCoords(latitude, longitude);
                        resolve();
                    } catch (error) {
                        reject(error);
                    }
                },
                (error) => {
                    // Fallback to default location (New York) if geolocation fails
                    console.warn('Geolocation failed, using default location:', error.message);
                    this.fetchWeatherByCoords(40.7128, -74.0060);
                    reject(error);
                },
                options
            );
        });
    }

    // Fetch weather data by coordinates
    async fetchWeatherByCoords(lat, lon) {
        try {
            // Fetch current weather and forecast in parallel
            const [currentWeather, forecast] = await Promise.all([
                this.fetchCurrentWeather(lat, lon),
                this.fetchForecast(lat, lon)
            ]);

            this.currentLocationData = { lat, lon };
            this.renderCurrentWeather(currentWeather);
            this.renderForecast(forecast);
            this.hideLoading();
            
        } catch (error) {
            this.handleError('Failed to fetch weather data', error);
        }
    }

    // Fetch current weather data
    async fetchCurrentWeather(lat, lon) {
        const url = `${this.apiUrl}/weather?lat=${lat}&lon=${lon}&appid=${this.apiKey}&units=metric`;
        const response = await fetch(url);
        
        if (!response.ok) {
            throw new Error(`Weather API error: ${response.status}`);
        }
        
        return await response.json();
    }

    // Fetch 5-day forecast data
    async fetchForecast(lat, lon) {
        const url = `${this.apiUrl}/forecast?lat=${lat}&lon=${lon}&appid=${this.apiKey}&units=metric`;
        const response = await fetch(url);
        
        if (!response.ok) {
            throw new Error(`Forecast API error: ${response.status}`);
        }
        
        return await response.json();
    }

    // Render current weather information
    renderCurrentWeather(data) {
        const currentWeatherEl = document.getElementById('current-weather');
        if (!currentWeatherEl) return;

        const temperature = Math.round(data.main.temp);
        const feelsLike = Math.round(data.main.feels_like);
        const description = data.weather[0].description;
        const icon = data.weather[0].icon;
        const humidity = data.main.humidity;
        const windSpeed = Math.round(data.wind.speed * 3.6); // Convert m/s to km/h
        const pressure = data.main.pressure;
        const visibility = data.visibility ? Math.round(data.visibility / 1000) : 'N/A';

        currentWeatherEl.innerHTML = `
            <div class="weather-header">
                <h2>${data.name}, ${data.sys.country}</h2>
                <p class="last-updated">Updated: ${new Date().toLocaleTimeString()}</p>
            </div>
            
            <div class="current-main">
                <div class="temperature-section">
                    <img src="https://openweathermap.org/img/wn/${icon}@4x.png" 
                         alt="${description}" class="weather-icon-large">
                    <div class="temperature-info">
                        <span class="current-temp">${temperature}°C</span>
                        <p class="feels-like">Feels like ${feelsLike}°C</p>
                        <p class="description">${this.capitalizeWords(description)}</p>
                    </div>
                </div>
            </div>
            
            <div class="weather-details">
                <div class="detail-item">
                    <span class="detail-label">Humidity</span>
                    <span class="detail-value">${humidity}%</span>
                </div>
                <div class="detail-item">
                    <span class="detail-label">Wind Speed</span>
                    <span class="detail-value">${windSpeed} km/h</span>
                </div>
                <div class="detail-item">
                    <span class="detail-label">Pressure</span>
                    <span class="detail-value">${pressure} hPa</span>
                </div>
                <div class="detail-item">
                    <span class="detail-label">Visibility</span>
                    <span class="detail-value">${visibility} km</span>
                </div>
            </div>
        `;
    }

    // Render 5-day forecast
    renderForecast(data) {
        const forecastEl = document.getElementById('forecast');
        if (!forecastEl) return;

        // Group forecast data by day (API returns 3-hour intervals)
        const dailyForecasts = this.groupForecastByDay(data.list);
        
        const forecastHTML = dailyForecasts.slice(0, 5).map(day => {
            const date = new Date(day.date);
            const dayName = date.toLocaleDateString('en-US', { weekday: 'short' });
            const monthDay = date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
            
            return `
                <div class="forecast-card">
                    <div class="forecast-date">
                        <span class="day-name">${dayName}</span>
                        <span class="month-day">${monthDay}</span>
                    </div>
                    <img src="https://openweathermap.org/img/wn/${day.icon}@2x.png" 
                         alt="${day.description}" class="forecast-icon">
                    <div class="forecast-temps">
                        <span class="high-temp">${Math.round(day.maxTemp)}°</span>
                        <span class="low-temp">${Math.round(day.minTemp)}°</span>
                    </div>
                    <p class="forecast-description">${this.capitalizeWords(day.description)}</p>
                </div>
            `;
        }).join('');

        forecastEl.innerHTML = `
            <h3>5-Day Forecast</h3>
            <div class="forecast-grid">
                ${forecastHTML}
            </div>
        `;
    }

    // Group forecast data by day and calculate min/max temperatures
    groupForecastByDay(forecastList) {
        const dailyData = {};
        
        forecastList.forEach(item => {
            const date = new Date(item.dt * 1000).toDateString();
            
            if (!dailyData[date]) {
                dailyData[date] = {
                    date: item.dt * 1000,
                    temps: [],
                    descriptions: [],
                    icons: []
                };
            }
            
            dailyData[date].temps.push(item.main.temp);
            dailyData[date].descriptions.push(item.weather[0].description);
            dailyData[date].icons.push(item.weather[0].icon);
        });
        
        return Object.values(dailyData).map(day => ({
            date: day.date,
            maxTemp: Math.max(...day.temps),
            minTemp: Math.min(...day.temps),
            description: this.getMostFrequent(day.descriptions),
            icon: this.getMostFrequent(day.icons)
        }));
    }

    // Get most frequent item from array
    getMostFrequent(arr) {
        const frequency = {};
        let maxCount = 0;
        let mostFrequent = arr[0];
        
        arr.forEach(item => {
            frequency[item] = (frequency[item] || 0) + 1;
            if (frequency[item] > maxCount) {
                maxCount = frequency[item];
                mostFrequent = item;
            }
        });
        
        return mostFrequent;
    }

    // Show loading state
    showLoading() {
        const loadingEl = document.getElementById('loading');
        const contentEl = document.getElementById('weather-content');
        
        if (loadingEl) loadingEl.style.display = 'flex';
        if (contentEl) contentEl.style.display = 'none';
    }

    // Hide loading state
    hideLoading() {
        const loadingEl = document.getElementById('loading');
        const contentEl = document.getElementById('weather-content');
        
        if (loadingEl) loadingEl.style.display = 'none';
        if (contentEl) contentEl.style.display = 'block';
    }

    // Handle and display errors
    handleError(message, error) {
        console.error(message, error);
        
        const errorEl = document.getElementById('error-message');
        if (errorEl) {
            errorEl.textContent = `${message}. Please try again.`;
            errorEl.style.display = 'block';
            
            // Hide error after 5 seconds
            setTimeout(() => {
                errorEl.style.display = 'none';
            }, 5000);
        }
        
        this.hideLoading();
    }

    // Cache location in localStorage
    cacheLocation(lat, lon) {
        const locationData = {
            lat,
            lon,
            timestamp: Date.now()
        };
        
        try {
            localStorage.setItem('weather-location', JSON.stringify(locationData));
        } catch (error) {
            console.warn('Failed to cache location:',