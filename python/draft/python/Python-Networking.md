---
title: Networking
---

## Netaddr

`Netaddr` has a lot of useful functions for working with ip addresses.

```python

>>> import netaddr
>>> dir(netaddr)
['AddrConversionError', 'AddrFormatError', 'EUI', 'IAB', 'INET_PTON', 'IPAddress', 'IPGlob', 'IPNetwork', 'IPRange', 'IPSet', 'N', 'NOHOST', 'NotRegisteredError', 'OUI', 'P', 'STATUS', 'SubnetSplitter', 'VERSION', 'Z', 'ZEROFILL', '__builtins__', '__doc__', '__file__', '__name__', '__package__', '__path__', '__version__', '_sys', 'all_matching_cidrs', 'base85_to_ipv6', 'cidr_abbrev_to_verbose', 'cidr_exclude', 'cidr_merge', 'cidr_to_glob', 'compat', 'contrib', 'core', 'eui', 'eui64_bare', 'eui64_base', 'eui64_cisco', 'eui64_unix', 'eui64_unix_expanded', 'glob_to_cidrs', 'glob_to_iprange', 'glob_to_iptuple', 'ip', 'iprange_to_cidrs', 'iprange_to_globs', 'ipv6_compact', 'ipv6_full', 'ipv6_to_base85', 'ipv6_verbose', 'iter_iprange', 'iter_nmap_range', 'iter_unique_ips', 'largest_matching_cidr', 'mac_bare', 'mac_cisco', 'mac_eui48', 'mac_pgsql', 'mac_unix', 'mac_unix_expanded', 'smallest_matching_cidr', 'spanning_cidr', 'strategy', 'valid_eui64', 'valid_glob', 'valid_ipv4', 'valid_ipv6', 'valid_mac', 'valid_nmap_range']
>>> netaddr.valid_ipv4('192.168.1.1')
True
>>> netaddr.valid_ipv4('192.168.1.300')
False
```

## Get IP Address from Interface

```python

import os, re

def getIP(iface):
    search_str = 'ip addr show wlan0'.format(iface)
    ipv4 = re.search(re.compile(r'(?<=inet )(.*)(?=\/)', re.M), os.popen(search_str).read()).groups()[0]
    ipv6 = re.search(re.compile(r'(?<=inet6 )(.*)(?=\/)', re.M), os.popen(search_str).read()).groups()[0]
    return (ipv4, ipv6)
```

## Networking

A really good resource for network programming with python is [here](static/PythonNetBinder.pdf)

## Get Host IP Address

```python
# Get Your External IP Address
def get_ip():
	"""
	Returns the host IP address or None if address could not be discovered.
	"""
    ip_addr = None
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        s.connect(('<broadcast>', 0))
        ip_addr=s.getsockname()[0]
    except Exception:
        pass
    return ip_addr
```
