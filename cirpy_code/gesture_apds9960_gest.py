# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import board
import time
from adafruit_apds9960.apds9960 import APDS9960

i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller

apds = APDS9960(i2c)
apds.enable_proximity = True
apds.enable_gesture = True
apds.enable_color = True

# Uncomment and set the rotation if depending on how your sensor is mounted.
# apds.rotation = 270 # 270 for CLUE

gesture_dict = {0x01: "up", 0x02: "down", 0x03: "left", 0x04: "right"}

while True:
    gesture = apds.gesture()
    if gesture:
        gesture_name = gesture_dict.get(gesture, "unknown")
        print("gesture:", gesture_name)
    # time.sleep(0.1)    

    # # prox
    # prox = apds.proximity
    # print("prox:", prox)

    # # color
    # color = apds.color_data
    # print("color:", color)
    # time.sleep(0.1)