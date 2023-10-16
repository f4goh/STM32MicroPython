# Objet du script :
# Connexion d'un module LoRa-E5 à un réseau LoRaWAN privé sur TTN,
# préalablement configuré.
# Publication de données de température, humidité et pression sur TTN au
# format Cayenne LPP
# Cet exemple est obtenu à partir des ressources mises à disposition par
# Vittascience :
# https://github.com/vittascience/stm32-libraries/tree/main/grove_modules

# Importation des différents pilotes
import machine
from stm32_LoRa import *
from utime import sleep_ms

# Port série de la NUCLEO_WB55
UART_WB55 = const(2)

# Identifiants sur le réseau LoRaWAN
devAddr = '42 00 1A 4A'
appEui = '00 00 00 00 00 00 00 00'
appKey = '75 10 63 98 B1 15 8E 4E D0 33 19 DC 65 27 88 AB'

# Temporisations diverses
DelayRebootLostConnection = 300 # Exprimé en minutes
DelayTryJoin = 10 # Exprimé en secondes
MaxTryJoin = int((DelayRebootLostConnection * 60) / DelayTryJoin)
DelaySend = 30 # Exprimé en secondes


# Fonction de callback chargée de traiter et réagir aux messages envoyés par le serveur
# LoRaWAN au module LoRa-E5 
def DataReceived(Port = 0, DataReceived = b''):
	print("#### = Data received")
	print("Data received on PORT: " + str(Port) +
				", Size = "+ str(len(DataReceived)) +
				", Data = "+str([hex(x) for x in list(DataReceived)]))


# Initialisation du module LoRa-E5 
loRa = LoRa(9600, UART_WB55, DataReceiveCallback = DataReceived)

# Paramètres d'identification du module pour sa connexion au réseau LoRaWAN
status = loRa.setIdentify(DevAddr = devAddr,AppEui	= appEui,AppKey	= appKey)

# Affichage des différents paramètres du réseau LoRaWAN
def PrintLoRaParameters():
	identify = loRa.getIdentify()
	if(identify != -1):
		print("#####################################################################")
		print("########## INITIALIZE                                        ########")
		print("#####################################################################")
		print("LORA_DRIVER_VERSION : " + loRa.getDriverVersion())
		print("#### " + loRa.getMode() + " ####")
		print("#### AppKey: " + identify['AppKey'])
		print("#### DevEUI: " + identify['DevEui'])
		print("#### AppEUI: " + identify['AppEui'])
		print("#### DevAddr: " + identify['DevAddr'])
	else:
		print("#### = Read identify fail.\nReboot!")
		sleep_ms(2000)
		machine.reset()
	if status == -1:
		print("#### = Initialize fail.\nReboot!")
		sleep_ms(2000)
		machine.reset()
	else:
		print("#### = Initialize success.")

# Etablissement de la connexion ("join") LoRaWAN
def JoinNetwork():
	# Try to join network
	joinStatus = False
	tryJoin = 0
	while joinStatus == False:
		# Join LoRaWAN
		print("#### = Try join n°" + str(tryJoin + 1))
		status = loRa.join()
		if status == -1:
			print("#### = Join Fail, retry in " + str(DelayTryJoin) + " seconds.")
			tryJoin += 1
			if tryJoin > MaxTryJoin:
				# Reboot board
				print("Reboot!")
				machine.reset()
				sleep_ms(DelayTryJoin * 1000)
		else:
				joinStatus = True
				print("#### = Join sucess.")

# Emission de trames au format Cayenne LPP contenant les mesures du BME280
def GetSendData():

	# Temporisation en millisecondes, fréquence d'émission des trames
	TEMPO = const(600000)

	from time import sleep_ms # Pout temporiser
	from machine import I2C # Pilote du bus I2C
	import bme280 # Pilote du capteur 

	# On utilise l'I2C n°1 de la carte NUCLEO-WB55 pour communiquer avec le capteur
	i2c1 = I2C(1)

	# Pause d'une seconde pour laisser à l'I2C le temps de s'initialiser
	sleep_ms(1000)

	# Liste des adresses I2C des périphériques présents
	print("Adresses I2C utilisées : " + str(i2c1.scan()))

	# Instanciation du capteur
	sensor = bme280.BME280(i2c=i2c1)
	
	# Décompte des tentatives d'émission d'une trame 
	trySend = 0
	
	# Initialisation d'un tableau de 11 octets qui contiendra la trame
	# LoRaWAN au format Cayenne LPP
	loRaFrame = [0x00] * 11
	
	while True:
		
			# Lecture des valeurs mesurées
			bme280data = sensor.values
	
			# Préparation des mesures
			temp = bme280data[0]
			press = bme280data[1]
			humi = bme280data[2]

			# Affichage des mesures
			print('=' * 40)  # Imprime une ligne de séparation
			print("Température : %.1f °C" %temp)
			print("Pression : %d hPa" %press)
			print("Humidité relative : %d %%" %humi)
			
			# Construction de la trame LoRaWAN au format Cayenne LPP
			# Pour comprendre cette étape, consultez les lien suivants :
			# - https://www.framboise314.fr/mise-en-place-dune-passerelle-et-dun-noeud-lora/#Le_codage_Cayenne_LPP
			# - https://docs.mydevices.com/docs/lorawan/cayenne-lpp
			
			temp = int(temp * 10)
			press = int(press * 10)
			humi = int(humi * 2)
			
			loRaFrame[0] = 0x01 # Index de la donnée (tout simplement 1, 2, 3, 4, etc.).
			loRaFrame[1] = 0x67 # Identifiant du type de la donnée
			loRaFrame[2] = (temp >> 8) & 0xFF # Donnée codée sur 16 bits, extraction du bit de poids faible
			loRaFrame[3] = temp & 0xFF # Donnée codée sur 16 bits, extraction du bit de poids fort
			
			loRaFrame[4] = 0x02 # Index de la donnée (tout simplement 1, 2, 3, 4, etc.).
			loRaFrame[5] = 0x73 # Identifiant du type de la donnée
			loRaFrame[6] = (press >> 8) & 0xFF # Donnée codée sur 16 bits, extraction du bit de poids faible
			loRaFrame[7] = press & 0xFF # Donnée codée sur 16 bits, extraction du bit de poids fort
			
			loRaFrame[8] = 0x03 # Index de la donnée (tout simplement 1, 2, 3, 4, etc.).
			loRaFrame[9] = 0x68 # Identifiant du type de la donnée
			loRaFrame[10] = humi # Donnée codée sur 8 bits
			
			# Emission de la trame LoRaWAN
			
			print("#### = Send data.")
			trySend += 1
			sendStatus = loRa.sendData(loRaFrame, Port=1, NeedAck= False)
			
			# Si l'émission échoue, reessaye trySend fois puis reboote
			if sendStatus == -1:
				print("#### = Join fail.")
				if trySend > MaxTrySend:
					# Reboot board
					print("Reboot!")
					machine.reset()
			else:
				print("#### = Send success.")
				trySend = 0

			# Place le module LoRa-E5 en mode veille
			print("#### = LoRa module enter low power mode.")
			loRa.enterLowPowerMode()
			
			# Place le STM32WB55 en mode basse consommation
			pyb.wfi() 
			
			# Temporisation jusqu"à l'envoi de la prochaine trame
			sleep_ms(TEMPO)

# Exécution des fonctions
PrintLoRaParameters() # Affichage des paramètres
JoinNetwork() # Connexion à TTN
GetSendData() # Emission de trames au format Cayenne LPP