import bluetooth
import random
from ble_advertising import advertising_payload
from struct import pack
from micropython import const
import pyb

_IRQ_CENTRAL_CONNECT                 = const(1 << 0)
_IRQ_CENTRAL_DISCONNECT              = const(1 << 1)
_IRQ_GATTS_WRITE                     = const(3)

_ST_APP_UUID = bluetooth.UUID('00000000-0001-11E1-AC36-0002A5D5C51B')
_ENV_UUID = (bluetooth.UUID('001C0000-0001-11E1-AC36-0002A5D5C51B'), bluetooth.FLAG_NOTIFY) # Humidity + Temperature + Pressure Char
_SWITCH_UUID = (bluetooth.UUID('20000000-0001-11E1-AC36-0002A5D5C51B'), bluetooth.FLAG_NOTIFY|bluetooth.FLAG_WRITE) # Switch Char

_ST_APP_SERVICE = (_ST_APP_UUID, (_ENV_UUID, _SWITCH_UUID ))

_PROTOCOL_VERSION   = const(0x01)
_DEVICE_ID          = const(0x80)                           # Generic Nucleo Board
_FEATURE_MASK       = const(0x201C0000)                     # Switch (2^29), pressure (2^20), humidity (2^19), température (2^18)

# Aparté : calcul des masques
# Caractéristique SWITCH : 2^29 =      100000000000000000000000000000 (en binaire) = 20000000  (en hexadécimal)
# Caractéristique PRESSURE : 2^20 =    000000000100000000000000000000 (en binaire) = 100000    (en hexadécimal)
# Caractéristique HUMIDITY : 2^19 =    000000000010000000000000000000 (en binaire) = 80000     (en hexadécimal)
# Caractéristique TEMPERATURE : 2^18 = 000000000001000000000000000000 (en binaire) = 40000     (en hexadécimal)
# _FEATURE_MASK :                      100000000111000000000000000000 (en binaire) = 201C0000  (en hexadécimal)

_DEVICE_MAC         = [0x12, 0x34, 0x56, 0x78, 0x9A, 0xBC]  # Fake Device MAC
                        
_MANUFACTURER       = pack('>BBI6B', _PROTOCOL_VERSION, _DEVICE_ID, _FEATURE_MASK, *_DEVICE_MAC)

led_bleu = pyb.LED(3)
led_rouge = pyb.LED(1)

class BLESensor:
    def __init__(self, ble, name='WB55-MPY'):
        self._ble = ble
        self._ble.active(True)
        self._ble.irq(self._irq)
        ((self._env_handle,self._switch_handle),) = self._ble.gatts_register_services((_ST_APP_SERVICE, ))
        self._connections = set()
        self._payload = advertising_payload(name=name, manufacturer=_MANUFACTURER)
        self._advertise()
        self._handler = None

    def _irq(self, event, data):
        # Track connections so we can send notifications.
        if event == _IRQ_CENTRAL_CONNECT:
            conn_handle, _, _, = data
            self._connections.add(conn_handle)
            print("Connected")
            led_bleu.on()
            
        elif event == _IRQ_CENTRAL_DISCONNECT:
            conn_handle, _, _, = data
            self._connections.remove(conn_handle)
            # Start advertising again to allow a new connection.
            self._advertise()
            print("Disconnected")
            
        elif event == _IRQ_GATTS_WRITE:
            conn_handle, value_handle, = data
            if conn_handle in self._connections and value_handle == self._switch_handle:
                print("Write")
                data_received = self._ble.gatts_read(self._switch_handle)
                self._ble.gatts_write(self._switch_handle, pack('<HB', 1000, data_received[0]))
                self._ble.gatts_notify(conn_handle, self._switch_handle)
                if data_received[0] == 1:
                    led_rouge.on()
                else:
                    led_rouge.off()

    # Points d'attention :
    # - Les valeurs doivent être transmises dans l'ordre des ID des caractéristiques (pression : 20 eme bit, humidité : 19 eme bit, température 18 eme bit)
    # - Attention à la chaîne de formattage de la fonction Python "pack", égale ici à '<HiHh', voir la documentation de "pack"
    def set_data_env(self, timestamp, pressure, humidity, temperature, notify):
        self._ble.gatts_write(self._env_handle, pack('<HiHh', timestamp, pressure, humidity, temperature))
        if notify:
            for conn_handle in self._connections:
                # Notify connected centrals to issue a read.
                self._ble.gatts_notify(conn_handle, self._env_handle)

    def _advertise(self, interval_us=500000):
        self._ble.gap_advertise(interval_us, adv_data=self._payload)
        led_bleu.off()
