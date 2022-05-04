# WIZnet WIZnet Ethernet Hat with Raspberry PI PICO 
1. [Introduction](#introduction) 

2. [TCP Application](#TCPapplication)

3. [Adafruit IO Upgrade](#AdafruitIO)

4. [Others](#Others)

5. [IOT Platform](#IOT)

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
2. [TCP communication client][link-tcp client] - Echo TCP client example with auto reconnection.
3. [TCP with DHT11 Sensor and light controls][link-DHT11 led] - TCP communication to monitor records from Adding DHT11 and controls a Red LED light blub
4. [TCP with Soil moisture and relay][link-soil_relay] - Soil Moisture sensor calculates the moist of the soil and controls the amount of water into the plant
5. [TCP Pixel light control][link-TCP light control] - Contain a light sensor, using command to control on/off and color change (Based on WIZnet's [Neopixel-compatiable][link-wiznet piexl] example)
6. [TCP with File][link-TCP file] - Used file feature in Raspberry PI PICO, it includes DHT11 for readings and SNTP for collecting real time information from SNTP server (Based on WIZnet's [SNTP][link-SNTP] example)

<a name="AdafruitIO"></a>

# 🗺️ Adafruit IO Upgrade
WIZnet's Adafruiit IO samples codes with related application (Ref: [WIZnet's Ethernet HAT Adafruit IO][link-adafruit_io_wiznet] & [WIZnet's Adafruit IO][link-adafruit_io_wiznet_example] example)

1. [Adafruit IO Part 1][link-adafruitio1] - Contain DHT 11, Relay control and Soil Moisture sensor data
2. [Adafruit IO Part 2][link-adafruitio2] - Contain Light Sensor module to determine brightness and a Pixel Led light 

<a name="Others"></a>
# 📓 Others
1. [Soil moisture sensor module][link-soil moisture] - Codings for Soil moisture sensor's range setting and collect moisture

<a name="IOT"></a>
# 📈 IOT Platform
1. [BigIOT.net][link-bigiot] (Chinese IOT platform) - This platform used Simple TCP connection with Json format command to communicate with IOT platform
2. [Onenet IOT][link-onenet] (One of the largest IOT platform) - Used MQTT protocol to connect to the platform (login information required to encrypted)

# 📚 Reference
Adafruit Neopixel link: https://github.com/adafruit/Adafruit_NeoPixel

[link-getting_started]: https://github.com/Wiznet/RP2040-HAT-CircuitPython/blob/master/Ethernet%20Example%20Getting%20Started%20%5BCircuitpython%5D.md
[link-all examples]:https://github.com/Wiznet/RP2040-HAT-CircuitPython/tree/master/examples
[link-tcp communication]:https://github.com/ronpang/WIZnet-HK_Ron/blob/main/TCP/TCP%20server.py
[link-DHT11 led]:https://github.com/ronpang/WIZnet-HK_Ron/blob/main/TCP/TCP%20server%20(DHT11%2C%20led).py
[link-soil moisture]:https://github.com/ronpang/WIZnet-HK_Ron/blob/main/Soil%20Sensor/Soil%20sensor%20settings.py
[link-soil_relay]: https://github.com/ronpang/WIZnet-HK_Ron/blob/main/TCP/TCP%20server%20(soil%20sensor%20+%20relay).py
[link-TCP file]:https://github.com/ronpang/WIZnet-HK_Ron/blob/main/TCP/TCP%20server%20(DHT11%2C%20led)%20%2B%20file.py
[link-SNTP]:https://github.com/ronpang/RP2040-HAT-CircuitPython/tree/master/examples/SNTP
[link-adafruitio1]: https://github.com/ronpang/WIZnet-HK_Ron/blob/main/Adafruit%20io/Adafruit%20io%20(DHT11%2C%20led%2C%20soil%20sensor%2C%20relay)%20%2B%20previous%20setting.py
[link-tcp echo]:https://github.com/Wiznet/RP2040-HAT-CircuitPython/blob/master/examples/Network/W5x00_Echo_Demo_TCP.py
[link-adafruit_io_wiznet_example]:https://github.com/Wiznet/RP2040-HAT-CircuitPython/tree/master/examples/Adafruit_IO
[link-adafruit_io_wiznet]:https://github.com/Wiznet/RP2040-HAT-CircuitPython/blob/master/examples/Adafruit_IO/Getting%20Start%20Adafruit%20IO.md
[link-TCP light control]: https://github.com/ronpang/WIZnet-HK_Ron/blob/main/TCP/TCP%20server%20(Neopixel%20light%20control).py
[link-wiznet piexl]: https://github.com/Wiznet/RP2040-HAT-CircuitPython/blob/master/examples/Neopixel/W5x00_Neopixel.py
[link-adafruitio2]: https://github.com/ronpang/WIZnet-HK_Ron/blob/main/Adafruit%20io/Adafruit%20io%20(Neopixel%20light%20control).py
[link-tcp client]: https://github.com/ronpang/WIZnet-HK_Ron/blob/main/TCP/TCP%20client.py
[link-bigiot]: https://github.com/ronpang/WIZnet-HK_Ron/blob/main/IOT%20platform/Bigiot_tcp%20client.py
[link-onenet]: https://github.com/ronpang/WIZnet-HK_Ron/tree/main/IOT%20platform/onenet
