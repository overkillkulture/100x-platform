/**
 * Netlify Function: Get All Bugs from GitHub
 * Fetches issues from consciousness-bugs repo with caching to avoid rate limits
 */

// Simple in-memory cache (persists during function lifetime)
let cache = {
  data: null,
  timestamp: 0,
  ttl: 30000  // 30 seconds cache
};

exports.handler = async (event, context) => {
  // Enable CORS
  const headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Allow-Methods': 'GET, OPTIONS',
    'Content-Type': 'application/json'
  };

  // Handle OPTIONS request
  if (event.httpMethod === 'OPTIONS') {
    return { statusCode: 200, headers, body: '' };
  }

  // Check cache first
  const now = Date.now();
  if (cache.data && (now - cache.timestamp) < cache.ttl) {
    console.log('Returning cached data');
    return {
      statusCode: 200,
      headers,
      body: JSON.stringify(cache.data)
    };
  }

  try {
    // Fetch bugs from GitHub with authentication to avoid rate limits
    const fetchHeaders = {
      'Accept': 'application/vnd.github.v3+json',
      'User-Agent': 'Consciousness-Revolution-Bug-Monitor'
    };

    // Use GitHub token for 5000/hr rate limit (instead of 60/hr)
    if (process.env.GITHUB_TOKEN) {
      fetchHeaders['Authorization'] = `Bearer ${process.env.GITHUB_TOKEN}`;
    }

    const response = await fetch('https://api.github.com/repos/overkillkulture/consciousness-bugs/issues?state=all&per_page=100', {
      headers: fetchHeaders
    });

    if (!response.ok) {
      throw new Error(`GitHub API returned ${response.status}`);
    }

    const bugs = await response.json();

    // Filter to only include issues labeled as bugs or all issues
    const allBugs = bugs.map(bug => ({
      number: bug.number,
      title: bug.title,
      body: bug.body,
      state: bug.state,
      created_at: bug.created_at,
      updated_at: bug.updated_at,
      html_url: bug.html_url,
      user: {
        login: bug.user.login,
        avatar_url: bug.user.avatar_url
      },
      labels: bug.labels.map(l => l.name)
    }));

    // Update cache
    cache.data = allBugs;
    cache.timestamp = Date.now();
    console.log(`Cached ${allBugs.length} bugs`);

    return {
      statusCode: 200,
      headers,
      body: JSON.stringify(allBugs)
    };

  } catch (error) {
    console.error('Error fetching bugs:', error);
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({
        error: 'Failed to fetch bugs',
        message: error.message
      })
    };
  }
};
