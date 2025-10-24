// Netlify Function - Visitor Tracking
// Stores visitor data in simple JSON files

const fs = require('fs').promises;
const path = require('path');

exports.handler = async (event, context) => {
  // Handle CORS
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

  if (event.httpMethod !== "POST") {
    return {
      statusCode: 405,
      body: JSON.stringify({ error: "Method not allowed" })
    };
  }

  try {
    const data = JSON.parse(event.body);
    const now = new Date();

    // Create visitor log entry
    const logEntry = {
      timestamp: now.toISOString(),
      pin: data.pin || 'anonymous',
      name: data.name || 'Guest',
      page: data.page,
      action: data.action || 'pageview',
      userAgent: data.userAgent,
      referrer: data.referrer
    };

    // In Netlify Functions, we can't write to filesystem
    // So we'll use Netlify's built-in analytics
    // OR return the data to be logged client-side

    console.log('📊 Visitor tracked:', logEntry);

    return {
      statusCode: 200,
      headers: {
        "Access-Control-Allow-Origin": "*",
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        success: true,
        message: "Visitor tracked",
        timestamp: now.toISOString()
      })
    };

  } catch (error) {
    console.error('Tracking error:', error);
    return {
      statusCode: 500,
      body: JSON.stringify({ error: error.message })
    };
  }
};
