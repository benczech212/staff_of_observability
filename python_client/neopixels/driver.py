from adafruit_seesaw import rotaryio, digitalio, seesaw, neopixel

import board

class NeoPixelDriver():
    def __init__(self, pixel_count = 1, device_name="NeoPixels1", i2c_address=0x36, neo_pin = 15, brightness = 0.5):
        """
        Initialize the NeoPixels using I2C.
        
        Args:
            i2c_address (int): I2C address of the NeoPixels (default: 0x36).
        """
        i2c = board.I2C()
        self.seesaw = seesaw.Seesaw(i2c, addr=i2c_address)
        
    
        # Verify firmware product ID
        seesaw_product = (self.seesaw.get_version() >> 16) & 0xFFFF
        if seesaw_product != 4991:
            raise ValueError(f"Incorrect firmware detected for NeoPixels. Expected 4991, got {seesaw_product}")
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
            "pixels_on": self.pixels.value,
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