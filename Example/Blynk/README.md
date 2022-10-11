# WizFi360-EVB-PICO (Blynk)
This is a exmaple ussd W5100S-EVB-PICO in Circuitpython to communicate with Blynk

This example based on the python coding made from Blynk. (For the communication part, it shifted to the main code.)

For more information about Blynk's coding, please go to this [LINK][link-blynk].

## Getting start for Blynk
Blynk provided a good instruction on how to create a account and quickstart setup, please follow [Blynk getting started][link-get start].

## 🤖 Basic Setup
### Step 1: How to install circuit Python into WizFi360-EVB-PICO (same method as adding to Raspberry Pi Pico)
🟥Youtube: [Linux install method][link-linux install]

🟥Youtube: [Window install method][link-window install]


### Step 2: Add the libraries to your lib section
It is required to add libraries to the folder lib to allow the codes could run.

It must included wiznet5k libraries. (For more info, please refer to [WIZnet circuitpyhton code][link-cpy])

![link-lib_image]

### Step 3: Put the example codes to flash
Draging the examples codes to the flash inside the pico board, it should run the software easily.


```

## 🔰Blynk conncection setup
1. Required files: [TCP Blynk.py][link-aio], [Blynk_lib.py][link-blynk_lib] (Modified - No communication section)
2. Required commands:
For Blynk Setups, it is required to have the following information. (All the information will be showed on the "device info" section)
```python
BLYNK_TEMPLATE_ID =  "TEMPLATE_ID" 
BLYNK_DEVICE_NAME = "DEVICE_NAME"
BLYNK_AUTH_TOKEN = "AUTH_TOKEN"
```
For communicating with blynk Based on Blynk's example codings. ([Write Virtual pin][link-write] , [Read Virtual pin][link-read])
```python
esp.socket_connect("TCP",Dest_IP,Dest_PORT) #TCP connection. If SSL, please change "TCP" to "SSL"
blynk = Blynk(BLYNK_AUTH_TOKEN) #Open the class and connect to Blynk
counter = 0 # Counter for posting information to Blynk

# Register virtual pin handler
@blynk.on("V5") #collect data from Blynk (Virtual Pin V5)
def v5_write_handler(value):
    print('Current slider value: {}'.format(value[0])) 

while True:
    blynk.run()
    print("Adding counter: "+ str(counter))
    blynk.virtual_write(4, str(counter)) #post counter data to virtual pin 4
    time.sleep(1)
    counter +=1
```

## ☑️Results
### Blynk

![link-blynk reuslt]


### Thonny
![link-thonny result]


[link-aio]: https://github.com/ronpang/WizFi360-cpy/blob/main/examples/blynk/TCP%20blynk.py
[link-blynk_lib]: https://github.com/ronpang/WizFi360-cpy/blob/main/examples/blynk/BlynkLib%20(modfied).py
[link-linux install]: https://www.youtube.com/watch?v=onBkPkaqDnk&list=PL846hFPMqg3h4HpTVO8cPPHZnJIRA4I2p&index=3
[link-window install]: https://www.youtube.com/watch?v=e_f9p-_JWZw&t=374s
[link-lib_image]: https://github.com/ronpang/WizFi360-cpy/blob/main/img/lib%20image.PNG
[link-thonny_img]: https://github.com/ronpang/WizFi360-cpy/blob/main/img/thonny%20result%20-%20wizfi360%20-%20MQTT.PNG
[link-adadfruit_img]: https://github.com/ronpang/WizFi360-cpy/blob/main/img/adafruit%20io%20recevied%20result%20(updated)-%20wizfi360%20-%20MQTT.PNG
[link-get start]: https://docs.blynk.io/en/getting-started/what-do-i-need-to-blynk
[link-blynk]: https://github.com/blynkkk/lib-python
[link-write]: https://github.com/blynkkk/lib-python/blob/master/examples/01_write_virtual_pin.py
[link-read]: https://github.com/blynkkk/lib-python/blob/master/examples/02_read_virtual_pin.py
[link-cpy]: https://github.com/ronpang/RP2040-HAT-CircuitPython
[link-blynk reuslt]: https://github.com/ronpang/WIZnet-HK_Ron/blob/main/IOT%20platform/img/Blynk%20result%20-%20W5100S.PNG
[link-thonny result]: https://github.com/ronpang/WIZnet-HK_Ron/blob/main/IOT%20platform/img/thonny%20result%20-%20W5100S-%20Blynk.PNG
