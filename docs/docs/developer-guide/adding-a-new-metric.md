---
sidebar_position: 1
---

# Adding a New Metric

This guide will walk you through the process of adding a custom evaluation metric to Evalap.

## Understanding Metrics in Evalap

Evalap uses metrics to evaluate model outputs against reference answers. Each metric is implemented as a Python class that inherits from a base metric interface and provides specific evaluation logic.

## Prerequisites

Before adding a new metric, ensure you have:

- A local development environment set up
- Understanding of the metric you want to implement
- Basic knowledge of Python

## Step 1: Create a New Metric Class

Create a new Python file in the metrics directory with your metric implementation:

```python
# evalap/metrics/my_custom_metric.py

from evalap.metrics.base import BaseMetric
from typing import Any, Dict, List, Union

class MyCustomMetric(BaseMetric):
    """A custom metric for evaluating model outputs.
    
    This metric [describe what your metric does].
    """
    
    name = "my_custom_metric"  # Unique identifier for the metric
    display_name = "My Custom Metric"  # Human-readable name
    description = "A custom metric that evaluates [description]"  # Detailed description
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Initialize any specific parameters for your metric
        self.parameter1 = kwargs.get("parameter1", default_value)
        self.parameter2 = kwargs.get("parameter2", default_value)
    
    def compute(self, references: List[str], predictions: List[str]) -> Dict[str, Any]:
        """Compute the metric score between references and predictions.
        
        Args:
            references: List of reference answers
            predictions: List of model-generated answers
            
        Returns:
            Dictionary containing the metric scores
        """
        # Implement your metric computation logic here
        scores = []
        for ref, pred in zip(references, predictions):
            # Calculate individual score
            score = self._calculate_score(ref, pred)
            scores.append(score)
        
        # Return results
        return {
            "score": sum(scores) / len(scores) if scores else 0,  # Average score
            "individual_scores": scores,  # Individual scores for each sample
            # Add any additional metrics or statistics
        }
    
    def _calculate_score(self, reference: str, prediction: str) -> float:
        """Calculate the score for a single reference-prediction pair."""
        # Implement your specific scoring logic here
        # Example:
        # 1. Preprocess reference and prediction
        # 2. Calculate similarity or other relevant measure
        # 3. Return a score (typically between 0 and 1)
        
        # Placeholder implementation
        return 0.0
```

## Step 2: Register Your Metric

Register your new metric in the metrics registry:

```python
# evalap/metrics/__init__.py

from evalap.metrics.accuracy import AccuracyMetric
from evalap.metrics.f1_score import F1ScoreMetric
# ... other existing imports
from evalap.metrics.my_custom_metric import MyCustomMetric

# Update the METRICS dictionary
METRICS = {
    "accuracy": AccuracyMetric,
    "f1_score": F1ScoreMetric,
    # ... other existing metrics
    "my_custom_metric": MyCustomMetric,
}
```

## Step 3: Add Tests for Your Metric

Create tests to ensure your metric works correctly:

```python
# tests/metrics/test_my_custom_metric.py

import unittest
from evalap.metrics.my_custom_metric import MyCustomMetric

class TestMyCustomMetric(unittest.TestCase):
    def setUp(self):
        self.metric = MyCustomMetric()
    
    def test_perfect_match(self):
        references = ["This is a test", "Another test"]
        predictions = ["This is a test", "Another test"]
        result = self.metric.compute(references, predictions)
        self.assertEqual(result["score"], 1.0)  # Perfect match should score 1.0
    
    def test_no_match(self):
        references = ["This is a test", "Another test"]
        predictions = ["Completely different", "Not matching at all"]
        result = self.metric.compute(references, predictions)
        self.assertEqual(result["score"], 0.0)  # No match should score 0.0
    
    def test_partial_match(self):
        references = ["This is a test", "Another test"]
        predictions = ["This is a test", "Different answer"]
        result = self.metric.compute(references, predictions)
        # Partial match should have a score between 0 and 1
        self.assertTrue(0 < result["score"] < 1)

if __name__ == "__main__":
    unittest.main()
```

## Step 4: Document Your Metric

Add documentation for your metric in the API reference:

```markdown
# docs/docs/api-reference/metrics.md

## MyCustomMetric

**Identifier**: `my_custom_metric`

**Description**: A custom metric that evaluates [description]

### Parameters

- `parameter1` (type): Description of parameter1. Default: `default_value`
- `parameter2` (type): Description of parameter2. Default: `default_value`

### Example Usage

```python
from evalap.metrics import METRICS

my_metric = METRICS["my_custom_metric"](parameter1=value1, parameter2=value2)
result = my_metric.compute(references, predictions)
print(f"Score: {result['score']}")
```
```

## Step 5: Test Your Metric in the Platform

1. Restart the Evalap service to load your new metric
2. Create a new experiment using your custom metric
3. Verify that the metric works as expected

## Advanced Customization

### Metric Parameters

You can make your metric configurable by accepting parameters in the constructor:

```python
def __init__(self, threshold=0.5, case_sensitive=True, **kwargs):
    super().__init__(**kwargs)
    self.threshold = threshold
    self.case_sensitive = case_sensitive
```

### Handling Edge Cases

Ensure your metric handles edge cases gracefully:

- Empty strings
- Very long inputs
- Special characters
- Different languages
- Null or missing values

## Conclusion

By following these steps, you've successfully added a custom metric to Evalap. Your metric can now be used in experiments to evaluate model performance according to your specific criteria.