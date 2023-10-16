from micropython import const
import struct
from struct import *
import bluetooth
import time
import random


from machine import Pin, SPI
import max7219

spi = None
display = None
# ---------------------------------------------
#                  advertising
# ---------------------------------------------
# Advertising payloads are repeated packets of the following form:
#   1 byte data length (N + 1)
#   1 byte type (see constants below)
#   N bytes type-specific data

_ADV_TYPE_FLAGS = const(0x01)
_ADV_TYPE_NAME = const(0x09)
_ADV_TYPE_UUID16_COMPLETE = const(0x3)
_ADV_TYPE_UUID32_COMPLETE = const(0x5)
_ADV_TYPE_UUID128_COMPLETE = const(0x7)
_ADV_TYPE_UUID16_MORE = const(0x2)
_ADV_TYPE_UUID32_MORE = const(0x4)
_ADV_TYPE_UUID128_MORE = const(0x6)
_ADV_TYPE_APPEARANCE = const(0x19)
_ADV_TYPE_MANUFACTURER = const(0xFF)

# Generate a payload to be passed to gap_advertise(adv_data=...).
def advertising_payload(limited_disc=False, br_edr=False, name=None, services=None, appearance=0, manufacturer=0):
    payload = bytearray()

    def _append(adv_type, value):
        nonlocal payload
        payload += struct.pack('BB', len(value) + 1, adv_type) + value

    _append(_ADV_TYPE_FLAGS, struct.pack('B', (0x01 if limited_disc else 0x02) + (0x00 if br_edr else 0x04)))

    if name:
        _append(_ADV_TYPE_NAME, name)

    if services:
        for uuid in services:
            b = bytes(uuid)
            if len(b) == 2:
                _append(_ADV_TYPE_UUID16_COMPLETE, b)
            elif len(b) == 4:
                _append(_ADV_TYPE_UUID32_COMPLETE, b)
            elif len(b) == 16:
                _append(_ADV_TYPE_UUID128_COMPLETE, b)

    if appearance:
        # See org.bluetooth.characteristic.gap.appearance.xml
        _append(_ADV_TYPE_APPEARANCE, struct.pack('<h', appearance))

    if manufacturer:
        _append(_ADV_TYPE_MANUFACTURER, manufacturer)

    return payload

# ---------------------------------------------
#            BLE sensor service
# ---------------------------------------------
_IRQ_CENTRAL_CONNECT        = const(1)
_IRQ_CENTRAL_DISCONNECT     = const(2)
_IRQ_GATTS_WRITE            = const(3)
_IRQ_GATTS_READ             = const(4)

_ST_APP_UUID = bluetooth.UUID('00000000-0001-11E1-AC36-0002A5D5C51B')
# Temperature char: 0x04 (TEMPERATURE) 00XX0000-0001-11E1-AC36-0002A5D5C51B)
_TEMPERATURE_UUID = (bluetooth.UUID('00040000-0001-11E1-AC36-0002A5D5C51B'), bluetooth.FLAG_READ|bluetooth.FLAG_NOTIFY) #Temperature Char
# LED char: 0x20 (LED) XX000000-0001-11E1-AC36-0002A5D5C51B
_LED_UUID = (bluetooth.UUID('20000000-0001-11E1-AC36-0002A5D5C51B'), bluetooth.FLAG_WRITE|bluetooth.FLAG_NOTIFY) # LED Char

_DISPLAY_UUID = (bluetooth.UUID('5930b535-bc2a-4436-a9c1-d98dcbb2bb23'), bluetooth.FLAG_WRITE|bluetooth.FLAG_NOTIFY)

_ST_APP_SERVICE = (_ST_APP_UUID, (_TEMPERATURE_UUID, _LED_UUID, _DISPLAY_UUID))

_PROTOCOL_VERSION   = const(0x01)
_DEVICE_ID          = const(0x80)	 # Generic Nucleo Board
_FEATURE_MASK       = const(0x20040000)   # Temperature (2^18) and LED (2^29)
_DEVICE_MAC         = [0x10, 0xE7, 0x7A, 0x78, 0x9A, 0xBC]
_MANUFACTURER       = pack('>BBI6B', _PROTOCOL_VERSION, _DEVICE_ID, _FEATURE_MASK, *_DEVICE_MAC)

led_bleu = pyb.LED(1)
led_rouge = pyb.LED(3)

class BLESensor:
    # NOTE: The name could be changed to be more easily recognize
    def __init__(self, ble, name='WB55-MPY-XXX'):
        self._ble = ble
        self._ble.active(True)
        self._ble.irq(self._irq)
        ((self._temperature_handle,self._led_handle,self._display_handle),) = self._ble.gatts_register_services((_ST_APP_SERVICE, ))

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
            self._advertise(
            print("Disconnected")
        elif event == _IRQ_GATTS_WRITE:
            conn_handle, value_handle, = data
            print("READ request")
            if conn_handle in self._connections and value_handle == self._led_handle:
                data_received = self._ble.gatts_read(self._led_handle)
                print("LED receive: ", data_received[0])
                print(data_received)
                self._ble.gatts_write(self._led_handle, struct.pack('<HB', 1000, data_received[0]))
                self._ble.gatts_notify(conn_handle, self._led_handle)
                if data_received[0] == 1:
                    led_rouge.on()
                else:
                    led_rouge.off()
            if conn_handle in self._connections and value_handle == self._display_handle:
                data_received = self._ble.gatts_read(self._display_handle)
                print("DISPLAY receive: ", data_received)
                self._ble.gatts_write(self._display_handle, struct.pack('<HB', 1000, 1))
                self._ble.gatts_notify(conn_handle, self._display_handle)
                display_text_scroll(data_received)

        elif event == _IRQ_GATTS_READ:
            conn_handle, value_handle, = data
            if conn_handle in self._connections and value_handle == self._temperature_handle:
                print("temperature: ", struct.pack('<hh', 0,990))
                self.set_data_temperature(0, 99, notify=1)

    def set_data_temperature(self, timestamp, temperature, notify=False):
        self._ble.gatts_write(self._temperature_handle, struct.pack('<hh', timestamp, temperature))
        if notify:
            for conn_handle in self._connections:
                # Notify connected centrals to issue a read.
                self._ble.gatts_notify(conn_handle, self._temperature_handle)

    def _advertise(self, interval_us=500000):
        self._ble.gap_advertise(interval_us, adv_data=self._payload)
        led_bleu.off()


# ---------------------------------------------
#                  screen max7219
# ---------------------------------------------
def display_text_scroll(text):
    # for 4 led blocks
    for p in range(4 * 8, len(text) * -8 - 1, -1):
        display.fill(False)
        display.text(text, p, 0, not False)
        display.show()
        time.sleep_ms(50)

# ---------------------------------------------
#                  main
# ---------------------------------------------
if __name__ == '__main__':
    spi = SPI(1, baudrate=10000000)
    display = max7219.Max7219(32, 8, spi, Pin('B2'))

    display_text_scroll("STMicroelectronics")

    ble = bluetooth.BLE()
    ble_device = BLESensor(ble, name='WB55-MPY-001')

    display_text_scroll("BLE ready")

    while True:
        timestamp = time.time()
        temperature = (random.randint(0, 1000)) # random value between 0 and 100,0 °C
        # via BLE: send timestamp and temperature with notification
        ble_device.set_data_temperature(timestamp, temperature, notify=1)
#        ble_device.set_data_temperature(0, 550, notify=1)
        # wait 1 seconds before next loop
        time.sleep_ms(5000)
