"""
MODULE #27: TIME SERIES FORECASTING
Instance 3: Module Developer
Built: 2025-11-08

Predict the future from past patterns.
Track trends, detect seasonality, forecast what comes next.
"""

import numpy as np
from typing import List, Dict, Any, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
import json


class ForecastMethod(Enum):
    """Forecasting methods"""
    MOVING_AVERAGE = "moving_average"
    EXPONENTIAL_SMOOTHING = "exponential_smoothing"
    LINEAR_REGRESSION = "linear_regression"
    ARIMA = "arima"
    SEASONAL_DECOMPOSE = "seasonal_decompose"


@dataclass
class ForecastResult:
    """Result of forecasting"""
    predictions: List[float]
    confidence_intervals: Optional[List[Tuple[float, float]]]
    method: str
    metrics: Dict[str, float]


class TimeSeriesAnalyzer:
    """
    Complete time series analysis and forecasting toolkit

    Features:
    - Trend detection
    - Seasonality analysis
    - Anomaly detection
    - Multiple forecasting methods
    - Accuracy metrics
    """

    def __init__(self, data: List[float]):
        self.data = np.array(data)
        self.n = len(data)

    def detect_trend(self) -> Dict[str, Any]:
        """
        Detect trend in time series

        Returns:
            Direction, strength, and slope
        """

        # Linear regression to find trend
        x = np.arange(self.n)
        y = self.data

        # Calculate slope and intercept
        x_mean = np.mean(x)
        y_mean = np.mean(y)

        numerator = np.sum((x - x_mean) * (y - y_mean))
        denominator = np.sum((x - x_mean) ** 2)

        slope = numerator / denominator if denominator != 0 else 0
        intercept = y_mean - slope * x_mean

        # Calculate R-squared (strength of trend)
        y_pred = slope * x + intercept
        ss_res = np.sum((y - y_pred) ** 2)
        ss_tot = np.sum((y - y_mean) ** 2)
        r_squared = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0

        # Determine direction
        if abs(slope) < 0.01:
            direction = "flat"
        elif slope > 0:
            direction = "increasing"
        else:
            direction = "decreasing"

        return {
            'direction': direction,
            'slope': slope,
            'intercept': intercept,
            'r_squared': r_squared,
            'strength': 'strong' if r_squared > 0.7 else 'moderate' if r_squared > 0.4 else 'weak'
        }

    def detect_seasonality(self, period: int = None) -> Dict[str, Any]:
        """
        Detect seasonality in time series

        Args:
            period: Expected seasonal period (auto-detect if None)

        Returns:
            Seasonality information
        """

        if period is None:
            # Auto-detect period using autocorrelation
            period = self._find_period()

        if period is None or period >= self.n // 2:
            return {
                'has_seasonality': False,
                'period': None,
                'strength': 0
            }

        # Calculate seasonal component
        seasonal = self._extract_seasonal(period)

        # Calculate strength (variance explained by seasonality)
        deseasonalized = self.data - seasonal
        var_original = np.var(self.data)
        var_deseasonalized = np.var(deseasonalized)

        strength = 1 - (var_deseasonalized / var_original) if var_original != 0 else 0

        return {
            'has_seasonality': strength > 0.1,
            'period': period,
            'strength': strength,
            'seasonal_pattern': seasonal[:period].tolist()
        }

    def _find_period(self) -> Optional[int]:
        """Find dominant period using autocorrelation"""

        max_lag = min(self.n // 2, 50)

        autocorr = []
        for lag in range(1, max_lag):
            corr = np.corrcoef(self.data[:-lag], self.data[lag:])[0, 1]
            autocorr.append(corr)

        # Find peaks in autocorrelation
        autocorr = np.array(autocorr)

        if len(autocorr) < 3:
            return None

        peaks = []
        for i in range(1, len(autocorr) - 1):
            if autocorr[i] > autocorr[i-1] and autocorr[i] > autocorr[i+1] and autocorr[i] > 0.2:
                peaks.append((i + 1, autocorr[i]))

        if peaks:
            # Return lag with highest autocorrelation
            return max(peaks, key=lambda x: x[1])[0]

        return None

    def _extract_seasonal(self, period: int) -> np.ndarray:
        """Extract seasonal component"""

        n_periods = self.n // period
        seasonal_avg = np.zeros(period)

        for i in range(period):
            values = [self.data[i + j * period] for j in range(n_periods) if i + j * period < self.n]
            seasonal_avg[i] = np.mean(values)

        # Normalize (center around 0)
        seasonal_avg -= np.mean(seasonal_avg)

        # Repeat to match data length
        seasonal = np.tile(seasonal_avg, (self.n // period) + 1)[:self.n]

        return seasonal

    def decompose(self, period: int = None) -> Dict[str, np.ndarray]:
        """
        Decompose time series into trend, seasonal, and residual

        Returns:
            Dictionary with trend, seasonal, and residual components
        """

        # Extract trend
        trend_info = self.detect_trend()
        x = np.arange(self.n)
        trend = trend_info['slope'] * x + trend_info['intercept']

        # Extract seasonal
        if period is None:
            seasonality = self.detect_seasonality()
            period = seasonality.get('period')

        if period and period < self.n // 2:
            seasonal = self._extract_seasonal(period)
        else:
            seasonal = np.zeros(self.n)

        # Residual
        residual = self.data - trend - seasonal

        return {
            'trend': trend,
            'seasonal': seasonal,
            'residual': residual,
            'original': self.data
        }

    def detect_anomalies(self, threshold: float = 3.0) -> List[int]:
        """
        Detect anomalies using statistical methods

        Args:
            threshold: Number of standard deviations for anomaly

        Returns:
            List of anomaly indices
        """

        # Use residuals from decomposition
        decomp = self.decompose()
        residual = decomp['residual']

        # Z-score method
        mean = np.mean(residual)
        std = np.std(residual)

        if std == 0:
            return []

        z_scores = np.abs((residual - mean) / std)

        anomalies = np.where(z_scores > threshold)[0].tolist()

        return anomalies

    def forecast_moving_average(self, window: int, steps: int) -> ForecastResult:
        """
        Forecast using moving average

        Args:
            window: Window size
            steps: Number of steps to forecast

        Returns:
            ForecastResult
        """

        predictions = []
        current_data = self.data.copy()

        for _ in range(steps):
            # Take average of last 'window' points
            avg = np.mean(current_data[-window:])
            predictions.append(avg)

            # Add prediction to data for next step
            current_data = np.append(current_data, avg)

        # Calculate metrics on training data
        train_pred = []
        for i in range(window, self.n):
            train_pred.append(np.mean(self.data[i-window:i]))

        mae = np.mean(np.abs(np.array(train_pred) - self.data[window:]))

        return ForecastResult(
            predictions=predictions,
            confidence_intervals=None,
            method="moving_average",
            metrics={'mae': mae, 'window': window}
        )

    def forecast_exponential_smoothing(
        self,
        alpha: float,
        steps: int
    ) -> ForecastResult:
        """
        Forecast using exponential smoothing

        Args:
            alpha: Smoothing parameter (0-1)
            steps: Number of steps to forecast

        Returns:
            ForecastResult
        """

        # Calculate smoothed values
        smoothed = [self.data[0]]

        for i in range(1, self.n):
            s = alpha * self.data[i] + (1 - alpha) * smoothed[-1]
            smoothed.append(s)

        # Forecast (flat forecast at last smoothed value)
        last_smoothed = smoothed[-1]
        predictions = [last_smoothed] * steps

        # Calculate MAE on training data
        smoothed = np.array(smoothed)
        mae = np.mean(np.abs(smoothed - self.data))

        return ForecastResult(
            predictions=predictions,
            confidence_intervals=None,
            method="exponential_smoothing",
            metrics={'mae': mae, 'alpha': alpha}
        )

    def forecast_linear_regression(self, steps: int) -> ForecastResult:
        """
        Forecast using linear regression (trend extrapolation)

        Args:
            steps: Number of steps to forecast

        Returns:
            ForecastResult
        """

        trend_info = self.detect_trend()

        slope = trend_info['slope']
        intercept = trend_info['intercept']

        # Extrapolate
        future_x = np.arange(self.n, self.n + steps)
        predictions = (slope * future_x + intercept).tolist()

        # Calculate MAE on training data
        x = np.arange(self.n)
        train_pred = slope * x + intercept
        mae = np.mean(np.abs(train_pred - self.data))

        return ForecastResult(
            predictions=predictions,
            confidence_intervals=None,
            method="linear_regression",
            metrics={'mae': mae, 'r_squared': trend_info['r_squared']}
        )

    def forecast_seasonal(self, period: int, steps: int) -> ForecastResult:
        """
        Forecast using seasonal decomposition

        Args:
            period: Seasonal period
            steps: Number of steps to forecast

        Returns:
            ForecastResult
        """

        decomp = self.decompose(period)

        # Project trend forward
        trend = decomp['trend']
        slope = (trend[-1] - trend[0]) / len(trend)
        future_trend = [trend[-1] + slope * (i + 1) for i in range(steps)]

        # Repeat seasonal pattern
        seasonal = decomp['seasonal']
        seasonal_pattern = seasonal[:period]
        future_seasonal = [seasonal_pattern[i % period] for i in range(steps)]

        # Combine
        predictions = [future_trend[i] + future_seasonal[i] for i in range(steps)]

        # Calculate MAE
        reconstructed = decomp['trend'] + decomp['seasonal']
        mae = np.mean(np.abs(reconstructed - self.data))

        return ForecastResult(
            predictions=predictions,
            confidence_intervals=None,
            method="seasonal_decompose",
            metrics={'mae': mae, 'period': period}
        )

    def auto_forecast(self, steps: int) -> ForecastResult:
        """
        Automatically select best forecasting method

        Args:
            steps: Number of steps to forecast

        Returns:
            Best ForecastResult
        """

        # Try different methods
        methods = []

        # Moving average
        for window in [3, 5, 7, 10]:
            if window < self.n:
                result = self.forecast_moving_average(window, steps)
                methods.append(result)

        # Exponential smoothing
        for alpha in [0.1, 0.3, 0.5, 0.7, 0.9]:
            result = self.forecast_exponential_smoothing(alpha, steps)
            methods.append(result)

        # Linear regression
        result = self.forecast_linear_regression(steps)
        methods.append(result)

        # Seasonal (if seasonality detected)
        seasonality = self.detect_seasonality()
        if seasonality['has_seasonality']:
            result = self.forecast_seasonal(seasonality['period'], steps)
            methods.append(result)

        # Select method with lowest MAE
        best = min(methods, key=lambda x: x.metrics['mae'])

        return best


def calculate_accuracy_metrics(
    actual: List[float],
    predicted: List[float]
) -> Dict[str, float]:
    """
    Calculate forecasting accuracy metrics

    Returns:
        MAE, RMSE, MAPE
    """

    actual = np.array(actual)
    predicted = np.array(predicted)

    # Mean Absolute Error
    mae = np.mean(np.abs(actual - predicted))

    # Root Mean Squared Error
    rmse = np.sqrt(np.mean((actual - predicted) ** 2))

    # Mean Absolute Percentage Error
    mape = np.mean(np.abs((actual - predicted) / (actual + 1e-10))) * 100

    return {
        'mae': mae,
        'rmse': rmse,
        'mape': mape
    }


def demo_trend_detection():
    """Demonstrate trend detection"""

    print("=" * 60)
    print("TIME SERIES - TREND DETECTION DEMO")
    print("=" * 60)
    print()

    # Create data with upward trend
    np.random.seed(42)
    data = [10 + 0.5 * i + np.random.randn() * 2 for i in range(100)]

    analyzer = TimeSeriesAnalyzer(data)
    trend = analyzer.detect_trend()

    print("Time series with upward trend")
    print(f"Direction: {trend['direction']}")
    print(f"Slope: {trend['slope']:.4f}")
    print(f"R-squared: {trend['r_squared']:.4f}")
    print(f"Strength: {trend['strength']}")
    print()


def demo_seasonality():
    """Demonstrate seasonality detection"""

    print("=" * 60)
    print("TIME SERIES - SEASONALITY DETECTION DEMO")
    print("=" * 60)
    print()

    # Create data with seasonality (period=12)
    np.random.seed(42)
    seasonal_pattern = [0, 2, 4, 6, 4, 2, 0, -2, -4, -6, -4, -2]
    data = []
    for i in range(120):
        trend = 0.1 * i
        seasonal = seasonal_pattern[i % 12]
        noise = np.random.randn()
        data.append(trend + seasonal + noise)

    analyzer = TimeSeriesAnalyzer(data)
    seasonality = analyzer.detect_seasonality()

    print("Time series with monthly seasonality")
    print(f"Has seasonality: {seasonality['has_seasonality']}")
    print(f"Period: {seasonality['period']}")
    print(f"Strength: {seasonality['strength']:.4f}")
    print(f"Pattern: {[f'{x:.2f}' for x in seasonality['seasonal_pattern'][:6]]}...")
    print()


def demo_forecasting():
    """Demonstrate forecasting"""

    print("=" * 60)
    print("TIME SERIES - FORECASTING DEMO")
    print("=" * 60)
    print()

    # Create realistic data (trend + seasonality + noise)
    np.random.seed(42)
    data = []
    for i in range(50):
        trend = 100 + 2 * i
        seasonal = 10 * np.sin(2 * np.pi * i / 12)
        noise = np.random.randn() * 5
        data.append(trend + seasonal + noise)

    analyzer = TimeSeriesAnalyzer(data)

    print(f"Historical data: {len(data)} points")
    print(f"Last 5 values: {[f'{x:.1f}' for x in data[-5:]]}")
    print()

    # Auto forecast
    print("Running auto-forecast (selects best method)...")
    forecast = analyzer.auto_forecast(steps=10)

    print(f"Best method: {forecast.method}")
    print(f"Training MAE: {forecast.metrics['mae']:.2f}")
    print(f"Forecast (next 10 steps): {[f'{x:.1f}' for x in forecast.predictions]}")
    print()


def demo_anomaly_detection():
    """Demonstrate anomaly detection"""

    print("=" * 60)
    print("TIME SERIES - ANOMALY DETECTION DEMO")
    print("=" * 60)
    print()

    # Create data with anomalies
    np.random.seed(42)
    data = [50 + np.random.randn() * 5 for _ in range(100)]

    # Insert anomalies
    data[20] = 80  # Spike
    data[50] = 20  # Dip
    data[75] = 90  # Spike

    analyzer = TimeSeriesAnalyzer(data)
    anomalies = analyzer.detect_anomalies(threshold=3.0)

    print(f"Data points: {len(data)}")
    print(f"Anomalies detected: {len(anomalies)}")
    print(f"Anomaly indices: {anomalies}")
    print(f"Anomaly values: {[f'{data[i]:.1f}' for i in anomalies]}")
    print()


def demo():
    """Run all time series demos"""

    demo_trend_detection()
    demo_seasonality()
    demo_forecasting()
    demo_anomaly_detection()

    print("=" * 60)
    print("TIME SERIES FORECASTING DEMO COMPLETE")
    print("=" * 60)
    print()
    print("Demonstrated:")
    print("1. Trend detection (direction, strength)")
    print("2. Seasonality detection (period, pattern)")
    print("3. Multiple forecasting methods")
    print("4. Anomaly detection")
    print()
    print("Applications for Consciousness Revolution:")
    print("- User engagement trends")
    print("- Consciousness progression tracking")
    print("- Usage pattern prediction")
    print("- Anomaly detection (unusual behavior)")
    print()


if __name__ == "__main__":
    demo()
