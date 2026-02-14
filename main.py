import digitalio
import board
from time import sleep
import random
from i2ctarget import I2CTarget
from pixelstrip import PixelStrip, current_time, MATRIX_COLUMN_MAJOR, MATRIX_ZIGZAG, RGB, MATRIX_TOP, MATRIX_LEFT
from colors import *

from animation_pulse import PulseAnimation
from animation_ladder import LadderAnimation

I2C_ADDRESS = 0x41
BRIGHTNESS = 0.5

# List of Animations
animation = [
    LadderAnimation(color=RED),
]

# List of PixelStrips
strip = [
    PixelStrip(board.GP13, 120, offset=0, bpp=4, pixel_order="GRB", brightness=BRIGHTNESS),
    PixelStrip(board.GP15, offset=0, width=8, height=8, bpp=4, pixel_order="GRB", brightness=BRIGHTNESS, options={MATRIX_TOP, MATRIX_LEFT, MATRIX_COLUMN_MAJOR}),
    PixelStrip(board.GP16, offset=0, width=8, height=8, bpp=4, pixel_order="GRB", brightness=BRIGHTNESS, options={MATRIX_TOP, MATRIX_LEFT, MATRIX_COLUMN_MAJOR, MATRIX_ZIGZAG}),
    PixelStrip(board.GP18, offset=0, width=32, height=8, bpp=4, pixel_order="GRB", brightness=BRIGHTNESS, options={MATRIX_TOP, MATRIX_LEFT, MATRIX_COLUMN_MAJOR})
]
# The built-in LED will turn on for half a second after every message 
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

i2c = None
google_eyes_on = False
google_eye_timeout = 0.0


def receive_message():
    """
    Receive a message through I2C, if available.  The first byte will
    contain the strip number and animation number, packed into the single
    byte.  If there is a param associated with this message, it is 
    concatenated after the first byte.
    """
    global i2c
    message = i2c.request()
    if not message:
        return None
    with message:
        message_bytes = message.read()
        b = message_bytes[0]
        strip_num = int((b & 0xE0) >> 5)
        anim_num = int(b & 0x1F)
        param = None 
        if len(message_bytes) > 1:
            param = message_bytes[1:].decode('utf-8')
        print(f"received {len(message_bytes)} bytes      {(strip_num, anim_num, param)}")
        return (strip_num, anim_num, param)


def main(i2c): 
    "Main program loop, for reading messages and changing Animations." 
    global strip, led, google_eyes_on, google_eye_timeout
    last_msg_time = 0.0
    strip[0].animation = animation[0] 
    strip[1].animation = animation[0]
    strip[2].animation = animation[0]
    strip[3].animation = animation[0]
    while True:
        for s in strip:
            s.draw()
        message = receive_message()
        if message is not None:
            strip_num = message[0]
            anim_num = message[1]
            if strip_num == 1 or strip_num == 2:
                if anim_num == 15:
                    google_eyes_on = True
                    google_eye_timeout = current_time + 5.0
                    pick_random_eyes()
                else
                    google_eyes_on = False
            if strip_num < len(strip) and anim_num < len(animation) and (not google_eyes_on):
                strip[strip_num].animation = animation[anim_num]
                if message[2] is not None or animation[anim_num].param is not None:
                    animation[anim_num].param = message[2]
            elif strip_num < len(strip):
                strip[strip_num].animation = None
            last_msg_time = current_time()
        led.value = (current_time() < last_msg_time + 0.5)
        if google_eyes_on and current_time() > google_eye_timeout:
            google_eye_timeout = current_time + 5.0
            pick_random_eyes()

def pick_random_eyes:
    "Pick a random googly-eye animation and set them into strips 1 and 2"
    pass

def blink(n, color=BLUE, sleep_time=0.4): 
    "Blink lights to show that the program is progressing."
    global strip, led
    for s in strip:
        s.clear()
    for _ in range(n):
        for s in strip:
            s[0] = color
            s.show()
            led.value = True
        sleep(sleep_time)
        for s in strip:
            s.clear()
            s.show()
            led.value = False
        sleep(sleep_time)


if __name__ == "__main__": 
    blink(2, BLUE)
    with I2CTarget(scl=board.SCL, sda=board.SDA, addresses=[I2C_ADDRESS]) as i2c:
        blink(1, GREEN)
        main(i2c) 