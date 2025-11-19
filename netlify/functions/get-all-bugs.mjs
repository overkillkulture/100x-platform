// PROXY FOR GITHUB BUGS - Fixes CORS issue + Rate Limiting
export async function handler(event, context) {
    try {
        // Use GitHub token if available for higher rate limits
        const headers = {
            'Accept': 'application/vnd.github.v3+json',
            'User-Agent': 'Consciousness-Revolution-Bug-Monitor'
        };

        // Add auth if token available (5000 req/hr vs 60 req/hr)
        if (process.env.GITHUB_TOKEN) {
            headers['Authorization'] = `Bearer ${process.env.GITHUB_TOKEN}`;
        }

        const response = await fetch(
            'https://api.github.com/repos/overkillkulture/consciousness-bugs/issues?state=all&sort=created&direction=desc&per_page=50',
            { headers }
        );

        if (!response.ok) {
            throw new Error(`GitHub API error: ${response.status}`);
        }

        const bugs = await response.json();

        return {
            statusCode: 200,
            headers: {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Cache-Control': 'no-cache'
            },
            body: JSON.stringify(bugs)
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
                error: 'Failed to fetch bugs',
                message: error.message
            })
        };
    }
}
