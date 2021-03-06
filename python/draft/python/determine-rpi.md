---
title: Determine Raspberry Pi
date: 27 Oct 2019
---

## Ubuntu

```python
>>> import platform
>>> platform.platform()
'Linux-4.15.0-1048-raspi2-aarch64-with-Ubuntu-18.04-bionic'
>>> import os
>>> os.uname()
posix.uname_result(sysname='Linux', nodename='ros', release='4.15.0-1048-raspi2', version='#52-Ubuntu SMP PREEMPT Wed Sep 18 08:57:33 UTC 2019', machine='aarch64')
>>> 
```

## Raspbian (Buster)

```python
>>> import platform
>>> platform.platform()
'Linux-4.19.73-v7+-armv7l-with-debian-10.1'
>>> import os
>>> os.uname()
posix.uname_result(sysname='Linux', nodename='ultron', release='4.19.73-v7+', version='#1267 SMP Fri Sep 20 18:10:01 BST 2019', machine='armv7l')
```


# References

- [Adafruit example](https://github.com/adafruit/Adafruit_Python_GPIO/blob/master/Adafruit_GPIO/Platform.py)
