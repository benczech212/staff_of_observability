from prometheus_client import Gauge, start_http_server
import time
import board
import busio
from adafruit_bno08x import (
    BNO_REPORT_ACCELEROMETER,
    BNO_REPORT_GYROSCOPE,
    BNO_REPORT_MAGNETOMETER,
    BNO_REPORT_ROTATION_VECTOR,
    BNO_REPORT_ACTIVITY_CLASSIFIER,
    BNO_REPORT_GAME_ROTATION_VECTOR,
    BNO_REPORT_GEOMAGNETIC_ROTATION_VECTOR,
    BNO_REPORT_STEP_COUNTER,
    BNO_REPORT_GRAVITY,
    BNO_REPORT_LINEAR_ACCELERATION,
    BNO_REPORT_GYRO_INTEGRATED_ROTATION_VECTOR,
    BNO_REPORT_RAW_ACCELEROMETER,
    BNO_REPORT_RAW_GYROSCOPE,
    BNO_REPORT_RAW_MAGNETOMETER,
    BNO_REPORT_SHAKE_DETECTOR,
)
from adafruit_bno08x.i2c import BNO08X_I2C


class BNO08X_Sensor:
    def __init__(self, instance_name="BNO08X"):
        self.instance_name = instance_name
        try:
            i2c = busio.I2C(board.SCL, board.SDA, frequency=400000)
            self.sensor = BNO08X_I2C(i2c)

            # Enable all features
            features = [
                BNO_REPORT_ACCELEROMETER,
                BNO_REPORT_GYROSCOPE,
                BNO_REPORT_MAGNETOMETER,
                BNO_REPORT_ROTATION_VECTOR,
                BNO_REPORT_ACTIVITY_CLASSIFIER,
                BNO_REPORT_GAME_ROTATION_VECTOR,
                BNO_REPORT_GEOMAGNETIC_ROTATION_VECTOR,
                BNO_REPORT_STEP_COUNTER,
                BNO_REPORT_GRAVITY,
                BNO_REPORT_LINEAR_ACCELERATION,
                BNO_REPORT_GYRO_INTEGRATED_ROTATION_VECTOR,
                BNO_REPORT_RAW_ACCELEROMETER,
                BNO_REPORT_RAW_GYROSCOPE,
                BNO_REPORT_RAW_MAGNETOMETER,
                BNO_REPORT_SHAKE_DETECTOR,
            ]

            for feature in features:
                self.sensor.enable_feature(feature)

        except Exception as e:
            print(f"Error initializing BNO08X sensor: {e}")
            self.sensor = None

        # Labels and Prometheus metrics
        self.labels = {'sensor': 'BNO08X', 'instance': instance_name}
        self.metrics = {
            'acceleration': Gauge(
                'sensor_acceleration',
                'Acceleration (m/s^2)',
                list(self.labels.keys()) + ['axis']
            ),
            'gyroscope': Gauge(
                'sensor_gyroscope',
                'Gyroscope rotation (rad/s)',
                list(self.labels.keys()) + ['axis']
            ),
            'magnetometer': Gauge(
                'sensor_magnetic_field',
                'Magnetic field (microteslas)',
                list(self.labels.keys()) + ['axis']
            ),
            'gravity': Gauge(
                'sensor_gravity',
                'Gravity vector (m/s^2)',
                list(self.labels.keys()) + ['axis']
            ),
            'linear_acceleration': Gauge(
                'sensor_linear_acceleration',
                'Linear acceleration (m/s^2)',
                list(self.labels.keys()) + ['axis']
            ),
            'rotation_vector': Gauge(
                'sensor_rotation_vector',
                'Rotation vector quaternion',
                list(self.labels.keys()) + ['component']
            ),
            'activity_classifier': Gauge(
                'sensor_activity_classifier',
                'Most likely activity classifier output',
                list(self.labels.keys())
            ),
            'game_rotation_vector': Gauge(
                'sensor_game_rotation_vector',
                'Game rotation vector quaternion',
                list(self.labels.keys()) + ['component']
            ),
            'geomagnetic_rotation_vector': Gauge(
                'sensor_geomagnetic_rotation_vector',
                'Geomagnetic rotation vector quaternion',
                list(self.labels.keys()) + ['component']
            ),
            'step_counter': Gauge(
                'sensor_step_counter',
                'Number of steps counted',
                list(self.labels.keys())
            ),
            'gyro_integrated_rotation_vector': Gauge(
                'sensor_gyro_integrated_rotation_vector',
                'Gyro-integrated rotation vector quaternion',
                list(self.labels.keys()) + ['component']
            ),
            'raw_acceleration': Gauge(
                'sensor_raw_acceleration',
                'Raw accelerometer data (m/s^2)',
                list(self.labels.keys()) + ['axis']
            ),
            'raw_gyroscope': Gauge(
                'sensor_raw_gyroscope',
                'Raw gyroscope data (rad/s)',
                list(self.labels.keys()) + ['axis']
            ),
            'raw_magnetometer': Gauge(
                'sensor_raw_magnetometer',
                'Raw magnetometer data (microteslas)',
                list(self.labels.keys()) + ['axis']
            ),
            'shake_detector': Gauge(
                'sensor_shake_detector',
                'Shake detector status (1 = shake detected, 0 = no shake)',
                list(self.labels.keys())
            ),
        }
        self.sensor_values = {}

    def update_metrics(self):
        """Update Prometheus metrics for BNO08X."""
        if not self.sensor:
            print("Sensor not initialized. Skipping metrics update.")
            return

        try:
            # Update acceleration
            acc = self.sensor.acceleration or (0, 0, 0)
            for axis, value in zip(['x', 'y', 'z'], acc):
                self.metrics['acceleration'].labels(axis=axis, **self.labels).set(value)

            # Update gyroscope
            gyro = self.sensor.gyro or (0, 0, 0)
            for axis, value in zip(['x', 'y', 'z'], gyro):
                self.metrics['gyroscope'].labels(axis=axis, **self.labels).set(value)

            # Update magnetometer
            mag = self.sensor.magnetic or (0, 0, 0)
            for axis, value in zip(['x', 'y', 'z'], mag):
                self.metrics['magnetometer'].labels(axis=axis, **self.labels).set(value)

            # Update gravity
            gravity = self.sensor.gravity or (0, 0, 0)
            for axis, value in zip(['x', 'y', 'z'], gravity):
                self.metrics['gravity'].labels(axis=axis, **self.labels).set(value)

            # Update linear acceleration
            lin_acc = self.sensor.linear_acceleration or (0, 0, 0)
            for axis, value in zip(['x', 'y', 'z'], lin_acc):
                self.metrics['linear_acceleration'].labels(axis=axis, **self.labels).set(value)

            # Update rotation vector quaternion
            quaternion = self.sensor.quaternion or (0, 0, 0, 0)
            for component, value in zip(['i', 'j', 'k', 'real'], quaternion):
                self.metrics['rotation_vector'].labels(component=component, **self.labels).set(value)

            # Update activity classifier
            activity = self.sensor.activity_classification.get('most_likely', 'unknown')
            self.metrics['activity_classifier'].labels(**self.labels).set(activity)

            # Update game rotation vector quaternion
            game_quat = self.sensor.game_rotation_vector or (0, 0, 0, 0)
            for component, value in zip(['i', 'j', 'k', 'real'], game_quat):
                self.metrics['game_rotation_vector'].labels(component=component, **self.labels).set(value)

            # Update geomagnetic rotation vector quaternion
            geo_quat = self.sensor.geomagnetic_rotation_vector or (0, 0, 0, 0)
            for component, value in zip(['i', 'j', 'k', 'real'], geo_quat):
                self.metrics['geomagnetic_rotation_vector'].labels(component=component, **self.labels).set(value)

            # Update step counter
            steps = self.sensor.step_count or 0
            self.metrics['step_counter'].labels(**self.labels).set(steps)

            # Update gyro-integrated rotation vector quaternion
            gyro_quat = self.sensor.gyro_integrated_rotation_vector or (0, 0, 0, 0)
            for component, value in zip(['i', 'j', 'k', 'real'], gyro_quat):
                self.metrics['gyro_integrated_rotation_vector'].labels(component=component, **self.labels).set(value)

            # Update raw acceleration
            raw_acc = self.sensor.raw_acceleration or (0, 0, 0)
            for axis, value in zip(['x', 'y', 'z'], raw_acc):
                self.metrics['raw_acceleration'].labels(axis=axis, **self.labels).set(value)

            # Update raw gyroscope
            raw_gyro = self.sensor.raw_gyro or (0, 0, 0)
            for axis, value in zip(['x', 'y', 'z'], raw_gyro):
                self.metrics['raw_gyroscope'].labels(axis=axis, **self.labels).set(value)

            # Update raw magnetometer
            raw_mag = self.sensor.raw_magnetic or (0, 0, 0)
            for axis, value in zip(['x', 'y', 'z'], raw_mag):
                self.metrics['raw_magnetometer'].labels(axis=axis, **self.labels).set(value)

            # Update shake detector
            shake = 1 if self.sensor.shake_detected else 0
            self.metrics['shake_detector'].labels(**self.labels).set(shake)


            self.sensor_values = {
                "acceleration": acc,
                "gyro": gyro,
                "magnetometer": mag,
                "gravity": gravity,
                "linear_acceleration": lin_acc,
                "rotation_vector": quaternion,
                "activity_classifier": activity,
                "game_rotation_vector": game_quat,
                "geomagnetic_rotation_vector": geo_quat,
                "step_counter": steps,
                "gyro_integrated_rotation_vector": gyro_quat,
                "raw_acceleration": raw_acc,
                "raw_gyro": raw_gyro,
                "raw_magnetometer": raw_mag,
                "shake_detector": shake,
            }
        except Exception as e:
            print(f"Error updating BNO08X metrics: {e}")