---
title: Asyncio
date: 16 Jan 2021
image: "https://i.pinimg.com/564x/6c/f0/af/6cf0af36e1267a4c7985a4abf73a5d25.jpg"
image-height: "400px"
---

The asyncio package is part of the python language. It has undergone a lot of change from 3.4 to present. *Not sure how useful it is.*

- Asyncio: for io-bound tasks, single threaded, single-process, cooperative multitasking, not parallelism (multi-process), more similar to threading, 1 processor
    - Don’t use with code that is all blocking, it will slow things down
    - Scales better than threading, can’t create 1000’s of thread, but can do
    - Simplier to implement, threading can produce “infamous impossible-to-trace bugs due to race conditions and memory usage”
    - Shine where blocking IO wait times would dominate task
    - Asyncio.run()
    - Asyncio.create_task(): schedule execution of coroutine object followed by asyncio.run()
        - For python < 3.7, use asyncio.ensure_future()
    - Asyncio.gather(): similar to `threading.join()` for multiple coroutines
- Multiprocessing: meant to effect parallelism, spread tasks over a computer’s CPU/cores, cpu-bound tasks, many processors
- Threading: a concurrent execution model where multiple threads take turns executing within a single process thanks to the GIL. Io-bound tasks, 1 processor
- Asynchronous
    - Asynchronous routines are able to “pause” while waiting on their ultimate result and let other routines run in the meantime.
    - Asynchronous code, through the mechanism above, facilitates concurrent execution. To put it differently, asynchronous code gives the look and feel of concurrency.
- `async def` is a coroutine
    - It can use await, return or yield
    - You must call `await` to get results from a coroutine
    - `yield`  is less common and only recently allowed
    - `yield from` is not allowed for a corouine
    - Outdated decorator `@asyncio.coroutine`
- For http stuff use `aiohttp`, everything is `await`able coroutine
    - Don’t use `requests`, it doesn’t support coroutines

```python
async def f(x):
    y = await z(x)  # OK - `await` and `return` allowed in coroutines
    return y

async def g(x):
    yield x  # OK - this is an async generator

async def m(x):
    yield from gen(x)  # No - SyntaxError

def m(x):
    y = await z(x)  # Still no - SyntaxError (no `async def` here)
    return y

@asyncio.coroutine
def py34_coro():
    """Generator-based coroutine, outdated syntax with decorator"""
    yield from stuff()
```

```python
start = time.perf_counter()
# do something
end = time.perf_counter() – start

print(f"Program finished in {end:0.2f} seconds.")
```


# References

- realpython: [asyncio python](https://realpython.com/async-io-python/)
