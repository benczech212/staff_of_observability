# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT
"""NeoKey simpletest."""
import time
import board
import busio
from adafruit_neokey.neokey1x4 import NeoKey1x4
from rainbowio import colorwheel
from adafruit_seesaw import seesaw, neopixel,  rotaryio, digitalio
import digitalio as dio 

import threading

class NeoKey1x4_Driver():
    def __init__(self, device_name="NeoKey1", i2c_address=0x30, brightness=0.5):
        self.key_count = 4
        self.device_name = device_name
        self.i2c_address = i2c_address
        self.initial_brightness = brightness
        self.initalized = False
        """
        Initialize the NeoKey using I2C.
        
        Args:
            i2c_address (int): I2C address of the NeoKey (default: 0x30).
        """
        self.init_device()
        self.status = {}
        self.update()
        


        
    def init_device(self):
        if not self.initalized:
            try:
                i2c = board.I2C()
                self.seesaw = seesaw.Seesaw(i2c, addr=self.i2c_address)
                self.seesaw.set_GPIO_interrupts(24, True)
                self.neokey = NeoKey1x4(i2c, addr=self.i2c_address)
                self.keys = {i: False for i in range(self.key_count)}
                # self.previous_state = [False] * self.key_count
                self.brightness = self.set_brightness(self.initial_brightness)
                self.neokey.set_GPIO_interrupts(24, True)
                self.initalized = True
            except:
                self.initalized = False
            

        
        
        
      
        
    def update(self):
        """
        Update the state of the NeoKey buttons.
        
        This method should be called periodically in the main loop or a background thread.
        """
        if not self.initalized:
            self.init_device()
        if self.initalized:
            self.keys = {i: self.neokey[i] for i in range(self.key_count)}
            self.status = {
                "keys": self.keys,
                "brightness": self.brightness,
                "pixels": self.neokey.pixels
            }
            return self.status


    def clear_key_colors(self):
        for i in range(4):
            self.neokey.pixels[i] = 0x0
        self.update()
    
    def set_key_color(self, key, color):
        self.neokey.pixels[key] = color
        self.update()

    def set_brightness(self, brightness):
        self.neokey.brightness = brightness
        self.update()
        return self.neokey.brightness

class RotoryEncoder_Driver():
    def __init__(self, device_name="RotoryEncoder1", i2c_address=0x36,buton_pin=24,encoder_interrupt_pin=board.D5):
        """
        Initialize the Rotary Encoder using I2C.
        
        Args:
            i2c_address (int): I2C address of the rotary encoder (default: 0x36).
        """
        i2c = board.I2C()
        self.seesaw = seesaw.Seesaw(i2c, addr=i2c_address)
        # self.seesaw.pin_mode(buton_pin, seesaw.INPUT_PULLUP)
        self.seesaw.enable_encoder_interrupt()
        self.seesaw.set_GPIO_interrupts(buton_pin, True)
        self.encoder_interrupt_pin = encoder_interrupt_pin
        self.encoder_interrupt = dio.DigitalInOut(self.encoder_interrupt_pin)
        self.encoder_interrupt.direction = dio.Direction.INPUT
        self.encoder_interrupt.pull = dio.Pull.UP

        # Verify firmware product ID
        self.seesaw_product = (self.seesaw.get_version() >> 16) & 0xFFFF
        # if seesaw_product != 4991:
            # raise ValueError(f"Incorrect firmware detected for Rotary Encoder. Expected 4991, got {seesaw_product}")
        self.device_name = device_name
        # Configure the rotary encoder and button
        
        self.button_pin = buton_pin
        self.encoder = rotaryio.IncrementalEncoder(self.seesaw)
        self.button = digitalio.DigitalIO(self.seesaw, buton_pin)
        self.button_held = False
        self.last_position = 0
        self.position = 0
        self.status = {}
        self.update()

    def handle_encoder_interrupt(self):
        """
        Handle interrupts from the Seesaw device.
        
        This method should be called when the interrupt pin is triggered.
        """
        # Update rotary encoder position
        self.position = -self.encoder.position  # Negate to make clockwise positive
        if self.position != self.last_position and abs(self.position - self.last_position) < 10:
            self.last_position = self.position
            print(f"Rotary Encoder Position: {self.position}")
        else: self.position = self.last_position
        return self.position
    
    def update(self):
        """
        Update the state of the rotary encoder and button.
        
        This method should be called periodically in the main loop or a background thread.
        """
        if not self.encoder_interrupt.value: position = self.handle_encoder_interrupt()
        
        # Update button state
        if not self.button.value and not self.button_held:
            self.button_held = True
            print("Rotary Encoder Button Pressed")
        elif self.button.value and self.button_held:
            self.button_held = False
            print("Rotary Encoder Button Released")
        self.status = {
            "position": self.last_position,
            "button_pressed": not self.button.value
        }
        # print(self.status)
        return self.status
    
    def get_position(self):
        """
        Get the current position of the rotary encoder.
        
        Returns:
            int: The current position.
        """
        return -self.encoder.position
    
    def is_button_pressed(self):
        """
        Check if the rotary encoder button is currently pressed.
        
        Returns:
            bool: True if the button is pressed, False otherwise.
        """
        return not self.button.value
    
    def reset_position(self):
        """
        Reset the position of the rotary encoder to zero.
        """
        self.encoder.position = 0
        self.last_position = 0
        print("Rotary Encoder Position Reset")

class IOPannel():
    def __init__(self):
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.ss = seesaw.Seesaw(self.i2c, addr=0x60)
        self.neo_pin = 15
        self.num_pixels = 28
        self.pixels = neopixel.NeoPixel(self.ss, self.neo_pin, self.num_pixels, brightness = 0.1)
        self.neokey = NeoKey1x4_Driver()
        self.rotory_encoder = RotoryEncoder_Driver()


io = IOPannel()
neokey = io.neokey.neokey
pixels = io.pixels


def triangle_wave(x, period=1):
    scaled_x = (x / period) % 1
    return ((4 * abs(scaled_x - 0.5) - 1) + 1) / 2
    

class Layer():
    def __init__(self, layer_id = 0):
        self.layer_id = layer_id
        self.effect_id = 0
        self.enabled = False
        self.focused = False
        self.tick_count = 0
        self.key_color = (255, 255, 255)

    def set_effect(self, effect_id):
        self.effect_id = effect_id
    
    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False

    def focus(self):
        self.focused = True

    def unfocus(self):
        self.focused = False
        

    def update(self):
        self.tick_count += 1
        t = 100
        if self.focused:
            # brightness = triangle_wave(self.tick_count, period=t)
            # color = tuple(int(brightness * c) for c in self.key_color)
            
            # neokey.pixels[self.layer_id] = color
            pass
    
    def __str__(self):
        return f"Layer {self.layer_id}: {self.effect_id}"

class LayerManager():
    def __init__(self, num_layers = 4):
        self.num_layers = num_layers    
        self.layers = [Layer(i) for i in range(num_layers)]
        self.current_layer = None
    
    def focus(self, layer_id):
        if self.current_layer == layer_id:
            return None
        else:
            for this_layer_id, layer in enumerate(self.layers):
                if this_layer_id != layer_id:
                    layer.unfocus()
                    neokey.pixels[this_layer_id] = (0, 0, 0)
                else:
                    layer.focus()
            self.current_layer = layer_id
            print(f"Focused on layer {layer_id}")

    def update(self):
        self.check_for_input()
        for layer in self.layers:
            layer.update()

    def check_for_input(self):
        for i in range(self.num_layers):
            if neokey[i]:
                self.focus(i)
                break

lm = LayerManager()


# for i in range(100):
#     print(triangle_wave(i, period=100))


while True:
    # lm.update()
    io.neokey.update()
    io.rotory_encoder.update()
    color = colorwheel(io.rotory_encoder.encoder.position % 256)
    print(color)
    io.pixels.fill(color)

    # if lm.layers[0].focused:
    #     pos = io.rotory_encoder.get_position() % io.num_pixels
    #     for i in range(io.num_pixels):
    #         if i == pos:
    #             pixels[i] = colorwheel(pos * 256 // io.num_pixels)
    #         else:
    #             pixels[i] = (0, 0, 0)

    #     pixels.show()


   