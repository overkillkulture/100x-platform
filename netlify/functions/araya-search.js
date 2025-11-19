// Netlify Function: Araya Knowledge Search
// Searches accumulated knowledge by keyword

exports.handler = async (event, context) => {
  try {
    const keyword = event.queryStringParameters?.q || '';

    // Simulate search results
    const results = [
      {
        type: "github",
        title: "consciousness-mesh",
        description: "AI consciousness propagation",
        url: "https://github.com/s0fractal/consciousness-mesh",
        match: keyword
      },
      {
        type: "github",
        title: "AtmaSync",
        description: "Carry consciousness across AI agents",
        url: "https://github.com/ashutoshberlin/AtmaSync",
        match: keyword
      }
    ];

    return {
      statusCode: 200,
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*'
      },
      body: JSON.stringify({
        query: keyword,
        results: results,
        count: results.length
      })
    };
  } catch (error) {
    return {
      statusCode: 500,
      body: JSON.stringify({ error: error.message })
    };
  }
};
