import pyb
import time

print("Leds with MicroPython it's easy")
# Init of leds(LED_1, LED_2, LED_3)

led_red = pyb.LED(1)
led_green = pyb.LED(2)
led_blue = pyb.LED(3)

# Init of  du counter of LED
counter_led = 0

while 1: # Création d'une boucle infinie
    if counter_led == 0:
        led_red.on()
        led_green.off()
        led_blue.off()
    elif counter_led == 1:
        led_red.off()
        led_green.on()
        led_blue.off()
    else:
        led_red.off()
        led_green.off()
        led_blue.on()
    # we sould like to turn on next led at next iteration
    counter_led = counter_led + 1
    if counter_led > 2:
        counter_led = 0
    time.sleep_ms(500) # Système sleep during 500ms
