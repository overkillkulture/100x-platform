// Netlify function to receive console logs from browser
import fs from 'fs/promises';
import path from 'path';

export async function handler(event, context) {
    // Only allow POST
    if (event.httpMethod !== 'POST') {
        return {
            statusCode: 405,
            body: JSON.stringify({ error: 'Method not allowed' })
        };
    }

    try {
        const log = JSON.parse(event.body);

        // Append to log file
        const logFile = '/tmp/console_logs.jsonl';
        const logLine = JSON.stringify(log) + '\n';

        await fs.appendFile(logFile, logLine);

        return {
            statusCode: 200,
            body: JSON.stringify({ success: true })
        };
    } catch (error) {
        return {
            statusCode: 500,
            body: JSON.stringify({ error: error.message })
        };
    }
}
