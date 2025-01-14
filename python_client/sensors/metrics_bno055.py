from prometheus_client import Gauge
import time
import board
import adafruit_bno055

class BNO055_Sensor:
    def __init__(self, instance_name="BNO055"):
        # Initialize the sensor
        i2c = board.I2C()
        self.sensor = adafruit_bno055.BNO055_I2C(i2c)
        

        # Labels and metrics
        self.labels = {'sensor': 'BNO055', 'sensor_type': 'IMU', 'instance': instance_name}
        self.metrics = {
            'temperature': Gauge(
                'sensor_temperature_celsius',
                'Temperature in degrees Celsius',
                list(self.labels.keys())
            ).labels(**self.labels),
            'acceleration': Gauge(
                'sensor_acceleration',
                'Acceleration (m/s^2)',
                list(self.labels.keys()) + ['axis']
            ),
            'magnetic': Gauge(
                'sensor_magnetic_field',
                'Magnetic field (microteslas)',
                list(self.labels.keys()) + ['axis']
            ),
            'gyroscope': Gauge(
                'sensor_gyroscope',
                'Gyroscope rotation (rad/sec)',
                list(self.labels.keys()) + ['axis']
            ),
            'euler': Gauge(
                'sensor_euler_angle',
                'Euler angle (degrees)',
                list(self.labels.keys()) + ['axis']
            ),
            'quaternion': Gauge(
                'sensor_quaternion',
                'Quaternion components',
                list(self.labels.keys()) + ['component']
            ),
            'linear_acceleration': Gauge(
                'sensor_linear_acceleration',
                'Linear acceleration (m/s^2)',
                list(self.labels.keys()) + ['axis']
            ),
            'gravity': Gauge(
                'sensor_gravity',
                'Gravity (m/s^2)',
                list(self.labels.keys()) + ['axis']
            ),
        }

    def update_metrics(self):
        """Update Prometheus metrics for BNO055."""
        try:
            # Update temperature
            self.metrics['temperature'].set(self.sensor.temperature)

            # Update acceleration
            acc = self.sensor.acceleration or (0, 0, 0)
            for axis, value in zip(['x', 'y', 'z'], acc):
                self.metrics['acceleration'].labels(axis=axis, **self.labels).set(value)

            # Update magnetic field
            mag = self.sensor.magnetic or (0, 0, 0)
            for axis, value in zip(['x', 'y', 'z'], mag):
                self.metrics['magnetic'].labels(axis=axis, **self.labels).set(value)

            # Update gyroscope
            gyro = self.sensor.gyro or (0, 0, 0)
            for axis, value in zip(['x', 'y', 'z'], gyro):
                self.metrics['gyroscope'].labels(axis=axis, **self.labels).set(value)

            # Update Euler angles
            euler = self.sensor.euler or (0, 0, 0)
            for axis, value in zip(['x', 'y', 'z'], euler):
                self.metrics['euler'].labels(axis=axis, **self.labels).set(value)

            # Update quaternion
            quaternion = self.sensor.quaternion or (0, 0, 0, 0)
            for component, value in zip(['w', 'x', 'y', 'z'], quaternion):
                self.metrics['quaternion'].labels(component=component, **self.labels).set(value)

            # Update linear acceleration
            lin_acc = self.sensor.linear_acceleration or (0, 0, 0)
            for axis, value in zip(['x', 'y', 'z'], lin_acc):
                self.metrics['linear_acceleration'].labels(axis=axis, **self.labels).set(value)

            # Update gravity
            gravity = self.sensor.gravity or (0, 0, 0)
            for axis, value in zip(['x', 'y', 'z'], gravity):
                self.metrics['gravity'].labels(axis=axis, **self.labels).set(value)

        except Exception as e:
            print(f"Error updating BNO055 metrics: {e}")

# Example usage
if __name__ == "__main__":
    sensor = BNO055_Sensor()
    while True:
        sensor.update_metrics()
        time.sleep(1)
