from machine import I2C, Pin
# display SSD1306 is connected on I2C1 of arduino connector
import framebuf
import ssd1306

# ----------------------------------------
# screen parameters
SCREEN_WIDTH = 128
SCREEN_HEIGHT = 64

# ----------------------------------------
# READ Picture from file
def load_image(filename):
    with open(filename, 'rb') as f:
        f.readline()
        width, height = [int(v) for v in f.readline().split()]
        data = bytearray(f.read())
    return framebuf.FrameBuffer(data, width, height, framebuf.MONO_HLSB)


# ----------------------------------------
# search if i2c id are present on i2c bus
def isPresentOnI2C(i2c, i2c2_list, id_tofound):
    if i2c2_list is None:
        local_i2clist = self.i2c.scan()
    else:
        local_i2clist = i2c2_list
    for i in local_i2clist:
        if i == id_tofound:
            return 1
    return 0

# -------------------------------------------
# display ST logo
def display_logo(screen):
    if screen is not None:
        screen.fill(0)

        logo_pbm = load_image("logo_st.pbm")
        screen.blit(logo_pbm, 0, 0)

        screen.show()
# -------------------------------------------
# display temperature and humidity
def display_temperature_humidity(screen, temp, hum):
    if screen is not None:
        screen.fill(0)

        temperature_pbm = load_image("climate.pbm")
        screen.blit(temperature_pbm, 0, 16)

        screen.text('{:14s}'.format('Temperature:'), 32, 0)
        screen.text('{:^14s}'.format(str(temp) + 'C'), 16, 16)

        screen.text('{:14s}'.format('Humidity:'), 32, 32)
        screen.text('{:^14s}'.format(str(hum) + '%'), 16, 48)

        screen.show()
# -------------------------------------------
# display pressure and altitude
def display_pressure_altitude(screen, press, alt):
    if screen is not None:
        screen.fill(0)

        pressure_pbm = load_image("pressure.pbm")
        screen.blit(pressure_pbm, 0, 16)

        screen.text('{:18s}'.format('Pressure:'), 36, 0)
        screen.text('{:^14s}'.format('{:.1f}'.format(press) + 'hPa'), 18, 16)

        screen.text('{:18s}'.format('Altitude:'), 36, 32)
        screen.text('{:^14s}'.format('{:.1f}'.format(alt) + 'M'), 18, 48)

        screen.show()

# -------------------------------------------
# display temperature and humidity

# ---------------------------------------------
#                  main
# ---------------------------------------------
i2c1 = I2C(1)
display = None
if __name__ == '__main__':
    # scan i2c bus to see which ip components are present
    print(i2c1.scan())
    # wait to be sure all the component are present
    time.sleep_ms(1000)
    # init display
    if isPresentOnI2C(i2c1, None, 60):
        display = ssd1306.SSD1306_I2C(SCREEN_WIDTH, SCREEN_HEIGHT, i2c1)

    # display log during 5 seconds
    display_logo(display)
    time.sleep_ms(5000)

    # display temperature
    display_temperature_humidity(display, 25.2, 45.6)
    time.sleep_ms(5000)

    # display pressure
    display_pressure_altitude(display, 1024.2, 122.1)
    time.sleep_ms(5000)

