---
title: Software Serial Port
---

You can create a software serial port (bit banging) using the `pigpio` library.

```python
#!/usr/bin/env python

# bb_serial.py
# 2014-12-23
# Public Domain

# bit bang transmit and receive of serial data
#
# tested by connecting the arbitrary RX/TX gpios to a USB
# serial dongle plugged in to a Linux box.
#
# on the Linux box set the baud and data bits (cs5-cs8)
#
# stty -F /dev/ttyUSB0 19200 cs8
# cat </dev/ttyUSB0 >/dev/ttyUSB0
#
# so the Linux box echoes back data received from the Pi.
#
# laptop timings deviations
#
# baud  exp us   act us
#   50   20000    13310 * 75
#   75   13333    13310
#  110    9091    13310 * 75
#  134    7462     6792 * 150
#  150    6667     6792
#  200    5000     6792 * 150
#  300    3333     3362
#

import sys
import time
import difflib

import pigpio

RX=19
TX=26

MSGLEN=256

if len(sys.argv) > 1:
   baud = int(sys.argv[1])
else:
   baud = 115200

if len(sys.argv) > 2:
   bits = int(sys.argv[2])
else:
   bits = 8

if len(sys.argv) > 3:
   runtime = int(sys.argv[3])
else:
   runtime = 300

ten_char_time = 100.0 / float(baud)

if ten_char_time < 0.1:
   ten_char_time = 0.1

MASK=(1<<bits)-1

# initialise test data

msg = [0] * (MSGLEN+256)

for i in range(len(msg)):
   msg[i] = i & MASK

first = 0

pi = pigpio.pi()

pi.set_mode(TX, pigpio.OUTPUT)

# fatal exceptions off (so that closing an unopened gpio doesn't error)

pigpio.exceptions = False

pi.bb_serial_read_close(RX)

# fatal exceptions on

pigpio.exceptions = True

# create a waveform representing the serial data

pi.wave_clear()

TEXT=msg[first:first+MSGLEN]
pi.wave_add_serial(TX, baud, TEXT)
wid=pi.wave_create()

# open a gpio to bit bang read the echoed data

pi.bb_serial_read_open(RX, baud, bits)

# zero error counts

bad_char = 0
total_char = 0

# run for fixed time

start=time.time()

while (time.time()-start) < runtime:

   pi.wave_send_once(wid)   # transmit serial data
   pi.wave_delete(wid)

   TXTEXT = TEXT

   first += 1
   if first >= MSGLEN:
      first = 0

   TEXT=msg[first:first+MSGLEN]
   pi.wave_add_serial(TX, baud, TEXT,bb_bits=7)

   while pi.wave_tx_busy(): # wait until all data sent
     pass

   wid=pi.wave_create()

   count = 1
   text=""
   lt = 0
   total_char += MSGLEN

   while count: # read echoed serial data
      (count, data) = pi.bb_serial_read(RX)
      if count:
         text += data
         lt += count
      time.sleep(ten_char_time) # enough time to ensure more data

   if text != TXTEXT: # Do sent and received match?
      if lt == MSGLEN: # No, is message correct length?
         for i in range(MSGLEN): # If so compare byte by byte.
            if text[i] != TXTEXT[i]:
               # print("{:2X} {:2X}".format(text[i], TXTEXT[i]))
               bad_char += 1
      else: # Wrong message length, find matching blocks.
         ok = 0
         s=difflib.SequenceMatcher(None, TXTEXT, text)
         for frag in  s.get_matching_blocks():
            ok += frag[2] # More matching bytes found.
            # print(frag)
         # print(text, MSGLEN, ok)
         if ok < MSGLEN: # Sanity check.
            bad_char += (MSGLEN - ok)
         else:
            print("*** ERRONEOUS good={} LEN={} ***".format(ok, MSGLEN))

print("secs={} baud={} bits={} bad={:.3f}%".
   format(runtime, baud, bits, float(bad_char)*100.0/float(total_char)))

print("total={} badchar={}".format(total_char, bad_char))

# free resources

pi.wave_delete(wid)

pi.bb_serial_read_close(RX)

pi.stop()
```
