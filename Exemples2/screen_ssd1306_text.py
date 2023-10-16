from machine import Pin, I2C
import ssd1306
from time import sleep

#Init I2C1
i2c = I2C(1)

# Screen settings
width_oled_screen = 128
height_oled_screen = 64

oled = ssd1306.SSD1306_I2C(width_oled_screen, height_oled_screen, i2c)

#Envoi du texte à afficher sur l'écran OLED
oled.text("MicroPython OLED!", 0, 0)
oled.text("    I2C   ", 0, 10)
oled.text("It's too easy !!!", 0, 20)
oled.show()

