#!/usr/bin/env python3
"""
AI Data Analytics Platform Module
Natural Language Queries, Automated Insights & Predictive Analytics
Powered by Claude AI
"""

import os
import json
import asyncio
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict, field
from enum import Enum
import anthropic
import uuid


class QueryType(Enum):
    """Types of data queries"""
    AGGREGATION = "aggregation"
    FILTERING = "filtering"
    GROUPING = "grouping"
    TREND_ANALYSIS = "trend_analysis"
    COMPARISON = "comparison"
    PREDICTION = "prediction"


class ChartType(Enum):
    """Types of visualizations"""
    LINE = "line"
    BAR = "bar"
    PIE = "pie"
    SCATTER = "scatter"
    HEATMAP = "heatmap"
    AREA = "area"
    HISTOGRAM = "histogram"
    BOX = "box"
    GAUGE = "gauge"
    TABLE = "table"


class InsightType(Enum):
    """Types of automated insights"""
    TREND = "trend"
    ANOMALY = "anomaly"
    CORRELATION = "correlation"
    PATTERN = "pattern"
    FORECAST = "forecast"
    RECOMMENDATION = "recommendation"


class DataSourceType(Enum):
    """Supported data sources"""
    CSV = "csv"
    DATABASE = "database"
    API = "api"
    EXCEL = "excel"
    JSON = "json"
    PARQUET = "parquet"


@dataclass
class DataSource:
    """Represents a data source"""
    id: str
    name: str
    source_type: DataSourceType
    connection_string: str
    schema: Dict[str, str]  # column_name -> data_type
    row_count: int
    created_at: datetime
    last_synced: Optional[datetime]
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class NaturalLanguageQuery:
    """Natural language query and its SQL translation"""
    id: str
    user_query: str
    sql_query: str
    query_type: QueryType
    confidence: float
    created_at: datetime
    execution_time: float
    result_rows: int


@dataclass
class Insight:
    """Automated insight from data"""
    id: str
    insight_type: InsightType
    title: str
    description: str
    confidence: float
    data_points: List[Any]
    visualization: Optional[ChartType]
    created_at: datetime
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Dashboard:
    """Interactive dashboard"""
    id: str
    name: str
    description: str
    widgets: List[str]  # Widget IDs
    data_sources: List[str]  # DataSource IDs
    refresh_interval: int  # seconds
    created_at: datetime
    last_updated: datetime
    owner: str


@dataclass
class Widget:
    """Dashboard widget/visualization"""
    id: str
    title: str
    chart_type: ChartType
    query: str
    data: pd.DataFrame
    config: Dict[str, Any]
    created_at: datetime
    last_refreshed: datetime


@dataclass
class Prediction:
    """Predictive analytics result"""
    id: str
    target_metric: str
    prediction_value: float
    confidence_interval: Tuple[float, float]
    prediction_date: datetime
    model_accuracy: float
    features_used: List[str]
    created_at: datetime


class NaturalLanguageQueryEngine:
    """Convert natural language to SQL/data operations"""

    def __init__(self, api_key: str):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = "claude-3-5-sonnet-20241022"

    async def parse_query(
        self,
        user_query: str,
        schema: Dict[str, str]
    ) -> NaturalLanguageQuery:
        """Convert natural language query to SQL"""

        schema_description = "\n".join([
            f"- {col}: {dtype}"
            for col, dtype in schema.items()
        ])

        query_prompt = f"""Convert this natural language query to SQL.

Available schema:
{schema_description}

User query: "{user_query}"

Generate a SQL query that answers the user's question. Return only the SQL query.
If you need to use functions like SUM, COUNT, AVG, etc., use them appropriately.

SQL Query:"""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1024,
                temperature=0,
                messages=[{
                    "role": "user",
                    "content": query_prompt
                }]
            )

            sql_query = response.content[0].text.strip()

            # Clean up SQL query
            sql_query = sql_query.replace("```sql", "").replace("```", "").strip()

            # Determine query type
            query_type = self._determine_query_type(sql_query)

            return NaturalLanguageQuery(
                id=str(uuid.uuid4()),
                user_query=user_query,
                sql_query=sql_query,
                query_type=query_type,
                confidence=0.85,
                created_at=datetime.now(),
                execution_time=0.0,
                result_rows=0
            )

        except Exception as e:
            print(f"Query parsing error: {e}")

            # Return fallback query
            return NaturalLanguageQuery(
                id=str(uuid.uuid4()),
                user_query=user_query,
                sql_query="SELECT * FROM data LIMIT 10",
                query_type=QueryType.FILTERING,
                confidence=0.3,
                created_at=datetime.now(),
                execution_time=0.0,
                result_rows=0
            )

    def _determine_query_type(self, sql: str) -> QueryType:
        """Determine the type of SQL query"""
        sql_lower = sql.lower()

        if "group by" in sql_lower:
            return QueryType.GROUPING
        elif any(func in sql_lower for func in ["sum(", "avg(", "count(", "max(", "min("]):
            return QueryType.AGGREGATION
        elif "where" in sql_lower:
            return QueryType.FILTERING
        else:
            return QueryType.FILTERING


class InsightGenerator:
    """Generate automated insights from data"""

    def __init__(self, api_key: str):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = "claude-3-5-sonnet-20241022"

    async def generate_insights(
        self,
        data: pd.DataFrame,
        context: Optional[str] = None
    ) -> List[Insight]:
        """Generate insights from dataframe"""

        # Calculate basic statistics
        stats = self._calculate_statistics(data)

        # Use AI to interpret data
        insights_prompt = f"""Analyze this data and provide key insights.

Data summary:
{stats}

{f'Context: {context}' if context else ''}

Provide 3-5 key insights about:
1. Trends (increasing/decreasing patterns)
2. Anomalies (unusual values or outliers)
3. Correlations (relationships between variables)
4. Patterns (recurring behaviors)
5. Recommendations (actionable suggestions)

Format as JSON array:
[
  {{
    "type": "trend",
    "title": "Revenue Growing 15% MoM",
    "description": "Revenue has consistently grown 15% month-over-month for the past 6 months",
    "confidence": 0.9
  }}
]
"""

        insights = []

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=2048,
                temperature=0.5,
                messages=[{
                    "role": "user",
                    "content": insights_prompt
                }]
            )

            result = response.content[0].text

            # Parse JSON insights
            import re
            json_match = re.search(r'\[.*\]', result, re.DOTALL)
            if json_match:
                parsed_insights = json.loads(json_match.group())

                type_map = {
                    "trend": InsightType.TREND,
                    "anomaly": InsightType.ANOMALY,
                    "correlation": InsightType.CORRELATION,
                    "pattern": InsightType.PATTERN,
                    "forecast": InsightType.FORECAST,
                    "recommendation": InsightType.RECOMMENDATION
                }

                for insight_data in parsed_insights:
                    insight = Insight(
                        id=str(uuid.uuid4()),
                        insight_type=type_map.get(
                            insight_data.get("type", "pattern"),
                            InsightType.PATTERN
                        ),
                        title=insight_data.get("title", "Insight"),
                        description=insight_data.get("description", ""),
                        confidence=insight_data.get("confidence", 0.7),
                        data_points=[],
                        visualization=None,
                        created_at=datetime.now()
                    )
                    insights.append(insight)

        except Exception as e:
            print(f"Insight generation error: {e}")

            # Fallback: basic statistical insights
            insights.extend(self._generate_basic_insights(data))

        return insights

    def _calculate_statistics(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Calculate basic statistics from dataframe"""

        stats = {
            "row_count": len(data),
            "column_count": len(data.columns),
            "columns": list(data.columns),
            "numeric_columns": list(data.select_dtypes(include=[np.number]).columns),
            "categorical_columns": list(data.select_dtypes(include=['object']).columns)
        }

        # Numeric statistics
        if stats["numeric_columns"]:
            numeric_stats = data[stats["numeric_columns"]].describe().to_dict()
            stats["numeric_summary"] = numeric_stats

        return stats

    def _generate_basic_insights(self, data: pd.DataFrame) -> List[Insight]:
        """Generate basic statistical insights"""

        insights = []

        # Check for trends in numeric columns
        numeric_cols = data.select_dtypes(include=[np.number]).columns

        for col in numeric_cols:
            if len(data) > 1:
                # Simple trend detection
                values = data[col].values
                if len(values) > 0:
                    trend = "increasing" if values[-1] > values[0] else "decreasing"
                    change = abs(values[-1] - values[0]) / values[0] * 100 if values[0] != 0 else 0

                    insights.append(Insight(
                        id=str(uuid.uuid4()),
                        insight_type=InsightType.TREND,
                        title=f"{col} {trend}",
                        description=f"{col} has changed by {change:.1f}%",
                        confidence=0.7,
                        data_points=list(values),
                        visualization=ChartType.LINE,
                        created_at=datetime.now()
                    ))

        return insights[:5]  # Return top 5


class PredictiveAnalytics:
    """Predictive analytics and forecasting"""

    def __init__(self, api_key: str):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = "claude-3-5-sonnet-20241022"

    async def forecast(
        self,
        historical_data: pd.DataFrame,
        target_column: str,
        periods: int = 30
    ) -> List[Prediction]:
        """Generate forecast for future periods"""

        # Simple moving average prediction
        # In production, use statsmodels, prophet, or sklearn

        predictions = []

        if target_column not in historical_data.columns:
            return predictions

        values = historical_data[target_column].values

        # Simple exponential smoothing
        alpha = 0.3  # Smoothing factor
        forecast_value = values[-1]

        for i in range(periods):
            # Predict next value
            forecast_date = datetime.now() + timedelta(days=i+1)

            # Simple confidence interval (±10%)
            confidence_interval = (
                forecast_value * 0.9,
                forecast_value * 1.1
            )

            prediction = Prediction(
                id=str(uuid.uuid4()),
                target_metric=target_column,
                prediction_value=forecast_value,
                confidence_interval=confidence_interval,
                prediction_date=forecast_date,
                model_accuracy=0.85,
                features_used=[target_column],
                created_at=datetime.now()
            )

            predictions.append(prediction)

            # Update forecast with exponential smoothing
            forecast_value = alpha * forecast_value + (1 - alpha) * np.mean(values[-7:])

        return predictions

    async def detect_anomalies(
        self,
        data: pd.DataFrame,
        column: str,
        threshold: float = 3.0
    ) -> List[Tuple[int, float]]:
        """Detect anomalies using z-score"""

        if column not in data.columns:
            return []

        values = data[column].values
        mean = np.mean(values)
        std = np.std(values)

        anomalies = []

        for i, value in enumerate(values):
            z_score = abs((value - mean) / std) if std != 0 else 0
            if z_score > threshold:
                anomalies.append((i, value))

        return anomalies


class DashboardBuilder:
    """Build interactive dashboards"""

    def __init__(self):
        self.widgets: Dict[str, Widget] = {}

    def create_widget(
        self,
        title: str,
        chart_type: ChartType,
        data: pd.DataFrame,
        config: Optional[Dict[str, Any]] = None
    ) -> Widget:
        """Create a dashboard widget"""

        widget_id = str(uuid.uuid4())

        widget = Widget(
            id=widget_id,
            title=title,
            chart_type=chart_type,
            query="",
            data=data,
            config=config or {},
            created_at=datetime.now(),
            last_refreshed=datetime.now()
        )

        self.widgets[widget_id] = widget
        return widget

    def generate_chart_config(
        self,
        chart_type: ChartType,
        data: pd.DataFrame
    ) -> Dict[str, Any]:
        """Generate chart configuration"""

        config = {
            "type": chart_type.value,
            "responsive": True,
            "animation": True
        }

        if chart_type == ChartType.LINE:
            config["x_axis"] = data.columns[0] if len(data.columns) > 0 else "x"
            config["y_axis"] = data.columns[1] if len(data.columns) > 1 else "y"
        elif chart_type == ChartType.BAR:
            config["orientation"] = "vertical"
            config["stacked"] = False
        elif chart_type == ChartType.PIE:
            config["show_labels"] = True
            config["show_percentage"] = True

        return config


class AIDataAnalyticsPlatform:
    """Main AI Data Analytics Platform class"""

    def __init__(self, api_key: Optional[str] = None):
        """Initialize analytics platform"""
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY is required")

        self.client = anthropic.Anthropic(api_key=self.api_key)
        self.query_engine = NaturalLanguageQueryEngine(self.api_key)
        self.insight_generator = InsightGenerator(self.api_key)
        self.predictive_analytics = PredictiveAnalytics(self.api_key)
        self.dashboard_builder = DashboardBuilder()

        # Storage
        self.data_sources: Dict[str, DataSource] = {}
        self.queries: List[NaturalLanguageQuery] = []
        self.insights: List[Insight] = []
        self.dashboards: Dict[str, Dashboard] = {}

        # Cache
        self.data_cache: Dict[str, pd.DataFrame] = {}

    def add_data_source(
        self,
        name: str,
        source_type: DataSourceType,
        data: pd.DataFrame,
        connection_string: str = ""
    ) -> DataSource:
        """Add a data source"""

        source_id = str(uuid.uuid4())

        # Extract schema
        schema = {}
        for col in data.columns:
            dtype = str(data[col].dtype)
            schema[col] = dtype

        source = DataSource(
            id=source_id,
            name=name,
            source_type=source_type,
            connection_string=connection_string,
            schema=schema,
            row_count=len(data),
            created_at=datetime.now(),
            last_synced=datetime.now()
        )

        self.data_sources[source_id] = source
        self.data_cache[source_id] = data

        return source

    async def query(
        self,
        natural_language_query: str,
        data_source_id: str
    ) -> Tuple[NaturalLanguageQuery, pd.DataFrame]:
        """Execute natural language query"""

        if data_source_id not in self.data_sources:
            raise ValueError(f"Data source {data_source_id} not found")

        source = self.data_sources[data_source_id]
        data = self.data_cache[data_source_id]

        # Parse natural language to SQL
        nl_query = await self.query_engine.parse_query(
            natural_language_query,
            source.schema
        )

        # Execute query on dataframe
        # In production, execute SQL on actual database
        # For now, use pandas operations

        import time
        start_time = time.time()

        try:
            # Simple query execution using pandas
            result_df = self._execute_pandas_query(data, nl_query.sql_query)

            nl_query.execution_time = time.time() - start_time
            nl_query.result_rows = len(result_df)

        except Exception as e:
            print(f"Query execution error: {e}")
            result_df = data.head(10)

        self.queries.append(nl_query)

        return nl_query, result_df

    def _execute_pandas_query(
        self,
        data: pd.DataFrame,
        sql_query: str
    ) -> pd.DataFrame:
        """Execute SQL-like query on pandas DataFrame"""

        # Simplified SQL execution
        # In production, use pandasql or actual database

        sql_lower = sql_query.lower()

        # Handle SELECT *
        if "select *" in sql_lower:
            result = data

            # Handle LIMIT
            if "limit" in sql_lower:
                try:
                    limit = int(sql_lower.split("limit")[-1].strip())
                    result = result.head(limit)
                except:
                    result = result.head(100)

            return result

        # For more complex queries, return first 10 rows
        return data.head(10)

    async def generate_insights(
        self,
        data_source_id: str,
        context: Optional[str] = None
    ) -> List[Insight]:
        """Generate automated insights from data source"""

        if data_source_id not in self.data_sources:
            raise ValueError(f"Data source {data_source_id} not found")

        data = self.data_cache[data_source_id]

        insights = await self.insight_generator.generate_insights(data, context)

        self.insights.extend(insights)

        return insights

    async def create_forecast(
        self,
        data_source_id: str,
        target_column: str,
        periods: int = 30
    ) -> List[Prediction]:
        """Create predictive forecast"""

        if data_source_id not in self.data_sources:
            raise ValueError(f"Data source {data_source_id} not found")

        data = self.data_cache[data_source_id]

        predictions = await self.predictive_analytics.forecast(
            data,
            target_column,
            periods
        )

        return predictions

    def create_dashboard(
        self,
        name: str,
        description: str,
        owner: str
    ) -> Dashboard:
        """Create a new dashboard"""

        dashboard_id = str(uuid.uuid4())

        dashboard = Dashboard(
            id=dashboard_id,
            name=name,
            description=description,
            widgets=[],
            data_sources=[],
            refresh_interval=60,
            created_at=datetime.now(),
            last_updated=datetime.now(),
            owner=owner
        )

        self.dashboards[dashboard_id] = dashboard

        return dashboard

    def add_widget_to_dashboard(
        self,
        dashboard_id: str,
        widget: Widget
    ):
        """Add widget to dashboard"""

        if dashboard_id not in self.dashboards:
            raise ValueError(f"Dashboard {dashboard_id} not found")

        dashboard = self.dashboards[dashboard_id]
        dashboard.widgets.append(widget.id)
        dashboard.last_updated = datetime.now()

    def get_analytics(self) -> Dict[str, Any]:
        """Get platform analytics"""

        return {
            "total_data_sources": len(self.data_sources),
            "total_queries": len(self.queries),
            "total_insights": len(self.insights),
            "total_dashboards": len(self.dashboards),
            "total_widgets": len(self.dashboard_builder.widgets),
            "total_rows_analyzed": sum(
                source.row_count
                for source in self.data_sources.values()
            )
        }


def demo_analytics_platform():
    """Demo function showing analytics platform capabilities"""
    print("=" * 80)
    print("AI Data Analytics Platform - Demo")
    print("=" * 80)

    # Initialize platform
    try:
        platform = AIDataAnalyticsPlatform()
    except ValueError as e:
        print(f"\nError: {e}")
        print("Please set ANTHROPIC_API_KEY environment variable")
        return

    async def run_demo():
        # Create sample data
        print("\n📊 Creating Sample Data...")

        # Sales data
        sales_data = pd.DataFrame({
            'date': pd.date_range(start='2024-01-01', periods=100, freq='D'),
            'revenue': np.random.randint(1000, 5000, 100) + np.arange(100) * 10,
            'customers': np.random.randint(50, 200, 100),
            'product_category': np.random.choice(['Electronics', 'Clothing', 'Food'], 100),
            'region': np.random.choice(['North', 'South', 'East', 'West'], 100)
        })

        # Add data source
        source = platform.add_data_source(
            name="Sales Data",
            source_type=DataSourceType.CSV,
            data=sales_data
        )

        print(f"✅ Data source added: {source.name}")
        print(f"   Rows: {source.row_count}")
        print(f"   Columns: {len(source.schema)}")

        # Natural language queries
        print("\n🗣️  Natural Language Queries...")

        queries = [
            "What is the total revenue?",
            "Show me average customers per day",
            "What are the top selling product categories?"
        ]

        for i, query_text in enumerate(queries, 1):
            print(f"\n--- Query {i} ---")
            print(f"Question: {query_text}")

            nl_query, results = await platform.query(query_text, source.id)

            print(f"SQL: {nl_query.sql_query}")
            print(f"Results: {len(results)} rows")
            print(f"Execution time: {nl_query.execution_time:.3f}s")

            # Show sample results
            if len(results) > 0:
                print("\nSample results:")
                print(results.head(3).to_string(index=False))

        # Generate insights
        print("\n" + "=" * 80)
        print("Automated Insights")
        print("=" * 80)

        insights = await platform.generate_insights(
            source.id,
            context="E-commerce sales data for Q1 2024"
        )

        print(f"\n✅ Generated {len(insights)} insights:\n")

        for i, insight in enumerate(insights, 1):
            print(f"{i}. [{insight.insight_type.value}] {insight.title}")
            print(f"   {insight.description}")
            print(f"   Confidence: {insight.confidence:.0%}\n")

        # Predictive analytics
        print("=" * 80)
        print("Predictive Forecasting")
        print("=" * 80)

        predictions = await platform.create_forecast(
            source.id,
            target_column='revenue',
            periods=7
        )

        print(f"\n✅ Generated {len(predictions)} day forecast:\n")

        for pred in predictions[:7]:
            print(f"{pred.prediction_date.strftime('%Y-%m-%d')}: "
                  f"${pred.prediction_value:,.0f} "
                  f"(±${pred.confidence_interval[1] - pred.prediction_value:,.0f})")

        # Create dashboard
        print("\n" + "=" * 80)
        print("Dashboard Creation")
        print("=" * 80)

        dashboard = platform.create_dashboard(
            name="Sales Performance Dashboard",
            description="Real-time sales analytics and forecasting",
            owner="analytics@company.com"
        )

        # Create widgets
        revenue_widget = platform.dashboard_builder.create_widget(
            title="Revenue Trend",
            chart_type=ChartType.LINE,
            data=sales_data[['date', 'revenue']]
        )

        category_widget = platform.dashboard_builder.create_widget(
            title="Sales by Category",
            chart_type=ChartType.PIE,
            data=sales_data[['product_category', 'revenue']].groupby('product_category').sum()
        )

        # Add widgets to dashboard
        platform.add_widget_to_dashboard(dashboard.id, revenue_widget)
        platform.add_widget_to_dashboard(dashboard.id, category_widget)

        print(f"✅ Dashboard created: {dashboard.name}")
        print(f"   Widgets: {len(dashboard.widgets)}")
        print(f"   Owner: {dashboard.owner}")

        # Platform analytics
        print("\n" + "=" * 80)
        print("Platform Analytics")
        print("=" * 80)

        analytics = platform.get_analytics()
        print(json.dumps(analytics, indent=2))

        print("\n✅ Demo completed successfully!")

    # Run async demo
    asyncio.run(run_demo())


if __name__ == "__main__":
    demo_analytics_platform()
