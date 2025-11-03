/**
 * ARAYA_API
 * Returns user profile data
 */

export const handler = async (event, context) => {
  try {
    // Get user ID from path
    const path = event.path || '';
    const userId = path.split('/').pop();

    // Return user profile
    return {
      statusCode: 200,
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type',
      },
      body: JSON.stringify({
        user: {
          id: userId || 'unknown',
          name: 'Builder',
          role: 'Beta Tester',
          status: 'Active',
          permissions: ['dashboard', 'jarvis', 'analytics'],
          joined: new Date().toISOString()
        }
      })
    };
  } catch (error) {
    return {
      statusCode: 500,
      body: JSON.stringify({ error: error.message })
    };
  }
};
