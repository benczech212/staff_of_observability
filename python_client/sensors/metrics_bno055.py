from prometheus_client import Gauge
import time
import board
import adafruit_bno055
from math import atan2, degrees

class BNO055_Sensor:
    def __init__(self, instance_name="BNO055"):
        self.instance_name = instance_name
        try:
        # Initialize the sensor
            i2c = board.I2C()
            self.sensor = adafruit_bno055.BNO055_I2C(i2c)    
        except Exception as e:
            print(f"Error initializing BNO055 sensor: {e}")    
            self.sensor = None


        
        # Labels and metrics
        self.labels = {'sensor': 'BNO055', 'sensor_type': 'IMU', 'instance': instance_name}
        self.metrics = {
            # 'temperature': Gauge(
            #     'sensor_temperature',
            #     'Temperature in degrees Celsius',
            #     list(self.labels.keys())
            # ).labels(**self.labels),
            'acceleration': Gauge(
                'sensor_acceleration',
                'Acceleration (m/s^2)',
                list(self.labels.keys()) + ['axis', 'unit']
            ),
            'magnetic': Gauge(
                'sensor_magnetic_field',
                'Magnetic field (microteslas)',
                list(self.labels.keys()) + ['axis', 'unit']
            ),
            'heading': Gauge(
                'sensor_heading',
                'Heading (degrees)',
                list(self.labels.keys()) + ['unit']
            ),
            'gyroscope': Gauge(
                'sensor_gyroscope',
                'Gyroscope rotation (rad/sec)',
                list(self.labels.keys()) + ['axis', 'unit']
            ),
            'euler': Gauge(
                'sensor_euler_angle',
                'Euler angle (degrees)',
                list(self.labels.keys()) + ['axis', 'unit']
            ),
            'quaternion': Gauge(
                'sensor_quaternion',
                'Quaternion components',
                list(self.labels.keys()) + ['component']
            ),
            'linear_acceleration': Gauge(
                'sensor_linear_acceleration',
                'Linear acceleration (m/s^2)',
                list(self.labels.keys()) + ['axis', 'unit']
            ),
            'gravity': Gauge(
                'sensor_gravity',
                'Gravity (m/s^2)',
                list(self.labels.keys()) + ['axis', 'unit']
            ),
        }
        sensor_values = {}

    def vector_2_degrees(self, x, y):
        """Convert a 2D vector into degrees."""
        angle = degrees(atan2(y, x))
        return angle + 360 if angle < 0 else angle

    def update_metrics(self):
        """Update Prometheus metrics for BNO055."""
        try:
            # Update temperature
            # self.metrics['temperature'].set(self.sensor.temperature)

            # Update acceleration
            acc = self.sensor.acceleration or (0, 0, 0)
            acc = (0,0,0) if acc == (None, None, None) else acc
            for axis, value in zip(['x', 'y', 'z'], acc):
                self.metrics['acceleration'].labels(axis=axis, **self.labels,unit="m/s^2").set(value)

            # Update magnetic field
            mag = self.sensor.magnetic or (0, 0, 0)
            mag = (0, 0, 0) if mag == (None, None, None) else mag
            for axis, value in zip(['x', 'y', 'z'], mag):
                self.metrics['magnetic'].labels(axis=axis, **self.labels,unit="MicroTesla").set(value)

            heading = self.vector_2_degrees(mag[0], mag[1])
            self.metrics['heading'].labels(**self.labels,unit="Degrees").set(heading)

            # Update gyroscope
            gyro = self.sensor.gyro or (0, 0, 0)
            gyro = (0, 0, 0) if gyro == (None, None, None) else gyro
            for axis, value in zip(['x', 'y', 'z'], gyro):
                self.metrics['gyroscope'].labels(axis=axis, **self.labels,unit="rad/s").set(value)

            # Update Euler angles
            euler = self.sensor.euler or (0, 0, 0)
            euler = (0, 0, 0) if euler == (None, None, None) else euler
            for axis, value in zip(['x', 'y', 'z'], euler):
                self.metrics['euler'].labels(axis=axis, **self.labels,unit="Degrees").set(value)

            # Update quaternion
            quaternion = self.sensor.quaternion or (0.0, 0.0, 0.0, 0.0)
            quaternion = (0.0, 0.0, 0.0, 0.0) if quaternion == (None, None, None, None) else quaternion
            for component, value in zip(['w', 'x', 'y', 'z'], quaternion):
                self.metrics['quaternion'].labels(component=component, **self.labels).set(value)

            # Update linear acceleration
            lin_acc = self.sensor.linear_acceleration or (0, 0, 0)
            lin_acc = (0, 0, 0) if lin_acc == (None, None, None) else lin_acc
            for axis, value in zip(['x', 'y', 'z'], lin_acc):
                self.metrics['linear_acceleration'].labels(axis=axis, **self.labels,unit="m/s^2").set(value)

            # Update gravity
            gravity = self.sensor.gravity or (0, 0, 0)
            gravity = (0, 0, 0) if gravity == (None, None, None) else gravity
            for axis, value in zip(['x', 'y', 'z'], gravity):
                self.metrics['gravity'].labels(axis=axis, **self.labels,unit="m/s^2").set(value)
            
            self.sensor_values = {
                'acceleration': {'x': acc[0], 'y': acc[1], 'z': acc[2]},
                'magnetic': {'x': mag[0], 'y': mag[1], 'z': mag[2]},
                'heading': heading,
                'gyroscope': {'x': gyro[0], 'y': gyro[1], 'z': gyro[2]},
                'euler': {'x': euler[0], 'y': euler[1], 'z': euler[2]},
                'quaternion': {'w': quaternion[0], 'x': quaternion[1], 'y': quaternion[2], 'z': quaternion[3]},
                'linear_acceleration': {'x': lin_acc[0], 'y': lin_acc[1], 'z': lin_acc[2]},
                'gravity': {'x': gravity[0], 'y': gravity[1], 'z': gravity[2]}
            }
        except Exception as e:
            print(f"Error updating BNO055 metrics: {e}")

# Example usage
if __name__ == "__main__":
    sensor = BNO055_Sensor()
    while True:
        sensor.update_metrics()
        # time.sleep(1)
