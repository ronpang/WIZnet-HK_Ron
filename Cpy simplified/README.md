# Simplified WIZnet coding 
Due to the codes for creating a simple TCP connection required a lot of codings, I had simplified some codes into understandable codes to share.

The codes does is in .py file rather than .mpy file. You could change the codes as you want. 

# Required libraries:
```python
import board
import digitalio
import time
import busio
from adafruit_wiznet5k.adafruit_wiznet5k import * #active WIZnet chip library
import adafruit_wiznet5k.adafruit_wiznet5k_socket as socket #open socket from WIZnet library
```

## Features
1. Class - network: Creating a class function to activate the chip and work as a network module.
      - _ _ init _ _ Variables:
          - DHCP: Activate DHCP or Deactivate DHCP mode - True / False (Default: True = Activate)
          - MY_MAC: The device's MAC address - Tuple format (Default: 0x00,0x01,0x02,0x03)
          - IP_ADDRESS: IP address of your device - Tuple format (Default: 192, 168, 0, 111)
          - SUBNET_MASK: Subnet Mask of your device - Tuple format (Default: 255, 255, 0, 0)
          - GATEWAY_ADDRESS: Gateway address of your device - Tuple format (Default: 192, 168, 0, 1)
          - DNS_SERVER: DNS server address ofr your devoce - Tuple format (Default: 8, 8, 8, 8)
      - Function: Create a workable network module that has it's IP address
2. Network - SPI setup: Setup the SPI interface by using Busio
    - Variables: None
    - Function: Setup SPI interface, soft reset WIZnet chip for working normally (WIZnet chips required)
3. Network - connection: Create a socket for specific feature for connecting other device
    - Current function: TCP Server or TCP client mode ONLY
    - Variables:
        - Server_type: Choose the TCP type - True / False (TCP server or TCP client) (Default: True = TCP server mode)
        - r_ip: Remote device IP address - String (only required on TCP client mode) (Default: None, Example: "192.168.0.11")
        - r_port: Port number for connection. 
            1. Server mode: Port number for listening TCP clients 
            2. Clinet mode: Port number to connect with a TCP server
   - Function: Create a netwokr socket for TCP connection 
4. Network - check mode: Checking the selected communication mode and create a network connection
    - Variable: None
    - Function: Using the created socket to connect the opposite device
5. Network - communication: Start to communication and handle each kind of situation that will happen in TCP commnuication.
    - Vairable:
        - send_data: Send data variables - String (If there isn't any data input, it will loopback the received message) (Default: None)
     - Function: 
        - Read data: Received data from the device through WIZnet's RX buffer
        - Send data: Send data to the device through WIZnet's TX buffer
        - Disconnected:
            1. TCP server - back to listening mode to listen for new connection
            2. TCP client - Try to reconnect to the server. If it has passes the time limited, it will show error msg
        
