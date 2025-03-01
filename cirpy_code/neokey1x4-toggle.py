# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT
"""NeoKey toggle test."""
import board
from adafruit_neokey.neokey1x4 import NeoKey1x4
import time

# use default I2C bus
i2c_bus = board.I2C()

# Create a NeoKey object
neokey = NeoKey1x4(i2c_bus, addr=0x30)

print("Adafruit NeoKey toggle test")

# Define initial state for each pixel (off by default)
pixel_states = [0x0, 0x0, 0x0, 0x0]

# Define colors for each pixel
pixel_colors = [0xFF0000, 0xFFFF00, 0x00FF00, 0x00FFFF]

# To debounce button presses
previous_states = [False, False, False, False]

while True:
    for i in range(4):
        if neokey[i] and not previous_states[i]:  # Button pressed (and not held)
            # Toggle the pixel state
            pixel_states[i] = pixel_colors[i] if pixel_states[i] == 0x0 else 0x0
            neokey.pixels[i] = pixel_states[i]
            print(f"Button {chr(65 + i)} toggled")

        # Update the previous state
        previous_states[i] = neokey[i]

    # Small delay to debounce
    time.sleep(0.05)

