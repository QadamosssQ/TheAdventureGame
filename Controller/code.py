import board
from analogio import AnalogIn
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
import time
import digitalio

keyboard = Keyboard(usb_hid.devices)
xAxis = AnalogIn(board.A1)
yAxis = AnalogIn(board.A0)

button_a = digitalio.DigitalInOut(board.GP15)
button_b = digitalio.DigitalInOut(board.GP14)

button_a.switch_to_input(pull=digitalio.Pull.UP)
button_b.switch_to_input(pull=digitalio.Pull.UP)

DEADZONE = 5000
CENTER_VALUE = 32768
DELAY = 0.1

def get_direction(value):
    if value < CENTER_VALUE - DEADZONE:
        return -1
    elif value > CENTER_VALUE + DEADZONE:
        return 1
    else:
        return 0

while True:
    x_direction = get_direction(xAxis.value) * -1
    y_direction = get_direction(yAxis.value)

    if x_direction < 0:
        keyboard.press(Keycode.LEFT_ARROW)
    elif x_direction > 0:
        keyboard.press(Keycode.RIGHT_ARROW)
    else:
        keyboard.release(Keycode.LEFT_ARROW)
        keyboard.release(Keycode.RIGHT_ARROW)

    if y_direction < 0:
        keyboard.press(Keycode.DOWN_ARROW)
    elif y_direction > 0:
        keyboard.press(Keycode.UP_ARROW)
    else:
        keyboard.release(Keycode.UP_ARROW)
        keyboard.release(Keycode.DOWN_ARROW)

    if not button_a.value:
        keyboard.press(Keycode.A)
    else:
        keyboard.release(Keycode.A)

    if not button_b.value:
        keyboard.press(Keycode.B)
    else:
        keyboard.release(Keycode.B)

    time.sleep(DELAY)
