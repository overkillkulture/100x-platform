// Netlify serverless function to receive bug reports and SAVE TO AIRTABLE

const AIRTABLE_TOKEN = "pat8DtOnZ1crQT56g.a83c21fa77ead56a661353b0cd0b286816ca14502ce717c8b247c0c52a326757";
const BASE_ID = "app7F75X1uny6jPfd";
const TABLE_NAME = "Documents"; // Using Documents table with Category="Bug Report"

export const handler = async (event, context) => {
  // Only allow POST requests
  if (event.httpMethod !== 'POST') {
    return {
      statusCode: 405,
      body: JSON.stringify({ error: 'Method not allowed' })
    };
  }

  try {
    // Parse the bug report data
    const bugData = JSON.parse(event.body);

    // Add metadata
    const bugReport = {
      ...bugData,
      received_at: new Date().toISOString(),
      ip: event.headers['x-forwarded-for'] || 'unknown',
      userAgent: bugData.userAgent || event.headers['user-agent'] || 'unknown'
    };

    console.log('🐛 BUG REPORT RECEIVED - SAVING TO AIRTABLE 🐛');
    console.log('Title:', bugReport.title || 'N/A');
    console.log('Description:', bugReport.description || 'N/A');
    console.log('Reporter:', bugReport.reporter || 'Anonymous');

    // SAVE TO AIRTABLE (using Documents table schema)
    // Note: Full bug details stored in Filename and Path fields
    const bugDetails = `REPORTER: ${bugReport.reporter || 'Anonymous'} | DESC: ${bugReport.description || 'No description'} | AGENT: ${bugReport.userAgent}`;

    const airtableUrl = `https://api.airtable.com/v0/${BASE_ID}/${TABLE_NAME}`;
    const airtableData = {
      fields: {
        "Filename": `BUG: ${bugReport.title || 'Untitled'}`,
        "Path": bugDetails.substring(0, 500), // Store bug details in Path field (max 500 chars)
        "Extension": "bug",
        "Category": "bug", // Simple category value
        "Size (KB)": bugReport.description ? bugReport.description.length / 1024 : 0,
        "Created": bugReport.timestamp || bugReport.received_at,
        "Modified": bugReport.received_at,
        "Indexed": new Date().toISOString()
      }
    };

    const airtableResponse = await fetch(airtableUrl, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${AIRTABLE_TOKEN}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(airtableData)
    });

    if (!airtableResponse.ok) {
      const errorText = await airtableResponse.text();
      console.error('Airtable error:', errorText);
      throw new Error(`Airtable failed: ${errorText}`);
    }

    const airtableResult = await airtableResponse.json();
    console.log('✅ SAVED TO AIRTABLE:', airtableResult.id);

    // Return success
    return {
      statusCode: 200,
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type'
      },
      body: JSON.stringify({
        success: true,
        message: 'Bug report saved to Airtable',
        id: airtableResult.id
      })
    };

  } catch (error) {
    console.error('Error processing bug report:', error);

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
