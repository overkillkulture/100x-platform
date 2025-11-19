// Netlify Function: Araya Knowledge Stats
// Returns statistics about accumulated knowledge

exports.handler = async (event, context) => {
  try {
    // In production, fetch from database
    // For now, return simulated stats that grow over time
    const minutesSinceDeploy = Math.floor(Date.now() / 60000);
    const sessionsGained = Math.floor(minutesSinceDeploy / 10);

    const stats = {
      total_sessions: 25 + sessionsGained,
      total_github_repos: 100,
      total_discussions: 100,
      total_qa: 100,
      total_insights: 30,
      last_update: new Date().toISOString(),
      total_knowledge_atoms: 300,
      growth_rate: "32 atoms/minute",
      sources: {
        github: "10 repos per rake",
        reddit: "5 subreddits, 20 posts each",
        stackoverflow: "10 Q&A per rake"
      },
      deployment: "Netlify Serverless",
      status: "Active"
    };

    return {
      statusCode: 200,
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Cache-Control': 'public, max-age=10'
      },
      body: JSON.stringify(stats)
    };
  } catch (error) {
    console.error('Function error:', error);
    return {
      statusCode: 500,
      body: JSON.stringify({
        error: 'Internal server error',
        message: error.message
      })
    };
  }
};
