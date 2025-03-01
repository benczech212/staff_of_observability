# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-FileCopyrightText: 2021 John Furcean
# SPDX-License-Identifier: MIT

"""NeoKey and I2C rotary encoder test example."""

import board
import time
from adafruit_neokey.neokey1x4 import NeoKey1x4
from adafruit_seesaw import seesaw, rotaryio, digitalio

# Set up NeoKey
i2c_bus = board.I2C()
neokey = NeoKey1x4(i2c_bus, addr=0x30)
print("Adafruit NeoKey toggle test")

# Initial state for NeoKey pixels (off by default)
pixel_states = [0x0, 0x0, 0x0, 0x0]
pixel_colors = [0xFF0000, 0xFFFF00, 0x00FF00, 0x00FFFF]
previous_states = [False, False, False, False]

# Set up Rotary Encoder
seesaw = seesaw.Seesaw(i2c_bus, addr=0x36)
seesaw_product = (seesaw.get_version() >> 16) & 0xFFFF
print("Found product {}".format(seesaw_product))
if seesaw_product != 4991:
    print("Wrong firmware loaded? Expected 4991")

button = digitalio.DigitalIO(seesaw, 24)
button_held = False
encoder = rotaryio.IncrementalEncoder(seesaw)
last_position = None

while True:
    # NeoKey handling
    for i in range(4):
        if neokey[i] and not previous_states[i]:  # Button pressed
            pixel_states[i] = pixel_colors[i] if pixel_states[i] == 0x0 else 0x0
            neokey.pixels[i] = pixel_states[i]
            print(f"NeoKey Button {chr(65 + i)} toggled")
        previous_states[i] = neokey[i]

    # Rotary Encoder handling
    position = -encoder.position  # Negate position for clockwise positive
    if position != last_position:
        last_position = position
        print("Encoder Position: {}".format(position))

    if not button.value and not button_held:  # Button pressed
        button_held = True
        print("Encoder Button pressed")

    if button.value and button_held:  # Button released
        button_held = False
       
