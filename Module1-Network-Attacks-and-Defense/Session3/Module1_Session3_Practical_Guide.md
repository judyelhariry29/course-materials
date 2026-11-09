# Module 1 · Session 3 — Practical Guide

## Scapy and Raw Packet Crafting

### Professional Training in Cybersecurity I

---

## Overview

Every header you have built so far was a `struct.pack` with a format string, and every length and checksum was worked out separately.
Scapy holds each header as an object with named fields, builds the bytes for you, reads bytes back into fields, and sends, matches and captures packets on a real link.
This lab uses Scapy on your Kali machine against a **target**, a container on a lab network that Docker runs inside Kali.
In this practical session, you will:

1. Install Scapy in this session's virtual environment, and start the lab network and its target
2. Rebuild your own hand-built frame as **layer objects**, and compare the two byte for byte
3. **Dissect** two captured frames back into fields, and find where the data stops
4. **Probe** the target with `sr1`, read its reply, and probe an address no host holds
5. **Capture** an exchange with a callback on each packet, and save it as a **pcap** file
6. Choose at least one of: `send` against `sendp`, timeouts and retries, a binding overridden by hand
7. Solve **CTF Challenge 1**: rebuild the message the target accepted, from segments a damaged link delivered
8. Document everything in your Practical Guide Submission

**Primary lab environment:** Kali Linux VM, Docker inside Kali running the lab network, VS Code, Python virtual environment.

> [!note] Offline first, then on the wire
> Exercises 1 and 2, and Exercise 7 if you choose it, build and read packets in memory: they need neither the lab nor any privilege.
> Exercises 3 to 6 and the CTF put packets on the lab link, so they need the lab up and run under `sudo`.

> [!warning] Your own lab only
> Every packet in this guide goes to the lab network inside your own Kali machine, `10.10.3.0/24`, and nowhere else.
> Scapy writes any header you ask for, including forged and malformed ones, and it sends them as easily as correct ones.
> Never point a Scapy send, probe or capture at a network that is not yours.

> [!example] 📝 Submission
> Work in **Module1_Session3_Practical_Guide_Submission.md** throughout: paste your code, terminal output, and answers into its slots as you go.
> Guided exercises give you a starter with `# TODO` gaps **in this guide**.
> Copy it out, complete it in your IDE, and paste your finished code into the Submission.
> From-scratch exercises leave the slot empty for your own solution.

> [!important] You must complete
> Exercises 1 to 4 + **at least one** choice exercise (5–7) + CTF Challenge 1.

---

# Pre-Session Setup

---

## Step 1: Start the session in your repository

Every session starts the same way: pull your own repository, which brings this session's guide, its Home Task and both worksheets.
Pull `course-materials` too, where the Tooling Reference, the Troubleshooting FAQ and the session's presentation are.

```bash
cd ~/course-materials
git pull
cd ~/student-YOUR-USERNAME
git pull
ls Module1-Network-Attacks-and-Defense/Session3
```

**Checkpoint:** `ls` lists `Module1_Session3_Practical_Guide.md`, `Module1_Session3_Home_Task.md`, the two `_Submission.md` worksheets and `screenshots`.
In Obsidian, open the Practical Guide worksheet, then right-click **Module1_Session3_Practical_Guide.md** and choose **Open to the right**, so this guide sits beside it.

> [!important] Fill in the worksheets only
> Never edit, move or delete the guide or the Home Task in your repository.
> Your instructor's fixes arrive in them through `git pull`, and a changed copy stops that pull.

## Step 2: A working folder for your code

> [!note] Why the code lives outside your repository
> Your repository holds what you hand in: the worksheets and their screenshots.
> The scripts you write today, the lab's compose file and this session's virtual environment live in a folder of their own, at the same path the session has in your repository, under `~/cyberlabs`.
> Your code reaches your instructor by being pasted into the worksheet.

1. **Create the folder and open it in VS Code:**

   ```bash
   mkdir -p ~/cyberlabs/Module1-Network-Attacks-and-Defense/Session3
   code ~/cyberlabs/Module1-Network-Attacks-and-Defense/Session3
   ```

2. **Trust the folder.**
   The first time VS Code opens it, a window asks *Do you trust the authors of the files in this folder?*
   You made the folder yourself, so click **Yes, I trust the authors**.
3. **Open the built-in terminal** with **Terminal**, then **New Terminal**.
   Its prompt ends in `~/cyberlabs/Module1-Network-Attacks-and-Defense/Session3`.
   **Run every command in this guide in this terminal**, unless a step says otherwise.

## Step 3: This session's virtual environment and Scapy

Every session gets a virtual environment of its own, inside its working folder, so what one session installs never reaches another.
Create it, activate it, and install Scapy 2.8.0 into it:

```bash
python3 -m venv .venv
source .venv/bin/activate
which python3   # should end in Session3/.venv/bin/python3
python3 -m pip install scapy==2.8.0
python3 -c "import scapy; print(scapy.__version__)"
```

The last command prints the version the virtual environment holds:

```
2.8.0
```

Your prompt now starts with `(.venv)`.
Every new terminal you open in this folder activates it by itself, because VS Code finds `.venv` and runs the same `source` line for you.
Scapy is pure Python and needs no other package.
Kali also ships an older Scapy of its own, which this session never uses.

Each code block in this guide begins with a **tag line**, a comment that names the file to save the block as:

- `@starter` marks a starter for a guided exercise: copy it out, complete its `# TODO`s in the editor, and keep the finished version for your Submission.
- `@generator` marks a program that writes the files an exercise uses: run it as given.
- `@infra` marks any other complete file you save and use as given.

The tag is a comment, so Python and Docker ignore it: copy the whole block, tag included.

## Step 4: Running Scapy as root

Building and reading packets needs no privilege.
**Sending and capturing do:** every Scapy send and capture opens a packet socket, and the kernel opens one only for a process that holds `CAP_NET_RAW`.
Root holds it, so those programs run under `sudo`, with the virtual environment's own Python named by its path:

```bash
sudo .venv/bin/python -c "import scapy; print(scapy.__version__)"
```

It asks for your Kali password, then prints:

```
2.8.0
```

> [!tip] Why not `sudo python3`
> `sudo` runs a command with its own fixed search path, which never includes `.venv`, even while it is activated.
> So `sudo python3` starts Kali's own Python, with Kali's older Scapy, and every printed version and default can differ from this guide's.
> Always write `sudo .venv/bin/python`.

## Step 5: Start the lab

The lab is one network and one host, described in a **compose file** that Docker runs inside Kali.
The network is a bridge named `m1s3-lab` on `10.10.3.0/24`.
Kali is its gateway, `10.10.3.1`, and the **target** is a container at `10.10.3.10` with the fixed MAC address `02:42:0a:0a:03:0a`.
Because the addresses are fixed, your packets carry the same addresses and checksums as this guide's.

Create a `lab` folder in your working folder, and save this as `lab/compose.yaml`:

```yaml
# @infra compose.yaml
# @expect from lab/: "docker compose up -d" starts m1s3-target-1, the bridge m1s3-lab holds 10.10.3.1/24, and the target 10.10.3.10 answers ping
name: m1s3
services:
  target:
    image: alpine:3.24
    hostname: target
    init: true
    command: ["sleep", "infinity"]
    networks:
      lab:
        ipv4_address: 10.10.3.10
        mac_address: "02:42:0a:0a:03:0a"
networks:
  lab:
    driver: bridge
    driver_opts:
      com.docker.network.bridge.name: m1s3-lab
    ipam:
      config:
        - subnet: 10.10.3.0/24
          gateway: 10.10.3.1
```

Start it from the `lab` folder, and check it:

```bash
mkdir -p lab
cd lab
docker compose up -d
docker compose ps
ip -br -4 addr show m1s3-lab
ping -c 2 10.10.3.10
cd ..
```

The first `up` also downloads the `alpine:3.24` image, which needs Kali's internet connection once.

```
(.venv) $ mkdir -p lab
(.venv) $ cd lab
(.venv) $ docker compose up -d
 Network m1s3_lab  Creating
 Network m1s3_lab  Created
 Container m1s3-target-1  Creating
 Container m1s3-target-1  Created
 Container m1s3-target-1  Starting
 Container m1s3-target-1  Started
(.venv) $ docker compose ps
NAME            IMAGE         COMMAND            SERVICE   CREATED                  STATUS                  PORTS
m1s3-target-1   alpine:3.24   "sleep infinity"   target    Less than a second ago   Up Less than a second   
(.venv) $ ip -br -4 addr show m1s3-lab
m1s3-lab         UP             10.10.3.1/24 
(.venv) $ ping -c 2 10.10.3.10
PING 10.10.3.10 (10.10.3.10) 56(84) bytes of data.
64 bytes from 10.10.3.10: icmp_seq=1 ttl=64 time=0.071 ms
64 bytes from 10.10.3.10: icmp_seq=2 ttl=64 time=0.056 ms

--- 10.10.3.10 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1022ms
rtt min/avg/max/mdev = 0.056/0.063/0.071/0.007 ms
(.venv) $ cd ..
```

**Checkpoint:** `docker compose ps` lists `m1s3-target-1` as `Up`, the bridge `m1s3-lab` holds `10.10.3.1/24`, and `ping` reports `2 received`.
The lab stays up for the rest of the session.

> [!tip] How this guide shows a terminal
> The transcripts were recorded on Kali against this lab, and shorten the prompt to `(.venv) $`.
> Times, the container's age and the bridge's own MAC address differ in your run: Docker gives the bridge a new MAC at every `up`.
> Everything else in a transcript is what your run prints.

---

# Exercises

---

| Exercise | Status | Needs | Type | Difficulty |
|----------|--------|-------|------|------------|
| Exercise 1: Rebuild the Reference Frame With Layer Objects | **Required** | nothing | Guided (starter in guide) | ⭐ Easy |
| Exercise 2: Dissect a Frame From Its Bytes | **Required** | nothing | Guided (starter in guide) | ⭐ Easy |
| Exercise 3: Probe the Target With `sr1` | **Required** | the lab, `sudo` | Guided (starter in guide) | ⭐⭐ Medium |
| Exercise 4: Capture an Exchange and Save It as pcap | **Required** | the lab, `sudo` | Guided (starter in guide) | ⭐⭐ Medium |
| Exercise 5: `send` and `sendp`: The Same Bytes on the Wire | **Choose ≥1** | the lab, `sudo` | From Scratch | ⭐⭐ Medium |
| Exercise 6: Timeouts and Retries Against a Silent Address | **Choose ≥1** | the lab, `sudo` | From Scratch | ⭐ Easy |
| Exercise 7: An Explicit Value Overrides the Binding | **Choose ≥1** | nothing | From Scratch | ⭐ Easy |

---

# Required Exercises

---

## Exercise 1: Rebuild the Reference Frame With Layer Objects — REQUIRED

> **🧩 GUIDED: complete the starter below** | Difficulty: ⭐ Easy
> *Rebuild the 59-byte reference frame with Scapy, compare it with the frame you built by hand, and read the fields the build computed.*

> [!note] Concept note
> You built the reference frame by hand once, one `struct.pack` per header, from the inside out (each call joined onto one line here):
>
> ```text
> tcp = struct.pack("!HHLLBBHHH", SRC_PORT, DST_PORT, SEQ, ACK, data_offset, FLAGS, WINDOW, TCP_CHECKSUM, 0)
> ip = struct.pack("!BBHHHBBH4s4s", version_ihl, 0x00, total_length, 0x1C46, 0x4000, 64, PROTO_TCP, IP_CHECKSUM, SRC_IP, DST_IP)
> eth = struct.pack("!6s6sH", DST_MAC, SRC_MAC, ETHERTYPE_IPV4)
> ```
>
> Every field there is a position in a format string, and the total length and both checksums were worked out separately and copied in.
> A **layer object** holds one header as named fields instead: `IP(src="10.0.0.4")` is one IPv4 header with its source set.
> A field that no argument sets keeps its **default**, such as TTL 64.
> A **computed field**, such as a length or a checksum, stays `None` until the packet is **built** into bytes with `raw()`, and the build fills it from the rest.
> The `/` operator stacks layers from the outside in, `Ether(...) / IP(...) / TCP(...) / b"hello"`, and each lower layer's next-protocol field is written for the layer stacked on it.
> **Dissecting** runs the other way: `Ether(frame_bytes)` reads bytes back into layer objects, every computed field now holding its value.

The reference frame's values, the ones your build set by hand:

| Layer | Field | Value |
|---|---|---|
| Ethernet | destination, source | `08:00:27:ab:cd:ef`, `08:00:27:12:34:56` |
| IPv4 | source, destination | `10.0.0.4`, `10.0.2.5` |
| IPv4 | identification, flags | `0x1C46`, `DF` |
| TCP | source port, destination port | `50000`, `80` |
| TCP | sequence, acknowledgment | `SEQ`, `ACK` (given in the starter) |
| TCP | flags, window | `PA` (PSH and ACK), `0xFFFF` |
| data | | `b"hello"` |

Every other field of the frame is a class default or a computed field.

Your own build wrote its frame to `built_frame.bin`, in that earlier session's working folder.
Check that it is still there:

```bash
ls -l ~/cyberlabs/Module1-Network-Attacks-and-Defense/Session1/built_frame.bin
```

> [!tip] When `built_frame.bin` is gone
> Copy your completed `build_frame.py` from that session's Practical Guide Submission, in your repository, into `~/cyberlabs/Module1-Network-Attacks-and-Defense/Session1`, and run it there with `python3 build_frame.py`.
> It writes `built_frame.bin` before it compares anything.

Complete the three TODOs in `rebuild_frame.py`:

```python
# @starter rebuild_frame.py
"""rebuild_frame.py: rebuild the reference frame with Scapy and compare it with your own build"""
import sys
from pathlib import Path

from scapy.all import Ether, IP, TCP, raw

if len(sys.argv) != 2:
    sys.exit("usage: python3 rebuild_frame.py PATH_TO_built_frame.bin")
own_build = Path(sys.argv[1]).read_bytes()

SEQ, ACK = 0x001A2B3C, 0x00E5F6A7

# TODO 1: build scapy_packet as four layers stacked with /, from the outside in:
#   Ether, IP and TCP with the values in the table above, then b"hello".
#   Set only the fields the table lists: the classes supply everything else.
scapy_packet = Ether() / IP() / TCP()
print("before the build:", "IPv4 len", scapy_packet[IP].len, "IPv4 chksum", scapy_packet[IP].chksum,
      "TCP chksum", scapy_packet[TCP].chksum)

# TODO 2: build scapy_packet into its bytes, and store them in scapy_frame.
scapy_frame = b""
print(len(scapy_frame), "bytes:", scapy_frame.hex(" "))
print("identical to your own build:", scapy_frame == own_build)

# TODO 3: dissect scapy_frame back into layer objects, from its outermost layer,
#   and store the result in built_packet.
built_packet = None
print("after the build:", "IPv4 len", built_packet[IP].len, "IPv4 chksum", hex(built_packet[IP].chksum),
      "TCP chksum", hex(built_packet[TCP].chksum))
print("objects equal:", built_packet == scapy_packet)
```

**Run it** with the path of your own build:

```bash
python3 rebuild_frame.py ~/cyberlabs/Module1-Network-Attacks-and-Defense/Session1/built_frame.bin
```

It prints five lines.
The third must read `identical to your own build: True`: until it does, compare the 59 bytes it prints with your build's, and the first byte that differs names the field to check.

**Answer from your run** (paste each into the Submission):

1. The line printed after the build.
   - **1a.** What total length did the build write into IPv4?
   - **1b.** Which IPv4 checksum did it compute, in hex?
   - **1c.** Which TCP checksum did it compute, in hex?
2. The last line.
   - **2a.** Did `built_packet == scapy_packet` print `True` or `False`?

> [!example] 📝 Submission
> Paste your completed `rebuild_frame.py`, the `ls` line, its output, and a screenshot of the run, then answer the Exercise 1 questions.

---

## Exercise 2: Dissect a Frame From Its Bytes — REQUIRED

> **🧩 GUIDED: complete the starter below** | Difficulty: ⭐ Easy
> *Dissect two captured frames you did not build, read their fields by layer, and find where each one's data stops.*

> [!note] Concept note
> Received bytes carry no layer objects: each header must tell a reader which protocol follows and where it starts.
> **Dissection** answers both from the outermost header in.
> The next-protocol field picks the next class (Ethernet's type, IPv4's protocol, IPv6's next header), and a length places it.
> Where no class is bound to a value, dissection stops, and Scapy keeps the remaining bytes as one `Raw` layer.
> A layer is reached by its class, `frame[UDP]`, and a field by one more dot, `frame[UDP].dport`.
> `UDP in frame` tests for a layer first, because indexing a layer the frame does not carry raises `IndexError`.
> A length also says where a packet **ends**.
> Ethernet will not carry a frame shorter than 60 bytes, so a short packet arrives with zero bytes after it.
> IPv4's total length and IPv6's payload length stop the packet before those bytes, and Scapy keeps them apart from the data, as a **`Padding`** layer.

Save this as `make_frames.py` and run it.
It writes the two frames, byte for byte, as a capture holds them:

```python
# @generator make_frames.py
# @expect writes frame_a.bin (78 bytes) and frame_b.bin (60 bytes)
"""make_frames.py: write two captured frames to disk, byte for byte, for dissection"""

# Each frame exactly as a capture holds it, 16 bytes to a row. Nothing here
# marks where one header ends and the next begins: dissection finds that.
FRAME_A_HEX = (
    "08 00 27 ab cd ef 08 00 27 12 34 56 86 dd 60 00 "
    "00 00 00 18 11 40 fd 00 00 00 00 00 00 00 00 00 "
    "00 00 00 00 00 04 fd 00 00 00 00 00 00 00 00 00 "
    "00 00 00 02 00 05 9c 40 1e 61 00 18 79 3d 73 65 "
    "6e 73 6f 72 3d 37 3b 74 65 6d 70 3d 32 31"
)
FRAME_B_HEX = (
    "08 00 27 ab cd ef 08 00 27 12 34 56 08 00 45 00 "
    "00 1e 2b 2b 40 00 40 11 f9 9b 0a 00 00 04 0a 00 "
    "02 05 9c 40 1e 61 00 0a bf c4 6f 6b 00 00 00 00 "
    "00 00 00 00 00 00 00 00 00 00 00 00"
)

for name, frame_hex in (("frame_a.bin", FRAME_A_HEX), ("frame_b.bin", FRAME_B_HEX)):
    frame_bytes = bytes.fromhex(frame_hex)
    with open(name, "wb") as out:
        out.write(frame_bytes)
    print(f"wrote {name}: {len(frame_bytes)} bytes")
```

```bash
python3 make_frames.py
```

```
wrote frame_a.bin: 78 bytes
wrote frame_b.bin: 60 bytes
```

Complete the three TODOs in `dissect_frame.py`:

```python
# @starter dissect_frame.py
"""dissect_frame.py: dissect one captured frame and read its fields by layer"""
import sys

from scapy.all import Ether, IP, IPv6, UDP, Raw, Padding

if len(sys.argv) != 2:
    sys.exit("usage: python3 dissect_frame.py FRAME_FILE")
with open(sys.argv[1], "rb") as capture:
    frame_bytes = capture.read()

# TODO 1: dissect frame_bytes, from its outermost layer, and store the result in frame.
frame = None
print(len(frame_bytes), "bytes:", frame.summary())

# TODO 2: when the frame carries IPv6, print its source, destination, hop limit
#   and payload length, the way the IPv4 lines below print IPv4's fields.
#   Its fields are named src, dst, hlim and plen.
if IP in frame:
    print("IPv4", frame[IP].src, ">", frame[IP].dst, "TTL", frame[IP].ttl,
          "total length", frame[IP].len)

# TODO 3: when the frame carries UDP, print its two ports and its length field,
#   and when it carries Raw, print the data: Raw holds it in its field load.
if Padding in frame:
    print("padding:", len(frame[Padding].load), "bytes")
```

**Run it** on each frame:

```bash
python3 dissect_frame.py frame_a.bin
python3 dissect_frame.py frame_b.bin
```

Each run prints the frame's size and one summary line, then a line for each layer it carries.

**Answer from your run:**

1. `frame_a.bin`.
   - **1a.** What summary line did Scapy print?
   - **1b.** What is the IPv6 hop limit?
   - **1c.** What data does the `Raw` layer hold?
2. `frame_b.bin`.
   - **2a.** What summary line did Scapy print?
   - **2b.** What total length does the IPv4 header give?
   - **2c.** What data does the `Raw` layer hold?
   - **2d.** How many bytes of padding follow it?

> [!example] 📝 Submission
> Paste your completed `dissect_frame.py`, the output of both runs, and a screenshot of the two runs, then answer the Exercise 2 questions.

---

## Exercise 3: Probe the Target With `sr1` — REQUIRED

> **🧩 GUIDED: complete the starter below** | Difficulty: ⭐⭐ Medium
> *Send an ICMP echo request to the target with `sr1`, read the reply it matched, and probe an address that no host holds.*

> [!note] Concept note
> A probe learns something only from its reply: a tool must catch it, tell it from every other packet on the link, and notice when none comes.
> **Send-and-receive** does all three.
> `sr1(packet, timeout=2)` sends the packet, waits up to 2 seconds after the send, and returns the first packet that answers it, or `None` when nothing answered in time.
> A reply is matched by its fields: its addresses are the request's reversed, and an echo reply repeats the request's identifier and sequence number.
> `reply.answers(request)` runs that same test on two packets.
> You give `sr1` the packet from IPv4 up.
> Scapy picks the interface from its own routing table, finds the next hop's MAC address with a lookup of its own, and writes the Ethernet header itself.
> Every send opens a packet socket, so the program needs `CAP_NET_RAW`, and runs under `sudo`.
>
> The request is the one you built by hand over a raw socket, now as layer objects:
>
> | Field | Value |
> |---|---|
> | ICMP type, code | `8`, echo request (Scapy's `ICMP` default), `0` |
> | identifier, sequence number | `0x1234`, `1` |
> | data | `b"hello"` |

Complete the three TODOs in `probe.py`:

```python
# @starter probe.py
"""probe.py: send one ICMP echo request with sr1 and read the reply"""
import sys
import time

from scapy.all import IP, ICMP, Raw, conf, raw, sr1

conf.verb = 0
if len(sys.argv) != 2:
    sys.exit("usage: sudo .venv/bin/python probe.py TARGET_ADDRESS")
target_address = sys.argv[1]

# TODO 1: build probe_request: IPv4 to target_address, then ICMP with the
#   identifier and sequence number in the table above (fields id and seq), then b"hello".
probe_request = IP()
print("request:", probe_request.summary(), "-", len(raw(probe_request)), "bytes from IPv4 up")

start = time.monotonic()
# TODO 2: send probe_request with sr1, waiting at most 2 seconds, and store
#   what it returns in target_reply.
target_reply = None
elapsed = time.monotonic() - start

if target_reply is None:
    print(f"no reply: sr1 returned None after {elapsed:.2f} s")
else:
    print(f"reply after {elapsed:.2f} s:", target_reply.summary())
    print("from", target_reply[IP].src, "to", target_reply[IP].dst)
    print("ICMP type", target_reply[ICMP].type, "identifier", hex(target_reply[ICMP].id),
          "sequence", target_reply[ICMP].seq)
    print("data:", target_reply[Raw].load)
    # TODO 3: print whether target_reply answers probe_request, with answers().
```

**Run it** three times.

1. **Without privilege** first:

   ```bash
   python3 probe.py 10.10.3.10
   ```

   It prints the request, and then `sr1` fails before anything is sent.

2. **Under `sudo`**, against the target:

   ```bash
   sudo .venv/bin/python probe.py 10.10.3.10
   ```

   It prints the request, the reply's summary and four lines read from the reply's fields.

3. **Under `sudo`**, against `10.10.3.99`, an address on the lab link that no host holds:

   ```bash
   sudo .venv/bin/python probe.py 10.10.3.99
   ```

   Scapy's MAC lookup finds no host and prints a `WARNING`, and the request goes out to the broadcast address instead.

**Answer from your run:**

1. The run without privilege.
   - **1a.** What is the last line of its traceback?
2. The run against the target.
   - **2a.** What summary line did the reply print?
   - **2b.** What did `answers()` return?
3. The run against `10.10.3.99`.
   - **3a.** What was the last line it printed?

> [!example] 📝 Submission
> Paste your completed `probe.py`, all three runs, and a screenshot of the two runs under `sudo`, then answer the Exercise 3 questions.

---

## Exercise 4: Capture an Exchange and Save It as pcap — REQUIRED

> **🧩 GUIDED: complete the starter below** | Difficulty: ⭐⭐ Medium
> *Capture three echo exchanges in the background while your program sends them, print one line per packet, then save the capture to a pcap file and read it back.*

> [!note] Concept note
> Reading the packets that cross an interface, including ones you did not send, is **capture**.
> A capture makes four choices: the interface to listen on (`iface`), the packets to keep (`filter`), what to do with each one (`prn`), and whether to store it (`store`, on by default).
> A `filter` is a **BPF** expression such as `"icmp"`: libpcap compiles it, and the kernel runs it before Python sees a packet.
> `prn` is a function called on each kept packet, and its return value is printed, so a function that returns one line of fields prints one line per packet.
> `sniff()` blocks until it is done, so a program that must also send uses `AsyncSniffer`, the same capture in a thread: `start()` it, send, then `stop()` returns the list.
> `start()` returns **before** the capture's socket is open, so a program that sends at once can miss its own packets.
> `started_callback` is a function the sniffer calls once its socket is open, and waiting for it closes that gap.
> A **pcap** file stores a capture as the bytes on the wire: `wrpcap` writes a packet list to one, `rdpcap` reads it back, and other capture tools read the same file.

Complete the three TODOs in `capture_echo.py`:

```python
# @starter capture_echo.py
"""capture_echo.py: capture three echo exchanges, print a line per packet, save and reload them"""
import sys
import threading

from scapy.all import IP, ICMP, AsyncSniffer, conf, raw, rdpcap, sr, wrpcap

conf.verb = 0
if len(sys.argv) != 3:
    sys.exit("usage: sudo .venv/bin/python capture_echo.py INTERFACE TARGET_ADDRESS")
interface, target_address = sys.argv[1], sys.argv[2]


def show(packet):
    """Called on each captured packet: its return value is printed."""
    # TODO 1: return one line with the packet's IPv4 source and destination,
    #   and its ICMP type and sequence number, such as "A > B type T seq S".
    return ""


sniffer_ready = threading.Event()
# TODO 2: make sniffer an AsyncSniffer on interface that keeps only ICMP,
#   calls show on each packet, and calls sniffer_ready.set once its socket is open.
sniffer = None
sniffer.start()
sniffer_ready.wait()

probe_requests = [IP(dst=target_address) / ICMP(id=0x1234, seq=n) / b"hello" for n in (1, 2, 3)]
answered, unanswered = sr(probe_requests, timeout=2)
print("answered", len(answered), "unanswered", len(unanswered))

captured = sniffer.stop()
print("captured", captured)

# TODO 3: write captured to "echo3.pcap", then read it back into read_back.
read_back = []
print("wrote echo3.pcap")
print("read back", read_back)
print("same bytes:", [raw(sent) == raw(loaded) for sent, loaded in zip(captured, read_back)])
```

**Run it** under `sudo`, then read the file it wrote with `tcpdump`, a capture tool of its own, under `sudo` too:

```bash
sudo .venv/bin/python capture_echo.py m1s3-lab 10.10.3.10
sudo tcpdump -r echo3.pcap -nn
```

`capture_echo.py` prints one `show` line per captured packet, the counts, the captured list, and the comparison of every packet with its copy read back from the file.
`tcpdump -r` prints one line per packet in the file.
The program ran under `sudo`, so the file it wrote belongs to root, and your own user cannot read it: that is why `tcpdump` runs under `sudo` as well.

**Answer from your run:**

1. The capture.
   - **1a.** How many lines did `show` print?
   - **1b.** What did `show` print for the reply to sequence number 2?
   - **1c.** What did `print("captured", captured)` print?
2. The pcap file.
   - **2a.** What did the `same bytes:` line print?
   - **2b.** Which identifier does `tcpdump` print for the requests, in decimal?

> [!example] 📝 Submission
> Paste your completed `capture_echo.py`, its output, the `tcpdump` output, and a screenshot of both, then answer the Exercise 4 questions.

---

# Choice Exercises — Pick At Least 1

---

> [!tip] From scratch
> These exercises give you requirements and no starter.
> Reuse anything you wrote today: Exercise 4's `capture_echo.py` is a good start for Exercise 5, and Exercise 3's `probe.py` for Exercise 6.

## Exercise 5: `send` and `sendp`: The Same Bytes on the Wire

> **🔨 FROM SCRATCH** | Difficulty: ⭐⭐ Medium

> [!note] Concept note
> A packet reaches the link only inside a frame: something must pick the interface it leaves by and write the Ethernet header in front of it.
> `send(packet)` takes the packet from IPv4 up and does both itself, from Scapy's own route and MAC lookups.
> `sendp(frame, iface=...)` takes the whole frame from Ethernet up, sends it on the interface you name, and adds no layer.
> So `send` is Scapy's layer-3 send and `sendp` its layer-2 send, and a frame built with the right destination MAC reaches the wire as the same bytes either way.

**Write one program**, `send_both.py`, that runs under `sudo` and takes three arguments: the interface, the target's address and the target's MAC address.

- It builds one packet from IPv4 up: the reference frame's IPv4 and TCP values from Exercise 1, with the target's address as the destination and no source set, then `b"hello"`.
- It captures on the interface, in the background, the TCP packets to the target's port 80, and waits until the capture is ready before it sends.
- It sends the packet once with `send`, then once with `sendp`, inside an `Ether` layer whose destination is the target's MAC, on the interface given.
- It prints the length and summary of each of the two captured frames, and whether their bytes are identical.

```bash
sudo .venv/bin/python send_both.py m1s3-lab 10.10.3.10 02:42:0a:0a:03:0a
```

**Answer from your run:**

1. The two captured frames.
   - **1a.** Were their bytes identical?

> [!example] 📝 Submission
> Paste `send_both.py`, its output, and a screenshot of the run, then answer the Exercise 5 questions.

---

## Exercise 6: Timeouts and Retries Against a Silent Address

> **🔨 FROM SCRATCH** | Difficulty: ⭐ Easy

> [!note] Concept note
> `timeout` is how long `sr` waits after its last send, in seconds.
> Left unset, `sr` waits for an unanswered request until it is interrupted, so every probe sets one.
> `retry=2` sends each request still unanswered twice more, one round after another.
> To an address no host holds, every round also pays for Scapy's own MAC lookup before it sends.
> An empty answer list is a result too: nothing answered before the timeout.

**Write one program**, `retries.py`, that runs under `sudo` and takes one or more addresses as arguments.

- For each address, it sends one ICMP echo request with `sr(..., timeout=1, retry=2)`.
- It times each call with `time.monotonic()`, and prints the address, the number answered, the number unanswered and the seconds the call took.

```bash
sudo .venv/bin/python retries.py 10.10.3.10 10.10.3.99
```

**Answer from your run:**

1. The two calls.
   - **1a.** How long did the call to `10.10.3.10` take?
   - **1b.** How long did the call to `10.10.3.99` take?
   - **1c.** How many `WARNING` lines did the call to `10.10.3.99` print?

> [!example] 📝 Submission
> Paste `retries.py`, its output, and a screenshot of the run, then answer the Exercise 6 questions.

---

## Exercise 7: An Explicit Value Overrides the Binding

> **🔨 FROM SCRATCH** | Difficulty: ⭐ Easy

> [!note] Concept note
> A **binding** is Scapy's rule that writes a lower layer's next-protocol field for the layer stacked on it: IPv6's next header, `nh`, becomes 6 above TCP.
> A binding fills only a field left unset, so a value set by hand stays.
> Every reader follows that field, Scapy's dissection included, so the same TCP bytes under a different next header are read as a different protocol.
> Scapy checks no such value against the layer above it.

**Write one program**, `override.py`, that needs no privilege.

- It builds one TCP layer with the reference frame's TCP values from Exercise 1, then `b"hello"`.
- It builds that layer under `IPv6(src="fd00::4", dst="fd00::2:5")` twice, once with `nh` left to the binding and once with `nh=17`, and takes the bytes of each.
- It dissects each from its IPv6 header with `IPv6(...)`, and prints the next header it reads, the length in bytes and the summary.
- For the one read as UDP, it also prints the UDP length field and how many bytes Scapy kept as data.
- It prints whether the bytes after the 40-byte IPv6 header are identical in the two builds.

```bash
python3 override.py
```

**Answer from your run:**

1. The build with `nh=17`.
   - **1a.** What summary line did Scapy print?
   - **1b.** Which value did Scapy read as the UDP length field?

> [!example] 📝 Submission
> Paste `override.py`, its output, and a screenshot of the run, then answer the Exercise 7 questions.

---

# CTF Challenge — Solve Challenge 1

---

The CTF runs on Kali and the lab: a given sender on Kali sends a burst of TCP segments across the lab link to the target, and you write the solver that captures them.

| Challenge | Status | Difficulty | Skill |
|-----------|--------|------------|-------|
| Challenge 1: Rebuild the Message the Receiver Accepted | **Required** | ⭐⭐ Medium | capture with a filter, a checksum checked by a rebuild, ordering by sequence number |

> [!important] You must complete
> Challenge 1.

## Setup: save the challenge sender

Save this as `ctf_service.py` in your working folder.
Do not run it yet: the challenge says when.

```python
# @infra ctf_service.py
# @expect under sudo with the target's address 10.10.3.10: prints "sending 15 segments to 10.10.3.10" and "sent", and exits; a capture on m1s3-lab sees 14 segments to port 31337, 1 to port 31338, and 8 RSTs from the target, 7 of them from port 31337
"""ctf_service.py: the CTF's sender: one burst of TCP segments across the lab link to the target"""
import random
import sys

from scapy.all import IP, TCP, conf, raw, send

conf.verb = 0
if len(sys.argv) != 2:
    sys.exit("usage: sudo .venv/bin/python ctf_service.py TARGET_ADDRESS")
target_address = sys.argv[1]

SENDER_PORT, MESSAGE_PORT, NOTE_PORT = 40404, 31337, 31338
FIRST_SEQ = 1000
# The message is stored XORed, only so that it is not plain text in this file.
HIDDEN = bytes.fromhex("1c161b1d216a343623052c6e366b3e0529693d3769342e2905396a2f342e27")
COPY = b"FLAG{r34d_th3_byt3s_n0t_th3_ck}"
NOTE = b"FLAG{gr3p_f1nds_th3_wr0ng_0n3}"
CUTS = (0, 4, 9, 13, 17, 22, 26, 31)


def segment(port, seq, data, corrupt=False):
    built = IP(dst=target_address) / TCP(sport=SENDER_PORT, dport=port, seq=seq, flags="PA") / data
    if corrupt:
        # The same segment with its checksum damaged, as a bad link would leave it.
        good_checksum = IP(raw(built))[TCP].chksum
        built[TCP].chksum = good_checksum ^ 0x0F0F
    return built


message = bytes(byte ^ 0x5A for byte in HIDDEN)
burst = [segment(NOTE_PORT, FIRST_SEQ, NOTE)]
for start, end in zip(CUTS, CUTS[1:]):
    burst.append(segment(MESSAGE_PORT, FIRST_SEQ + start, message[start:end]))
    burst.append(segment(MESSAGE_PORT, FIRST_SEQ + start, COPY[start:end], corrupt=True))
random.Random(31337).shuffle(burst)

print("sending", len(burst), "segments to", target_address)
send(burst, inter=0.05)
print("sent")
```

It sends its burst once, in about one second, and exits.
Run it again whenever you need the burst again:

```
(.venv) $ sudo .venv/bin/python ctf_service.py 10.10.3.10
sending 15 segments to 10.10.3.10
sent
```

## Challenge 1: Rebuild the Message the Receiver Accepted — REQUIRED

> **🚩 CTF** | Difficulty: ⭐⭐ Medium

> [!note] Brief
> A sender split a message into TCP segments to the target's port 31337, each segment's sequence number giving its data's position in the message.
> The link damaged the burst: every piece also arrives as a second copy, with the same sequence number, other bytes and a checksum that fails.
> A receiver's kernel checks each segment's checksum and drops any that fails, then places the data it kept by sequence number.
> The target is a real receiver: nothing listens on port 31337, so its kernel answers each segment it accepted with a RST, and stays silent for each one it dropped.
> The flag is the message the target accepted.
> The segments arrive out of order, and one segment to another port carries text shaped like a flag.

**Step 1: look at what you are up against.**
In one terminal, print a summary of every segment for 15 seconds:

```bash
sudo .venv/bin/python -c "from scapy.all import sniff; sniff(iface='m1s3-lab', filter='tcp port 31337', prn=lambda p: p.summary(), timeout=15)"
```

Open a second terminal with **+**, and start the sender there while the first one captures:

```bash
sudo .venv/bin/python ctf_service.py 10.10.3.10
```

**Step 2: solve it in Python** (write `solve1.py`, paste it into your Submission):
- Capture on `m1s3-lab`, with a BPF filter for port 31337 and the target, for long enough to start the sender in your second terminal.
- For each captured segment sent to port 31337, print its sequence number, its data length and its checksum, and whether that checksum verifies.
- Keep only the segments whose checksum verifies, order them by sequence number, and print their data joined together.
- Count the RSTs the target sent back, and print the count beside the number of segments you kept.

**Flag format:** `FLAG{...}`

> [!tip] Hint
> A computed field set to `None` is filled again by the next build.
> So copy a captured packet's IPv4 layer with `.copy()`, set the copy's TCP `chksum` to `None`, build it with `raw()`, dissect it back with `IP(...)`, and compare the checksum the build computed with the one that arrived.
> `bytes(packet[TCP].payload)` is a segment's data, and `"R" in packet[TCP].flags` tests for a RST.
> `sniff()` blocks, so the sender runs in the other terminal.

> [!example] 📝 Submission
> Paste `solve1.py`, its output with every segment and the flag, a screenshot of the solver and the sender side by side, and a one-line approach into your Submission.

### Rules

- **Solve the challenge by writing a Python script.**
  A flag picked out by eye, or by searching the captured bytes for `FLAG{`, earns nothing: the decoys exist to make that fail.
- **Cleanup:** the sender exits by itself and leaves no files behind.
  When you have finished with the lab, stop it from its folder:

  ```bash
  cd lab
  docker compose down
  cd ..
  ```

---

# Hand In

When every exercise you are handing in is done, commit your worksheet and its screenshots once, then push and check that GitHub has everything:

```bash
cd ~/student-YOUR-USERNAME
git add Module1-Network-Attacks-and-Defense/Session3
git commit -m "Module 1 Session 3: practical guide"
git push
git status
```

**Checkpoint:** `git status` says `Your branch is up to date with 'origin/main'.`, and on GitHub your Practical Guide Submission shows every screenshot.
Only GitHub's copy counts: until the push succeeds, your work exists only on this machine.
Your scripts and the lab's compose file stay in `~/cyberlabs/Module1-Network-Attacks-and-Defense/Session3`: the worksheet carries the code you hand in.

---

# What "done" looks like

- `python3 -c "import scapy; print(scapy.__version__)"` and `sudo .venv/bin/python -c "import scapy; print(scapy.__version__)"` both print `2.8.0`
- `docker compose ps` lists `m1s3-target-1` as `Up`, and `ping -c 2 10.10.3.10` reports `2 received`
- `rebuild_frame.py` prints `identical to your own build: True`
- `dissect_frame.py` prints a summary line and the fields of each layer for both frames
- `probe.py` fails without `sudo`, prints the target's reply and the result of `answers()` under `sudo`, and reports no reply from `10.10.3.99`
- `capture_echo.py` prints one `show` line per captured packet and the comparison of every packet with its copy read back, and `sudo tcpdump -r echo3.pcap -nn` reads the file
- At least one of Exercises 5 to 7 prints what its exercise asks for
- `solve1.py` prints every segment with its checksum verdict, the target's RST count, and a flag in the `FLAG{...}` format
- Your worksheet holds every completed exercise's code, output, screenshot and answers, with **Anything that failed** and **AI Assistance** filled in
- On GitHub, `Module1-Network-Attacks-and-Defense/Session3` shows the worksheet with every screenshot, and `git status` says **up to date**
