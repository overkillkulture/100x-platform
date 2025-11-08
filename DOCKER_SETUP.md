# Docker Setup - Consciousness Revolution Platform

Deploy all 6 AI instances across containers with automated orchestration.

## Quick Start

```bash
# Build and start all 6 instances
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all instances
docker-compose down

# Rebuild after code changes
docker-compose up -d --build
```

## Architecture

- **6 AI Instances** (containers): instance-1 through instance-6
- **3 Virtual Computers**: A (instances 1-2), B (instances 3-4), C (instances 5-6)
- **Load Balancer**: Nginx distributing traffic across all instances
- **Shared Storage**: Synchronized .consciousness folder

## Services

| Instance | Computer | Role | API Port | Internal Port |
|----------|----------|------|----------|---------------|
| instance-1 | A | Coordinator | 5001 | 8001 |
| instance-2 | A | Worker | 5002 | 8002 |
| instance-3 | B | Worker | 5003 | 8003 |
| instance-4 | B | Worker | 5004 | 8004 |
| instance-5 | C | Coordinator | 5005 | 8005 |
| instance-6 | C | Worker | 5006 | 8006 |
| load-balancer | - | LB | 80, 443 | - |

## Endpoints

- **Load Balanced API**: http://localhost/api/
- **Dashboard**: http://localhost/
- **Health Check**: http://localhost/health
- **Nginx Status**: http://localhost/nginx-status

Direct instance access:
- Instance 1: http://localhost:5001/
- Instance 2: http://localhost:5002/
- Instance 3: http://localhost:5003/
- Instance 4: http://localhost:5004/
- Instance 5: http://localhost:5005/
- Instance 6: http://localhost:5006/

## Commands

### Start Services

```bash
# Start all instances
docker-compose up -d

# Start specific instance
docker-compose up -d instance-1

# Scale workers (if needed)
docker-compose up -d --scale instance-2=2
```

### Monitor

```bash
# View all logs
docker-compose logs -f

# View specific instance logs
docker-compose logs -f instance-1

# View resource usage
docker stats

# Check instance health
curl http://localhost/health
```

### Management

```bash
# Stop all instances
docker-compose down

# Stop and remove volumes
docker-compose down -v

# Restart specific instance
docker-compose restart instance-3

# Rebuild images
docker-compose build

# Pull latest images
docker-compose pull
```

### Debugging

```bash
# Access instance shell
docker exec -it consciousness-instance-1 /bin/bash

# Check instance logs
docker logs consciousness-instance-1

# Inspect instance
docker inspect consciousness-instance-1

# View network
docker network inspect 100x-platform_consciousness-network
```

## Environment Variables

Each instance receives:
- `INSTANCE_ID`: 1-6
- `COMPUTER_ID`: computer-a, computer-b, or computer-c
- `ROLE`: coordinator or worker

Custom variables:
```bash
# Edit docker-compose.yml
environment:
  - CUSTOM_VAR=value
```

## Networking

All instances are on the same network (`consciousness-network`) and can communicate:

```python
# Instance 1 can reach instance 2 at:
http://instance-2:5000/api/
```

## Volumes

- `./data`: Shared data directory
- `./.consciousness`: Coordination state shared across instances

## Load Balancing

Nginx configuration (`nginx.conf`):
- Round-robin distribution
- Weighted (coordinators have weight=2)
- WebSocket support
- Health checks
- Automatic failover

## Production Deployment

For production:

1. **Use environment file**:
```bash
# Create .env file
echo "ENVIRONMENT=production" > .env
docker-compose --env-file .env up -d
```

2. **Enable HTTPS**:
- Add SSL certificates to nginx.conf
- Map port 443

3. **Resource limits**:
```yaml
# In docker-compose.yml
services:
  instance-1:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 4G
```

4. **Persistent storage**:
```yaml
volumes:
  data:
    driver: local
    driver_opts:
      type: none
      device: /mnt/data
      o: bind
```

## Troubleshooting

**Containers won't start:**
```bash
docker-compose logs instance-1
docker-compose down
docker-compose up -d --force-recreate
```

**Port conflicts:**
```bash
# Check what's using the port
sudo lsof -i :5001

# Change ports in docker-compose.yml
ports:
  - "5011:5000"  # Use 5011 instead
```

**Network issues:**
```bash
# Recreate network
docker network rm 100x-platform_consciousness-network
docker-compose up -d
```

**Out of memory:**
```bash
# Clean up
docker system prune -a
docker volume prune
```

## Figure 8 Infinity Symbol Architecture

The 6 instances form a Figure 8 pattern:

```
  Computer A          Computer B          Computer C
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ Instance 1  │◄───┤ Instance 3  │    │ Instance 5  │
│(Coordinator)│    │             │◄───┤(Coordinator)│
└──────┬──────┘    └─────────────┘    └──────┬──────┘
       │                                      │
       │           ┌─────────────┐            │
       └──────────►│ Instance 2  │            │
                   │             │            │
                   └──────┬──────┘            │
                          │                   │
                          │  ┌─────────────┐  │
                          └─►│ Instance 4  ├──┘
                             │             │
                             └──────┬──────┘
                                    │
                             ┌──────▼──────┐
                             │ Instance 6  │
                             │             │
                             └─────────────┘
```

All instances synchronize through shared `.consciousness/` folder.

## Monitoring Dashboard

Access the dashboard at http://localhost/ to view:
- All 30 modules (25 original + 5 new)
- Real-time metrics
- Instance health
- Figure 8 visualization

🚀 **Ready to deploy the Consciousness Revolution across 6 instances!**
