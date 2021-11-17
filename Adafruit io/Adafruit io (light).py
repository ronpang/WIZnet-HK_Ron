import board
import busio
import digitalio
import analogio
import time
import neopixel
from random import randint

import adafruit_dht

from adafruit_wiznet5k.adafruit_wiznet5k import *
import adafruit_wiznet5k.adafruit_wiznet5k_socket as socket

from adafruit_io.adafruit_io import IO_MQTT
import adafruit_minimqtt.adafruit_minimqtt as MQTT

secrets = {
    'aio_username' : '******',   ### Wirte Username here ###
    'aio_key' : '*******'  ### Write Active Key here ###
    }

# Set your Adafruit IO Username and Key in secrets.py
# (visit io.adafruit.com if you need to create an account,
# or if you need your Adafruit IO key.)
aio_username = secrets["aio_username"]
aio_key = secrets["aio_key"]

#SPI
SPI0_SCK = board.GP18
SPI0_TX = board.GP19
SPI0_RX = board.GP16
SPI0_CSn = board.GP17

#Reset
W5x00_RSTn = board.GP20


print("Wiznet5k Adafruit Up&Down Link Test (DHCP)")
# Setup your network configuration below
# random MAC, later should change this value on your vendor ID
MY_MAC = (0x00, 0x01, 0x02, 0x03, 0x04, 0x05)
IP_ADDRESS = (192, 168, 1, 100)
SUBNET_MASK = (255, 255, 255, 0)
GATEWAY_ADDRESS = (192, 168, 1, 1)
DNS_SERVER = (8, 8, 8, 8)

# Activate the Pixel pins
pixel_pin = board.GP0
num_pixels = 12 #open how many leds in the Pixel

# Set A1 for receving data from the light sensor module
light = analogio.AnalogIn(board.A1)

ethernetRst = digitalio.DigitalInOut(W5x00_RSTn)
ethernetRst.direction = digitalio.Direction.OUTPUT

# For Adafruit Ethernet FeatherWing
cs = digitalio.DigitalInOut(SPI0_CSn)
# For Particle Ethernet FeatherWing
# cs = digitalio.DigitalInOut(board.D5)

spi_bus = busio.SPI(SPI0_SCK, MOSI=SPI0_TX, MISO=SPI0_RX)

# Reset W5x00 first
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

### Topic Setup ###
# Adafruit IO-style Topic
# Use this topic if you'd like to connect to io.adafruit.com
# mqtt_topic = secrets["aio_username"] + '/feeds/test'

### Code ###
# Define callback methods which are called when events occur
# pylint: disable=unused-argument, redefined-outer-name
def connected(clinet):
    # This function will be called when the mqtt_client is connected
    # successfully to the broker.
    print("Connected to Adafruit IO!")
    
    # Subscribe to Group
    io.subscribe(group_key=group_name)

def disconnected(clinet):
    # This method is called when the mqtt_client disconnects
    # from the broker.
    print("Disconnected from Adafruit IO!")

def subscribe(client, userdata, topic, granted_qos):
    # This method is called when the client subscribes to a new feed.
    print("Subscribed to {0} with QOS level {1}".format(topic, granted_qos))
    
def message(client, topic, message):
    # Method callled when a client's subscribed feed has a new value.
    print("New message on topic {0}: {1}".format(topic, message))

def on_led_color(client, topic, message):
    # Method callled when a client's subscribed feed has a new value.
    print("New message on topic {0}: {1}".format(topic, message))
    if message.find("#") == 0:
        message.split("#", 6)
        hex1 = int(message[1] + message[2],16)
        hex2 = int(message[3] + message[4],16)
        hex3 = int(message[5] + message[6],16)
        pixels.fill((hex1,hex2,hex3))
        pixels.show() #Change color
        
    else:
        print("Unexpected message on LED feed")

def on_led_onoff(client, topic, message):
    # Method callled when a client's subscribed feed has a new value.
    global light_onoff
    global brightness
    print("New message on topic {0}: {1}".format(topic, message))
    if message == "on":
        light_onoff = 1
        if brightness == 0:
            pixels.brightness = 0.1    #turn on the light to lowest brightness (default)
        else:
            pixels.brightness = brightness #if there is brightness changes, it will based on changed brightness value
            
        pixels.show() #Turn ON
    elif message == "off":
        light_onoff = 0
        pixels.brightness = 0
        pixels.show() #Turn OFF
    else:
        print("Unexpected message on LED feed")

def on_sensor_onoff(client, topic, message): 
    # Method callled when a client's subscribed feed has a new value.
    global sensor_onoff 
    print("New message on topic {0}: {1}".format(topic, message))
    if message == "on": # turn on the light sensor 
        sensor_onoff = 1
    elif message == "off": #turn off the light sensor
        sensor_onoff = 0
    else:
        print("Unexpected message on LED feed / the led is off")
        
def on_led_bright(client, topic, message):
    # Method callled when a client's subscribed feed has a new value.
    global light_onoff
    global sensor_onoff
    global brightness
    print("New message on topic {0}: {1}".format(topic, message))
    if message.isdigit() == True:
        brightness = int(message)/100 #accept the changes of the brightness
        if sensor_onoff == 0 and  light_onoff == 1:
            pixels.brightness = brightness #change the brightness when it is on
            pixels.show()
    else:
        print("The light sensor is on")

# Initialize MQTT interface with the ethernet interface
MQTT.set_socket(socket, eth)

# Initialize a new MQTT Client object
mqtt_client = MQTT.MQTT(
    broker="io.adafruit.com",
    username=secrets["aio_username"],
    password=secrets["aio_key"],
    is_ssl=False,
)

# Initialize an Adafruit IO MQTT Client
io = IO_MQTT(mqtt_client)

# Setup the callback methods above
io.on_connect = connected
io.on_disconnect = disconnected
io.on_message = message
io.on_subscribe = subscribe

# Set up a callback for the led feed
io.add_feed_callback("led-onoff", on_led_onoff)
io.add_feed_callback("led-color", on_led_color)
io.add_feed_callback("sensor-onoff", on_sensor_onoff)
io.add_feed_callback("led-brightness", on_led_bright) 

# Group name
group_name = "weatherstation"

# Feeds within the group
temp_feed = "weatherstation.temperature"
humid_feed = "weatherstation.humidity"
soil_feed = "weatherstation.soil"

# Connect to Adafruit IO
print("Connecting to Adafruit IO...")
io.connect()

# # Subscribe to all messages on the led feed
io.subscribe("led-onoff")
io.subscribe("led-color")
io.subscribe("sensor-onoff")
io.subscribe("led-brightness")
print("Connected to Adafruit !!")

# Activate the Neopixel - status Turn off, the default color is white
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0, auto_write=False)
pixels.fill((255,255,255)) # set to turn off the pixel
pixels.show()

# Set global variables for controlling the lights and sensors

global light_onoff #Light on/off
global brightness  #Brightness control
global sensor_onoff  # Sensor on/off
light_onoff = 0
brightness = 0
sensor_onoff = 0

#Random Data Send to Adafurit IO
while True:
    io.loop()
    if sensor_onoff == 1 and light_onoff == 1: #when the sensor is on and the light is turn on 
        light_per= light.value/ 65535* 100 #convert to %
        #print("light(%):" + str(light_per))
        for i in range(10):
            if light_per > i*10 and light_per < i*10 +10: # check the value is in which range
                value = (10-i)/10 #calucate the related brightness based on light sensor 
                #print(value)
                brightness = value #set the value into global
                pixels.brightness = brightness # change the light
                pixels.show() #change the brightness
    