from flask import Flask
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from sensors.metrics_lsm6ds import LSM6DS3_Sensor
from sensors.metrics_lis3mdl import LIS3MDL_Sensor
from sensors.metrics_bh1750 import BH1750_Sensor
from sensors.metrics_tsl2591 import TSL2591_Sensor
from sensors.metrics_lsm6dsox import LSM6DSOX_Sensor
from sensors.metrics_bno055 import BNO055_Sensor
import threading
import time

app = Flask(__name__)

# Load sensors
sensors = [
    # LSM6DS3_Sensor(),
    # LIS3MDL_Sensor(),
    # LSM6DSOX_Sensor(),
    # BH1750_Sensor(),
    # TSL2591_Sensor(),
    BNO055_Sensor()
]

# Background thread to update all sensor metrics
def update_sensor_metrics():
    while True:
        for sensor in sensors:
            try:
                sensor.update_metrics()
            except Exception as e:
                print(f"Error updating metrics for {sensor.__class__.__name__}: {e}")
        time.sleep(0.5)

# Start the background thread
thread = threading.Thread(target=update_sensor_metrics, daemon=True)
thread.start()

@app.route('/metrics')
def metrics():
    """Expose Prometheus metrics."""
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}
