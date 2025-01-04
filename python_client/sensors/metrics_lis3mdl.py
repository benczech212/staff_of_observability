from prometheus_client import Gauge
import board
import adafruit_lis3mdl
from math import atan2, degrees

class LIS3MDL_Sensor:
    def __init__(self):
        # Initialize the sensor
        i2c = board.I2C()
        self.sensor = adafruit_lis3mdl.LIS3MDL(i2c)

        # Labels and metrics
        self.labels = {'sensor': 'LIS3MDL', 'sensor_type': 'Magneometer'}
        self.metrics = {
            'heading': Gauge(
                'sensor_heading',
                'Compass heading (degrees from 0 to 360)',
                list(self.labels.keys())
            ).labels(**self.labels),
            'magnetic_field': Gauge(
                'sensor_magnetic_field',
                'Magnetic field strength (uT)',
                list(self.labels.keys()) + ['axis']
            )
        }

    def vector_2_degrees(self, x, y):
        """Convert a 2D vector into degrees."""
        angle = degrees(atan2(y, x))
        return angle + 360 if angle < 0 else angle

    def update_metrics(self):
        """Update Prometheus metrics for LIS3MDL."""
        try:
            # Get magnetic field data
            mag_x, mag_y, mag_z = self.sensor.magnetic

            # Calculate heading
            heading = self.vector_2_degrees(mag_x, mag_y)

            # Update metrics
            self.metrics['heading'].set(heading)
            self.metrics['magnetic_field'].labels(**self.labels, axis='x').set(mag_x)
            self.metrics['magnetic_field'].labels(**self.labels, axis='y').set(mag_y)
            self.metrics['magnetic_field'].labels(**self.labels, axis='z').set(mag_z)
        except Exception as e:
            print(f"Error updating LIS3MDL metrics: {e}")
