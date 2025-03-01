import time
import board
from adafruit_lsm6ds.lsm6ds3 import LSM6DS3
from prometheus_client import Gauge, start_http_server

# Create I2C or SPI bus object.
# I2C is recommended
try:
    i2c = board.I2C()  # uses board.SCL and board.SDA
    sensor = LSM6DS3(i2c)
except ValueError:
    # If I2C fails due to a pin conflict, attempt to use SPI
    spi = board.SPI()
    cs = board.D5  # Replace D5 with the actual Chip Select pin you're using
    sensor = LSM6DS3(spi, cs)

# Enable the pedometer
sensor.pedometer_enable = True

# Optional: Reset the step count to 0
# sensor.reset_pedometer() # You might want to do this at the beginning of a walk/run

while True:
    # Get acceleration, gyroscope, and temperature data
    acc_x, acc_y, acc_z = sensor.acceleration
    gyro_x, gyro_y, gyro_z = sensor.gyro
    temperature = sensor.temperature

    # Get the step count
    step_count = sensor.pedometer_steps
    # Define Prometheus metrics
    acc_x_gauge = Gauge('acceleration_x', 'Acceleration in X direction')
    acc_y_gauge = Gauge('acceleration_y', 'Acceleration in Y direction')
    acc_z_gauge = Gauge('acceleration_z', 'Acceleration in Z direction')
    gyro_x_gauge = Gauge('gyroscope_x', 'Gyroscope in X direction')
    gyro_y_gauge = Gauge('gyroscope_y', 'Gyroscope in Y direction')
    gyro_z_gauge = Gauge('gyroscope_z', 'Gyroscope in Z direction')
    temperature_gauge = Gauge('temperature', 'Temperature in Celsius')
    step_count_gauge = Gauge('step_count', 'Number of steps')

    # Start Prometheus server
    start_http_server(8000)

    # Set the sensor values to the Prometheus metrics
    acc_x_gauge.set(acc_x)
    acc_y_gauge.set(acc_y)
    acc_z_gauge.set(acc_z)
    gyro_x_gauge.set(gyro_x)
    gyro_y_gauge.set(gyro_y)
    gyro_z_gauge.set(gyro_z)
    temperature_gauge.set(temperature)
    step_count_gauge.set(step_count)

    # Delay for a short period (adjust as needed)
    time.sleep(0.5)