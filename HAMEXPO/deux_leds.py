import pyb
import uasyncio as asyncio

led1 = pyb.LED(1)
led2 = pyb.LED(2)


async def blink(led, delay):  # coroutine
    while True:
        print(led, "on")
        led.on()
        await asyncio.sleep_ms(delay)
        print(led, "off")
        led.off()
        await asyncio.sleep_ms(delay)


# boucle d’événements
loop = asyncio.get_event_loop()
loop.create_task(blink(led1, 500))  # Schedule ASAP
loop.create_task(blink(led2, 1000))  # Schedule ASAP
loop.run_forever()
