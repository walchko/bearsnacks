---
title: ZeroMQ
---

# Dealer and Router

![](https://raw.githubusercontent.com/booksbyus/zguide/master/images/fig17.png)

DEALER and ROUTER are sockets, which can allow easy scaling of REQ / REP pairs.

In direct communication, REQ and REP are talking in blocking manner.

## ROUTER - accept requests - from REQ side

A router is able to accepts requests, adds an envelope with information about that requestee, and makes this new message available for further processing by interconnecting code). When the response comes back (in an envelop), it can pass the response back to the requestee.

## DEALER - talks to workers - on REP side

Dealer cares about workers. Note, that to make the whole solution usable, workers have to connect to the dealer, not the other way around.

DEALER also allows non-blocking connection with REP.

Some connecting code passes a request in an envelope to the DEALER. The dealer manages the distribution of such requests to workers (without the envelope) and later responds back to the interconnecting code (again in an envelope).

## Interconnecting code

An interconnecting code is to shuffle messages between ROUTER and DEALER sockets.

The simplest version is here: http://zguide.zeromq.org/py:rrbroker

<script src="https://gist.github.com/walchko/cc321de35351596f570b80df0d3d0d1d.js"></script>

Other capabilities can be found in the docs.

## Reference

- [zmq guide](http://zguide.zeromq.org/page:all#toc39)
- [Stackoverflow](https://stackoverflow.com/questions/23581172/what-is-zmq-router-and-zmq-dealer-in-python-zeromq)
