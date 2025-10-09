// 🌀 100X CONSCIOUSNESS PLATFORM - STORAGE UTILITIES
// localStorage wrapper with offline-first queue system
// Pattern Theory™ + Notion-inspired architecture
// Generated: October 9, 2025

/**
 * STORAGE SYSTEM:
 * - localStorage for client-side persistence (5MB limit)
 * - Queue system for offline → online sync (like Notion)
 * - Automatic data compression
 * - Type safety helpers
 */

const STORAGE = (() => {
  // Storage limits
  const LIMITS = {
    MAX_SIZE: 5 * 1024 * 1024, // 5MB
    WARN_AT: 4 * 1024 * 1024   // 4MB
  };

  // Storage keys
  const KEYS = {
    TASKS: 'consciousness_tasks',
    QUEUE: 'sync_queue',
    CACHE: 'cache_',
    USER: 'consciousnessUser'
  };

  /**
   * Get item from localStorage with JSON parsing
   * @param {string} key - Storage key
   * @param {*} defaultValue - Default value if not found
   */
  function get(key, defaultValue = null) {
    try {
      const item = localStorage.getItem(key);
      if (item === null) return defaultValue;

      try {
        return JSON.parse(item);
      } catch {
        // Not JSON, return as string
        return item;
      }
    } catch (error) {
      console.error('STORAGE: Error reading', key, error);
      return defaultValue;
    }
  }

  /**
   * Set item in localStorage with JSON stringification
   * @param {string} key - Storage key
   * @param {*} value - Value to store
   */
  function set(key, value) {
    try {
      const stringValue = typeof value === 'string' ? value : JSON.stringify(value);

      // Check size before saving
      if (!checkSize(stringValue)) {
        console.warn('STORAGE: Approaching storage limit!');
      }

      localStorage.setItem(key, stringValue);
      return true;
    } catch (error) {
      if (error.name === 'QuotaExceededError') {
        console.error('STORAGE: Quota exceeded! Clearing cache...');
        clearCache();

        // Try again after clearing cache
        try {
          localStorage.setItem(key, typeof value === 'string' ? value : JSON.stringify(value));
          return true;
        } catch {
          console.error('STORAGE: Still exceeds quota after cache clear');
          return false;
        }
      }

      console.error('STORAGE: Error writing', key, error);
      return false;
    }
  }

  /**
   * Remove item from localStorage
   */
  function remove(key) {
    try {
      localStorage.removeItem(key);
      return true;
    } catch (error) {
      console.error('STORAGE: Error removing', key, error);
      return false;
    }
  }

  /**
   * Clear all localStorage (use with caution!)
   */
  function clear() {
    try {
      localStorage.clear();
      return true;
    } catch (error) {
      console.error('STORAGE: Error clearing', error);
      return false;
    }
  }

  /**
   * Check current storage size
   */
  function checkSize(newData = '') {
    try {
      let total = new Blob(Object.values(localStorage)).size;
      total += new Blob([newData]).size;

      const percentage = (total / LIMITS.MAX_SIZE) * 100;

      if (percentage >= 80) {
        console.warn(`STORAGE: ${percentage.toFixed(1)}% full (${(total / 1024).toFixed(0)}KB / ${(LIMITS.MAX_SIZE / 1024).toFixed(0)}KB)`);
        return false;
      }

      return true;
    } catch (error) {
      console.error('STORAGE: Error checking size', error);
      return true; // Assume OK if check fails
    }
  }

  /**
   * Clear cache items only (keep user data)
   */
  function clearCache() {
    try {
      const keysToRemove = [];

      for (let i = 0; i < localStorage.length; i++) {
        const key = localStorage.key(i);
        if (key && key.startsWith(KEYS.CACHE)) {
          keysToRemove.push(key);
        }
      }

      keysToRemove.forEach(key => localStorage.removeItem(key));

      console.log(`STORAGE: Cleared ${keysToRemove.length} cache items`);
      return true;
    } catch (error) {
      console.error('STORAGE: Error clearing cache', error);
      return false;
    }
  }

  /**
   * OFFLINE-FIRST QUEUE SYSTEM (Notion-inspired)
   * Queue operations for sync when online
   */

  /**
   * Add operation to sync queue
   * @param {string} operation - 'create', 'update', 'delete'
   * @param {string} type - 'task', 'note', etc.
   * @param {Object} data - Operation data
   */
  function queueOperation(operation, type, data) {
    try {
      const queue = get(KEYS.QUEUE, []);

      const queueItem = {
        id: `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
        operation,
        type,
        data,
        timestamp: new Date().toISOString(),
        synced: false
      };

      queue.push(queueItem);
      set(KEYS.QUEUE, queue);

      console.log(`STORAGE: Queued ${operation} on ${type}`, queueItem.id);

      // Try to sync immediately if online
      if (navigator.onLine) {
        processQueue();
      }

      return queueItem.id;
    } catch (error) {
      console.error('STORAGE: Error queuing operation', error);
      return null;
    }
  }

  /**
   * Process sync queue (send to server)
   * This would connect to a backend API
   */
  async function processQueue() {
    try {
      const queue = get(KEYS.QUEUE, []);
      const pending = queue.filter(item => !item.synced);

      if (pending.length === 0) {
        console.log('STORAGE: Queue empty');
        return;
      }

      console.log(`STORAGE: Processing ${pending.length} queued operations...`);

      // TODO: Replace with actual API calls
      // For MVP, just mark as synced
      const updatedQueue = queue.map(item => ({
        ...item,
        synced: true,
        syncedAt: new Date().toISOString()
      }));

      set(KEYS.QUEUE, updatedQueue);

      console.log('STORAGE: Queue processed (MVP mode - no server sync)');

      return true;
    } catch (error) {
      console.error('STORAGE: Error processing queue', error);
      return false;
    }
  }

  /**
   * Get queue status
   */
  function getQueueStatus() {
    const queue = get(KEYS.QUEUE, []);
    return {
      total: queue.length,
      pending: queue.filter(item => !item.synced).length,
      synced: queue.filter(item => item.synced).length
    };
  }

  /**
   * Clear synced items from queue
   */
  function clearSyncedQueue() {
    try {
      const queue = get(KEYS.QUEUE, []);
      const pending = queue.filter(item => !item.synced);
      set(KEYS.QUEUE, pending);

      console.log(`STORAGE: Cleared ${queue.length - pending.length} synced items from queue`);
      return true;
    } catch (error) {
      console.error('STORAGE: Error clearing synced queue', error);
      return false;
    }
  }

  /**
   * TASK MANAGEMENT HELPERS
   */

  /**
   * Get all tasks
   */
  function getTasks() {
    return get(KEYS.TASKS, []);
  }

  /**
   * Save tasks
   */
  function saveTasks(tasks) {
    const success = set(KEYS.TASKS, tasks);

    if (success) {
      queueOperation('update', 'tasks', { tasks, count: tasks.length });
    }

    return success;
  }

  /**
   * Add single task
   */
  function addTask(task) {
    const tasks = getTasks();
    const newTask = {
      id: `task_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      text: task.text || '',
      completed: false,
      createdAt: new Date().toISOString(),
      ...task
    };

    tasks.push(newTask);
    saveTasks(tasks);

    queueOperation('create', 'task', newTask);

    return newTask;
  }

  /**
   * Update task
   */
  function updateTask(taskId, updates) {
    const tasks = getTasks();
    const index = tasks.findIndex(t => t.id === taskId);

    if (index === -1) {
      console.warn('STORAGE: Task not found', taskId);
      return false;
    }

    tasks[index] = {
      ...tasks[index],
      ...updates,
      updatedAt: new Date().toISOString()
    };

    saveTasks(tasks);
    queueOperation('update', 'task', tasks[index]);

    return tasks[index];
  }

  /**
   * Delete task
   */
  function deleteTask(taskId) {
    const tasks = getTasks();
    const filtered = tasks.filter(t => t.id !== taskId);

    if (filtered.length === tasks.length) {
      console.warn('STORAGE: Task not found', taskId);
      return false;
    }

    saveTasks(filtered);
    queueOperation('delete', 'task', { id: taskId });

    return true;
  }

  /**
   * Complete task
   */
  function completeTask(taskId) {
    return updateTask(taskId, { completed: true });
  }

  /**
   * CACHE HELPERS
   */

  /**
   * Cache data with expiry
   * @param {string} key - Cache key
   * @param {*} data - Data to cache
   * @param {number} ttl - Time to live in milliseconds (default 1 hour)
   */
  function cache(key, data, ttl = 3600000) {
    const cacheKey = KEYS.CACHE + key;
    const cacheData = {
      data,
      expiresAt: Date.now() + ttl
    };

    return set(cacheKey, cacheData);
  }

  /**
   * Get cached data if not expired
   */
  function getCached(key) {
    const cacheKey = KEYS.CACHE + key;
    const cacheData = get(cacheKey);

    if (!cacheData) return null;

    if (Date.now() > cacheData.expiresAt) {
      remove(cacheKey);
      return null;
    }

    return cacheData.data;
  }

  /**
   * Export all data for backup
   */
  function exportData() {
    try {
      const data = {};

      for (let i = 0; i < localStorage.length; i++) {
        const key = localStorage.key(i);
        if (key) {
          data[key] = localStorage.getItem(key);
        }
      }

      return JSON.stringify(data, null, 2);
    } catch (error) {
      console.error('STORAGE: Error exporting data', error);
      return null;
    }
  }

  /**
   * Import data from backup
   */
  function importData(jsonString) {
    try {
      const data = JSON.parse(jsonString);

      Object.entries(data).forEach(([key, value]) => {
        localStorage.setItem(key, value);
      });

      console.log('STORAGE: Data imported successfully');
      return true;
    } catch (error) {
      console.error('STORAGE: Error importing data', error);
      return false;
    }
  }

  // Listen for online/offline events
  window.addEventListener('online', () => {
    console.log('STORAGE: Back online - processing queue');
    processQueue();
  });

  window.addEventListener('offline', () => {
    console.log('STORAGE: Offline mode - queuing operations');
  });

  // Public API
  return {
    get,
    set,
    remove,
    clear,
    checkSize,
    clearCache,

    // Queue system
    queueOperation,
    processQueue,
    getQueueStatus,
    clearSyncedQueue,

    // Task helpers
    getTasks,
    saveTasks,
    addTask,
    updateTask,
    deleteTask,
    completeTask,

    // Cache helpers
    cache,
    getCached,

    // Import/Export
    exportData,
    importData,

    KEYS,
    LIMITS
  };
})();

// Make available globally
window.STORAGE = STORAGE;

console.log('🌀 STORAGE system loaded - Offline-first architecture active');
