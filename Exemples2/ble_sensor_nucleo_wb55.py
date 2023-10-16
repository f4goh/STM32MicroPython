from micropython import const
import struct
from struct import *
import bluetooth
import pyb

# I2C and SPI screen
from machine import I2C, SPI, Pin

# IKS01a3
# HTS221: Temperature / Humidity sensor
import hts221
# LPS22 sensor is connected on I2C1 of arduino connector
import LPS22
# LSM6DSO: Accelerometer / Gyroscope sensor
import LSM6DSO

# display SSD1306 is connected on I2C1 of arduino connector
import framebuf
import ssd1306
# display mx7219 is connected on SPI1 of arduino connector

import max7219

import math
import time
import random


spi = None
display_oled = None
display_led = None

max7219_present = 0 # to change if it's present on bus

# ----------------------------------------
# Screen & READ Picture
SCREEN_WIDTH = 128
SCREEN_HEIGHT = 64
def load_image(filename):
    with open(filename, 'rb') as f:
        f.readline()
        width, height = [int(v) for v in f.readline().split()]
        data = bytearray(f.read())
    return framebuf.FrameBuffer(data, width, height, framebuf.MONO_HLSB)

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
# Environment char: 1C = 0x04 (TEMPERATURE) | 0x08 (Humidity) | 0x10 (Pressure)

# Temperature char: 0x04 (TEMPERATURE) 00XX0000-0001-11E1-AC36-0002A5D5C51B)
_TEMPERATURE_UUID = (bluetooth.UUID('00040000-0001-11E1-AC36-0002A5D5C51B'), bluetooth.FLAG_NOTIFY) #Temperature Char
# Humidity char: 0x08 (HUMIDITY) 00XX0000-0001-11E1-AC36-0002A5D5C51B)
_HUMIDITY_UUID = (bluetooth.UUID('00080000-0001-11E1-AC36-0002A5D5C51B'), bluetooth.FLAG_NOTIFY) #humidity Char
# Pressure char: 0x10 (Pressure) 00XX0000-0001-11E1-AC36-0002A5D5C51B)
_PRESSURE_UUID = (bluetooth.UUID('00100000-0001-11E1-AC36-0002A5D5C51B'), bluetooth.FLAG_NOTIFY) #pressure Char

# 00XX0000-0001-11E1-AC36-0002A5D5C51B
_ENVIRONMENTAL_UUID = (bluetooth.UUID('001C0000-0001-11E1-AC36-0002A5D5C51B'), bluetooth.FLAG_NOTIFY)
# LED char: 0x20 (LED) XX000000-0001-11E1-AC36-0002A5D5C51B
_LED_UUID = (bluetooth.UUID('20000000-0001-11E1-AC36-0002A5D5C51B'), bluetooth.FLAG_WRITE|bluetooth.FLAG_NOTIFY) # LED Char

_DISPLAY_UUID = (bluetooth.UUID('5930b535-bc2a-4436-a9c1-d98dcbb2bb23'), bluetooth.FLAG_WRITE|bluetooth.FLAG_NOTIFY)

_ST_APP_SERVICE = (_ST_APP_UUID, ( _TEMPERATURE_UUID, _HUMIDITY_UUID, _PRESSURE_UUID,_LED_UUID, _DISPLAY_UUID))

_PROTOCOL_VERSION   = const(0x01)
_DEVICE_ID          = const(0x80)	 # Generic Nucleo Board
_FEATURE_MASK       = const(0x201C0000)   # Temperature (2^18) and Humidity(2^19) and Pressure (2^20) and LED (2^29)
_DEVICE_MAC         = [0x10, 0xE7, 0x7A, 0x78, 0x9A, 0xBC]
_MANUFACTURER       = pack('>BBI6B', _PROTOCOL_VERSION, _DEVICE_ID, _FEATURE_MASK, *_DEVICE_MAC)

led_blue = pyb.LED(1)
led_red = pyb.LED(3)

class BLESensor:
    # NOTE: The name could be changed to be more easily recognize
    def __init__(self, ble, screen_oled, screen_matrice, sensors, name='WB55-MPY-XXX'):
        self._ble = ble
        self._ble.active(True)
        self._ble.irq(self._irq)
        self.screen_oled = screen_oled
        self.screen_matrice = screen_matrice
        self.sensors = sensors
        ((self._temp_handle,self._humidity_handle,self._pressure_handle,self._led_handle,self._display_handle),) = self._ble.gatts_register_services((_ST_APP_SERVICE, ))

        self._connections = set()
        self._payload = advertising_payload(name=name, manufacturer=_MANUFACTURER)
        self._advertise()
        self._handler = None

        self.state_disconnected = 0
        self.state_connected = 1
        self.switch_connected = 1
        self.switch_disconnected = 0
        self.state = self.state_disconnected
        self.switch = self.switch_disconnected

    def get_state(self):
        return self.state
    def get_switch(self):
        return self.switch

    def _irq(self, event, data):
        # Track connections so we can send notifications.
        if event == _IRQ_CENTRAL_CONNECT:
            conn_handle, _, _, = data
            self._connections.add(conn_handle)
            self.state = self.state_connected
            print("Connected added: ", conn_handle)
            led_blue.on()
        elif event == _IRQ_CENTRAL_DISCONNECT:
            conn_handle, _, _, = data
            self._connections.remove(conn_handle)
            # Start advertising again to allow a new connection.
            self._advertise()
            self.state = self.state_disconnected
            print("Disconnected")
        elif event == _IRQ_GATTS_WRITE:
            conn_handle, value_handle, = data
            # -----------------------------------------------
            # Write Section
            # LED switch
            if conn_handle in self._connections and value_handle == self._led_handle:
                data_received = self._ble.gatts_read(self._led_handle)
                print("LED receive: ", data_received)
                self._ble.gatts_write(self._led_handle, struct.pack('<HB', 1000, data_received[0]))
                self._ble.gatts_notify(conn_handle, self._led_handle)
                if data_received[0] == 1:
                    led_red.on()
                    self.switch_logo(fill=1)
                    self.switch = self.switch_connected
                else:
                    led_red.off()
                    self.switch_logo()
                    self.switch = self.switch_disconnected
            # Display
            if conn_handle in self._connections and value_handle == self._display_handle:
                data_received = self._ble.gatts_read(self._display_handle)
                print("DISPLAY receive: ", data_received)
                self._ble.gatts_write(self._display_handle, struct.pack('<HB', 1000, 1))
                self._ble.gatts_notify(conn_handle, self._display_handle)
                if max7219_present:
                    display_text_scroll(data_received)
            # -----------------------------------------------

    def set_data_environment(self, timestamp, temperature, pressure, humidity, notify=False):
        self._ble.gatts_write(self._environment_handle,
                              struct.pack('<hihh', timestamp, pressure * 100, humidity*10, temperature * 10))
        if notify:
            for conn in self._connections:
                self._ble.gatts_notify(conn, self._environment_handle)

    def set_data_temperature(self, timestamp, temperature, notify=False):
        self._ble.gatts_write(self._temp_handle, struct.pack('<hh', timestamp, temperature * 10))
        if notify:
            for conn in self._connections:
                self._ble.gatts_notify(conn, self._temp_handle)
    def set_data_humidity(self, timestamp, humidity, notify=False):
        self._ble.gatts_write(self._humidity_handle, struct.pack('<hh', timestamp, humidity * 10))
        if notify:
            for conn in self._connections:
                self._ble.gatts_notify(conn, self._humidity_handle)
    def set_data_pressure(self, timestamp, pressure, notify=False):
        self._ble.gatts_write(self._pressure_handle, struct.pack('<hi', timestamp, pressure *100))
        if notify:
            for conn in self._connections:
                self._ble.gatts_notify(conn, self._pressure_handle)

    def _advertise(self, interval_us=500000):
        self._ble.gap_advertise(interval_us, adv_data=self._payload)
        led_blue.off()

    def switch_logo(self, fill=None):
        if self.screen_oled is not None:
            self.screen_oled.fill(0)
            if fill is not None:
                logo_pbm = load_image("logo_st.pbm")
                self.screen_oled.blit(logo_pbm, 0, 0)
            self.screen_oled.show()

# ---------------------------------------------
#                  Sensor management
# ---------------------------------------------
class Sensors:
    def __init__(self, i2c):
        self.i2c = i2c
        self.temperature_humidity = None
        self.pressure             = None
        self.accelerometer_sensor = None
        if self.isPresentOnI2C(None, 95):
            self.temperature_humidity = hts221.HTS221(i2c)
        if self.isPresentOnI2C(None, 93):
            self.pressure      = LPS22.LPS22(i2c)
        if self.isPresentOnI2C(None, 107):
            self.accelerometer_sensor = LSM6DSO.LSM6DSO(i2c)

        self.ORIENTATION_LEFT_UP        = 0
        self.ORIENTATION_RIGHT_UP       = 1
        self.ORIENTATION_VERTICAL_DOWN  = 2
        self.ORIENTATION_VERTICAL_UP    = 3
        self.ORIENTATION_NORMAL         = 4


    def get_temperature(self):
        if self.temperature_humidity is not None:
            return int(self.temperature_humidity.get()[0])
        else:
            return (random.randint(0, 1000)) # random value between 0 and 100,0 °C
    def get_humidity(self):
        if self.temperature_humidity is not None:
            return int(self.temperature_humidity.get()[1])
        else:
            return (random.randint(0, 1000)) # random value between 0 and 100,0 %
    def get_pressure(self):
        if self.pressure is not None:
            return int(self.pressure.pressure())
        else:
            return (random.randint(8000, 12000)) # random value between 800 and 1200,0 hPa
    def get_altitude(self):
        if self.pressure is not None:
            return int(self.pressure.altitude())
        else:
            return (random.randint(0, 5000)) # random value between 0 and 500,0 m
    def get_accel_raw(self):
        if self.accelerometer_sensor is not None:
            return self.accelerometer_sensor.get_a_raw()
        else:
            return [(random.randint(-1000, 1000)), (random.randint(-1000, 1000)), (random.randint(-1000, 1000))]

    def isPresentOnI2C(self, i2c2_list, id_tofound):
        result = 0
        if i2c2_list is None:
            local_i2clist = self.i2c.scan()
        else:
            local_i2clist = i2c2_list
        for i in local_i2clist:
            if i == id_tofound:
                return 1

    # Acceleromter
    def calculate_imu(self, accel):
        local_accel = accel
        if accel is None:
            local_accel = self.get_accel_raw()
        x = local_accel[0]
        y = local_accel[1]
        z = local_accel[2]
        if x == 0 and y == 0 and z == 0:
            return [0, 0, 0]
        pitch = round(math.atan(x / math.sqrt(y * y + z * z)) * 180.0 * math.pi)
        roll  = round(math.atan(y / math.sqrt(x * x + z * z)) * 180.0 * math.pi)
        yaw   = round(math.atan(z / math.sqrt(x * x + z * z)) * 180.0 * math.pi)
        return [pitch, roll, yaw]


    def get_imu_orientation(self, accel):
        ''' return value array:
            [ enum, string ]
        '''
        pitch, roll, yaw = self.calculate_imu(accel)
        if abs(pitch) > 200:
            ''' (pitch > 0) ? ORIENTATION_LEFT_UP : ORIENTATION_RIGHT_UP;'''
            if pitch > 0:
                return [self.ORIENTATION_LEFT_UP, pitch, roll, "left-up"]
            else:
                return [self.ORIENTATION_RIGHT_UP, pitch, roll, "right-up"]
        elif abs(roll) > 200:
            '''
                ret = (roll < 0) ? ORIENTATION_VERTICAL_DOWN :
                    ORIENTATION_VERTICAL_UP;'''
            if roll < 0:
                return [self.ORIENTATION_VERTICAL_DOWN, pitch, roll, "bottom-down"]
            else:
                return [self.ORIENTATION_VERTICAL_UP, pitch, roll, "top-up"]
        else:
            return [self.ORIENTATION_NORMAL, pitch, roll, "normal"]

# ---------------------------------------------
#                  Oled display
# ---------------------------------------------
class DisplayOnScreen:
    def __init__(self, display):
        self.display = display
        self.remaing_scren_display = 0
        self.DISPLAYED_TIME = 2000

    def dec(self):
        #print("[DEBUG]: request to dec remaining = %d" % self.remaing_scren_display)
        if self.remaing_scren_display < 0:
            self.remaing_scren_display = 0
        elif self.remaing_scren_display == 0:
            self.remaing_scren_display = 0
        else:
            self.remaing_scren_display -= 500
    def inc(self, t):
        self.remaing_scren_display += t

    def reset_remaining(self):
        self.remaing_scren_display = 0

    def display_logo(self, ble_force_display=False):
        if ble_force_display:
            return
        if self.remaing_scren_display > 0:
            return
        self.inc(self.DISPLAYED_TIME)
        if self.display is not None:
            self.display.fill(0)

            logo_pbm = load_image("logo_st.pbm")
            self.display.blit(logo_pbm, 0, 0)

            self.display.show()

    def display_clear(self):
        #print("[DEBUG]: remaining = %d" % self.remaing_scren_display)
        self.dec()
        if self.remaing_scren_display > 0:
            return
        if self.display is not None:
            self.display.fill(0)
            self.display.show()


    def display_temperature_humidity(self, temp, hum, ble_force_display):
        if ble_force_display:
            return
        #print("[DEBUG]: remaining = %d" % self.remaing_scren_display)
        if self.remaing_scren_display > 0:
            return
        self.inc(self.DISPLAYED_TIME)
        if self.display is not None:
            self.display.fill(0)

            temperature_pbm = load_image("climate.pbm")
            self.display.blit(temperature_pbm, 0, 16)

            self.display.text('{:14s}'.format('Temperature:'), 32, 0)
            self.display.text('{:^14s}'.format(str(temp) + 'C'), 16, 16)

            self.display.text('{:14s}'.format('Humidity:'), 32, 32)
            self.display.text('{:^14s}'.format(str(hum) + '%'), 16, 48)

            self.display.show()

    def display_temperature(self, temp, ble_force_display):
        #print("[DEBUG]: remaining = %d" % self.remaing_scren_display, " Force BLE:",  ble_force_display)
        if ble_force_display:
            return
        #print("[DEBUG]: remaining = %d" % self.remaing_scren_display)
        if self.remaing_scren_display > 0:
            return
        self.inc(self.DISPLAYED_TIME)
        if self.display is not None:
            self.display.fill(0)

            temperature_pbm = load_image("climate.pbm")
            self.display.blit(temperature_pbm, 0, 16)

            self.display.text('{:14s}'.format('Temperature:'), 32, 0)
            self.display.text('{:^14s}'.format(str(temp) + 'C'), 16, 16)

            self.display.show()

    def display_humidity(self, hum, ble_force_display):
        #print("[DEBUG]: remaining = %d" % self.remaing_scren_display, " Force BLE:",  ble_force_display)
        if ble_force_display:
            return
        if self.remaing_scren_display > 0:
            return
        self.inc(self.DISPLAYED_TIME)
        if self.display is not None:
            self.display.fill(0)

            temperature_pbm = load_image("climate.pbm")
            self.display.blit(temperature_pbm, 0, 16)

            self.display.text('{:14s}'.format('Humidity:'), 32, 0)
            self.display.text('{:^14s}'.format(str(hum) + '%'), 16, 16)

            self.display.show()

    def display_pressure_altitude(self, press, alt, ble_force_display):
        if ble_force_display:
            return
        if self.remaing_scren_display > 0:
            return
        self.inc(self.DISPLAYED_TIME)
        if self.display is not None:
            self.display.fill(0)

            pressure_pbm = load_image("pressure.pbm")
            self.display.blit(pressure_pbm, 0, 16)

            self.display.text('{:18s}'.format('Pressure:'), 36, 0)
            self.display.text('{:^14s}'.format('{:.1f}'.format(press) + 'hPa'), 18, 16)

            self.display.text('{:18s}'.format('Altitude:'), 36, 32)
            self.display.text('{:^14s}'.format('{:.1f}'.format(alt) + 'M'), 18, 48)

            self.display.show()

    def display_pressure(self, press, ble_force_display):
        if ble_force_display:
            return
        if self.remaing_scren_display > 0:
            return
        self.inc(self.DISPLAYED_TIME)
        if self.display is not None:
            self.display.fill(0)

            pressure_pbm = load_image("pressure.pbm")
            self.display.blit(pressure_pbm, 0, 16)

            self.display.text('{:18s}'.format('Pressure:'), 36, 0)
            self.display.text('{:^14s}'.format('{:.1f}'.format(press) + 'hPa'), 18, 16)

            self.display.show()

    def display_altitude(self, alt, ble_force_display):
        if ble_force_display:
            return
        if self.remaing_scren_display > 0:
            return
        self.inc(self.DISPLAYED_TIME)
        if self.display is not None:
            self.display.fill(0)

            pressure_pbm = load_image("pressure.pbm")
            self.display.blit(pressure_pbm, 0, 16)

            self.display.text('{:18s}'.format('Altitude:'), 36, 0)
            self.display.text('{:^14s}'.format('{:.1f}'.format(alt) + 'M'), 18, 16)

            self.display.show()
# ---------------------------------------------
#                  screen max7219
# ---------------------------------------------
def display_text_scroll(text):
    if max7219_present:
        if display_led is not None:
            # for 4 led blocks
            for p in range(4 * 8, len(text) * -8 - 1, -1):
                display_led.fill(False)
                display_led.text(text, p, 0, not False)
                display_led.show()
                time.sleep_ms(50)

# ---------------------------------------------
#                  main
# ---------------------------------------------
i2c1 = I2C(1)
i2c1_list = []
spi = SPI(1, baudrate=10000000)
sensors = None

if __name__ == '__main__':
   # scan i2c bus to see which ip components are present
    i2c1_list = i2c1.scan()
    print(i2c1_list)

    # wait to be sure all the component are present
    time.sleep_ms(1000)
    # init sensor
    sensors = Sensors(i2c1)

    # init display
    display_led = None
    if max7219_present:
        display_led = max7219.Max7219(32, 8, spi, Pin('B2'))
    display_oled = None
    if sensors.isPresentOnI2C(i2c1_list, 60):
        display_oled = ssd1306.SSD1306_I2C(SCREEN_WIDTH, SCREEN_HEIGHT, i2c1)

    display_text_scroll("STMicroelectronics")

    # init bluetooth
    ble = bluetooth.BLE()
    ble_device = BLESensor(ble, display_oled, display_led, sensors, name='WB55-GADGET')

    display_text_scroll("BLE ready")
    print("BLESensor initialized: ", ble.config("mac"))

    screen_displayed = DisplayOnScreen(display_oled)
    screen_displayed.display_logo()

    while True:
        timestamp = time.time()
        humidity = sensors.get_humidity()
        temperature = sensors.get_temperature()
        pressure = sensors.get_pressure()
        altitude = sensors.get_altitude()

        # BLUETOOTH management
        if ble_device.get_state() == ble_device.state_connected:
            # via BLE: send timestamp and environment with notification
            print("send BLE environment")
            ble_device.set_data_temperature(timestamp, temperature, notify=1)
            ble_device.set_data_humidity(timestamp, humidity, notify=1)
            ble_device.set_data_pressure(timestamp, pressure, notify=1)


        ble_force_display = False
        if ble_device.get_switch() == ble_device.switch_connected:
            ble_force_display = True
        imu = sensors.get_imu_orientation(None)
        if imu[0] == sensors.ORIENTATION_LEFT_UP:
            # display humidity
            print("Humidite: %s %s" % (str(humidity), "%") )
            screen_displayed.display_humidity(humidity, ble_force_display)
            time.sleep_ms(1000)
        elif imu[0] == sensors.ORIENTATION_RIGHT_UP:
            # display temperature
            print("Temperature: %s C" % str(temperature) )
            screen_displayed.display_temperature(temperature, ble_force_display)
            time.sleep_ms(1000)
        elif imu[0] == sensors.ORIENTATION_VERTICAL_DOWN:
            # display altitude
            print("Altitude: %s M" % str(altitude) )
            screen_displayed.display_altitude(altitude, ble_force_display)
            time.sleep_ms(1000)
        elif imu[0] == sensors.ORIENTATION_VERTICAL_UP:
            # display pressure
            print("Pressure: %s hPa" % str(pressure) )
            screen_displayed.display_pressure(pressure, ble_force_display)
            time.sleep_ms(1000)
        if ble_device.get_state() == ble_device.state_connected:
            if ble_device.get_switch() == ble_device.switch_connected:
                screen_displayed.reset_remaining()
            else:
                screen_displayed.display_clear()
        else:
            screen_displayed.display_clear()

        time.sleep_ms(1000)
