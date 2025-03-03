# SPDX-FileCopyrightText: 2020 Bryan Siepert, written for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense
import time
import board
import busio
from adafruit_bno08x import (
    BNO_REPORT_ACCELEROMETER,
    BNO_REPORT_GYROSCOPE,
    BNO_REPORT_MAGNETOMETER,
    BNO_REPORT_ROTATION_VECTOR,
    BNO_REPORT_ACTIVITY_CLASSIFIER,
    BNO_REPORT_GAME_ROTATION_VECTOR,
    BNO_REPORT_GEOMAGNETIC_ROTATION_VECTOR,
    BNO_REPORT_STEP_COUNTER,
    BNO_REPORT_GRAVITY,
    BNO_REPORT_LINEAR_ACCELERATION,
    BNO_REPORT_GYRO_INTEGRATED_ROTATION_VECTOR,
    BNO_REPORT_RAW_ACCELEROMETER,
    BNO_REPORT_RAW_GYROSCOPE,
    BNO_REPORT_RAW_MAGNETOMETER,
    BNO_REPORT_SHAKE_DETECTOR,

)
from adafruit_bno08x.i2c import BNO08X_I2C

i2c = busio.I2C(board.SCL, board.SDA, frequency=400000)
bno = BNO08X_I2C(i2c)

features = [BNO_REPORT_ACCELEROMETER, BNO_REPORT_GYROSCOPE, BNO_REPORT_MAGNETOMETER, BNO_REPORT_ROTATION_VECTOR, BNO_REPORT_ACTIVITY_CLASSIFIER]

bno.enable_feature(BNO_REPORT_ACCELEROMETER)
bno.enable_feature(BNO_REPORT_GYROSCOPE)
bno.enable_feature(BNO_REPORT_MAGNETOMETER)
bno.enable_feature(BNO_REPORT_ROTATION_VECTOR)
bno.enable_feature(BNO_REPORT_ACTIVITY_CLASSIFIER)
bno.enable_feature(BNO_REPORT_GAME_ROTATION_VECTOR)
bno.enable_feature(BNO_REPORT_GEOMAGNETIC_ROTATION_VECTOR)
bno.enable_feature(BNO_REPORT_STEP_COUNTER)
bno.enable_feature(BNO_REPORT_GRAVITY)
bno.enable_feature(BNO_REPORT_LINEAR_ACCELERATION)
bno.enable_feature(BNO_REPORT_GYRO_INTEGRATED_ROTATION_VECTOR)
bno.enable_feature(BNO_REPORT_RAW_ACCELEROMETER)
bno.enable_feature(BNO_REPORT_RAW_GYROSCOPE)
bno.enable_feature(BNO_REPORT_RAW_MAGNETOMETER)
bno.enable_feature(BNO_REPORT_SHAKE_DETECTOR)


while True:
    time.sleep(0.5)
    print("Acceleration:")
    accel_x, accel_y, accel_z = bno.acceleration  # pylint:disable=no-member
    print("X: %0.6f  Y: %0.6f Z: %0.6f  m/s^2" % (accel_x, accel_y, accel_z))
    print("")

    print("Gyro:")
    gyro_x, gyro_y, gyro_z = bno.gyro  # pylint:disable=no-member
    print("X: %0.6f  Y: %0.6f Z: %0.6f rads/s" % (gyro_x, gyro_y, gyro_z))
    print("")

    print("Magnetometer:")
    mag_x, mag_y, mag_z = bno.magnetic  # pylint:disable=no-member
    print("X: %0.6f  Y: %0.6f Z: %0.6f uT" % (mag_x, mag_y, mag_z))
    print("")

    print("Rotation Vector Quaternion:")
    quat_i, quat_j, quat_k, quat_real = bno.quaternion  # pylint:disable=no-member
    print(
        "I: %0.6f  J: %0.6f K: %0.6f  Real: %0.6f" % (quat_i, quat_j, quat_k, quat_real)
    )
    activity = bno.activity_classification
    print(activity)

    print("Game Rotation Vector Quaternion:")
    quat_i, quat_j, quat_k, quat_real = bno.game_rotation_vector  # pylint:disable=no-member
    print(
        "I: %0.6f  J: %0.6f K: %0.6f  Real: %0.6f" % (quat_i, quat_j, quat_k, quat_real)
    )

    print("Geomagnetic Rotation Vector Quaternion:")
    quat_i, quat_j, quat_k, quat_real = bno.geomagnetic_rotation_vector  # pylint:disable=no-member
    print(
        "I: %0.6f  J: %0.6f K: %0.6f  Real: %0.6f" % (quat_i, quat_j, quat_k, quat_real)
    )

    print("Step Counter:")
    print(bno.step_count)

    print("Gravity:")
    grav_x, grav_y, grav_z = bno.gravity  # pylint:disable=no-member
    print("X: %0.6f  Y: %0.6f Z: %0.6f  m/s^2" % (grav_x, grav_y, grav_z))

    print("Linear Acceleration:")
    linear_accel_x, linear_accel_y, linear_accel_z = bno.linear_acceleration  # pylint:disable=no-member
    print(
        "X: %0.6f  Y: %0.6f Z: %0.6f  m/s^2" % (linear_accel_x, linear_accel_y, linear_accel_z)
    )

    print("Gyro Integrated Rotation Vector Quaternion:")
    quat_i, quat_j, quat_k, quat_real = bno.gyro_integrated_rotation_vector  # pylint:disable=no-member
    print(
        "I: %0.6f  J: %0.6f K: %0.6f  Real: %0.6f" % (quat_i, quat_j, quat_k, quat_real)
    )

    print("Raw Accelerometer:")
    raw_accel_x, raw_accel_y, raw_accel_z = bno.raw_acceleration  # pylint:disable=no-member
    print("X: %0.6f  Y: %0.6f Z: %0.6f  m/s^2" % (raw_accel_x, raw_accel_y, raw_accel_z))

    print("Raw Gyro:")
    raw_gyro_x, raw_gyro_y, raw_gyro_z = bno.raw_gyro  # pylint:disable=no-member
    print("X: %0.6f  Y: %0.6f Z: %0.6f rads/s" % (raw_gyro_x, raw_gyro_y, raw_gyro_z))

    print("Raw Magnetometer:")
    raw_mag_x, raw_mag_y, raw_mag_z = bno.raw_magnetic  # pylint:disable=no-member
    print("X: %0.6f  Y: %0.6f Z: %0.6f uT" % (raw_mag_x, raw_mag_y, raw_mag_z))

    print("Shake Detector:")
    print(bno.shake_detected)
    
    print("")

