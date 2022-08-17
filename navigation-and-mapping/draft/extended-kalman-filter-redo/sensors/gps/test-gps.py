#!/usr/bin/env python

import serial
import time
from adafruit_gps import GPS

port = "/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_A506BOT5-if00-port0"

ser = serial.Serial(port, baudrate=9600, timeout=3000)
gps = GPS(ser)

"""
PMTK_A11.pdf pg 12
Data Field：
There are totally 19 data fields that present output frequencies for the 19 supported
NMEA sentences individually.
Supported NMEA Sentences
0 NMEA_SEN_GLL, // GPGLL interval - Geographic Position - Latitude longitude
1 NMEA_SEN_RMC, // GPRMC interval - Recommended Minimum Specific GNSS Sentence
2 NMEA_SEN_VTG, // GPVTG interval - Course over Ground and Ground Speed
3 NMEA_SEN_GGA, // GPGGA interval - GPS Fix Data
4 NMEA_SEN_GSA, // GPGSA interval - GNSS DOPS and Active Satellites
5 NMEA_SEN_GSV, // GPGSV interval - GNSS Satellites in View
6 //Reserved
7 //Reserved
13 //Reserved
14 //Reserved
15 //Reserved
16 //Reserved
17 //Reserved
18 NMEA_SEN_MCHN, // PMTKCHN interval – GPS channel status
Supported Frequency Setting
0 - Disabled or not supported sentence
1 - Output once every one position fix
2 - Output once every two position fixes
3 - Output once every three position fixes
4 - Output once every four position fixes
5 - Output once every five position fixes
Example:
$PMTK314,1,1,1,1,1,5,0,0,0,0,0,0,0,0,0,0,0,0,0*2C<CR><LF>
"""
# gps.send_command(b'PMTK314,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0') # minimum
gps.send_command(b'PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0') # setup typical
# gps.send_command(b'PMTK314,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0') # everything
gps.send_command(b'PMTK220,1000')  # 1 Hz
# gps.send_command(b'PMTK220,500')  # 2 Hz, 500 msec

for i in range(10):
    # data = ser.read(1024)
    # print(data, flush=True)
    time.sleep(0.5)

    ok = gps.update()
    if not ok or gps.has_fix is False:
        print("no data")
    else:
        print('=' * 40)  # Print a separator line.
        print("Fix:", gps.has_fix)
        print("Satellites:", gps.satellites)
        print("Sats:", gps.sats)
        print('Latitude: {0:.6f} degrees'.format(gps.latitude))
        print('Longitude: {0:.6f} degrees'.format(gps.longitude))
        print("Alititude [m]:", gps.altitude_m)
        print("Altitude Geod [m]", gps.height_geoid)
        print("Speed [knots]:", gps.speed_knots)
        print("Dop: {} {} {}".format(gps.pdop, gps.hdop, gps.vdop))
        print("Fix: {} {}".format(gps.fix_quality, gps.fix_quality_3d))
        print("PRNs:", gps.sat_prns)
        # print("Fix Raw timestamp:", gps.timestamp_utc)
        print('Fix timestamp: {:02}/{:02}/{} {:02}:{:02}:{:02}'.format(
            gps.timestamp_utc.tm_mon,   # Grab parts of the time from the
            gps.timestamp_utc.tm_mday,  # struct_time object that holds
            gps.timestamp_utc.tm_year,  # the fix time.  Note you might
            gps.timestamp_utc.tm_hour,  # not get all data like year, day,
            gps.timestamp_utc.tm_min,   # month!
            gps.timestamp_utc.tm_sec))
