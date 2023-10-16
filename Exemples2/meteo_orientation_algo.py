from machine import I2C
import LSM6DSO
import math
import time

i2c = I2C(1)
time.sleep_ms(1000) # wait sensor available on bus
inertial_sensor = LSM6DSO.LSM6DSO(i2c)

while 1:
    accel = inertial_sensor.get_a_raw()
    x = accel[0]
    y = accel[1]
    z = accel[2]

    if x == 0 and y == 0 and z == 0:
        pitch = 0
        roll = 0
        yaw = 0
    else:
        # Calcul IMU
        pitch = round(math.atan(x / math.sqrt(y * y + z * z)) * 180.0 * math.pi)
        roll  = round(math.atan(y / math.sqrt(x * x + z * z)) * 180.0 * math.pi)
        yaw   = round(math.atan(z / math.sqrt(x * x + z * z)) * 180.0 * math.pi)
        #print("[DEBUG]: Pitch: ", pitch)
        #print("[DEBUG]: Roll: ", roll)
        #print("[debug]: yaw: ", yaw)

        # display orientation
        if abs(pitch) > 200:
            ''' (pitch > 0) ? ORIENTATION_LEFT_UP : ORIENTATION_RIGHT_UP;'''
            if pitch > 0:
                print("Left")
            else:
                print("Right")
        elif abs(roll) > 200:
            '''ret = (roll < 0) ? ORIENTATION_VERTICAL_DOWN : ORIENTATION_VERTICAL_UP;'''
            if roll < 0:
                print("Bottom")
            else:
                print("UP")
        else:
            print("Not moving")
        time.sleep_ms(500)
