# WIZnet WIZnet Ethernet Hat with Raspberry PI PICO 
1. [Introduction](#introduction) 

2. [TCP Application](#TCPapplication)

3. [Adafruit IO Upgrade](#AdafruitIO)

4. [Others](#Others)

<a name="introduction"></a>

# 🔴Introduction

This site is creating different kind of related codings and application based on WIZnet's solution with Raspberry PI PICO. 
For more information, please refer to the links below.

[WIZnet's Ethernet Hat ][link-getting_started]

[WIZnet's Example codings][link-all examples]

<a name="TCPapplication"></a>

# 💻 TCP Application
WIZnet's TCP's sample codes to create a step by step codings for developing different kind of applications 

1. [TCP communication][link-tcp communication] - Echo TCP server example with Status register controls from WIZnet's chip. (Based on WIZnet's [TCP Echo][link-tcp echo] example)
2. [TCP with DHT11 Sensor and light controls][link-DHT11 led] - TCP communication to monitor records from Adding DHT11 and controls a Red LED light blub
3. [TCP with Soil moisture, DHT sensor and light control][link-DHT11 led soil moisture] -Combined everything and use WIZnet's Ehternet HAT for TCP communication
4. [TCP Pixel light control][link-TCP light control] - Contain a light sensor, using command to control on/off and color change (Based on WIZnet's [Neopixel][link-wiznet neopiexl] example)

<a name="AdafruitIO"></a>

# 🗺️ Adafruit IO Upgrade
WIZnet's Adafruiit IO samples codes with related application (Ref: [WIZnet's Ethernet HAT Adafruit IO][link-adafruit_io_wiznet] & [WIZnet's Adafruit IO][link-adafruit_io_wiznet_example] example)

1. [Adafruit IO Part 1][link-adafruitio1] - Contain DHT 11, Light controls and Soil Moisture sensor data upload and download 
2. [Adafruit IO Part 2][link-adafruitio2] - Contain Light Sensor module to determine brightness and a Pixel Led light 

<a name="Others"></a>
# 📓 Others
1. [Soil moisture sensor module][link-soil moisture] - Codings for Soil moisture sensor's range setting and collect moisture

[link-getting_started]: https://github.com/Wiznet/RP2040-HAT-CircuitPython/blob/master/Ethernet%20Example%20Getting%20Started%20%5BCircuitpython%5D.md
[link-all examples]:https://github.com/Wiznet/RP2040-HAT-CircuitPython/tree/master/examples
[link-tcp communication]:https://github.com/ronpang/WIZnet-HK_Ron/blob/main/TCP/TCP%20server.py
[link-DHT11 led]:https://github.com/ronpang/WIZnet-HK_Ron/blob/main/TCP/TCP%20server%20(DHT11%2C%20led).py
[link-soil moisture]:https://github.com/ronpang/WIZnet-HK_Ron/blob/main/Soil%20Sensor/Soil%20sensor%20settings.py
[link-DHT11 led soil moisture]: https://github.com/ronpang/WIZnet-HK_Ron/blob/main/TCP/TCP%20server%20(DHT11%2C%20led%2C%20soil%20sensor).py
[link-adafruitio1]:https://github.com/ronpang/WIZnet-HK_Ron/blob/main/Adafruit%20io/Adafruit%20io%20(DHT11%2C%20led%2C%20soil%20sensor).py
[link-tcp echo]:https://github.com/Wiznet/RP2040-HAT-CircuitPython/blob/master/examples/Network/W5x00_Echo_Demo_TCP.py
[link-adafruit_io_wiznet_example]:https://github.com/Wiznet/RP2040-HAT-CircuitPython/tree/master/examples/Adafruit_IO
[link-adafruit_io_wiznet]:https://github.com/Wiznet/RP2040-HAT-CircuitPython/blob/master/examples/Adafruit_IO/Getting%20Start%20Adafruit%20IO.md
[link-TCP light control]: https://github.com/ronpang/WIZnet-HK_Ron/blob/main/TCP/TCP%20server%20(Neopixel%20light%20control).py
[link-wiznet neopiexl]: https://github.com/Wiznet/RP2040-HAT-CircuitPython/blob/master/examples/Neopixel/W5x00_Neopixel.py
[link-adafruitio2]: https://github.com/ronpang/WIZnet-HK_Ron/blob/main/Adafruit%20io/Adafruit%20io%20(Neopixel%20light%20control).py
