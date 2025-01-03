from prometheus_client import Gauge, Counter

# Labels for LSM6DS3
LSM6DS3_LABELS = {'sensor': 'LSM6DS3', 'sensor_type': 'IMU'}

# Create metrics
LSM6DS3_METRICS = {
    'acceleration': Gauge('sensor_acceleration', 'Acceleration (m/s^2)', list(LSM6DS3_LABELS.keys()) + ['orientation']),
    'gyroscope': Gauge('sensor_gyroscope', 'Gyroscope (radians/s)', list(LSM6DS3_LABELS.keys()) + ['orientation']),
    'temperature': Gauge('sensor_temperature', 'Sensor temperature (Celsius)', list(LSM6DS3_LABELS.keys())),
    'step_count': Counter('sensor_step_count', 'Total number of steps counted by the pedometer', list(LSM6DS3_LABELS.keys())),
}

# Metric update functions
def update_acceleration(x, y, z):
    LSM6DS3_METRICS['acceleration'].labels(**LSM6DS3_LABELS, orientation='x').set(x)
    LSM6DS3_METRICS['acceleration'].labels(**LSM6DS3_LABELS, orientation='y').set(y)
    LSM6DS3_METRICS['acceleration'].labels(**LSM6DS3_LABELS, orientation='z').set(z)

def update_gyroscope(x, y, z):
    LSM6DS3_METRICS['gyroscope'].labels(**LSM6DS3_LABELS, orientation='x').set(x)
    LSM6DS3_METRICS['gyroscope'].labels(**LSM6DS3_LABELS, orientation='y').set(y)
    LSM6DS3_METRICS['gyroscope'].labels(**LSM6DS3_LABELS, orientation='z').set(z)

def update_temperature(temp):
    LSM6DS3_METRICS['temperature'].labels(**LSM6DS3_LABELS).set(temp)

def increment_step_count(steps):
    LSM6DS3_METRICS['step_count'].labels(**LSM6DS3_LABELS).inc(steps)
