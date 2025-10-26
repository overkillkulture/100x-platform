/**
 * Memory Operations Module
 * Handles memory storage, recall, clear, and add operations for the calculator
 * Uses localStorage for persistence across browser sessions
 */

class MemoryManager {
    constructor() {
        this.memoryKey = 'calculator-memory';
        this.memoryValue = this.loadMemoryFromStorage();
        this.initializeEventListeners();
    }

    /**
     * Load memory value from localStorage
     * @returns {number} The stored memory value or 0 if none exists
     */
    loadMemoryFromStorage() {
        try {
            const stored = localStorage.getItem(this.memoryKey);
            return stored ? parseFloat(stored) : 0;
        } catch (error) {
            console.warn('Failed to load memory from storage:', error);
            return 0;
        }
    }

    /**
     * Save memory value to localStorage
     * @param {number} value - The value to store
     */
    saveMemoryToStorage(value) {
        try {
            localStorage.setItem(this.memoryKey, value.toString());
        } catch (error) {
            console.warn('Failed to save memory to storage:', error);
        }
    }

    /**
     * Store current display value in memory (MS - Memory Store)
     * @param {number} value - The value to store in memory
     */
    store(value) {
        if (typeof value !== 'number' || isNaN(value)) {
            console.error('Invalid value for memory store:', value);
            return false;
        }

        this.memoryValue = value;
        this.saveMemoryToStorage(this.memoryValue);
        this.dispatchMemoryEvent('memory-stored', { value: this.memoryValue });
        return true;
    }

    /**
     * Recall value from memory (MR - Memory Recall)
     * @returns {number} The current memory value
     */
    recall() {
        this.dispatchMemoryEvent('memory-recalled', { value: this.memoryValue });
        return this.memoryValue;
    }

    /**
     * Clear memory (MC - Memory Clear)
     */
    clear() {
        this.memoryValue = 0;
        this.saveMemoryToStorage(this.memoryValue);
        this.dispatchMemoryEvent('memory-cleared', { value: this.memoryValue });
    }

    /**
     * Add value to memory (M+ - Memory Add)
     * @param {number} value - The value to add to memory
     */
    add(value) {
        if (typeof value !== 'number' || isNaN(value)) {
            console.error('Invalid value for memory add:', value);
            return false;
        }

        this.memoryValue += value;
        this.saveMemoryToStorage(this.memoryValue);
        this.dispatchMemoryEvent('memory-added', { 
            addedValue: value, 
            totalValue: this.memoryValue 
        });
        return true;
    }

    /**
     * Subtract value from memory (M- - Memory Subtract)
     * @param {number} value - The value to subtract from memory
     */
    subtract(value) {
        if (typeof value !== 'number' || isNaN(value)) {
            console.error('Invalid value for memory subtract:', value);
            return false;
        }

        this.memoryValue -= value;
        this.saveMemoryToStorage(this.memoryValue);
        this.dispatchMemoryEvent('memory-subtracted', { 
            subtractedValue: value, 
            totalValue: this.memoryValue 
        });
        return true;
    }

    /**
     * Get current memory value without triggering recall event
     * @returns {number} The current memory value
     */
    getValue() {
        return this.memoryValue;
    }

    /**
     * Check if memory has a non-zero value
     * @returns {boolean} True if memory contains a non-zero value
     */
    hasValue() {
        return this.memoryValue !== 0;
    }

    /**
     * Dispatch custom events for memory operations
     * @param {string} eventType - The type of memory event
     * @param {object} detail - Event details
     */
    dispatchMemoryEvent(eventType, detail) {
        const event = new CustomEvent(eventType, {
            detail: detail,
            bubbles: true
        });
        document.dispatchEvent(event);
    }

    /**
     * Initialize event listeners for memory operations
     */
    initializeEventListeners() {
        // Listen for memory button clicks
        document.addEventListener('click', (event) => {
            const target = event.target;
            
            if (!target.classList.contains('memory-btn')) {
                return;
            }

            const operation = target.dataset.memory;
            const currentDisplay = this.getCurrentDisplayValue();

            switch (operation) {
                case 'store':
                    this.store(currentDisplay);
                    break;
                case 'recall':
                    const recalled = this.recall();
                    this.updateDisplay(recalled);
                    break;
                case 'clear':
                    this.clear();
                    break;
                case 'add':
                    this.add(currentDisplay);
                    break;
                case 'subtract':
                    this.subtract(currentDisplay);
                    break;
                default:
                    console.warn('Unknown memory operation:', operation);
            }
        });

        // Listen for keyboard shortcuts
        document.addEventListener('keydown', (event) => {
            if (event.ctrlKey || event.metaKey) {
                const currentDisplay = this.getCurrentDisplayValue();
                
                switch (event.key.toLowerCase()) {
                    case 'm': // Ctrl+M - Memory Store
                        event.preventDefault();
                        this.store(currentDisplay);
                        break;
                    case 'r': // Ctrl+R - Memory Recall
                        event.preventDefault();
                        const recalled = this.recall();
                        this.updateDisplay(recalled);
                        break;
                    case 'l': // Ctrl+L - Memory Clear
                        event.preventDefault();
                        this.clear();
                        break;
                    case 'p': // Ctrl+P - Memory Add
                        event.preventDefault();
                        this.add(currentDisplay);
                        break;
                }
            }
        });
    }

    /**
     * Get current display value from the calculator
     * @returns {number} The current display value
     */
    getCurrentDisplayValue() {
        const display = document.querySelector('.display-current');
        if (!display) {
            console.warn('Display element not found');
            return 0;
        }

        const value = parseFloat(display.textContent || display.value || '0');
        return isNaN(value) ? 0 : value;
    }

    /**
     * Update calculator display with a value
     * @param {number} value - The value to display
     */
    updateDisplay(value) {
        const event = new CustomEvent('display-update', {
            detail: { value: value },
            bubbles: true
        });
        document.dispatchEvent(event);
    }

    /**
     * Reset memory manager (useful for testing or initialization)
     */
    reset() {
        this.clear();
        localStorage.removeItem(this.memoryKey);
    }

    /**
     * Export memory state (useful for debugging or data export)
     * @returns {object} Current memory state
     */
    exportState() {
        return {
            memoryValue: this.memoryValue,
            hasValue: this.hasValue(),
            timestamp: new Date().toISOString()
        };
    }

    /**
     * Import memory state (useful for data import or restoration)
     * @param {object} state - Memory state to import
     */
    importState(state) {
        if (state && typeof state.memoryValue === 'number') {
            this.memoryValue = state.memoryValue;
            this.saveMemoryToStorage(this.memoryValue);
            this.dispatchMemoryEvent('memory-imported', { value: this.memoryValue });
            return true;
        }
        return false;
    }
}

// Create and export memory manager instance
const memoryManager = new MemoryManager();

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = MemoryManager;
} else {
    window.MemoryManager = MemoryManager;
    window.memoryManager = memoryManager;
}