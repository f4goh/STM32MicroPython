# Pilote pour les capteur analogiques d'humidité du sol de type :
# - Capacitifs, ex. : https://wiki.seeedstudio.com/Grove-Capacitive_Moisture_Sensor-Corrosion-Resistant/
# - Résistifs, ex. : https://wiki.seeedstudio.com/Grove-Moisture_Sensor/
# Après un premier relevé de mesures dans l'air (résultat : sig_air ) et dans l'eau (résultat : sig_eau )
# il est possible de calibrer le capteur en passant ces deux résultats dans la méthode d'intialisation.

class SOILMOIST:

	# Initialisation
	# sig_air : retour analogique du capteur lorsqu'il est dans l'air
	# sig_eau : retour analogique du capteur lorqu'il est plongé dans l'eau
	def __init__(self, adc, sig_air = 0, sig_water = 4095):
		self._adc = adc
		self._min = sig_air
		self._max = sig_water

	# Mesure analogique "brute"
	def raw(self):
		return self._adc.read()

	# Mesure recentrée dans l'intervalle calibré, en %
	# 0% : Capteur dans l'air
	# 100% : Capteur baignant dans l'eau
	def measure(self):
		return self._map(self._adc.read(), self._min, self._max, 0, 100 )

	# Fonction map de l'API Arduino
	# https://www.arduino.cc/reference/en/language/functions/math/map/
	def _map(self, x, in_min, in_max, out_min, out_max):
		return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min