## Connection diagram ##

![][link-connection diagram]

## Suggested TCP terminal Software ##
 [**Hercules**][link-hercules]
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

Updated:

1. DHT11 - added runtime error handling

## Soil moisture sensor and Relay ##

Added:

1. Soil moisture sensor 
    1. Converting adc values to percentage values(%) ([Soil moisture sensor coding][link-soil moisture readme])
    2. Find the mositure range of the sensor 
2. Relay - controls the valve for water input.
    1. Manual
    2. Automatic - determine by the percentage values from the soil moist sensor

Updated:
1. Class function (Soil_range_set) for simplify the function

## Neopixel light control with light sensor ##
It is based on the above TCP server code.

Added:

1. Light sensor module (Diode type Photosensitive Sensor)
     1. Converting adc values to  percentage values (%), based on this value to change the brightness of the Pixel LED
2. Commands to control on/off and color
     1. Determine the command (on/off) and do related response
     2. Inputting RBG values in interger form (xxx,xxx,xxx) to change the color of the Pixel leds 

## TCP Server with File records ##
Bsed on TCP Server with file features in Raspberry PI PICO

File settings are required for Circuit Python coding - For more information, please refer adafruit's file settings. ([Information][link - boot.py])

Example feature:

DHT11 - Readings from DHT11 will be record in temp_humid.txt

Added: 
1. SNTP - Real time collected from DNS sever and will be record in temp_humid.txt 


[link-hercules]: https://www.hw-group.com/software/hercules-setup-utility
[link-connection diagram]: https://github.com/ronpang/WIZnet-HK_Ron/blob/main/TCP/connection%20diagram%20-%20github.PNG
[link-soil moisture readme]: https://github.com/ronpang/WIZnet-HK_Ron/blob/main/Soil%20Sensor/README.md
[link - boot.py]:https://learn.adafruit.com/getting-started-with-raspberry-pi-pico-circuitpython/data-logger
