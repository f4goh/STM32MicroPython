from machine import Pin, I2C
import ssd1306
import framebuf
from time import sleep

#Init I2C1
i2c = I2C(1)

# screen parameters
SCREEN_WIDTH = 128
SCREEN_HEIGHT = 64

# ----------------------------------------
# READ Picture from file
def load_image(filename):
    with open(filename, 'rb') as f:
        f.readline()
        width, height = [int(v) for v in f.readline().split()]
        data = bytearray(f.read())
    return framebuf.FrameBuffer(data, width, height, framebuf.MONO_HLSB)

# -------------------------------------------
# display ST logo
def display_logo(screen):
    if screen is not None:
        screen.fill(0)
        logo_pbm = load_image("logo_st.pbm")
        screen.blit(logo_pbm, 0, 0)
        screen.show()


display = ssd1306.SSD1306_I2C(SCREEN_WIDTH, SCREEN_HEIGHT, i2c)

# display log during 5 seconds
display_logo(display)
