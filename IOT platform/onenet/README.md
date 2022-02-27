# Onenet (MQTT method)
There are few steps need to do before using the provided source code:
1. Creating a account through onenet website
2. Go to onenet studio to create a product (Product ID is required for the communication)
3. Create a device from the product (Device ID & Device key is required)
4. Create properties for receving the data

Network Protocol Required:
1. NTP - Collecting the actual time from the server ([WIZnet reference][link-ntp])
2. MQTT - minimqtt is based on MQTT 3.12 that is suitable on using onenet's MQTT format([WIZnet reference][link-mqtt])

Used Adafruit circuit library:
1. adafruit_minimqtt - Activate MQTT protocol
2. adafruit_bus_device - SPI interface for communicating with WIZnet's chip
3. adafruit_WIZnet5k - Using WIZnet solution, it is required to use this library
4. adafruit_requests - used on WIZnet solution and MQTT protocol
5. adafruit_hashlib - Hashing the codes for the login password [hashlib][link-hashlib]
6. circuitpython_hmac (create by:Jim Bennett) - Finiaize the login password by using HMAC encryption ([HMAC github][link-hmac])

Communication method on Onenet:
1. login to onenet
    1. Where to find the important login information
    2. create a correct login password
2. using property names to send data to the platform and receive confirmation message from the platform
3. using property names to receive data from the platform and send feedback to the server for confirmation

# Login to onenet
For login to Onenet, it is required the following information.

**Login site**: studio-mqtt.heclouds.com / IP address: 218.201.45.7

**Port number**: 1883

**Username**: Product ID

**Password**: Login password

**Client ID**: device name

## Where to find the important login information
1. Go to onenet website and login ([onenet webiste][link-onenetwebsite])
2. Go to Service products and choose "OneNET Studio"



## How to generate a correct login password
For the login password of onenet, it combines with different information with a specific key provided by the site. 

By usimg the HMAC encrytion method, it will generate the correct password for login into the server.

### Required information
Original documentation: [Onenet document][link-password]

```python
Product_ID = AAAAAAAA
device_name = BBBBBBBBB
Token = CCCCCCCCC
```

| No. | Name |Variable Type | Parameters Description | Example|
| ------------- | ------------- | ------------- | ------------- | ------------- |
| 1  | Version | string | Fixed data provided by onenet | 2018-10-31 |
| 2  | Resource (res) | string | Resource format: products/**Product ID**/device/**device name**| products/AAAAAAAA/device/BBBBBBBBB|
| 3  | Expiration Time (et) | int | Expiration Time in Epoch Time to seconds. If the access time is over your expiration time, it will reject your access.|1645884887 = 2022/2/26 10:14:47pm (GMT +8)|
| 4  | Method | string | HMAC encrytion method: MD5, Sha1, Sha256 | MD5 |
| 5  | Signature (sign) |  string | The signature made by Token and the above information |DDDDDDDD

### How to make the Signature
The whole process required HMAC with the encrypyion method that you had used above (Sha1, sha256 or MD5)

The message to encryption (in 1 string): et + \n + method + \n + res + \n + version

Key for encryption: Token = CCCCCCCCC

Encryption formula: 
Sign = base64encode(HMAC_your method (base64decode(**Token**), UTF-8_encode(**message**)))

Steps:
1. Encode the message into UTF-8 format
2. base64 decode Token
3. Decoded Token will be used to encrypt the message by HMAC method
4. base64 encode the emcrypted message and it used as Signature

### Combine all the information into a password
**Formula:** version=**version**&res=**Resource**&et=**Expiration Time**&method=**Method**&sign=**Signature**

**Example:**  version=2018-10-31&res=products/AAAAAAAA/device/BBBBBBBBB&et=1645884887&method=md5&sign=DDDDDDDD

***Please know that the '&' symbol are used to seperate each variables and information***

About the Signuature, the symbols required to converted into URL format like the following

1. **+** => %2B
2. **/** => %2F
3. **=** => %3D


[link-ntp]: https://github.com/ronpang/RP2040-HAT-CircuitPython/tree/master/examples/SNTP
[link-mqtt]: https://github.com/ronpang/RP2040-HAT-CircuitPython/tree/master/examples/MQTT
[link-hashlib]: https://github.com/adafruit/Adafruit_CircuitPython_hashlib
[link-hmac]: https://github.com/jimbobbennett/CircuitPython_HMAC
[link-onenetwebsite]: https://open.iot.10086.cn/
[link-password]: https://open.iot.10086.cn/doc/v5/develop/detail/624
