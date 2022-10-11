import board
import busio
import digitalio
import time

import circuitpython_hmac as hmac
import binascii

from adafruit_wiznet5k.adafruit_wiznet5k import *
import adafruit_wiznet5k.adafruit_wiznet5k_socket as socket

from adafruit_wiznet5k.adafruit_wiznet5k_ntp import NTP #NTP library
import adafruit_wiznet5k.adafruit_wiznet5k_dns as dns #DNS library

import adafruit_minimqtt.adafruit_minimqtt as MQTT


def set_password (cal_time):
#set the password
    print(cal_time)
    decoded_data = binascii.a2b_base64("CCCCCCCCCCCC") #C = device key

#other variables settings
    et = str(cal_time)
    method = "md5" 
    res = "products/AAAAAAA/devices/BBBBB" #A = Product ID, B = Device name
    version = "2018-10-31"
#create the signiture for the password
    secret = decoded_data
    msg = et + "\n" + method+ "\n" + res+ "\n" + version
    en_msg = msg.encode()
    key = hmac.new(secret, msg=en_msg, digestmod="md5").digest()
    encoded_data = binascii.b2a_base64(key).strip()
    encoded_data = encoded_data.decode("UTF-8")
    new_res = res.replace("/","%2F")
#modified the password into url format
    if encoded_data.find("=")>= 0:
        new_encoded_data = encoded_data.replace("=","%3D")
    if encoded_data.find("+")>= 0:
        new_encoded_data = new_encoded_data.replace("+","%2B")
    if encoded_data.find("/")>= 0:
        new_encoded_data = new_encoded_data.replace("/","%2F")

#combine the whole password
    login_msg = "version=" + version+ "&res=" + new_res+ "&et=" + et+ "&method=" + method+ "&sign="+ new_encoded_data
    return login_msg


### MQTT Setup ###
# MQTT Topic
# Use this topic if you'd like to connect to a standard MQTT broker
# pubs
Monitoring_pub = "$sys/AAAAAAA/BBBBBBBB/thing/property/post" # Subscribe channel for sending information to the platform
Control_pub = "$sys/AAAAAAA/BBBBBBBB/thing/property/set_reply" # Subscribe channel for returning message after received data from platform

#subs
Monitoring_sub = "$sys/AAAAAAA/BBBBBBBB/thing/property/post/reply" #Checking did the platform received message from the device
Control_sub = "$sys/AAAAAAA/BBBBBBBB/thing/property/set" #Receiving data from the platform

#MQTT send msg format
def Monitor_message_setup (cal_time):
    cal_time_ms = (cal_time- 28800) *1000
    cal_time_ms = str(cal_time_ms)
    Monitoring_msg = '{"id": "123","version": "1.0","params": {"Power": {"value": "500","time": '+cal_time_ms+'},"temp": {"value": 20,"time": '+cal_time_ms+'}}}'
    return Monitoring_msg



### Message Code ###
# Define callback methods which are called when events occur
# pylint: disable=unused-argument, redefined-outer-name
def message(client, topic, message):
    # Method callled when a client's subscribed feed has a new value.
    # print("New message on topic {0}: {1}".format(topic, message))
    # function used subs and pub (same like the above pub & subs)
    Monitoring_sub = "$sys/AAAAAAA/BBBBBBBB/thing/property/post/reply" 
    Control_sub = "$sys/AAAAAAA/BBBBBBBB/thing/property/set"
    Control_pub = "$sys/AAAAAAA/BBBBBBBB/thing/property/set_reply"
    counter = 0
    value = 0
    if (topic == Monitoring_sub and message.find('"code":200') >= 0 ):
        print("New message on topic {0} : {1}".format(topic, message))
    if topic == Control_sub:
        print("Received message on topic {0} : {1}".format(topic, message))
        s_msg = message.split('"id":"')

        while value != 1:
            if s_msg[1].find('{0}"'.format(counter)) == 0:
                print("found value = {0}".format(counter))
                value = 1
            counter += 1

        control_msg = '{"id":"'+str(counter-1)+'","code":200,"msg":"success"}'
        print(control_msg)
        mqtt_client.publish(Control_pub, control_msg)

 

#SPI0
SPI0_SCK = board.GP18
SPI0_TX = board.GP19
SPI0_RX = board.GP16
SPI0_CSn = board.GP17

#Reset
W5x00_RSTn = board.GP20

print("Wiznet5k MQTT Test (DHCP)")
# Setup your network configuration below
# random MAC, later should change this value on your vendor ID
MY_MAC = (0x00, 0x01, 0x02, 0x03, 0x04, 0x05)
IP_ADDRESS = (192, 168, 1, 100)
SUBNET_MASK = (255, 255, 255, 0)
GATEWAY_ADDRESS = (192, 168, 1, 1)
DNS_SERVER = (8, 8, 8, 8)

led = digitalio.DigitalInOut(board.GP25)
led.direction = digitalio.Direction.OUTPUT

ethernetRst = digitalio.DigitalInOut(W5x00_RSTn)
ethernetRst.direction = digitalio.Direction.OUTPUT

# For Adafruit Ethernet FeatherWing
cs = digitalio.DigitalInOut(SPI0_CSn)
# For Particle Ethernet FeatherWing
# cs = digitalio.DigitalInOut(board.D5)

spi_bus = busio.SPI(SPI0_SCK, MOSI=SPI0_TX, MISO=SPI0_RX)

# Reset W5500 first
ethernetRst.value = False
time.sleep(1)
ethernetRst.value = True

# # Initialize ethernet interface without DHCP
# eth = WIZNET5K(spi_bus, cs, is_dhcp=False, mac=MY_MAC, debug=False)
# # Set network configuration
# eth.ifconfig = (IP_ADDRESS, SUBNET_MASK, GATEWAY_ ADDRESS, DNS_SERVER)

# Initialize ethernet interface with DHCP
eth = WIZNET5K(spi_bus, cs, is_dhcp=True, mac=MY_MAC, debug=False)

print("Chip Version:", eth.chip)
print("MAC Address:", [hex(i) for i in eth.mac_address])
print("My IP address is:", eth.pretty_ip(eth.ip_address))

ntpserver_ip = eth.pretty_ip(eth.get_host_by_name("time.google.com"))
print("NTP : %s" % ntpserver_ip)  #DNS Domain
ntp = NTP(iface = eth, ntp_address =ntpserver_ip ,utc=8)
cal_time = ntp.get_time()
cal_time = time.mktime(cal_time) + 300000
login_msg = set_password(cal_time)

# Set up a MQTT Client
# NOTE: We'll need to connect insecurely for ethernet configurations.
mqtt_client = MQTT.MQTT(
    broker="218.201.45.7",  #MQTT server IP address
    port=1883,
    username="AAAAAA",  #username = product id    
    password=login_msg, #created by the function -> set_password
    client_id="BBBBBB", # client id = device name
    is_ssl=False,
    socket_pool=None,
    ssl_context=None,
    keep_alive=60,
)

# Initialize MQTT interface with the ethernet interface
MQTT.set_socket(socket, eth)

# Setup the callback methods above
mqtt_client.on_message = message

# Connect the client to the MQTT broker.
print("Connecting to Broker...")
mqtt_client.connect()

#MQTT Subscriber Run
while True:
    mqtt_client.loop()
    print("connected")
    #send a new message
    mqtt_client.subscribe(Monitoring_sub) 
    mqtt_client.subscribe(Control_sub)
    cal_time = ntp.get_time()
    Monitoring_msg = Monitor_message_setup(time.mktime(cal_time))
    print("Message to topic {0} : {1}".format(Monitoring_pub, Monitoring_msg))
    mqtt_client.publish(Monitoring_pub, Monitoring_msg)

    time.sleep(2)

#Disconnected
print("Disconnecting from %s" % mqtt_client.broker)
