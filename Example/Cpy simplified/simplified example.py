import board
import digitalio
import time
from wiznet_simplify import *

print("Wiznet5k SimpleServer Test (DHCP)")
# init and create a TCP network
TCP_server = network()
# Create a socket for TCP server
TCP_server.connection()

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

while True:
    led.value = not led.value #showing the light is blinking
    time.sleep(0.1) #transmit data speed
    
    # Check TCP mode from the socket and starts the connection
    TCP_server.check_mode()
    # Starts communicate with other device
    received = TCP_server.communication()
    #print (received)

          
