# Objet du script : Allumer ou éteindre une LED en appuyant sur un bouton.
# Le bouton est géré en "polling" (scrutation) : une boucle infinie
# surveille l'état du bouton.

from pyb import Pin # Pour gérer les GPIO
from time import sleep_ms

# On configure le bouton en entrée (IN) sur la broche D4.
# Le mode choisi est PULL UP : le potentiel de D4 est forcé à +3.3V
# lorsque le bouton n'est pas appuyé.

button_in = Pin('D4', Pin.IN, Pin.PULL_UP)

# On configure la LED en sortie Push-Pull (OUT_PP) sur la broche D2.
# Le mode choisi est PULL NONE : le potentiel de D2 n'est pas fixé.
led_out = Pin('D2', Pin.OUT_PP, Pin.PULL_NONE) # Broche de la LED

# On commence avec la LED éteinte
led_state = 0
led_out.value(led_state)


# Boucle sans clause de sortie ("infinie")
while True :
    # Dans notre configuration button_in.value() vaut 1 lorsque le bouton est enfoncé, 
    # ce qui inverse l'état de la LED

    if button_in.value() == 1:
        led_state = 0
    else:
        led_state = 1
    
    led_out.value(led_state)
    sleep_ms(1000)
    