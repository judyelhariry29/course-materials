# Module 1 · Session 3 — Tooling Reference

## Scapy and Raw Packet Crafting

### Professional Training in Cybersecurity I

---

> [!note] What this document is for
> The session used Scapy to build, read, send, probe and capture packets, and the lab's command-line tools to start the target and read a capture.
> **This is the fuller treatment**: every Scapy call, standard-library call and command-line tool the Practical Guide and the Home Task use, each with what it is for, an example with its real output, and the mistakes it invites.
> Nothing here is required reading in order.
> Come to it when you need it.
>
> Every example is a small file followed by the command that runs it and what it printed, so you can save it in your working folder, `~/cyberlabs/Module1-Network-Attacks-and-Defense/Session3`, and see the same.
> The examples use values of their own (the echo identifier `0x0b0b`, UDP ports 33333 and 9999, the data `ref-data` and `reference`), so no example repeats an exercise or a task.
> Where an example needs two terminals, the line marked `[first terminal]` is the program started first, and its output follows under `[first terminal output]`.

> [!note] Recorded on Kali
> These examples were recorded on the lab's Kali (kernel 6.12.25) with **Python 3.13.12**, **Scapy 2.8.0** in the session's `.venv`, **Docker 28.5.2**, **Docker Compose 2.40.3**, **iproute2 6.14.0** and **tcpdump 4.99.6**, against the Practical Guide's compose lab.
> The compose file fixes the lab's addresses, so every `10.10.3.x` address and the target's MAC address `02:42:0a:0a:03:0a` are the same in your run.
> The recording machine's other interfaces, `eth0` at `10.0.2.15` and `eth1` at `192.168.56.107`, are its own: read yours from your own output.
> Times, timestamps and the bridge's own MAC address differ on every run.

> [!warning] Your own lab only
> Every example that sends or captures uses the lab network inside your own Kali, `10.10.3.0/24`, and nothing else.
> Run under `sudo` only programs you wrote or read.

---

# The Session's Python Environment

The Practical Guide's setup installed Scapy 2.8.0 in `.venv`, inside your working folder.
Building and reading packets needs no privilege, and sending and capturing need root, so which Python runs under `sudo` matters.

## Which Python runs, with and without `sudo`

```
(.venv) $ which python3
/home/kali/cyberlabs/Module1-Network-Attacks-and-Defense/Session3/.venv/bin/python3
(.venv) $ python3 -c "import scapy; print(scapy.__version__, scapy.__file__)"
2.8.0 /home/kali/cyberlabs/Module1-Network-Attacks-and-Defense/Session3/.venv/lib/python3.13/site-packages/scapy/__init__.py
(.venv) $ sudo .venv/bin/python -c "import scapy; print(scapy.__version__, scapy.__file__)"
2.8.0 /home/kali/cyberlabs/Module1-Network-Attacks-and-Defense/Session3/.venv/lib/python3.13/site-packages/scapy/__init__.py
(.venv) $ sudo sh -c 'command -v python3'
/usr/bin/python3
```

- `which` names the file the shell runs for a command, and inside the environment it is the environment's own `python3`.
- `scapy.__file__` names the file Python loaded the library from, so it shows which Scapy a program really uses: here the one in `.venv`.
- `sudo` runs one command as root, with a fixed search path of its own that never includes `.venv`.
  So a bare `python3` under `sudo` is Kali's own `/usr/bin/python3`, as the last command shows.
- `sudo .venv/bin/python` names the environment's interpreter by its path, so the program runs as root with the session's Scapy.
  The path is relative: run it from the working folder.
- The first `sudo` in a terminal asks for your Kali password, and later ones in the same terminal reuse it for a few minutes.

## Arguments and files: `sys.argv` and `pathlib`

Every program in the session reads its interface, its addresses or its file from the command line, and stops with a usage line when they are missing.

```python
"""args_files.py: read the file named on the command line, and write a copy beside it"""
import sys
from pathlib import Path

if len(sys.argv) != 2:
    sys.exit("usage: python3 args_files.py FILE")
source = Path(sys.argv[1])
print("sys.argv:", sys.argv)
print("name:", source.name, "| suffix:", source.suffix, "| exists:", source.exists())
content = source.read_bytes()
print(len(content), "bytes, the first 8:", content[:8])
copy = source.with_name("copy_of_" + source.name)
copy.write_bytes(content)
print("wrote", copy.name, "-", copy.stat().st_size, "bytes")
```

```
(.venv) $ python3 args_files.py args_files.py
sys.argv: ['args_files.py', 'args_files.py']
name: args_files.py | suffix: .py | exists: True
564 bytes, the first 8: b'"""args_'
wrote copy_of_args_files.py - 564 bytes
(.venv) $ python3 args_files.py
usage: python3 args_files.py FILE
(.venv) $ echo $?
1
```

| Call | What it does |
|---|---|
| `sys.argv` | the list of words on the command line: the script's name first, then each argument as a string |
| `sys.exit("usage: ...")` | prints the string on the error stream and ends the program with exit status 1 |
| `Path(text)` | a path object for a file name, with no file opened yet |
| `.name`, `.suffix`, `.exists()` | the last part of the path, its extension, and whether the file is there |
| `.read_bytes()`, `.write_bytes(data)` | the whole file as `bytes`, or `bytes` written as the whole file |
| `.with_name(name)` | the same folder with another file name |
| `.stat().st_size` | the file's size in bytes |

- `echo $?` prints the exit status of the last command: 1 after the usage line, 0 after a normal end.
- `read_bytes` returns `bytes`, the type Scapy dissects, so a captured frame saved to a file goes straight back into a layer class.

---

# Building Packets

A **layer object** holds one header as named fields, and a packet is a stack of layer objects.
Building needs no privilege and no lab: everything in this section runs with plain `python3`.

## Protocol classes and `ls()`

Each header has a **protocol class**, and `ls()` lists a class's fields in wire order, each with its type and its default.

```python
"""classes_demo.py: every field of a class, its type and its default"""
from scapy.all import Ether, TCP, ls

print("=== ls(Ether) ===")
ls(Ether)
print("=== ls(TCP) ===")
ls(TCP)
```

```
(.venv) $ python3 classes_demo.py
=== ls(Ether) ===
dst        : DestMACField                        = ('None')
src        : SourceMACField                      = ('None')
type       : XShortEnumField                     = ('36864')
=== ls(TCP) ===
sport      : ShortEnumField                      = ('20')
dport      : ShortEnumField                      = ('80')
seq        : IntField                            = ('0')
ack        : IntField                            = ('0')
dataofs    : BitField  (4 bits)                  = ('None')
reserved   : BitField  (3 bits)                  = ('0')
flags      : FlagsField                          = ('<Flag 2 (S)>')
window     : ShortField                          = ('8192')
chksum     : XShortField                         = ('None')
urgptr     : ShortField                          = ('0')
options    : TCPOptionsField                     = ("b''")
```

| Class | Header |
|---|---|
| `Ether` | Ethernet: `dst`, `src`, `type` |
| `IP`, `IPv6` | IPv4 and IPv6 |
| `TCP`, `UDP` | the transport headers |
| `ICMP` | an ICMP message: `type`, `code`, `chksum`, and `id` and `seq` for an echo |
| `Raw` | bytes no class describes, in its field `load` |
| `Padding` | bytes after the end of the packet, such as zeros that fill a short frame |

- `None` marks a field the build fills in: `Ether`'s `dst` and `src` come from Scapy's route and MAC lookup, and TCP's `dataofs` and `chksum` from the rest of the packet.
- `Ether`'s `type` default, `36864`, is `0x9000`, which stays only when no layer is stacked on it.
- TCP's defaults make a SYN from port 20 to port 80, so every field you do not set still has a value.

## Fields: set, read and change, then build with `raw()`

```python
"""fields_demo.py: set, read and change fields, then build the bytes"""
from scapy.all import IP, UDP, raw

datagram = IP(src="10.10.3.1", dst="10.10.3.10") / UDP(sport=33333, dport=9999) / b"ref-data"
print("the object:", repr(datagram))
print("a default:", datagram[IP].ttl, "| computed, not built yet:", datagram[IP].len, datagram[UDP].chksum)
datagram[IP].ttl = 32
print("after the change:", datagram[IP].ttl)
built = raw(datagram)
print("built:", len(built), "bytes:", built.hex(" "))
print("raw() and bytes() agree:", built == bytes(datagram))
print("the object still holds:", datagram[IP].len, datagram[UDP].chksum)
```

```
(.venv) $ python3 fields_demo.py
the object: <IP  frag=0 proto=udp src=10.10.3.1 dst=10.10.3.10 |<UDP  sport=33333 dport=9999 |<Raw  load=b'ref-data' |>>>
a default: 64 | computed, not built yet: None None
after the change: 32
built: 36 bytes: 45 00 00 24 00 01 00 00 20 11 80 aa 0a 0a 03 01 0a 0a 03 0a 82 35 27 0f 00 10 8b 15 72 65 66 2d 64 61 74 61
raw() and bytes() agree: True
the object still holds: None None
```

| Call | What it does |
|---|---|
| `IP(src=..., dst=...)` | a layer with those fields set by keyword, in any order |
| `packet[IP].ttl` | reads one field of one layer |
| `packet[IP].ttl = 32` | changes it |
| `raw(packet)` | builds the packet into its bytes, filling every computed field |
| `bytes(packet)` | the same bytes as `raw(packet)` |

- The object prints the fields that were set: by an argument, or by the layer stacked on it (`proto=udp` and `frag=0`, both written for the UDP layer above).
- The TTL's default is 64, and the change shows in the built bytes: byte 8 is `20`, which is 32.
- `raw()` returns the bytes and leaves the object as it was: its length and checksum are still `None` after the build.
  To read the computed values, dissect the bytes, or use `show2()` (*Reading Packets* below).

## Stacking layers with `/`

`A / B` puts B under the last layer of A, so a stack is written from the outside in.

```python
"""stack_demo.py: what each / writes into the layer below it"""
from scapy.all import Ether, IP, IPv6, UDP, raw

over_ipv4 = (Ether(dst="02:42:0a:0a:03:0a", src="08:00:27:12:34:56")
             / IP(src="10.10.3.1", dst="10.10.3.10") / UDP(sport=33333, dport=9999) / b"ref-data")
over_ipv6 = (Ether(dst="02:42:0a:0a:03:0a", src="08:00:27:12:34:56")
             / IPv6(src="fd00::1", dst="fd00::a") / UDP(sport=33333, dport=9999) / b"ref-data")
print("after the /, before any build: Ether type", hex(over_ipv4.type), "| IPv4 proto", over_ipv4[IP].proto,
      "| IPv4 len", over_ipv4[IP].len)

built_ipv4 = Ether(raw(over_ipv4))
print("IPv4 stack: Ether type", hex(built_ipv4.type), "| IPv4 proto", built_ipv4[IP].proto,
      "| IPv4 len", built_ipv4[IP].len, "| UDP len", built_ipv4[UDP].len)
built_ipv6 = Ether(raw(over_ipv6))
print("IPv6 stack: Ether type", hex(built_ipv6.type), "| IPv6 nh", built_ipv6[IPv6].nh,
      "| IPv6 plen", built_ipv6[IPv6].plen, "| UDP len", built_ipv6[UDP].len)
```

```
(.venv) $ python3 stack_demo.py
after the /, before any build: Ether type 0x800 | IPv4 proto 17 | IPv4 len None
IPv4 stack: Ether type 0x800 | IPv4 proto 17 | IPv4 len 36 | UDP len 16
IPv6 stack: Ether type 0x86dd | IPv6 nh 17 | IPv6 plen 16 | UDP len 16
```

- The `/` writes the lower layer's **next-protocol field** at once: Ethernet's `type` and IPv4's `proto` already read `0x800` and 17 before any build.
- Lengths and checksums wait for the build, so IPv4's `len` is still `None` until then.
- The field changes its name with the header: `type` in Ethernet, `proto` in IPv4, `nh` (next header) in IPv6, and 17 means UDP in both IP versions.
- `hex()` drops leading zeros, so the EtherType `0x0800` prints as `0x800`.
- IPv4's `len` counts its own 20 bytes and the 16 under it, and IPv6's `plen` counts only the 16 under its 40-byte header.

## A copy, not a second name: `.copy()`

```python
"""copy_demo.py: a second name for a packet, against a copy of it"""
from scapy.all import IP, UDP

original = IP(dst="10.10.3.10") / UDP(sport=33333, dport=9999) / b"ref-data"
same_packet = original
copied_packet = original.copy()
same_packet[IP].ttl = 16
copied_packet[UDP].dport = 9998
print("original:     ttl", original[IP].ttl, "dport", original[UDP].dport)
print("copied_packet: ttl", copied_packet[IP].ttl, "dport", copied_packet[UDP].dport)
print("same_packet is original:", same_packet is original, "| copied_packet is original:", copied_packet is original)
```

```
(.venv) $ python3 copy_demo.py
original:     ttl 16 dport 9999
copied_packet: ttl 64 dport 9998
same_packet is original: True | copied_packet is original: False
```

- `same_packet = original` gives the same object a second name, so a change through either name changes it.
- `original.copy()` makes a new, independent packet with every field copied, so changing the copy leaves the original as it was.
- Copy a captured packet before you change it, when the original is still needed: a computed field set to `None` on the copy is filled again by the copy's next build.

---

# Reading Packets

A packet can be read four ways, and each answers a different question.
Every example in this section uses the same datagram, from `10.10.3.1` to the target's UDP port 9999.

## Four views: `summary()`, `show()`, `show2()` and `hexdump()`

```python
"""read_views.py: one datagram as a line, as fields before and after its build, and as bytes"""
from scapy.all import IP, UDP, hexdump

datagram = IP(src="10.10.3.1", dst="10.10.3.10") / UDP(sport=33333, dport=9999) / b"ref-data"
print("=== summary() ===")
print(datagram.summary())
print("=== show() ===")
datagram.show()
print("=== show2() ===")
datagram.show2()
print("=== hexdump() ===")
hexdump(datagram)
```

```
(.venv) $ python3 read_views.py
=== summary() ===
IP / UDP 10.10.3.1:33333 > 10.10.3.10:9999 / Raw
=== show() ===
###[ IP ]###
  version   = 4
  ihl       = None
  tos       = 0x0
  len       = None
  id        = 1
  flags     = 
  frag      = 0
  ttl       = 64
  proto     = udp
  chksum    = None
  src       = 10.10.3.1
  dst       = 10.10.3.10
  \options   \
###[ UDP ]###
     sport     = 33333
     dport     = 9999
     len       = None
     chksum    = None
###[ Raw ]###
        load      = b'ref-data'

=== show2() ===
###[ IP ]###
  version   = 4
  ihl       = 5
  tos       = 0x0
  len       = 36
  id        = 1
  flags     = 
  frag      = 0
  ttl       = 64
  proto     = udp
  chksum    = 0x60aa
  src       = 10.10.3.1
  dst       = 10.10.3.10
  \options   \
###[ UDP ]###
     sport     = 33333
     dport     = 9999
     len       = 16
     chksum    = 0x8b15
###[ Raw ]###
        load      = b'ref-data'

=== hexdump() ===
0000  45 00 00 24 00 01 00 00 40 11 60 AA 0A 0A 03 01  E..$....@.`.....
0010  0A 0A 03 0A 82 35 27 0F 00 10 8B 15 72 65 66 2D  .....5'.....ref-
0020  64 61 74 61                                      data
```

| Call | Shows |
|---|---|
| `packet.summary()` | one line: the layers, the addresses and ports, and TCP's flags when there is TCP |
| `packet.show()` | every field of every layer, **as the object holds it now**: a computed field not built yet is `None` |
| `packet.show2()` | the same after a build: the packet is built into bytes and dissected back, so every computed field holds its value |
| `hexdump(packet)` | the built bytes, 16 to a row: the offset in hex, the bytes in hex, and the same bytes as text |

- Each layer's block in `show()` is indented one step deeper than the layer carrying it.
- Known numbers print by name: `proto = udp` is 17.
- In `hexdump`, the text column shows a byte as a character when it is printable and as `.` otherwise, which is why the data `ref-data` is readable at the end.

## Reaching layers and fields: indexing, `in`, `getlayer`, `layers()` and `payload`

```python
"""index_demo.py: reach a layer by its class, a field by its name, and test before indexing"""
from scapy.all import IP, TCP, UDP, Raw

datagram = IP(src="10.10.3.1", dst="10.10.3.10") / UDP(sport=33333, dport=9999) / b"ref-data"
print("datagram[UDP].dport:", datagram[UDP].dport)
print("datagram[UDP]:", datagram[UDP].summary())
print("datagram[1]:  ", datagram[1].summary())
print("datagram[Raw].load:", datagram[Raw].load)
print("UDP in datagram:", UDP in datagram, "| TCP in datagram:", TCP in datagram)
print("getlayer(UDP).sport:", datagram.getlayer(UDP).sport, "| getlayer(TCP):", datagram.getlayer(TCP))
print("layers():", [layer.__name__ for layer in datagram.layers()])
print("UDP's payload:", datagram[UDP].payload.name, bytes(datagram[UDP].payload))
try:
    datagram[TCP]
except IndexError as error:
    print("datagram[TCP] raised IndexError:", error)
```

```
(.venv) $ python3 index_demo.py
datagram[UDP].dport: 9999
datagram[UDP]: UDP 10.10.3.1:33333 > 10.10.3.10:9999 / Raw
datagram[1]:   UDP 10.10.3.1:33333 > 10.10.3.10:9999 / Raw
datagram[Raw].load: b'ref-data'
UDP in datagram: True | TCP in datagram: False
getlayer(UDP).sport: 33333 | getlayer(TCP): None
layers(): ['IP', 'UDP', 'Raw']
UDP's payload: Raw b'ref-data'
datagram[TCP] raised IndexError: Layer [TCP] not found
```

| Expression | Returns |
|---|---|
| `packet[UDP]` | the UDP layer, with every layer inside it |
| `packet[UDP].dport` | one field of that layer |
| `packet[1]` | the layer at that position: 0 is the outermost |
| `UDP in packet` | `True` or `False`, without raising |
| `packet.getlayer(UDP)` | the same as `packet[UDP]`, but `None` when the layer is missing |
| `packet.layers()` | the list of the packet's layer classes, outermost first, each with its name in `__name__` |
| `packet[UDP].payload` | the layer carried inside UDP, and `bytes(...)` of it gives its bytes |

- Indexing a layer the packet does not carry raises `IndexError`, so test with `in` first, or use `getlayer` and check for `None`.
- A layer carries everything inside it, so `packet[UDP]` still holds the `Raw` data.

## Bytes back into layers: dissecting, and `Padding`

**Dissecting** reads bytes into layer objects: call the class of the outermost header on the bytes.

```python
"""dissect_demo.py: bytes back into layers, from Ethernet or from IPv4, with and without padding"""
from scapy.all import Ether, IP, Raw, Padding, ICMP, raw

request_frame = (Ether(dst="02:42:0a:0a:03:0a", src="08:00:27:12:34:56")
                 / IP(src="10.10.3.1", dst="10.10.3.10") / ICMP(id=0x0b0b, seq=5) / b"reference")
frame_bytes = raw(request_frame)
print(len(frame_bytes), "bytes")
print("Ether(frame_bytes):    ", Ether(frame_bytes).summary())
print("IP(frame_bytes[14:]):  ", IP(frame_bytes[14:]).summary())
print("computed fields filled:", Ether(frame_bytes)[IP].len, hex(Ether(frame_bytes)[IP].chksum))

padded_bytes = frame_bytes + bytes(60 - len(frame_bytes))
padded_frame = Ether(padded_bytes)
print(len(padded_bytes), "bytes:", padded_frame.summary())
print("IPv4 total length", padded_frame[IP].len, "| data", padded_frame[Raw].load,
      "| padding", len(padded_frame[Padding].load), "bytes")
```

```
(.venv) $ python3 dissect_demo.py
51 bytes
Ether(frame_bytes):     Ether / IP / ICMP 10.10.3.1 > 10.10.3.10 echo-request 0 / Raw
IP(frame_bytes[14:]):   IP / ICMP 10.10.3.1 > 10.10.3.10 echo-request 0 / Raw
computed fields filled: 37 0x60b9
60 bytes: Ether / IP / ICMP 10.10.3.1 > 10.10.3.10 echo-request 0 / Raw / Padding
IPv4 total length 37 | data b'reference' | padding 9 bytes
```

- `Ether(frame_bytes)` reads from byte 0 as Ethernet, and each next-protocol field picks the next class.
  `IP(frame_bytes[14:])` starts after Ethernet's 14 bytes, so it reads the same packet from IPv4 up.
- The dissected object holds every computed field: the IPv4 length 37 and its checksum.
- Ethernet will not carry a frame shorter than 60 bytes, so a short packet arrives followed by zero bytes.
  IPv4's total length says where the packet ends, and Scapy keeps the bytes after it as a **`Padding`** layer, apart from the data.
- Bytes that no class is bound to stay **`Raw`**: the UDP data in *Four views* above is `Raw`, because no class is bound to port 9999.

## Common mistakes

```python
"""read_mistakes.py: three readings that look right and are not"""
from scapy.all import IP, UDP, Raw, raw

datagram = IP(src="10.10.3.1", dst="10.10.3.10") / UDP(sport=33333, dport=9999) / b"ref-data"
print('load == "ref-data":', datagram[Raw].load == "ref-data", '| load == b"ref-data":', datagram[Raw].load == b"ref-data")
print('dport == "9999":', datagram[UDP].dport == "9999", "| dport == 9999:", datagram[UDP].dport == 9999)
print("len before the build:", datagram[IP].len, "| len after it:", IP(raw(datagram)).len)
```

```
(.venv) $ python3 read_mistakes.py
load == "ref-data": False | load == b"ref-data": True
dport == "9999": False | dport == 9999: True
len before the build: None | len after it: 36
```

| Mistake | What happens | Instead |
|---|---|---|
| Comparing `Raw`'s `load` with a string | `load` is `bytes`, so `== "ref-data"` is always `False` | compare with `b"ref-data"` |
| Comparing a port with a string | a port is an `int`, so `== "9999"` is always `False` | compare with `9999`, or convert the argument with `int()` |
| Reading a computed field from the object | the object holds `None` until it is built | read it from `show2()`, or from the dissected bytes |

---

# Sending

Every Scapy send opens a packet socket, and the kernel opens one only for a process that holds `CAP_NET_RAW`.
So every program from here on runs as `sudo .venv/bin/python`, from the working folder.

## Route and MAC lookups: `conf.route` and `getmacbyip`

Before Scapy writes the Ethernet header for a packet you give it from IPv4 up, it runs two lookups of its own: the route, then the MAC address of the next hop.

```python
"""route_demo.py: Scapy's routing table, and the lookups send() runs before it writes a frame"""
import time

from scapy.all import IP, conf, getmacbyip

print(conf.route)
print("route to 10.10.3.10:", conf.route.route("10.10.3.10"))
print("route to 192.0.2.1: ", conf.route.route("192.0.2.1"))
print("IP(dst='10.10.3.10').route():", IP(dst="10.10.3.10").route())
for attempt in ("first", "second"):
    start = time.monotonic()
    target_mac = getmacbyip("10.10.3.10")
    print(f"{attempt} getmacbyip('10.10.3.10'): {target_mac} after {time.monotonic() - start:.3f} s")
```

```
(.venv) $ sudo .venv/bin/python route_demo.py
Network          Netmask          Gateway   Iface     Output IP       Metric
0.0.0.0          0.0.0.0          10.0.2.2  eth0      10.0.2.15       100   
10.0.2.0         255.255.255.0    0.0.0.0   eth0      10.0.2.15       100   
10.0.2.15        255.255.255.255  0.0.0.0   eth0      10.0.2.15       0     
10.0.2.255       255.255.255.255  0.0.0.0   eth0      10.0.2.15       0     
10.10.3.0        255.255.255.0    0.0.0.0   m1s3-lab  10.10.3.1       0     
10.10.3.1        255.255.255.255  0.0.0.0   m1s3-lab  10.10.3.1       0     
10.10.3.255      255.255.255.255  0.0.0.0   m1s3-lab  10.10.3.1       0     
127.0.0.0        255.0.0.0        0.0.0.0   lo        127.0.0.1       0     
127.0.0.1        255.255.255.255  0.0.0.0   lo        127.0.0.1       0     
127.255.255.255  255.255.255.255  0.0.0.0   lo        127.0.0.1       0     
172.17.0.0       255.255.0.0      0.0.0.0   docker0   172.17.0.1      0     
172.17.0.1       255.255.255.255  0.0.0.0   docker0   172.17.0.1      0     
172.17.255.255   255.255.255.255  0.0.0.0   docker0   172.17.0.1      0     
192.168.56.0     255.255.255.0    0.0.0.0   eth1      192.168.56.107  101   
192.168.56.107   255.255.255.255  0.0.0.0   eth1      192.168.56.107  0     
192.168.56.255   255.255.255.255  0.0.0.0   eth1      192.168.56.107  0     
224.0.0.0        240.0.0.0        0.0.0.0   eth0      10.0.2.15       250   
224.0.0.0        240.0.0.0        0.0.0.0   eth1      192.168.56.107  250   
224.0.0.0        240.0.0.0        0.0.0.0   docker0   172.17.0.1      250   
224.0.0.0        240.0.0.0        0.0.0.0   m1s3-lab  10.10.3.1       250   
route to 10.10.3.10: ('m1s3-lab', '10.10.3.1', '0.0.0.0')
route to 192.0.2.1:  ('eth0', '10.0.2.15', '10.0.2.2')
IP(dst='10.10.3.10').route(): ('m1s3-lab', '10.10.3.1', '0.0.0.0')
first getmacbyip('10.10.3.10'): 02:42:0a:0a:03:0a after 0.044 s
second getmacbyip('10.10.3.10'): 02:42:0a:0a:03:0a after 0.000 s
```

| Call | Returns |
|---|---|
| `conf.route` | Scapy's routing table, a copy of the kernel's, read when Scapy starts |
| `conf.route.route(address)` | `(interface, source address, gateway)`, where the gateway `0.0.0.0` means the address is on the link |
| `packet.route()` | the same, for the packet's own destination |
| `getmacbyip(address)` | the MAC address of the next hop toward the address, or `None` when no host answers |

- The target is on the link through `m1s3-lab`, and Kali's own address there, `10.10.3.1`, is the source of every packet sent to it.
- `192.0.2.1`, an address reserved for documentation, is off the link: its route leaves by `eth0` through the gateway `10.0.2.2`, so its next hop is the gateway.
- `getmacbyip` asks the link for the MAC address with a request Scapy sends itself, not the kernel's.
  That request belongs to a protocol of its own, taught in a later session.
  Scapy keeps each answer for 120 seconds, which is why the second lookup took no time.
- A route added to the kernel after Scapy started is used only after `conf.route.resync()`.

## `send` and `sendp`

```python
"""send_demo.py: one echo request at layer 3, the same inside a frame at layer 2, then quietly"""
from scapy.all import Ether, IP, ICMP, conf, send, sendp

echo_request = IP(dst="10.10.3.10") / ICMP(id=0x0b0b, seq=5) / b"reference"
print("send:")
returned = send(echo_request)
print("send returned", returned)
print("sendp:")
sendp(Ether(dst="02:42:0a:0a:03:0a") / echo_request, iface="m1s3-lab")
print("send with count=3 and inter=0.5:")
send(echo_request, count=3, inter=0.5)
conf.verb = 0
send(echo_request)
print("with conf.verb = 0, send printed nothing")
```

```
(.venv) $ sudo .venv/bin/python send_demo.py
send:
.
Sent 1 packets.
send returned None
sendp:
.
Sent 1 packets.
send with count=3 and inter=0.5:
...
Sent 3 packets.
with conf.verb = 0, send printed nothing
```

| Call | What it does |
|---|---|
| `send(packet)` | **layer-3 send**: takes the packet from IPv4 up, picks the interface from `conf.route`, writes the Ethernet header from the MAC lookup, and sends |
| `sendp(frame, iface="m1s3-lab")` | **layer-2 send**: takes the frame from Ethernet up and sends it on the interface named, adding no layer |
| `count=3` | sends the packet that many times |
| `inter=0.5` | waits that many seconds after each send |
| a list of packets | sends each one in turn |
| `conf.verb = 0` | turns off Scapy's progress lines, so a program prints only its own |

- Each dot is one packet sent, and `Sent N packets.` ends the call.
- `send` returns `None`: it reports nothing about replies.
  Catching a reply needs the send-and-receive calls below.
- `sendp` here set only the Ethernet destination, the target's MAC, and Scapy filled the source from the interface.

---

# Send and Receive

A probe learns something only from its reply.
The **send-and-receive** calls send, wait, and match each received packet against the requests: a reply's addresses are the request's reversed, and an echo reply repeats the request's identifier and sequence number.

## `sr`: answered pairs and unanswered requests

```python
"""sr_demo.py: two requests, the answered pairs and the unanswered list"""
from scapy.all import IP, ICMP, sr

echo_requests = [IP(dst="10.10.3.10") / ICMP(id=0x0b0b, seq=n) / b"reference" for n in (5, 6)]
answered, unanswered = sr(echo_requests, timeout=2, inter=0.2)
print(answered, unanswered)
for sent_request, reply in answered:
    print(f"request seq {sent_request[ICMP].seq}: reply from {reply[IP].src}, type {reply[ICMP].type},"
          f" id {hex(reply[ICMP].id)}, seq {reply[ICMP].seq}")
first_pair = answered[0]
print("answered[0] is a", type(first_pair).__name__, "| query seq", first_pair.query[ICMP].seq,
      "| answer seq", first_pair.answer[ICMP].seq)
print("sent apart:", round(answered[1].query.sent_time - answered[0].query.sent_time, 2), "s")
```

```
(.venv) $ sudo .venv/bin/python sr_demo.py
Begin emission
.**
Finished sending 2 packets

Received 3 packets, got 2 answers, remaining 0 packets
<Results: TCP:0 UDP:0 ICMP:2 Other:0> <Unanswered: TCP:0 UDP:0 ICMP:0 Other:0>
request seq 5: reply from 10.10.3.10, type 0, id 0xb0b, seq 5
request seq 6: reply from 10.10.3.10, type 0, id 0xb0b, seq 6
answered[0] is a QueryAnswer | query seq 5 | answer seq 5
sent apart: 0.2 s
```

- `Begin emission` and `Finished sending 2 packets` frame the sends.
  Each `*` is a received packet that answers a request, and each `.` is a received packet that answers none.
- The `.` here is the answer to Scapy's own MAC lookup, which a new process runs before its first send: it was received and matched to nothing, so `Received 3 packets` counts it.
- `sr` returns two lists: the **answered** pairs and the **unanswered** requests, and their names in angle brackets count each by protocol.
- Each answered pair is a `QueryAnswer`: unpack it as `for sent_request, reply in answered`, or read `.query` and `.answer`.
- `inter=0.2` spaced the two sends by 0.2 s, as each sent request's `sent_time` shows.

## `sr1`, `answers()`, `timeout` and `retry`

```python
"""sr1_demo.py: one answer, the match it passed, and no answer at all"""
import time

from scapy.all import IP, ICMP, Raw, conf, sr1

conf.verb = 0
echo_request = IP(dst="10.10.3.10") / ICMP(id=0x0b0b, seq=5) / b"reference"
reply = sr1(echo_request, timeout=2)
print("reply:", reply[IP].src, ">", reply[IP].dst, "| type", reply[ICMP].type, "| id", hex(reply[ICMP].id),
      "| seq", reply[ICMP].seq, "|", reply[Raw].load)
print("reply.answers(echo_request):", reply.answers(echo_request))
print("echo_request.answers(reply):", echo_request.answers(reply))

silent_request = IP(dst="10.10.3.99") / ICMP(id=0x0b0b, seq=5) / b"reference"
for retry in (0, 1):
    start = time.monotonic()
    reply = sr1(silent_request, timeout=1, retry=retry)
    print(f"timeout=1, retry={retry}: {reply} after {time.monotonic() - start:.2f} s")
```

```
(.venv) $ sudo .venv/bin/python sr1_demo.py
reply: 10.10.3.10 > 10.10.3.1 | type 0 | id 0xb0b | seq 5 | b'reference'
reply.answers(echo_request): 1
echo_request.answers(reply): 0
WARNING: MAC address to reach destination not found. Using broadcast.
timeout=1, retry=0: None after 3.07 s
WARNING: MAC address to reach destination not found. Using broadcast.
WARNING: MAC address to reach destination not found. Using broadcast.
timeout=1, retry=1: None after 6.10 s
```

| Call or argument | What it does |
|---|---|
| `sr1(packet, timeout=2)` | the same exchange as `sr`, returning only the **first answer**, or `None` when nothing answered |
| `reply.answers(request)` | runs the match on two packets: 1 when `reply` answers `request`, 0 otherwise |
| `timeout=1` | how long to wait after the last send, in seconds |
| `retry=1` | sends each unanswered request that many more times, one round after another |

- `answers` has a direction: the reply answers the request, and the request answers nothing.
- `10.10.3.99` is on the lab link, and no host holds it.
  Scapy's MAC lookup waits 2 s for an answer, prints the `WARNING`, and sends the request to the broadcast address.
  Then `sr1` waits its 1 s timeout, so one round took about 3 s, and `retry=1` paid for a second round.
- Without `timeout`, a request that nothing answers is waited for until you press **Ctrl+C**: always set one.
- `sr1` returns `None` for no answer, so check `if reply is None` before reading a field from it.

## `srp` and `srp1`: the same exchange at layer 2

```python
"""srp_demo.py: the same exchange at layer 2, in a frame you build"""
from scapy.all import Ether, IP, ICMP, conf, srp, srp1

conf.verb = 0
request_frame = Ether(dst="02:42:0a:0a:03:0a") / IP(dst="10.10.3.10") / ICMP(id=0x0b0b, seq=5) / b"reference"
reply_frame = srp1(request_frame, iface="m1s3-lab", timeout=2)
print("reply from MAC", reply_frame[Ether].src, "| Ether in reply_frame:", Ether in reply_frame,
      "| seq", reply_frame[ICMP].seq)
print("reply_frame.answers(request_frame):", reply_frame.answers(request_frame))
answered, unanswered = srp(request_frame, iface="m1s3-lab", timeout=2)
print(answered, unanswered)
```

```
(.venv) $ sudo .venv/bin/python srp_demo.py
reply from MAC 02:42:0a:0a:03:0a | Ether in reply_frame: True | seq 5
reply_frame.answers(request_frame): 1
<Results: TCP:0 UDP:0 ICMP:1 Other:0> <Unanswered: TCP:0 UDP:0 ICMP:0 Other:0>
```

- `srp` and `srp1` take the frame from Ethernet up and the interface by name, as `sendp` does, and return replies from Ethernet up.
- With the destination MAC set in the frame, Scapy runs no MAC lookup, so the frame goes out exactly as written.
- The reply keeps its Ethernet header, so its source MAC address can be read: here the target's.
  `sr` and `sr1` return a reply from IPv4 up.

---

# Capturing

**Capture** is reading the packets that cross an interface, including ones you did not send.
A capture makes four choices: the interface to listen on, the packets to keep, what to do with each one, and whether to store it.

## `sniff()`: `iface`, `filter`, `prn` and `timeout`

`sniff()` blocks until it is done, so the sender runs in a second terminal.

```python
"""sniff_demo.py: capture for 6 seconds, and print one line per packet the filter keeps"""
from scapy.all import IP, ICMP, sniff


def describe(packet):
    """Called on each kept packet: its return value is printed."""
    return f"{packet[IP].src} > {packet[IP].dst} id {packet[ICMP].id} seq {packet[ICMP].seq}"


print("capturing on m1s3-lab for 6 s")
packets = sniff(iface="m1s3-lab", filter="icmp and host 10.10.3.10", prn=describe, timeout=6)
print("sniff returned", packets)
print("packets[0] is a", type(packets[0]).__name__, "object, captured on", packets[0].sniffed_on)
```

```
(.venv) $ sudo .venv/bin/python sniff_demo.py   [first terminal]
(.venv) $ sudo .venv/bin/python -c "from scapy.all import IP, ICMP, conf, sr; conf.verb = 0; sr([IP(dst='10.10.3.10') / ICMP(id=0x0b0b, seq=n) / b'reference' for n in (5, 6)], timeout=2)"
[first terminal output]
capturing on m1s3-lab for 6 s
10.10.3.1 > 10.10.3.10 id 2827 seq 5
10.10.3.10 > 10.10.3.1 id 2827 seq 5
10.10.3.1 > 10.10.3.10 id 2827 seq 6
10.10.3.10 > 10.10.3.1 id 2827 seq 6
sniff returned <Sniffed: TCP:0 UDP:0 ICMP:4 Other:0>
packets[0] is a Ether object, captured on m1s3-lab
```

| Argument | What it does |
|---|---|
| `iface="m1s3-lab"` | the interface to listen on |
| `filter="icmp and host 10.10.3.10"` | a **BPF** expression: libpcap compiles it, and the kernel runs it, so a packet it drops never reaches Python |
| `lfilter=function` | a Python test called on every packet after it is dissected: the packet is kept when it returns `True` |
| `prn=function` | called on each kept packet, and its return value is printed when it is not `None` |
| `count=2` | stops after that many kept packets |
| `timeout=6` | stops after that many seconds |
| `store=False` | keeps nothing, so the list returned is empty |

- `sniff` returns the kept packets as a list of layer objects, each from Ethernet up, indexed as any packet is.
- Each packet records the interface it was captured on in `sniffed_on`.
- The sender sent two requests with `sr`, so the capture kept four packets: each request and its reply.
- `sniff` stops at `count` or `timeout`, whichever comes first, and with neither it waits until you press **Ctrl+C**.

## `lfilter`, `count` and `store=False`

```python
"""lfilter_demo.py: keep echo replies only with a Python test, stop after two, store nothing"""
from scapy.all import ICMP, sniff


def is_reply(packet):
    """Called on every captured packet: keep it when this returns True."""
    return ICMP in packet and packet[ICMP].type == 0


print("waiting for two echo replies")
kept = sniff(iface="m1s3-lab", lfilter=is_reply, count=2, store=False,
             prn=lambda packet: f"reply seq {packet[ICMP].seq}")
print("sniff returned", kept)
```

```
(.venv) $ sudo .venv/bin/python lfilter_demo.py   [first terminal]
(.venv) $ sudo .venv/bin/python -c "from scapy.all import IP, ICMP, conf, sr; conf.verb = 0; sr([IP(dst='10.10.3.10') / ICMP(id=0x0b0b, seq=n) / b'reference' for n in (5, 6)], timeout=2)"
[first terminal output]
waiting for two echo replies
reply seq 5
reply seq 6
sniff returned <Sniffed: TCP:0 UDP:0 ICMP:0 Other:0>
```

- `is_reply` kept only echo replies, type 0, so `count=2` stopped the capture at the second reply.
- `prn` still printed each kept packet, and `store=False` left the returned list empty.
- An `lfilter` can test anything Scapy dissects, but every packet on the interface reaches Python first.
  A `filter` drops packets in the kernel, before Python does any work.

## `AsyncSniffer`, with `threading.Event` and `time.monotonic()`

`AsyncSniffer` runs the same capture in a thread, so the program that captures can also send.

```python
"""async_demo.py: capture in a thread while the same program sends, then wait for it to end"""
import threading
import time

from scapy.all import IP, ICMP, AsyncSniffer, conf, sr

conf.verb = 0
sniffer_ready = threading.Event()
sniffer = AsyncSniffer(iface="m1s3-lab", filter="icmp and host 10.10.3.10", count=4,
                       started_callback=sniffer_ready.set)
start = time.monotonic()
sniffer.start()
print("start() returned, socket open:", sniffer_ready.is_set())
sniffer_ready.wait()
print(f"socket open after {time.monotonic() - start:.3f} s")
sr([IP(dst="10.10.3.10") / ICMP(id=0x0b0b, seq=n) / b"reference" for n in (5, 6)], timeout=2)
sniffer.join(timeout=5)
print("running:", sniffer.running, "| results:", sniffer.results)
```

```
(.venv) $ sudo .venv/bin/python async_demo.py
start() returned, socket open: False
socket open after 0.018 s
running: False | results: <Sniffed: TCP:0 UDP:0 ICMP:4 Other:0>
```

| Call | What it does |
|---|---|
| `AsyncSniffer(...)` | takes `sniff`'s arguments, except `timeout` |
| `started_callback=function` | called once the capture's socket is open |
| `.start()` | starts the capture in a thread, and returns at once |
| `.join(timeout=5)` | waits for the capture to end on its own (`count` reached), at most that many seconds |
| `.stop()` | ends a capture that is still running, and returns the list of kept packets |
| `.running`, `.results` | whether the capture is still running, and the list it kept |
| `threading.Event()` | a flag one thread sets with `.set()` and another waits for with `.wait()`, or reads with `.is_set()` |
| `time.monotonic()` | seconds from a clock that never goes back, for measuring how long something took |

- `start()` returned before the socket was open: the flag read `False`.
  A program that sends at that moment can miss its own packets, so it waits for `started_callback` first.
- Here `count=4` ended the capture by itself, so `join` was the right call.
  A capture with no `count` keeps running, and `stop()` ends it and returns the list.
- `stop()` on a capture that has already ended raises an exception, so call one of the two, not both.

## pcap files: `wrpcap` and `rdpcap`

A **pcap** file stores a capture as the bytes that crossed the wire, with the time of each packet, in a format every capture tool reads.

```python
"""pcap_demo.py: capture one exchange, save it as a pcap file, and read it back"""
import threading

from scapy.all import IP, ICMP, AsyncSniffer, conf, raw, rdpcap, sr1, wrpcap

conf.verb = 0
sniffer_ready = threading.Event()
sniffer = AsyncSniffer(iface="m1s3-lab", filter="icmp and host 10.10.3.10", started_callback=sniffer_ready.set)
sniffer.start()
sniffer_ready.wait()
sr1(IP(dst="10.10.3.10") / ICMP(id=0x0b0b, seq=5) / b"reference", timeout=2)
exchange = sniffer.stop()
wrpcap("ref_echo.pcap", exchange)
read_back = rdpcap("ref_echo.pcap")
print("captured: ", exchange)
print("read back:", read_back)
print("same bytes:", [raw(captured) == raw(loaded) for captured, loaded in zip(exchange, read_back)])
print("time:", exchange[0].time, "->", read_back[0].time)
```

```
(.venv) $ sudo .venv/bin/python pcap_demo.py
captured:  <Sniffed: TCP:0 UDP:0 ICMP:2 Other:0>
read back: <ref_echo.pcap: TCP:0 UDP:0 ICMP:2 Other:0>
same bytes: [True, True]
time: 1794241162.4372044 -> 1794241162.437204
(.venv) $ ls -l ref_echo.pcap
-rw-r----- 1 root root 158 Nov  9 11:19 ref_echo.pcap
(.venv) $ sudo tcpdump -r ref_echo.pcap -nn
reading from file ref_echo.pcap, link-type EN10MB (Ethernet), snapshot length 65535
11:19:22.437204 IP 10.10.3.1 > 10.10.3.10: ICMP echo request, id 2827, seq 5, length 17
11:19:22.437238 IP 10.10.3.10 > 10.10.3.1: ICMP echo reply, id 2827, seq 5, length 17
```

| Call | What it does |
|---|---|
| `wrpcap("file.pcap", packets)` | writes a list of packets to a pcap file |
| `rdpcap("file.pcap")` | reads it back as a list of layer objects, named after the file |
| `packet.time` | the time the packet was captured, in seconds since 1970 |

- The file is 158 bytes: a 24-byte header, then each 51-byte frame behind a 16-byte record of its time and length.
- The bytes come back identical, and the time comes back to the microsecond: the file stores no finer.
- The program ran under `sudo`, so the file belongs to root, and your own user cannot read it.
  That is why `tcpdump` reads it under `sudo` too.

## Common mistakes

| Mistake | What happens | Instead |
|---|---|---|
| Sending at once after `AsyncSniffer.start()` | the capture can miss the packets the program sends | wait for `started_callback` with a `threading.Event` |
| `AsyncSniffer(..., timeout=5)` | `ValueError`: it takes no `timeout` | `.join(timeout=5)`, or `.stop()` |
| `sniff(count=2)` while nothing is sent | it waits forever, because `count` is never reached | give it a `timeout` too |
| Capturing on `lo` | every packet is captured twice | capture on the lab's bridge, `m1s3-lab` |

The **Troubleshooting FAQ** shows each of these as it fails, with its exact message.

---

# Command-Line Tools

Four commands run the lab and read what it carried.

## `docker compose`: `ps`, `down` and `up -d`

`docker compose` reads `compose.yaml` in the current folder, so run it in `lab/`.

```
(.venv) $ cd lab
(.venv) $ docker compose ps
NAME            IMAGE         COMMAND            SERVICE   CREATED              STATUS              PORTS
m1s3-target-1   alpine:3.24   "sleep infinity"   target    About a minute ago   Up About a minute   
(.venv) $ docker compose down
 Container m1s3-target-1  Stopping
 Container m1s3-target-1  Stopped
 Container m1s3-target-1  Removing
 Container m1s3-target-1  Removed
 Network m1s3_lab  Removing
 Network m1s3_lab  Removed
(.venv) $ docker compose up -d
 Network m1s3_lab  Creating
 Network m1s3_lab  Created
 Container m1s3-target-1  Creating
 Container m1s3-target-1  Created
 Container m1s3-target-1  Starting
 Container m1s3-target-1  Started
(.venv) $ docker compose ps
NAME            IMAGE         COMMAND            SERVICE   CREATED        STATUS                  PORTS
m1s3-target-1   alpine:3.24   "sleep infinity"   target    1 second ago   Up Less than a second   
(.venv) $ cd ..
```

| Command | What it does |
|---|---|
| `docker compose ps` | lists the project's running containers and their status |
| `docker compose ps -a` | lists them all, stopped ones included |
| `docker compose down` | stops and removes the container and the lab network |
| `docker compose up -d` | creates the network and the container if they are missing, and starts them in the background (`-d`, detached) |

- `down` removed the bridge `m1s3-lab` too, and `up -d` made a new one, with a new MAC address of its own.
  The target's addresses come from the compose file, so they never change.
- The compose file sets no restart policy, so after Kali restarts the target stays stopped until `docker compose up -d`.

## `ip -br addr`: the machine's addresses

```
(.venv) $ ip -br -4 addr
lo               UNKNOWN        127.0.0.1/8 
eth0             UP             10.0.2.15/24 
eth1             UP             192.168.56.107/24 
docker0          DOWN           172.17.0.1/16 
m1s3-lab         UP             10.10.3.1/24 
(.venv) $ ip -br -4 addr show m1s3-lab
m1s3-lab         UP             10.10.3.1/24 
```

- `-br` prints one line per interface: its name, its state and its addresses with their prefix lengths, and `-4` keeps IPv4 only.
- `show m1s3-lab` prints one interface.
  The lab's bridge must read `UP` with `10.10.3.1/24`.
- `docker0` is Docker's default bridge, which the lab does not use.

## `ping`: is the target there?

```
(.venv) $ ping -c 2 10.10.3.10
PING 10.10.3.10 (10.10.3.10) 56(84) bytes of data.
64 bytes from 10.10.3.10: icmp_seq=1 ttl=64 time=0.080 ms
64 bytes from 10.10.3.10: icmp_seq=2 ttl=64 time=0.049 ms

--- 10.10.3.10 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1005ms
rtt min/avg/max/mdev = 0.049/0.064/0.080/0.015 ms
```

- `ping -c 2` sends two ICMP echo requests and stops, and prints each reply with its round-trip time.
- `2 received` means the target is up.
  Run it first whenever a Scapy program gets no reply, because it tells a lab that is down from a bug in the program.

## `tcpdump -r`: reading a pcap file

The `tcpdump` lines in *pcap files* above read the file Scapy wrote.

| Option | What it does |
|---|---|
| `-r file.pcap` | reads packets from the file instead of from an interface |
| `-n` | prints addresses and port numbers as numbers, never as names |
| `-nn` | `-n` given twice: on these files it printed exactly what `-n` prints |

- `reading from file ..., link-type EN10MB (Ethernet)` says the file holds Ethernet frames.
- Each line is one packet: its capture time, then what it carries.
  `length 17` is the ICMP message's length: its 8-byte header and the 9 bytes of `reference`.
- `id 2827` is the identifier `0x0b0b` in decimal.

---

# Beyond This Session

Three Scapy features sit next to this session's material.
Each one is a pointer to Scapy's documentation, so you know the name when you meet it.

## The `scapy` shell

The `scapy` command, installed in `.venv/bin`, opens an interactive session with every Scapy name already imported, so `IP`, `sr1` and `sniff` need no `import`.
Run it as `sudo .venv/bin/scapy` to send and capture from it.
Documentation: *Starting Scapy*, in [Scapy's usage guide](https://scapy.readthedocs.io/en/latest/usage.html).

## Large captures: `sniff(offline=...)` and `PcapReader`

`rdpcap` loads a whole file into memory at once.
`sniff(offline="file.pcap", ...)` reads a file with the same `filter`, `lfilter` and `prn` as a live capture, and `PcapReader("file.pcap")` returns one packet at a time, so a file larger than memory can still be read.
Documentation: *Importing and Exporting Data*, in [Scapy's usage guide](https://scapy.readthedocs.io/en/latest/usage.html), and `help(PcapReader)` after `from scapy.utils import PcapReader`.

## Values a field type cannot hold: `RawVal`

A value that a field's type cannot encode, such as a TTL of 300 in a one-byte field, is refused when the packet is built, and Scapy's error message names `RawVal`.
`RawVal` copies bytes into a field as they are, bypassing the field's type, so the packet no longer follows its specification.
It belongs with the attacks of later sessions, which build such packets on purpose.
Documentation: *Injecting bytes*, in [Scapy's usage guide](https://scapy.readthedocs.io/en/latest/usage.html).
