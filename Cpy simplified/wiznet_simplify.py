# SPDX-FileCopyrightText: 2010 WIZnet
#
# SPDX-License-Identifier: MIT
"""
`wiznet.simplify.py`
================================================================================
Pure-Python interface based on WIZnet's library codes in circuitpython coding.
* Author(s): Ron Pang
Implementation Notes
--------------------
**Software and Dependencies:**
* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases
* Adafruit's Bus Device library: https://github.com/adafruit/Adafruit_CircuitPython_BusDevice
* WIZnet library: https://github.com/Wiznet/RP2040-HAT-CircuitPython
"""
import board
import digitalio
import time
import busio
from adafruit_wiznet5k.adafruit_wiznet5k import * #active WIZnet chip library
import adafruit_wiznet5k.adafruit_wiznet5k_socket as socket #open socket from WIZnet library

class network:
     """Interface for wiznet_simplified module.
    :param bool DHCP: Turn on / off the DHCP mode (IP assignment from Router) 
    :param Tuple MY_MAC: The WIZnet's MAC address (Default: 0x00,0x01,0x02,0x03)
    :param Tuple IP_ADDRESS: The WIZnet's IP address (Default: 192, 168, 0, 111)
    :param Tuple SUBNET_MASK: The WIZnet's Subnet Mask address (Default: 255, 255, 0, 0)
    :param Tuple GATEWAY_ADDRESS: The WIZnet's Gateway address  (Default: 192, 168, 0, 1)
    :param Tuple DNS_SERVER: The Wiznet's DNS address (Default: 8, 8, 8, 8)
    """
    mo = None #TCP mode selection
   
    def __init__(self,
        DHCP = True,
        MY_MAC = (0x00, 0x01, 0x02, 0x03, 0x04, 0x05),
        IP_ADDRESS = (192, 168, 0, 111),
        SUBNET_MASK = (255, 255, 0, 0),
        GATEWAY_ADDRESS = (192, 168, 0, 1),
        DNS_SERVER = (8, 8, 8, 8)
        ):
        self.mac = MY_MAC
        self.ip = IP_ADDRESS
        self.sub = SUBNET_MASK
        self.gate = GATEWAY_ADDRESS
        self.dns = DNS_SERVER
        
        self.SPI_setup()
        self.eth = WIZNET5K(self.spi_bus, self.cs, is_dhcp = DHCP, mac=self.mac, debug=False)
        if DHCP == False:
            self.eth.ifconfig = self.ip, self.sub, self.gate, self.dns
        print("Chip Version:", self.eth.chip)
        print("MAC Address:", [hex(i) for i in self.eth.mac_address])
        print("My IP address is:", self.eth.pretty_ip(self.eth.ip_address))
        
        
    def SPI_setup(self):
    """GPIO pins setup and create a SPI communication with WIZnet's chip"""
    # Activate GPIO pins for SPI communication
        SPI0_SCK = board.GP18
        SPI0_TX = board.GP19
        SPI0_RX = board.GP16
        SPI0_CSn = board.GP17

    # Activate Reset pin for communication with W5500 chip
        W5x00_RSTn = board.GP20
    
    # Set reset function
        ethernetRst = digitalio.DigitalInOut(W5x00_RSTn)
        ethernetRst.direction = digitalio.Direction.OUTPUT

    # Set this SPI for selecting the correct chip
        self.cs = digitalio.DigitalInOut(SPI0_CSn)

    # Set the GPIO pins for SPI communication
        self.spi_bus = busio.SPI(SPI0_SCK, MOSI=SPI0_TX, MISO=SPI0_RX)

    # Reset WIZnet's chip first
        ethernetRst.value = False
        time.sleep(1)
        ethernetRst.value = True
    
    def connection(self,
        Server_type = True,
        r_ip = None,
        r_port = 5000
        ):
        """Create a socket for TCP connection
        :param bool Server_type: Select TCP mode ( On = Server / Off = Client) (Default: True)
        :param str r_ip: Set Remote device IP address (Default: None)
        :param int r_port: Set Remote device Port number (Default: 5000)
        """
        socket.set_interface(self.eth)
        self.communicate = socket.socket()  # Set and name the socket to be a TCP server
        self.remote_ip = r_ip  
        self.remote_port = r_port
        if self.remote_port is None:
            assert self.communicate == None, "Port number is required for TCP connnection"
        if Server_type == True:
            self.communicate.bind((self.remote_ip, self.remote_port))  # Binding the IP address and Port number 
            self.communicate.listen()
        else:
            if self.remote_ip is None:
                assert self.communicate == None, "IP address is required for TCP client"
            else:
                self.communicate.connect((self.remote_ip, self.remote_port), None)


    def check_mode(self):
        """Check the TCP mode and connect with the remote device"""
        self.eth.maintain_dhcp_lease()
        if self.mo is None:
            if self.communicate.status == SNSR_SOCK_LISTEN: #TCP server status: WIZnet's chip is listening for a client device's request
                self.mo, addr = self.communicate.accept()
            else:
                if self.communicate.status == SNSR_SOCK_CLOSED: #when the server has disconnect, it will try to reconnect the server
                    self.communicate.connect((self.remote_ip, self.remote_port), None)
                    self.mo = self.communicate
                else:
                    self.mo = self.communicate
           
    def communication(self, send_data = None):
        """Communicate with the device and handle differnet kind of communcation status
        :param str send_data: The data required to send out through TCP communication (None = loopback mode, contain data = send out data) (Default: None)
        """
        if self.mo.status == SNSR_SOCK_SYNRECV: #WIZnet received a request from the remote device, give time for established the connection
            time.sleep(0.5)
        if self.mo.status == SNSR_SOCK_ESTABLISHED: #WIZnet has established with the remote deivce, it could start communcate
            if send_data == None:
                data = self.mo.recv() # Data size that you could receive
                self.mo.send(data)  # Echo message back to client
                r_data = None
            
            else:
                r_data = self.mo.recv() # Data size that you could receive
                data = send_data.encode()
                self.mo.send(data)  # Echo message back to client
        
        elif self.mo.status == SNSR_SOCK_CLOSE_WAIT: #WIZnet received command to close the socket, confirm to close the connection and socket
            self.mo.disconnect() #close the connection
            self.mo.close() #close the socket
            r_data = None
        
        elif self.mo.status == SNSR_SOCK_FIN_WAIT: #WIZnet has been disconnected from the remote device, close the socket
            communicate.close()
            r_data = None
    
        elif self.mo.status == SNSR_SOCK_CLOSED: #WIZnet has closed a socket, user could recreate a new socket through check_mode
            r_data = None
            self.mo = None
        
        return r_data

