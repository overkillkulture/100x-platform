/**
 * Display Management Module
 * Handles calculator display updates, operation history, and visual feedback
 */

class Display {
    constructor() {
        this.displayElement = null;
        this.historyElement = null;
        this.currentValue = '0';
        this.history = [];
        this.maxHistoryItems = 10;
        this.maxDisplayLength = 12;
        
        this.init();
    }

    /**
     * Initialize display elements and event listeners
     */
    init() {
        this.displayElement = document.getElementById('display');
        this.historyElement = document.getElementById('history');
        
        if (!this.displayElement) {
            console.error('Display element not found');
            return;
        }

        // Listen for custom events from other modules
        document.addEventListener('calculatorResult', (e) => {
            this.updateDisplay(e.detail.result);
            this.addToHistory(e.detail.operation, e.detail.result);
        });

        document.addEventListener('calculatorError', (e) => {
            this.showError(e.detail.message);
        });

        document.addEventListener('calculatorClear', () => {
            this.clear();
        });

        document.addEventListener('displayUpdate', (e) => {
            this.updateDisplay(e.detail.value);
        });

        // Load history from localStorage
        this.loadHistory();
    }

    /**
     * Update the main display with a value
     * @param {string|number} value - Value to display
     */
    updateDisplay(value) {
        if (value === undefined || value === null) {
            value = '0';
        }

        let displayValue = String(value);

        // Handle very large or very small numbers with scientific notation
        if (Math.abs(parseFloat(displayValue)) > Math.pow(10, this.maxDisplayLength) || 
            (Math.abs(parseFloat(displayValue)) < Math.pow(10, -6) && parseFloat(displayValue) !== 0)) {
            displayValue = parseFloat(displayValue).toExponential(6);
        }

        // Truncate if too long
        if (displayValue.length > this.maxDisplayLength) {
            if (displayValue.includes('.')) {
                const decimalIndex = displayValue.indexOf('.');
                const integerPart = displayValue.substring(0, decimalIndex);
                const availableDecimals = this.maxDisplayLength - integerPart.length - 1;
                
                if (availableDecimals > 0) {
                    displayValue = parseFloat(displayValue).toFixed(availableDecimals);
                } else {
                    displayValue = parseFloat(displayValue).toExponential(4);
                }
            } else {
                displayValue = parseFloat(displayValue).toExponential(4);
            }
        }

        this.currentValue = displayValue;
        
        if (this.displayElement) {
            this.displayElement.textContent = displayValue;
            this.animateDisplay();
        }
    }

    /**
     * Show error message on display
     * @param {string} message - Error message to display
     */
    showError(message = 'Error') {
        this.currentValue = message;
        
        if (this.displayElement) {
            this.displayElement.textContent = message;
            this.displayElement.classList.add('error');
            
            // Remove error class after animation
            setTimeout(() => {
                this.displayElement.classList.remove('error');
            }, 2000);
        }
    }

    /**
     * Clear the display
     */
    clear() {
        this.updateDisplay('0');
    }

    /**
     * Add animation effect to display updates
     */
    animateDisplay() {
        if (this.displayElement) {
            this.displayElement.classList.add('updated');
            setTimeout(() => {
                this.displayElement.classList.remove('updated');
            }, 200);
        }
    }

    /**
     * Add operation to history
     * @param {string} operation - The operation performed
     * @param {string|number} result - The result of the operation
     */
    addToHistory(operation, result) {
        const historyItem = {
            operation: operation,
            result: String(result),
            timestamp: new Date().toLocaleTimeString()
        };

        this.history.unshift(historyItem);

        // Limit history size
        if (this.history.length > this.maxHistoryItems) {
            this.history = this.history.slice(0, this.maxHistoryItems);
        }

        this.updateHistoryDisplay();
        this.saveHistory();
    }

    /**
     * Update the history display
     */
    updateHistoryDisplay() {
        if (!this.historyElement) return;

        this.historyElement.innerHTML = '';

        this.history.forEach((item, index) => {
            const historyItem = document.createElement('div');
            historyItem.className = 'history-item';
            
            const operation = document.createElement('div');
            operation.className = 'history-operation';
            operation.textContent = item.operation;
            
            const result = document.createElement('div');
            result.className = 'history-result';
            result.textContent = `= ${item.result}`;
            
            const timestamp = document.createElement('div');
            timestamp.className = 'history-timestamp';
            timestamp.textContent = item.timestamp;

            historyItem.appendChild(operation);
            historyItem.appendChild(result);
            historyItem.appendChild(timestamp);

            // Add click handler to reuse result
            historyItem.addEventListener('click', () => {
                this.updateDisplay(item.result);
                document.dispatchEvent(new CustomEvent('historyItemSelected', {
                    detail: { value: item.result }
                }));
            });

            this.historyElement.appendChild(historyItem);

            // Add entrance animation
            setTimeout(() => {
                historyItem.classList.add('show');
            }, index * 50);
        });
    }

    /**
     * Clear history
     */
    clearHistory() {
        this.history = [];
        this.updateHistoryDisplay();
        this.saveHistory();
        
        // Dispatch event for other modules
        document.dispatchEvent(new CustomEvent('historyClear'));
    }

    /**
     * Get current display value
     * @returns {string} Current display value
     */
    getCurrentValue() {
        return this.currentValue;
    }

    /**
     * Get history array
     * @returns {Array} History array
     */
    getHistory() {
        return [...this.history];
    }

    /**
     * Save history to localStorage
     */
    saveHistory() {
        try {
            localStorage.setItem('calculator_history', JSON.stringify(this.history));
        } catch (error) {
            console.warn('Could not save history to localStorage:', error);
        }
    }

    /**
     * Load history from localStorage
     */
    loadHistory() {
        try {
            const savedHistory = localStorage.getItem('calculator_history');
            if (savedHistory) {
                this.history = JSON.parse(savedHistory);
                this.updateHistoryDisplay();
            }
        } catch (error) {
            console.warn('Could not load history from localStorage:', error);
            this.history = [];
        }
    }

    /**
     * Toggle history panel visibility
     */
    toggleHistory() {
        if (this.historyElement) {
            this.historyElement.classList.toggle('visible');
            
            // Dispatch event for other modules to know about visibility change
            const isVisible = this.historyElement.classList.contains('visible');
            document.dispatchEvent(new CustomEvent('historyToggle', {
                detail: { visible: isVisible }
            }));
        }
    }

    /**
     * Format number for display
     * @param {number} num - Number to format
     * @returns {string} Formatted number string
     */
    formatNumber(num) {
        if (isNaN(num)) return 'Error';
        
        // Handle infinity
        if (!isFinite(num)) {
            return num > 0 ? 'Infinity' : '-Infinity';
        }

        // Convert to string and handle scientific notation
        let str = String(num);
        
        // If number is too long, use scientific notation
        if (str.length > this.maxDisplayLength && !str.includes('e')) {
            return num.toExponential(6);
        }

        return str;
    }

    /**
     * Append character to display (for input building)
     * @param {string} char - Character to append
     */
    appendToDisplay(char) {
        if (this.currentValue === '0' || this.currentValue === 'Error') {
            this.currentValue = char;
        } else {
            this.currentValue += char;
        }
        
        if (this.displayElement) {
            this.displayElement.textContent = this.currentValue;
        }
    }

    /**
     * Remove last character from display
     */
    backspace() {
        if (this.currentValue.length > 1 && this.currentValue !== 'Error') {
            this.currentValue = this.currentValue.slice(0, -1);
        } else {
            this.currentValue = '0';
        }
        
        if (this.displayElement) {
            this.displayElement.textContent = this.currentValue;
        }
    }

    /**
     * Show memory indicator
     * @param {boolean} hasMemory - Whether memory contains a value
     */
    showMemoryIndicator(hasMemory) {
        const indicator = document.getElementById('memory-indicator');
        if (indicator) {
            indicator.style.display = hasMemory ? 'block' : 'none';
        }
    }
}

// Export for use in other modules
window.Display = Display;