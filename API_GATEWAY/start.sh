#!/bin/bash

# ===========================
# 100X PLATFORM API GATEWAY
# STARTUP SCRIPT
# ===========================

set -e

echo "================================"
echo "100X Platform API Gateway"
echo "Starting up..."
echo "================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if .env file exists
if [ ! -f .env ]; then
    echo -e "${RED}ERROR: .env file not found!${NC}"
    echo "Copying .env.example to .env..."
    cp .env.example .env
    echo -e "${YELLOW}WARNING: Please edit .env file with your configuration before continuing.${NC}"
    exit 1
fi

echo -e "${GREEN}✓ .env file found${NC}"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo -e "${GREEN}✓ Virtual environment activated${NC}"

# Install/update dependencies
echo "Installing dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt
echo -e "${GREEN}✓ Dependencies installed${NC}"

# Check Redis connection
echo "Checking Redis connection..."
if command -v redis-cli &> /dev/null; then
    if redis-cli ping &> /dev/null; then
        echo -e "${GREEN}✓ Redis is running${NC}"
    else
        echo -e "${YELLOW}WARNING: Redis is not running. Starting Redis...${NC}"
        if command -v redis-server &> /dev/null; then
            redis-server --daemonize yes
            sleep 2
            echo -e "${GREEN}✓ Redis started${NC}"
        else
            echo -e "${RED}ERROR: Redis is not installed. Please install Redis.${NC}"
            exit 1
        fi
    fi
else
    echo -e "${YELLOW}WARNING: redis-cli not found. Skipping Redis check.${NC}"
fi

# Check PostgreSQL connection (optional)
echo "Checking database configuration..."
if command -v psql &> /dev/null; then
    # Extract database URL from .env
    DB_URL=$(grep DATABASE_URL .env | cut -d '=' -f2)
    if [ ! -z "$DB_URL" ]; then
        echo -e "${GREEN}✓ Database configured${NC}"
    else
        echo -e "${YELLOW}WARNING: DATABASE_URL not set in .env${NC}"
    fi
else
    echo -e "${YELLOW}WARNING: psql not found. Skipping database check.${NC}"
fi

# Print configuration summary
echo ""
echo "================================"
echo "Configuration Summary:"
echo "================================"
python -c "from config import print_config_summary; print_config_summary()"

# Start the server
echo ""
echo "================================"
echo "Starting API Gateway Server..."
echo "================================"
echo ""
echo -e "${GREEN}Server will be available at:${NC}"
echo "  - API: http://localhost:8000"
echo "  - Docs: http://localhost:8000/api/docs"
echo "  - ReDoc: http://localhost:8000/api/redoc"
echo ""
echo -e "${YELLOW}Press Ctrl+C to stop the server${NC}"
echo ""

# Start uvicorn with appropriate settings
if [ "$1" == "production" ]; then
    echo "Starting in PRODUCTION mode..."
    uvicorn gateway:app --host 0.0.0.0 --port 8000 --workers 4
else
    echo "Starting in DEVELOPMENT mode..."
    uvicorn gateway:app --host 0.0.0.0 --port 8000 --reload
fi
