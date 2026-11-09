# Module 1 · Session 2 — Tooling Reference

## The Python Networking Stack

### Professional Training in Cybersecurity I

---

> [!note] What this document is for
> The session used each tool once, on the way to servers, clients, a TLS connection and a raw socket.
> **This is the fuller treatment**: every Python library, call and command-line tool the session used, each with what it is for, an example with its real output, and the mistakes it invites.
> Nothing here is required reading in order.
> Come to it when you need it.
>
> Everything is Python's standard library or a standard Kali command, with **nothing to install**.
> Every example is a small file followed by the command that runs it and what it printed, so you can save it in your session folder and see the same.
> The examples run on Kali alone, on its loopback address `127.0.0.1`, and use ports 9001 to 9010 and 9443, so they never collide with the session's own servers.
> Where an example needs two terminals, the line marked `[first terminal]` is the program started first, and its output follows under `[first terminal output]`.

> [!note] Recorded on Kali
> These examples were recorded on the lab's Kali with **Python 3.13.12**, **OpenSSL 3.6.3**, **netcat-traditional 1.10-50.1**, **iproute2 6.14.0**, **iptables 1.8.11**, **tcpdump 4.99.6** and **curl 8.20.0**.
> The lab that recorded them puts Kali at `192.168.56.107` and the peer at `192.168.56.1`, so those addresses appear in them.
> Your addresses are on CyberLab, `10.0.2.x`, and the ports the system picks, process IDs and dates differ on every run.

---

# The Session's Python Environment

The Practical Guide's setup creates `.venv` in your working folder.
Everything this session uses is in the standard library, so `.venv` installs nothing: it keeps this session's Python apart from every other session's.

## Which Python runs, with and without `sudo`

```
(.venv) $ which python3
/home/kali/cyberlabs/Module1-Network-Attacks-and-Defense/Session2/.venv/bin/python3
(.venv) $ python3 --version
Python 3.13.12
(.venv) $ python3 -c "import ssl; print(ssl.OPENSSL_VERSION)"
OpenSSL 3.6.3 9 Jun 2026
(.venv) $ sudo sh -c 'command -v python3; python3 --version'
/usr/bin/python3
Python 3.13.12
```

- `which` names the file the shell runs for a command, and inside the environment it is the environment's own `python3`.
- `ssl.OPENSSL_VERSION` names the OpenSSL library behind Python's `ssl` module, which is the TLS implementation every `ssl` example below uses.
- `sudo` runs one command as root, and it starts that command with a fresh, minimal environment.
  So `sudo python3` runs Kali's own `/usr/bin/python3`, not the one in `.venv`.
  For this session that changes nothing, because the raw-socket programs use only the standard library, which both interpreters have.
- The first `sudo` in a terminal asks for your Kali password, and later ones in the same terminal reuse it for a few minutes.

## A usage line and an exit status: `sys.exit`

Every program in this session checks its arguments first, and stops with a usage line when they are wrong:

```python
if len(sys.argv) != 2:
    sys.exit("usage: python3 tls_ref_client.py SERVER_NAME")
```

```
(.venv) $ python3 tls_ref_client.py
usage: python3 tls_ref_client.py SERVER_NAME
(.venv) $ echo $?
1
```

`sys.exit` with a string prints the string on the error stream and ends the program with **exit status** 1, which `echo $?` reads.
A run that ends normally has status 0.

---

# Socket Calls

A **socket** is an endpoint the kernel keeps for one program.
The program calls the socket's methods, and the kernel does the work underneath: TCP's handshake and retransmission, or UDP's single datagrams.

## A TCP server and client

```python
"""tcp_demo_server.py: accept one client, answer one message, then close"""
import socket

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listener:
    listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listener.bind(("127.0.0.1", 9001))
    listener.listen()
    print("listening on", listener.getsockname())
    conn, client_address = listener.accept()
    with conn:
        print("accepted", client_address)
        print("this end", conn.getsockname(), "other end", conn.getpeername())
        message = conn.recv(1024)
        print("received", message)
        conn.sendall(b"ECHO: " + message)
print("both sockets closed")
```

```python
"""tcp_demo_client.py: connect, send one message, print the reply"""
import socket

with socket.create_connection(("127.0.0.1", 9001)) as client_socket:
    print("this end", client_socket.getsockname(), "other end", client_socket.getpeername())
    client_socket.sendall("status?\n".encode())
    reply = client_socket.recv(1024)
    print("reply", reply)
    print("decoded", reply.decode().rstrip())
```

```
(.venv) $ python3 tcp_demo_server.py   [first terminal]
(.venv) $ python3 tcp_demo_client.py
this end ('127.0.0.1', 38236) other end ('127.0.0.1', 9001)
reply b'ECHO: status?\n'
decoded ECHO: status?
[first terminal output]
listening on ('127.0.0.1', 9001)
accepted ('127.0.0.1', 38236)
this end ('127.0.0.1', 9001) other end ('127.0.0.1', 38236)
received b'status?\n'
both sockets closed
```

| Call | What it does |
|---|---|
| `socket.socket(AF_INET, SOCK_STREAM)` | a new IPv4 TCP socket: `AF_INET` is the IPv4 address family, `SOCK_STREAM` a byte stream |
| `bind((host, port))` | claims the address and port for this socket |
| `listen()` | marks the socket as a server's, ready to accept connections |
| `accept()` | waits for a client, and returns a **new** socket for that one connection and the client's address |
| `connect((host, port))` | the client's side: performs the handshake |
| `socket.create_connection((host, port))` | makes a TCP socket and connects it, in one call |
| `getsockname()` | this socket's own address and port |
| `getpeername()` | the address and port at the other end of the connection |
| `fileno()` | the small integer the kernel uses to name the socket inside this process |

- The client's port, `38236`, was picked by the kernel: an **ephemeral port**.
  The server's `accept` reported the same number, because both ends describe the same connection.
- `with socket.socket(...) as listener:` closes the socket when the block ends, even when an exception ends it.
  The server's last line prints after both `with` blocks have closed their sockets.
- `accept` left the listener as it was, so a server that loops back to `accept` serves the next client on the same port.

> [!tip] Bytes at the boundary
> A socket carries **bytes**.
> Text is encoded on the way out (`"status?\n".encode()`) and decoded on the way in (`reply.decode()`).

## Binding: loopback or every interface

The address a server binds decides which of the machine's addresses reach it.

```python
"""bind_where.py: a loopback listener and a wildcard listener, reached two ways"""
import socket
import sys

own_address = sys.argv[1]
loopback = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
loopback.bind(("127.0.0.1", 9002))
loopback.listen()
wildcard = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
wildcard.bind(("0.0.0.0", 9003))
wildcard.listen()
print("listening on", loopback.getsockname(), "and", wildcard.getsockname())

for host in ("127.0.0.1", own_address):
    for port in (9002, 9003):
        try:
            with socket.create_connection((host, port), timeout=1.0):
                print(f"{host}:{port} connected")
        except OSError as error:
            print(f"{host}:{port} {type(error).__name__}, errno {error.errno}")
```

```
(.venv) $ python3 bind_where.py 192.168.56.107
listening on ('127.0.0.1', 9002) and ('0.0.0.0', 9003)
127.0.0.1:9002 connected
127.0.0.1:9003 connected
192.168.56.107:9002 ConnectionRefusedError, errno 111
192.168.56.107:9003 connected
```

- `127.0.0.1` is the **loopback** address: it never leaves the machine, so a socket bound to it answers only connections made from the same machine to `127.0.0.1`.
- `0.0.0.0` is the **wildcard** address: the socket listens on every address the machine has, loopback included.
- The same program reached its own LAN address `192.168.56.107` too, and only the wildcard listener answered there.
  A server that another machine must reach binds the wildcard, or the address of the interface that machine reaches.

## UDP: `sendto` and `recvfrom`

A datagram socket (`SOCK_DGRAM`) has no connection, so it has no `listen`, `accept` or `connect`.
Each `sendto` names its destination, and each `recvfrom` returns one datagram together with the address it came from.

```python
"""udp_demo.py: three sendto calls arrive as three recvfrom calls"""
import socket

receiver = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
receiver.bind(("127.0.0.1", 9004))
sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
for text in (b"alpha", b"bravo-bravo", b"c"):
    sender.sendto(text, ("127.0.0.1", 9004))
print("sender bound to", sender.getsockname(), "by its first sendto")
for _ in range(3):
    datagram, source = receiver.recvfrom(1024)
    print(len(datagram), "bytes", datagram, "from", source)
sender.close()
receiver.close()
```

```
(.venv) $ python3 udp_demo.py
sender bound to ('0.0.0.0', 44979) by its first sendto
5 bytes b'alpha' from ('127.0.0.1', 44979)
11 bytes b'bravo-bravo' from ('127.0.0.1', 44979)
1 bytes b'c' from ('127.0.0.1', 44979)
```

- Each `recvfrom` returned exactly one datagram, whatever its size, so the boundaries the sender made are the boundaries that arrived.
- The sender never called `bind`: its first `sendto` bound it to the wildcard address and an ephemeral port.
- `recvfrom(1024)` reads at most 1024 bytes of one datagram, and *The real length of a datagram* below shows what happens to the rest of a longer one.

---

# Sending and Receiving Bytes

A stream socket keeps the order of the bytes and nothing else: where one `send` ended is not recorded anywhere.
These calls are how a program moves bytes in and out, and how it learns that the other end has gone.

## `send`, `sendall`, `recv` and the empty read

```python
"""partial_recv.py: recv returns what has arrived, up to the size asked for"""
import socket

sender, receiver = socket.socketpair()
print("send returned", sender.send(b"stream-bytes"))
print("recv(4):  ", receiver.recv(4))
print("recv(100):", receiver.recv(100))
sender.sendall(b"last")
sender.close()
print("recv(100):", receiver.recv(100))
print("recv(100):", receiver.recv(100))
receiver.close()
```

```
(.venv) $ python3 partial_recv.py
send returned 12
recv(4):   b'stre'
recv(100): b'am-bytes'
recv(100): b'last'
recv(100): b''
```

| Call | Returns |
|---|---|
| `send(data)` | how many bytes the kernel took, which can be fewer than `len(data)` |
| `sendall(data)` | `None`, after calling `send` until every byte is taken |
| `recv(n)` | **up to** `n` bytes, whatever has arrived, and `b''` once the other end has closed |

- `socket.socketpair()` gives two sockets already connected to each other, a quick way to try a call without a server.
- `recv(4)` returned 4 of the 12 bytes waiting, and the next `recv` returned the other 8: the stream kept the order, and the reads chose the pieces.
- `b''` is not an error.
  It is how `recv` says the other end has closed, so a receive loop ends on `b''`.
  The Practical Guide's given `framed_server.py` holds a complete `recv_exact`, the loop that reads exactly `n` bytes with these calls.

## The real length of a datagram: `recvmsg` and `MSG_TRUNC`

```python
"""trunc_calls.py: the real length of a datagram, and the flag that marks a cut one"""
import socket

receiver = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
receiver.bind(("127.0.0.1", 9004))
sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sender.sendto(b"A" * 20, ("127.0.0.1", 9004))
sender.sendto(b"B" * 6, ("127.0.0.1", 9004))

for _ in range(2):
    real_length = receiver.recv_into(bytearray(1), 1, socket.MSG_PEEK | socket.MSG_TRUNC)
    data, ancdata, msg_flags, address = receiver.recvmsg(8)
    print("peeked length", real_length, "| recvmsg kept", data, "| msg_flags", msg_flags,
          "| MSG_TRUNC bit", msg_flags & socket.MSG_TRUNC)
print("socket.MSG_TRUNC =", socket.MSG_TRUNC, "and socket.MSG_PEEK =", socket.MSG_PEEK)
sender.close()
receiver.close()
```

```
(.venv) $ python3 trunc_calls.py
peeked length 20 | recvmsg kept b'AAAAAAAA' | msg_flags 32 | MSG_TRUNC bit 32
peeked length 6 | recvmsg kept b'BBBBBB' | msg_flags 0 | MSG_TRUNC bit 0
socket.MSG_TRUNC = 32 and socket.MSG_PEEK = 2
```

| Call | Returns |
|---|---|
| `recv_into(buffer, nbytes, flags)` | reads into a `bytearray` you made, and returns a count |
| the flags `MSG_PEEK \| MSG_TRUNC` | leave the datagram in the queue, and make the count its **real** length, however small the buffer |
| `recvmsg(bufsize)` | a 4-tuple: the data, the ancillary data (none here), the message flags, and the sender's address |

- The 20-byte datagram did not fit the 8-byte buffer: `recvmsg` kept 8 bytes, discarded the other 12, and set the `MSG_TRUNC` bit, 32, in `msg_flags`.
- The 6-byte datagram fit, so its flags were 0.
- `msg_flags & socket.MSG_TRUNC` keeps that one bit: a bitwise AND with a **mask**, the same operation that reads a flag bit out of a header.

---

# Packing Fields: `struct` and Address Bytes

A protocol header is a run of fixed-size numbers.
`struct` turns Python numbers into those bytes and back, and the `socket` module converts addresses and port numbers into the form a header holds.

## `pack`, `unpack` and `calcsize`

```python
"""struct_demo.py: fixed-size fields in network byte order"""
import struct

prefix = struct.pack("!I", 300)
print("!I of 300:", prefix, prefix.hex(" "))
print("back:", struct.unpack("!I", prefix))
(length,) = struct.unpack("!I", prefix)
print("unpacked into one name:", length)

record_header = struct.pack("!BH", 7, 1000)
print("!BH of 7, 1000:", record_header.hex(" "))
for fmt in ("!I", "!BH", "!BBHHH"):
    print(f"calcsize({fmt!r}) = {struct.calcsize(fmt)}")

header = struct.pack("!BBHHH", 3, 1, 0, 0xABCD, 7)
kind, code, checksum, identifier, sequence = struct.unpack("!BBHHH", header)
print(header.hex(" "), "->", kind, code, checksum, hex(identifier), sequence)

word = "Zürich"
body = word.encode("utf-8")
print(repr(word), len(word), "characters,", len(body), "bytes:", body)
print("prefix for its bytes:", struct.pack("!I", len(body)).hex(" "))
```

```
(.venv) $ python3 struct_demo.py
!I of 300: b'\x00\x00\x01,' 00 00 01 2c
back: (300,)
unpacked into one name: 300
!BH of 7, 1000: 07 03 e8
calcsize('!I') = 4
calcsize('!BH') = 3
calcsize('!BBHHH') = 8
03 01 00 00 ab cd 00 07 -> 3 1 0 0xabcd 7
'Zürich' 6 characters, 7 bytes: b'Z\xc3\xbcrich'
prefix for its bytes: 00 00 00 07
```

| Code | Size | Meaning |
|---|---|---|
| `!` | none | network byte order, big-endian, with no padding between fields |
| `B` | 1 | an unsigned byte, 0 to 255 |
| `H` | 2 | an unsigned 16-bit number, 0 to 65,535 |
| `I` | 4 | an unsigned 32-bit number |
| `4s` | 4 | 4 bytes, copied as they are: an IPv4 address from `inet_aton` |

- `unpack` always returns a **tuple**, even for one field, so `(length,) = ...` unpacks the one value into a name.
- `calcsize` gives the byte count of a format, which is how a reader knows how many bytes to take before it unpacks.
- `0x012c` is 300, and its low byte `0x2c` is the character `,`, which is why the printed `bytes` end in `,`.
- `ü` takes 2 bytes in UTF-8, so a length prefix counts `len(body)`, the encoded bytes, never `len(word)`.

Module 1 Session 1's Tooling Reference has the full treatment of `struct`, byte order and the bit operations a header needs.

## Addresses and port numbers as bytes: `inet_aton`, `inet_ntoa` and `htons`

```python
"""addr_demo.py: addresses as text and as the 4 bytes a header holds"""
import socket

packed = socket.inet_aton("10.0.2.15")
print("inet_aton('10.0.2.15') =", packed, packed.hex(" "))
print("inet_ntoa(bytes.fromhex('c0a83801')) =", socket.inet_ntoa(bytes.fromhex("c0a83801")))
print("htons(0x0800) =", socket.htons(0x0800), "and ntohs(8) =", hex(socket.ntohs(8)))
```

```
(.venv) $ python3 addr_demo.py
inet_aton('10.0.2.15') = b'\n\x00\x02\x0f' 0a 00 02 0f
inet_ntoa(bytes.fromhex('c0a83801')) = 192.168.56.1
htons(0x0800) = 8 and ntohs(8) = 0x800
```

- `inet_aton` turns dotted text into the 4 bytes of an IPv4 address field, and `inet_ntoa` turns 4 bytes back into text.
- `htons` ("host to network, short") puts a 16-bit number into network byte order.
  Kali's processor is little-endian, so it swaps the two bytes: `0x0800` comes back as `0x0008`, printed `8`.
  On a big-endian machine it changes nothing, which is why code that needs network order calls it instead of swapping by hand.
- `AF_PACKET` takes its protocol number this way, as *Raw Sockets* below shows.

---

# Errors, Deadlines and Socket Options

A socket call that fails raises an exception, and the exception's class says which event happened.
A deadline turns a wait that could last forever into one more exception.

## The `OSError` family

```python
"""errors_demo.py: the socket exceptions are all OSError"""
import errno
import socket

for error_class in (ConnectionRefusedError, ConnectionResetError, TimeoutError, PermissionError):
    print(error_class.__name__, "is an OSError:", issubclass(error_class, OSError))
print("socket.timeout is TimeoutError:", socket.timeout is TimeoutError)
for number in (98, 104, 110, 111):
    print(number, errno.errorcode[number])
```

```
(.venv) $ python3 errors_demo.py
ConnectionRefusedError is an OSError: True
ConnectionResetError is an OSError: True
TimeoutError is an OSError: True
PermissionError is an OSError: True
socket.timeout is TimeoutError: True
98 EADDRINUSE
104 ECONNRESET
110 ETIMEDOUT
111 ECONNREFUSED
```

- Every socket exception is a subclass of `OSError`, so `except OSError` catches all of them, and a more specific handler must come first (*Common mistakes* below).
- An exception from the kernel carries the kernel's error number in `.errno`, and `errno.errorcode` names it.
- `socket.timeout` is another name for `TimeoutError`, which older code still uses.

## Refused, reset and timed out

**Refused**: nothing listens on the port, so the other host answers the handshake with a reset at once.

```python
"""refused_demo.py: nothing listens on 9005"""
import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("127.0.0.1", 9005))
```

```
(.venv) $ python3 refused_demo.py
Traceback (most recent call last):
  File "/home/kali/cyberlabs/Module1-Network-Attacks-and-Defense/Session2/refused_demo.py", line 5, in <module>
    client_socket.connect(("127.0.0.1", 9005))
    ~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^
ConnectionRefusedError: [Errno 111] Connection refused
```

**Reset**: a connection that existed is aborted by the other end.

```python
"""reset_demo.py: a peer that aborts its connection, and what recv then raises"""
import socket
import struct

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listener:
    listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listener.bind(("127.0.0.1", 9010))
    listener.listen()
    client_socket = socket.create_connection(("127.0.0.1", 9010))
    conn, _ = listener.accept()
    # Linger on, with a time of 0: close() aborts with a reset instead of a normal close.
    conn.setsockopt(socket.SOL_SOCKET, socket.SO_LINGER, struct.pack("ii", 1, 0))
    conn.close()
    try:
        client_socket.recv(1024)
    except ConnectionResetError as error:
        print(f"{type(error).__name__}: {error}")
    client_socket.close()
```

```
(.venv) $ python3 reset_demo.py
ConnectionResetError: [Errno 104] Connection reset by peer
```

A normal close makes the next `recv` return `b''`.
An abort sends a reset instead, and the next `recv` raises `ConnectionResetError`, so the reader knows the stream was cut, not finished.

**Timed out**: no answer at all, until a deadline passes.
The next section shows the deadline, and *`iptables`* under *Command-Line Tools* shows a timeout on a real connection attempt.

## `settimeout`: a deadline on every blocking call

```python
"""timeout_demo.py: a deadline on a recv that nothing will answer"""
import socket
import time

quiet, listening = socket.socketpair()
print("timeout before:", listening.gettimeout())
listening.settimeout(1.5)
print("timeout after: ", listening.gettimeout())
start = time.perf_counter()
try:
    listening.recv(1024)
except TimeoutError as error:
    elapsed = time.perf_counter() - start
    print(f"{type(error).__name__}: {error}, errno {error.errno}, after {elapsed:.2f} s")
```

```
(.venv) $ python3 timeout_demo.py
timeout before: None
timeout after:  1.5
TimeoutError: timed out, errno None, after 1.50 s
```

- A new socket's timeout is `None`: every blocking call waits as long as it takes.
- `settimeout(1.5)` gives **every** blocking call on that socket, `connect`, `accept`, `recv` and `send` alike, a deadline of 1.5 seconds.
- `TimeoutError` comes from Python's own clock, not from the kernel, so its `errno` is `None`.
- `time.perf_counter()` is a clock meant for measuring intervals: subtract two readings to get the seconds between them.
- `socket.create_connection((host, port), timeout=1.0)` sets the same deadline on the socket it makes.

## Socket options: `setsockopt` and `getsockopt`

A **socket option** is a per-socket setting the kernel reads.
Each one is named by a level and an option name.

```python
"""reuse_demo.py: read a socket option, set it, read it again"""
import socket

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listener:
    print("SO_REUSEADDR before:", listener.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR))
    listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print("SO_REUSEADDR after: ", listener.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR))
```

```
(.venv) $ python3 reuse_demo.py
SO_REUSEADDR before: 0
SO_REUSEADDR after:  1
```

| Level, option | Used for |
|---|---|
| `SOL_SOCKET, SO_REUSEADDR` | a listener that may bind its port while old connections on it are still in `TIME_WAIT` |
| `SOL_SOCKET, SO_LINGER` | how `close` ends a connection: `reset_demo.py` above sets it to abort |
| `IPPROTO_IP, IP_HDRINCL` | a raw socket whose sends start with an IPv4 header the program wrote (*Raw Sockets* below) |

An option is set **before** the call it changes: `SO_REUSEADDR` before `bind`.

## Common mistakes

**A general handler above a specific one:**

```python
"""order_mistake.py: the general handler first catches everything below it"""
import socket

try:
    socket.create_connection(("127.0.0.1", 9005), timeout=1.0)
except OSError as error:
    print("OSError handler ran, for", type(error).__name__)
except ConnectionRefusedError:
    print("refused handler ran")
```

```
(.venv) $ python3 order_mistake.py
OSError handler ran, for ConnectionRefusedError
```

Python tries the `except` clauses from the top and runs the first one that matches.
`ConnectionRefusedError` is an `OSError`, so the first clause matched and the second can never run.
Put the specific handlers first and `except OSError` last.

**Starting a second server on a port that is taken:**

```python
"""bind_twice.py: two sockets cannot listen on one port"""
import socket

first = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
first.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
first.bind(("127.0.0.1", 9002))
first.listen()
print("first socket listening on 9002")
second = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
second.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
second.bind(("127.0.0.1", 9002))
```

```
(.venv) $ python3 bind_twice.py
first socket listening on 9002
Traceback (most recent call last):
  File "/home/kali/cyberlabs/Module1-Network-Attacks-and-Defense/Session2/bind_twice.py", line 11, in <module>
    second.bind(("127.0.0.1", 9002))
    ~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^
OSError: [Errno 98] Address already in use
```

`SO_REUSEADDR` was on for both, and the bind still failed.
It lets a new listener bind past connections in `TIME_WAIT`, never past another socket that is still listening.
In practice the first socket is a server left running in another terminal, and `ss -tlnp` names its process (*Command-Line Tools* below, and the **Troubleshooting FAQ**).

---

# TLS: `ssl` and `openssl`

TLS wraps an ordinary TCP socket.
The program still sends and receives, but the bytes on the wire are encrypted, and the client checks the server's **certificate** before any data moves.

## A test certificate: `openssl req -x509` and `openssl x509`

```
(.venv) $ openssl req -x509 -newkey ec -pkeyopt ec_paramgen_curve:P-256 -noenc -days 3650 -subj "/CN=ref.lab" -addext "subjectAltName=DNS:ref.lab" -keyout ref.key -out ref.crt
-----
(.venv) $ openssl x509 -in ref.crt -noout -subject -issuer -ext subjectAltName -dates
subject=CN=ref.lab
issuer=CN=ref.lab
X509v3 Subject Alternative Name: 
    DNS:ref.lab
notBefore=Oct 28 18:17:09 2026 GMT
notAfter=Oct 25 18:17:09 2036 GMT
(.venv) $ ls -l ref.crt ref.key
-rw-rw-r-- 1 kali kali 599 Oct 28 14:17 ref.crt
-rw------- 1 kali kali 241 Oct 28 14:17 ref.key
```

| Option | Meaning |
|---|---|
| `req -x509` | make a certificate, not a request for one |
| `-newkey ec -pkeyopt ec_paramgen_curve:P-256` | also make a new elliptic-curve key on the P-256 curve (the Practical Guide's `-newkey rsa:2048` makes an RSA key instead) |
| `-noenc` | leave the key unencrypted, so a server can load it without a password (`-nodes` is the older name) |
| `-days 3650` | valid for ten years from now |
| `-subj "/CN=ref.lab"` | the certificate's subject name, given on the command line so `openssl` asks no questions |
| `-addext "subjectAltName=DNS:ref.lab"` | the name a client checks, in the subject alternative name extension |
| `-keyout ref.key -out ref.crt` | where the key and the certificate are written |
| `x509 -noout -subject -issuer -ext subjectAltName -dates` | print those fields of a certificate, and not the certificate itself |

- `-----` is all `openssl req` prints when it succeeds with `-subj`: it is not an error.
- `subject` and `issuer` are the same name, which is what **self-signed** means: the certificate vouches for itself.
- `ref.key` is readable by its owner only, because whoever holds it can be the server.

## Wrapping a socket: `SSLContext` and `wrap_socket`

```python
"""tls_ref_server.py: present ref.crt to each client, and answer one message"""
import socket
import ssl

server_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
server_context.load_cert_chain("ref.crt", "ref.key")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listener:
    listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listener.bind(("127.0.0.1", 9443))
    listener.listen()
    print("TLS server on", listener.getsockname())
    while True:
        conn, client_address = listener.accept()
        try:
            with server_context.wrap_socket(conn, server_side=True) as tls_conn:
                print(client_address, "handshake done:", tls_conn.version())
                tls_conn.sendall(b"SECURE-ECHO: " + tls_conn.recv(1024))
        except (ssl.SSLError, ConnectionError) as error:
            print(client_address, "handshake failed:", error)
            conn.close()
```

```python
"""tls_ref_client.py: check the server's certificate against ref.crt and a name"""
import socket
import ssl
import sys

if len(sys.argv) != 2:
    sys.exit("usage: python3 tls_ref_client.py SERVER_NAME")
server_name = sys.argv[1]

client_context = ssl.create_default_context(cafile="ref.crt")
print("verify_mode", client_context.verify_mode, "check_hostname", client_context.check_hostname)
with socket.create_connection(("127.0.0.1", 9443)) as client_socket:
    try:
        tls_socket = client_context.wrap_socket(client_socket, server_hostname=server_name)
    except ssl.SSLCertVerificationError as error:
        print("verify_code", error.verify_code)
        print("verify_message", repr(error.verify_message))
        sys.exit(1)
    with tls_socket:
        print("version:", tls_socket.version())
        print("cipher: ", tls_socket.cipher())
        print("subjectAltName:", tls_socket.getpeercert()["subjectAltName"])
        tls_socket.sendall(b"hello over TLS")
        print(tls_socket.recv(1024))
```

With the server running in the first terminal:

```
(.venv) $ python3 tls_ref_client.py ref.lab
verify_mode 2 check_hostname True
version: TLSv1.3
cipher:  ('TLS_AES_256_GCM_SHA384', 'TLSv1.3', 256)
subjectAltName: (('DNS', 'ref.lab'),)
b'SECURE-ECHO: hello over TLS'
```

| Call | What it does |
|---|---|
| `ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)` | the server's settings |
| `load_cert_chain(certfile, keyfile)` | the certificate the server presents, and its private key |
| `wrap_socket(conn, server_side=True)` | runs the handshake as the server on an **accepted** socket, and returns the TLS socket |
| `ssl.create_default_context(cafile=...)` | the client's settings, with both checks on, trusting the certificates in the file |
| `wrap_socket(sock, server_hostname=...)` | runs the handshake as the client, and checks the certificate against that name |
| `version()`, `cipher()` | the protocol the two ends agreed on, and the cipher suite as `(name, protocol, secret bits)` |
| `getpeercert()` | the server's certificate as a dictionary, after it has been verified |

- `verify_mode 2` is `ssl.CERT_REQUIRED`: the **trust** check, the certificate must trace to a certificate in `cafile`.
  `check_hostname True` is the **name** check, the certificate's `subjectAltName` must match `server_hostname`.
- After the wrap, `sendall` and `recv` work exactly as on a plain socket.
- The server wraps each accepted connection, never the listener: every client gets its own handshake.

## When verification fails: `verify_code` and `verify_message`

A failed check raises `ssl.SSLCertVerificationError` during `wrap_socket`, before any data moves.
The exception carries OpenSSL's verdict in two attributes.
This run passes the address as the server name:

```
(.venv) $ python3 tls_ref_client.py 127.0.0.1
verify_mode 2 check_hostname True
verify_code 64
verify_message "IP address mismatch, certificate is not valid for '127.0.0.1'."
```

- `verify_code` is OpenSSL's error number, and `verify_message` its text: the reason that follows `certificate verify failed:` in the exception's message.
- The client connects to an address, but it checks the **name** in `server_hostname`.
  This certificate names `ref.lab`, so `server_hostname` must be `ref.lab`, whatever address the socket connected to.
- Leaving out `cafile` fails the trust check instead, with a reason of its own: the Practical Guide's Exercise 4 has you read it from your run.

The server's terminal shows every client in this section from its side: the two runs above, the `openssl s_client` run below, and the first of the *Common mistakes*:

```
[first terminal output]
TLS server on ('127.0.0.1', 9443)
('127.0.0.1', 51530) handshake done: TLSv1.3
('127.0.0.1', 51542) handshake failed: [SSL: SSLV3_ALERT_BAD_CERTIFICATE] ssl/tls alert bad certificate (_ssl.c:1033)
('127.0.0.1', 51556) handshake done: TLSv1.3
('127.0.0.1', 51570) handshake failed: [SSL: WRONG_VERSION_NUMBER] wrong version number (_ssl.c:1033)
```

A client that rejects the certificate tells the server why, with an **alert**, before it closes: here `bad certificate`, the alert this client sent for the failed name check.
The refusal protects the client, so the fix is always on the client's side.

## `openssl s_client`: a TLS client on the command line

`openssl s_client` connects, runs the handshake and prints what it negotiated, which checks a TLS server without writing any code.

```
(.venv) $ openssl s_client -brief -connect 127.0.0.1:9443 -servername ref.lab -CAfile ref.crt < /dev/null
Connecting to 127.0.0.1
CONNECTION ESTABLISHED
Protocol version: TLSv1.3
Ciphersuite: TLS_AES_256_GCM_SHA384
Peer certificate: CN=ref.lab
Hash used: SHA256
Signature type: ecdsa_secp256r1_sha256
Verification: OK
Negotiated TLS1.3 group: X25519MLKEM768
DONE
```

| Option | Meaning |
|---|---|
| `-connect HOST:PORT` | where to connect |
| `-servername NAME` | the name to ask for, sent in the ClientHello's `server_name` extension |
| `-noservername` | send no `server_name` extension at all |
| `-CAfile FILE` | trust the certificates in this file |
| `-brief` | print only the summary, not the certificate and the session details |
| `< /dev/null` | give it no input, so it closes as soon as the handshake is done |

`Verification: OK` means the certificate traced to `-CAfile`, the trust check.
Unlike Python's default context, `s_client` checks the name only when given `-verify_hostname NAME`, and when a check fails it still completes the handshake, printing `Verification error:` and the reason instead of `OK`.
So read that line, never only `CONNECTION ESTABLISHED`.
The Home Task's Task 1 points `s_client` at a program that never answers, and the **Troubleshooting FAQ** explains the error it then prints.

## Common mistakes

**A plain client pointed at a TLS server:**

```python
"""plain_to_tls.py: a plain client pointed at the TLS server"""
import socket

with socket.create_connection(("127.0.0.1", 9443)) as client_socket:
    client_socket.sendall(b"hello in the clear\n")
    print("reply:", client_socket.recv(1024))
```

```
(.venv) $ python3 plain_to_tls.py
Traceback (most recent call last):
  File "/home/kali/cyberlabs/Module1-Network-Attacks-and-Defense/Session2/plain_to_tls.py", line 6, in <module>
    print("reply:", client_socket.recv(1024))
                    ~~~~~~~~~~~~~~~~~~^^^^^^
ConnectionResetError: [Errno 104] Connection reset by peer
```

The server read `hello in the clear` where a TLS record should start, and gave up with `WRONG_VERSION_NUMBER` (the server's last line above).
It closed the connection, and the client saw a reset.

**A TLS client pointed at a plain server**, here `tcp_demo_server.py` on 9001:

```python
"""tls_to_plain.py: a TLS client pointed at a server that does not speak TLS"""
import socket
import ssl

client_context = ssl.create_default_context(cafile="ref.crt")
with socket.create_connection(("127.0.0.1", 9001)) as client_socket:
    client_context.wrap_socket(client_socket, server_hostname="ref.lab")
```

```
(.venv) $ python3 tls_to_plain.py
Traceback (most recent call last):
  File "/home/kali/cyberlabs/Module1-Network-Attacks-and-Defense/Session2/tls_to_plain.py", line 7, in <module>
    client_context.wrap_socket(client_socket, server_hostname="ref.lab")
    ~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.13/ssl.py", line 455, in wrap_socket
    return self.sslsocket_class._create(
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        sock=sock,
        ^^^^^^^^^^
    ...<5 lines>...
        session=session
        ^^^^^^^^^^^^^^^
    )
    ^
  File "/usr/lib/python3.13/ssl.py", line 1076, in _create
    self.do_handshake()
    ~~~~~~~~~~~~~~~~~^^
  File "/usr/lib/python3.13/ssl.py", line 1372, in do_handshake
    self._sslobj.do_handshake()
    ~~~~~~~~~~~~~~~~~~~~~~~~~^^
ssl.SSLError: [SSL: WRONG_VERSION_NUMBER] wrong version number (_ssl.c:1033)
```

The plain server echoed `ECHO: ` and the client's own bytes back, and the client read `ECHO` as a TLS record header with no valid version.
Both mistakes print `WRONG_VERSION_NUMBER` on whichever side expected TLS, so that message means *the other end is not speaking TLS on this port*: check the port first.
The number in `(_ssl.c:1033)` is a line in Python's C source, so it differs between Python builds, and it says nothing about your program.

---

# Threads and Selectors

A server built from blocking calls serves one client at a time.
There are two ways to serve many: a thread for each, or one thread that only touches the sockets that are ready.

## `threading`: a thread per job, and a `Lock`

```python
"""thread_demo.py: one thread per job, and a Lock around the shared list"""
import threading
import time

finished = []
finished_lock = threading.Lock()


def job(name):
    time.sleep(0.25)
    with finished_lock:
        finished.append(name)


start = time.perf_counter()
workers = [threading.Thread(target=job, args=(f"job-{n}",), daemon=True) for n in range(4)]
for worker in workers:
    worker.start()
print("running threads:", threading.active_count())
for worker in workers:
    worker.join()
print(sorted(finished))
print(f"four quarter-second jobs took {time.perf_counter() - start:.2f} s")
```

```
(.venv) $ python3 thread_demo.py
running threads: 5
['job-0', 'job-1', 'job-2', 'job-3']
four quarter-second jobs took 0.25 s
```

| Call | What it does |
|---|---|
| `threading.Thread(target=job, args=(...,))` | prepares a call to `job` with those arguments, to run in a new thread |
| `daemon=True` | the thread does not keep the program alive once the main thread ends |
| `start()` | starts the thread, and returns at once |
| `join()` | waits until that thread has finished |
| `threading.active_count()` | how many threads are running, the main thread included |
| `threading.Lock()`, `with lock:` | lets one thread at a time into the block |

- `args` is a tuple, so one argument is written `(value,)`, with the comma.
- The four waits overlapped, so four quarter-second jobs took a quarter of a second.
- Every thread that changes the shared list does it under the same lock, so no two threads change it at once.
- A server starts each connection's thread with `daemon=True` and does not `join` it, so the main thread goes straight back to `accept`.

## `selectors`: which sockets are ready

```python
"""selector_demo.py: ask which sockets are ready, without blocking on any"""
import selectors
import socket

selector = selectors.DefaultSelector()
print("selector:", type(selector).__name__)
a_sender, a_receiver = socket.socketpair()
b_sender, b_receiver = socket.socketpair()
selector.register(a_receiver, selectors.EVENT_READ, "socket A")
selector.register(b_receiver, selectors.EVENT_READ, "socket B")

print("ready before any send:", [key.data for key, events in selector.select(timeout=0.5)])
b_sender.sendall(b"hi")
ready = selector.select(timeout=0.5)
print("ready after B sends:  ", [key.data for key, events in ready])
for key, events in ready:
    print(key.data, "has", key.fileobj.recv(1024))

a_receiver.setblocking(False)
try:
    a_receiver.recv(1024)
except BlockingIOError as error:
    print("non-blocking recv with nothing waiting:", error)
selector.unregister(a_receiver)
print("still registered:", [key.data for key in selector.get_map().values()])
```

```
(.venv) $ python3 selector_demo.py
selector: EpollSelector
ready before any send: []
ready after B sends:   ['socket B']
socket B has b'hi'
non-blocking recv with nothing waiting: [Errno 11] Resource temporarily unavailable
still registered: ['socket B']
```

| Call | What it does |
|---|---|
| `selectors.DefaultSelector()` | a selector built on the best mechanism the system has: `epoll` on Linux |
| `register(sock, EVENT_READ, data)` | watch `sock` for something to read, and attach `data` to it |
| `select(timeout=...)` | wait until at least one socket is ready, and return a list of `(key, events)` pairs for the ready ones |
| `key.fileobj`, `key.data` | the ready socket, and what was attached to it |
| `unregister(sock)` | stop watching `sock`, which comes before closing it |
| `setblocking(False)` | make the socket's calls return at once, raising `BlockingIOError` instead of waiting |

- `select` returned an empty list when nothing became ready before the timeout, and only socket B after B's data arrived.
- `data` can be anything: here a label, in a server often the function that handles that socket.
- Errno 11 is `EAGAIN`: the call would have had to wait, so a non-blocking socket refused to.

---

# Raw Sockets

Every socket above let the kernel write all the headers.
A raw socket moves that line, and it needs the Linux capability `CAP_NET_RAW`, so these examples run with `sudo`.
Without it, `socket()` itself raises `PermissionError`.

> [!warning] Your own lab only
> A raw socket can send packets with any header you write.
> These examples only receive, or send to Kali's own loopback address.

## An ICMP raw socket receives the IPv4 header too

```python
"""raw_listen.py: read two ICMP packets off a raw socket, IPv4 header and all"""
import socket

with socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP) as raw_socket:
    raw_socket.settimeout(5.0)
    print("raw socket open, waiting")
    for _ in range(2):
        packet, (source_address, _) = raw_socket.recvfrom(65535)
        print(len(packet), "bytes from", source_address, "| first 8:", packet[:8].hex(" "))
```

```
(.venv) $ sudo python3 raw_listen.py   [first terminal]
(.venv) $ ping -c 1 127.0.0.1
PING 127.0.0.1 (127.0.0.1) 56(84) bytes of data.
64 bytes from 127.0.0.1: icmp_seq=1 ttl=64 time=0.050 ms

--- 127.0.0.1 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 0.050/0.050/0.050/0.000 ms
[first terminal output]
raw socket open, waiting
84 bytes from 127.0.0.1 | first 8: 45 00 00 54 02 96 40 00
84 bytes from 127.0.0.1 | first 8: 45 00 00 54 02 97 00 00
```

- `socket(AF_INET, SOCK_RAW, IPPROTO_ICMP)` receives a copy of every ICMP packet the machine receives, whichever program it was for.
  On loopback the machine receives both `ping`'s echo request and the echo reply, so the raw socket saw two packets.
  This is why a program waiting for its own reply checks the source, the type and the identifier of each packet.
- Each packet starts with its IPv4 header: `45` is version 4 and the header length, and `00 54` is the total length, 84 bytes.
  Module 1 Session 1's Tooling Reference shows how to read both nibbles of that first byte.
- `ping` prints `56(84)`: 56 bytes of data, 84 bytes in the whole IPv4 packet.

## `IP_HDRINCL`: who writes the IPv4 header

```python
"""hdrincl_flag.py: IP_HDRINCL is a socket option you can read back"""
import socket

with socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP) as icmp_socket:
    print("ICMP raw socket, IP_HDRINCL:", icmp_socket.getsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL))
    icmp_socket.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
    print("after setsockopt,  IP_HDRINCL:", icmp_socket.getsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL))
with socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW) as any_socket:
    print("IPPROTO_RAW socket, IP_HDRINCL:", any_socket.getsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL))
```

```
(.venv) $ sudo python3 hdrincl_flag.py
ICMP raw socket, IP_HDRINCL: 0
after setsockopt,  IP_HDRINCL: 1
IPPROTO_RAW socket, IP_HDRINCL: 1
```

- With `IP_HDRINCL` at 0, the kernel writes the IPv4 header in front of what the program sends.
  At 1, what the program sends must already start with an IPv4 header.
- A raw socket opened for `IPPROTO_RAW` has the option on from the start (the Linux `raw(7)` manual page).
- On receive, nothing changes: an IPv4 raw socket hands over the IPv4 header either way.

## `AF_PACKET`: a socket bound to an interface

```python
"""packet_demo.py: an AF_PACKET socket's own name, and one frame from loopback"""
import socket
import sys

interface = sys.argv[1]
with socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(0x0800)) as packet_socket:
    packet_socket.bind((interface, 0))
    name = packet_socket.getsockname()
    print("getsockname():", name)
    print("own MAC:", name[4].hex(":"))

with socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(0x0800)) as packet_socket:
    packet_socket.bind(("lo", 0))
    packet_socket.settimeout(5.0)
    frame = packet_socket.recv(65535)
    print("frame on lo:", len(frame), "bytes | Ethernet header:", frame[:14].hex(" "))
```

```
(.venv) $ sudo python3 packet_demo.py eth1   [first terminal]
(.venv) $ ping -c 1 127.0.0.1 > /dev/null
[first terminal output]
getsockname(): ('eth1', 2048, 0, 1, b"\x08\x00'\xb7\xbc\x9d")
own MAC: 08:00:27:b7:bc:9d
frame on lo: 98 bytes | Ethernet header: 00 00 00 00 00 00 00 00 00 00 00 00 08 00
```

- `socket(AF_PACKET, SOCK_RAW, htons(0x0800))` works one layer lower than `AF_INET`: it sends and receives whole **Ethernet frames**, here only those whose EtherType is `0x0800`, IPv4.
  The protocol number goes in network byte order, hence `htons`.
- It binds to an **interface name** and `0`, not to an address and a port.
- `getsockname()` returns the interface, the protocol (`2048` is `0x0800`), the packet type, the hardware type (`1` is Ethernet) and the interface's own MAC address, as 6 bytes.
- A frame received this way starts with the 14-byte Ethernet header: destination MAC, source MAC, EtherType.
  The loopback interface has no real MAC addresses, so both are zeros, and the frame is 14 bytes longer than the 84-byte packet inside it.

## `tcpdump -X`: the bytes that crossed the interface

`tcpdump` prints the packets an interface carries, and `-X` adds each one's bytes in hex and ASCII, which is how to see exactly what a raw socket sent.

```
(.venv) $ sudo tcpdump -i lo -n -X -c 2 icmp   [first terminal]
(.venv) $ ping -c 1 -p 6c6162 127.0.0.1 > /dev/null
[first terminal output]
tcpdump: verbose output suppressed, use -v[v]... for full protocol decode
listening on lo, link-type EN10MB (Ethernet), snapshot length 262144 bytes
14:17:16.106281 IP 127.0.0.1 > 127.0.0.1: ICMP echo request, id 13, seq 1, length 64
	0x0000:  4500 0054 040a 4000 4001 389d 7f00 0001  E..T..@.@.8.....
	0x0010:  7f00 0001 0800 f1c6 000d 0001 2c3c e26a  ............,<.j
	0x0020:  0000 0000 079f 0100 0000 0000 6162 6c61  ............abla
	0x0030:  626c 6162 6c61 626c 6162 6c61 626c 6162  blablablablablab
	0x0040:  6c61 626c 6162 6c61 626c 6162 6c61 626c  lablablablablabl
	0x0050:  6162 6c61                                abla
14:17:16.106295 IP 127.0.0.1 > 127.0.0.1: ICMP echo reply, id 13, seq 1, length 64
	0x0000:  4500 0054 040b 0000 4001 789c 7f00 0001  E..T....@.x.....
	0x0010:  7f00 0001 0000 f9c6 000d 0001 2c3c e26a  ............,<.j
	0x0020:  0000 0000 079f 0100 0000 0000 6162 6c61  ............abla
	0x0030:  626c 6162 6c61 626c 6162 6c61 626c 6162  blablablablablab
	0x0040:  6c61 626c 6162 6c61 626c 6162 6c61 626c  lablablablablabl
	0x0050:  6162 6c61                                abla
2 packets captured
4 packets received by filter
0 packets dropped by kernel
```

| Option | Meaning |
|---|---|
| `-i lo` | the interface to listen on |
| `-n` | print addresses as numbers, with no name lookups |
| `-X` | print each packet's bytes in hex and ASCII |
| `-c 2` | stop after 2 packets |
| `icmp` | a filter: keep ICMP packets only |

- The dump starts at the IPv4 header (`0x0000: 4500`), not at the Ethernet header.
- `ping -p 6c6162` repeats the bytes `6c 61 62`, `lab`, through the echo data, so the data is easy to find in the dump.
  In the echo reply the type byte at the start of the ICMP message changed from `08` to `00` and the data came back unchanged, which is what an echo reply is.

---

# Command-Line Tools

These are the commands that show what the sockets above are doing, from outside the program.

## `ss`: the sockets that exist right now

`ss` ("socket statistics") lists the sockets on a machine while they are open.
The examples run `hold_pair.py`, which listens on 9006, connects to itself and holds the connection open for 4 seconds:

```python
"""hold_pair.py: one listener and one connection to it, held open for 4 seconds"""
import socket
import time

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listener:
    listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listener.bind(("127.0.0.1", 9006))
    listener.listen()
    client_socket = socket.create_connection(("127.0.0.1", 9006))
    conn, _ = listener.accept()
    time.sleep(4)
    conn.close()
    client_socket.close()
```

```
(.venv) $ python3 hold_pair.py   [first terminal]
(.venv) $ ss -tln 'sport = :9006'
State  Recv-Q Send-Q Local Address:Port Peer Address:Port
LISTEN 0      128        127.0.0.1:9006      0.0.0.0:*   
(.venv) $ ss -tn state established '( sport = :9006 or dport = :9006 )'
Recv-Q Send-Q Local Address:Port  Peer Address:Port 
0      0          127.0.0.1:9006     127.0.0.1:54228
0      0          127.0.0.1:54228    127.0.0.1:9006 
(.venv) $ ss -tnp state established 'sport = :9006'
Recv-Q Send-Q Local Address:Port Peer Address:Port Process                            
0      0          127.0.0.1:9006    127.0.0.1:54228 users:(("python3",pid=50957,fd=5))
```

And a UDP socket bound to 9004:

```
(.venv) $ ss -uan 'sport = :9004'
State  Recv-Q Send-Q Local Address:Port Peer Address:Port
UNCONN 0      0          127.0.0.1:9004      0.0.0.0:*   
```

| Option or filter | Meaning |
|---|---|
| `-t`, `-u` | TCP sockets, UDP sockets |
| `-l` | listening sockets only |
| `-a` | all sockets: listening and not |
| `-n` | numbers, not service names: `9006`, not a name looked up for it |
| `-p` | the process that holds each socket, with its PID and file descriptor (sockets of other users' processes need `sudo`) |
| `-o` | timer information, such as how long a closed connection stays in `TIME_WAIT` |
| `state established`, `state time-wait` | only sockets in that TCP state |
| `'sport = :9006'`, `'dport = :9006'` | only sockets whose source port, or destination port, is 9006 |

- One connection showed up as **two** lines, one per end, because both ends live on this machine: each line is one socket, seen from its own side.
- On a `LISTEN` line, `Send-Q` is the listener's **backlog**: `listen()` with no argument gave 128 (*Beyond This Session* below).
- A UDP socket has no connection, so its state is `UNCONN` and its peer is `0.0.0.0:*`.
- Quote a filter, because the shell would read `(` and `)` itself.

> [!tip] The defender's first look
> `ss -tlnp` answers *what is listening on this machine, and which program opened it*.
> An unexpected listener is the first thing an incident responder looks for.

## `ip` and `ping`: addresses, neighbors and reachability

```
(.venv) $ ip -br -4 addr
lo               UNKNOWN        127.0.0.1/8 
eth1             UP             192.168.56.107/24 
docker0          DOWN           172.17.0.1/16 
(.venv) $ ping -c 3 192.168.56.1
PING 192.168.56.1 (192.168.56.1) 56(84) bytes of data.
64 bytes from 192.168.56.1: icmp_seq=1 ttl=64 time=0.303 ms
64 bytes from 192.168.56.1: icmp_seq=2 ttl=64 time=0.432 ms
64 bytes from 192.168.56.1: icmp_seq=3 ttl=64 time=0.806 ms

--- 192.168.56.1 ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2035ms
rtt min/avg/max/mdev = 0.303/0.513/0.806/0.213 ms
(.venv) $ ip neigh show 192.168.56.1
192.168.56.1 dev eth1 lladdr 0a:00:27:00:00:00 REACHABLE 
```

| Command | What it shows |
|---|---|
| `ip -br -4 addr` | one line per interface: its name, its state and its IPv4 address with the prefix length (`-br` brief, `-4` IPv4 only) |
| `ping -c 3 HOST` | sends 3 ICMP echo requests and reports each reply and the round-trip time |
| `ip neigh show HOST` | the **neighbor table** entry for a host on the same link: its MAC address after `lladdr`, and the entry's state |

- The recording lab's interface is `eth1`, and this machine also has a `docker0` interface.
  On CyberLab, your Kali's line is `eth0` with a `10.0.2.x` address: read the name from your own output, never from this one.
- A neighbor entry appears only after the machine has talked to that host, which is why `ping` comes first.
  `REACHABLE` means the entry was confirmed recently.

## `nc`: a socket on the command line

`nc` (netcat) connects to a port, or listens on one, and moves its input and output across the connection.

```
(.venv) $ nc -h 2>&1 | head -1
[v1.10-50.1]
```

As a client, against `tcp_demo_server.py`:

```
(.venv) $ python3 tcp_demo_server.py   [first terminal]
(.venv) $ printf 'hi from nc\n' | nc 127.0.0.1 9001
ECHO: hi from nc
[first terminal output]
listening on ('127.0.0.1', 9001)
accepted ('127.0.0.1', 38548)
this end ('127.0.0.1', 9001) other end ('127.0.0.1', 38548)
received b'hi from nc\n'
both sockets closed
```

As a listener, with a Python client:

```
(.venv) $ nc -l -p 9007   [first terminal]
(.venv) $ python3 -c "import socket; s = socket.create_connection(('127.0.0.1', 9007)); s.sendall(b'hello, listener\n'); s.close()"
[first terminal output]
hello, listener
```

| Command | What it does |
|---|---|
| `nc HOST PORT` | connect, send what it reads on its input, and print what arrives |
| `nc HOST PORT < /dev/null` | connect and send nothing, only print what the server sends |
| `nc -l -p PORT` | listen on `PORT` for one connection, and print what arrives |
| `nc -u HOST PORT` | the same over UDP |

Kali's `nc` is **netcat-traditional**, version 1.10, which exits once the server closes the connection.

> [!tip] Another machine's `nc` may be a different program
> Ubuntu's `nc` is OpenBSD netcat, a different program with different options.
> Given a terminal as its input instead of `< /dev/null`, it prints what the server sent and then waits, where Kali's exits.
> The **Troubleshooting FAQ** has the symptom.

## `python3 -m http.server`: a listener in one line

`python3 -m http.server` serves the current folder over HTTP, which makes a real TCP listener without writing one.

```
(.venv) $ python3 -m http.server 9008 --bind 127.0.0.1   [first terminal]
(.venv) $ curl -sI http://127.0.0.1:9008/
HTTP/1.0 200 OK
Server: SimpleHTTP/0.6 Python/3.13.12
Date: Wed, 28 Oct 2026 18:17:24 GMT
Content-type: text/html; charset=utf-8
Content-Length: 1696

[first terminal output]
Serving HTTP on 127.0.0.1 port 9008 (http://127.0.0.1:9008/) ...
127.0.0.1 - - [28/Oct/2026 14:17:24] "HEAD / HTTP/1.1" 200 -
```

- `--bind` takes the address to listen on, so `--bind 127.0.0.1` answers only this machine.
- `curl -sI` sends one HTTP `HEAD` request and prints the reply's headers (`-s` silent, `-I` headers only), and the server logs one line per request.
- Stop the server with **Ctrl+C**.
  It serves every file in the folder it was started in, so start it in a folder that holds nothing private.

## `iptables`: a rule that drops packets

`iptables` edits the Linux firewall's rule lists, called **chains**.
`INPUT` holds the rules for packets arriving for this machine.

```
(.venv) $ sudo iptables -I INPUT -p tcp --dport 9009 -j DROP
(.venv) $ sudo iptables -L INPUT -n
Chain INPUT (policy ACCEPT)
target     prot opt source               destination         
DROP       tcp  --  0.0.0.0/0            0.0.0.0/0            tcp dpt:9009
(.venv) $ python3 -c "import socket; socket.create_connection(('127.0.0.1', 9009), timeout=1.0)" 2>&1 | tail -1
TimeoutError: timed out
(.venv) $ sudo iptables -D INPUT -p tcp --dport 9009 -j DROP
(.venv) $ sudo iptables -L INPUT -n
Chain INPUT (policy ACCEPT)
target     prot opt source               destination         
(.venv) $ python3 -c "import socket; socket.create_connection(('127.0.0.1', 9009), timeout=1.0)" 2>&1 | tail -1
ConnectionRefusedError: [Errno 111] Connection refused
```

| Part | Meaning |
|---|---|
| `-I INPUT` | insert a rule at the top of the `INPUT` chain |
| `-p tcp --dport 9009` | match TCP packets to destination port 9009 |
| `-j DROP` | the action: drop the packet, and send nothing back |
| `-D INPUT ...` | delete the rule that matches the rest of the line exactly |
| `-L INPUT -n` | list the chain's rules, with numeric addresses |

- With the rule in place, the connection attempt got no answer at all, and the 1-second deadline ended it.
- With the rule gone, nothing listened on 9009, so the same attempt was refused at once: a closed port answers, a filtered one stays silent.
- `2>&1 | tail -1` keeps only the traceback's last line, the exception.
- The `prot` column shows the protocol by name here, and some versions of `iptables` print its number instead, `6` for TCP.

> [!warning] Remove what you add
> A rule stays until it is deleted or the machine restarts.
> Delete each rule you add with the same line and `-D`, and list the chain to check that it is gone.

## `sudo`, `ssh` and `scp`

- `sudo COMMAND` runs one command as root, and asks for your password the first time in a terminal.
  It is needed for raw sockets, `tcpdump` and `iptables`, and nothing else in this session.
  Run with `sudo` only programs you wrote or read.
- `ssh lab` and `scp FILE lab:FOLDER/` reach the peer through the `lab` entry you made in Module 0 Session 1, which teaches both.

---

# Beyond This Session

Five topics sit next to this session's material and belong to later work.
Each one is a pointer to the Python documentation, so you know the name when you meet it.

## The accept queue and `listen`'s backlog

The kernel completes TCP handshakes before the program calls `accept`, and keeps those connections in a queue until it does.
`listen(backlog)` sets how long that queue may grow, and `listen()` with no argument picked 128 on Kali, the `Send-Q` of the `LISTEN` line in the `ss` example.
What happens when the queue is full is TCP's own behavior, which belongs with the transport layer.
Documentation: [`socket.listen`](https://docs.python.org/3/library/socket.html#socket.socket.listen).

## Names to addresses: `getaddrinfo`

Every program in this session was given an address.
A program given a name, such as `example.com`, asks `socket.getaddrinfo(host, port)`, which returns every address and family the name resolves to, as 5-tuples `(family, type, proto, canonname, sockaddr)`.
`socket.create_connection` calls it for you, and tries each address in turn.
Documentation: [`socket.getaddrinfo`](https://docs.python.org/3/library/socket.html#socket.getaddrinfo).

## IPv6 and dual-stack sockets

An IPv6 socket is `socket(AF_INET6, ...)`, and its addresses are 4-tuples `(host, port, flowinfo, scope_id)`.
A **dual-stack** listener is one `AF_INET6` socket bound to `::` with the option `IPV6_V6ONLY` off, which also accepts IPv4 clients, shown as IPv4-mapped addresses such as `::ffff:10.0.2.15`.
`socket.create_server(address, family=socket.AF_INET6, dualstack_ipv6=True)` builds one.
Documentation: [`socket.create_server`](https://docs.python.org/3/library/socket.html#socket.create_server).

## Local sockets: `AF_UNIX`

An `AF_UNIX` socket connects two programs on the **same machine** through a path in the filesystem, with no IP address and no port.
Many system services talk to their clients this way, and `ss -x` lists these sockets.
Documentation: [`socket` address families](https://docs.python.org/3/library/socket.html#socket-families).

## `asyncio`: coroutines on one thread

`asyncio` serves many connections on one thread, like a selector loop, but each connection's handler is written as straight-line code: a **coroutine** that pauses at each `await` until its socket is ready.
`asyncio.start_server` gives each connection a reader and a writer object instead of a socket.
Documentation: [`asyncio` streams](https://docs.python.org/3/library/asyncio-stream.html).
