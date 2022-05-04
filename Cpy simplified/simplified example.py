import board
import digitalio
import time
import gc
from wiznet_simplify import *

print("Wiznet5k SimpleServer Test (DHCP)")
TCP_server = network()
TCP_server.connection()

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

while True:
# Maintain DHCP lease (continue the DHCP setting while TCP is connected)
    #eth.maintain_dhcp_lease()

    led.value = not led.value #showing the light is blinking
    time.sleep(0.1) #transmit data speed
    
    TCP_server.check_mode()
    #TCP_mode.test()
    received = TCP_server.communication()
    #print (received)
    print( gc.mem_free() )
          
