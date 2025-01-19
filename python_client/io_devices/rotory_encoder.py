from adafruit_seesaw import rotaryio, digitalio, seesaw
# from base_io_device import BaseIODevice
import board

class RotoryEncoder():
    def __init__(self, device_name="RotoryEncoder1", i2c_address=0x36):
        """
        Initialize the Rotary Encoder using I2C.
        
        Args:
            i2c_address (int): I2C address of the rotary encoder (default: 0x36).
        """
        i2c = board.I2C()
        self.seesaw = seesaw.Seesaw(i2c, addr=i2c_address)
        
        # Verify firmware product ID
        seesaw_product = (self.seesaw.get_version() >> 16) & 0xFFFF
        if seesaw_product != 4991:
            raise ValueError(f"Incorrect firmware detected for Rotary Encoder. Expected 4991, got {seesaw_product}")
        self.device_name = device_name
        # Configure the rotary encoder and button
        self.encoder = rotaryio.IncrementalEncoder(self.seesaw)
        self.button = digitalio.DigitalIO(self.seesaw, 24)
        self.button_held = False
        self.last_position = None
        self.status = {}
        self.update()
    
    def update(self):
        """
        Update the state of the rotary encoder and button.
        
        This method should be called periodically in the main loop or a background thread.
        """
        # Update rotary encoder position
        position = -self.encoder.position  # Negate to make clockwise positive
        if position != self.last_position:
            self.last_position = position
            print(f"Rotary Encoder Position: {position}")
        
        # Update button state
        if not self.button.value and not self.button_held:
            self.button_held = True
            print("Rotary Encoder Button Pressed")
        elif self.button.value and self.button_held:
            self.button_held = False
            print("Rotary Encoder Button Released")
        self.status = {
            "position": position,
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