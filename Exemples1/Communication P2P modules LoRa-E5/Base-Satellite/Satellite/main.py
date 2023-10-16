# Objet du script : Echanges de messages LoRa entre deux modules LoRa-E5.
# Ce script est celui d'une station MEASURE qui réalise une mesure de température
# avec un capteur BME280 et la partage avec la station COMMAND via LoRa.
# MESURE attend ensuite un message retour de COMMAND qui lui donnera l'ordre de
# procéder à une nouvelle mesure de température, etc.
# Matériel :
# - Un module I2C afficheur OLED SSD1327 (Grove 1.12” OLED displays v2.1)
# - Un module UART Grove LoRa-E5
# - Une carte d'extension Grove pour Arduino
# - Une carte NUCLEO-WB55

from machine import UART, I2C # Pour piloter l'UART et l'I2C
from time import sleep # pour temporiser
import ssd1327 # Pilote de l'afficheur Grove - OLED Display 1.12" (96 x 96)

# On utilise l'I2C n°1 de la carte NUCLEO-WB55 
i2c1 = I2C(1)

# Pause d'une seconde pour laisser à l'I2C le temps de s'initialiser
sleep(1)

# Initialisation de l'afficheur
display = ssd1327.SEEED_OLED_96X96(i2c1) 
display.clear() # On efface l'écran

# Variables globales pour mémoriser les mesures de température 
prev_temp = "NA"
temp = "NA"

import bme280 # Pilote du capteur  de température
sensor = bme280.BME280(i2c=i2c1) # Initialisation du capteur

# Définition de la fonction de la station ...
STATION_ID = 'MEASURE_01'

# Ordre de prise de mesure en provenance de la station de commande
MEA = 'GO' 

# Constantes relatives au paramétrage de l'UART
DELAY_TIMEOUT = const(1000) # Durée (en millisecondes) pendant laquelle l'UART attend de reçevoir un message
BAUDRATE = const(9600) # Débit, en bauds, de la communication série
UART_NUMBER = const(2) # Identifiant de l'UART de la carte NUCLEO-WB55 qui sera utilisé
RX_BUFF = const(512) # Taille du buffer de réception (les messages reçus seront tronqués à ce nombre de caractères)
EOL = "\n\r" # Terminaison de commande pour valider l'envoi

# Initialisation de l'UART
uart = UART(UART_NUMBER, BAUDRATE, timeout = DELAY_TIMEOUT, rxbuf = RX_BUFF)

# Fonction de service de l'interruption de réception de l'UART
@micropython.native # Optimise le bytecode pour STM32
def receive(uart_object):

	# Buffer de réception
	message_received = bytearray(RX_BUFF)
	
	# Lecture des caractères reçus
	message_received = uart_object.read()

	# Si réception d'un message
	if not (message_received is None):
		 
		# Affiche le message complet
		# print('Message reçu : ' +  message_received.decode("utf-8"), end='')
		
		# Transforme le en chaîne de caractères
		str_message = str(message_received)
		
		# Recherche les symboles "" dans la chaîne
		if(str_message.count('''"''') == 2 and str_message.find('+TEST: RX') > 0 ):
			
			# S'il y en a deux, récupère la payload contenue entre eux
			str_message = str_message.split('''"''')[1]
			
			# Essaie de convertir la payload du format hexadécimal en chaîne de caractères
			try:
				str_message = bytearray.fromhex(str_message).decode()
			except:
				str_message = ''
		
			# Si la payload reçue est MEA, nouvelle séquence mesure - transmission
			if str_message == MEA:
				# Affiche la payload
				print('Message reçu : ' + str_message)
				measure_transmit_sequence()
					
# On active l'interruption de l'UART (vecteur d'interruption) pour la réception
irq_uart = uart.irq(receive, UART.IRQ_RXIDLE, False)

# Mesure de température avec le BME280
def get_temp():
		
	# Important : siganle que temp et glob_temp sont les variables
	# globales définies plus haut
	global  temp, prev_temp
		
	# Lecture des valeurs mesurées
	bme280data = sensor.values
		
	# Récupération de la température et arrondi à une décimale
	temp = str(round(bme280data[0],1))
		
	# Affichage de la nouvelle température mesurée
	# et de celle qui précédait.
	display.clear()
	display.text(STATION_ID, 0, 0, 255) 
	display.text("T = " + temp + " C", 0, 9, 255)
	display.text("Prev " + prev_temp + " C", 0, 19, 255)
	display.show()
			
	# Sauvegarde pour l'itération suivante
	prev_temp = temp

# Configuration du module en réception
def set_receiver_mode():
	print("-" * 55)
	print("Initialisation du mode récepteur")
	uart.write('AT+MODE=TEST' + EOL)
	sleep(2)
	# Fréquence 866 MHz, puissance 20 dBm
	uart.write("AT+TEST=RFCFG,866,SF12,125,12,15,20,ON,OFF,OFF" + EOL)
	sleep(2)
	uart.write('AT+TEST=RXLRPKT' + EOL)
	sleep(2)
	print("L'objet est en mode récepteur !")
	print("-" * 55)
	
# Configuration du module en émission
def set_transmitter_mode():
	print("-" * 55)
	print("Initialisation du mode émetteur")
	uart.write('AT+MODE=TEST' + EOL)
	sleep(2)
	# Fréquence 866 MHz, puissance 20 dBm
	uart.write("AT+TEST=RFCFG,866,SF12,125,12,15,20,ON,OFF,OFF" + EOL)
	sleep(2)
	print("L'objet est en mode émetteur !")
	print("-" * 55)

# Séquence de la station MEASURE
def measure_transmit_sequence():
	# 1 - Passe en mode émetteur
	set_transmitter_mode()
	# 2 - Mesure et envoie la température en LoRa
	get_temp()
	message_sent = '''AT+TEST=TXLRSTR,''' + '''"'''+ STATION_ID + '|' + temp + '''"'''
	uart.write( message_sent + EOL)
	print('Message envoyé : ', end='')
	print(message_sent)
	# 3 - Passe en mode récepteur
	set_receiver_mode()
	# 4 - Si un message est reçu de la station COMMAND, recommence à 
	#  partir de l'étape 1 (géré par l'interruption de réception de l'UART)



print('Je suis ' + STATION_ID)
sleep(5)

# Lance une première séquence mesure + transmission
# Les suivantes seront lancées par l'interruption de réception de l'UART
measure_transmit_sequence()