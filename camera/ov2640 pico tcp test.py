# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2021 Jeff Epler for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense

"""Capture an image from the camera and display it as ASCII art.

This demo is designed to run on the Kaluga, but you can adapt it
to other boards by changing the constructors for `bus` and `cam`
appropriately.

The camera is placed in YUV mode, so the top 8 bits of each color
value can be treated as "greyscale".

It's important that you use a terminal program that can interpret
"ANSI" escape sequences.  The demo uses them to "paint" each frame
on top of the prevous one, rather than scrolling.

Remember to take the lens cap off, or un-comment the line setting
the test pattern!
"""

import sys
import time
import binascii
import busio
import board

from wiznet_simplify import *

import adafruit_ov2640
import digitalio
import gc
import os

TCP_server = network()
TCP_server.connection()

with digitalio.DigitalInOut(board.GP10) as reset:
    reset.switch_to_output(False)
    time.sleep(0.1)
    bus = busio.I2C(board.GP15, board.GP14)

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
    mclk=None,
    shutdown=None,
    reset = board.GP10,

    
)

cam.size = adafruit_ov2640.OV2640_SIZE_QVGA
cam.colorspace = adafruit_ov2640.OV2640_COLOR_JPEG
cam.flip_y = True
cam.flip_x = True
cam.test_pattern = False
buf = bytearray(cam.width * cam.height // 5)
while True:
    TCP_server.check_mode()
    
    length = cam.capture(buf)
    b_len = len(length)
    if b_len < 25000:
        a_value = bytes(length[0:b_len])
    else:
        print("captured image is too big")
        a_value = None
    print("Transferred data and delete current variables")
    del buf
    del length
    gc.collect()
    if a_value != None:
        encoded_data = binascii.b2a_base64(a_value).strip()
        if len(encoded_data) > 2048:
            chunks, chunk_size = len(encoded_data), 2048
            splited = [ encoded_data[i:i+chunk_size] for i in range(0, chunks, chunk_size) ]
            en_len = "len="+ str(len(encoded_data))
            TCP_server.communication(send_data = en_len.encode())
            for i in range(len(splited)):
                TCP_server.communication(send_data = splited[i])
        else:
            en_len = "len="+ str(len(encoded_data))
            TCP_server.communication(send_data = en_len.encode())
            time.sleep(0.1)
            TCP_server.communication(send_data = encoded_data)
    else:
        encoded_data = None
    
    print("Deleted buffer")
    del a_value
    del encoded_data
    del splited
    gc.collect()

    print("Remaked buffer")
    buf = bytearray(cam.width * cam.height // 5)
    print("Recreated buffer")
    gc.collect()

    time.sleep(0.5)
