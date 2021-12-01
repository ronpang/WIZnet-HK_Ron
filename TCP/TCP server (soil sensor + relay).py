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

import os

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

# Set external relay for controlling the valve
relay = digitalio.DigitalInOut(board.GP0)
relay.direction = digitalio.Direction.OUTPUT

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
eth = WIZNET5K(spi_bus, cs, is_dhcp=True, mac=MY_MAC, debug=True)

# Show all information
print("Chip Version:", eth.chip)
print("MAC Address:", [hex(i) for i in eth.mac_address])
print("My IP address is:", eth.pretty_ip(eth.ip_address))

#Set the soil moisture precentage range
class Soil_range_set:

# Waiting time for changing to collecting dry value
    def delay(self,counter,condition):
        message = "Please change to collect {} value...{}\r\n".format(condition,counter)
        time.sleep(1)
        return message

# Collecting value 
    def value_collect(self,counter,condition,collected):
        collected= soil.value + collected
        time.sleep(0.1)
        message = "{} value counting...{}\r\n".format(condition, counter)
        return message , collected

#Average calculation
    def Average_count(self,counter,collected):
        average = collected / counter
        return average

#function manage the DHT and soil moisture data into related string
def collect_data(dry_average, wet_average):                    
    #Soil Humidity sensor
    if soil.value < dry_average or soil.value > wet_average:
        All_tostring =  "error"
        percentage_value = 0   
    else:
        percentage_value = (soil.value - dry_average) / ((wet_average - dry_average)/100)
        #Soil Mositure sensor convert from int to string to byte (with time value)
        cal = ntp.get_time()
        All_tostring = "{:02}/{:02}/{:04}-{:02}:{:02}:{:02}-Soil Moisture:{:02}            \r\n".format(cal.tm_mday,cal.tm_mon,cal.tm_year,cal.tm_hour,cal.tm_min,cal.tm_sec,int(percentage_value))
        
    return All_tostring, percentage_value  
            
    
#NTP
ntpserver_ip = eth.pretty_ip(eth.get_host_by_name("time.google.com")) #collect IP address from google and set it for NTP IP address
print("NTP : %s" % ntpserver_ip)  #DNS Domain
ntp = NTP(iface = eth, ntp_address =ntpserver_ip ,utc=8) #ntp fuction activate (Use 1 socket)
cal = ntp.get_time() 

# Initialize steps for WIZnet's socket to create TCP server
socket.set_interface(eth)
server = socket.socket()  # Set and initizalize the socket to be a TCP server
server_ip = None  #Set the TCP Server IP address. As in this case, it does not required
server_port = 50007  # Port number to listen on
server.bind((server_ip, server_port))  # Binding the IP address and Port number 
server.listen()  # Begin listening for incoming clients


#the variable for checking the connection status
soil_setting = Soil_range_set() #activate the class function
soil_collected = 0 # For calculating the average value for the soil sensor
soil_counter = 0 #calculate the amount of value that has been taken
soil_delay = 0 # for providing delay time to change the sensor to collect different values (Dry / Wet)
dry_average = 0 #dry average varibale 
wet_average = 0 #Wet average varibale 
soil_condition = "dry" #Determine the value that I need to collect - first dry value, then wet value
data_flag = "off" #Confirmation flag to allow data transmission 
soil_flag = "off" #Checking the soil moisture sensor has set it's range before collecting data
relay_flag = 0 # flag to control the relay
conn= None
led.value = 0
relay.value = 0 #control the relay for opening the valve
delay_counter= 0 #delay the readings

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
        #print(conn.status)
        if conn.status in (SNSR_SOCK_FIN_WAIT,): #Socket is closed, you could close your Socket
            conn.close()
            conn = None
            delay_counter = 0
                    
        elif conn.status in (SNSR_SOCK_CLOSE_WAIT,):# Closing stage, close connection
            conn.disconnect() #close the connection
            conn.close() #close the socket
            conn = None # reset the variable for the next connection
            delay_counter = 0
                        
        elif conn.status in (SNSR_SOCK_CLOSED,):
            conn = None
            delay_counter = 0
            
            
        elif conn.status in (SNSR_SOCK_ESTABLISHED,): #other condition - TCP connection has been established
                     
            data = conn.recv() # Data size that you could receive
            #conn.send(data) # Echo message back to client
            #print(data) #print out the data that you sent
            
            data2 = data.decode("UTF-8") #decode the data receive from TCP
            
            #Relay manual control
            if data2 == "on": 
                relay.value = 1 #turn on
                relay_flag = 0 #turn off automatic control
            elif data2 == "off":
                relay.value = 0 #turn off
                relay_flag = 1 #turn on automatic control
            
            if data2 == "soil reset" or soil_flag == "on":
                soil_flag = "on"
                if soil_delay <10:
                    soil_delay = soil_delay + 1
                    msg = soil_setting.delay(soil_delay,soil_condition)
                if soil_delay == 10 and soil_counter <100:
                    soil_counter = soil_counter + 1
                    msg, soil_collected = soil_setting.value_collect(soil_counter,soil_condition,soil_collected)
                if soil_delay ==10 and soil_counter ==100 and soil_condition == "dry":
                    dry_average = soil_setting.Average_count(soil_counter, soil_collected)
                    soil_condition = "wet"
                    soil_collected = 0
                    soil_counter = 0
                    soil_delay = 0
                if soil_delay ==10 and soil_counter ==100 and soil_condition == "wet":
                    wet_average = soil_setting.Average_count(soil_counter, soil_collected)
                    data_flag = "on"
                    soil_flag = "off"
            elif data_flag == "off" and soil_flag == "off" :
                msg = "Please input 'soil reset' to reset the soil sensor\r\n"
                
            if data_flag == "off":
                data = conn.send(msg.encode())
                
            if delay_counter > 5 and data_flag == "on":#wait for 0.5 seconds
                delay_counter = 0
                All_tostring, percentage_value = collect_data(dry_average,wet_average)
                if All_tostring == "error":
                    All_tostring = "Error value, please put the sensor to your plant\r\n"
                #make sure the automation flag is on to use the sensor measurement
                if percentage_value < 20 and relay_flag == 1:
                     relay.value = 1
                else:
                    relay.value = 0
                All_convert = All_tostring.encode()
                if conn.status in (SNSR_SOCK_ESTABLISHED,):
                    #send all data in one string with date
                    conn.send(All_convert)  

                elif conn.status in (SNSR_SOCK_CLOSE_WAIT,):
                    conn.disconnect() #close the connection
                    conn.close() #close the socket
                    conn = None # reset the variable for the next connection
                    delay_counter = 0
                    
                elif conn.status in (SNSR_SOCK_CLOSED,):
                    conn = None
                    delay_counter = 0

            

             

            
