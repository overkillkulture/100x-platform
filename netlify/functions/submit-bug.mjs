// Netlify function to submit bugs to GitHub Issues
export const handler = async (event, context) => {
  // Only allow POST
  if (event.httpMethod !== 'POST') {
    return {
      statusCode: 405,
      body: JSON.stringify({ error: 'Method not allowed' })
    };
  }

  try {
    const bugData = JSON.parse(event.body);

    // Create GitHub issue
    const response = await fetch(
      `https://api.github.com/repos/${process.env.GITHUB_REPO}/issues`,
      {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${process.env.GITHUB_TOKEN}`,
          'Accept': 'application/vnd.github.v3+json',
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          title: bugData.title || 'Untitled Bug',
          body: `**Description:**\n${bugData.description || 'No description provided'}\n\n**Reporter:** ${bugData.reporter || 'Anonymous'}\n\n**URL:** ${bugData.url || 'N/A'}\n\n**Submitted:** ${new Date().toISOString()}`
        })
      }
    );

    if (response.ok) {
      const issue = await response.json();
      return {
        statusCode: 200,
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*'
        },
        body: JSON.stringify({
          success: true,
          issueUrl: issue.html_url,
          issueNumber: issue.number
        })
      };
    } else {
      const error = await response.text();
      console.error('GitHub API error:', error);
      return {
        statusCode: 500,
        body: JSON.stringify({ error: 'Failed to create issue' })
      };
    }

  } catch (error) {
    console.error('Error:', error);
    return {
      statusCode: 500,
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*'
      },
      body: JSON.stringify({ error: error.message })
    };
  }
};
