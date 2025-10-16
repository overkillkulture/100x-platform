/**
 * 🏗️ MODULE CORE - Universal Foundation for All 100X Modules
 *
 * Every module gets these functions automatically.
 * Copy-paste template, customize functionality.
 */

window.ModuleCore = {
    // Module configuration
    config: {
        moduleName: null,
        moduleId: null,
        requiresAuth: false,
        encryptData: true,
        trackAnalytics: true,
        version: '1.0'
    },

    /**
     * Initialize module
     */
    init(options = {}) {
        this.config = { ...this.config, ...options };

        console.log(`🚀 ${this.config.moduleName} initialized`);
        console.log(`🔒 Security: ${this.config.encryptData ? 'ENABLED' : 'DISABLED'}`);
        console.log(`📊 Analytics: ${this.config.trackAnalytics ? 'ENABLED' : 'DISABLED'}`);

        // Check authentication if required
        if (this.config.requiresAuth && !this.isAuthenticated()) {
            this.notify('Please log in to use this module', 'warning');
            // Redirect to login (implement when auth system ready)
            return false;
        }

        // Track module load
        if (this.config.trackAnalytics && window.Analytics100X) {
            Analytics100X.trackSystemAccess({
                systemName: this.config.moduleName,
                systemUrl: window.location.pathname,
                accessMethod: 'direct'
            });
        }

        return true;
    },

    /**
     * Save data to localStorage (auto-encrypted if enabled)
     */
    saveData(key, value) {
        const fullKey = `100x_${this.config.moduleId}_${key}`;

        const dataPackage = {
            version: this.config.version,
            created: this.loadData(key)?.created || Date.now(),
            modified: Date.now(),
            encrypted: this.config.encryptData,
            data: value
        };

        try {
            let dataToStore = JSON.stringify(dataPackage);

            // Encrypt if enabled
            if (this.config.encryptData && window.ModuleSecurity) {
                dataToStore = ModuleSecurity.encrypt(dataToStore);
            }

            localStorage.setItem(fullKey, dataToStore);
            return true;
        } catch (error) {
            console.error('❌ Save failed:', error);
            this.notify('Failed to save data', 'error');
            return false;
        }
    },

    /**
     * Load data from localStorage (auto-decrypted if needed)
     */
    loadData(key) {
        const fullKey = `100x_${this.config.moduleId}_${key}`;

        try {
            let stored = localStorage.getItem(fullKey);
            if (!stored) return null;

            // Decrypt if needed
            if (this.config.encryptData && window.ModuleSecurity && !stored.startsWith('{')) {
                stored = ModuleSecurity.decrypt(stored);
            }

            const dataPackage = JSON.parse(stored);
            return dataPackage.data;
        } catch (error) {
            console.error('❌ Load failed:', error);
            return null;
        }
    },

    /**
     * Delete data
     */
    deleteData(key) {
        const fullKey = `100x_${this.config.moduleId}_${key}`;
        localStorage.removeItem(fullKey);
    },

    /**
     * Clear all module data
     */
    clearAllData() {
        const prefix = `100x_${this.config.moduleId}_`;
        Object.keys(localStorage).forEach(key => {
            if (key.startsWith(prefix)) {
                localStorage.removeItem(key);
            }
        });
    },

    /**
     * Track user action (analytics)
     */
    trackAction(actionType, data = {}) {
        if (!this.config.trackAnalytics || !window.Analytics100X) return;

        Analytics100X.trackButtonClick({
            text: actionType,
            id: `${this.config.moduleId}-${actionType}`,
            target: this.config.moduleName,
            system: this.config.moduleId,
            ...data
        });
    },

    /**
     * Show notification to user
     */
    notify(message, type = 'info') {
        // For now, simple alert (replace with toast notification system)
        const icons = {
            success: '✅',
            error: '❌',
            warning: '⚠️',
            info: 'ℹ️'
        };

        const icon = icons[type] || icons.info;
        alert(`${icon} ${message}`);

        console.log(`${icon} ${message}`);
    },

    /**
     * Check if user is authenticated
     */
    isAuthenticated() {
        // Placeholder - implement when auth system ready
        const user = localStorage.getItem('100x_current_user');
        return !!user;
    },

    /**
     * Get current user
     */
    getCurrentUser() {
        try {
            const user = localStorage.getItem('100x_current_user');
            return user ? JSON.parse(user) : null;
        } catch {
            return null;
        }
    },

    /**
     * Export module data (for backup)
     */
    exportData() {
        const prefix = `100x_${this.config.moduleId}_`;
        const exportData = {};

        Object.keys(localStorage).forEach(key => {
            if (key.startsWith(prefix)) {
                const shortKey = key.replace(prefix, '');
                exportData[shortKey] = this.loadData(shortKey);
            }
        });

        return exportData;
    },

    /**
     * Import module data (from backup)
     */
    importData(data) {
        Object.entries(data).forEach(([key, value]) => {
            this.saveData(key, value);
        });

        this.notify('Data imported successfully', 'success');
    },

    /**
     * Get module statistics
     */
    getStats() {
        const prefix = `100x_${this.config.moduleId}_`;
        const keys = Object.keys(localStorage).filter(k => k.startsWith(prefix));

        return {
            totalItems: keys.length,
            totalSize: keys.reduce((sum, key) => {
                return sum + (localStorage.getItem(key)?.length || 0);
            }, 0),
            moduleId: this.config.moduleId,
            moduleName: this.config.moduleName,
            version: this.config.version
        };
    }
};

console.log('🏗️ MODULE CORE LOADED - Universal foundation ready');
