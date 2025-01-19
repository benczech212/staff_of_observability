
SERVER_PORT = 9200
LOG_PATH = '/var/log/staff_of_o11y.log'


import threading
import time
import busio
import board
from flask import Flask
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
import logging

# Sensors
# from sensors.metrics_lsm6ds import LSM6DS3_Sensor
from sensors.metrics_lis3mdl import LIS3MDL_Sensor
from sensors.metrics_bh1750 import BH1750_Sensor
from sensors.metrics_tsl2591 import TSL2591_Sensor
from sensors.metrics_lsm6dsox import LSM6DSOX_Sensor
from sensors.metrics_bno055 import BNO055_Sensor
from sensors.metrics_pa1010d import PA1010D_Sensor
from sensors.metrics_bme680 import BME680_Sensor

# IO
from io_devices.rotory_encoder import RotoryEncoder
import os

# NeoPixel

from neopixels.driver import NeoPixelDriver

driver = NeoPixelDriver(pixel_count=24)


driver.pixels.fill((0, 255, 0))
driver.pixels.show()

def setup_logs():
    ''' Setup logging for the application 
    TODO add otel logging support '''
    # Ensure log directory exists
    log_format = '%(asctime)s - %(levelname)s - %(message)s'
    log_dir = os.path.dirname(LOG_PATH)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Ensure log file exists
    if not os.path.exists(LOG_PATH):
        with open(LOG_PATH, 'w') as f:
            pass

    logging.basicConfig(level=logging.INFO, format=log_format, filename=LOG_PATH)
    print(f"Logging to {LOG_PATH}")
    ### ---------------- ###

setup_logs()

app = Flask(__name__)

# Load sensors
sensors = [
    # LSM6DS3_Sensor(),
    # LIS3MDL_Sensor(),
    # LSM6DSOX_Sensor(),
    # BH1750_Sensor(),
    # TSL2591_Sensor(),
    BNO055_Sensor(), #imu
    PA1010D_Sensor(), #gps
    BME680_Sensor() #air quality
]

io_devices = [
    RotoryEncoder()
]

# Background thread to update all sensor metrics
def update_sensor_metrics(refresh_delay=0.5):
    while True:
        for sensor in sensors:
            try:
                sensor.update_metrics()
            except Exception as e:
                print(f"Error updating metrics for {sensor.__class__.__name__}: {e}")
        time.sleep(refresh_delay)

def update_io_devices(refresh_delay=0.5):
    while True:
        for device in io_devices:
            try:
                if hasattr(device, 'update'):
                    device.update()
                    logging.info(f"Updated state for {device.__class__.__name__}")
            except Exception as e:
                logging.error(f"Error updating state for {device.__class__.__name__}: {e}")
        time.sleep(refresh_delay)

# Start sensor metrics update thread
sensor_thread = threading.Thread(target=update_sensor_metrics, daemon=True)
sensor_thread.start()

# Start I/O devices update thread
io_thread = threading.Thread(target=update_io_devices, daemon=True)
io_thread.start()


@app.route('/io')
def io_status():
    """Expose the current status of all I/O devices."""
    all_device_status = {}
    for device in io_devices:
        try:
            all_device_status[device.device_name] = device.update()
        except Exception as e:
            all_device_status[device.device_name] = f"Error: {e}"

@app.route('/')
def home():
    """Home page."""
    return "Welcome to the Staff of Observability!", 200

@app.route('/metrics')
def metrics():
    """Expose Prometheus metrics."""
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

@app.route('/health')
def health():
    """Health check endpoint."""
    return {"status": "healthy", "sensors_count": len(sensors), "io_devices_count": len(io_devices)}, 200

if __name__ == "__main__":
    logging.info("Starting Flask server...")
    app.run(host='0.0.0.0', port=SERVER_PORT)