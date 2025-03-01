from prometheus_client import start_http_server, Gauge
import board
import adafruit_bme680
from sensors.base_sensor import BaseSensor

class BME680_Sensor(BaseSensor):
    def __init__(self, instance_name="BME680"):
        self.instance_name = instance_name
        self.metrics = {}
        try:
            # Initialize I2C and the sensor
            i2c = board.I2C()
            self.sensor = adafruit_bme680.Adafruit_BME680_I2C(i2c)
        except Exception as e:
            print(f"Error initializing BME680 sensor: {e}")
            self.sensor = None


        # Define Prometheus metrics
        self.base_labels = {'sensor': 'BME680', 'sensor_type': 'Environmental'}
        self.metrics = {
            'temperature': self.get_or_create_metric_gauge(
                'sensor_temperature',
                'Temperature in Celsius from the BME680 sensor',
                {'unit': 'Celsius'}
                
            ),
            'gas': self.get_or_create_metric_gauge(
                'sensor_gas',
                'Gas resistance in ohms from the BME680 sensor',
                {'unit': 'Ohms'}
            ),
            'humidity': self.get_or_create_metric_gauge(
                'sensor_humidity',
                'Relative humidity percentage from the BME680 sensor',
                {'unit': 'Percent'}
            ),
            'pressure': self.get_or_create_metric_gauge(
                'sensor_pressure',
                'Pressure in hPa from the BME680 sensor',
                {'unit': 'hPa'}
            ),
            # 'altitude': self.get_or_create_metric_gauge(
            #     'sensor_altitude',
            #     'Estimated altitude in meters from the BME680 sensor',
            #     {'unit': 'Meters'}
            # )
        }
        self.sensor_values = {}
        # self.metrics = {
        #     'temperature': Gauge(
        #     'temperature',
        #     'Temperature in Celsius from the BME680 sensor',
        #     list(self.base_labels.keys()) + ['unit']
        #     ).labels(**self.base_labels, unit='Celsius'),
        #     'gas': Gauge(
        #     'sensor_gas',
        #     'Gas resistance in ohms from the BME680 sensor',
        #     list(self.base_labels.keys()) + ['unit']
        #     ).labels(**self.base_labels,unit="Ohms"),
        #     'humidity': Gauge(
        #     'sensor_humidity',
        #     'Relative humidity percentage from the BME680 sensor',
        #     list(self.base_labels.keys()) + ['unit']
        #     ).labels(**self.base_labels,unit="Percent"),
        #     'pressure': Gauge(
        #     'sensor_pressure',
        #     'Pressure in hPa from the BME680 sensor',
        #     list(self.base_labels.keys())  + ['unit']
        #     ).labels(**self.base_labels, unit="hPa"),
        #     'altitude': Gauge(
        #     'sensor_altitude',
        #     'Estimated altitude in meters from the BME680 sensor',
        #     list(self.base_labels.keys()) + ['unit']
        #     ).labels(**self.base_labels, unit="Meters")
        # }

    def update_metrics(self):
        try:
            temperature = self.sensor.temperature
            gas = self.sensor.gas
            humidity = self.sensor.relative_humidity
            pressure = self.sensor.pressure
            altitude = self.sensor.altitude

            self.sensor_values = {
                'temperature': temperature,
                'gas': gas,
                'humidity': humidity,
                'pressure': pressure,
                # 'altitude': altitude
            }

            # Update Prometheus metrics
            self.metrics['temperature'].set(temperature)
            self.metrics['gas'].set(gas)
            self.metrics['humidity'].set(humidity)
            self.metrics['pressure'].set(pressure)
            # self.metrics['altitude'].set(altitude)
        except Exception as e:
            print(f"Error updating BME680 metrics: {e}")
