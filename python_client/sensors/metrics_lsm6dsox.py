from prometheus_client import Gauge
import board
from adafruit_lsm6ds.lsm6dsox import LSM6DSOX

class LSM6DSOX_Sensor:
    def __init__(self,instance_name="LSM6DSOX"):
        # Initialize the sensor
        try:
            i2c = board.I2C()  # Uses board.SCL and board.SDA
            self.sensor = LSM6DSOX(i2c)
        except Exception as e:
            print(f"Error initializing LSM6DSOX sensor: {e}")
            self.sensor = None
        self.instance_name = instance_name
        # Labels and metrics
        self.base_labels = {'sensor': 'LSM6DSOX','instance_name': instance_name}
        self.metrics = {
            'acceleration': Gauge(
                'sensor_acceleration',
                'Acceleration in m/s^2',
                list(self.base_labels.keys()) + ['axis', 'sensor_type','unit']
            ),
            'gyro': Gauge(
                'sensor_gyro',
                'Gyroscope rotation in radians/s',
                list(self.base_labels.keys()) + ['axis', 'sensor_type','unit']
            )
        }
        self.sensor_values = {}

    def update_metrics(self):
        """Update Prometheus metrics for LSM6DSOX."""
        try:
            # Get sensor readings
            acc_x, acc_y, acc_z = self.sensor.acceleration
            gyro_x, gyro_y, gyro_z = self.sensor.gyro

            self.sensor_values = {
                'acceleration': {'x': acc_x, 'y': acc_y, 'z': acc_z},
                'gyro': {'x': gyro_x, 'y': gyro_y, 'z': gyro_z}
            }
            # Update acceleration metrics with sensor_type = "Accelerometer"
            self.metrics['acceleration'].labels(**self.base_labels, axis='x', sensor_type='Accelerometer',unit="m/s^2").set(acc_x)
            self.metrics['acceleration'].labels(**self.base_labels, axis='y', sensor_type='Accelerometer',unit="m/s^2").set(acc_y)
            self.metrics['acceleration'].labels(**self.base_labels, axis='z', sensor_type='Accelerometer',unit="m/s^2").set(acc_z)

            # Update gyroscope metrics with sensor_type = "Gyroscope"
            self.metrics['gyro'].labels(**self.base_labels, axis='x', sensor_type='Gyroscope',unit="rad/s").set(gyro_x)
            self.metrics['gyro'].labels(**self.base_labels, axis='y', sensor_type='Gyroscope',unit="rad/s").set(gyro_y)
            self.metrics['gyro'].labels(**self.base_labels, axis='z', sensor_type='Gyroscope',unit="rad/s").set(gyro_z)
        except Exception as e:
            print(f"Error updating LSM6DSOX metrics: {e}")
