#!/bin/bash

# 🚀 ONE-COMMAND DEPLOY TO RAILWAY
# This will deploy the conversational system so you can access from your iPhone

echo "🚀 DEPLOYING CONVERSATIONAL SYSTEM TO RAILWAY..."
echo ""

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "📦 Installing Railway CLI..."
    npm install -g @railway/cli
fi

# Login to Railway
echo "🔐 Logging into Railway..."
railway login

# Initialize project
echo "🎯 Initializing Railway project..."
railway init

# Deploy
echo "🚀 Deploying..."
railway up

echo ""
echo "✅ DEPLOYMENT COMPLETE!"
echo ""
echo "📱 Your iPhone can now access the system at:"
railway domain
echo ""
echo "💡 The URL will be something like:"
echo "   https://your-app-production.up.railway.app"
echo ""
echo "🌀 Test it:"
echo "   Open Safari on your iPhone"
echo "   Go to the URL above"
echo "   Ask: 'What is Cyclotron?'"
echo ""
