import math
import time
import ws2812bstm32

# --------------------------------
french_flag = [
    (0,0,250), (0,0,250), (0,0,250),
    (250,250,250), (250,250,250), (250,250,250),
    (250,0,0), (250,0,0), (250,0,0)]
italien_flag = [
    (0,250,0), (0,250,0), (0,250,0),
    (250,250,250), (250,250,250), (250,250,250),
    (250,0,0), (250,0,0), (250,0,0)]

# --------------------------------
def test_led(leds, led_count, color):
    for i in range(0, led_count):
        if i != 0:
            leds.clean(i-1)
        leds.put_pixel(i, color[0], color[1], color[2])
        leds.send_buf()
        time.sleep_ms(500)
    leds.clean(i)
    leds.send_buf()
    time.sleep_ms(500)
# --------------------------------
def flag(leds, data,display=True):
    i = 0
    for d in data:
        leds.put_pixel(i, d[0], d[1], d[2])
        if display:
            leds.send_buf()
            time.sleep_ms(1000)
        i+=1
def invflag(leds, data, display):
    i = len(data) - 1
    while i >= 0:
        d = data[i]
        leds.put_pixel(i, d[0], d[1], d[2])
        if display:
            leds.send_buf()
            time.sleep_ms(1000)
        i-=1
# --------------------------------
def dual_flag(leds, data0, data1, num_led, t, display):
    i = 0
    while i < num_led:
        if (i + len(data0)) < num_led:
            for d in data0:
                leds.put_pixel(i, d[0], d[1], d[2])
                if display:
                    leds.send_buf()
                    time.sleep_ms(t)
                i+=1
            if not display:
                leds.send_buf()
            i+=1
        else:
            break
        if (i + len(data1)) < num_led:
            for d in data1:
                leds.put_pixel(i, d[0], d[1], d[2])
                if display:
                    leds.send_buf()
                    time.sleep_ms(t)
                i+=1
            if not display:
                leds.send_buf()
            i+=1
        else:
            break
# --------------------------------
def flag_move(leds, data, num_led, t):
    i = 0
    while i < num_led:
        if (i + len(data)) < num_led:
            if i != 0:
                leds.clean(i-1)
            j = i
            for d in data:
                leds.put_pixel(j, d[0], d[1], d[2])
                j+=1
            leds.send_buf()
            time.sleep_ms(t)
            i+=1
        else:
            break

# init led strip
strip = ws2812bstm32.WS2812(spi_bus=1, ledNumber=30, intensity=0.5)

#test_led(30, [0,0,250])
#test_led(60, [250,250,0])

#clear strip
strip.clear()
strip.send_buf()

# display two flag
dual_flag(strip, french_flag, italien_flag, 30, 500, True)

while 1:
    #clear strip
    strip.clear()
    strip.send_buf()

    # flag move
    flag_move(strip, french_flag, 30, 500)

    #clear strip
    strip.clear()
    strip.send_buf()

    # flag move
    flag_move(strip, italien_flag, 30, 500)


