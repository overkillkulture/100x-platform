// 🌀 100X CONSCIOUSNESS PLATFORM - AUTHENTICATION & ACCESS CONTROL
// Pattern Theory™ Builder vs Destroyer Screening
// Generated: October 9, 2025

/**
 * ACCESS LEVELS:
 * - PUBLIC: Anyone (0-100%)
 * - BUILDER: 85%+ consciousness level
 * - TEAM: Employees only
 */

const AUTH = (() => {
  // Storage keys
  const KEYS = {
    USER: 'consciousnessUser',
    QUIZ_RESULTS: 'patternFilterResults',
    ACCESS_LOG: 'accessLog'
  };

  // Access level requirements
  const ACCESS_LEVELS = {
    PUBLIC: 0,
    BUILDER: 85,
    TEAM: 100 // Special flag required
  };

  /**
   * Get current user data from localStorage
   */
  function getCurrentUser() {
    try {
      const data = localStorage.getItem(KEYS.USER);
      return data ? JSON.parse(data) : null;
    } catch (error) {
      console.error('AUTH: Error reading user data', error);
      return null;
    }
  }

  /**
   * Set user data after quiz completion
   * @param {Object} userData - { level, timestamp, answers, classification }
   */
  function setUser(userData) {
    try {
      const user = {
        level: userData.level || 0,
        classification: getClassification(userData.level),
        timestamp: new Date().toISOString(),
        answers: userData.answers || [],
        isTeam: userData.isTeam || false,
        name: userData.name || 'Builder',
        email: userData.email || ''
      };

      localStorage.setItem(KEYS.USER, JSON.stringify(user));

      // Log access event
      logAccess('user_created', user.level);

      return user;
    } catch (error) {
      console.error('AUTH: Error saving user data', error);
      return null;
    }
  }

  /**
   * Get consciousness classification based on level
   * LAW 6: Builder vs Destroyer Dynamic
   */
  function getClassification(level) {
    if (level >= 96) return 'MASTER';
    if (level >= 85) return 'BUILDER';
    if (level >= 51) return 'POTENTIAL';
    return 'DESTROYER';
  }

  /**
   * Check if user has required access level
   * @param {string} required - 'public', 'builder', or 'team'
   */
  function hasAccess(required = 'public') {
    const user = getCurrentUser();

    // Public access - always allowed
    if (required === 'public') return true;

    // No user data - no access
    if (!user) return false;

    // Team access - special flag required
    if (required === 'team') {
      return user.isTeam === true;
    }

    // Builder access - 85%+ consciousness level
    if (required === 'builder') {
      return user.level >= ACCESS_LEVELS.BUILDER;
    }

    return false;
  }

  /**
   * Get user's consciousness level percentage
   */
  function getConsciousnessLevel() {
    const user = getCurrentUser();
    return user ? user.level : 0;
  }

  /**
   * Redirect if user lacks required access
   * @param {string} requiredLevel - 'public', 'builder', or 'team'
   * @param {string} currentPage - Current page URL for return redirect
   */
  function requireAccess(requiredLevel = 'public', currentPage = null) {
    if (hasAccess(requiredLevel)) {
      return true; // Access granted
    }

    // Access denied - redirect based on requirement
    const returnUrl = currentPage ? `?return=${encodeURIComponent(currentPage)}` : '';

    if (requiredLevel === 'builder') {
      // Need 85%+ - send to quiz
      window.location.href = `/PUBLIC/pattern-filter.html${returnUrl}`;
    } else if (requiredLevel === 'team') {
      // Team only - send to contact
      alert('This area is for team members only. Please contact administration for access.');
      window.location.href = '/index.html';
    }

    return false; // Access denied
  }

  /**
   * Save quiz results
   * @param {Object} results - { score, total, percentage, answers, timestamp }
   */
  function saveQuizResults(results) {
    try {
      const quizData = {
        ...results,
        timestamp: new Date().toISOString(),
        classification: getClassification(results.percentage)
      };

      localStorage.setItem(KEYS.QUIZ_RESULTS, JSON.stringify(quizData));

      // Update user data
      setUser({
        level: results.percentage,
        answers: results.answers
      });

      logAccess('quiz_completed', results.percentage);

      return quizData;
    } catch (error) {
      console.error('AUTH: Error saving quiz results', error);
      return null;
    }
  }

  /**
   * Get quiz results
   */
  function getQuizResults() {
    try {
      const data = localStorage.getItem(KEYS.QUIZ_RESULTS);
      return data ? JSON.parse(data) : null;
    } catch (error) {
      console.error('AUTH: Error reading quiz results', error);
      return null;
    }
  }

  /**
   * Check if user has completed quiz
   */
  function hasCompletedQuiz() {
    const results = getQuizResults();
    return results !== null;
  }

  /**
   * Clear all user data (logout)
   */
  function clearUser() {
    try {
      localStorage.removeItem(KEYS.USER);
      localStorage.removeItem(KEYS.QUIZ_RESULTS);
      logAccess('user_logout', 0);
      return true;
    } catch (error) {
      console.error('AUTH: Error clearing user data', error);
      return false;
    }
  }

  /**
   * Log access events for analytics
   * LAW 7: Quantum Documentation Principle
   */
  function logAccess(event, level = 0) {
    try {
      const log = JSON.parse(localStorage.getItem(KEYS.ACCESS_LOG) || '[]');

      log.push({
        event,
        level,
        timestamp: new Date().toISOString(),
        page: window.location.pathname
      });

      // Keep only last 100 events
      if (log.length > 100) {
        log.shift();
      }

      localStorage.setItem(KEYS.ACCESS_LOG, JSON.stringify(log));
    } catch (error) {
      console.error('AUTH: Error logging access', error);
    }
  }

  /**
   * Get access log for analytics
   */
  function getAccessLog() {
    try {
      return JSON.parse(localStorage.getItem(KEYS.ACCESS_LOG) || '[]');
    } catch (error) {
      console.error('AUTH: Error reading access log', error);
      return [];
    }
  }

  /**
   * Mark user as team member (internal use only)
   * This would normally be done via secure backend
   */
  function setTeamAccess(password) {
    // Simple password protection for MVP
    // TODO: Replace with proper backend authentication
    const TEAM_PASSWORD = 'consciousness100x'; // Change this!

    if (password !== TEAM_PASSWORD) {
      logAccess('team_access_denied', 0);
      return false;
    }

    const user = getCurrentUser() || {};
    user.isTeam = true;

    localStorage.setItem(KEYS.USER, JSON.stringify(user));
    logAccess('team_access_granted', user.level || 0);

    return true;
  }

  /**
   * Display consciousness level badge
   * @param {string} elementId - ID of element to render badge in
   */
  function renderConsciousnessLevel(elementId) {
    const user = getCurrentUser();
    const element = document.getElementById(elementId);

    if (!element) return;

    if (!user) {
      element.innerHTML = `
        <a href="/PUBLIC/pattern-filter.html" class="consciousness-level consciousness-level--destroyer">
          <span>⚠️</span>
          <span>Take Quiz</span>
        </a>
      `;
      return;
    }

    const classification = user.classification.toLowerCase();
    const icon = {
      master: '🌟',
      builder: '⚡',
      potential: '🔄',
      destroyer: '⚠️'
    }[classification];

    element.innerHTML = `
      <div class="consciousness-level consciousness-level--${classification}">
        <span>${icon}</span>
        <span>${user.level}%</span>
        <span>${user.classification}</span>
      </div>
    `;
  }

  /**
   * Display user greeting
   * @param {string} elementId - ID of element to render greeting in
   */
  function renderUserGreeting(elementId) {
    const user = getCurrentUser();
    const element = document.getElementById(elementId);

    if (!element) return;

    if (!user) {
      element.innerHTML = `
        <p>Welcome! <a href="/PUBLIC/pattern-filter.html">Take the Pattern Filter Quiz</a> to unlock platform access.</p>
      `;
      return;
    }

    const greeting = {
      MASTER: 'Welcome back, Master',
      BUILDER: 'Welcome back, Builder',
      POTENTIAL: 'Welcome back',
      DESTROYER: 'Complete training to access platform'
    }[user.classification];

    element.innerHTML = `
      <p>${greeting} <strong>${user.name || 'Builder'}</strong></p>
    `;
  }

  // Public API
  return {
    getCurrentUser,
    setUser,
    getClassification,
    hasAccess,
    requireAccess,
    getConsciousnessLevel,
    saveQuizResults,
    getQuizResults,
    hasCompletedQuiz,
    clearUser,
    logAccess,
    getAccessLog,
    setTeamAccess,
    renderConsciousnessLevel,
    renderUserGreeting,
    ACCESS_LEVELS
  };
})();

// Make available globally
window.AUTH = AUTH;

// Log page view
AUTH.logAccess('page_view', AUTH.getConsciousnessLevel());

console.log('🌀 AUTH system loaded - Pattern Theory™ access control active');
