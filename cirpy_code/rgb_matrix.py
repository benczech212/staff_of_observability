# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import board
from rainbowio import colorwheel

from adafruit_is31fl3741.adafruit_rgbmatrixqt import Adafruit_RGBMatrixQT
import adafruit_is31fl3741

i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
is31 = Adafruit_RGBMatrixQT(i2c, allocate=adafruit_is31fl3741.PREFER_BUFFER)
is31.set_led_scaling(128)
is31.global_current = 0xFF
# print("Global current is: ", is31.global_current)
is31.enable = True
# print("Enabled? ", is31.enable)

wheeloffset = 0
pixels_x = 13
pixels_y = 9
pixel_count = pixels_x * pixels_y

def xy_to_index(x, y):
    return y * pixels_x + x

def index_to_xy(index):
    return index % pixels_x, index // pixels_x




while True:
    for i in range(pixel_count):
        x, y = index_to_xy(i)
        is31.pixel(x, y, colorwheel((wheeloffset + i) % 256))
    wheeloffset += 1
    is31.show()
