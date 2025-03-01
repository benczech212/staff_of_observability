from adafruit_seesaw import rotaryio, digitalio, seesaw, neopixel

import board
import time
import random

class NeoPixel_Driver():
    def __init__(self, pixel_count = 1, device_name="NeoPixels1", i2c_address=0x60, neo_pin = 15, brightness = 0.5):
        """
        Initialize the NeoPixels using I2C.
        
        Args:
            i2c_address (int): I2C address of the NeoPixels (default: 0x36).
        """
        i2c = board.I2C()
        while True:
            try:
                self.seesaw = seesaw.Seesaw(i2c, addr=i2c_address)
                # Verify firmware product ID
                self.seesaw_product = (self.seesaw.get_version() >> 16) & 0xFFFF
                break
            except Exception as e:
                print(f"Failed to initialize I2C or verify product: {e}. Retrying...")
                time.sleep(1)
        # if seesaw_product != 4991:
        #     raise ValueError(f"Incorrect firmware detected for NeoPixels. Expected 4991, got {seesaw_product}")
        self.device_name = device_name
        # Configure the NeoPixels
        self.neo_pin = neo_pin
        self.pixel_count = pixel_count
        self.brightness = brightness
        self.pixels = neopixel.NeoPixel(self.seesaw, self.neo_pin, self.pixel_count, brightness = self.brightness)

        self.status = {}
        self.update()

    def update(self):
        """
        Update the state of the NeoPixels.
        
        This method should be called periodically in the main loop or a background thread.
        """
        self.status = {
            "pixels" : self.pixels,
            "brightness": self.brightness,
            "pixel_count": self.pixel_count
        }
        print(self.status)
        return self.status

    def set_brightness(self, brightness):
        """
        Set the brightness of the NeoPixels.
        
        Args:
            brightness (float): The brightness value between 0.0 and 1.0.
        """
        self.brightness = brightness
        self.pixels.brightness = self.brightness
        print(f"NeoPixels brightness set to {self.brightness}")
        self.update()

    def set_pixel_count(self, pixel_count):
        """
        Set the number of NeoPixels.
        
        Args:
            pixel_count (int): The number of NeoPixels.
        """
        self.pixel_count = pixel_count
        self.pixels = neopixel.NeoPixel(self.seesaw, self.neo_pin, self.pixel_count, brightness = self.brightness)
        print(f"NeoPixels count set to {self.pixel_count}")
        self.update()

    def set_pixel_color(self, pixel, color):
        """
        Set the color of a NeoPixel.
        
        Args:
            pixel (int): The index of the NeoPixel.
            color (int): The color value.
        """
        self.pixels[pixel] = color
        print(f"NeoPixel {pixel} color set to {color}")
        self.update()


px_driver = NeoPixel_Driver(pixel_count=10)

class Brush():
    def __init__(self, color = (255, 255, 255), postion = 0, velocity = random.uniform(0.01, 0.1)):
        self.color = color
        self.postion = postion
        self.velocity = velocity
        self.age = 1.0
        self.age_rate = 0.01


    def set_color(self, color):
        self.color = color

    def get_color(self):
        return self.color

    def update(self):
        self.age -= self.age_rate
        if self.age <= 0:
            del self
            return
        self.postion += self.velocity
        pixel_id = int((px_driver.pixel_count - 1) * self.postion)
        px_driver.set_pixel_color(pixel_id, self.color)

    
brush = Brush()

while True:
    brush.update()
    # brush.postion += 0.01
    time.sleep(0.1)
        
