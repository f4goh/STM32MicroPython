# Objet du script : mise en œuvre d'un clavier matriciel 4x4.
# Matériel requis (en plus de la NUCLEO-WB55) : un clavier matriciel 4x4 et, 
# bien sûr, des câbles pour le connecter à la NUCLEO-WB55...

from keypad import Keypad4x4 # Bibliothèque pour gérer le clavier

keyboard = Keypad4x4() # Instanciation du clavier

while True:
	key = keyboard.read_key() # Lecture de la touche appuyée
	print(key) # Affichage de la touche appuyée
