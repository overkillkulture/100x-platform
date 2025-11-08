"""MODULE #43: ML PIPELINE - End-to-end ML workflow automation"""
import numpy as np
from typing import Callable, List, Dict, Any

class MLPipeline:
    def __init__(self, name: str):
        self.name = name
        self.steps: List[Dict] = []
        self.data = None

    def add_preprocessing(self, func: Callable, name: str):
        """Add preprocessing step"""
        self.steps.append({'type': 'preprocess', 'func': func, 'name': name})
        return self

    def add_feature_engineering(self, func: Callable, name: str):
        """Add feature engineering step"""
        self.steps.append({'type': 'features', 'func': func, 'name': name})
        return self

    def add_model(self, model: Any, name: str):
        """Add model training step"""
        self.steps.append({'type': 'model', 'model': model, 'name': name})
        return self

    def fit(self, X, y):
        """Train pipeline"""
        print(f"Training ML Pipeline: {self.name}")
        current_X = X

        for step in self.steps:
            print(f"  → {step['name']}")
            if step['type'] in ['preprocess', 'features']:
                current_X = step['func'](current_X)
            elif step['type'] == 'model':
                if hasattr(step['model'], 'fit'):
                    step['model'].fit(current_X, y)

        self.data = current_X
        print("  ✅ Training complete")
        return self

    def predict(self, X):
        """Make predictions"""
        current_X = X

        for step in self.steps:
            if step['type'] in ['preprocess', 'features']:
                current_X = step['func'](current_X)
            elif step['type'] == 'model':
                if hasattr(step['model'], 'predict'):
                    return step['model'].predict(current_X)

        return current_X

    def evaluate(self, X, y) -> Dict[str, float]:
        """Evaluate pipeline"""
        predictions = self.predict(X)

        # Simple metrics
        if isinstance(predictions, np.ndarray):
            accuracy = np.mean(predictions == y) if len(predictions) == len(y) else 0
            return {'accuracy': accuracy}

        return {'status': 'evaluated'}

if __name__ == "__main__":
    # Demo with simple transformations
    pipeline = MLPipeline("demo_pipeline")
    pipeline.add_preprocessing(lambda x: x * 2, "double_values")
    pipeline.add_feature_engineering(lambda x: x + 1, "add_one")

    X = np.array([[1, 2], [3, 4]])
    y = np.array([0, 1])

    pipeline.fit(X, y)
    print("✅ ML Pipeline working!")
