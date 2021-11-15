# WIZnet WIZnet Ethernet Hat with Raspberry PI PICO 
[Introduction](#introduction) 

[Application](#application)

<a name="introduction"></a>

# 🔴Introduction

This site is creating different kind of related codings and application based on WIZnet's solution with Raspberry PI PICO. 
For more information, please refer to the links below.

[WIZnet's Ethernet Hat ][link-getting_started]

[WIZnet's Example codings][link-all examples]

<a name="application"></a>

# 🔴Application
The followings codes is using WIZnet's sample codes to create a step by step codings for developing different kind of applications

1. [TCP communication][link-tcp communication] - Echo TCP server example with Status register controls from WIZnet's chip. (based on WIZnet's [TCP Echo][link-tcp echo] example)
2. [TCP with DHT11 Sensor and light controls] - TCP communication to monitor records from Adding DHT11 and controls a Red LED light blub
3. [Soil moisture sensor module] - Codings for Soil moisture sensor's range setting and collect moisture
4. [TCP with Soil moisture, DHT sensor and light control] -Combined everything and use WIZnet's Ehternet HAT for TCP communication
5. [Adafruit_io Part 1] - Contain DHT 11, Light controls and Soil Moisture sensor data upload and download (For more information about Adafruit io, please refer [WIZnet's Ethernet HAT Adafruit IO example][link-adafruit_io_wiznet])([WIZnet's Adafruit IO codes][link-adafruit_io_wiznet_example])




[link-tcp communication]:https://github.com/ronpang/WIZnet-HK_Ron/blob/main/TCP%20server.py
[link-all examples]:https://github.com/Wiznet/RP2040-HAT-CircuitPython/tree/master/examples
[link-tcp echo]:https://github.com/Wiznet/RP2040-HAT-CircuitPython/blob/master/examples/Network/W5x00_Echo_Demo_TCP.py
[link-adafruit_io_wiznet_example]:https://github.com/Wiznet/RP2040-HAT-CircuitPython/tree/master/examples/Adafruit_IO
[link-adafruit_io_wiznet]:https://github.com/Wiznet/RP2040-HAT-CircuitPython/blob/master/examples/Adafruit_IO/Getting%20Start%20Adafruit%20IO.md
[link-getting_started]: https://github.com/Wiznet/RP2040-HAT-CircuitPython/blob/master/Ethernet%20Example%20Getting%20Started%20%5BCircuitpython%5D.md
