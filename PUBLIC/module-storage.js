/**
 * 💾 MODULE STORAGE - Data Management for All Modules
 *
 * Unified storage system with backup, sync, and export capabilities.
 */

window.ModuleStorage = {
    /**
     * Get all module data (for analytics/debugging)
     */
    getAllModuleData() {
        const data = {};

        Object.keys(localStorage).forEach(key => {
            if (key.startsWith('100x_')) {
                data[key] = localStorage.getItem(key);
            }
        });

        return data;
    },

    /**
     * Get storage usage by module
     */
    getStorageUsage() {
        const usage = {};
        let totalSize = 0;

        Object.keys(localStorage).forEach(key => {
            if (key.startsWith('100x_')) {
                const size = localStorage.getItem(key).length;
                const module = key.split('_')[1] || 'unknown';

                if (!usage[module]) {
                    usage[module] = { size: 0, items: 0 };
                }

                usage[module].size += size;
                usage[module].items++;
                totalSize += size;
            }
        });

        return {
            byModule: usage,
            totalSize,
            totalItems: Object.values(usage).reduce((sum, m) => sum + m.items, 0),
            maxSize: 5 * 1024 * 1024, // 5MB typical localStorage limit
            percentUsed: (totalSize / (5 * 1024 * 1024)) * 100
        };
    },

    /**
     * Export all data (for backup)
     */
    exportAll() {
        const data = this.getAllModuleData();

        const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `100x_backup_${Date.now()}.json`;
        a.click();
        URL.revokeObjectURL(url);

        console.log('📦 Backup exported successfully');
        return true;
    },

    /**
     * Import data (from backup)
     */
    importAll(jsonData) {
        try {
            const data = typeof jsonData === 'string' ? JSON.parse(jsonData) : jsonData;

            Object.entries(data).forEach(([key, value]) => {
                localStorage.setItem(key, value);
            });

            console.log('📥 Data imported successfully');
            return true;
        } catch (error) {
            console.error('❌ Import failed:', error);
            return false;
        }
    },

    /**
     * Clear old data (cleanup)
     */
    clearOldData(daysOld = 30) {
        const cutoffTime = Date.now() - (daysOld * 24 * 60 * 60 * 1000);
        let deletedCount = 0;

        Object.keys(localStorage).forEach(key => {
            if (!key.startsWith('100x_')) return;

            try {
                const data = JSON.parse(localStorage.getItem(key));
                if (data.modified && data.modified < cutoffTime) {
                    localStorage.removeItem(key);
                    deletedCount++;
                }
            } catch {
                // Skip if can't parse
            }
        });

        console.log(`🗑️ Deleted ${deletedCount} old items`);
        return deletedCount;
    },

    /**
     * Sync to cloud (placeholder for future implementation)
     */
    async syncToCloud() {
        // TODO: Implement cloud sync
        console.log('☁️ Cloud sync not yet implemented');
        return false;
    },

    /**
     * Get data statistics
     */
    getStats() {
        const usage = this.getStorageUsage();

        return {
            ...usage,
            oldestItem: this.getOldestItem(),
            newestItem: this.getNewestItem(),
            moduleCount: Object.keys(usage.byModule).length
        };
    },

    /**
     * Get oldest stored item
     */
    getOldestItem() {
        let oldest = null;
        let oldestTime = Date.now();

        Object.keys(localStorage).forEach(key => {
            if (!key.startsWith('100x_')) return;

            try {
                const data = JSON.parse(localStorage.getItem(key));
                if (data.created && data.created < oldestTime) {
                    oldestTime = data.created;
                    oldest = { key, created: data.created };
                }
            } catch {}
        });

        return oldest;
    },

    /**
     * Get newest stored item
     */
    getNewestItem() {
        let newest = null;
        let newestTime = 0;

        Object.keys(localStorage).forEach(key => {
            if (!key.startsWith('100x_')) return;

            try {
                const data = JSON.parse(localStorage.getItem(key));
                if (data.modified && data.modified > newestTime) {
                    newestTime = data.modified;
                    newest = { key, modified: data.modified };
                }
            } catch {}
        });

        return newest;
    },

    /**
     * Check if storage is nearly full
     */
    checkStorageHealth() {
        const usage = this.getStorageUsage();

        if (usage.percentUsed > 90) {
            return {
                status: 'critical',
                message: 'Storage nearly full! Please export and clear old data.',
                percentUsed: usage.percentUsed
            };
        } else if (usage.percentUsed > 75) {
            return {
                status: 'warning',
                message: 'Storage usage high. Consider cleanup.',
                percentUsed: usage.percentUsed
            };
        }

        return {
            status: 'healthy',
            message: 'Storage usage normal.',
            percentUsed: usage.percentUsed
        };
    },

    /**
     * Create searchable index of all data
     */
    createSearchIndex() {
        const index = [];

        Object.keys(localStorage).forEach(key => {
            if (!key.startsWith('100x_')) return;

            try {
                const data = JSON.parse(localStorage.getItem(key));
                index.push({
                    key,
                    module: key.split('_')[1],
                    created: data.created,
                    modified: data.modified,
                    size: localStorage.getItem(key).length
                });
            } catch {}
        });

        return index;
    }
};

console.log('💾 MODULE STORAGE LOADED');
console.log('📊 Storage monitoring active');
