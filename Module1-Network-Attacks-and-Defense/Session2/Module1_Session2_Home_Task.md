# Module 1 · Session 2 — Home Task

## The Python Networking Stack

### Professional Training in Cybersecurity I

---

> [!note] How this home task works
> The Practical Guide used each kind of socket once, the way it is meant to be used.
> This home task uses the same sockets to read and write the bytes that the usual calls hide from you.
> You build **four tools** in two parts.
> The first part reads what a socket really delivered: the name inside a TLS client's first record, and the size of a datagram that did not fit your buffer.
> The second part writes headers the kernel normally writes for you: the IPv4 header, and then the whole Ethernet frame.
>
> Each task is marked **🧩 GUIDED** or **🔨 FROM SCRATCH**.
> A guided task gives you a starter with `# TODO` gaps, so the plumbing is done and you can focus on the idea.
> A from-scratch task gives you the requirements, and you write the whole script.
>
> Your worksheet is **`Module1_Session2_Home_Task_Submission.md`**, already in your repository's `Module1-Network-Attacks-and-Defense/Session2` folder since the Practical Guide's setup.
> Work in `~/cyberlabs/Module1-Network-Attacks-and-Defense/Session2`, the working folder you made for the Practical Guide, with its `.venv`.
> Everything uses the Python standard library only.
> Paste your finished code, its output, your screenshots and your answers into the worksheet, which is the graded document.

> [!important] Everything here is required
> There are no optional parts: all four tools, every run and every question.
> Every script must run without errors.

> [!warning] Raw sockets are for your own lab only
> Tasks 3 and 4 send packets whose headers you write, so they need `sudo` on Kali.
> Send them only from Kali to your own Ubuntu peer, on the CyberLab network, and only with your own addresses: both tools ask the kernel for Kali's own address and MAC, so every source field you send is Kali's own.
> Run with `sudo` only the scripts you wrote for these tasks, and never give `CAP_NET_RAW` to the Python interpreter itself, because every script that interpreter runs would then hold it.

---

# Before You Start

1. **Pull your repository**, because your instructor's feedback on the Practical Guide arrives there:

   ```bash
   cd ~/student-YOUR-USERNAME
   git pull
   ```

2. **Open your working folder** and a new terminal in it:

   ```bash
   code ~/cyberlabs/Module1-Network-Attacks-and-Defense/Session2
   ```

   In VS Code, open **Terminal**, then **New Terminal**.
   It activates `.venv` by itself, so its prompt starts with `(.venv)`.

3. **Check that Kali reaches the peer**, which Tasks 3 and 4 need.
   Start the Ubuntu peer, then on Kali:

   ```bash
   ping -c 1 PEER_ADDRESS
   ```

   `PEER_ADDRESS` is the peer's lab address from the Practical Guide's lab check, and the line `1 received` must appear.
   Tasks 1 and 2 run on Kali alone, on its own loopback address.

---

# What Arrives on the Socket

*Shared idea: a socket hands you bytes, and only your code decides what they mean.*
*Read a record by its own header, and a datagram by its real size, or you misread what arrived.*

---

## Task 1: Read the Server Name from a TLS First Flight — REQUIRED

> **🧩 GUIDED: complete the starter below** | Difficulty: ⭐⭐⭐ Hard
> *Copy the starter out, fill its three `# TODO` gaps in your IDE, and run it against `openssl s_client`.*

> [!note] Concept note
> A TLS client speaks first: before any key exists, it sends a **ClientHello**, its **first flight**.
> Nothing in the ClientHello is encrypted, because the two sides have not yet agreed on a key.
> One of its extensions, **`server_name`** (RFC 6066), carries the hostname the client passed as `server_hostname`, so a server that hosts many names can choose the right certificate.
> Anyone on the path can therefore read which name the client asked for, even though everything after the handshake is encrypted.
>
> TLS sends its messages over TCP in **records**, and TCP keeps no message boundaries, so a record is read the way the Practical Guide's length prefix taught: a fixed 5-byte header first, then exactly the length it states.
>
> | bytes | field |
> |---|---|
> | 1 | content type: which kind of message the record carries |
> | 2 | version |
> | 2 | length of the record's body |
>
> The body is the handshake message.
> Its first byte is the handshake type, 3 bytes give its length, and then the ClientHello's fields follow in this order (RFC 8446, section 4.1.2):
>
> | field | size |
> |---|---|
> | `legacy_version` | 2 bytes |
> | `random` | 32 bytes |
> | `legacy_session_id` | a 1-byte length, then that many bytes |
> | `cipher_suites` | a 2-byte length, then that many bytes |
> | `legacy_compression_methods` | a 1-byte length, then that many bytes |
> | `extensions` | a 2-byte length, then the extensions |
>
> Each extension is a 2-byte type, a 2-byte length and its data.
> The `server_name` extension has type `0`, and its data is a 2-byte list length, a 1-byte name type, a 2-byte name length and then the name in ASCII.

Your program plays the server on `127.0.0.1:8444`, but it never answers the handshake: it is a plain TCP socket that reads the client's first record and parses it.
The client is `openssl s_client`, the OpenSSL command-line TLS client, so the bytes you parse come from a real TLS implementation.

Create `sni_reader.py` and complete its three TODOs:

```python
# @starter sni_reader.py
"""sni_reader.py: accept one TLS client and read the server name from its first flight"""
import socket
import struct


def recv_exact(conn, count):
    """Read exactly count bytes, as in the Practical Guide's framed client."""
    data = b""
    while len(data) < count:
        chunk = conn.recv(count - len(data))
        if chunk == b"":
            raise ConnectionError("the client closed before the record ended")
        data += chunk
    return data


def server_name_from(hello):
    """Walk a ClientHello to its server_name extension and return the name."""
    offset = 4 + 2 + 32  # handshake header, legacy_version, random
    # Each variable field starts with its own length: 1, 2 and 1 bytes.
    # TODO 2: move offset past legacy_session_id (a 1-byte length, then its bytes),
    #   cipher_suites (a 2-byte length, read with struct.unpack("!H", ...)) and
    #   legacy_compression_methods (a 1-byte length), so it points at the extensions.
    extensions_end = offset + 2 + struct.unpack("!H", hello[offset:offset + 2])[0]
    offset += 2
    while offset < extensions_end:
        extension_type, extension_length = struct.unpack("!HH", hello[offset:offset + 4])
        offset += 4
        if extension_type == 0:
            # list length (2), name type (1), name length (2), then the name
            # TODO 3: read name_length from the 2 bytes at offset + 3, and return the
            #   name_length bytes after them, decoded as ASCII.
            return None
        offset += extension_length
    return None


listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listener.bind(("127.0.0.1", 8444))
listener.listen()
print("listening on", listener.getsockname())
conn, client_address = listener.accept()
with conn:
    record_header = recv_exact(conn, 5)
    # TODO 1: unpack record_header with "!BHH" into record_type, record_version
    #   and record_length.
    record_type, record_version, record_length = 0, 0, 0
    print(f"record type {record_type}, version 0x{record_version:04x}, length {record_length}")
    client_hello = recv_exact(conn, record_length)
    print("handshake type", client_hello[0])
    print("server_name:", server_name_from(client_hello))
listener.close()
```

**Run it** on Kali, in two terminals, twice.

1. **With a name.**
   In the first terminal, start the reader:

   ```bash
   python3 sni_reader.py
   ```

   In the second terminal, connect a TLS client that asks for `peer.lab`:

   ```bash
   openssl s_client -connect 127.0.0.1:8444 -servername peer.lab < /dev/null
   ```

   The reader prints its address, then three lines about the record, and ends.
   The client then reports an error and exits, because nothing ever answered its ClientHello: that error is expected.

2. **Without a name.**
   Start the reader again, then run the client with `-noservername`, which sends no `server_name` extension:

   ```bash
   openssl s_client -connect 127.0.0.1:8444 -noservername < /dev/null
   ```

> [!tip] When the reader prints nonsense
> A record length in the tens of thousands, or an `IndexError`, means an offset is off by a field.
> Count TODO 2 again against the table: each length is read *at* the offset, and then the offset moves past the length *and* the bytes it counts.
> The record's length depends on your OpenSSL version, so it will not match a classmate's, and that is expected.

**Answer from your run:**

1. The run with `-servername peer.lab`.
   - **1a.** What record type did the reader print?
   - **1b.** What record version did it print, in hexadecimal?
   - **1c.** What record length did it print?
2. The run with `-noservername`.
   - **2a.** What did the `server_name:` line print?
   - **2b.** What record length did it print?
   - **2c.** How many bytes shorter was this record than the one in 1c?

> [!example] 📝 Submission
> Paste your completed `sni_reader.py`, the reader's output from both runs, and a screenshot of both terminals from the first run into your **Home Task Submission**, then answer the Task 1 questions.

---

## Task 2: Detect a Datagram That Was Cut Short — REQUIRED

> **🔨 FROM SCRATCH** | Difficulty: ⭐⭐ Medium
> *Read the requirements and write the complete script yourself.*

> [!note] Concept note
> A datagram socket delivers one whole datagram per `recvfrom`, and the Practical Guide showed what a too-small buffer does: the rest of the datagram is dropped, and the call raises nothing.
> A program that receives into a fixed buffer therefore cannot tell, from the bytes alone, whether it saw a whole datagram or the beginning of a longer one.
> Linux reports the loss anyway, in two places.
> `recvmsg(bufsize)` returns a 4-tuple `(data, ancdata, msg_flags, address)`, and its `msg_flags` has the **`MSG_TRUNC`** bit set when the datagram was longer than the buffer.
> And a receive called with the flags `MSG_PEEK | MSG_TRUNC` leaves the datagram in the queue and returns its **real length**, however small the buffer (the Linux `recv(2)` manual page).
> In Python that second call is `recv_into(bytearray(1), 1, socket.MSG_PEEK | socket.MSG_TRUNC)`, which returns the length as an `int`.

Create `trunc_detector.py`.

**Requirements:**

- Bind a UDP socket to `127.0.0.1` port `8090`, and receive with a fixed buffer of **64 bytes** (`BUFFER_SIZE = 64`).
- For every datagram, first peek at its real length with `MSG_PEEK | MSG_TRUNC`, then receive it with `recvmsg(BUFFER_SIZE)`.
- Decide truncation from the `MSG_TRUNC` bit in `msg_flags` (`msg_flags & socket.MSG_TRUNC`), never by comparing the data's length with the buffer size.
- Print one line per datagram: `complete` with its length, or `TRUNCATED` with how many bytes were kept and the real length.
- Stop at a datagram that is exactly `b"END"`, and print how many datagrams were truncated.

**Run it** on Kali, in two terminals.
In the first, start the detector:

```bash
python3 trunc_detector.py
```

In the second, send five datagrams of 12, 64, 65, 300 and 1200 bytes, then `END`:

```bash
python3 -c "import socket; s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM); [s.sendto(b'x' * n, ('127.0.0.1', 8090)) for n in (12, 64, 65, 300, 1200)]; s.sendto(b'END', ('127.0.0.1', 8090))"
```

**What your detector must report:** the 12-byte and 64-byte datagrams complete, the other three truncated with their real lengths, and a count of 3.
The 64-byte datagram is the test of your rule: it fills the buffer exactly and is **not** truncated, while the 65-byte one fills it the same way and is.

> [!example] 📝 Submission
> Paste your `trunc_detector.py`, its output, and a screenshot of both terminals into your **Home Task Submission**, then answer the Task 2 questions.

---

# Headers the Program Writes

*Shared idea: a raw socket moves the line between the headers the kernel writes and the bytes your program writes.*
*Write the IPv4 header next, and then every header down to Ethernet.*

---

## Task 3: Write the IPv4 Header with IP_HDRINCL — REQUIRED

> **🧩 GUIDED: complete the starter below** | Difficulty: ⭐⭐ Medium
> *Copy the starter out, fill its three `# TODO` gaps in your IDE, and run it on Kali with `sudo`.*

> [!note] Concept note
> In the Practical Guide's Exercise 9 you wrote the ICMP message, and the kernel wrote the IPv4 header in front of it.
> The socket option **`IP_HDRINCL`** ("header included") moves that line one layer down: once it is set, the bytes you pass to `sendto` must **start with an IPv4 header you wrote**.
> Linux still completes four fields for you (the `raw(7)` manual page): it always fills the **total length** and the **header checksum**, and it fills the **identification** and the **source address** when you leave them `0`.
> This task writes the source address itself, and the starter's `own_address` function asks the kernel which of the client's addresses reaches the server, so the header names the address the client really has.
> Setting the source by hand changes nothing about who may receive the reply: it goes to whatever address the header names.
>
> The IPv4 header you write, 20 bytes with no options:
>
> | field | size | this header |
> |---|---|---|
> | version and IHL | 1 | `0x45`: version 4, 5 words |
> | type of service | 1 | `0` |
> | total length | 2 | `0`, filled by Linux |
> | identification | 2 | `0`, filled by Linux |
> | flags and fragment offset | 2 | `0` |
> | time to live | 1 | `64` |
> | protocol | 1 | `1`, ICMP (`socket.IPPROTO_ICMP`) |
> | header checksum | 2 | `0`, filled by Linux |
> | source address | 4 | the client's own address |
> | destination address | 4 | the server's address |

Create `hdrincl_echo.py` and complete its three TODOs.
The ICMP echo request is Exercise 9's, given here complete:

```python
# @starter hdrincl_echo.py
"""hdrincl_echo.py: send an ICMP echo request whose IPv4 header the program writes"""
import socket
import struct
import sys

IDENTIFIER = 0x4321
SEQUENCE = 1
PAYLOAD = b"hdrincl"


def checksum(data):
    """The Internet checksum (RFC 1071), as in Module 1 Session 1."""
    if len(data) % 2:
        data += b"\x00"
    total = sum(struct.unpack(f"!{len(data) // 2}H", data))
    while total >> 16:
        total = (total & 0xFFFF) + (total >> 16)
    return ~total & 0xFFFF


def own_address(peer_address):
    """Ask the kernel which of this machine's addresses reaches peer_address."""
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as probe:
        probe.connect((peer_address, 9))  # a UDP connect sends nothing
        return probe.getsockname()[0]


def build_request():
    """The echo request of the Practical Guide's Exercise 9, with this task's values."""
    header = struct.pack("!BBHHH", 8, 0, 0, IDENTIFIER, SEQUENCE)
    request_checksum = checksum(header + PAYLOAD)
    return struct.pack("!BBHHH", 8, 0, request_checksum, IDENTIFIER, SEQUENCE) + PAYLOAD


if len(sys.argv) != 2:
    sys.exit("usage: sudo python3 hdrincl_echo.py PEER_ADDRESS")
peer_address = sys.argv[1]
client_address = own_address(peer_address)

# Total length, identification and checksum are 0: Linux fills them in.
# TODO 1: pack ip_header with "!BBHHHBBH4s4s" in the table's order: 0x45, 0, 0, 0,
#   0, 64, socket.IPPROTO_ICMP, 0, then client_address and peer_address, each
#   turned into 4 bytes with socket.inet_aton.
ip_header = b""
print("IPv4 header written:", ip_header.hex(" "))

with socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP) as raw_socket:
    # TODO 2: set the option IP_HDRINCL to 1, at level socket.IPPROTO_IP, so the
    #   kernel sends your ip_header instead of writing its own.
    raw_socket.settimeout(2.0)
    print("sent", raw_socket.sendto(ip_header + build_request(), (peer_address, 0)), "bytes")
    while True:
        reply, (source_address, _) = raw_socket.recvfrom(65535)
        header_length = (reply[0] & 0x0F) * 4
        icmp = reply[header_length:]
        reply_type, code, _, identifier, sequence = struct.unpack("!BBHHH", icmp[:8])
        if (source_address == peer_address and reply_type == 0
                and identifier == IDENTIFIER and sequence == SEQUENCE):
            break

# TODO 3: set reply_destination from the reply's destination address field
#   (reply[16:20]), turned into text with socket.inet_ntoa.
reply_destination = "?"
print("reply IPv4 header:  ", reply[:header_length].hex(" "))
print("reply from", source_address, "to", reply_destination)
print("ICMP type", reply_type, "code", code, "data:", icmp[8:])
```

**Run it** on Kali, with `sudo`, which asks for your Kali password:

```bash
sudo python3 hdrincl_echo.py PEER_ADDRESS
```

It prints the 20 bytes your program wrote, how many bytes it sent, the reply's 20-byte IPv4 header, who the reply came from and went to, and the reply's ICMP type, code and data.
The data must read `b'hdrincl'`, and the header you wrote must show `00 00` in the total length, identification and checksum positions.

> [!tip] When the reply never comes
> A `TimeoutError` after 2 seconds means no matching reply arrived.
> Without TODO 2 the kernel writes its own header in front of yours, so the peer reads your 20 bytes as a broken ICMP message and does not answer.
> If `ping -c 1 PEER_ADDRESS` fails too, the problem is the lab, not your header.

**Answer from your run**, reading the reply's IPv4 header byte by byte against the table:

3. The reply's IPv4 header.
   - **3a.** How many bytes did `sendto` report sending?
   - **3b.** What is the reply's total length field, in decimal?
   - **3c.** What is the reply's identification field, in hexadecimal?
   - **3d.** What destination address did the reply carry?

> [!example] 📝 Submission
> Paste your completed `hdrincl_echo.py`, its `sudo` run, and a screenshot of the run into your **Home Task Submission**, then answer the Task 3 questions.

---

## Task 4: Send a Complete Ethernet Frame with AF_PACKET — REQUIRED

> **🔨 FROM SCRATCH** | Difficulty: ⭐⭐⭐ Hard
> *Read the requirements and write the complete script yourself.*

> [!note] Concept note
> An **`AF_PACKET`** socket moves the line to the bottom: it is bound to a network interface, not to an address or a port, and what you send is a **complete Ethernet frame**.
> Nothing is filled in for you, so the frame needs the server's MAC address, the client's own MAC address, the EtherType `0x0800` for IPv4, an IPv4 header with its total length and checksum **computed by you**, and then the ICMP message.
> Created as `socket(AF_PACKET, SOCK_RAW, htons(0x0800))`, the same socket also receives every IPv4 frame the interface carries, Ethernet header included, so the reply is found by testing each frame.
> The server's MAC address comes from the client's neighbor table, which a `ping` fills: `ip neigh show PEER_ADDRESS` prints it after `lladdr`.

First fill the neighbor table and read the peer's MAC address, on Kali:

```bash
ping -c 1 PEER_ADDRESS
ip neigh show PEER_ADDRESS
```

Your interface is the one that holds Kali's CyberLab address, `10.0.2.x`, in the output of `ip -br -4 addr`.

Create `frame_echo.py`.

**Requirements:**

- Take the interface, the peer's IPv4 address and the peer's MAC address on the command line (`sys.argv[1:4]`).
- Create an `AF_PACKET`, `SOCK_RAW` socket for `socket.htons(0x0800)`, bind it to `(INTERFACE, 0)`, and read Kali's own MAC address from `getsockname()[4]`.
- Get Kali's own IPv4 address with Task 3's `own_address` function.
- Build an ICMP echo request with identifier `0x5678`, sequence `1` and the data `b"frame"`, its checksum computed as in Task 3.
- Build a 20-byte IPv4 header whose **total length** and **header checksum** you compute, with Kali's address as source and the peer's as destination.
- Build the 14-byte Ethernet header (peer MAC, Kali MAC, EtherType `0x0800`), and send the whole frame with `send`.
- With a 2-second timeout, receive frames until one is an ICMP echo reply from the peer carrying your identifier.
- Print how many bytes were sent, the reply frame's length, its source MAC and EtherType, the reply's ICMP type, whether the reply's IPv4 header checksum verifies, and the reply's data, cut at the end the IPv4 total length gives.

**Run it** on Kali, first without `sudo` and then with it:

```bash
python3 frame_echo.py INTERFACE PEER_ADDRESS PEER_MAC
sudo python3 frame_echo.py INTERFACE PEER_ADDRESS PEER_MAC
```

**What your tool must report:** without `sudo`, `socket()` raises `PermissionError`.
With `sudo`, a reply frame from the peer's MAC address with EtherType `0800`, ICMP type `0`, an IPv4 checksum that verifies, and the data `b'frame'`.

**Answer from your run:**

4. The `sudo` run.
   - **4a.** How many bytes long was the frame you sent?
   - **4b.** How many bytes long was the reply frame you received?

> [!example] 📝 Submission
> Paste your `frame_echo.py`, the `ip neigh` line, both runs, and a screenshot of the `sudo` run into your **Home Task Submission**, then answer the Task 4 questions.

---

> [!tip] The connection
> Task 1 read a record by its own header, and Task 2 read a datagram by its real length: in both, the socket delivered bytes, and only the program decided where a message ended.
> Tasks 3 and 4 wrote headers that the kernel writes for every ordinary socket, first one layer and then all of them.
> A packet carries only what its sender wrote, so nothing in its headers proves who sent it, and a receiver that trusts a field it cannot check is trusting the sender.

---

# Hand In

When all four tasks are done, commit your worksheet and its screenshots once, then push and check that GitHub has everything:

```bash
cd ~/student-YOUR-USERNAME
git add Module1-Network-Attacks-and-Defense/Session2
git commit -m "Module 1 Session 2: home task"
git push
git status
```

**Checkpoint:** `git status` says `Your branch is up to date with 'origin/main'.`, and on GitHub your Home Task Submission shows every screenshot.
If it says **ahead**, the push did not happen: read the error `git push` printed.
Only GitHub's copy counts: until the push succeeds, your work exists only on this machine.

---

# What "done" looks like

- `sni_reader.py` prints `server_name: peer.lab` for the client run with `-servername peer.lab`, and a different line for the run with `-noservername`
- `trunc_detector.py` reports the 12-byte and 64-byte datagrams complete, the 65-, 300- and 1200-byte ones truncated with their real lengths, and a count of 3
- `hdrincl_echo.py`, run with `sudo`, prints a written header with `00 00` in its length, identification and checksum, and a reply whose data is `b'hdrincl'`
- `frame_echo.py` raises `PermissionError` without `sudo`, and with it prints an ICMP type 0 reply from the peer's MAC, an IPv4 checksum that verifies, and `b'frame'`
- Your worksheet holds all four tools' code, output, screenshots and answers, with **Anything that failed** and **AI Assistance** filled in
- On GitHub, `Module1-Network-Attacks-and-Defense/Session2` shows the worksheet with every screenshot, and `git status` says **up to date**
