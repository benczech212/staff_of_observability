import time
import board
from adafruit_lsm6ds.lsm6dsox import LSM6DSOX
import adafruit_lis3mdl
import math

i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
sensor_magnetometer = adafruit_lis3mdl.LIS3MDL(i2c)
sensor_imu = LSM6DSOX(i2c)


def vector_2_degrees(x, y):
    angle = math.degrees(math.atan2(y, x))
    if angle < 0:
        angle += 360
    return angle


def get_heading(_sensor):
    magnet_x, magnet_y, _ = _sensor.magnetic
    return vector_2_degrees(magnet_x, magnet_y)


def get_acceleration(_sensor):
    return _sensor.acceleration

def get_gyro(_sensor):
    return _sensor.gyro


def get_magnetic(_sensor):
    return _sensor.magnetic

while True:
    heading = get_heading(sensor_magnetometer)
    magnetic = get_magnetic(sensor_magnetometer)
    accel = get_acceleration(sensor_imu)
    gyro = get_gyro(sensor_imu)
    

    print("Heading: {:.2f} degrees".format(heading))
    print("Magnetic: X:%.2f, Y: %.2f, Z: %.2f uT" % (magnetic))
    print("Acceleration: X:%.2f, Y: %.2f, Z: %.2f m/s^2" % (accel))
    print("Gyro X:%.2f, Y: %.2f, Z: %.2f radians/s" % (gyro))
    time.sleep(0.2)


i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
sensor_magnetometer = LSM6DSOX(i2c)

while True:
    
    print("")
    time.sleep(0.5)