from prometheus_client import Gauge, Counter

def create_metrics(sensor_labels, metric_definitions):
    """
    Dynamically creates metrics based on definitions and sensor labels.

    Args:
        sensor_labels (dict): Labels specific to the sensor.
        metric_definitions (list): List of metric definitions.

    Returns:
        dict: Dictionary of Prometheus metrics.
    """
    metrics = {}
    for metric_def in metric_definitions:
        full_labels = {**sensor_labels, 'metric_group': metric_def['group']}
        label_keys = list(full_labels.keys())

        if metric_def['metric_type'] == 'gauge':
            metrics[metric_def['name']] = Gauge(
                metric_def['name'],
                metric_def['description'],
                label_keys,
            ).labels(**full_labels)
        elif metric_def['metric_type'] == 'counter':
            metrics[metric_def['name']] = Counter(
                metric_def['name'],
                metric_def['description'],
                label_keys,
            ).labels(**full_labels)
    return metrics
