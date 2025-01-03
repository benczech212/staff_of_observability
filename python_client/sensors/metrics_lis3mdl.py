from prometheus_client import Gauge
from app.metrics_manager import create_metrics

# Labels for LIS3MDL
LIS3MDL_LABELS = {'sensor': 'LIS3MDL', 'sensor_type': 'Compass'}

# Define metrics
LIS3MDL_METRIC_DEFINITIONS = [
    {'name': 'sensor_heading', 'description': 'Compass heading (degrees)', 'metric_type': 'gauge', 'group': 'heading'},
]

# Create metrics for LIS3MDL
LIS3MDL_METRICS = create_metrics(LIS3MDL_LABELS, LIS3MDL_METRIC_DEFINITIONS)

# Metric update function
def update_heading(heading):
    LIS3MDL_METRICS['sensor_heading'].labels(**LIS3MDL_LABELS).set(heading)
