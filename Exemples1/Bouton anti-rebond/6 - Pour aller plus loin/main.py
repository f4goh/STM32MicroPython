# Objet du script : Allumer ou éteindre une LED avec un bouton en lui appliquant un 
# filtre anti-rebond inclus de la bibliothèque proposée ici :
# https://gist.github.com/SpotlightKid/0a0aac56606286a80f860b116423c94f

from debounce import DebouncedSwitch

from pyb import Pin # Pour gérer les GPIO

# On configure le bouton en entrée (IN) sur la broche D4.
# Le mode choisi est PULL UP : le potentiel de D4 est forcé à +3.3V
# lorsque le bouton n'est pas appuyé.

button_in = Pin('D4', Pin.IN, Pin.PULL_UP)

# On configure la LED en sortie Push-Pull (OUT_PP) sur la broche D2.
# Le mode choisi est PULL NONE : le potentiel de D2 n'est pas fixé.
led_out = Pin('D2', Pin.OUT_PP, Pin.PULL_NONE) # Broche de la LED

# Numéro du timer utilisé pour l'anti-rebond
TIMER_NUM = const(1) 

# Gestion du bouton et de la LED.
# La LED est pilotée par une fonction "callback" contenue dans une
# "lambda expression" : lambda l: l.value(not l.value())
DebouncedSwitch(button_in, lambda l: l.value(not l.value()), led_out, delay = 50, tid = TIMER_NUM)