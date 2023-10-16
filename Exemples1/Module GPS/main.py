# Exemple de décodage de trames GPS à l'aide la lib adafruit_gps https://github.com/alexmrqt/micropython-gps

# Ce code est adapté de l'exemple fourni par Adafruit.
# Il a été testé et fonctionne correctement, en l'état: 
#  - avec le module GPS Grove (SIM28) de Seeed Studio: https://wiki.seeedstudio.com/Grove-GPS/
#  - avec le module Ultimate GPS Breakout d'Adafruit: https://www.adafruit.com/product/746
# En principe, il devrait fonctionner avec tous les modules GPS UART sauf, peut-être les 
# commandes d'itialisation qui sont propres au module PMTK314 du GPS Adafruit :
# https://cdn-shop.adafruit.com/datasheets/PMTK_A11.pdf.

# Attention : les antennes intégrées à ces modules n'étant pas actives, vous serez très certainement
# obligé(e) de tester les modules à l'extérieur, avec un ciel ouvert au-dessus de votre tête, pour 
# acquérir les satellites.

# Consulter Wikipédia pour l'explication des trames NMEA : https://fr.wikipedia.org/wiki/NMEA_0183

from pyb import UART # Classe pour gérer l'UART
import time
import adafruit_gps # Classe pour décoder les trames NMEA

# Ouverture du LPUART sur les broches D0(RX) D1(TX)
# Attention, le Time-Out doit être plus grand que la fréquence d'interrogation du module GPS !
uart = UART(2, 9600, timeout = 5000) 

# Crée une instance du module GPS
gps = adafruit_gps.GPS(uart)

# Initialise le module PMTK314 en précisant quelles trames il renvoie et à quelle fréquence.

# Renvoie les trames GGA et RMC :
gps.send_command('PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0')

# Renvoie les infos minimum (trames RMC seulement, position):
#gps.send_command('PMTK314,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0')

# Demande au GPS de ne plus renvoyer aucune trame (pour économiser l'énergie)
#gps.send_command('PMTK314,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0')

# Demande au GPS de transmettre TOUTES les trames NMEA (mais la lib adafruit_gps
# ne sait pas toutes les décoder) :
#gps.send_command('PMTK314,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0')

# Demande au GPS de renvoyer les trames une fois par seconde:
gps.send_command('PMTK220,1000') # 1000 => 1000 ms <=> 1s
# Si vous augmentez ce délai au delà de 1000 ms, assurez vous que le TimeOut de 
# l'UART est plus grand que sa nouvelle valeur !
# Vous pouvez aussi réduire ce délai. Par exemple, pour deux mesures par seconde:
# gps.send_command('PMTK220,500')
# Mais sachez que si la fréquence devient trop élevée, la lib adafruit_gps ne sera 
# plus forcément capable de décoder les trames assez vite et vous risquerez perdre
# des informations.

last_print = time.ticks_ms() # Mesure du temps initial

print("Acquisition des satellites en cours...")

# Boucle sans clause de sortie avec une temporisation de 1000 ms.
# Affiche la localisation chaque seconde si le "fix" des satellites est validé.

while True:
	# Assurez vous d'appeler gps.update() à chaque itération et au moins deux fois
	# plus souvent que la fréquence des trames renvoyées par le module GPS.
	# Cette méthode renvoie un bool qui prend la valeur 'True' si elle est parvenue à décoder une nouvelle trame.
	# Nous ne vérifions pas son retour et testons plutôt la propriété 'has_fix'.
	gps.update()
	
	current = time.ticks_ms() # Mesure du temps actuel
	
	if current-last_print >= 1000: # Si le temps écoulé est au moins égal à 1 seconde
	
		last_print = current # mémorise le temps pour l'itération suivante

		if gps.has_fix: # Acquisition des satellites réalisée !
		
			# Affiche les informations de la trame : localisation, date, etc.
			print('=' * 40)  # Imprime une ligne de séparation
			
			# Décode et formatte les données d'horodatage (instant du fix)
			print('Horodatage acquisition: {}/{}/{} {:02}:{:02}:{:02}'.format(
				gps.timestamp_utc[1],
				gps.timestamp_utc[2],
				gps.timestamp_utc[0],
				gps.timestamp_utc[3],
				gps.timestamp_utc[4],
				gps.timestamp_utc[5]))
			print('Latitude: {} degrés'.format(gps.latitude)) # Latitude du module
			print('Longitude: {} degrés'.format(gps.longitude)) # Longitude du module
			print('Qualité acquisition: {}'.format(gps.fix_quality)) # Qualité de la localisation fournie

			# Certaines informations au-delà de la latitude, la longitude et l'étiquette d'horodatage sont optionnelles
			# selon la configuration que vous avez appliquée au module.
			if gps.satellites is not None:
				print('# satellites: {}'.format(gps.satellites)) # Nombre de satellites acquis par le module
			if gps.altitude_m is not None:
				print('Altitude: {} mètres'.format(gps.altitude_m)) # Altitude estimée du module au-dessus d'un ellipsoïde théorique "moyen" qui englobe la Terre
			if gps.track_angle_deg is not None:
				print('Vitesse: {} noeuds'.format(gps.speed_knots)) # Vitesse estimée du module en noeuds (1 noeud = 1,852 km/h)
			if gps.track_angle_deg is not None:
				print('Cap: {} degrés'.format(gps.track_angle_deg)) # Angle entre la direction du nord géographique et la direction suivie par le module
			if gps.horizontal_dilution is not None:
				print('Dilution de précision horizontale: {}'.format(gps.horizontal_dilution)) # Qualité de la localisation du module en latitude et longitude
			if gps.height_geoid is not None:
				print('Elévation au-dessus du géoïde: {} mètres'.format(gps.height_geoid)) # Ecart entre l'altitude du géoïde terrestre et celle de l'ellipsoïde moyen (altitude effectivement rapportée) à l'emplacement du module
