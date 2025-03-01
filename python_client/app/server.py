
SERVER_PORT = 9200
LOG_PATH = '/var/log/staff_of_o11y.log'
PIXEL_COUNT = 28

import os
import threading
import time
import busio
import board
import requests
from flask import Flask, request, jsonify, render_template
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
from sensors.metrics_bno085 import BNO08X_Sensor


# IO
from io_devices.rotory_encoder import RotoryEncoder_Driver
from io_devices.neokey_1x4 import NeoKey1x4_Driver


# NeoPixel
from neopixels.driver import NeoPixelDriver



def setup_logs():
    ''' Setup logging for the application 
        TODO add otel logging support '''
    logging.getLogger().setLevel(logging.INFO)
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
    # BNO08X_Sensor(), #imu
    BNO055_Sensor(), #imu
    PA1010D_Sensor(), #gps
    BME680_Sensor() #air quality
]

io_devices = [
    # RotoryEncoder_Driver(),
    # NeoKey1x4_Driver()
]

pixel_driver = NeoPixelDriver(pixel_count=PIXEL_COUNT)

# Background thread to update all sensor metrics
def update_sensor_metrics(refresh_delay=0.1):
    while True:
        for sensor in sensors:
            try:
                sensor._get_gas()
            except Exception as e:
                print(f"Error updating metrics for {sensor.__class__.__name__}: {e}")
        time.sleep(refresh_delay)

def update_io_devices(refresh_delay=0.1):
    while True:
        for device in io_devices:
            try:
                if hasattr(device, 'update'):
                    device.update()
                    logging.debug(f"Updated state for {device.__class__.__name__}")
            except Exception as e:
                logging.error(f"Error updating state for {device.__class__.__name__}: {e}")
        time.sleep(refresh_delay)

# Start sensor metrics update thread
# sensor_thread = threading.Thread(target=update_sensor_metrics, daemon=True)
# sensor_thread.start()

# Start I/O devices update thread
# io_thread = threading.Thread(target=update_io_devices, daemon=True)
# io_thread.start()








########### 
# Routes



@app.route('/')
def home():
    """Home page."""
    return "Welcome to the Staff of Observability!", 200

@app.route('/metrics')
def metrics():
    """Expose Prometheus metrics."""
    for sensor in sensors:
        try:
            sensor.update_metrics()
        except Exception as e:
            logging.error(f"Error updating metrics for {sensor.__class__.__name__}: {e}")

    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

@app.route('/health')
def health():
    """Health check endpoint."""
    return {"status": "healthy", "sensors_count": len(sensors), "io_devices_count": len(io_devices)}, 200



# ########### Pixel Control
# @app.route('/pixels/<int:pixel_id>/set_color_rgb')
# def set_pixel_color(pixel_id):
#     """Set the color of a NeoPixel."""
#     try:
#         r = int(request.args.get('r'))
#         g = int(request.args.get('g'))
#         b = int(request.args.get('b'))
#         color = (r, g, b)
#         pixel_driver.set_pixel_color(pixel_id, color)
#         return f"Key {pixel_id} color set to {color}", 200
#     except Exception as e:
#         return f"Error setting key color: {e}", 500
# def set_pixel_color(pixel_id, r,g,b):
#     """Set the color of a NeoPixel."""
#     try:
#         color = (r,g,b)
#         pixel_driver.set_pixel_color(pixel_id, color)
#         return f"Key {pixel_id} color set to {color}", 200
#     except Exception as e:
#         return f"Error setting key color: {e}", 500

# @app.route('/pixels/set_pixels', methods=['POST'])
# def set_all_pixels():
#     """Set the color of all NeoPixels with a single request."""
#     try:
#         # Parse the JSON payload
#         data = request.get_json()
#         if not data:
#             return "No JSON payload provided", 400

#         # Validate and set colors for each pixel
#         for pixel_id, color in data.items():
#             if not isinstance(color, list) or len(color) != 3:
#                 return f"Invalid color format for pixel {pixel_id}. Must be [r, g, b]", 400

#             r, g, b = color

#             # Ensure the RGB values are integers and within range
#             if not (isinstance(r, int) and isinstance(g, int) and isinstance(b, int)) or not (0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255):
#                 return f"Invalid RGB values for pixel {pixel_id}. Must be integers between 0 and 255.", 400

#             pixel_driver.set_pixel_color(int(pixel_id), (r, g, b))

#         return "All pixels updated successfully", 200
#     except Exception as e:
#         logging.error(f"Error in /pixels/set_pixels: {e}")
#         return f"Error setting pixels: {e}", 500




#### UI 
@app.route('/io_ui')
def ui():
    """Serve the UI HTML page."""
    html_file = 'io_ui.html'
    return render_template(html_file), 200

@app.route('/sensors_ui')
def sensors_ui():
    """Render sensor status as an HTML page."""
    html_file = 'sensor_ui.html'
    return render_template(html_file,sensors=sensors), 200



@app.route('/io')
def io_status():
    """Expose the current status of all I/O devices."""
    all_device_status = {}
    for device in io_devices:
        all_device_status[device.device_name] = device.status
        print(device.device_name, device.status)
    return jsonify(all_device_status), 200

@app.route('/sensors')
def sensors_status():
    """Expose the current status of all sensors."""
    all_sensor_status = {}
    for sensor in sensors:
        try:
            sensor.update_metrics()
            all_sensor_status[sensor.instance_name] = sensor.sensor_values
            print(sensor.instance_name, sensor.sensor_values)
        except Exception as e:
            logging.error(f"Error updating metrics for {sensor.__class__.__name__}: {e}")
    return jsonify(all_sensor_status), 200


if __name__ == "__main__":
    logging.info("Starting Flask server...")
    app.run(host='0.0.0.0', port=SERVER_PORT)