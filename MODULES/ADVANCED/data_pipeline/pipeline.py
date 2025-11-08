"""
MODULE #31: DATA PIPELINE
Built: 2025-11-08
ETL (Extract, Transform, Load) system for data processing.
"""

from typing import List, Dict, Any, Callable
import json
import time


class DataPipeline:
    """ETL pipeline for data processing"""

    def __init__(self, name: str):
        self.name = name
        self.stages: List[Callable] = []
        self.metrics = {'processed': 0, 'errors': 0, 'duration': 0}

    def add_stage(self, func: Callable):
        """Add processing stage"""
        self.stages.append(func)
        return self

    def process(self, data: List[Dict]) -> List[Dict]:
        """Process data through pipeline"""
        start = time.time()
        result = data

        for stage in self.stages:
            try:
                result = [stage(item) for item in result]
                self.metrics['processed'] += len(result)
            except Exception as e:
                self.metrics['errors'] += 1
                print(f"Error in stage: {e}")

        self.metrics['duration'] = time.time() - start
        return result


# Demo
if __name__ == "__main__":
    pipeline = DataPipeline("user_data")

    # Add stages
    pipeline.add_stage(lambda x: {**x, 'processed': True})
    pipeline.add_stage(lambda x: {**x, 'score': x.get('value', 0) * 2})

    # Process data
    data = [{'id': 1, 'value': 10}, {'id': 2, 'value': 20}]
    result = pipeline.process(data)

    print(f"Processed: {result}")
    print(f"Metrics: {pipeline.metrics}")
