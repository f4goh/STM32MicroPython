# Objet du script :
# Valider la connexion d'un module LoRa-E5 à un réseau LoRaWAN privé sur TTN,
# préalablement configuré.
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

# Initialisation du module LoRa-E5 
loRa = LoRa(9600, UART_WB55, DataReceiveCallback = None)

# Paramètres d'identification du module pour sa connexion au réseau LoRaWAN
status = loRa.setIdentify(DevAddr = devAddr,AppEui = appEui,AppKey = appKey)

# Affichage des différents paramètres du réseau LoRaWAN
def PrintLoRaParameters():
	identify = loRa.getIdentify()
	if(identify != -1):
		print("#####################################################################")
		print("########## INITIALIZE                                        ########")
		print("#####################################################################")
		print("LORA_DRIVER_VERSION: " + loRa.getDriverVersion())
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
	# Essaie de se connecter au réseau
	joinStatus = False
	tryJoin = 0
	while joinStatus == False:
		# Join LoRaWAN
		print("#### = Try join n°" + str(tryJoin + 1))
		status = loRa.join()
		if status == -1:
			print("#### = Join Fail, retry in " + str(DelayTryJoin) + " seconds.")
			tryJoin += 1
			# Si MaxTryJoin tentatives de connexion ont échoué
			if tryJoin > MaxTryJoin:
				# Reboot de la carte
				print("Reboot!")
				machine.reset()
			sleep_ms(DelayTryJoin * 1000)
		else:
				joinStatus = True
				print("#### = Join sucess.")

# Exécution des fonctions
PrintLoRaParameters() # Affichage des paramètres
JoinNetwork() # Join
