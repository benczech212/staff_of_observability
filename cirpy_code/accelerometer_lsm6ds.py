import time
import board
from adafruit_lsm6ds.lsm6ds3 import LSM6DS3

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

    # Print the sensor values
    print("Acceleration (m/s^2): ({0:0.3f}, {1:0.3f}, {2:0.3f})".format(acc_x, acc_y, acc_z))
    print("Gyroscope (radians/s): ({0:0.3f}, {1:0.3f}, {2:0.3f})".format(gyro_x, gyro_y, gyro_z))
    print("Temperature: {0:0.3f}C".format(temperature))
    print("Step count:", step_count)
    print("")  # Add a blank line for readability

    # Delay for a short period (adjust as needed)
    time.sleep(0.5)