import board
import digitalio
import time
import busio

import adafruit_requests as requests
from adafruit_wiznet5k.adafruit_wiznet5k import * #active WIZnet chip library
import adafruit_wiznet5k.adafruit_wiznet5k_socket as socket #open socket from WIZnet library

# Activate GPIO pins for SPI communication
SPI0_SCK = board.GP18
SPI0_TX = board.GP19
SPI0_RX = board.GP16
SPI0_CSn = board.GP17

# Activate Reset pin for communication with W5500 chip
W5x00_RSTn = board.GP20

print("Wiznet5k SimpleServer Test (DHCP)")

# Setup your network configuration below
# random MAC, later should change this value on your vendor ID
MY_MAC = (0x00, 0x01, 0x02, 0x03, 0x04, 0x05)
IP_ADDRESS = (192, 168, 0, 111)
SUBNET_MASK = (255, 255, 0, 0)
GATEWAY_ADDRESS = (192, 168, 0, 1)
DNS_SERVER = (8, 8, 8, 8)

# Set LED for checking the network system  working
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

# Set reset function
ethernetRst = digitalio.DigitalInOut(W5x00_RSTn)
ethernetRst.direction = digitalio.Direction.OUTPUT

# Set this SPI for selecting the correct chip
cs = digitalio.DigitalInOut(SPI0_CSn)

# Set the GPIO pins for SPI communication
spi_bus = busio.SPI(SPI0_SCK, MOSI=SPI0_TX, MISO=SPI0_RX)

# Reset WIZnet's chip first
ethernetRst.value = False
time.sleep(1)
ethernetRst.value = True

class bigiot:
    confirmed = 0 #flag variable to control the data to send out
    temp_value = 0 #Testing variables 
    checkout_time = 10 # the number of data that could send out to the IOT platform
    def checking (self,datain): #function to check the connecting status
        checked = None
        
        if datain.find('"M":') == 1:
            found = datain.split('"M":')
            if found[1].find('"WELCOME') == 0: #check is it connected to the platform
                checked = '{"M":"checkin","ID":"AAAAA","K":"XXXXXX"}\n' #login to the platform
                
            elif found[1].find('"checkinok"') == 0:
                self.confirmed = 1
                
            elif found[1].find('"b"') == 0:
                checked = '{"M":"beat"}\n'
        return checked
    
    def transmit (self): #function for transmitting the data
        temp = None
        if self.confirmed == 1:
            self.temp_value += 1
            temp = '{"M":"u","ID":"AAAAAA","V":{"BBBBB":"'+str(self.temp_value)+'"}}\n' #format to send data
            time.sleep(5)
        return temp
    
    def checkout (self,waited):
        if  waited == self.checkout_time:
            logout = '{"M":"checkout","ID":"AAAAAA","K":"XXXXXX"}\n' #logout from the platform
            print('Disconnected') #Server will disconnect with us
            return logout

# Initialize ethernet interface with DHCP
eth = WIZNET5K(spi_bus, cs, is_dhcp=True, mac=MY_MAC, debug=False)

# Show all information
print("Chip Version:", eth.chip)
print("MAC Address:", [hex(i) for i in eth.mac_address])
print("My IP address is:", eth.pretty_ip(eth.ip_address))

# Initialize steps for WIZnet's socket to create TCP server
socket.set_interface(eth)
client = socket.socket()  # Set and name the socket to be a TCP server
client_ip = "bigiot.net"  #Set the TCP Server IP address. As in this case, it does not required
client_port = 8282  # Port number to listen on
client.connect((client_ip, client_port), None)

counter = 0
wiz_big = bigiot()
while True:
# Maintain DHCP lease (continue the DHCP setting while TCP is connected)
    eth.maintain_dhcp_lease()

    led.value = not led.value #showing the light is blinking
    time.sleep(0.1) #transmit data speed
    
    if client.status == SNSR_SOCK_ESTABLISHED:
        data = client.recv() # Data size that you could receive
        data2 = data.decode("UTF-8")
        
        check = wiz_big.checking(data2)
        value = wiz_big.transmit()
        logout = wiz_big.checkout(counter)
        if check != None:
            client.send(check.encode())
        if value != None and logout == None:
            client.send(value.encode()) 
            counter += 1
        if logout != None:
            client.send(logout.encode()) 
        print(data) #print out the data that you sent
        
