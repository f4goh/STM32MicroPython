import pyb
import time

print("GPIO with MicroPython it's easy")

# Init entries Pin(SW1, SW2, SW3)
sw1 = pyb.Pin('SW1', pyb.Pin.IN)
sw1.init(pyb.Pin.IN, pyb.Pin.PULL_UP, af=-1)

sw2 = pyb.Pin('SW2', pyb.Pin.IN)
sw2.init(pyb.Pin.IN, pyb.Pin.PULL_UP, af=-1)

sw3 = pyb.Pin('SW3', pyb.Pin.IN)
sw3.init(pyb.Pin.IN, pyb.Pin.PULL_UP, af=-1)

# Init variables
old_state_sw1 = 0
old_state_sw2 = 0
old_state_sw3 = 0

while 1:
    # System sleep during 300ms
    time.sleep_ms(300)

    # get state of button
    state_sw1 = sw1.value()
    state_sw2 = sw2.value()
    state_sw3 = sw3.value()

    #print("DEBUG STATE: ", [state_sw1, state_sw2, state_sw3])

    if state_sw1 != old_state_sw1:
        if state_sw1 == 0:
            print("Buton 1 (SW1) is pressed")
        else:
            print("Buton 1 (SW1) is released")
        old_state_sw1 = state_sw1
    if state_sw2 != old_state_sw2:
        if state_sw2 == 0:
            print("Buton 2 (SW2) is pressed")
        else:
            print("Buton 2 (SW2) is released")
        old_state_sw2 = state_sw2
    if state_sw3 != old_state_sw3:
        if state_sw3 == 0:
            print("Buton 3 (SW3) is pressed")
        else:
            print("Buton 3 (SW3) is released")
        old_state_sw3 = state_sw3

