import max7219
from machine import Pin, SPI
import time


def display_text_scroll(text):
    # for 4 led blocks
    for p in range(4 * 8, len(text) * -8 - 1, -1):
        display.fill(False)
        display.text(text, p, 0, not False)
        display.show()
        time.sleep_ms(50)


spi = SPI(1)

time.sleep_ms(1000)

display = max7219.Max7219(32,8, spi, Pin('D10'))

display_text_scroll("STMicroelectronics")
