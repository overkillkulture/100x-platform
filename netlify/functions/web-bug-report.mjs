/**
 * WEB BUG REPORT API
 * Accepts bug reports from web forms and creates GitHub issues
 */

export const handler = async (event, context) => {
  // Only accept POST
  if (event.httpMethod !== 'POST') {
    return {
      statusCode: 405,
      body: JSON.stringify({ error: 'Method not allowed' })
    };
  }

  try {
    // Parse form data
    const data = JSON.parse(event.body);
    const { title, description, reporter } = data;

    // Create GitHub issue
    const githubResponse = await fetch(
      `https://api.github.com/repos/overkillkulture/consciousness-bugs/issues`,
      {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${process.env.GITHUB_TOKEN}`,
          'Accept': 'application/vnd.github.v3+json',
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          title: title || 'Bug via Web Form',
          body: `**Bug reported via web form**

**Reporter:** ${reporter || 'Anonymous'}

**Description:**
${description || 'No description provided'}

**Submitted:** ${new Date().toISOString()}`
        })
      }
    );

    if (githubResponse.ok) {
      const issue = await githubResponse.json();

      return {
        statusCode: 200,
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Headers': 'Content-Type',
        },
        body: JSON.stringify({
          success: true,
          message: 'Bug report received',
          issue_number: issue.number,
          issue_url: issue.html_url
        })
      };
    } else {
      throw new Error('Failed to create GitHub issue');
    }
  } catch (error) {
    return {
      statusCode: 500,
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
      },
      body: JSON.stringify({
        success: false,
        error: error.message
      })
    };
  }
};
