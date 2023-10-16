# Objet du script : Echange de messages entre deux modules LoRa-E5.
# Le script est prévu pour fonctionner sur la station COMMAND qui reçoit les mesures 
# de températures envoyées par une (des) station(s) MEASURE et va lui en commander de nouvelles  
# toutes les cinq minutes, à l'aide de l'interruption d'un timer.
# Matériel :
# - Un module I2C afficheur OLED SSD1306 ou SSD1308 (Grove - OLED Display 0.96 inch V1.1)
# - Un module UART Grove LoRa-E5
# - Une carte d'extension Grove pour Arduino
# - Une carte NUCLEO-WB55

from machine import UART, I2C # Pour piloter l'UART et l'I2C
from time import sleep # pour temporiser
import ssd1308 # Pilote de l'afficheur

# Initialisation du contrôleur de bus I2C numéro 1
i2c1 = I2C(1)

# Pause d'une seconde pour laisser à l'I2C le temps de s'initialiser
sleep(1)

# Paramétrage des caractéristiques de l'afficheur OLED
screen_width_pix = const(128)
screen_length_pix = const(32)
display = ssd1308.SSD1308_I2C(screen_width_pix, screen_length_pix, i2c1)
display.clear()

# Identifiant de la station
STATION_ID = 'COMMAND_01'

# Ordre de prise de mesure en provenance pour la station de mesure
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
		msg = str(message_received)
	 
		# On s'assure qu'on traite bien le message qui nous intéresse.
		# Pour rappel, le message que nous allons exploiter a cette structure :
		# +TEST: LEN:15, RSSI:-79, SNR:4 +TEST: RX "4D4541535552455F30317C32362E37"
		if msg.count('''"''')==2 and msg.find('+TEST: RX')>0 and msg.find('RSSI:')>0 :
 
			# Découpe le message reçu de sorte à extraire la payload et le RSSI
 
			data = msg.split('''"''')
			pyld = data[1]
			rssi = (data[0].split(', '))[1]
				 
			# Convertit la payload du format hexadécimal en chaîne de caractères
			try:
				pyld = bytearray.fromhex(pyld).decode()
			except:
				pyld = ''
								
			disp = pyld.split('|')
			
			# Affichage sur l'OLED			
			display.clear()
			display.text(disp[0], 0, 0)
			display.text("T = " + disp[1] + " C", 0, 10)
			display.text(rssi + ' dBm', 0, 20)
			display.show()
			
			# Affiche les données reçues sur le port série 
			print('Payload reçue de ' + disp[0] + ' : ' + disp[1] + 'C, ' + rssi + ' dBm')
			
# On active l'interruption de l'UART (vecteur d'interruption) pour la réception
irq_uart = uart.irq(receive, UART.IRQ_RXIDLE, False)
	
# Variable globale qui servira de base de temps
n = 0
 
# Nombre de secondes entre deux consignes envoyées aux stations de mesure 
MEASURE_TIMING = const(300) # 300 secondes, soit 5 minutes
 
# Routine de service de l'interruption (ISR) de dépassement de compteur du timer 1.
# Elle incrémente la variable n de 1 à chaque interruption de dépassement du timer.
@micropython.native # Optimise le bytecode pour STM32
def tick(timer):
	global n  # TRES IMPORTANT, ne pas oublier le mot-clef "global" devant la variable n
	n += 1
 
# Démarre le timer 1 à la fréquence de 1 Hz.
# Assigne la fonction "tick" à l'interruption de dépassement de compteur du timer 1.
tim1 = pyb.Timer(1, freq=1, callback=tick)

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

print('Je suis ' + STATION_ID)
sleep(5)

set_receiver_mode()

while True:

	# Lorque n atteint MEASURE_TIMING, il est remis à zéro et la station envoie le message MEA

	if n > MEASURE_TIMING:
		n = 0
		# Passe en mode émetteur
		set_transmitter_mode()
		message_sent = '''AT+TEST=TXLRSTR,''' + '''"''' + MEA + '''"'''
		uart.write( message_sent + EOL)
		print('Message envoyé : ' + message_sent)
		# Passe en mode récepteur
		set_receiver_mode()