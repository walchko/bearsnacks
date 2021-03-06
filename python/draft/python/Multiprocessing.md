---
title: Multi-Processing
---

I generally dislike how python does threads, so I don't use them. They tend
to be more trouble than they are worth.

## Queues

Think FIFO

## Events

Boolean values shared across processes

## Sharing Namespace

Using the `SyncManager`, you can provide a shared namespace between running
processes. Data in the namespace is automagically updated when a new assignment
is made.

- Data needs to be **picklable**, so objects that do hardware I/O aren't picklable. Therefore, things like i2c, serial, etc won't work in namespaces
   - You need to keep any classes/functions/whatever that talk to hardware in one process. You cannot have multiple processes read/write to them.
   - You can have the hardware code read dat into a namespace variable or grad data from a namespace and write it out to hardware. I do not know what the latency of something like that is.
- Updates namespace on assignment: namespace.data = new_data
- Doesn't update namespace: namespace.data.append(new value)



<script src="https://gist.github.com/walchko/22c79428d11fcdc188dd7b934dce968a.js"></script>

# References

- [Python module of the week: multiprocessing](https://pymotw.com/2/multiprocessing/communication.html)
- [A great comparision of threads and processes](static/multiprocessing.pdf)
