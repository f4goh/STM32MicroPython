#CLK 13, MOSI 11, CS 10
import max7219
from machine import Pin, SPI
import time,sys


def display_text_scroll(text):
    # for 4 led blocks
    for p in range(4 * 8, len(text) * -8 - 1, -1):
        display.fill(False)
        display.text(text, p, 0, not False)
        display.show()
        time.sleep_ms(50)


spi = SPI(1)

time.sleep_ms(1000)

display = max7219.Max7219(8,8, spi, Pin('D10'))



while True:
    try:
        display_text_scroll("F4GOH")
    except KeyboardInterrupt:
        print('Ctrl-C pressed...exiting')
        sys.exit()
        