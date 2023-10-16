# Objet du Script : 
# Réalisation d'un télémètre avec une sortie sonore (type "radar de recul").
# Le buzzer émet des bips de fréquence variable, inversement proportionnelle 
# à la distance mesurée par le VL53L0x (plus la distance est courte, plus les bips 
# sont rapprochés).
# La distance mesurée par le VL53L0x est convertie en valeur de fréquence, 
# qui est ensuite attribuée à l'interruption de dépassement périodique d'un  
# timer, laquelle contrôle le buzzer.
# Matériel (en plus de la carte NUCLEO-WB55) :
# - un Grove Base Shield
# - un module buzzer Grove connecté sur D6 du Grove Base Shield.
# - un capteur Time of Flight Grove connecté sur une prise I2C du Grove Base Shield.
# Source : https://github.com/uceeatz/VL53L0X

from time import sleep_ms # Pour temporiser
import gc # Ramasse miettes, pour éviter de saturer la mémoire
import pyb

# Fréquence du timer, en hertz
MIN_FREQUENCY_HZ = 0.25
MAX_FREQUENCY_HZ = 10.

# Bornage de l'intervalle de mesures du capteur, valeurs en mm
MIN_DIST_MM = const(1)
MAX_DIST_MM = const(1700)

frequency = MIN_FREQUENCY_HZ # Fréquence initiale du timer
distance = MAX_DIST_MM # distance initiale d'un supposé obstacle

# Initialisation de la broche du buzzer
buzzer_pin = pyb.Pin('D6', pyb.Pin.OUT_PP) 

timer_id = 1 # Timer sur D6

# Routine de service de l'interruption (ISR) de dépassement de compteur du timer 1.
# Génère un bip de 5 millisecondes
@micropython.native # Produit un bytecode optimisé pour STM32
def tick(timer):

    global distance
    
    if distance < MAX_DIST_MM:
        buzzer_pin.value(1)
        sleep_ms(55)
        buzzer_pin.value(0)
    else:
        buzzer_pin.value(0)
        
# Démarre le timer 1 à la fréquence de frequency Hz.
# Assigne la fonction "tick" à l'interruption de dépassement de compteur du timer 1.
tim1 = pyb.Timer(timer_id, freq=frequency, callback=tick)

from machine import I2C # Bibliothèque pour le bus I2C
import VL53L0X # Bibliothèque pour le VL53L0X

#Initialisation du bus I2C numéro 1 du STM32WB55 
i2c = I2C(1)

# Pause d'une seconde pour laisser à l'I2C le temps de s'initialiser
sleep_ms(1000)

tof = VL53L0X.VL53L0X(i2c) # Instance du capteur de distance

# Fonction pour remapper un intervalle de valeurs dans un autre
@micropython.native # Produit un bytecode optimisé pour STM32
def map (value, from_min, from_max, to_min, to_max):
    return (value-from_min) * (to_max-to_min) / (from_max-from_min) + to_min

# Fonction principale
@micropython.native  # Produit un bytecode optimisé pour STM32
def main():

    global distance
        
    sleep_ms(500) # Temporisation "de sécurité"
    tof.start() # démarrage du capteur
    tof.read() # Première mesure "à blanc"
    sleep_ms(500) # Temporisation "de sécurité"

    try: # Gestion d'erreurs
        
        while True:

            # Mesure de la distance et correction des valeurs aberrantes
            distance = min(max(tof.read(), MIN_DIST_MM), MAX_DIST_MM)
            
            # Remappe la distance dans l'intervalle de fréquence souhaité
            frequency = map(distance, MIN_DIST_MM, MAX_DIST_MM, MIN_FREQUENCY_HZ, MAX_FREQUENCY_HZ)
            
            # Prend le complément de la fréquence (pour qu'elle augmente lorsqu'on s'approche d'un obstacle).
            frequency = round(max(MAX_FREQUENCY_HZ - frequency, MIN_FREQUENCY_HZ),3)

            # Ajuste la fréquence du timer
            tim1.freq(frequency)
            
            # Appel du ramasse-miettes, indispensable pour que le programme ne se bloque pas
            # très rapidement en fragmentant complètement la RAM.
            gc.collect()
            
            sleep_ms(500) # Temporisation de 50 millisecondes
            print(distance)
    # En cas d'interruption clavier avec CTRL+C
    except KeyboardInterrupt:
        tim1.deinit() # Arrêt du timer
        buzzer_pin.value(0) # Arrêt du buzzer
        tof.stop() # Arrêt du capteur

# Appel de la fonction principale
main()