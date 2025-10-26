// Task Manager Application - Main Logic
class TaskManager {
    constructor() {
        this.tasks = [];
        this.currentFilter = 'all';
        this.editingTaskId = null;
        
        // Initialize DOM elements
        this.taskInput = document.getElementById('task-input');
        this.addButton = document.getElementById('add-task');
        this.taskList = document.getElementById('task-list');
        this.filterButtons = document.querySelectorAll('.filter-btn');
        this.taskCounter = document.getElementById('task-counter');
        this.clearCompleted = document.getElementById('clear-completed');
        
        this.init();
    }
    
    // Initialize the application
    init() {
        this.loadTasks();
        this.bindEvents();
        this.render();
        this.updateCounter();
    }
    
    // Bind all event listeners
    bindEvents() {
        // Add task events
        this.addButton.addEventListener('click', () => this.addTask());
        this.taskInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.addTask();
        });
        
        // Filter events
        this.filterButtons.forEach(btn => {
            btn.addEventListener('click', (e) => {
                this.setFilter(e.target.dataset.filter);
            });
        });
        
        // Clear completed tasks
        this.clearCompleted.addEventListener('click', () => this.clearCompletedTasks());
        
        // Task list events (using event delegation)
        this.taskList.addEventListener('click', (e) => this.handleTaskClick(e));
        this.taskList.addEventListener('keypress', (e) => this.handleTaskKeypress(e));
        this.taskList.addEventListener('blur', (e) => this.handleTaskBlur(e), true);
    }
    
    // Add a new task
    addTask() {
        const text = this.taskInput.value.trim();
        if (!text) return;
        
        const task = {
            id: Date.now().toString(),
            text: text,
            completed: false,
            createdAt: new Date().toISOString()
        };
        
        this.tasks.unshift(task);
        this.taskInput.value = '';
        this.saveTasks();
        this.render();
        this.updateCounter();
        
        // Focus back to input for continuous task adding
        this.taskInput.focus();
    }
    
    // Toggle task completion status
    toggleTask(id) {
        const task = this.tasks.find(t => t.id === id);
        if (task) {
            task.completed = !task.completed;
            this.saveTasks();
            this.render();
            this.updateCounter();
        }
    }
    
    // Delete a task
    deleteTask(id) {
        this.tasks = this.tasks.filter(t => t.id !== id);
        this.saveTasks();
        this.render();
        this.updateCounter();
    }
    
    // Start editing a task
    editTask(id) {
        this.editingTaskId = id;
        this.render();
        
        // Focus on the input field
        const input = document.querySelector(`[data-task-id="${id}"] .edit-input`);
        if (input) {
            input.focus();
            input.select();
        }
    }
    
    // Save edited task
    saveEdit(id, newText) {
        const text = newText.trim();
        if (!text) {
            this.deleteTask(id);
            return;
        }
        
        const task = this.tasks.find(t => t.id === id);
        if (task) {
            task.text = text;
            this.saveTasks();
        }
        
        this.editingTaskId = null;
        this.render();
    }
    
    // Cancel editing
    cancelEdit() {
        this.editingTaskId = null;
        this.render();
    }
    
    // Set active filter
    setFilter(filter) {
        this.currentFilter = filter;
        
        // Update active filter button
        this.filterButtons.forEach(btn => {
            btn.classList.toggle('active', btn.dataset.filter === filter);
        });
        
        this.render();
    }
    
    // Get filtered tasks based on current filter
    getFilteredTasks() {
        switch (this.currentFilter) {
            case 'active':
                return this.tasks.filter(task => !task.completed);
            case 'completed':
                return this.tasks.filter(task => task.completed);
            default:
                return this.tasks;
        }
    }
    
    // Clear all completed tasks
    clearCompletedTasks() {
        this.tasks = this.tasks.filter(task => !task.completed);
        this.saveTasks();
        this.render();
        this.updateCounter();
    }
    
    // Handle clicks on task list
    handleTaskClick(e) {
        const taskItem = e.target.closest('.task-item');
        if (!taskItem) return;
        
        const taskId = taskItem.dataset.taskId;
        
        if (e.target.classList.contains('toggle-btn')) {
            this.toggleTask(taskId);
        } else if (e.target.classList.contains('edit-btn')) {
            this.editTask(taskId);
        } else if (e.target.classList.contains('delete-btn')) {
            this.deleteTask(taskId);
        } else if (e.target.classList.contains('task-text') && this.editingTaskId !== taskId) {
            this.editTask(taskId);
        }
    }
    
    // Handle keypress events on task list
    handleTaskKeypress(e) {
        if (e.target.classList.contains('edit-input')) {
            const taskId = e.target.closest('.task-item').dataset.taskId;
            
            if (e.key === 'Enter') {
                this.saveEdit(taskId, e.target.value);
            } else if (e.key === 'Escape') {
                this.cancelEdit();
            }
        }
    }
    
    // Handle blur events on edit inputs
    handleTaskBlur(e) {
        if (e.target.classList.contains('edit-input')) {
            const taskId = e.target.closest('.task-item').dataset.taskId;
            this.saveEdit(taskId, e.target.value);
        }
    }
    
    // Render the task list
    render() {
        const filteredTasks = this.getFilteredTasks();
        
        if (filteredTasks.length === 0) {
            this.taskList.innerHTML = `
                <div class="empty-state">
                    <p>${this.getEmptyStateMessage()}</p>
                </div>
            `;
            return;
        }
        
        this.taskList.innerHTML = filteredTasks.map(task => {
            const isEditing = this.editingTaskId === task.id;
            
            return `
                <div class="task-item ${task.completed ? 'completed' : ''}" data-task-id="${task.id}">
                    <button class="toggle-btn" title="${task.completed ? 'Mark as incomplete' : 'Mark as complete'}">
                        <span class="checkmark">${task.completed ? '✓' : ''}</span>
                    </button>
                    
                    <div class="task-content">
                        ${isEditing ? `
                            <input type="text" class="edit-input" value="${this.escapeHtml(task.text)}">
                        ` : `
                            <span class="task-text">${this.escapeHtml(task.text)}</span>
                        `}
                    </div>
                    
                    <div class="task-actions">
                        ${!isEditing ? `
                            <button class="edit-btn" title="Edit task">✎</button>
                        ` : ''}
                        <button class="delete-btn" title="Delete task">×</button>
                    </div>
                </div>
            `;
        }).join('');
    }
    
    // Get appropriate empty state message
    getEmptyStateMessage() {
        switch (this.currentFilter) {
            case 'active':
                return 'No active tasks. Great job! 🎉';
            case 'completed':
                return 'No completed tasks yet.';
            default:
                return 'No tasks yet. Add one above to get started!';
        }
    }
    
    // Update task counter
    updateCounter() {
        const activeTasks = this.tasks.filter(task => !task.completed).length;
        const totalTasks = this.tasks.length;
        const completedTasks = totalTasks - activeTasks;
        
        this.taskCounter.textContent = `${activeTasks} active, ${completedTasks} completed`;
        
        // Show/hide clear completed button
        this.clearCompleted.style.display = completedTasks > 0 ? 'block' : 'none';
    }
    
    // Escape HTML to prevent XSS
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
    
    // Load tasks from localStorage
    loadTasks() {
        try {
            const stored = localStorage.getItem('personal-task-manager-tasks');
            if (stored) {
                this.tasks = JSON.parse(stored);
                // Ensure all tasks have required properties
                this.tasks = this.tasks.map(task => ({
                    id: task.id || Date.now().toString(),
                    text: task.text || '',
                    completed: Boolean(task.completed),
                    createdAt: task.createdAt || new Date().toISOString()
                }));
            }
        } catch (error) {
            console.error('Error loading tasks from localStorage:', error);
            this.tasks = [];
        }
    }
    
    // Save tasks to localStorage
    saveTasks() {
        try {
            localStorage.setItem('personal-task-manager-tasks', JSON.stringify(this.tasks));
        } catch (error) {
            console.error('Error saving tasks to localStorage:', error);
            // Could implement fallback storage or user notification here
        }
    }
    
    // Public method to get task statistics
    getStats() {
        const total = this.tasks.length;
        const completed = this.tasks.filter(task => task.completed).length;
        const active = total - completed;
        
        return { total, active, completed };
    }
    
    // Public method to export tasks (for potential future features)
    exportTasks() {
        return {
            tasks: this.tasks,
            exportDate: new Date().toISOString(),
            version: '1.0'
        };
    }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    // Create global task manager instance
    window.taskManager = new TaskManager();
    
    // Add keyboard shortcuts
    document.addEventListener('keydown', (e) => {
        // Focus input with Ctrl/Cmd + /
        if ((e.ctrlKey || e.metaKey) && e.key === '/') {
            e.preventDefault();
            document.getElementById('task-input').focus();
        }
        
        // Clear completed with Ctrl/Cmd + Shift + C
        if ((e.ctrlKey || e.metaKey) && e.shiftKey && e.key === 'C') {
            e.preventDefault();
            window.taskManager.clearCompletedTasks();
        }
    });
    
    // Handle browser back/forward buttons for filter state
    window.addEventListener('popstate', (e) => {
        const filter = new URLSearchParams(window.location.search).get('filter') || 'all';