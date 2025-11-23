# 📊 Analytics Dashboard Backend

Backend API for the 100X Platform Analytics Dashboard - provides unified access to all analytics systems.

## Features

- **Business Phase Tracking**: Current phase and transition predictions
- **Metrics Management**: Business metrics (revenue, users, engagement, conversion)
- **Data Vacuum Integration**: Content extraction statistics
- **Visitor Analytics**: Daily visitor stats, pageviews, bounce rates
- **Event Tracking**: Page views and button clicks
- **Auto-Demo Data**: Generates realistic demo data on first run
- **JSON Storage**: Simple file-based storage for development

## Quick Start

### Option 1: Windows Launcher (Easiest)

```bash
# Double-click START_ANALYTICS_DASHBOARD.bat
# Or run from command line:
START_ANALYTICS_DASHBOARD.bat
```

### Option 2: Manual Setup

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate.bat
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run server
python app.py
```

Server will start on `http://localhost:5100`

## API Endpoints

### Health Check
```
GET /api/health
```

Returns server status and all system states.

**Response:**
```json
{
  "status": "operational",
  "service": "analytics-dashboard",
  "timestamp": "2025-11-22T07:30:00.000Z",
  "systems": {
    "business_metrics": "ok",
    "phase_prediction": "ok",
    "vacuum": "ok",
    "analytics": "ok"
  }
}
```

### Master Dashboard
```
GET /api/dashboard
```

Get all metrics in one unified response.

**Response:**
```json
{
  "timestamp": "2025-11-22T07:30:00.000Z",
  "business_metrics": {
    "timestamp": "2025-11-22T07:00:00.000Z",
    "revenue": 0,
    "users": 0,
    "engagement_score": 0,
    "conversion_rate": 0
  },
  "phase_prediction": {
    "prediction": {
      "current_phase": "Phase 1: Platform Development",
      "next_phase": "Phase 2: Beta Testing",
      "transition_probability": 67.5,
      "estimated_days": 14
    }
  },
  "vacuum_stats": {
    "files_scanned": 1247,
    "total_data_points": 8934,
    "scan_time": "2025-11-22T07:00:00.000Z"
  },
  "analytics": {
    "page_views": 0,
    "button_clicks": 0,
    "unique_visitors": 0
  }
}
```

### Business Phase
```
GET /api/business-phase
```

Get current business phase and predictions.

**Response:**
```json
{
  "current_phase": "Phase 1: Platform Development",
  "next_phase": "Phase 2: Beta Testing",
  "transition_probability": 67.5,
  "estimated_days": 14
}
```

### Business Metrics

**Get Metrics:**
```
GET /api/metrics
```

**Update Metrics:**
```
POST /api/metrics
Content-Type: application/json

{
  "revenue": 1500,
  "users": 42,
  "engagement_score": 8.5,
  "conversion_rate": 3.2
}
```

### Visitor Statistics

**Get Daily Stats:**
```
GET /api/visitors?days=30
```

Returns last N days of visitor data.

**Get Summary:**
```
GET /api/visitors/summary
```

Returns aggregated visitor statistics.

**Response:**
```json
{
  "total_visitors": 3542,
  "total_pageviews": 12847,
  "avg_bounce_rate": 45.3,
  "avg_session_duration": 182,
  "days_tracked": 30
}
```

### Event Tracking

**Track Page View:**
```
POST /api/track/pageview
Content-Type: application/json

{
  "page": "analytics-dashboard.html",
  "referrer": "user-dashboard.html",
  "user_agent": "Mozilla/5.0..."
}
```

**Track Button Click:**
```
POST /api/track/click
Content-Type: application/json

{
  "button": "export-data",
  "page": "analytics-dashboard.html"
}
```

### Data Vacuum Stats
```
GET /api/vacuum-stats
```

Returns statistics from the consciousness data vacuum.

### Analytics Summary
```
GET /api/analytics-summary
```

Returns summary of page views, clicks, and unique visitors.

## Data Storage

The backend stores data in JSON files:

- `data/business_metrics.json`: Business metrics history
- `data/phase_prediction.json`: Phase prediction data
- `data/consciousness_data.json`: Data vacuum statistics
- `data/analytics_data.json`: Page views and click tracking
- `data/visitor_data.json`: Daily visitor statistics

**Auto-Generated Demo Data:**

On first run, the system generates realistic demo data:
- 30 days of visitor statistics
- Random daily visitors (50-250)
- Random pageviews (150-800)
- Realistic bounce rates (30-60%)
- Session durations (60-300 seconds)

## Frontend Integration

The backend is designed to work with:
- `PLATFORM/analytics-dashboard.html` (main dashboard)
- `PLATFORM/analytics-traps-dashboard.html` (visitor intelligence)

The frontend expects the API at `http://localhost:5100`

## Configuration

No environment variables required - works out of the box!

Optional configurations can be added via `.env` file if needed for production deployment.

## Dependencies

- **Flask**: Web framework
- **flask-cors**: CORS support for frontend integration
- **python-dotenv**: Environment variable management (optional)

## Testing

Test endpoints using curl:

```bash
# Health check
curl http://localhost:5100/api/health

# Get dashboard
curl http://localhost:5100/api/dashboard

# Get business phase
curl http://localhost:5100/api/business-phase

# Get visitor summary
curl http://localhost:5100/api/visitors/summary

# Update metrics
curl -X POST http://localhost:5100/api/metrics \
  -H "Content-Type: application/json" \
  -d '{"revenue":1500,"users":42,"engagement_score":8.5,"conversion_rate":3.2}'

# Track page view
curl -X POST http://localhost:5100/api/track/pageview \
  -H "Content-Type: application/json" \
  -d '{"page":"analytics-dashboard.html","referrer":"user-dashboard.html"}'
```

## Production Deployment

For production deployment:

1. Set up proper database (PostgreSQL, MongoDB)
2. Add authentication for metric updates
3. Implement rate limiting
4. Enable HTTPS/SSL
5. Add proper logging and monitoring
6. Configure CORS for specific domains
7. Set up backup/restore for data files

## Integration with Other Systems

This backend can integrate with:

- **Business Phase Clock**: Reads phase predictions
- **Data Vacuum**: Reads content extraction stats
- **Analytics Traps**: Receives tracking events
- **Metrics Tracker**: Stores business metrics

## Next Steps

1. ✅ Basic API implementation complete
2. ⏳ Test with frontend integration
3. ⏳ Add authentication for write endpoints
4. ⏳ Migrate to PostgreSQL database
5. ⏳ Deploy to production server

## Status

**✅ COMPLETE - Ready for Testing**

All core endpoints implemented. Demo data auto-generated. Frontend integration ready.

---

**Part of**: 100x Platform - Consciousness Revolution
**Created**: 2025-11-22
**Trinity Instance**: C1 Mechanic (Autonomous Work Protocol)
