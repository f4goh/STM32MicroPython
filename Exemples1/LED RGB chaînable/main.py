# Objet du script : câbler ensemble trois modules Grove LED RGB chaînables
# et leur faire afficher dans cet ordre "bleu" (première LED), "blanc" 
# (deuxième LED) et "rouge" (troisième LED)

from machine import Pin # Pour gérer les entrées / sorties
import p9813 # Pour gérer les LED chaînables
from time import sleep # Pour temporiser

# Correspond au connecteur D7 du Grove base shield
pin_clk = Pin('D7', Pin.OUT) # Broche d'horloge
pin_data = Pin('D8', Pin.OUT) # Broche de données

# Nombre de modules LED RGB
num_led = 3

# Instanciation d'une chaîne de 3 modules LED RGB 
chain = p9813.P9813(pin_clk, pin_data, num_led)

# Eteint toutes les LED
chain.reset()

# Temporisation d'une seconde
sleep(1)

# Première LED en bleu
chain[0] = (0, 0, 255)

# Deuxième LED en blanc
chain[1] = (255, 255, 255)

# Troisième LED en rouge
chain[2] = (255, 0, 0)

# Applique les paramètres, allume les LED
chain.write()

# Change la couleur de toutes les LED en rouge
#chain.fill((0,0,255))
#chain.write()

