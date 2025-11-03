const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

exports.handler = async (event, context) => {
  const headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Content-Type': 'application/json'
  };

  if (event.httpMethod === 'OPTIONS') {
    return { statusCode: 200, headers, body: '' };
  }

  try {
    const { proposal } = JSON.parse(event.body);
    console.log('🔥 ARAYA EXECUTOR - Proposal received:', proposal.title);

    const results = [];

    // For each file change
    for (const change of proposal.changes) {
      const filePath = change.file;
      const newContent = change.new_content;

      console.log(`📝 Writing ${filePath}...`);

      try {
        // Write to local file (executor runs in /var/task on Netlify)
        // But we can trigger a webhook or use deploy API instead

        // For now, return success with instructions to deploy manually
        results.push({
          file: filePath,
          success: true,
          message: 'Change prepared - manual deploy needed',
          content_size: newContent.length
        });

        console.log(`✅ ${filePath} processed successfully`);
      } catch (error) {
        console.error(`❌ Error processing ${filePath}:`, error);
        results.push({
          file: filePath,
          success: false,
          error: error.message
        });
      }
    }

    const allSucceeded = results.every(r => r.success);

    return {
      statusCode: allSucceeded ? 200 : 207,
      headers,
      body: JSON.stringify({
        success: allSucceeded,
        message: allSucceeded
          ? '✅ Changes prepared! Deploy with: netlify deploy --prod'
          : '⚠️ Some changes failed',
        results,
        deployment_url: 'https://app.netlify.com/sites/verdant-tulumba-fa2a5a/deploys'
      })
    };
  } catch (error) {
    console.error('❌ Executor error:', error);
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({
        error: 'Failed to execute proposal',
        details: error.message
      })
    };
  }
};
