from pyb import UART # Classe pour gérer l'UART

# Ouverture du LPUART sur les broches D0(RX) D1(TX)
# Attention, le Time-Out doit être plus grand que la fréquence d'interrogation du peripherique
uart = UART(2, 9600, timeout = 5000)
uart.write('hello')
