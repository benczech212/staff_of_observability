from prometheus_client import Gauge, Counter
from app.metrics_manager import create_metrics

# Labels for LSM6DS3
LSM6DS3_LABELS = {'sensor': 'LSM6DS3', 'sensor_type': 'IMU'}

# Define metrics
LSM6DS3_METRIC_DEFINITIONS = [
    {'name': 'sensor_acceleration', 'description': 'Acceleration (m/s^2)', 'metric_type': 'gauge', 'group': 'acceleration', 'label_keys': ['orientation']},
    {'name': 'sensor_gyroscope', 'description': 'Gyroscope (radians/s)', 'metric_type': 'gauge', 'group': 'gyroscope', 'label_keys': ['orientation']},
    {'name': 'sensor_temperature', 'description': 'Sensor temperature (Celsius)', 'metric_type': 'gauge', 'group': 'environment'},
    {'name': 'sensor_step_count', 'description': 'Total number of steps counted by the pedometer', 'metric_type': 'counter', 'group': 'pedometer'},
]

# Create metrics
LSM6DS3_METRICS = {
    'acceleration': {
        'x': Gauge('sensor_acceleration', 'Acceleration (m/s^2)', list(LSM6DS3_LABELS.keys()) + ['orientation']).labels(**LSM6DS3_LABELS, orientation='x'),
        'y': Gauge('sensor_acceleration', 'Acceleration (m/s^2)', list(LSM6DS3_LABELS.keys()) + ['orientation']).labels(**LSM6DS3_LABELS, orientation='y'),
        'z': Gauge('sensor_acceleration', 'Acceleration (m/s^2)', list(LSM6DS3_LABELS.keys()) + ['orientation']).labels(**LSM6DS3_LABELS, orientation='z'),
    },
    'gyroscope': {
        'x': Gauge('sensor_gyroscope', 'Gyroscope (radians/s)', list(LSM6DS3_LABELS.keys()) + ['orientation']).labels(**LSM6DS3_LABELS, orientation='x'),
        'y': Gauge('sensor_gyroscope', 'Gyroscope (radians/s)', list(LSM6DS3_LABELS.keys()) + ['orientation']).labels(**LSM6DS3_LABELS, orientation='y'),
        'z': Gauge('sensor_gyroscope', 'Gyroscope (radians/s)', list(LSM6DS3_LABELS.keys()) + ['orientation']).labels(**LSM6DS3_LABELS, orientation='z'),
    },
    'temperature': Gauge('sensor_temperature', 'Sensor temperature (Celsius)', list(LSM6DS3_LABELS.keys())).labels(**LSM6DS3_LABELS),
    'step_count': Counter('sensor_step_count', 'Total number of steps counted by the pedometer', list(LSM6DS3_LABELS.keys())).labels(**LSM6DS3_LABELS),
}

# Metric update functions
def update_acceleration(x, y, z):
    LSM6DS3_METRICS['acceleration']['x'].set(x)
    LSM6DS3_METRICS['acceleration']['y'].set(y)
    LSM6DS3_METRICS['acceleration']['z'].set(z)

def update_gyroscope(x, y, z):
    LSM6DS3_METRICS['gyroscope']['x'].set(x)
    LSM6DS3_METRICS['gyroscope']['y'].set(y)
    LSM6DS3_METRICS['gyroscope']['z'].set(z)

def update_temperature(temp):
    LSM6DS3_METRICS['temperature'].set(temp)

def increment_step_count(steps):
    LSM6DS3_METRICS['step_count'].inc(steps)
