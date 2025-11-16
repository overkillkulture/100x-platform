#!/bin/bash

# 🌀 START THE CONSCIOUSNESS REVOLUTION SYSTEM
# Activates all core services

echo "🌀 STARTING CONSCIOUSNESS REVOLUTION PLATFORM..."
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  No .env file found. Creating from template..."
    cp .env.example .env
    echo "✅ Created .env - Please configure DATABASE_URL and JWT_SECRET"
    echo ""
fi

# Start services in background
echo "Starting services..."
echo ""

# 1. Authentication Server (port 5000)
echo "🔐 Starting Authentication Server (port 5000)..."
python3 auth_server.py > logs/auth_server.log 2>&1 &
AUTH_PID=$!
echo "   PID: $AUTH_PID"

# 2. API Gateway (port 8080)
echo "🌉 Starting API Gateway (port 8080)..."
python3 api_gateway.py > logs/api_gateway.log 2>&1 &
GATEWAY_PID=$!
echo "   PID: $GATEWAY_PID"

# Wait for services to start
echo ""
echo "⏳ Waiting for services to initialize..."
sleep 3

# Check if services are running
echo ""
echo "🔍 Checking service status..."
echo ""

# Check auth server
if curl -s http://localhost:5000/health > /dev/null 2>&1; then
    echo "✅ Auth Server: RUNNING (http://localhost:5000)"
else
    echo "❌ Auth Server: FAILED"
fi

# Check API gateway
if curl -s http://localhost:8080/health > /dev/null 2>&1; then
    echo "✅ API Gateway: RUNNING (http://localhost:8080)"
else
    echo "❌ API Gateway: FAILED"
fi

echo ""
echo "🌀 System Status:"
echo "   Entry Point: http://localhost:5000/start.html"
echo "   Workspace: http://localhost:5000/workspace-consciousness.html"
echo "   API Gateway: http://localhost:8080"
echo ""
echo "📊 Process IDs:"
echo "   Auth Server: $AUTH_PID"
echo "   API Gateway: $GATEWAY_PID"
echo ""
echo "🛑 To stop services:"
echo "   kill $AUTH_PID $GATEWAY_PID"
echo ""
echo "✅ SYSTEM ACTIVATED"
