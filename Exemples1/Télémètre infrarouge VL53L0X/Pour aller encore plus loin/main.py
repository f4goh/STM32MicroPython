# Source : https://github.com/uceeatz/VL53L0X
# Objets du Script : 
#  - Mesure de distance avec le capteur VL53L0X 
#  - Affichage de la distance sur l'application ST BLE-SENSOR

# Déclage du capteur (en mm, différent pour chaque module)
SENSOR_OFFSET = const(30)

# Intervalle de mesures du capteur
MIN_DIST = const(0)
MAX_DIST = const(2000)

from time import sleep_ms, time # Pour gérer les temporisations et l'horodatage
import bluetooth # Pour gérer le protocole BLE 
import ble_sensor # Pour l'implémentation du protocole GATT Blue-ST
import vl53l0x # Bibliothèque pour le VL53L0X
from machine import I2C
from struct import pack

#Initialisation du bus I2C numéro 1 du STM32WB55 
i2c = I2C(1)

# Pause d'une seconde pour laisser à l'I2C le temps de s'initialiser
sleep_ms(1000)

tof = vl53l0x.VL53L0X(i2c) # Instance du capteur
sleep_ms(500) # Temporisation "de sécurité"
tof.start() # démarrage du capteur
tof.read() # Première mesure "à blanc"
sleep_ms(500) # Temporisation "de sécurité"

ble = bluetooth.BLE() # Instance de la classe BLE
ble_device = ble_sensor.BLESensor(ble) # Instance de la classe Blue-ST

while True:

	try:
		# Mesure de la distance et correction des valeurs aberrantes
		distance =  min(max(tof.read() - SENSOR_OFFSET, MIN_DIST), MAX_DIST)
		print("Distance : %1d mm" %distance)
		# Pause de 1 seconde
		sleep_ms(1000)
	except:
		print("Erreur de mesure")
		break

	# Horodatage
	timestamp = time()
	
	# Envoi en BLE de l'horodatage et de la distance en choisissant de notifier l'application
	ble_device.set_data_proximity(timestamp, distance, notify=1) 

tof.stop() # arrêt du capteur