/**
 * STRIPE PAYMENT INTEGRATION
 * Universal payment system for 100X Store
 * Handles Products, Investments, and Campaigns in one checkout
 */

class StripePaymentSystem {
    constructor() {
        // Initialize Stripe (use your publishable key)
        this.stripePublishableKey = 'pk_live_51S5fRP5IBd71iNToyK5xhDyCAuId25fk1pECa2qTc1X1mG1isXAEToeRqXWmPBsd5PxuEunR3jb0aMnG8smkLgI0euC51Veaa'; // LIVE KEY
        this.stripe = null;
        this.initialized = false;

        // Load Stripe SDK
        this.loadStripeSDK();
    }

    loadStripeSDK() {
        // Check if Stripe already loaded
        if (window.Stripe) {
            this.stripe = window.Stripe(this.stripePublishableKey);
            this.initialized = true;
            console.log('✓ Stripe SDK ready');
            return;
        }

        // Load Stripe script
        const script = document.createElement('script');
        script.src = 'https://js.stripe.com/v3/';
        script.onload = () => {
            this.stripe = window.Stripe(this.stripePublishableKey);
            this.initialized = true;
            console.log('✓ Stripe SDK loaded');
        };
        script.onerror = () => {
            console.error('❌ Failed to load Stripe SDK');
        };
        document.head.appendChild(script);
    }

    /**
     * Get cart items from localStorage
     */
    getCart() {
        return JSON.parse(localStorage.getItem('100x_cart') || '[]');
    }

    /**
     * Calculate cart total
     */
    calculateTotal(cart) {
        return cart.reduce((total, item) => total + (item.price * item.quantity), 0);
    }

    /**
     * Create checkout session
     */
    async createCheckout(cart) {
        if (!this.initialized) {
            throw new Error('Stripe not initialized yet. Please wait...');
        }

        try {
            // Send cart to backend to create Stripe session
            const response = await fetch('http://localhost:3001/api/stripe/create-checkout', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('auth_token')}`
                },
                body: JSON.stringify({
                    items: cart,
                    successUrl: `${window.location.origin}/PLATFORM/store-success.html`,
                    cancelUrl: `${window.location.origin}/PLATFORM/store-cart.html`
                })
            });

            if (!response.ok) {
                throw new Error('Failed to create checkout session');
            }

            const session = await response.json();

            // Redirect to Stripe Checkout
            const result = await this.stripe.redirectToCheckout({
                sessionId: session.id
            });

            if (result.error) {
                throw new Error(result.error.message);
            }

        } catch (error) {
            console.error('Checkout error:', error);
            throw error;
        }
    }

    /**
     * Quick checkout button (for single items)
     */
    async quickCheckout(item) {
        try {
            const cart = [{ ...item, quantity: 1 }];
            await this.createCheckout(cart);
        } catch (error) {
            alert(`Checkout failed: ${error.message}`);
        }
    }

    /**
     * Full cart checkout
     */
    async checkoutCart() {
        try {
            const cart = this.getCart();

            if (cart.length === 0) {
                alert('Your cart is empty!');
                return;
            }

            await this.createCheckout(cart);
        } catch (error) {
            alert(`Checkout failed: ${error.message}`);
        }
    }

    /**
     * Add item to cart
     */
    addToCart(item) {
        const cart = this.getCart();

        // Check if item already in cart
        const existing = cart.find(i => i.id === item.id);
        if (existing) {
            existing.quantity += 1;
        } else {
            cart.push({ ...item, quantity: 1 });
        }

        localStorage.setItem('100x_cart', JSON.stringify(cart));

        // Trigger event for cart UI updates
        window.dispatchEvent(new Event('cartUpdated'));

        return cart;
    }

    /**
     * Remove item from cart
     */
    removeFromCart(itemId) {
        let cart = this.getCart();
        cart = cart.filter(item => item.id !== itemId);
        localStorage.setItem('100x_cart', JSON.stringify(cart));
        window.dispatchEvent(new Event('cartUpdated'));
        return cart;
    }

    /**
     * Update item quantity
     */
    updateQuantity(itemId, quantity) {
        const cart = this.getCart();
        const item = cart.find(i => i.id === itemId);
        if (item) {
            item.quantity = Math.max(1, quantity);
            localStorage.setItem('100x_cart', JSON.stringify(cart));
            window.dispatchEvent(new Event('cartUpdated'));
        }
        return cart;
    }

    /**
     * Clear cart
     */
    clearCart() {
        localStorage.removeItem('100x_cart');
        window.dispatchEvent(new Event('cartUpdated'));
    }
}

// Initialize global instance
window.StripePayment = new StripePaymentSystem();

console.log('✓ Stripe Payment System loaded');


/**
 * HELPER FUNCTIONS FOR EASY USE
 */

// Add "Buy Now" button to product
function createBuyButton(product) {
    const button = document.createElement('button');
    button.className = 'buy-button';
    button.innerHTML = `💳 Buy Now - $${product.price}`;
    button.onclick = () => {
        window.StripePayment.quickCheckout(product);
    };
    return button;
}

// Add "Add to Cart" button
function createAddToCartButton(product) {
    const button = document.createElement('button');
    button.className = 'add-to-cart-button';
    button.innerHTML = `🛒 Add to Cart - $${product.price}`;
    button.onclick = () => {
        window.StripePayment.addToCart(product);
        button.innerHTML = '✓ Added to Cart!';
        setTimeout(() => {
            button.innerHTML = `🛒 Add to Cart - $${product.price}`;
        }, 2000);
    };
    return button;
}

// Checkout cart button
function createCheckoutButton() {
    const button = document.createElement('button');
    button.className = 'checkout-button';
    button.innerHTML = '💳 Proceed to Checkout';
    button.onclick = () => {
        window.StripePayment.checkoutCart();
    };
    return button;
}
