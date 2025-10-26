/**
 * 🔥 ARAYA EXECUTION ENGINE 🔥
 * MORTAL KOMBAT FINISHER - Actually executes approved proposals
 */

const fetch = require('node-fetch');

exports.handler = async (event, context) => {
  // CORS headers
  const headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Content-Type': 'application/json'
  };

  // Handle preflight
  if (event.httpMethod === 'OPTIONS') {
    return { statusCode: 200, headers, body: '' };
  }

  if (event.httpMethod !== 'POST') {
    return {
      statusCode: 405,
      headers,
      body: JSON.stringify({ error: 'Method not allowed' })
    };
  }

  try {
    const { proposal } = JSON.parse(event.body);

    if (!proposal || !proposal.changes || proposal.changes.length === 0) {
      return {
        statusCode: 400,
        headers,
        body: JSON.stringify({ error: 'Invalid proposal - no changes specified' })
      };
    }

    // Get GitHub token from environment
    const GITHUB_TOKEN = process.env.GITHUB_TOKEN;
    const GITHUB_REPO = process.env.GITHUB_REPO || 'overkillkulture/consciousness-revolution';
    const GITHUB_BRANCH = process.env.GITHUB_BRANCH || 'master';

    if (!GITHUB_TOKEN) {
      console.log('⚠️ No GitHub token - would execute:', proposal);
      return {
        statusCode: 200,
        headers,
        body: JSON.stringify({
          success: true,
          message: '✅ Proposal approved! (GitHub integration pending - add GITHUB_TOKEN to Netlify env vars)',
          simulated: true,
          changes: proposal.changes
        })
      };
    }

    // Execute each change via GitHub API
    const results = [];

    for (const change of proposal.changes) {
      const filePath = change.file;
      const newContent = change.new_content;

      // GitHub API: Get current file to get SHA
      const getFileUrl = `https://api.github.com/repos/${GITHUB_REPO}/contents/${filePath}?ref=${GITHUB_BRANCH}`;

      const getResponse = await fetch(getFileUrl, {
        headers: {
          'Authorization': `token ${GITHUB_TOKEN}`,
          'Accept': 'application/vnd.github.v3+json',
          'User-Agent': 'ARAYA-Executor'
        }
      });

      let sha = null;
      if (getResponse.ok) {
        const fileData = await getResponse.json();
        sha = fileData.sha;
      }

      // GitHub API: Create or update file
      const updateFileUrl = `https://api.github.com/repos/${GITHUB_REPO}/contents/${filePath}`;

      const updatePayload = {
        message: `🤖 ARAYA Auto-Edit: ${proposal.description}\n\nRisk: ${proposal.risk_level || proposal.risk}\nApproved by: User via Platform Help Widget`,
        content: Buffer.from(newContent).toString('base64'),
        branch: GITHUB_BRANCH
      };

      if (sha) {
        updatePayload.sha = sha; // Update existing file
      }

      const updateResponse = await fetch(updateFileUrl, {
        method: 'PUT',
        headers: {
          'Authorization': `token ${GITHUB_TOKEN}`,
          'Accept': 'application/vnd.github.v3+json',
          'Content-Type': 'application/json',
          'User-Agent': 'ARAYA-Executor'
        },
        body: JSON.stringify(updatePayload)
      });

      const result = await updateResponse.json();

      results.push({
        file: filePath,
        success: updateResponse.ok,
        commit: result.commit?.html_url || null,
        error: updateResponse.ok ? null : result.message
      });
    }

    // Check if all succeeded
    const allSucceeded = results.every(r => r.success);

    return {
      statusCode: allSucceeded ? 200 : 207,
      headers,
      body: JSON.stringify({
        success: allSucceeded,
        message: allSucceeded
          ? '✅ Changes committed to GitHub! Netlify will auto-deploy in ~30 seconds.'
          : '⚠️ Some changes failed to commit',
        results,
        deployment_url: 'https://app.netlify.com/sites/verdant-tulumba-fa2a5a/deploys'
      })
    };

  } catch (error) {
    console.error('Error executing proposal:', error);
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
