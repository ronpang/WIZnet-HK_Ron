## BigIOT net (Basic)
This IOT platform is one of the Chinese IOT platform. It used the TCP communication to transmit command directly to the IOT platform.
- Code: [Bigiot reference code][link-bigiot_code]
1. How to create a account?
   - Go to [bigiot.net][link-bigiot] and select register on the top right corner
   ![][link-register]
   - Proivde the information for creating your account
   - Email confirmation
3. How to create a device?
   - Login to your account
   - Go to Device -> list -> add new device (please refer the image below)
   ![][link-device1]
   
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
    ```python
        - Device Login: {"M":"checkin","ID":"AAAAAA","K":"XXXXXX"}\n
        - Send Data: {"M":"update","ID":"AAAAAA","V":{"BBBBBB":"CCCCCC"}}\n
        - Device Logout: {"M":"checkout","ID":"AAAAAA","K":"XXXXXX"}\n
        #AAAAAA = ID of the device
        #BBBBBB = ID of the interface
        #XXXXXX = Apikey
        #CCCCCC = value for first interface
    ```
    Information:
    ![][link-device]
    ![][link-interface]
7. Result: 
   Testing method: add 1 to Bigiot.net
   ![][link-result]
   
   
[link-bigiot]: https://www.bigiot.net/
[link-device1]: https://github.com/ronpang/WIZnet-HK_Ron/blob/main/IOT%20platform/img/bigiot%20device%201.PNG
[link-device2]: https://github.com/ronpang/WIZnet-HK_Ron/blob/main/IOT%20platform/img/bigiot%20Device%202.PNG
[link-device3]: https://github.com/ronpang/WIZnet-HK_Ron/blob/main/IOT%20platform/img/bigiot%20Device%203.PNG
[link-interface1]: https://github.com/ronpang/WIZnet-HK_Ron/blob/main/IOT%20platform/img/bigiot%20interface%201.PNG
[link-interface2]: https://github.com/ronpang/WIZnet-HK_Ron/blob/main/IOT%20platform/img/bigiot%20interface%202.PNG
[link-communication]: https://github.com/ronpang/WIZnet-HK_Ron/blob/main/IOT%20platform/img/Bigiot%20Communication%20diagram.PNG
[link-register]: https://github.com/ronpang/WIZnet-HK_Ron/blob/main/IOT%20platform/img/big%20iot%20register.PNG
[link-result]: https://github.com/ronpang/WIZnet-HK_Ron/blob/main/IOT%20platform/img/bigiot%20testing%20result.PNG
[link-interface]: https://github.com/ronpang/WIZnet-HK_Ron/blob/main/IOT%20platform/img/bigiot%20interface%20information%202.PNG
[link-device]: https://github.com/ronpang/WIZnet-HK_Ron/blob/main/IOT%20platform/img/bigiot%20device%20information.PNG
[link-bigiot_code]: https://github.com/ronpang/WIZnet-HK_Ron/blob/main/IOT%20platform/Bigiot_tcp%20client.py
