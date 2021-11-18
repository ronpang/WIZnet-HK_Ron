## Connection diagram ##

![][link-connection diagram]

## TCP server ##

This sample code is based on TCP server Echo provided by WIZnet  
- TCP server rather than using client is allowing user doesn't need to change their code frequently. 

Device:
1. Raspberry PI PICO - The mainboard converted to circuit python and bundle with adafruit's and WIZnet's library
2. WIZnet Ethernet HAT - Provides the Ethernet feature 

Modified: 

* Status register checking to handle different kind of communication stage  

## DHT11 and LED control ##

It is based on the above TCP server code.

Added:
1. DHT11 temperature and humidity sensor
2. LED light control 

## DHT11, LED control and Soil moisture sensor ##

Added:

1. DHT11 and LED light control 
2. Added Soil moisture sensor 
    1. Converting adc values to percentage values(%) ([Soil moisture sensor coding][link-soil moisture readme])
    2. Find the mositure range of the sensor 

## Neopixel light control with light sensor ##

1. Light sensor module
     1. Converting adc values to  percentage values (%), based on this value to change the brightness of the Pixel LED
2. Commands to control on/off and color
     1. Determine the command (on/off) and do related response
     2. Inputting RBG values in interger form (xxx,xxx,xxx) to change the color of the Pixel leds 



[link-connection diagram]: https://github.com/ronpang/WIZnet-HK_Ron/blob/main/TCP/github-%20connection%20diagram.PNG
[link-soil moisture readme]: https://github.com/ronpang/WIZnet-HK_Ron/blob/main/Soil%20Sensor/README.md
