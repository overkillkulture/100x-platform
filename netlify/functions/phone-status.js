// 📱 Phone Status Endpoint
// Returns status of phone/SMS automation system

exports.handler = async (event, context) => {
  // Handle CORS preflight
  if (event.httpMethod === "OPTIONS") {
    return {
      statusCode: 200,
      headers: {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "Content-Type, ngrok-skip-browser-warning",
        "Access-Control-Allow-Methods": "GET, POST, OPTIONS"
      },
      body: ""
    };
  }

  try {
    // Check if this is a GET request for status
    if (event.httpMethod === "GET") {
      const status = {
        service: "phone-automation",
        status: "operational",
        timestamp: new Date().toISOString(),
        features: {
          sms_receiving: "active",
          call_forwarding: "active",
          verification_code_extraction: "active",
          twilio_integration: "ready"
        },
        endpoints: {
          status: "/phone/status",
          receive_sms: "/phone/sms/receive",
          receive_call: "/phone/call/receive",
          get_latest_code: "/phone/code/latest"
        },
        phone_number: process.env.TWILIO_PHONE_NUMBER || "not_configured",
        provider: "twilio",
        version: "1.0.0"
      };

      return {
        statusCode: 200,
        headers: {
          "Content-Type": "application/json",
          "Access-Control-Allow-Origin": "*"
        },
        body: JSON.stringify(status, null, 2)
      };
    }

    // If POST, could be a webhook or status update
    if (event.httpMethod === "POST") {
      const body = event.body ? JSON.parse(event.body) : {};

      return {
        statusCode: 200,
        headers: {
          "Content-Type": "application/json",
          "Access-Control-Allow-Origin": "*"
        },
        body: JSON.stringify({
          success: true,
          message: "Phone status endpoint received POST request",
          received: body
        })
      };
    }

    // Method not allowed
    return {
      statusCode: 405,
      headers: {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*"
      },
      body: JSON.stringify({
        error: "Method not allowed",
        allowed_methods: ["GET", "POST", "OPTIONS"]
      })
    };

  } catch (error) {
    console.error('Phone status endpoint error:', error);
    return {
      statusCode: 500,
      headers: {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*"
      },
      body: JSON.stringify({
        error: error.message,
        service: "phone-status"
      })
    };
  }
};
