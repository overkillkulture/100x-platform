// Netlify serverless function to retrieve bug reports
import { getStore } from '@netlify/blobs';

export const handler = async (event, context) => {
  try {
    const bugStore = getStore('bug-reports');

    // List all bugs
    const bugList = await bugStore.list();
    const bugs = [];

    // Fetch each bug's data
    for await (const blob of bugList.blobs) {
      const bugData = await bugStore.get(blob.key);
      if (bugData) {
        try {
          const parsedBug = JSON.parse(bugData);
          bugs.push({
            id: blob.key,
            ...parsedBug,
            metadata: blob.metadata
          });
        } catch (e) {
          console.error(`Failed to parse bug ${blob.key}:`, e);
        }
      }
    }

    // Sort by timestamp (newest first)
    bugs.sort((a, b) => {
      const timeA = new Date(a.timestamp || a.received_at || 0);
      const timeB = new Date(b.timestamp || b.received_at || 0);
      return timeB - timeA;
    });

    return {
      statusCode: 200,
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type'
      },
      body: JSON.stringify({
        success: true,
        count: bugs.length,
        bugs: bugs
      })
    };

  } catch (error) {
    console.error('Error fetching bugs:', error);

    return {
      statusCode: 500,
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*'
      },
      body: JSON.stringify({
        success: false,
        error: error.message
      })
    };
  }
};
