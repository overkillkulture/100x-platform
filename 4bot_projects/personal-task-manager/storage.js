/**
 * Storage Module - localStorage abstraction layer for task persistence
 * Provides a clean interface for saving and loading task data
 */

const Storage = {
    // Key used for localStorage
    STORAGE_KEY: 'personal-task-manager-tasks',

    /**
     * Load tasks from localStorage
     * @returns {Array} Array of task objects, empty array if no data exists
     */
    loadTasks() {
        try {
            const tasksJson = localStorage.getItem(this.STORAGE_KEY);
            if (!tasksJson) {
                return [];
            }
            
            const tasks = JSON.parse(tasksJson);
            
            // Validate that we have an array
            if (!Array.isArray(tasks)) {
                console.warn('Invalid task data format in localStorage, returning empty array');
                return [];
            }
            
            // Validate each task object has required properties
            return tasks.filter(task => {
                if (typeof task !== 'object' || task === null) {
                    return false;
                }
                
                // Check for required properties
                const hasId = typeof task.id === 'string' || typeof task.id === 'number';
                const hasText = typeof task.text === 'string';
                const hasCompleted = typeof task.completed === 'boolean';
                const hasTimestamp = typeof task.timestamp === 'number';
                
                return hasId && hasText && hasCompleted && hasTimestamp;
            });
            
        } catch (error) {
            console.error('Error loading tasks from localStorage:', error);
            return [];
        }
    },

    /**
     * Save tasks to localStorage
     * @param {Array} tasks - Array of task objects to save
     * @returns {boolean} True if save was successful, false otherwise
     */
    saveTasks(tasks) {
        try {
            // Validate input
            if (!Array.isArray(tasks)) {
                console.error('saveTasks expects an array of tasks');
                return false;
            }
            
            // Convert to JSON and save
            const tasksJson = JSON.stringify(tasks);
            localStorage.setItem(this.STORAGE_KEY, tasksJson);
            
            return true;
            
        } catch (error) {
            console.error('Error saving tasks to localStorage:', error);
            
            // Check if it's a quota exceeded error
            if (error.name === 'QuotaExceededError') {
                console.error('localStorage quota exceeded. Consider cleaning up old data.');
            }
            
            return false;
        }
    },

    /**
     * Clear all tasks from localStorage
     * @returns {boolean} True if clear was successful, false otherwise
     */
    clearTasks() {
        try {
            localStorage.removeItem(this.STORAGE_KEY);
            return true;
        } catch (error) {
            console.error('Error clearing tasks from localStorage:', error);
            return false;
        }
    },

    /**
     * Check if localStorage is available and working
     * @returns {boolean} True if localStorage is available, false otherwise
     */
    isAvailable() {
        try {
            const testKey = '__storage_test__';
            localStorage.setItem(testKey, 'test');
            localStorage.removeItem(testKey);
            return true;
        } catch (error) {
            console.warn('localStorage is not available:', error);
            return false;
        }
    },

    /**
     * Get storage usage information
     * @returns {Object} Object with storage usage stats
     */
    getStorageInfo() {
        try {
            const tasksData = localStorage.getItem(this.STORAGE_KEY);
            const dataSize = tasksData ? new Blob([tasksData]).size : 0;
            const taskCount = tasksData ? JSON.parse(tasksData).length : 0;
            
            return {
                taskCount,
                dataSize,
                dataSizeFormatted: this.formatBytes(dataSize),
                isAvailable: this.isAvailable()
            };
        } catch (error) {
            console.error('Error getting storage info:', error);
            return {
                taskCount: 0,
                dataSize: 0,
                dataSizeFormatted: '0 B',
                isAvailable: false
            };
        }
    },

    /**
     * Format bytes to human readable string
     * @param {number} bytes - Number of bytes
     * @returns {string} Formatted string (e.g., "1.2 KB")
     */
    formatBytes(bytes) {
        if (bytes === 0) return '0 B';
        
        const k = 1024;
        const sizes = ['B', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    },

    /**
     * Export tasks as JSON string for backup
     * @returns {string|null} JSON string of tasks or null if error
     */
    exportTasks() {
        try {
            const tasks = this.loadTasks();
            return JSON.stringify(tasks, null, 2);
        } catch (error) {
            console.error('Error exporting tasks:', error);
            return null;
        }
    },

    /**
     * Import tasks from JSON string
     * @param {string} jsonString - JSON string containing tasks array
     * @returns {boolean} True if import was successful, false otherwise
     */
    importTasks(jsonString) {
        try {
            const tasks = JSON.parse(jsonString);
            
            if (!Array.isArray(tasks)) {
                console.error('Import data must be an array of tasks');
                return false;
            }
            
            return this.saveTasks(tasks);
        } catch (error) {
            console.error('Error importing tasks:', error);
            return false;
        }
    }
};

// Export for use in other modules (if using ES6 modules)
// export default Storage;

// Make available globally for vanilla JS usage
if (typeof window !== 'undefined') {
    window.Storage = Storage;
}