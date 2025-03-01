import board
import time
from adafruit_seesaw import seesaw, rotaryio, digitalio
import digitalio as dio

# Pin configuration
ROTORY_INT_PIN = board.D5

# Initialize I2C and Seesaw
i2c = board.I2C()
seesaw = seesaw.Seesaw(i2c, addr=0x36)

# Enable encoder and GPIO interrupts
seesaw.enable_encoder_interrupt()
seesaw.set_GPIO_interrupts(24, True)

# Configure the rotary interrupt pin
rotory_int = dio.DigitalInOut(ROTORY_INT_PIN)
rotory_int.direction = dio.Direction.INPUT
rotory_int.pull = dio.Pull.UP

# Configure button pin
button = digitalio.DigitalIO(seesaw, 24)

# Initialize the encoder
encoder = rotaryio.IncrementalEncoder(seesaw)
last_position = 0
button_held = False

def handle_interrupt():
    """Handle the interrupt triggered by the Seesaw."""
    global last_position, button_held

    # Read the encoder position
    position = -encoder.position
    if position != last_position:
        last_position = position
        print("Position: {}".format(position))

    # Check the button state
    if not button.value and not button_held:
        button_held = True
        print("Button pressed")
    elif button.value and button_held:
        button_held = False
        print("Button released")


# Main loop
while True:
    # Check if the interrupt pin is triggered
    if not rotory_int.value:
        handle_interrupt()

    # Small delay to avoid busy-waiting
    time.sleep(0.01)
