import board
import time
from adafruit_seesaw import seesaw, rotaryio, digitalio
from adafruit_neokey.neokey1x4 import NeoKey1x4
import digitalio as dio


# Create a NeoKey object
class IO_RotoryEncoder():
    def __init__(self, i2c_addr = 0x36, button_pin = 24, int_pin = board.D5 ):
        self.i2c_addr = i2c_addr
        self.button_pin = button_pin
        self.int_pin = int_pin
        try:
            self.i2c = board.I2C()
            self.seesaw = seesaw.Seesaw(self.i2c, addr=self.i2c_addr)
            self.seesaw.pin_mode(self.button_pin, seesaw.INPUT_PULLUP)
            self.seesaw.enable_encoder_interrupt()
        except:
            print("Error initializing the Rotory Encoder")
            return None

        # self.seesaw.set_GPIO_interrupts(24, True)
        self.encoder_interrupt = dio.DigitalInOut(int_pin)
        self.encoder_interrupt.direction = dio.Direction.INPUT
        self.encoder_interrupt.pull = dio.Pull.UP
        self.encoder = rotaryio.IncrementalEncoder(self.seesaw)
        self.button = digitalio.DigitalIO(self.seesaw, self.button_pin)
        self.button_held = False

        self.status = {}
        self.update()

    def update(self):
        self.handle_encoder_interrupt()
        self.handle_button_interrupt()
            
    def handle_encoder_interrupt(self):
        print(self.encoder_interrupt)
        # if not self.encoder_interrupt.value:
            # position = self.seesaw.encoder_position()
            # self.status['position'] = position

    def handle_button_interrupt(self):
        if not self.button.value and not self.button_held:
            self.button_held = True
            print("Button pressed")
        elif self.button.value and self.button_held:
            self.button_held = False
            print("Button released")
        self.status['button'] = self.button.value
        self.status['button_held'] = self.button_held



menu_id = 0

menu_dict = {
    0: "Main Menu",
    1: "Effect Menu",
    2: "Color Menu",
}
knob = IO_RotoryEncoder()
while True:
    knob.update()
    if 'position' in knob.status:
        menu_id = knob.status['position']
        print(menu_dict[menu_id])
    if 'button' in knob.status:
        if knob.status['button']:
            print("Button Pressed")
    time.sleep(0.1)

