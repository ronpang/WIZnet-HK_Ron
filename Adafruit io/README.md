# Adafruit IO application 
Adafruit IO provides a lot of opportunity for devleoping a smart interface with open source hardware boards.

By having WIZnet Ethernet HAT, we could directly to create or modify your codes to work in Adafruit IO. ([Adafruit IO Introduction][link-adafruit_io_wiznet] , [Adafruit IO example][link-adafruit_io_wiznet_example])

## Part 1: Adding simple sensors
It is based on [Adafruit IO example][link-adafruit_io_wiznet_example] & [TCP server Sensor example][link- TCP server sensor/control]

Added:
1. DHT11 - Temperature and humidity sensor
2. LED - Red color LED light contol (on/off only)
3. Soil Humidity Sensor - Convert ADC to percentage value (%)

IO features:
1. Gauge for Temperature, Humiditiy and Soil Humidity Sensor
2. LED light on/off control

## Part 2: NeoPixel light control
It is based on [Adafruit IO example][link-adafruit_io_wiznet_example] & [TCP NeoPixel light example][link- TCP Neopixel]

Added:
1. NeoPixel light control 
      1. LED ON/OFF control
      2. Convert RGB signal in Hex formart to change the color of the Pixel LED (Example: #FF0000 = RED)
3. Light sensor (Diode Type Photosensitive Sensor)
      1. Sensor on/off Switch (ON = Light Sensor ON, OFF = Manual Control from Adafruit IO Dashboard)
      2. Convert ADC to percentage value for changing the brightness of the Pixel LED

[link-adafruit_io_wiznet_example]:https://github.com/Wiznet/RP2040-HAT-CircuitPython/tree/master/examples/Adafruit_IO
[link-adafruit_io_wiznet]:https://github.com/Wiznet/RP2040-HAT-CircuitPython/blob/master/examples/Adafruit_IO/Getting%20Start%20Adafruit%20IO.md
[link- TCP server sensor/control]: https://github.com/ronpang/WIZnet-HK_Ron/blob/main/TCP/TCP%20server%20(DHT11%2C%20led%2C%20soil%20sensor).py
[link- TCP Neopixel]: https://github.com/ronpang/WIZnet-HK_Ron/blob/main/TCP/TCP%20server%20(Neopixel%20light%20control).py
