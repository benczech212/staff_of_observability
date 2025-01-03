from flask import Flask
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from sensors.metrics_lsm6ds import update_acceleration, update_gyroscope, update_temperature, increment_step_count
import time
import threading
import board
from adafruit_lsm6ds.lsm6ds3 import LSM6DS3

app = Flask(__name__)

# Initialize the sensor
try:
    i2c = board.I2C()  # Uses board.SCL and board.SDA
    sensor = LSM6DS3(i2c)
except ValueError:
    # If I2C fails, fallback to SPI
    spi = board.SPI()
    cs = board.D5  # Replace D5 with the actual Chip Select pin
    sensor = LSM6DS3(spi, cs)

# Enable the pedometer
sensor.pedometer_enable = True

# Background thread to update metrics
def sensor_metrics_updater():
    while True:
        try:
            # Read real sensor values
            acc_x, acc_y, acc_z = sensor.acceleration
            gyro_x, gyro_y, gyro_z = sensor.gyro
            temperature = sensor.temperature
            step_count = sensor.pedometer_steps

            # Update Prometheus metrics
            update_acceleration(acc_x, acc_y, acc_z)
            update_gyroscope(gyro_x, gyro_y, gyro_z)
            update_temperature(temperature)
            increment_step_count(step_count)
        except Exception as e:
            print(f"Error reading sensor data: {e}")

        time.sleep(0.5)  # Adjust the update frequency as needed

# Start the background thread
thread = threading.Thread(target=sensor_metrics_updater, daemon=True)
thread.start()

@app.route('/metrics')
def metrics():
    """Expose Prometheus metrics."""
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}
