# Objet du script :
# Affiche un texte sur un module OLED contrôlé par un SSD1308.

from time import sleep_ms # Pour temporiser
from machine import Pin, I2C # Pilotes des entrées-sorties et du bus I2C
import ssd1308 # Pilote de l'afficheur

# Initialisation du périphérique I2C
i2c = I2C(1)

# Pause d'une seconde pour laisser à l'I2C le temps de s'initialiser
sleep_ms(1000)

# Liste des adresses I2C des périphériques présents
print("Adresses I2C utilisées : " + str(i2c.scan()))

# Paramétrage des caractéristiques de l'écran
screen_width_pix = 128
screen_length_pix = 32
oled_display = ssd1308.SSD1308_I2C(screen_width_pix, screen_length_pix, i2c)

# Envoi du texte à afficher sur l'écran OLED
oled_display.text('MicroPython OLED!', 0, 0)
oled_display.text('    I2C   ', 0, 10)
oled_display.text('Trop facile !!!', 0, 20)
oled_display.show() # Affichage !

sleep_ms(5000) # Temporisation de cinq secondes
oled_display.clear() # On efface l'écran

