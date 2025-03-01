from adafruit_seesaw import rotaryio, digitalio, seesaw
from adafruit_neokey.neokey1x4 import NeoKey1x4
# from base_io_device import BaseIODevice
import board

class NeoKey1x4_Driver():
    def __init__(self, device_name="NeoKey1", i2c_address=0x30,brightness = 0.5):
        self.key_count = 4
        """
        Initialize the Rotary Encoder using I2C.
        
        Args:
            i2c_address (int): I2C address of the rotary encoder (default: 0x36).
        """
        i2c = board.I2C()
        self.seesaw = seesaw.Seesaw(i2c, addr=i2c_address)
        self.seesaw.set_GPIO_interrupts(24, True)
        self.neokey = NeoKey1x4(i2c, addr=i2c_address)
        self.keys = {i: False for i in range(self.key_count)}
        self.previous_state = [False] * self.key_count
        self.brightness = self.set_brightness(brightness)
        self.neokey.set_GPIO_interrupts(24, True)
        
        # Verify firmware product ID
        seesaw_product = (self.seesaw.get_version() >> 16) & 0xFFFF
        
        self.device_name = device_name
        
        
        self.status = {}
        self.update()
        
    def update(self):
        """
        Update the state of the rotary encoder and button.
        
        This method should be called periodically in the main loop or a background thread.
        """
        # Update rotary encoder position
        for i in range(self.key_count):
            current_state = self.neokey[i]
            if current_state and not self.previous_state[i]:
                self.keys[i] = not self.keys[i]
                print(f"NeoKey Button {chr(65 + i)} Toggled to {'ON' if self.keys[i] else 'OFF'}")
            self.previous_state[i] = current_state
        
        self.status = {
            "keys": self.keys
        }
        print(self.status)
        return self.status

    def clear_keys(self):
        self.keys = {i: False for i in range(4)}
        self.update()

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

