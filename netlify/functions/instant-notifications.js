// 🔔 Instant Notification System
// Email opens, site visits, profile creation - all in real-time

const fs = require('fs');
const path = require('path');

// Notification channels (we'll expand this)
const NOTIFICATION_LOG = '/tmp/instant_notifications.jsonl';
const COMMANDER_ALERT_FILE = '/tmp/commander_alerts.json';

// Desktop notification file (Commander can monitor this)
const DESKTOP_ALERT = 'C:/Users/dwrek/Desktop/LIVE_ACTIVITY_ALERT.json';

function sendNotification(type, data) {
  const notification = {
    timestamp: new Date().toISOString(),
    type: type,
    data: data,
    read: false
  };

  // Log to file
  try {
    fs.appendFileSync(NOTIFICATION_LOG, JSON.stringify(notification) + '\n');
  } catch (e) {
    // Fallback if /tmp not available
  }

  // Update desktop alert file
  try {
    let alerts = [];
    if (fs.existsSync(DESKTOP_ALERT)) {
      alerts = JSON.parse(fs.readFileSync(DESKTOP_ALERT, 'utf8'));
    }

    alerts.unshift(notification); // Add to front

    // Keep only last 50 alerts
    if (alerts.length > 50) {
      alerts = alerts.slice(0, 50);
    }

    fs.writeFileSync(DESKTOP_ALERT, JSON.stringify(alerts, null, 2));
  } catch (e) {
    console.error('Desktop alert failed:', e);
  }

  return notification;
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
    const { type, data } = body;

    let notification;

    switch (type) {
      case 'email_open':
        notification = sendNotification('email_open', {
          recipient: data.recipient || 'unknown',
          email_subject: data.subject || 'Beta Invite',
          opened_at: new Date().toISOString(),
          ip: event.headers['x-forwarded-for'] || 'unknown',
          user_agent: event.headers['user-agent'] || 'unknown'
        });
        break;

      case 'site_visit':
        notification = sendNotification('site_visit', {
          page: data.page || 'unknown',
          referrer: data.referrer || 'direct',
          ip: event.headers['x-forwarded-for'] || 'unknown',
          user_agent: event.headers['user-agent'] || 'unknown',
          session_id: data.session_id || null
        });
        break;

      case 'profile_created':
        notification = sendNotification('profile_created', {
          user_id: data.user_id || 'unknown',
          email: data.email || null,
          username: data.username || null,
          ip: event.headers['x-forwarded-for'] || 'unknown'
        });
        break;

      case 'login':
        notification = sendNotification('login', {
          user_id: data.user_id || 'unknown',
          username: data.username || null,
          ip: event.headers['x-forwarded-for'] || 'unknown'
        });
        break;

      default:
        return {
          statusCode: 400,
          body: JSON.stringify({ error: 'Unknown notification type' })
        };
    }

    return {
      statusCode: 200,
      headers: {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*"
      },
      body: JSON.stringify({
        success: true,
        notification: notification
      })
    };

  } catch (error) {
    console.error('Notification error:', error);
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
