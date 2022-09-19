#!/usr/bin/env python
"""
This talks to the quadcopter controller board
"""
import serial
import struct
from collections import namedtuple

IDENT = namedtuple("IDENT", "version multitype msp_version capability")
IMU_RAW = namedtuple("IMU_RAW", "ax ay az gx gy gz mx my mz")
ATTITUDE = namedtuple("ATTITUDE", "roll pitch heading")
ALTITUDE = namedtuple("ALTITUDE", "alt vario")

class MSP:
    """
    https://web.archive.org/web/20190715222846/http://www.stefanocottafavi.com/msp-the-multiwii-serial-protocol/
    """

    # 1xx identify requests
    MSP_IDENT = 100
    MSP_STATUS = 101
    MSP_RAW_IMU = 102
    MSP_ATTITUDE = 108
    MSP_ALTITUDE = 109

    # 2xx identify commands
    MSP_SET_RAW_RC = 200
    MSP_SET_MOTOR = 214

    def request(self, cmd):
        # msg = bytes(6)
        msg = struct.pack("<cccBBB",b"$",b"M",b"<",0,cmd,cmd)
        # c = self.checksum(msg[3:])
        # print(f">> c: {c}")
        # msg[5] = struct.pack("<B", c)
        return msg

    def response(self, msg):
        i = msg.find(b"$M>")+3
        len = int(msg[i])
        kind = int(msg[i+1])
        payload = msg[i+2:i+2+len]
        csum = msg[i+2+len]

        calcsum = self.checksum(msg[i:i+2+len])
        if csum != calcsum:
            print(f"{csum} != {calcsum}")
            return None
        # print(f"{csum} == {self.checksum(msg[i:i+2+len])}")
        # print(kind, csum, payload)
        ret = None
        if kind == self.MSP_IDENT:
            data = struct.unpack("<BBBI", payload)
            ret = IDENT(*data)
        elif kind == self.MSP_RAW_IMU:
            data = struct.unpack("<hhhhhhhhh", payload)
            ret = IMU_RAW(*data)
        elif kind == self.MSP_ATTITUDE:
            r,p,h = struct.unpack("<hhh", payload)
            ret = ATTITUDE(r/10.0, p/10.0, h)
        elif kind == self.MSP_ALTITUDE:
            data = struct.unpack("<ih", payload)
            ret = ALTITUDE(*data)

        return ret

    def checksum(self, msg):
        cs = 0
        for m in msg:
            cs ^= m
        return cs



# port = "/dev/tty.usbserial-013950B1"
# s = serial.Serial()
# s.baudrate = 115200
# s.timeout = 0.1
# s.port = port
# s.open()

msp = MSP()
msg = msp.request(MSP.MSP_IDENT)
print(type(msg), msg)
# s.write(msg)
# resp = s.read(128)
# print(resp)
# rmsg = msp.response(resp)
# print(rmsg)
