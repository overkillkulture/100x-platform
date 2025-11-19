/**
 * Scientific Calculator Core Logic
 * Handles all mathematical operations and scientific functions
 */

class Calculator {
    constructor() {
        this.currentValue = '0';
        this.previousValue = null;
        this.operator = null;
        this.waitingForOperand = false;
        this.lastOperation = null;
        this.angleMode = 'deg'; // 'deg' or 'rad'
    }

    // Basic arithmetic operations
    add(a, b) {
        return a + b;
    }

    subtract(a, b) {
        return a - b;
    }

    multiply(a, b) {
        return a * b;
    }

    divide(a, b) {
        if (b === 0) {
            throw new Error('Division by zero');
        }
        return a / b;
    }

    // Scientific functions
    sin(value) {
        const radians = this.angleMode === 'deg' ? this.degreesToRadians(value) : value;
        return Math.sin(radians);
    }

    cos(value) {
        const radians = this.angleMode === 'deg' ? this.degreesToRadians(value) : value;
        return Math.cos(radians);
    }

    tan(value) {
        const radians = this.angleMode === 'deg' ? this.degreesToRadians(value) : value;
        const result = Math.tan(radians);
        // Handle tan(90°) and similar cases
        if (Math.abs(result) > 1e10) {
            throw new Error('Math Error');
        }
        return result;
    }

    log(value) {
        if (value <= 0) {
            throw new Error('Invalid input for logarithm');
        }
        return Math.log10(value);
    }

    ln(value) {
        if (value <= 0) {
            throw new Error('Invalid input for natural logarithm');
        }
        return Math.log(value);
    }

    sqrt(value) {
        if (value < 0) {
            throw new Error('Invalid input for square root');
        }
        return Math.sqrt(value);
    }

    power(base, exponent) {
        const result = Math.pow(base, exponent);
        if (!isFinite(result)) {
            throw new Error('Math Error');
        }
        return result;
    }

    factorial(n) {
        if (n < 0 || !Number.isInteger(n)) {
            throw new Error('Factorial requires non-negative integer');
        }
        if (n > 170) {
            throw new Error('Number too large for factorial');
        }
        if (n === 0 || n === 1) {
            return 1;
        }
        let result = 1;
        for (let i = 2; i <= n; i++) {
            result *= i;
        }
        return result;
    }

    // Additional scientific functions
    exp(value) {
        return Math.exp(value);
    }

    abs(value) {
        return Math.abs(value);
    }

    reciprocal(value) {
        if (value === 0) {
            throw new Error('Division by zero');
        }
        return 1 / value;
    }

    percent(value) {
        return value / 100;
    }

    // Angle conversion utilities
    degreesToRadians(degrees) {
        return degrees * (Math.PI / 180);
    }

    radiansToDegrees(radians) {
        return radians * (180 / Math.PI);
    }

    // Toggle angle mode
    toggleAngleMode() {
        this.angleMode = this.angleMode === 'deg' ? 'rad' : 'deg';
        return this.angleMode;
    }

    // Input handling
    inputNumber(num) {
        if (this.waitingForOperand) {
            this.currentValue = num;
            this.waitingForOperand = false;
        } else {
            this.currentValue = this.currentValue === '0' ? num : this.currentValue + num;
        }
        this.dispatchUpdate();
    }

    inputDecimal() {
        if (this.waitingForOperand) {
            this.currentValue = '0.';
            this.waitingForOperand = false;
        } else if (this.currentValue.indexOf('.') === -1) {
            this.currentValue += '.';
        }
        this.dispatchUpdate();
    }

    inputOperator(nextOperator) {
        const inputValue = parseFloat(this.currentValue);

        if (this.previousValue === null) {
            this.previousValue = inputValue;
        } else if (this.operator) {
            const currentValue = this.previousValue || 0;
            const newValue = this.performCalculation(this.operator, currentValue, inputValue);

            this.currentValue = String(newValue);
            this.previousValue = newValue;
        }

        this.waitingForOperand = true;
        this.operator = nextOperator;
        this.dispatchUpdate();
    }

    // Perform calculation based on operator
    performCalculation(operator, firstValue, secondValue) {
        try {
            switch (operator) {
                case '+':
                    return this.add(firstValue, secondValue);
                case '-':
                    return this.subtract(firstValue, secondValue);
                case '×':
                case '*':
                    return this.multiply(firstValue, secondValue);
                case '÷':
                case '/':
                    return this.divide(firstValue, secondValue);
                case '^':
                case '**':
                    return this.power(firstValue, secondValue);
                default:
                    return secondValue;
            }
        } catch (error) {
            throw error;
        }
    }

    // Execute scientific function
    executeFunction(func) {
        try {
            const value = parseFloat(this.currentValue);
            let result;

            switch (func) {
                case 'sin':
                    result = this.sin(value);
                    break;
                case 'cos':
                    result = this.cos(value);
                    break;
                case 'tan':
                    result = this.tan(value);
                    break;
                case 'log':
                    result = this.log(value);
                    break;
                case 'ln':
                    result = this.ln(value);
                    break;
                case 'sqrt':
                    result = this.sqrt(value);
                    break;
                case 'exp':
                    result = this.exp(value);
                    break;
                case 'abs':
                    result = this.abs(value);
                    break;
                case '1/x':
                    result = this.reciprocal(value);
                    break;
                case 'x²':
                    result = this.power(value, 2);
                    break;
                case 'x³':
                    result = this.power(value, 3);
                    break;
                case 'n!':
                    result = this.factorial(value);
                    break;
                case '%':
                    result = this.percent(value);
                    break;
                case '±':
                    result = -value;
                    break;
                default:
                    throw new Error('Unknown function');
            }

            // Format result to avoid floating point precision issues
            result = this.formatResult(result);
            this.currentValue = String(result);
            this.waitingForOperand = true;
            this.dispatchUpdate();
            
        } catch (error) {
            this.handleError(error.message);
        }
    }

    // Calculate final result
    calculate() {
        const inputValue = parseFloat(this.currentValue);

        if (this.previousValue !== null && this.operator) {
            try {
                const newValue = this.performCalculation(this.operator, this.previousValue, inputValue);
                const formattedResult = this.formatResult(newValue);
                
                this.lastOperation = {
                    operator: this.operator,
                    firstValue: this.previousValue,
                    secondValue: inputValue,
                    result: formattedResult
                };

                this.currentValue = String(formattedResult);
                this.previousValue = null;
                this.operator = null;
                this.waitingForOperand = true;
                
                this.dispatchUpdate();
            } catch (error) {
                this.handleError(error.message);
            }
        }
    }

    // Clear operations
    clear() {
        this.currentValue = '0';
        this.previousValue = null;
        this.operator = null;
        this.waitingForOperand = false;
        this.lastOperation = null;
        this.dispatchUpdate();
    }

    clearEntry() {
        this.currentValue = '0';
        this.waitingForOperand = false;
        this.dispatchUpdate();
    }

    // Backspace functionality
    backspace() {
        if (!this.waitingForOperand) {
            if (this.currentValue.length > 1) {
                this.currentValue = this.currentValue.slice(0, -1);
            } else {
                this.currentValue = '0';
            }
            this.dispatchUpdate();
        }
    }

    // Format result to handle precision issues
    formatResult(value) {
        if (!isFinite(value)) {
            throw new Error('Math Error');
        }

        // Handle very small numbers (close to zero)
        if (Math.abs(value) < 1e-10) {
            return 0;
        }

        // Round to 12 significant digits to avoid floating point errors
        const rounded = Math.round(value * 1e12) / 1e12;
        
        // Convert to string and handle scientific notation for very large/small numbers
        if (Math.abs(rounded) >= 1e12 || (Math.abs(rounded) < 1e-6 && rounded !== 0)) {
            return parseFloat(rounded.toExponential(6));
        }

        return rounded;
    }

    // Error handling
    handleError(message) {
        this.currentValue = 'Error';
        this.previousValue = null;
        this.operator = null;
        this.waitingForOperand = true;
        
        // Dispatch error event
        window.dispatchEvent(new CustomEvent('calculatorError', {
            detail: { message }
        }));
        
        this.dispatchUpdate();
        
        // Auto-clear error after 2 seconds
        setTimeout(() => {
            if (this.currentValue === 'Error') {
                this.clear();
            }
        }, 2000);
    }

    // Get current state
    getState() {
        return {
            currentValue: this.currentValue,
            previousValue: this.previousValue,
            operator: this.operator,
            waitingForOperand: this.waitingForOperand,
            angleMode: this.angleMode,
            lastOperation: this.lastOperation
        };
    }

    // Dispatch update event
    dispatchUpdate() {
        window.dispatchEvent(new CustomEvent('calculatorUpdate', {
            detail: this.getState()
        }));
    }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = Calculator;
} else {
    window.Calculator = Calculator;
}