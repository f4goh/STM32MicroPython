# Pilote pour le module Grove capteur de gaz basé sur MICS6814 adapté à partir de la 
# source : https://github.com/aparcar/groove-multichannel-gas-sensor-micropyton
# Fiche technique : https://www.sgxsensortech.com/content/uploads/2015/02/1143_Datasheet-MiCS-6814-rev-8.pdf

DEFAULT_I2C_ADDR = const(0x04)

# Version du firmware, valeur à 1126 s'il est à jour en version 2
ADDR_IS_SET = const(0) 

# Adresse des registres de sortie par défaut (fixés en usine)
ADDR_FACTORY_ADC_NH3 = const(2)
ADDR_FACTORY_ADC_CO = const(4)
ADDR_FACTORY_ADC_NO2 = const(6)

# Adresse des registres de sortie après calibrage utilisateur
ADDR_USER_ADC_NH3 = const(8)
ADDR_USER_ADC_CO = const(10)
ADDR_USER_ADC_NO2 = const(12)

# Adresse I2C du module
ADDR_I2C_ADDRESS = const(20)

# Commandes du MICS6814
CH_VALUE_NH3 = const(1)
CH_VALUE_CO = const(2)
CH_VALUE_NO2 = const(3)
CMD_READ_EEPROM = const(6)
CMD_WRITE_EEPROM = const(7)
CMD_CONTROL_LED = const(10)
CMD_CONTROL_PWR = const(11)

from math import pow # Fonction "puissance"
from time import sleep_ms # Pour temporiser

class MICS6814:

	# Initialisations
	def __init__(self, i2c, addr=DEFAULT_I2C_ADDR):
		self.i2c = i2c
		self.i2c.scan()
		self.addr = addr
		self.version = self.get_version()

	# Envoi de plusieurs octets à la suite (adresses registres et commandes) sur le bus I2C
	def cmd(self, cmd):
		self.i2c.writeto(self.addr, bytes(cmd))
		raw = self.i2c.readfrom(self.addr, 2)
		dta = raw[0];
		dta <<= 8;
		dta += raw[1];
		return dta

	# Version du firmware
	def get_version(self):
		if self.cmd([CMD_READ_EEPROM, ADDR_IS_SET]) == 1126:
			print("Version du firmware = 2\n")
			return 2
		else:
			print("Version du firmware = 1")
			print("Version non supportée\n")
			from sys import exit
			exit(1)
	
	# Pour changer l'adresse I2C du module
	def change_addr(self, new_addr):
		self.cmd([35, new_addr])
		self.addr = new_addr

	# Mise en chauffe du capteur
	def heater_on(self):
		self.cmd([CMD_CONTROL_PWR, 1])

	# Arrêt de la chauffe du capteur
	def heater_off(self):
		self.cmd([CMD_CONTROL_PWR, 0])

	# Allume la LED intégrée du module
	def led_on(self):
		self.cmd([CMD_CONTROL_LED, 1])

	# Eteint la LED intégrée du mdoule
	def led_off(self):
		self.cmd([CMD_CONTROL_LED, 0])

	# Affiche les paramètres enregistrés dans l'EEPROM du module
	def display_eeprom(self):
		
		print("ADDR_I2C_ADDRESS = %d" %self.cmd([CMD_READ_EEPROM, ADDR_I2C_ADDRESS]))
		print("ADDR_IS_SET = %d" %self.cmd([CMD_READ_EEPROM, ADDR_IS_SET]))
		
		print("ADDR_FACTORY_ADC_NH3 = %d" %self.cmd([CMD_READ_EEPROM, ADDR_FACTORY_ADC_NH3]))
		print("ADDR_FACTORY_ADC_CO = %d" %self.cmd([CMD_READ_EEPROM, ADDR_FACTORY_ADC_CO]))
		print("ADDR_FACTORY_ADC_NO2 = %d" %self.cmd([CMD_READ_EEPROM, ADDR_FACTORY_ADC_NO2]))
		
		print("ADDR_USER_ADC_NH3 = %d" %self.cmd([CMD_READ_EEPROM, ADDR_USER_ADC_NH3]))
		print("ADDR_USER_ADC_CO = %d" %self.cmd([CMD_READ_EEPROM, ADDR_USER_ADC_CO]))
		print("ADDR_USER_ADC_NO2 = %d" %self.cmd([CMD_READ_EEPROM, ADDR_USER_ADC_NO2]))
		print(" ")

	# Obtient la concentration (supposée) de CO (ppm), renvoie -1 si problème de mesure
	def get_co(self):
	
		A0_1 = 0
		An_1 = 0
		ratio1 = 0

		try:
			A0_1 = float(self.cmd([CMD_READ_EEPROM, ADDR_USER_ADC_CO]))
			An_1 = float(self.cmd([CH_VALUE_CO]))
			ratio1 = An_1 / A0_1 * (1023.0 - A0_1) / (1023.0 - An_1)
			c = round(4.385 * pow(ratio1, -1.179)) 
		except:
			c = -1
		finally:
			return c

	# Obtient la concentration (supposée) de NO2 (ppm), renvoie -1 si problème de mesure
	def get_no2(self):

		A0_2 = 0
		An_2 = 0
		ratio2 = 0

		try:
			A0_2 = float(self.cmd([CMD_READ_EEPROM, ADDR_USER_ADC_NO2]))
			An_2 = float(self.cmd([CH_VALUE_NO2]))
			ratio2 = An_2 / A0_2 * (1023.0 - A0_2) / (1023.0 - An_2)
			c = round(0.14588 * pow(ratio2, 1.007), 2) 
		except:
			c = -1
		finally:
			return c

	# Obtient la concentration (supposée) de NH3 (ppm), renvoie -1 si problème de mesure
	def get_nh3(self):

		A0_0 = 0
		An_0 = 0
		ratio0 = 0

		try:
			A0_0 = float(self.cmd([CMD_READ_EEPROM, ADDR_USER_ADC_NH3]))
			An_0 = float(self.cmd([CH_VALUE_NH3]))
			ratio0 = An_0 / A0_0 * (1023.0 - A0_0) / (1023.0 - An_0)
			c = round(0.6803 * pow(ratio0, -1.67)) 
		except:
			c = -1
		finally:
			return c

	# Obtient la concentration (supposée) de C3H8 (ppm), renvoie -1 si problème de mesure
	def get_c3h8(self):

		A0_0 = 0
		An_0 = 0
		ratio0 = 0

		try:
			A0_0 = float(self.cmd([CMD_READ_EEPROM, ADDR_USER_ADC_NH3]))
			An_0 = float(self.cmd([CH_VALUE_NH3]))
			ratio0 = An_0 / A0_0 * (1023.0 - A0_0) / (1023.0 - An_0)
			c = round(570.164 * pow(ratio0, -2.518)) 
		except:
			c = -1
		finally:
			return c

	# Obtient la concentration (supposée) de C4H10 (ppm), renvoie -1 si problème de mesure
	def get_c4h10(self):

		A0_0 = 0
		An_0 = 0
		ratio0 = 0

		try:
			A0_0 = float(self.cmd([CMD_READ_EEPROM, ADDR_USER_ADC_NH3]))
			An_0 = float(self.cmd([CH_VALUE_NH3]))
			ratio0 = An_0 / A0_0 * (1023.0 - A0_0) / (1023.0 - An_0)
			c = round(398.107 * pow(ratio0, -2.138)) 
		except:
			c = -1
		finally:
			return c

	# Obtient la concentration (supposée) de CH4 (ppm), renvoie -1 si problème de mesure
	def get_ch4(self):

		A0_1 = 0
		An_1 = 0
		ratio1 = 0

		try:
			A0_1 = float(self.cmd([CMD_READ_EEPROM, ADDR_USER_ADC_CO]))
			An_1 = float(self.cmd([CH_VALUE_CO]))
			ratio1 = An_1 / A0_1 * (1023.0 - A0_1) / (1023.0 - An_1)
			c = round(630.957 * pow(ratio1, -4.363))
		except:
			c = -1
		finally:
			return c

	# Obtient la concentration (supposée) de H2 (ppm), renvoie -1 si problème de mesure
	def get_h2(self):

		A0_1 = 0
		An_1 = 0
		ratio1 = 0

		try:
			A0_1 = float(self.cmd([CMD_READ_EEPROM, ADDR_USER_ADC_CO]))
			An_1 = float(self.cmd([CH_VALUE_CO]))
			ratio1 = An_1 / A0_1 * (1023.0 - A0_1) / (1023.0 - An_1)
			c = round(0.73 * pow(ratio1, -1.8)) 
		except:
			c = -1
		finally:
			return c

	# Obtient la concentration (supposée) de C2H5OH (ppm), renvoie -1 si problème de mesure
	def get_c2h5oh(self):
		A0_1 = 0
		An_1 = 0
		ratio1 = 0

		try:
			A0_1 = float(self.cmd([CMD_READ_EEPROM, ADDR_USER_ADC_CO]))
			An_1 = float(self.cmd([CH_VALUE_CO]))
			ratio1 = An_1 / A0_1 * (1023.0 - A0_1) / (1023.0 - An_1)
			c = round(1.622 * pow(ratio1, -1.552)) 
		except:
			c = -1
		finally:
			return c

	# Affiche les valeurs obtenues avec les ADC pour calculer les concentrations de gaz
	# Affiche les concentrations de gaz calculées sur la base de la calibration
	def flush_raw(self):

		A0_0 = self.cmd([CMD_READ_EEPROM, ADDR_USER_ADC_NH3])
		A0_1 = self.cmd([CMD_READ_EEPROM, ADDR_USER_ADC_CO])
		A0_2 = self.cmd([CMD_READ_EEPROM, ADDR_USER_ADC_NO2])

		An_0 = self.cmd([CH_VALUE_NH3])
		An_1 = self.cmd([CH_VALUE_CO])
		An_2 = self.cmd([CH_VALUE_NO2])

		print("\nRéférence EEPROM (calibrage) | Valeur actuelle mesurée")
		print(" A0_0 %04d | An_0 %04d " %(A0_0, An_0))
		print(" A0_1 %04d | An_1 %04d " %(A0_1, An_1))
		print(" A0_2 %04d | An_2 %04d " %(A0_2, An_2))
		print(" ")

		print("\nConcentration ambiante (offsets) des gaz (en ppm) : ")
		co = self.get_co()
		print("Offset_CO = %.1f" %co)
		no2 = self.get_no2()
		print("Offset_NO2 = %.1f" %no2)
		nh3 = self.get_nh3()
		print("Offset_NH3 = %.1f" %nh3)
		c3h8 = self.get_c3h8()
		print("Offset_C3H8 = %.1f" %c3h8)
		c4h10 = self.get_c4h10()
		print("Offset_C4H10 = %.1f" %c4h10)
		ch4 = self.get_ch4()
		print("Offset_CH4 = %.1f" %ch4)
		h2 = self.get_h2()
		print("Offset_H2 = %.1f" %h2)
		c2h5oh = self.get_c2h5oh()
		print("Offset_C2H5OH = %.1f" %c2h5oh)

	# Lance la procédure de calibration des trois ADC qui échantilonnent les concentrations de Gaz.
	def do_calibrate(self):

		while True:
		
			a0 = self.cmd([CH_VALUE_NH3])
			a1 = self.cmd([CH_VALUE_CO])
			a2 = self.cmd([CH_VALUE_NO2])

			print("Valeurs ADC initiales a0, a1, a2 : ")
			print("{}\t{}\t{}".format(a0, a1, a2))
			self.led_on()

			cnt = 0
			for i in range(20):

				a0 = self.cmd([CH_VALUE_NH3])
				a1 = self.cmd([CH_VALUE_CO])
				a2 = self.cmd([CH_VALUE_NO2])

				if (a0 - self.cmd([CH_VALUE_NH3])) > 2 or (self.cmd([CH_VALUE_NH3]) - a0) > 2:
					cnt += 1
				if (a1 - self.cmd([CH_VALUE_CO])) > 2 or (self.cmd([CH_VALUE_CO]) - a1) > 2:
					cnt += 1
				if (a2 - self.cmd([CH_VALUE_NO2])) > 2 or (self.cmd([CH_VALUE_NO2]) - a2) > 2:
					cnt += 1

				print("itération : %i, a0 : %d, a1 : %d, a2 : %d" %(i, a0, a1, a2))

				if cnt > 5:
					break
				sleep_ms(10000) 

			self.led_off()
			if cnt <= 5:
				break
			sleep_ms(200)

		print("Valeurs ADC calibrées a0, a1, a2 : ")
		print("{}\t{}\t{}".format(a0, a1, a2))
		
		# Ecriture en EEPROM
		self.cmd([CMD_WRITE_EEPROM, a0 >> 8, a0 & 0xFF, a1 >> 8, a1 & 0xFF, a2 >> 8, a2 & 0xFF ])