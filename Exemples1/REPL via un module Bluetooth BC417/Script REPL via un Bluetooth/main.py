# Objet du script : Duplication de la console REPL du firmware MicroPython
# sur un UART associé à un module Grove Serial Bluetooth V3.01.
# Il faut préalablement avoir configuré correctement le module sur un hôte
# (un PC Windows par exemple) qui exécutera le terminal série.

from machine import UART # Pour piloter l'UART
from os import dupterm  # Fonction pour cloner le terminal REPL

# Constantes relatives au paramétrage de l'UART
DELAY_TIMEOUT = const(1000) # Durée (en millisecondes) pendant laquelle l'UART attend de reçevoir un message
BAUDRATE = const(9600)	# Débit, en bauds, de la communication série
UART_NUMBER = const(2)	# Identifiant de l'UART de la carte NUCLEO-WB55 qui sera utilisé
RX_BUFF = const(512)	# Taille du buffer de réception (les messages reçus seront tronqués 
						# à ce nombre de caractères)

# Initialisation de l'UART du module Bluetooth
bt_uart = UART(UART_NUMBER, BAUDRATE, timeout = DELAY_TIMEOUT, rxbuf = RX_BUFF)

# Duplication de la console REPL sur le port série du module Bluetooth
dupterm( bt_uart )

# Message de confirmation
print("Console REPL accessible par le module Bluetooth !")
