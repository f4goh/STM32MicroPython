from time import sleep # Pour temporiser
import pyb

# Instanciation de la RTC
rtc = pyb.RTC()

# annee mois jour jour_de_la_semaine heure minute seconde subseconde(compteur interne)
#       year  m  j  wd h  m  s  sub
date = [2021, 1, 1, 5, 0, 0, 0, 0]
#indices : 0 1 2 3 4 5 6 7

# On initialise la date
rtc.datetime(date)

while True :
    # On récupère la date mise à jour
    date = rtc.datetime()
    # Et on l'affiche
    print('{0:02d}'.format(date[4])+'h'+'{0:02d}'.format(date[5])+'min'+'{0:02d}'.format(date[6])+'s')
    # On actualise toute les secondes
    sleep(1)