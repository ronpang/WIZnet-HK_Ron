import board
import digitalio
import analogio
import time
import busio
#WIZnet's required library
from adafruit_wiznet5k.adafruit_wiznet5k import * #active WIZnet chip library
import adafruit_wiznet5k.adafruit_wiznet5k_socket as socket #open socket from WIZnet library
#WIZnet's library for creating NTP
from adafruit_wiznet5k.adafruit_wiznet5k_ntp import NTP #NTP library
import adafruit_wiznet5k.adafruit_wiznet5k_dns as dns #DNS library
import adafruit_requests as requests #adafruit's request library

import adafruit_dht #DHT library
import os

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
eth = WIZNET5K(spi_bus, cs, is_dhcp=True, mac=MY_MAC, debug=True)

# Show all information
print("Chip Version:", eth.chip)
print("MAC Address:", [hex(i) for i in eth.mac_address])
print("My IP address is:", eth.pretty_ip(eth.ip_address))


#function manage the DHT and soil moisture data into related string
def collect_data():
    try:
        #Collect Temperature and Humidity readings
        temp_reading = dhtDevice.temperature
        humid_reading = dhtDevice.humidity
        cal = ntp.get_time() #collect the current time (through NTP server)
        #Set the current time and all the readings and put it all in 1 string
        All_tostring = "{:02}/{:02}/{:04}-{:02}:{:02}:{:02}-Temperature:{:02},Humidity:{:02}\r\n".format(cal.tm_mday,cal.tm_mon,cal.tm_year,cal.tm_hour,
                                                                                                                                 cal.tm_min,cal.tm_sec,temp_reading,humid_reading)
        return All_tostring   
    
    except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going
        print(error.args[0])
        time.sleep(2.0)
        error_result = "error"
        return error_result
    except Exception as error:
        dhtDevice.exit()
        raise error
    
#Simple function to find the records    
def find_record(search):
    findremove = search.split("find ",1) #command is "find " (space included), seperate the data from the command
    tempfile = open("temp_humid.txt","r") #open the file
    tempdata = tempfile.read() #read all data
    if tempdata.find(findremove[1]) == -1: #if there is no data, or the user inputs the wrong information, it will show "no record"
        record = "No record\r\n"
    else: #record found
        line = tempdata.find(findremove[1])/65 #each line = 65 bytes
        with open("temp_humid.txt") as f:
            record = f.readlines()[int(line)] #saved that line

    return record           
    
#NTP
ntpserver_ip = eth.pretty_ip(eth.get_host_by_name("time.google.com")) #connect to NTP - using google time (convert it back to IP address by using DNS protocol)
print("NTP : %s" % ntpserver_ip)  #DNS Domain
ntp = NTP(iface = eth, ntp_address =ntpserver_ip ,utc=8) #set the correct time 
cal = ntp.get_time() #collect the time 

# Initialize steps for WIZnet's socket to create TCP server
socket.set_interface(eth)
server = socket.socket()  # Set and initizalize the socket to be a TCP server
server_ip = None  #Set the TCP Server IP address. As in this case, it does not required
server_port = 50007  # Port number to listen on
server.bind((server_ip, server_port))  # Binding the IP address and Port number 
server.listen()  # Begin listening for incoming clients


#the variable for checking the connection status
conn= None
led_red.value = 0
delay_counter= 0

while True:
# Maintain DHCP lease (continue the DHCP setting while TCP is connected)
    eth.maintain_dhcp_lease()

    led.value = not led.value #showing the light is blinking
    time.sleep(0.1) #transmit data speed
    delay_counter= delay_counter + 1     


    if conn is None: #Not connected - just to this stage and wait for connection
        conn, addr = server.accept()  # Wait for a connection from a client.
        print("socket connected")
    
    
    else:
        if conn.status in (SNSR_SOCK_FIN_WAIT,): #Disconnected, you could close your Socket
            conn.close() #close the socket
            conn = None # reset the variable for the next connection
            delay_counter = 0
                    
        elif conn.status in (SNSR_SOCK_CLOSE_WAIT,):# Closing stage, close connection
            conn.disconnect() #close the connection
            conn.close() #close the socket
            print(conn.connected)
            conn = None # reset the variable for the next connection
            delay_counter = 0
                        
        elif conn.status in (SNSR_SOCK_CLOSED,): #prevent any sudden disconnection. Reset the variable for next TCP connection 
            conn = None  # reset the variable for the next connection
            delay_counter = 0
            
            
        elif conn.status in (SNSR_SOCK_ESTABLISHED,): #TCP connection has been established
                     
            data = conn.recv() # Data size that you could receive
            conn.send(data) # Echo message back to client
            #print(data) #print out the data that you sent
            data2 = data.decode("UTF-8") #decode the data receive from TCP
            #Check value to on and off the LED light
            if data2 == "on": 
                led_red.value = 1 #turn on
            elif data2 == "off":
                led_red.value = 0 #turn off
                
            #Command 1 "find " - find the previous records from temp_humid.txt
            if data2.find("find") == 0:
                #Collect data to files are required time
                record = find_record(data2) #find record function 
                conn.send(record.encode())
                
            if delay_counter > 20:#wait until 2 seconds to collect 1 data from the sensor
                delay_counter = 0
                All_tostring = collect_data() #collect data function
                if All_tostring == "error": #feedback error 1 = Runtime error of DHT, let is rest and starts the reading again  
                    All_tostring = "DHT Runtime error, please ignore                                \r\n" #aligned with the temperature and humidity records
                else:
                    All_convert = All_tostring.encode() #encode to bytes
                
                if conn.status in (SNSR_SOCK_ESTABLISHED,): #Prevent any sudden disconnection, check the connection status before sending data out 
                    #send all data in one string with date
                    conn.send(All_convert) #send data
                    #record data to files are required time
                    tempfile = open("temp_humid.txt","a+") #open file
                    tempfile.write(All_tostring) #record all information 
                    tempfile.close() #close file
                    
                elif conn.status in (SNSR_SOCK_CLOSE_WAIT,): #if it is closed, turn off the connection 
                    conn.disconnect() #close the connection
                    conn.close() #close the socket
                    conn = None # reset the variable for the next connection
                    delay_counter = 0
                    
                elif conn.status in (SNSR_SOCK_CLOSED,): #Prevent any sudden disconnection. If it is closed, reset the variables
                    conn = None# reset the variable for the next connection
                    delay_counter = 0

            

             

            
