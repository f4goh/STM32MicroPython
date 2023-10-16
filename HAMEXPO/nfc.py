import NFC_PN532 as nfc
from machine import Pin, SPI

# SPI
spi_dev = SPI(1, baudrate=1000000)
cs = Pin('D10',Pin.OUT)
cs.on()


# SENSOR INIT
pn532 = nfc.PN532(spi_dev,cs)
ic, ver, rev, support = pn532.get_firmware_version()
print('Found PN532 with firmware version: {0}.{1}'.format(ver, rev))

# Configure PN532 to communicate with MiFare cards
pn532.SAM_configuration()

# FUNCTION TO READ 
def read_nfc(dev, tmot):
    """Accepts a device and a timeout in millisecs """
    print('Reading...')
    uid = dev.read_passive_target(timeout=tmot)
    if uid is None:
        print('CARD NOT FOUND')
    else:
        numbers = [i for i in uid]
        string_ID = '{}-{}-{}-{}'.format(*numbers)
        print('Found card with UID:', [hex(i) for i in uid])
        print('Number_id: {}'.format(string_ID))


read_nfc(pn532, 500)
