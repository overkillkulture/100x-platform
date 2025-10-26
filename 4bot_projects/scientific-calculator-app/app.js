/**
 * Scientific Calculator App - Main Application Controller
 * Coordinates all modules and manages application lifecycle
 */

class ScientificCalculatorApp {
    constructor() {
        this.calculator = null;
        this.memory = null;
        this.keyboard = null;
        this.display = null;
        this.isInitialized = false;
    }

    /**
     * Initialize the application
     */
    async init() {
        try {
            // Wait for DOM to be ready
            if (document.readyState === 'loading') {
                await new Promise(resolve => {
                    document.addEventListener('DOMContentLoaded', resolve);
                });
            }

            // Initialize all modules
            await this.initializeModules();
            
            // Set up event listeners
            this.setupEventListeners();
            
            // Set up module communication
            this.setupModuleCommunication();
            
            // Initialize UI state
            this.initializeUIState();
            
            this.isInitialized = true;
            console.log('Scientific Calculator App initialized successfully');
            
        } catch (error) {
            console.error('Failed to initialize app:', error);
            this.showError('Application failed to initialize');
        }
    }

    /**
     * Initialize all required modules
     */
    async initializeModules() {
        // Initialize Calculator module
        if (typeof Calculator !== 'undefined') {
            this.calculator = new Calculator();
        } else {
            throw new Error('Calculator module not found');
        }

        // Initialize Memory module
        if (typeof Memory !== 'undefined') {
            this.memory = new Memory();
        } else {
            throw new Error('Memory module not found');
        }

        // Initialize Display module
        if (typeof Display !== 'undefined') {
            this.display = new Display();
        } else {
            throw new Error('Display module not found');
        }

        // Initialize Keyboard module
        if (typeof Keyboard !== 'undefined') {
            this.keyboard = new Keyboard();
        } else {
            throw new Error('Keyboard module not found');
        }
    }

    /**
     * Set up event listeners for calculator buttons
     */
    setupEventListeners() {
        // Number buttons (0-9)
        document.querySelectorAll('.number').forEach(button => {
            button.addEventListener('click', (e) => {
                this.handleNumberInput(e.target.textContent);
            });
        });

        // Basic operation buttons
        document.querySelectorAll('.operator').forEach(button => {
            button.addEventListener('click', (e) => {
                this.handleOperatorInput(e.target.dataset.operator || e.target.textContent);
            });
        });

        // Scientific function buttons
        document.querySelectorAll('.scientific').forEach(button => {
            button.addEventListener('click', (e) => {
                this.handleScientificFunction(e.target.dataset.function || e.target.textContent);
            });
        });

        // Memory buttons
        document.querySelectorAll('.memory').forEach(button => {
            button.addEventListener('click', (e) => {
                this.handleMemoryOperation(e.target.dataset.memory || e.target.textContent);
            });
        });

        // Special buttons
        const equalsBtn = document.querySelector('.equals');
        if (equalsBtn) {
            equalsBtn.addEventListener('click', () => this.handleEquals());
        }

        const clearBtn = document.querySelector('.clear');
        if (clearBtn) {
            clearBtn.addEventListener('click', () => this.handleClear());
        }

        const clearEntryBtn = document.querySelector('.clear-entry');
        if (clearEntryBtn) {
            clearEntryBtn.addEventListener('click', () => this.handleClearEntry());
        }

        const decimalBtn = document.querySelector('.decimal');
        if (decimalBtn) {
            decimalBtn.addEventListener('click', () => this.handleDecimal());
        }

        const backspaceBtn = document.querySelector('.backspace');
        if (backspaceBtn) {
            backspaceBtn.addEventListener('click', () => this.handleBackspace());
        }
    }

    /**
     * Set up communication between modules using custom events
     */
    setupModuleCommunication() {
        // Listen for calculation results
        document.addEventListener('calculationComplete', (e) => {
            this.display.updateResult(e.detail.result);
            this.display.addToHistory(e.detail.expression, e.detail.result);
        });

        // Listen for calculation errors
        document.addEventListener('calculationError', (e) => {
            this.display.showError(e.detail.message);
        });

        // Listen for memory operations
        document.addEventListener('memoryUpdated', (e) => {
            this.updateMemoryIndicator(e.detail.hasValue);
        });

        // Listen for keyboard events
        document.addEventListener('keyboardInput', (e) => {
            this.handleKeyboardInput(e.detail);
        });

        // Listen for display updates
        document.addEventListener('displayUpdate', (e) => {
            // Handle any display-related updates if needed
        });
    }

    /**
     * Initialize UI state
     */
    initializeUIState() {
        // Set initial display
        this.display.clear();
        
        // Update memory indicator
        this.updateMemoryIndicator(this.memory.hasValue());
        
        // Set focus for keyboard input
        document.body.focus();
    }

    /**
     * Handle number input
     */
    handleNumberInput(number) {
        this.display.appendNumber(number);
        this.provideFeedback('number');
    }

    /**
     * Handle operator input
     */
    handleOperatorInput(operator) {
        const currentValue = this.display.getCurrentValue();
        this.calculator.setOperator(operator, currentValue);
        this.display.setOperator(operator);
        this.provideFeedback('operator');
    }

    /**
     * Handle scientific function input
     */
    handleScientificFunction(func) {
        const currentValue = this.display.getCurrentValue();
        
        try {
            const result = this.calculator.calculateScientificFunction(func, currentValue);
            this.display.updateResult(result);
            this.display.addToHistory(`${func}(${currentValue})`, result);
            this.provideFeedback('function');
        } catch (error) {
            this.display.showError(error.message);
            this.provideFeedback('error');
        }
    }

    /**
     * Handle memory operations
     */
    handleMemoryOperation(operation) {
        const currentValue = this.display.getCurrentValue();
        
        try {
            switch (operation.toLowerCase()) {
                case 'ms':
                case 'store':
                    this.memory.store(currentValue);
                    break;
                case 'mr':
                case 'recall':
                    const recalled = this.memory.recall();
                    if (recalled !== null) {
                        this.display.updateResult(recalled);
                    }
                    break;
                case 'mc':
                case 'clear':
                    this.memory.clear();
                    break;
                case 'm+':
                case 'add':
                    this.memory.add(currentValue);
                    break;
                case 'm-':
                case 'subtract':
                    this.memory.subtract(currentValue);
                    break;
            }
            
            this.updateMemoryIndicator(this.memory.hasValue());
            this.provideFeedback('memory');
            
        } catch (error) {
            this.display.showError(error.message);
            this.provideFeedback('error');
        }
    }

    /**
     * Handle equals operation
     */
    handleEquals() {
        const currentValue = this.display.getCurrentValue();
        
        try {
            const result = this.calculator.calculate(currentValue);
            const expression = this.calculator.getLastExpression();
            
            this.display.updateResult(result);
            this.display.addToHistory(expression, result);
            this.provideFeedback('equals');
            
        } catch (error) {
            this.display.showError(error.message);
            this.provideFeedback('error');
        }
    }

    /**
     * Handle clear operation
     */
    handleClear() {
        this.calculator.clear();
        this.display.clear();
        this.provideFeedback('clear');
    }

    /**
     * Handle clear entry operation
     */
    handleClearEntry() {
        this.display.clearEntry();
        this.provideFeedback('clear');
    }

    /**
     * Handle decimal point input
     */
    handleDecimal() {
        this.display.appendDecimal();
        this.provideFeedback('number');
    }

    /**
     * Handle backspace operation
     */
    handleBackspace() {
        this.display.backspace();
        this.provideFeedback('backspace');
    }

    /**
     * Handle keyboard input events
     */
    handleKeyboardInput(input) {
        switch (input.type) {
            case 'number':
                this.handleNumberInput(input.value);
                break;
            case 'operator':
                this.handleOperatorInput(input.value);
                break;
            case 'function':
                this.handleScientificFunction(input.value);
                break;
            case 'equals':
                this.handleEquals();
                break;
            case 'clear':
                this.handleClear();
                break;
            case 'backspace':
                this.handleBackspace();
                break;
            case 'decimal':
                this.handleDecimal();
                break;
            case 'memory':
                this.handleMemoryOperation(input.value);
                break;
        }
    }

    /**
     * Update memory indicator in UI
     */
    updateMemoryIndicator(hasValue) {
        const indicator = document.querySelector('.memory-indicator');
        if (indicator) {
            indicator.style.display = hasValue ? 'block' : 'none';
            indicator.textContent = hasValue ? 'M' : '';
        }
    }

    /**
     * Provide visual/audio feedback for user actions
     */
    provideFeedback(type) {
        // Add visual feedback classes
        const button = document.activeElement;
        if (button && button.classList.contains('btn')) {
            button.classList.add('pressed');
            setTimeout(() => {
                button.classList.remove('pressed');
            }, 100);
        }

        // Dispatch custom event for feedback
        document.dispatchEvent(new CustomEvent('userFeedback', {
            detail: { type, timestamp: Date.now() }
        }));
    }

    /**
     * Show error message to user
     */
    showError(message) {
        if (this.display) {
            this.display.showError(message);
        } else {
            console.error(message);
            alert(message); // Fallback for critical errors
        }
    }

    /**
     * Get application state for debugging
     */
    getState() {
        if (!this.isInitialized) {
            return { status: 'not_initialized' };
        }

        return {
            status: 'initialized',
            calculator: this.calculator ? this.calculator.getState() : null,
            memory: this.memory ? this.memory.getState() : null,
            display: this.display ? this.display.getState() : null,
            hasMemoryValue: this.memory ? this.memory.hasValue() : false
        };
    }

    /**
     * Cleanup resources
     */
    destroy() {
        // Remove event listeners
        document.removeEventListener('calculationComplete', this.handleCalculationComplete);
        document.removeEventListener('calculationError', this.handleCalculationError);
        document.removeEventListener('memoryUpdated', this.handleMemoryUpdated);
        document.removeEventListener('keyboardInput', this.handleKeyboardInput);

        //