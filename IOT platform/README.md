# IOT platform
All IOT platforms are required to use different kind of network application protocol to ensure the data could be safe to delivery.

Normally, it would use the following methods to create 
1. MQTT protocol 
2. HTML protocol 

This section provides template reference source code for each platforms

# Directory
1. [Bigiot.net](#Bigiot)

<a name="Bigiot"></a>
## BigIOT net (Simple)
This IOT platform is one of the Chinese IOT platform. It used the TCP communication to transmit command directly to the IOT platform.

1. How to create a account?
   - Go to [bigiot.net][link-bigiot] and select register on the top right corner
   ![][link-register]
   - Proivde the information for creating your account
   - Email confirmation
3. How to create a device?
   - Login to your account
   - Go to Device -> list -> add new device (please refer the image below)
   ![][link-device]
   
   ![][link-device2]
   - input the device name -> press confirm (please refer the image bwlow)
   ![][link-device3]
4. How to create a interface?
   - Go to interface -> add
   ![][link-interface1]
   - Input the interface name -> choose the related device -> select the related input 
   - Select the unit output (optional)
   ![][link-interface2]
5. How to communicate?
   - DNS IP address: www.bigiot.net (you could directly input into 
   - Port Number: 8181 . 8282 (include heartbeat package - 40S) , 8383 (SSL, heartbeat package - 30S)
   - If there isn't any data transmittion, it will auto disconnected for Port 8181
   - Communication diagram
   ![][link-communication]
6. How to send commands?
   - Command format:
        - Device Login: {"M":"checkin","ID":"xx1","K":"xx2"}\n
        - Send data: {"M":"update","ID":"xx1","V":{"id1":"value1",...}}\n
        - Device Logout: {"M":"checkout","ID":"xx1","K":"xx2"}\n
7. Result: 
   Testing method: add 1 to Bigiot.net
   ![][link-result]
   
   
[link-bigiot]: https://www.bigiot.net/
[link-device]: https://github.com/ronpang/WIZnet-HK_Ron/blob/main/IOT%20platform/img/bigiot%20device%201.PNG
[link-device2]: https://github.com/ronpang/WIZnet-HK_Ron/blob/main/IOT%20platform/img/bigiot%20Device%202.PNG
[link-device3]: https://github.com/ronpang/WIZnet-HK_Ron/blob/main/IOT%20platform/img/bigiot%20Device%203.PNG
[link-interface1]: https://github.com/ronpang/WIZnet-HK_Ron/blob/main/IOT%20platform/img/bigiot%20interface%201.PNG
[link-interface2]: https://github.com/ronpang/WIZnet-HK_Ron/blob/main/IOT%20platform/img/bigiot%20interface%202.PNG
[link-communication]: https://github.com/ronpang/WIZnet-HK_Ron/blob/main/IOT%20platform/img/Bigiot%20Communication%20diagram.PNG
[link-register]: https://github.com/ronpang/WIZnet-HK_Ron/blob/main/IOT%20platform/img/big%20iot%20register.PNG
[link-result]: https://github.com/ronpang/WIZnet-HK_Ron/blob/main/IOT%20platform/img/bigiot%20testing%20result.PNG
