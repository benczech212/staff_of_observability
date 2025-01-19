from prometheus_client import Gauge
import board
import adafruit_tsl2591

class TSL2591_Sensor:
    def __init__(self, instance_name="TSL2591"):
        # Initialize the sensor
        i2c = board.I2C()  # Uses board.SCL and board.SDA
        self.sensor = adafruit_tsl2591.TSL2591(i2c)

        # Labels and metrics
        self.labels = {'sensor': 'TSL2591', 'sensor_type': 'Light', 'instance': instance_name}
        self.metrics = {
            'lux': Gauge(
                'sensor_light_lux',
                'Total light level in lux',
                list(self.labels.keys(),['unit'])
            ).labels(**self.labels),
            'infrared': Gauge(
                'sensor_light_infrared',
                'Infrared light level (raw)',
                list(self.labels.keys(),['unit'])
            ).labels(**self.labels),
            'visible': Gauge(
                'sensor_light_visible',
                'Visible light level (raw)',
                list(self.labels.keys(),['unit'])
            ).labels(**self.labels),
            'full_spectrum': Gauge(
                'sensor_light_full_spectrum',
                'Full spectrum light level (IR + visible, raw)',
                list(self.labels.keys(),['unit'])
            ).labels(**self.labels),
        }

    def update_metrics(self):
        """Update the TSL2591 metrics."""
        try:
            # Read sensor values
            lux = self.sensor.lux
            infrared = self.sensor.infrared
            visible = self.sensor.visible
            full_spectrum = self.sensor.full_spectrum

            # Update Prometheus metrics
            self.metrics['lux'].labels(**self.base_labels, unit='Lux').set(lux)
            self.metrics['infrared'].labels(**self.base_labels, unit='raw').set(infrared)
            self.metrics['visible'].labels(**self.base_labels, unit='raw').set(visible)
            self.metrics['full_spectrum'].labels(**self.base_labels, unit='raw').set(full_spectrum)
        except Exception as e:
            print(f"Error updating TSL2591 metrics: {e}")
