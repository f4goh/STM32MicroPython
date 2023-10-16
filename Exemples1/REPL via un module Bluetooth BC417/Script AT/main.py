# Objet du script : Emission / Réception de messages via UART en mode ligne de commande
# Ce script est utile pour dialoguer avec des modules dotés de firmwares AT.

from machine import UART # Pour piloter l'UART

# Constantes relatives au paramétrage de l'UART
DELAY_TIMEOUT = const(1000) # Durée (en millisecondes) pendant laquelle l'UART attend de reçevoir un message
BAUDRATE = const(9600)	# Débit, en bauds, de la communication série
UART_NUMBER = const(2)	# Identifiant de l'UART de la carte NUCLEO-WB55 qui sera utilisé
RX_BUFF = const(512)	# Taille du buffer de réception (les messages reçus seront tronqués 
						# à ce nombre de caractères)

EOL = "" # Terminaison de commande pour valider l'envoi

# Initialisation de l'UART
uart = UART(UART_NUMBER, BAUDRATE, timeout = DELAY_TIMEOUT, rxbuf = RX_BUFF)

# Fonction de service de l'interruption de réception de l'UART
@micropython.native # Optimise le bytecode pour STM32
def Reception(uart_object):

	# Lecture des caractères reçus
	message_received = uart_object.read()

	# Si réception d'un message
	if not (message_received is None):
		# Affiche le message reçu
		print("Message reçu : " + message_received.decode("utf-8"))
	
	print("Entrez votre commande : ", end='')
		
# On active l'interruption de l'UART (vecteur d'interruption) pour la réception
irq_uart = uart.irq(Reception, UART.IRQ_RXIDLE, False)

# Pour gérer l'envoi de messages
@micropython.native # Optimise le bytecode pour STM32
def Emission():
	
	while True:
	
		# Prompt de saisie d'un message (au clavier)
		message_sent = input()
		
		# Envoi du message saisi
		uart.write(message_sent + EOL)
		print("Envoyé : " + str(message_sent))

# Appel de la fonction principale
Emission()