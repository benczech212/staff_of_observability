# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT
"""NeoKey simpletest."""
import board
from adafruit_neokey.neokey1x4 import NeoKey1x4
from adafruit_seesaw import rotaryio, digitalio, seesaw
import digitalio as dio



NEOKEY_INT_PIN = board.D6
neokey_int = dio.DigitalInOut(NEOKEY_INT_PIN)
neokey_int.direction = dio.Direction.INPUT
neokey_int.pull = dio.Pull.UP

i2c = board.I2C()
ss = seesaw.Seesaw(i2c, addr=0x30)


# Create a NeoKey object
neokey = NeoKey1x4(i2c, addr=0x30,interrupt=True)
key_pins = 0b00001111  # Binary for keys 0-3
ss.set_GPIO_interrupts(key_pins, True)

while True:
    # Check if the interrupt pin is triggered
    if not neokey_int.value:  # Interrupt is active low
        print("Interrupt detected!")
        
        # Check which key is pressed
        pressed_keys = neokey.get_keys()  # Get the active keys
        for key in pressed_keys:
            print(f"Key {key} is pressed.")

        # Wait a moment to debounce
        ss.set_GPIO_interrupts(key_pins, False)  # Clear the interrupt
        ss.set_GPIO_interrupts(key_pins, True)