from adafruit_seesaw import seesaw, rotaryio, digitalio, neopixel
import digitalio as dio
# from base_io_device import BaseIODevice
import board
import time

class RotoryEncoder_Driver():
    def __init__(self, device_name="RotoryEncoder1", i2c_address=0x36,buton_pin=24,encoder_interrupt_pin=board.D5,expected_seesaw_product=4991,invert_position=False):
        """
        Initialize the Rotary Encoder using I2C.
        
        Args:
            i2c_address (int): I2C address of the rotary encoder (default: 0x36).
        """
        self.device_name = device_name
        self.i2c_address = i2c_address
        self.button_pin = buton_pin
        self.encoder_interrupt_pin = encoder_interrupt_pin
        self.expected_seesaw_product = expected_seesaw_product
        self.invert_position = invert_position
        self.position = 0
        self.last_position = 0
        self.button_held = False
        # self.pixels = neopixel.NeoPixel(seesaw,6,1)
        self.initialized = False
        # Initialize I2C connection to the Seesaw device
        self.init_device()

        # Verify firmware product ID
        self.seesaw_product = (self.seesaw.get_version() >> 16) & 0xFFFF
        while self.seesaw_product != 4991:
            # wait 5 seconds and try again
            print("Incorrect firmware detected for Rotary Encoder. Expected 4991, got {self.seesaw_product}")
            time.sleep(5)
            self.seesaw_product = (self.seesaw.get_version() >> 16) & 0xFFFF

        # if seesaw_product != 4991:
            # raise ValueError(f"Incorrect firmware detected for Rotary Encoder. Expected 4991, got {seesaw_product}")
        
        self.update()
        # self.test_rgb()

    def test_rgb(self):
        self.pixels.fill((255,0,0))
        self.pixels.show()
        time.sleep(1)
        self.pixels.fill((0,255,0))
        self.pixels.show()
        time.sleep(1)
        self.pixels.fill((0,0,255))
        self.pixels.show()
        time.sleep(1)
        self.pixels.fill((0,0,0))
        self.pixels.show()
    

    def init_device(self):
        try:
            self.i2c = board.I2C()
            self.seesaw = seesaw.Seesaw(self.i2c, addr=self.i2c_address)
            self.seesaw.enable_encoder_interrupt()
            self.seesaw.set_GPIO_interrupts(self.button_pin, True)
            self.encoder = rotaryio.IncrementalEncoder(self.seesaw)
            self.button = digitalio.DigitalIO(self.seesaw, self.button_pin)
            self.encoder_interrupt = dio.DigitalInOut(self.encoder_interrupt_pin)
            self.encoder_interrupt.direction = dio.Direction.INPUT
            self.encoder_interrupt.pull = dio.Pull.UP
            self.initialized = True
        except Exception as e:
            print(f"Error initializing Rotary Encoder: {e}")
            self.initialized = False



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
        print(self.status)
        return self.status
    
    def get_position(self):
        """
        Get the current position of the rotary encoder.
        
        Returns:
            int: The current position.
        """
        return -self.last_position if self.invert_position else self.last_position
    
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

    def set_color(self,color):
        self.pixels.fill(color)
        print(f"Rotary Encoder Color Set to {color}")