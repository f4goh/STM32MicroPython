# Objet du script : utiliser un capteur d'humidité et de température
# de la famille DHT (DHT11 ou DHT22).

import dht # Pour gérer les DHT11 et DHT22
from time import sleep_ms # Pour temporiser

# Instanciation du DHT22
sensor = dht.DHT22('D2')

# Pour un DHT11, utilisez simplement cette syntaxe :
# sensor = dht.DHT11('D2')

while True:

    # Structure de gestion des exceptions
    try:
        
        # On mesure et on lit les résultats
        sensor.measure()
        temp = sensor.temperature()
        humi = sensor.humidity()
        
        # Si les deux mesures renvoient 0 simultanément
        if humi == 0 and temp == 0:
            raise ValueError("Erreur capteur")

        # Formattage (arrondis) des mesures
        temperature = round(temp,1)
        humidity = int(humi)

        # Affichage des mesures
        print('=' * 40) # Imprime une ligne de séparation
        print("Température : " + str(temperature) + " °C")
        print("Humidité relative : " + str(humidity) + " %")

    # Si une exception est capturée
    except Exception as e:
        print(str(e) + '\n')

    # Temporisation de deux secondes
    sleep_ms(2000)