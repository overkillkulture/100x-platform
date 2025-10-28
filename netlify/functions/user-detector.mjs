/**
 * USER_DETECTOR API
 * Returns workspace state and online users
 */

export const handler = async (event, context) => {
  try {
    // Return mock workspace state for now
    // Later can connect to real database
    return {
      statusCode: 200,
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type',
      },
      body: JSON.stringify({
        workspace: {
          status: 'active',
          online_users: 0,
          modules_active: [],
          recent_activity: []
        },
        timestamp: new Date().toISOString()
      })
    };
  } catch (error) {
    return {
      statusCode: 500,
      body: JSON.stringify({ error: error.message })
    };
  }
};
