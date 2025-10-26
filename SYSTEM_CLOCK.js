// 🕐 SYSTEM CLOCK - Real-time clock for AI awareness
// Inject this on every page so Claude knows the actual time

class SystemClock {
    constructor() {
        this.updateInterval = null;
        this.init();
    }

    init() {
        // Update every second
        this.updateInterval = setInterval(() => this.update(), 1000);
        this.update(); // Initial update
    }

    update() {
        const now = new Date();

        // Store in global scope for AI access
        window.SYSTEM_TIME = {
            timestamp: now.getTime(),
            iso: now.toISOString(),
            local: now.toLocaleString(),
            date: now.toLocaleDateString(),
            time: now.toLocaleTimeString(),
            hour: now.getHours(),
            minute: now.getMinutes(),
            second: now.getSeconds(),
            isBusinessHours: (now.getHours() >= 9 && now.getHours() < 17),
            timeOfDay: this.getTimeOfDay(now.getHours())
        };

        // Emit event for other systems
        window.dispatchEvent(new CustomEvent('system-time-update', {
            detail: window.SYSTEM_TIME
        }));
    }

    getTimeOfDay(hour) {
        if (hour >= 5 && hour < 12) return 'morning';
        if (hour >= 12 && hour < 17) return 'afternoon';
        if (hour >= 17 && hour < 21) return 'evening';
        return 'night';
    }

    destroy() {
        if (this.updateInterval) {
            clearInterval(this.updateInterval);
        }
    }
}

// Auto-initialize
if (typeof window !== 'undefined') {
    window.systemClock = new SystemClock();
    console.log('🕐 System Clock initialized:', window.SYSTEM_TIME);
}
