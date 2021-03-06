---
title: Python and Command Line Args
image: "https://i.pinimg.com/564x/cb/47/c0/cb47c02aa9661d1761006db2c8e122e2.jpg"
---

```python
import sys

sys.argv[0]        # program
sys.argv[1]        # arg 1
len(sys.argv) - 1  # number args
```

```python
import argparse
import apt # my cool toolbox

def handle_args():
    parser = argparse.ArgumentParser(description="This is a cool program")
    parser.add_argument("filename", type=str, help="set filename")                 # manditory
    parser.add_argument("--width", "-w", type=int, help="set output width")        # optional, int
    parser.add_argument("-p", "--parse", help="do something", action="store_true") # bool
    parser.add_argument('-v', '--version', action='version', version=apt.__version__)
    return vars(parser.parse_args())
```
