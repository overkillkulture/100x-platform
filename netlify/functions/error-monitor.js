// 🚨 Error Monitoring System
// Catches all errors and sends instant alerts

const fs = require('fs');

const ERROR_LOG = '/tmp/error_log.jsonl';
const DESKTOP_ERROR_FILE = 'C:/Users/dwrek/Desktop/CRITICAL_ERRORS.json';

function logError(errorData) {
  const error = {
    timestamp: new Date().toISOString(),
    ...errorData,
    severity: calculateSeverity(errorData)
  };

  // Log to file
  try {
    fs.appendFileSync(ERROR_LOG, JSON.stringify(error) + '\n');
  } catch (e) {
    console.error('Failed to log error:', e);
  }

  // Update desktop alert file for critical errors
  if (error.severity === 'critical' || error.severity === 'high') {
    try {
      let errors = [];
      if (fs.existsSync(DESKTOP_ERROR_FILE)) {
        errors = JSON.parse(fs.readFileSync(DESKTOP_ERROR_FILE, 'utf8'));
      }

      errors.unshift(error);

      // Keep only last 100 errors
      if (errors.length > 100) {
        errors = errors.slice(0, 100);
      }

      fs.writeFileSync(DESKTOP_ERROR_FILE, JSON.stringify(errors, null, 2));
    } catch (e) {
      console.error('Desktop error log failed:', e);
    }
  }

  return error;
}

function calculateSeverity(errorData) {
  const { type, message, impact } = errorData;

  // Critical errors
  if (type === 'api_failure' && message.includes('all')) return 'critical';
  if (type === 'deployment_failure') return 'critical';
  if (type === 'database_error') return 'critical';
  if (impact === 'all_users') return 'critical';

  // High severity
  if (type === 'api_failure') return 'high';
  if (type === 'authentication_error') return 'high';
  if (impact === 'multiple_users') return 'high';

  // Medium severity
  if (type === 'rate_limit') return 'medium';
  if (type === 'timeout') return 'medium';

  // Low severity
  return 'low';
}

exports.handler = async (event, context) => {
  if (event.httpMethod === "OPTIONS") {
    return {
      statusCode: 200,
      headers: {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "Content-Type",
        "Access-Control-Allow-Methods": "POST, OPTIONS"
      },
      body: ""
    };
  }

  try {
    const body = JSON.parse(event.body);
    const {
      type,
      message,
      stack,
      context: errorContext,
      user_id,
      page,
      impact
    } = body;

    const errorData = {
      type: type || 'unknown',
      message: message || 'No message provided',
      stack: stack || null,
      context: errorContext || {},
      user_id: user_id || 'anonymous',
      page: page || 'unknown',
      impact: impact || 'single_user',
      ip: event.headers['x-forwarded-for'] || 'unknown',
      user_agent: event.headers['user-agent'] || 'unknown'
    };

    const logged = logError(errorData);

    // For critical errors, also send to notification system
    if (logged.severity === 'critical') {
      try {
        await fetch('https://conciousnessrevolution.io/.netlify/functions/instant-notifications', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            type: 'critical_error',
            data: logged
          })
        });
      } catch (e) {
        console.log('Notification failed:', e);
      }
    }

    return {
      statusCode: 200,
      headers: {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*"
      },
      body: JSON.stringify({
        success: true,
        error_id: logged.timestamp,
        severity: logged.severity
      })
    };

  } catch (error) {
    console.error('Error monitor failed:', error);
    return {
      statusCode: 500,
      headers: {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*"
      },
      body: JSON.stringify({
        error: error.message
      })
    };
  }
};
