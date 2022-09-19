###############################################
# The MIT License (MIT)
# Copyright (c) 2020 Kevin Walchko
# see LICENSE for full details
##############################################
from collections import namedtuple
from struct import Struct
import struct
from collections import namedtuple
from collections import deque
from enum import IntEnum, unique
import time


IDENT = namedtuple("IDENT", "version multitype msp_version capability")
IMU_RAW = namedtuple("IMU_RAW", "ax ay az gx gy gz mx my mz")
ATTITUDE = namedtuple("ATTITUDE", "roll pitch heading")
ALTITUDE = namedtuple("ALTITUDE", "alt vario")

CALIBRATION = namedtuple("CALIBRATION", "bx by bz sx sy sz") # bias, scale
PID = namedtuple("PID", "kp ki kd")

ImuAGMQT      = namedtuple("ImuAGMQT", "ax ay az wx wy wz mx my mz qw qx qy qz temperature ts")
ImuAGMT       = namedtuple("ImuAGMT",  "ax ay az wx wy wz mx my mz temperature ts")
ImuAGT        = namedtuple("ImuAGT",   "ax ay az wx wy wz temperature ts")
ImuAT         = namedtuple("ImuAT",    "ax ay az temperature ts")
MagneticField = namedtuple("MagneticField","mx my mz")
Range         = namedtuple("Range", "range")
# LaserScan     = namedtuple("LaserScan", "ranges intensities")
TemperaturePressure = namedtuple("TemperaturePressure", "temperature pressure")

YivoError = namedtuple("YivoError","error")
YivoOK = namedtuple("YivoOK", "val")


@unique
class Errors(IntEnum):
    INVALID_HEADER   = 1
    INVALID_LENGTH   = 2
    INVALID_CHECKSUM = 4
    INVALID_COMMAND  = 8
    
    
# class Ack(IntEnum):
#     OK = 0
#     ERROR = 127  # 0x7F
    
@unique
class MsgIDs(IntEnum):
    """MSP message ID"""
    # Commands
    # CALIBRATION_DATA     = 14  # bias, scale
    # SET_CALIBRATION_DATA = 15  # bias, scale
    REBOOT = 68
    
    # 100's are from the Flight Controller ===========
    IDENT    = 100
    STATUS   = 101
    RAW_IMU  = 102  # 9DOF
    SERVO    = 103
    MOTOR    = 104
    RC       = 105
    RAW_GPS  = 106
    COMP_GPS = 107
    # ATTITUDE = 108
    # ALTITUDE   = 109
    ANALOG     = 110
    RC_TUNING  = 111
    PID        = 112
    POSE       = 113
    # BOX        = 113
    # MISC       = 114
    # MOTOR_PINS = 115
    # BOXNAMES   = 116
    # PIDNAMES   = 117
    WP         = 118
    # BOXIDS     = 119
    SERVO_CONF = 120
    
    
    IMU_AGMQT = 140
    IMU_AGMT  = 141
    IMU_AGT   = 142
    IMU_AT    = 143
    MAGNETIC  = 144
    RANGE     = 145
    # LASER     = 146
    TEMP_PRES = 147

    
    # SET_RAW_RC       = 200
    # SET_RAW_GPS      = 201
    SET_PID          = 202
    # SET_BOX          = 203
    SET_RC_TUNING    = 204
    ACC_CALIBRATION  = 205  # bias, scale ??
    MAG_CALIBRATION  = 206  # bias, scale ??
    GYR_CALIBRATION  = 207  # bias, scale ??
    # SET_MISC         = 207
    # RESET_CONF       = 208
    SET_WP           = 209
    # SWITCH_RC_SERIAL = 210
    # SET_HEADING      = 211
    SET_POSE          = 211  # pos (x,y,altitude), attitude(roll,pitch,yaw)
    # SET_SERVO_CONF   = 212
    SET_MOTOR        = 214
    
    YIVO_ERROR = 250
    

def checksum(size,msgid,msg):
    a,b = struct.pack('H', size)
    # cs = size ^ msgid
    cs = a ^ b
    cs ^= msgid
    for m in msg:
        cs ^= m
    # print("cs", cs, cs.to_bytes(1,'little'))
    return cs

def chunk(msg):
    # size = msg[3]
    # msgid = msg[4]
    # payload = msg[5:-1]
    # cs = msg[-1]
    # return size, msgid, payload, cs
    size = msg[2] + (msg[3] << 8) # messages sent little endian
    msgid = msg[4]
    payload = msg[5:-1]
    cs = msg[-1]
    return size, msgid, payload, cs

def num_fields(sensor):
    return len(sensor._fields)

class Yivo:
        
    # [ 0, 1, 2, 3,4, ..., -1]
    # [h0,h1,LN,HN,T, ..., CS]
    # Header: h0, h1
    # N = (HN << 8) + LN, max data bytes is 65,536 Bytes 
    #   HN: High Byte
    #   LN: Low Byte
    # T: packet type or MsgID
    msgInfo = {
        MsgIDs.IDENT:     (Struct("<2chBBBBIB"), IDENT,),
        MsgIDs.RAW_IMU:   (Struct("<2chB9hB"),   IMU_RAW,),
        MsgIDs.IMU_AGMQT: (Struct("<2chB14fLB"), ImuAGMQT,),
        MsgIDs.IMU_AGMT:  (Struct("<2chB10fLB"), ImuAGMT,),
        MsgIDs.IMU_AGT:   (Struct("<2chB7fLB"),  ImuAGT,),
        MsgIDs.MAGNETIC:  (Struct("<2chB3fB"),   MagneticField,),
        MsgIDs.TEMP_PRES: (Struct("<2chB2fB"),   TemperaturePressure,),
        MsgIDs.ACC_CALIBRATION: (Struct("<2chB6fB"),   CALIBRATION,),
        MsgIDs.MAG_CALIBRATION: (Struct("<2chB6fB"),   CALIBRATION,),
        MsgIDs.GYR_CALIBRATION: (Struct("<2chB6fB"),   CALIBRATION,),
        MsgIDs.YIVO_ERROR: (Struct("<2chBBB"),   YivoError,),
    }
    pack_cs = Struct("<B")
    
    def __init__(self, h0=b'$', h1=b'K'):
        """
        Message header can be changed (not sure why) if you need to
        by setting a new h0 and h1. They must be binary characters.
        """
        if not isinstance(h0, bytes) or not isinstance(h1, bytes):
            raise Exception(f"Invalid header bytes: {h0}({type(h0)}) {h1}({type(h1)})")
        self.header = (h0,h1,)
        
    def pack(self, msgID, data):
        """
        Given a MsgID and a tuple of data, returns a yivo message packet
        """
        fmt, _ = self.msgInfo[msgID]
        sz = fmt.size - 6
        # print(f">> {fmt.size - 6} == {sz}")
        # cs = checksum(sz,msgID,data) # can't do this, cs will be diff!!
        # direction = b'>' if msgID < 200 else b'<'
        # msg = fmt.pack(b'$',b'M', sz, msgID, *data, 0)
        msg = fmt.pack(*self.header, sz, msgID, *data, 0)
        cs = checksum(sz,msgID,msg[5:-1])
        msg = msg[:-1] + self.pack_cs.pack(cs) #cs.to_bytes(1,'little')
        return msg
    
    def unpack(self,msg):
        """
        Unpacks a binary yivo packet
        
        Returns:
            MsgID
            Message
        """
        size, msgid, payload, cs = chunk(msg)
        # print(msg[0],self.header[0],msg[1], self.header[1])
        # if (msg[:2] != b"$M"):
        # if (msg[:2] != self.header):
        a = ord(self.header[0])
        b = ord(self.header[1])
        if (msg[0] != a) or (msg[1] != b):
            print(msg[:2], self.header)
            return Errors.INVALID_HEADER
        
        if (size != len(payload)):
            print(len(payload),"!=", size)
            return Errors.INVALID_LENGTH
        # print(size, len(payload))
        
        if checksum(size, msgid, payload) != cs:
            print("checksum failure", cs, "!=", checksum(size, msgid, payload))
            return Errors.INVALID_CHECKSUM
        # print(cs, checksum(size, msgid, payload))
        
        fmt, obj = self.msgInfo[msgid]
        info = fmt.unpack(msg)
        # print(info)
        
        return msgid, obj(*info[4:-1])
    
    def read_packet(self, ser, retry=32):
        while ser.in_waiting < 3:
            time.sleep(0.0001)

        # make a FIFO of size 2 to hold the header
        rbuf = deque(maxlen=2)
        rbuf.append(ser.read(1))
        # header = deque([b'\xff',b'\xff'])
        header = deque(self.header)

        # while True:
        while retry:
            retry -= 1
            # get header
            rbuf.append(ser.read(1))
            if rbuf != header:
                continue

            break

        # [0xff,0xff,len, [header[2], size[2], type, ...data..., check_sum]
        sz = ser.read(2)
        size = (sz[1] << 8) + sz[0]
        msgid = ord(ser.read(1))
        payload = ser.read(size)
        cs = ord(ser.read(1))
        return [self.h0,self.h1]+sz+[msgid]+payload+[cs]
        