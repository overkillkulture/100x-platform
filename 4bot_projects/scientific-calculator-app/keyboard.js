/**
 * Keyboard Event Handler for Scientific Calculator
 * Handles keyboard shortcuts and input mapping
 */

class KeyboardHandler {
    constructor() {
        this.keyMappings = this.initializeKeyMappings();
        this.shiftPressed = false;
        this.ctrlPressed = false;
        this.altPressed = false;
        this.bindEvents();
    }

    /**
     * Initialize keyboard mappings for calculator functions
     */
    initializeKeyMappings() {
        return {
            // Numbers
            '0': () => this.dispatchCalculatorEvent('number', '0'),
            '1': () => this.dispatchCalculatorEvent('number', '1'),
            '2': () => this.dispatchCalculatorEvent('number', '2'),
            '3': () => this.dispatchCalculatorEvent('number', '3'),
            '4': () => this.dispatchCalculatorEvent('number', '4'),
            '5': () => this.dispatchCalculatorEvent('number', '5'),
            '6': () => this.dispatchCalculatorEvent('number', '6'),
            '7': () => this.dispatchCalculatorEvent('number', '7'),
            '8': () => this.dispatchCalculatorEvent('number', '8'),
            '9': () => this.dispatchCalculatorEvent('number', '9'),

            // Basic operations
            '+': () => this.dispatchCalculatorEvent('operator', '+'),
            '-': () => this.dispatchCalculatorEvent('operator', '-'),
            '*': () => this.dispatchCalculatorEvent('operator', '×'),
            '/': () => this.dispatchCalculatorEvent('operator', '÷'),
            '=': () => this.dispatchCalculatorEvent('equals'),
            'Enter': () => this.dispatchCalculatorEvent('equals'),

            // Decimal point
            '.': () => this.dispatchCalculatorEvent('decimal'),
            ',': () => this.dispatchCalculatorEvent('decimal'), // Alternative decimal

            // Clear operations
            'Escape': () => this.dispatchCalculatorEvent('clear'),
            'Delete': () => this.dispatchCalculatorEvent('clear'),
            'Backspace': () => this.dispatchCalculatorEvent('backspace'),

            // Parentheses
            '(': () => this.dispatchCalculatorEvent('operator', '('),
            ')': () => this.dispatchCalculatorEvent('operator', ')'),

            // Scientific functions (single key shortcuts)
            's': () => this.handleScientificFunction('sin'),
            'c': () => this.handleScientificFunction('cos'),
            't': () => this.handleScientificFunction('tan'),
            'l': () => this.handleScientificFunction('log'),
            'r': () => this.handleScientificFunction('sqrt'),
            'p': () => this.handleScientificFunction('π'),
            'e': () => this.handleScientificFunction('e'),
            '!': () => this.handleScientificFunction('factorial'),

            // Power and root
            '^': () => this.dispatchCalculatorEvent('operator', '^'),

            // Memory functions
            'F1': () => this.dispatchCalculatorEvent('memory', 'store'),
            'F2': () => this.dispatchCalculatorEvent('memory', 'recall'),
            'F3': () => this.dispatchCalculatorEvent('memory', 'clear'),
            'F4': () => this.dispatchCalculatorEvent('memory', 'add'),

            // Percentage
            '%': () => this.dispatchCalculatorEvent('operator', '%')
        };
    }

    /**
     * Bind keyboard event listeners
     */
    bindEvents() {
        document.addEventListener('keydown', this.handleKeyDown.bind(this));
        document.addEventListener('keyup', this.handleKeyUp.bind(this));
        
        // Prevent default behavior for certain keys
        document.addEventListener('keydown', (e) => {
            if (this.shouldPreventDefault(e.key, e)) {
                e.preventDefault();
            }
        });

        // Handle focus management
        document.addEventListener('click', this.handleDocumentClick.bind(this));
    }

    /**
     * Handle keydown events
     */
    handleKeyDown(event) {
        const key = event.key;
        
        // Track modifier keys
        this.shiftPressed = event.shiftKey;
        this.ctrlPressed = event.ctrlKey;
        this.altPressed = event.altKey;

        // Handle special key combinations
        if (this.handleSpecialCombinations(event)) {
            return;
        }

        // Handle shift combinations for operators
        if (this.shiftPressed) {
            this.handleShiftCombinations(key, event);
            return;
        }

        // Handle ctrl combinations
        if (this.ctrlPressed) {
            this.handleCtrlCombinations(key, event);
            return;
        }

        // Handle regular key mappings
        if (this.keyMappings[key]) {
            this.keyMappings[key]();
            this.highlightButton(key);
        }
    }

    /**
     * Handle keyup events
     */
    handleKeyUp(event) {
        this.shiftPressed = event.shiftKey;
        this.ctrlPressed = event.ctrlKey;
        this.altPressed = event.altKey;
        
        // Remove button highlight
        this.removeButtonHighlight(event.key);
    }

    /**
     * Handle special key combinations
     */
    handleSpecialCombinations(event) {
        const key = event.key;

        // Ctrl + C: Copy result
        if (this.ctrlPressed && key === 'c') {
            this.copyResult();
            event.preventDefault();
            return true;
        }

        // Ctrl + V: Paste number
        if (this.ctrlPressed && key === 'v') {
            this.pasteNumber();
            event.preventDefault();
            return true;
        }

        // Alt + combinations for scientific functions
        if (this.altPressed) {
            return this.handleAltCombinations(key, event);
        }

        return false;
    }

    /**
     * Handle shift key combinations
     */
    handleShiftCombinations(key, event) {
        const shiftMappings = {
            '8': () => this.dispatchCalculatorEvent('operator', '×'), // Shift + 8 = *
            '=': () => this.dispatchCalculatorEvent('operator', '+'), // Shift + = = +
            '6': () => this.dispatchCalculatorEvent('operator', '^'), // Shift + 6 = ^
            '1': () => this.handleScientificFunction('factorial'), // Shift + 1 = !
            '9': () => this.dispatchCalculatorEvent('operator', '('), // Shift + 9 = (
            '0': () => this.dispatchCalculatorEvent('operator', ')'), // Shift + 0 = )
            '5': () => this.dispatchCalculatorEvent('operator', '%'), // Shift + 5 = %
        };

        if (shiftMappings[key]) {
            shiftMappings[key]();
            event.preventDefault();
        }
    }

    /**
     * Handle ctrl key combinations
     */
    handleCtrlCombinations(key, event) {
        const ctrlMappings = {
            'm': () => this.dispatchCalculatorEvent('memory', 'store'), // Ctrl + M: Memory Store
            'r': () => this.dispatchCalculatorEvent('memory', 'recall'), // Ctrl + R: Memory Recall
            'd': () => this.dispatchCalculatorEvent('memory', 'clear'), // Ctrl + D: Memory Clear
            'p': () => this.dispatchCalculatorEvent('memory', 'add'), // Ctrl + P: Memory Add
            'l': () => this.dispatchCalculatorEvent('clear'), // Ctrl + L: Clear
        };

        if (ctrlMappings[key]) {
            ctrlMappings[key]();
            event.preventDefault();
            return true;
        }
        return false;
    }

    /**
     * Handle alt key combinations for scientific functions
     */
    handleAltCombinations(key, event) {
        const altMappings = {
            's': () => this.handleScientificFunction('sin'),
            'c': () => this.handleScientificFunction('cos'),
            't': () => this.handleScientificFunction('tan'),
            'a': () => this.handleScientificFunction('asin'),
            'o': () => this.handleScientificFunction('acos'),
            'n': () => this.handleScientificFunction('atan'),
            'l': () => this.handleScientificFunction('ln'),
            'g': () => this.handleScientificFunction('log'),
            'r': () => this.handleScientificFunction('sqrt'),
            'p': () => this.handleScientificFunction('π'),
            'e': () => this.handleScientificFunction('e'),
        };

        if (altMappings[key]) {
            altMappings[key]();
            event.preventDefault();
            return true;
        }
        return false;
    }

    /**
     * Handle scientific function shortcuts
     */
    handleScientificFunction(func) {
        // Only trigger if not in an input field
        if (document.activeElement.tagName === 'INPUT') {
            return;
        }
        
        this.dispatchCalculatorEvent('scientific', func);
    }

    /**
     * Determine if default behavior should be prevented
     */
    shouldPreventDefault(key, event) {
        // Prevent default for calculator keys when not in input field
        if (document.activeElement.tagName !== 'INPUT') {
            const preventKeys = [
                '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                '+', '-', '*', '/', '=', 'Enter', '.', 
                'Backspace', 'Delete', 'Escape',
                'F1', 'F2', 'F3', 'F4'
            ];
            
            if (preventKeys.includes(key)) {
                return true;
            }

            // Prevent default for shift combinations
            if (event.shiftKey && ['8', '=', '6', '1', '9', '0', '5'].includes(key)) {
                return true;
            }
        }
        
        return false;
    }

    /**
     * Dispatch calculator events
     */
    dispatchCalculatorEvent(type, value = null) {
        const event = new CustomEvent('calculatorKeyboard', {
            detail: { type, value }
        });
        document.dispatchEvent(event);
    }

    /**
     * Highlight button when key is pressed
     */
    highlightButton(key) {
        const buttonMap = this.getButtonMapping(key);
        if (buttonMap) {
            const button = document.querySelector(`[data-key="${buttonMap}"]`);
            if (button) {
                button.classList.add('keyboard-active');
            }
        }
    }

    /**
     * Remove button highlight
     */
    removeButtonHighlight(key) {
        const buttonMap = this.getButtonMapping(key);
        if (buttonMap) {
            const button = document.querySelector(`[data-key="${buttonMap}"]`);
            if (button) {
                button.classList.remove('keyboard-active');
            }
        }
    }

    /**
     * Map keyboard keys to button data attributes
     */
    getButtonMapping(key) {
        const mappings = {
            '0': '0', '1': '1', '2': '2', '3': '3', '4': '4',
            '5': '5', '6': '6', '7': '7', '8': '8', '9': '9',
            '+': '+', '-': '-', '*': '×', '/': '÷',
            '=': '=