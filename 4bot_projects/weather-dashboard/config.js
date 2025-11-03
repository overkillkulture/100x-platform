// Weather Dashboard Configuration
// API configuration and constants for the weather dashboard application

// OpenWeatherMap API Configuration
const API_CONFIG = {
    // Base URL for OpenWeatherMap API
    BASE_URL: 'https://api.openweathermap.org/data/2.5',
    
    // API Key - Replace with your actual OpenWeatherMap API key
    // Get your free API key at: https://openweathermap.org/api
    API_KEY: 'YOUR_API_KEY_HERE',
    
    // API endpoints
    ENDPOINTS: {
        CURRENT: '/weather',
        FORECAST: '/forecast'
    },
    
    // Default parameters for API requests
    DEFAULT_PARAMS: {
        units: 'metric', // Use metric units (Celsius, km/h, etc.)
        appid: 'YOUR_API_KEY_HERE' // Will be overridden by API_KEY
    }
};

// Application Constants
const APP_CONSTANTS = {
    // Default location if geolocation fails
    DEFAULT_LOCATION: {
        lat: 40.7128,
        lon: -74.0060,
        name: 'New York, NY'
    },
    
    // Cache settings
    CACHE: {
        DURATION: 10 * 60 * 1000, // 10 minutes in milliseconds
        KEYS: {
            WEATHER_DATA: 'weather_cache',
            FORECAST_DATA: 'forecast_cache',
            LOCATION: 'user_location',
            TIMESTAMP: 'cache_timestamp'
        }
    },
    
    // Geolocation settings
    GEOLOCATION: {
        TIMEOUT: 10000, // 10 seconds
        MAXIMUM_AGE: 300000, // 5 minutes
        ENABLE_HIGH_ACCURACY: true
    },
    
    // UI update intervals
    UPDATE_INTERVALS: {
        WEATHER_REFRESH: 10 * 60 * 1000, // 10 minutes
        TIME_UPDATE: 60 * 1000 // 1 minute for time display
    }
};

// Weather condition mappings for icons and descriptions
const WEATHER_CONDITIONS = {
    // OpenWeatherMap condition codes to custom descriptions
    CONDITION_MAP: {
        200: { description: 'Thunderstorm with light rain', icon: '⛈️' },
        201: { description: 'Thunderstorm with rain', icon: '⛈️' },
        202: { description: 'Thunderstorm with heavy rain', icon: '⛈️' },
        210: { description: 'Light thunderstorm', icon: '🌩️' },
        211: { description: 'Thunderstorm', icon: '⛈️' },
        212: { description: 'Heavy thunderstorm', icon: '⛈️' },
        221: { description: 'Ragged thunderstorm', icon: '⛈️' },
        230: { description: 'Thunderstorm with light drizzle', icon: '⛈️' },
        231: { description: 'Thunderstorm with drizzle', icon: '⛈️' },
        232: { description: 'Thunderstorm with heavy drizzle', icon: '⛈️' },
        
        300: { description: 'Light drizzle', icon: '🌦️' },
        301: { description: 'Drizzle', icon: '🌦️' },
        302: { description: 'Heavy drizzle', icon: '🌧️' },
        310: { description: 'Light drizzle rain', icon: '🌦️' },
        311: { description: 'Drizzle rain', icon: '🌧️' },
        312: { description: 'Heavy drizzle rain', icon: '🌧️' },
        313: { description: 'Shower rain and drizzle', icon: '🌧️' },
        314: { description: 'Heavy shower rain and drizzle', icon: '🌧️' },
        321: { description: 'Shower drizzle', icon: '🌦️' },
        
        500: { description: 'Light rain', icon: '🌦️' },
        501: { description: 'Moderate rain', icon: '🌧️' },
        502: { description: 'Heavy rain', icon: '🌧️' },
        503: { description: 'Very heavy rain', icon: '🌧️' },
        504: { description: 'Extreme rain', icon: '🌧️' },
        511: { description: 'Freezing rain', icon: '🌨️' },
        520: { description: 'Light shower rain', icon: '🌦️' },
        521: { description: 'Shower rain', icon: '🌧️' },
        522: { description: 'Heavy shower rain', icon: '🌧️' },
        531: { description: 'Ragged shower rain', icon: '🌧️' },
        
        600: { description: 'Light snow', icon: '🌨️' },
        601: { description: 'Snow', icon: '❄️' },
        602: { description: 'Heavy snow', icon: '❄️' },
        611: { description: 'Sleet', icon: '🌨️' },
        612: { description: 'Light shower sleet', icon: '🌨️' },
        613: { description: 'Shower sleet', icon: '🌨️' },
        615: { description: 'Light rain and snow', icon: '🌨️' },
        616: { description: 'Rain and snow', icon: '🌨️' },
        620: { description: 'Light shower snow', icon: '🌨️' },
        621: { description: 'Shower snow', icon: '❄️' },
        622: { description: 'Heavy shower snow', icon: '❄️' },
        
        701: { description: 'Mist', icon: '🌫️' },
        711: { description: 'Smoke', icon: '🌫️' },
        721: { description: 'Haze', icon: '🌫️' },
        731: { description: 'Dust whirls', icon: '🌪️' },
        741: { description: 'Fog', icon: '🌫️' },
        751: { description: 'Sand', icon: '🌫️' },
        761: { description: 'Dust', icon: '🌫️' },
        762: { description: 'Volcanic ash', icon: '🌋' },
        771: { description: 'Squalls', icon: '💨' },
        781: { description: 'Tornado', icon: '🌪️' },
        
        800: { description: 'Clear sky', icon: '☀️' },
        801: { description: 'Few clouds', icon: '🌤️' },
        802: { description: 'Scattered clouds', icon: '⛅' },
        803: { description: 'Broken clouds', icon: '🌥️' },
        804: { description: 'Overcast clouds', icon: '☁️' }
    },
    
    // Night time alternatives for certain conditions
    NIGHT_ICONS: {
        800: '🌙', // Clear night
        801: '🌙', // Few clouds night
        802: '☁️', // Scattered clouds night
        803: '☁️', // Broken clouds night
        804: '☁️'  // Overcast night
    }
};

// Error messages and user feedback
const ERROR_MESSAGES = {
    GEOLOCATION_DENIED: 'Location access denied. Using default location.',
    GEOLOCATION_UNAVAILABLE: 'Location service unavailable. Using default location.',
    GEOLOCATION_TIMEOUT: 'Location request timed out. Using default location.',
    API_ERROR: 'Unable to fetch weather data. Please try again later.',
    NETWORK_ERROR: 'Network connection error. Please check your internet connection.',
    INVALID_API_KEY: 'Invalid API key. Please check your configuration.',
    CITY_NOT_FOUND: 'City not found. Please try a different location.',
    GENERIC_ERROR: 'An unexpected error occurred. Please refresh the page.'
};

// Export configuration for use in other modules
// Note: In a browser environment without modules, these will be global variables
if (typeof module !== 'undefined' && module.exports) {
    // Node.js environment
    module.exports = {
        API_CONFIG,
        APP_CONSTANTS,
        WEATHER_CONDITIONS,
        ERROR_MESSAGES
    };
}