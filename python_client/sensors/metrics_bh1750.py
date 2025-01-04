from prometheus_client import Gauge
import board
import adafruit_bh1750

class BH1750_Sensor:
    def __init__(self, instance_name="BH1750"):
        # Initialize the sensor
        i2c = board.I2C()  # Uses board.SCL and board.SDA
        self.sensor = adafruit_bh1750.BH1750(i2c)

        # Labels and metrics
        self.labels = {'sensor': 'BH1750', 'sensor_type': 'Light', 'instance': instance_name}
        self.metrics = {
            'lux': Gauge(
                'sensor_light_ambient_lux',
                'Total light level in lux',
                list(self.labels.keys())
            ).labels(**self.labels),
        }

    def update_metrics(self):
        """Update the BH1750 metrics."""
        try:
            # Read sensor values
            lux = self.sensor.lux

            # Update Prometheus metrics
            self.metrics['lux'].set(lux)
        except Exception as e:
            print(f"Error updating BH1750 metrics: {e}")
