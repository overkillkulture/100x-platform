# Consciousness Revolution Platform - Docker Image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements (if we had them)
# For now, we'll install common dependencies
RUN pip install --no-cache-dir \
    numpy \
    flask \
    flask-cors

# Copy application code
COPY . /app/

# Create necessary directories
RUN mkdir -p /app/.consciousness \
    /app/logs \
    /app/data

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    INSTANCE_ID=1 \
    COMPUTER_ID=computer-a

# Expose ports
EXPOSE 5000 8080 8001 8002 8003 8004 8005 8006

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import sys; sys.exit(0)"

# Default command
CMD ["python", "API_SERVER.py"]
