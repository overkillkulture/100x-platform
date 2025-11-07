/**
 * Netlify Function: Web Bug Report
 * Receives bug reports from SIMPLE_BUG_REPORTER.js and creates GitHub issues
 */

const https = require('https');

exports.handler = async (event, context) => {
  // Enable CORS
  const headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Content-Type': 'application/json'
  };

  // Handle OPTIONS request
  if (event.httpMethod === 'OPTIONS') {
    return { statusCode: 200, headers, body: '' };
  }

  // Only allow POST
  if (event.httpMethod !== 'POST') {
    return {
      statusCode: 405,
      headers,
      body: JSON.stringify({ error: 'Method not allowed' })
    };
  }

  try {
    const data = JSON.parse(event.body);
    const { description, reporter, page, pageName } = data;

    if (!description) {
      return {
        statusCode: 400,
        headers,
        body: JSON.stringify({ error: 'Description is required' })
      };
    }

    // Create GitHub issue if token is available
    if (process.env.GITHUB_TOKEN) {
      const issueBody = `**Bug reported via web form**

**Reporter:** ${reporter || 'Anonymous'}

**Page:** ${pageName || 'Unknown'}
**URL:** ${page || 'Not provided'}

**Description:**
${description}

**Submitted:** ${new Date().toISOString()}`;

      const issueData = JSON.stringify({
        title: description.substring(0, 100) + (description.length > 100 ? '...' : ''),
        body: issueBody,
        labels: ['bug', 'web-reported']
      });

      // Create GitHub issue using native https module
      const githubOptions = {
        hostname: 'api.github.com',
        port: 443,
        path: '/repos/overkillkulture/consciousness-bugs/issues',
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${process.env.GITHUB_TOKEN}`,
          'Accept': 'application/vnd.github.v3+json',
          'User-Agent': 'Consciousness-Revolution-Bug-Reporter',
          'Content-Type': 'application/json',
          'Content-Length': Buffer.byteLength(issueData)
        }
      };

      const createIssue = () => new Promise((resolve, reject) => {
        const req = https.request(githubOptions, (res) => {
          let body = '';
          res.on('data', (chunk) => body += chunk);
          res.on('end', () => {
            if (res.statusCode === 201) {
              resolve(JSON.parse(body));
            } else {
              reject(new Error(`GitHub API returned ${res.statusCode}: ${body}`));
            }
          });
        });

        req.on('error', reject);
        req.write(issueData);
        req.end();
      });

      try {
        const issue = await createIssue();
        console.log(`Created GitHub issue #${issue.number}`);

        return {
          statusCode: 200,
          headers,
          body: JSON.stringify({
            success: true,
            message: 'Bug reported successfully',
            issueNumber: issue.number,
            issueUrl: issue.html_url
          })
        };
      } catch (githubError) {
        console.error('GitHub API error:', githubError.message);
        // Continue to return success even if GitHub fails
        // Bug is still logged in Netlify logs
      }
    }

    // Fallback: Log to console (captured by Netlify)
    console.log('🐛 Bug Report:', {
      description,
      reporter,
      page,
      pageName,
      timestamp: new Date().toISOString()
    });

    return {
      statusCode: 200,
      headers,
      body: JSON.stringify({
        success: true,
        message: 'Bug report received and logged'
      })
    };

  } catch (error) {
    console.error('Error processing bug report:', error);
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({
        error: 'Failed to process bug report',
        message: error.message
      })
    };
  }
};
