---
title: C and Python Integration
image: "https://i.pinimg.com/564x/45/bc/6f/45bc6f01512339aed405a3aed860d0e8.jpg"
---

| Approach	          | Vintage |	Representative User	| Notable Pros                                          | Notable Cons |
|---------------------|---------|---------------------|-------------------------------------------------------|--------------|
| C extension modules |	1991    | Standard library    |	Extensive docs/tutorials. Total control and fast.     |	Compilation, portability, reference management. High C knowledge. |
| SWIG                | 1996    | crfsuite	          | Generate bindings for many languages at once          | Excessive overhead if Python is the only target. |
| ctypes              | 2003    | oscrypto            | No compilation, wide availability                     | Accessing and mutating C structures cumbersome, high overhead, and error prone. |
| Cython              | 2007    | gevent, kivy        | Python-like. Highly mature. High performance.	        | Compilation, new syntax and toolchain. |
| cffi                | 2013    | cryptography, pypy  | Ease of integration, PyPy compatibility               | New/High-velocity. |

- [Paypal blog](https://www.paypal-engineering.com/2016/09/22/python-by-the-c-side/)

## C Function Performance

- [ctypes example](http://www.dalkescientific.com/writings/NBN/c_extensions.html)

```python
import math, time, ctypes

R = range(100000)

# ctypes.RTLD_GLOBAL: Flag to use as mode parameter.
# The mode parameter can be used to specify how the library is loaded. For details,
# consult the dlopen(3) manpage. On Windows, mode is ignored. On posix systems,
# RTLD_NOW is always added, and is not configurable.
libc = ctypes.CDLL("libc.dylib", ctypes.RTLD_GLOBAL)
libc.cos.argtypes = [ctypes.c_double]  # args
libc.cos.restype = ctypes.c_double     # return type

def do_timings(cos):
  t1 = time.time()
  for x in R:
    cos(0.0)
  return time.time()-t1

def do_math_cos():
  return do_timings(math.cos)

def do_libc_cos():
  return do_timings(libc.cos)

print("math.cos", do_math_cos())
print("libc.cos", do_libc_cos())
```

```bash
math.cos 0.179316997528
libc.cos 0.487237215042
```

## C++ Function Example

- [How to return array from C++ function to Python using ctypes](https://stackoverflow.com/questions/14887378/how-to-return-array-from-c-function-to-python-using-ctypes)

```cpp
extern "C" int* function(){
    int* information = new int[10];
    for(int k=0;k<10;k++){
        information[k] = k;
    }
    return information;
}
```

```
g++ -c -fPIC function.cpp -o function.o
g++ -shared -Wl,-soname,library.so -o library.so function.o
```

It's probably easier to just use [np.ctypeslib](https://docs.scipy.org/doc/numpy/reference/routines.ctypeslib.html) instead of frombuffer yourself.

Using `numpy`:

```pytyhon
import ctypes
from numpy.ctypeslib import ndpointer

lib = ctypes.CDLL('./library.so')
lib.function.restype = ndpointer(dtype=ctypes.c_int, shape=(10,))

res = lib.function()
```

or

Using python `ctypes`:

```python
import ctypes

f = ctypes.CDLL('./library.so').function
f.restype = ctypes.POINTER(ctypes.c_int * 10)
print [i for i in f().contents] # output: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
```

## Another

```cpp
void square(double* array, int n) {
    int i;
    for (i=0; i<n; ++i) {
        array[i] = array[i] * array[i];
    }
}
```

```
gcc -c square.c # compile the code to an object file
gcc square.o -shared -o square.so # compile to shared object file
```

```python
import numpy as np
import ctypes

square = ctypes.cdll.LoadLibrary("./square.so")

n = 5
a = np.arange(n, dtype=np.double)

aptr = a.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
square.square(aptr, n)

print(a)
```

# References

- [ctypes tutorial](https://pgi-jcns.fz-juelich.de/portal/pages/using-c-from-python.html)
- [Python 3 ctypes](https://docs.python.org/3/library/ctypes.html)
- [Python 3 fundamental data types](https://docs.python.org/3/library/ctypes.html#fundamental-data-types)
- [another](http://intermediate-and-advanced-software-carpentry.readthedocs.io/en/latest/c++-wrapping.html)
