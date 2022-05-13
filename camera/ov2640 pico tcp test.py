# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2021 Jeff Epler for Adafruit Industries
# SPDX-FileCopyrightText: 2010 WIZnet
# SPDX-License-Identifier: Unlicense

"""Capture an image from the camera and display it as ASCII art.

This demo is has been modified to run on the PICO by using circuit python.

It's important that you use a terminal program that can interpret
"ANSI" escape sequences.  The demo uses them to "paint" each frame
on top of the prevous one, rather than scrolling.

Remember to take the lens cap off, or un-comment the line setting
the test pattern!

Thank you for adafruit share this source code to allow me to modified it with WIZnet's W5100S-EVB-PICO / Raspberry Pi PICO with WIZnet Ethernet HAT

For more information please refer to the following links:

WIZnet: https://github.com/Wiznet/RP2040-HAT-CircuitPython
Adafruit IO OV2640 : https://github.com/adafruit/Adafruit_CircuitPython_OV2640
WIZnet CPY functions: https://github.com/ronpang/WIZnet-HK_Ron/tree/main/Cpy%20simplified
"""

import sys
import time
import binascii
import busio
import board

from wiznet_simplify import * #used wiznet_simplify

import adafruit_ov2640
import digitalio
import gc #Clearing the unwanted data to ensure the PICO has enough RAM to run this code

TCP_server = network() # Init the wiznet simplify (WIZnet CPY function)
TCP_server.connection() # Create a socket and prepare to connect with a client

#reset the OV2640 before creating the class for OV2640
with digitalio.DigitalInOut(board.GP10) as reset: 
    reset.switch_to_output(False)
    time.sleep(0.1)
    bus = busio.I2C(board.GP15, board.GP14) #set Pin 14 and 15 to be the I2C bus

#INIT OV2640 - please refer to the table showed on readme to know the connection method between PICO and OV2640
cam = adafruit_ov2640.OV2640(
    bus,
    data_pins=[
        board.GP0,
        board.GP1,
        board.GP2,
        board.GP3,
        board.GP4,
        board.GP5,
        board.GP6,
        board.GP7,
    ],
    clock=board.GP12,  # PCLK
    vsync=board.GP11,  # VSYNC
    href=board.GP9,  # HERF
    mclk=None, #the ov2640 has a internal MCLK
    shutdown=None,
    reset = board.GP10,

    
)

cam.size = adafruit_ov2640.OV2640_SIZE_QVGA #OVGA side
cam.colorspace = adafruit_ov2640.OV2640_COLOR_JPEG #jpg format
cam.flip_y = True
cam.flip_x = True 
cam.test_pattern = False
buf = bytearray(cam.width * cam.height // 5) #set the size
while True:
    TCP_server.check_mode()
    
    length = cam.capture(buf) #capture the image
    b_len = len(length)
    if b_len < 25000:
        a_value = bytes(length[0:b_len]) #collect the wanted data (bytes)
    else:
        print("captured image is too big") # The image is too large, mostly is related to bad connection.
        a_value = None                     # Wait for the next loop to collect the image
        
    del buf #delete the variable to save more space for encoding the image
    del length
    gc.collect()
    if a_value != None:
        encoded_data = binascii.b2a_base64(a_value).strip() #encode to base64
        if len(encoded_data) > 2048: 
            chunks, chunk_size = len(encoded_data), 2048 #seperate the codes into chunks that fits for transmitting data to PC
            splited = [ encoded_data[i:i+chunk_size] for i in range(0, chunks, chunk_size) ]
            en_len = "len="+ str(len(encoded_data)) #measure the total length of the base64 msg
            TCP_server.communication(send_data = en_len.encode()) #convert the length into bytes for transmission 
            for i in range(len(splited)):
                TCP_server.communication(send_data = splited[i]) #sent the base64 msg
        else: #if the size is smaller than 2048, it will sent once
            en_len = "len="+ str(len(encoded_data))
            TCP_server.communication(send_data = en_len.encode())
            time.sleep(0.1)
            TCP_server.communication(send_data = encoded_data)
    else:
        encoded_data = None #prevent error data has created
    
    #deleted all the remaining variables to create more RAM
    del a_value
    del encoded_data
    del splited
    gc.collect()

    #recreate the buf for the next image
    buf = bytearray(cam.width * cam.height // 5)

    gc.collect()

    time.sleep(0.5)
