"""
analog read ADC 12 bits (mots de 16 bits)
"""

from machine import ADC
from time import sleep_ms
import sys

adc = ADC('A0')

while True:
    try:
        valeur=adc.read_u16()
        sleep_ms(100)
        print(valeur//64)
    except KeyboardInterrupt:
        print('Ctrl-C pressed...exiting')
        sys.exit()