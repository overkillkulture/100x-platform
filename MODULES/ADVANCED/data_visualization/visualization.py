"""MODULE #44: DATA VISUALIZATION - Charts, graphs, dashboards"""
import json
from typing import List, Dict, Any

class DataVisualization:
    def __init__(self):
        self.charts = []

    def bar_chart(self, data: Dict[str, float], title: str = "Bar Chart") -> str:
        """Create bar chart HTML"""
        html = f'<div class="chart"><h3>{title}</h3>'
        max_val = max(data.values()) if data else 1

        for label, value in data.items():
            width = (value / max_val) * 100
            html += f'<div class="bar">'
            html += f'<span class="label">{label}</span>'
            html += f'<div class="bar-fill" style="width:{width}%"></div>'
            html += f'<span class="value">{value}</span>'
            html += f'</div>'

        html += '</div>'
        return html

    def line_chart_data(self, data: List[float], labels: List[str] = None) -> Dict:
        """Generate line chart data"""
        return {
            'type': 'line',
            'data': data,
            'labels': labels or [str(i) for i in range(len(data))],
            'points': len(data)
        }

    def pie_chart_data(self, data: Dict[str, float]) -> Dict:
        """Generate pie chart data"""
        total = sum(data.values())
        return {
            'type': 'pie',
            'slices': [
                {'label': k, 'value': v, 'percent': (v/total)*100}
                for k, v in data.items()
            ]
        }

    def dashboard_html(self, charts: List[Dict]) -> str:
        """Create complete dashboard HTML"""
        html = '''
<!DOCTYPE html>
<html>
<head>
    <title>Data Dashboard</title>
    <style>
        body { font-family: Arial; background: #1a1a1a; color: #00ff00; padding: 20px; }
        .dashboard { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }
        .chart { background: #2a2a2a; border: 2px solid #00ff00; padding: 20px; border-radius: 8px; }
        .bar { margin: 10px 0; display: flex; align-items: center; }
        .bar-fill { height: 30px; background: #00ff00; margin: 0 10px; }
        .label { width: 100px; }
        .value { width: 60px; text-align: right; }
    </style>
</head>
<body>
    <h1>📊 Data Dashboard</h1>
    <div class="dashboard">
'''
        for chart in charts:
            html += f'<div class="chart">{chart}</div>'

        html += '''
    </div>
</body>
</html>
'''
        return html

if __name__ == "__main__":
    viz = DataVisualization()

    # Create bar chart
    data = {'Module 1': 100, 'Module 2': 85, 'Module 3': 95}
    chart = viz.bar_chart(data, "Module Completion")

    # Create dashboard
    dashboard = viz.dashboard_html([chart])

    with open('/tmp/test_dashboard.html', 'w') as f:
        f.write(dashboard)

    print("✅ Data Visualization working!")
    print("Dashboard saved to /tmp/test_dashboard.html")
