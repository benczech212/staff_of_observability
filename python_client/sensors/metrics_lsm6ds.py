from app.metrics_manager import create_metrics
from adafruit_lsm6ds.lsm6ds3 import LSM6DS3
import board

class LSM6DS3_Sensor:
    def __init__(self):
        # Initialize the sensor
        i2c = board.I2C()
        self.sensor = LSM6DS3(i2c)
        self.sensor.pedometer_enable = True

        # Labels and metrics
        self.labels = {'sensor': 'LSM6DS3', 'sensor_type': 'IMU'}
        self.metrics = {
            'acceleration': create_metrics(self.labels, [
                {'name': 'sensor_acceleration', 'description': 'Acceleration (m/s^2)', 'metric_type': 'gauge', 'group': 'acceleration', 'label_keys': ['orientation']},
            ]),
            'gyroscope': create_metrics(self.labels, [
                {'name': 'sensor_gyroscope', 'description': 'Gyroscope (radians/s)', 'metric_type': 'gauge', 'group': 'gyroscope', 'label_keys': ['orientation']},
            ]),
            'temperature': create_metrics(self.labels, [
                {'name': 'sensor_temperature', 'description': 'Sensor temperature (Celsius)', 'metric_type': 'gauge', 'group': 'environment'},
            ]),
            'step_count': create_metrics(self.labels, [
                {'name': 'sensor_step_count', 'description': 'Total number of steps counted by the pedometer', 'metric_type': 'counter', 'group': 'pedometer'},
            ]),
        }

    def update_metrics(self):
        acc_x, acc_y, acc_z = self.sensor.acceleration
        gyro_x, gyro_y, gyro_z = self.sensor.gyro
        temperature = self.sensor.temperature
        step_count = self.sensor.pedometer_steps

        self.metrics['acceleration']['x'].labels(orientation='x').set(acc_x)
        self.metrics['acceleration']['y'].labels(orientation='y').set(acc_y)
        self.metrics['acceleration']['z'].labels(orientation='z').set(acc_z)

        self.metrics['gyroscope']['x'].labels(orientation='x').set(gyro_x)
        self.metrics['gyroscope']['y'].labels(orientation='y').set(gyro_y)
        self.metrics['gyroscope']['z'].labels(orientation='z').set(gyro_z)

        self.metrics['temperature'].set(temperature)
        self.metrics['step_count'].inc(step_count)
