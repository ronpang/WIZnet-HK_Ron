# OV2640 camera TCP communication
It used Python coding and circuitpython coding to create connection between a PC with Raspberry PI PICO / W5100S-EVB PICO.

The coding includes a display to show the capturing result from the OV2640.

Coding that I used from other sources:
1. [Adafruit OV2640][link-ov2640]
2. [Raspberry Pi Pico - OV2640][link-pico_ov2640]

# Hardware Connection diagram
The PICO board required to use GPIO16 - GPIO21. Thus, the connection for the OV2640 will be used most of the pin from GPIO 0 - GPIO 15.

### GPIO 14 and GPIO 15 required to add 10K Ohm resistor for pull ups to activate I2C connection

For more information, please refer to the image below.

![][link-hardware]

# Connection Diagram
The communication method is using TCP communication and it used wiznet_simplifed.py to simplify codings for handling this communication.

1. PC = TCP client - Handles the received data, combines and display as a image through python
2. PICO = TCP server - Recevied data from OV2640, chuck it off in to 2048 byte and send it to the PC. (Length is provided from the first msg of data)

For more information, please refer to the image below.

![][link-connection]

# Codings
Please refer to the links below for your codings. It includes related description for explaining my coding method.

[PC][link-PC_code] - Combines the data received from PICO, save it as a image and display by using opencv library

[PICO][link-PICO] - Collect data from OV2640, chuck it into related size (2048 byte) and send it to the PC. (Length is provided with a seperate msg)

# Results
The coding is simple. PC codings will save it as a jpeg file, it used opencv's imshow to display the image.

### Display from Python:
![][link-display result]

### Jpeg Image:
![][link-jpeg]


[link-hardware]: https://github.com/ronpang/WIZnet-HK_Ron/blob/main/camera/OV2640%20connection%20diagram.PNG
[link-connection]: https://github.com/ronpang/WIZnet-HK_Ron/blob/main/camera/camera%20network%20connection.PNG
[link-PC_code]: https://github.com/ronpang/WIZnet-HK_Ron/blob/main/camera/camera%20display%20on%20PC.py
[link-PICO]: https://github.com/ronpang/WIZnet-HK_Ron/blob/main/camera/ov2640%20pico%20tcp%20test.py
[link-display result]: https://github.com/ronpang/WIZnet-HK_Ron/blob/main/camera/camera%20display%20result.PNG
[link-jpeg]: https://github.com/ronpang/WIZnet-HK_Ron/blob/main/camera/Testing.jpg
[link-ov2640]: https://github.com/adafruit/Adafruit_CircuitPython_OV2640
[link-pico_ov2640]: https://learn.adafruit.com/capturing-camera-images-with-circuitpython/raspberry-pi-pico-wiring
