# Objet du script : Implémentation du protocole GATT Blue-ST pour un périphérique
# Définition d'un service _ST_APP_SERVICE avec deux caractéristiques :
# 1 - SWITCH : pour éteindre et allumer une LED du périphérique depuis un central
# 2 - TEMPERATURE : pour envoyer une mesure de température du périphérique à un central 

import bluetooth # Pour gérer le BLE
from ble_advertising import adv_payload # Pour gérer l'advertising GAP
from struct import pack # Pour agréger les octets envoyés par les trames BLE
from micropython import const # Pour définir des constantes entières
import pyb # Pour gérer les LED

# Constantes définies pour le protocole Blue-ST
_IRQ_CENTRAL_CONNECT    = const(1)
_IRQ_CENTRAL_DISCONNECT = const(2) 
_IRQ_GATTS_WRITE        = const(3)

# Pour les UUID et les codes, on se réfère à la documentation du SDK Blue-ST disponible ici :
# https://www.st.com/resource/en/user_manual/dm00550659-getting-started-with-the-bluest-protocol-and-sdk-stmicroelectronics.pdf.

# 1 - Définition du service personnalisé selon le SDK Blue-ST

# Indique que l'on va communiquer avec une appli conforme au protocole Blue-ST :
_ST_APP_UUID = bluetooth.UUID('00000000-0001-11E1-AC36-0002A5D5C51B')

# UUID d'une caractéristique de proximity
_PROXIMITY_UUID = (bluetooth.UUID('02000000-0001-11E1-AC36-0002A5D5C51B'), bluetooth.FLAG_NOTIFY)

# UUID d'une caractéristique d'interrupteur
_SWITCH_UUID = (bluetooth.UUID('20000000-0001-11E1-AC36-0002A5D5C51B'), bluetooth.FLAG_WRITE|bluetooth.FLAG_NOTIFY)

# Le service contiendra ces deux caractéristiques
_ST_APP_SERVICE = (_ST_APP_UUID, (_PROXIMITY_UUID, _SWITCH_UUID))

# 2 - Construction de la trame (contenu du message) d'avertising GAP
_PROTOCOL_VERSION = const(0x01) # Version du protocole
_DEVICE_ID = const(0x80) # Carte NUCLEO générique
_DEVICE_MAC = [0x12, 0x34, 0x56, 0x78, 0x9A, 0xBC] # Adresse matérielle MAC fictive
_FEATURE_MASK = const(0x22000000) # Services sélectionnés : proximity (2^25) et interrupteur (2^29)

# Explication du calcul du masque déterminant les caractéristiques du service actif (_FEATURE_MASK)
# A chaque caractéristique est associé un code binaire. On doit simplement sommer les codes de toutes les caractéristiques
# que l'on souhaite exposer avec GATT :

# Caractéristique SWITCH : code = 2^29 =      100000000000000000000000000000 (en binaire) = 20000000  (en hexadécimal)
# Caractéristique PROXIMITY : code = 2^25 =   000010000000000000000000000000 (en binaire) = 02000000   en hexadécimal)
# _FEATURE_MASK = SWITCH + PROXIMITY =        100010000000000000000000000000 (en binaire) = 22000000  (en hexadécimal)

# Trame d'avertising : concaténation des informations avec la fonction Micropython "pack" 
# La chaîne '>BBI6B' désigne le format des arguments, voir la documention de pack ici : https://docs.python.org/3/library/struct.html
_MANUFACTURER = pack('>BBI6B', _PROTOCOL_VERSION, _DEVICE_ID, _FEATURE_MASK, *_DEVICE_MAC)

# Initialisation des LED
red_led = pyb.LED(1)
blue_led = pyb.LED(3)

class BLESensor:

	# Initialisation, démarrage de GAP et publication radio des trames d'advertising
	def __init__(self, ble, name='WB55-MPY'):
		self._ble = ble
		self._ble.active(True)
		self._ble.irq(self._irq)
		((self._proximity_handle,self._switch_handle),) = self._ble.gatts_register_services((_ST_APP_SERVICE, ))
		self._connections = set()
		self._payload = adv_payload(name=name, manufacturer=_MANUFACTURER)
		self._advertise()
		self._handler = None

	# Gestion des évènements BLE...
	def _irq(self, event, data):
		# Si un central a envoyé une demande de connexion
		if event == _IRQ_CENTRAL_CONNECT:
			conn_handle, _, _, = data
			# Se connecte au central (et arrête automatiquement l'advertising)
			self._connections.add(conn_handle)
			print("Connecté")
			blue_led.on() # Allume la LED bleue

		# Si le central a envoyé une demande de déconnexion
		elif event == _IRQ_CENTRAL_DISCONNECT:
			conn_handle, _, _, = data
			self._connections.remove(conn_handle)
			# Relance l'advertising pour permettre de nouvelles connexions
			self._advertise()
			print("Déconnecté")

		# Si une écriture est détectée dans la caractéristique SWITCH (interrupteur) de la LED
		elif event == _IRQ_GATTS_WRITE:
			conn_handle, value_handle, = data
			if conn_handle in self._connections and value_handle == self._switch_handle:
				
				# Lecture de la valeur de la caractéristique
				data_received = self._ble.gatts_read(self._switch_handle)
				self._ble.gatts_write(self._switch_handle, pack('<HB', 1000, data_received[0]))
				self._ble.gatts_notify(conn_handle, self._switch_handle)
				# Selon la valeur écrite, on allume ou on éteint la LED rouge
				if data_received[0] == 1:
					red_led.on() # Allume la LED rouge
				else:
					red_led.off() # Eteint la LED rouge

	# On écrit, dans la caractéristique "proximity", le timestamp (horodatage) et la valeur de la distance
	def set_data_proximity(self, timestamp, distance, notify):
		self._ble.gatts_write(self._proximity_handle, pack('<HH', timestamp, distance))
		if notify:
			for conn_handle in self._connections:
				# Signale au Central (le smartphone) que la caractéristique vient d'être écrite et peut être lue
				self._ble.gatts_notify(conn_handle, self._proximity_handle)

	# Démarre l'advertising avec une période de 5 secondes, précise qu'un central pourra se connecter au périphérique
	def _advertise(self, interval_us=500000):
		self._ble.gap_advertise(interval_us, adv_data=self._payload, connectable=True)
		blue_led.off() # Eteint la LED bleue
