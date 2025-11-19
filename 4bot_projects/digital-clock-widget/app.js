// Digital Clock Widget - Main Application Logic
class DigitalClock {
    constructor() {
        this.is24HourFormat = this.getStoredFormat();
        this.clockElement = null;
        this.toggleButton = null;
        this.intervalId = null;
        
        this.init();
    }
    
    // Initialize the clock application
    init() {
        // Wait for DOM to be fully loaded
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.setupClock());
        } else {
            this.setupClock();
        }
    }
    
    // Set up clock elements and start the clock
    setupClock() {
        this.clockElement = document.getElementById('timeDisplay');
        this.toggleButton = document.getElementById('formatToggle');
        
        if (!this.clockElement || !this.toggleButton) {
            console.error('Required clock elements not found in DOM');
            return;
        }
        
        // Set up event listener for format toggle
        this.toggleButton.addEventListener('click', () => this.toggleFormat());
        
        // Update button text based on current format
        this.updateToggleButton();
        
        // Start the clock
        this.updateTime();
        this.startClock();
    }
    
    // Start the interval to update time every second
    startClock() {
        // Clear any existing interval
        if (this.intervalId) {
            clearInterval(this.intervalId);
        }
        
        // Update time every second
        this.intervalId = setInterval(() => {
            this.updateTime();
        }, 1000);
    }
    
    // Stop the clock interval
    stopClock() {
        if (this.intervalId) {
            clearInterval(this.intervalId);
            this.intervalId = null;
        }
    }
    
    // Get current time and update the display
    updateTime() {
        const now = new Date();
        const timeString = this.formatTime(now);
        
        if (this.clockElement) {
            this.clockElement.textContent = timeString;
        }
    }
    
    // Format time based on current format preference
    formatTime(date) {
        let hours = date.getHours();
        const minutes = date.getMinutes();
        const seconds = date.getSeconds();
        
        let formattedTime;
        
        if (this.is24HourFormat) {
            // 24-hour format (00:00:00 - 23:59:59)
            formattedTime = `${this.padZero(hours)}:${this.padZero(minutes)}:${this.padZero(seconds)}`;
        } else {
            // 12-hour format with AM/PM
            const ampm = hours >= 12 ? 'PM' : 'AM';
            hours = hours % 12;
            hours = hours ? hours : 12; // 0 should be 12
            formattedTime = `${this.padZero(hours)}:${this.padZero(minutes)}:${this.padZero(seconds)} ${ampm}`;
        }
        
        return formattedTime;
    }
    
    // Add leading zero to single digit numbers
    padZero(num) {
        return num.toString().padStart(2, '0');
    }
    
    // Toggle between 12-hour and 24-hour format
    toggleFormat() {
        this.is24HourFormat = !this.is24HourFormat;
        this.saveFormat();
        this.updateToggleButton();
        this.updateTime(); // Immediately update display with new format
    }
    
    // Update toggle button text based on current format
    updateToggleButton() {
        if (this.toggleButton) {
            this.toggleButton.textContent = this.is24HourFormat ? 'Switch to 12H' : 'Switch to 24H';
        }
    }
    
    // Save format preference to localStorage
    saveFormat() {
        try {
            localStorage.setItem('clockFormat24Hour', JSON.stringify(this.is24HourFormat));
        } catch (error) {
            console.warn('Could not save format preference:', error);
        }
    }
    
    // Get stored format preference from localStorage
    getStoredFormat() {
        try {
            const stored = localStorage.getItem('clockFormat24Hour');
            return stored ? JSON.parse(stored) : false; // Default to 12-hour format
        } catch (error) {
            console.warn('Could not load format preference:', error);
            return false; // Default to 12-hour format
        }
    }
    
    // Clean up resources
    destroy() {
        this.stopClock();
        if (this.toggleButton) {
            this.toggleButton.removeEventListener('click', this.toggleFormat);
        }
    }
}

// Initialize the clock when script loads
const digitalClock = new DigitalClock();

// Handle page visibility changes to optimize performance
document.addEventListener('visibilitychange', () => {
    if (document.hidden) {
        // Page is hidden, could optionally stop the clock to save resources
        // digitalClock.stopClock();
    } else {
        // Page is visible, ensure clock is running and accurate
        digitalClock.updateTime();
        digitalClock.startClock();
    }
});

// Clean up when page unloads
window.addEventListener('beforeunload', () => {
    digitalClock.destroy();
});