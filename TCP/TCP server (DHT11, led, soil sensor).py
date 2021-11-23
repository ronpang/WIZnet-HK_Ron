import board
import digitalio
import analogio
import time
import busio
from adafruit_wiznet5k.adafruit_wiznet5k import * #active WIZnet chip library
import adafruit_wiznet5k.adafruit_wiznet5k_socket as socket #open socket from WIZnet library

import adafruit_dht #DHT library

# Activate GPIO pins for SPI communication
SPI0_SCK = board.GP18
SPI0_TX = board.GP19
SPI0_RX = board.GP16
SPI0_CSn = board.GP17

# Activate Reset pin for communication with W5500 chip
W5x00_RSTn = board.GP20

dhtDevice = adafruit_dht.DHT11(board.GP0) #DHT pin 

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

# Set external RED LED for controlling purpose
led_red = digitalio.DigitalInOut(board.GP1)
led_red.direction = digitalio.Direction.OUTPUT

# Set A0 for receving data from the soil hudmidity module
soil = analogio.AnalogIn(board.A0)

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

# Initialize ethernet interface with DHCP
eth = WIZNET5K(spi_bus, cs, is_dhcp=True, mac=MY_MAC, debug=False)

# Show all information
print("Chip Version:", eth.chip)
print("MAC Address:", [hex(i) for i in eth.mac_address])
print("My IP address is:", eth.pretty_ip(eth.ip_address))

# Find the range for dry and value value of the soil sensor
#Waiting time for changing to collecting dry value
delay_counter = 0
while delay_counter < 10:
    delay_counter = delay_counter + 1
    print("Please change to collect dry value..." + str(delay_counter))
    time.sleep(1)

# Collecting the dry value (Air value)
dry_counter= 0
dry_number = 0
dry_average = 0
while dry_counter < 100: #collect 100 samples
    dry_counter= dry_counter + 1
    dry_number = soil.value + dry_number
    time.sleep(0.1)
    print ("Dry value counting..." + str(dry_counter))

#Average dry value
dry_average = dry_number / dry_counter
print('Average(dry): '+ str(dry_counter) +' '+ str(dry_average))

#Waiting time for changing to collecting wet value
delay_counter = 0
while delay_counter < 10:
    delay_counter = delay_counter + 1
    print("Please change to collect wet value..." + str(delay_counter))
    time.sleep(1)

# Collecting the wet value (Water value)
wet_counter= 0
wet_number = 0
wet_average = 0
while wet_counter <100: #collect 100 samples 
    wet_counter = wet_counter + 1
    wet_number  = soil.value + wet_number
    time.sleep(0.1)
    print ("Wet value counting..." + str(wet_counter))

#Average wet value
wet_average = wet_number / wet_counter
print('Average(wet): '+ str(wet_counter) +' '+ str(wet_average))

# Initialize steps for WIZnet's socket to create TCP server
socket.set_interface(eth)
server = socket.socket()  # Set and name the socket to be a TCP server
server_ip = None  #Set the TCP Server IP address. As in this case, it does not required
server_port = 50007  # Port number to listen on
server.bind((server_ip, server_port))  # Binding the IP address and Port number 
server.listen()  # Begin listening for incoming clients

#the variable for checking the connection status
conn= None
led_red.value = 0
counter= 0

while True:
# Maintain DHCP lease (continue the DHCP setting while TCP is connected)
    eth.maintain_dhcp_lease()

    led.value = not led.value #showing the light is blinking
    time.sleep(0.1) #transmit data speed
    counter= counter+1    


    if conn is None: #Not connected - just to this stage and wait for connection
        conn, addr = server.accept()  # Wait for a connection from a client.
        print("socket connected")
    
    
    else:
        if conn.status in (SNSR_SOCK_FIN_WAIT,): #Socket is closed, you could close your Socket
            conn.close()
            conn = None
            counter = 0
             
        elif conn.status in (SNSR_SOCK_CLOSE_WAIT,):# Closing stage, close connection
            conn.disconnect() #close the connection
            conn.close() #close the socket
            conn = None # reset the variable for the next connection
            counter = 0
            
        else: #other condition - TCP connection has been established
                        
            data = conn.recv() # Data size that you could receive
            conn.send(data) # Echo message back to client
            #print(data) #print out the data that you sent
            
            data2 = data.decode("UTF-8") #decode the data receive from TCP
            
            #Check value to on and off the LED light
            if data2 == "on": 
                led_red.value = 1 #turn on
            elif data2 == "off":
                led_red.value = 0 #turn off
            try:     
                if counter == 50: #wait for 5 seconds
                    counter = 0
                    #Temperature sensor convert from int to string to byte
                    temp_reading = dhtDevice.temperature
                    temp_tostring ='Temperature: ' + str(temp_reading) + '\r\n'
                    temp_convert = temp_tostring.encode()
                       
                    #Humidity sensor convert from int to string to byte
                    humid_reading = dhtDevice.humidity
                    humid_tostring = 'Humid: ' + str(humid_reading) + '\r\n'
                    humid_convert = humid_tostring.encode()
                    
                    #Soil Humidity sensor
                    if soil.value < dry_average or soil.value > wet_average:
                        soil_humid_tostring = "Error value, please put the sensor to your plant\r\n"
                        soil_humid_convert = soil_humid_tostring.encode() 
                
                    else:
                        percentage_value = (soil.value - dry_average) / ((wet_average - dry_average)/100)
                        soil_humid_tostring ='Soil: ' + str(percentage_value) + '\r\n'
                        soil_humid_convert = soil_humid_tostring.encode()               

                
                    #send temperature and humidity data
                    conn.send(temp_convert)  
                    conn.send(humid_convert)
                    conn.send(soil_humid_convert)
                
            except RuntimeError as error:
                # Errors happen fairly often, DHT's are hard to read, just keep going
                print(error.args[0])
                time.sleep(2.0)
                continue
            except Exception as error:
                dhtDevice.exit()
                raise error
                
            
