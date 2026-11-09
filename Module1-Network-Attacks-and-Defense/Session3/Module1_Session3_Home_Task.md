# Module 1 · Session 3 — Home Task

## Scapy and Raw Packet Crafting

### Professional Training in Cybersecurity I

---

> [!note] How this home task works
> The Practical Guide used Scapy to build, dissect, probe and capture, each the way the session first taught it.
> This home task applies the same method on your own, with the parts of Scapy the guide left out.
> You build **four tools** in two parts.
> The first part reads packets without sending anything: one datagram in every view Scapy offers, and frames whose dissection stops early.
> The second part works on the lab link: the echo exchange at layer 2, and a count of the packets each kind of capture filter lets reach Python.
>
> Each task is marked **🧩 GUIDED** or **🔨 FROM SCRATCH**.
> A guided task gives you a starter with `# TODO` gaps, so the plumbing is done and you can focus on the idea.
> A from-scratch task gives you the requirements, and you write the whole script.
>
> Your worksheet is **`Module1_Session3_Home_Task_Submission.md`**, already in your repository's `Module1-Network-Attacks-and-Defense/Session3` folder since the Practical Guide's setup.
> Work in `~/cyberlabs/Module1-Network-Attacks-and-Defense/Session3`, the working folder you made for the Practical Guide, with its `.venv` and its Scapy 2.8.0.
> Paste your finished code, its output, your screenshots and your answers into the worksheet, which is the graded document.

> [!important] Everything here is required
> There are no optional parts: all four tools, every run and every question.
> Every script must run without errors.

> [!warning] Your own lab only
> Tasks 3 and 4 put packets on the lab network inside your own Kali machine, `10.10.3.0/24`, and capture there, so they run under `sudo`.
> Send and capture only on that network, and never point these tools at a network that is not yours.
> Run under `sudo` only the scripts you wrote for these tasks, always as `sudo .venv/bin/python`.

---

# Before You Start

1. **Pull your repository**, because your instructor's feedback on the Practical Guide arrives there:

   ```bash
   cd ~/student-YOUR-USERNAME
   git pull
   ```

2. **Open your working folder** and a new terminal in it:

   ```bash
   code ~/cyberlabs/Module1-Network-Attacks-and-Defense/Session3
   ```

   In VS Code, open **Terminal**, then **New Terminal**.
   It activates `.venv` by itself, so its prompt starts with `(.venv)`.

3. **Start the lab**, which Tasks 3 and 4 need, from the `lab` folder you made in the Practical Guide:

   ```bash
   cd lab
   docker compose up -d
   docker compose ps
   cd ..
   ping -c 2 10.10.3.10
   ```

   `docker compose ps` must list `m1s3-target-1` as `Up`, and `ping` must report `2 received`.
   Tasks 1 and 2 need neither the lab nor `sudo`.

---

# Reading a Packet Without Sending It

*Shared idea: a packet object and its bytes are two views of one thing, and Scapy shows each view on request.*
*Read the object before its build and after it, and read bytes whose dissection stops before the data.*

---

## Task 1: Read One Datagram Before and After Its Build — REQUIRED

> **🧩 GUIDED: complete the starter below** | Difficulty: ⭐ Easy
> *Copy the starter out, fill its three `# TODO` gaps in your IDE, and run it without `sudo`.*

> [!note] Concept note
> Scapy gives a packet four views, and each answers a different question.
> `ls(UDP)` lists a **class**: every field it has, the field's type and its default.
> `.show()` lists an **object** as it is now, so a computed field that the build has not filled yet prints `None`.
> `.show2()` builds the packet first and dissects the bytes back, so it prints every computed field as it will be sent.
> `hexdump()` prints the **bytes** themselves: an offset, 16 bytes in hex, and the same 16 as text, on each row.
> The first three print fields by name, and the last shows where each field sits in the bytes.

The datagram this task reads:

| Layer | Field | Value |
|---|---|---|
| IPv6 | source, destination | `fd00::4`, `fd00::2:5` |
| UDP | source port, destination port | `40000`, `7777` |
| data | | `b"status=ok;uptime=86400"` |

Create `inspect_datagram.py` and complete its three TODOs:

```python
# @starter inspect_datagram.py
"""inspect_datagram.py: read one datagram's fields before its build, after it, and as bytes"""
from scapy.all import IPv6, UDP, hexdump, ls

# TODO 1: build datagram as three layers stacked with /: IPv6 and UDP with the
#   values in the table above, then the data.
datagram = IPv6() / UDP()

print("=== ls(UDP) ===")
ls(UDP)
print("=== show() ===")
datagram.show()
print("=== show2() ===")
# TODO 2: print every field of datagram as it will be sent, computed fields included.
print("=== hexdump() ===")
# TODO 3: print the bytes of datagram, 16 to a row.
```

**Run it** on Kali, without `sudo`:

```bash
python3 inspect_datagram.py
```

It prints four sections.
In the `show()` section, IPv6's `plen` and UDP's `len` and `chksum` must read `None`, and in the `show2()` section they must hold numbers.
The `hexdump()` section's text column must end in the data, `=86400`.

**Answer from your run:**

1. The `show2()` section.
   - **1a.** What payload length (`plen`) does it print for IPv6?
   - **1b.** What length (`len`) does it print for UDP?
   - **1c.** What checksum (`chksum`) does it print for UDP?
2. The `hexdump()` section.
   - **2a.** How many rows does it print?
   - **2b.** How many bytes long is the datagram?

> [!example] 📝 Submission
> Paste your completed `inspect_datagram.py`, its output, and a screenshot of the run into your **Home Task Submission**, then answer the Task 1 questions.

---

## Task 2: Report Where Dissection Stops — REQUIRED

> **🔨 FROM SCRATCH** | Difficulty: ⭐⭐ Medium
> *Read the requirements and write the complete script yourself.*

> [!note] Concept note
> Dissection reads a frame from its outermost header in, and each next-protocol field picks the class of the header that follows.
> When no class is bound to that field's value, dissection stops there: the header that holds the value is the last one named, and every byte after it is kept as one `Raw` layer.
> EtherType `0x88b5` and IPv4 protocol `253` are both reserved for experiments, so Scapy binds no class to either.
> A defender who meets an unfamiliar protocol on a link starts here: which header was the last one understood, and how many bytes after it are still unread.
> `frame.layers()` returns the classes of a dissected frame in order, outermost first, and each class's name is its `__name__`.

Save this as `make_unbound_frames.py` and run it.
It writes three frames, byte for byte, as a capture holds them:

```python
# @generator make_unbound_frames.py
# @expect writes frame_udp.bin, frame_88b5.bin and frame_253.bin, 60 bytes each
"""make_unbound_frames.py: write three captured frames to disk, byte for byte, for triage"""

# Each frame exactly as a capture holds it, 16 bytes to a row. The three differ
# in one next-protocol field each: bytes 12-13 (the EtherType) or byte 23 (the
# IPv4 protocol), with the IPv4 checksum that goes with it.
FRAMES_HEX = {
    "frame_udp.bin": (
        "08 00 27 ab cd ef 08 00 27 12 34 56 08 00 45 00 "
        "00 2e 2b 2c 40 00 40 11 f9 8a 0a 00 00 04 0a 00 "
        "02 05 9c 40 1e 61 00 1a 7f fe 74 65 6c 65 6d 65 "
        "74 72 79 3a 62 61 74 63 68 3d 34 32"
    ),
    "frame_88b5.bin": (
        "08 00 27 ab cd ef 08 00 27 12 34 56 88 b5 45 00 "
        "00 2e 2b 2c 40 00 40 11 f9 8a 0a 00 00 04 0a 00 "
        "02 05 9c 40 1e 61 00 1a 7f fe 74 65 6c 65 6d 65 "
        "74 72 79 3a 62 61 74 63 68 3d 34 32"
    ),
    "frame_253.bin": (
        "08 00 27 ab cd ef 08 00 27 12 34 56 08 00 45 00 "
        "00 2e 2b 2c 40 00 40 fd f8 9e 0a 00 00 04 0a 00 "
        "02 05 9c 40 1e 61 00 1a 7f fe 74 65 6c 65 6d 65 "
        "74 72 79 3a 62 61 74 63 68 3d 34 32"
    ),
}

for name, frame_hex in FRAMES_HEX.items():
    frame_bytes = bytes.fromhex(frame_hex)
    with open(name, "wb") as out:
        out.write(frame_bytes)
    print(f"wrote {name}: {len(frame_bytes)} bytes")
```

```bash
python3 make_unbound_frames.py
```

```
wrote frame_udp.bin: 60 bytes
wrote frame_88b5.bin: 60 bytes
wrote frame_253.bin: 60 bytes
```

Create `where_stops.py`.

**Requirements:**

- Take one or more frame files on the command line (`sys.argv[1:]`), and print a usage line and exit when none is given.
- Dissect each file's bytes from Ethernet, the outermost layer.
- Print one line per frame with the file name, its size in bytes and the names of all its layers in order, joined with ` / `.
- Print a second line with the last layer dissection **named** (the last one that is not `Raw`) and how many bytes `Raw` holds, or `0` when there is no `Raw` layer.
- Use no fixed offsets: every answer comes from the dissected layers.

**Run it** on all three frames at once:

```bash
python3 where_stops.py frame_udp.bin frame_88b5.bin frame_253.bin
```

**What your tool must report:** for `frame_udp.bin`, dissection reaches UDP, and its `Raw` holds the 18 bytes of data.
For the other two, it stops at the header whose next-protocol field has no class, and `Raw` holds everything after that header.

**Answer from your run:**

1. `frame_88b5.bin`.
   - **1a.** Which layer did dissection name last?
   - **1b.** How many bytes does `Raw` hold?
2. `frame_253.bin`.
   - **2a.** Which layer did dissection name last?
   - **2b.** How many bytes does `Raw` hold?

> [!example] 📝 Submission
> Paste your `where_stops.py`, its output, and a screenshot of the run into your **Home Task Submission**, then answer the Task 2 questions.

---

# On the Lab Link

*Shared idea: where a packet enters Scapy decides what it carries.*
*A reply keeps its Ethernet header only when the exchange ran at layer 2, and a capture filter decides which packets reach Python at all.*

---

## Task 3: Run the Echo Exchange at Layer 2 With `srp1` — REQUIRED

> **🧩 GUIDED: complete the starter below** | Difficulty: ⭐⭐ Medium
> *Copy the starter out, fill its three `# TODO` gaps in your IDE, and run it on Kali with `sudo`.*

> [!note] Concept note
> `sr1` takes a packet from IPv4 up: Scapy writes the Ethernet header from its own route and MAC lookups, and the reply it returns starts at IPv4.
> **`srp1`** is the same exchange at layer 2: you give it the whole frame from Ethernet up and name the interface, as with `sendp`, and it returns the reply frame from Ethernet up.
> Its match adds one test before the IPv4 and ICMP ones: the reply's EtherType must equal the request's.
> With the destination MAC set in the frame you build, Scapy runs no MAC lookup, so the frame goes out exactly as written.
> Use `srp1` when the Ethernet fields are part of the question, such as which MAC address a reply came from.

The echo request this task sends:

| Field | Value |
|---|---|
| Ethernet destination | the target's MAC, `02:42:0a:0a:03:0a` |
| IPv4 destination | the target, `10.10.3.10` |
| ICMP identifier, sequence number | `0x2468`, `1` |
| data | `b"layer2"` |

Create `l2_echo.py` and complete its three TODOs:

```python
# @starter l2_echo.py
"""l2_echo.py: send the echo request inside a frame you build with srp1, and compare the reply with sr1's"""
import sys

from scapy.all import Ether, IP, ICMP, conf, srp1, sr1

conf.verb = 0
if len(sys.argv) != 4:
    sys.exit("usage: sudo .venv/bin/python l2_echo.py INTERFACE TARGET_ADDRESS TARGET_MAC")
interface, target_address, target_mac = sys.argv[1:4]

echo_request = IP(dst=target_address) / ICMP(id=0x2468, seq=1) / b"layer2"
# TODO 1: build request_frame: an Ether layer whose destination is target_mac,
#   with echo_request stacked on it.
request_frame = Ether()
print("frame sent:", request_frame.summary())

# TODO 2: send request_frame with srp1 on interface, waiting at most 2 seconds,
#   and store the reply frame in frame_reply.
frame_reply = None
print("srp1 reply:", frame_reply.summary())
print("   Ethernet source", frame_reply[Ether].src, "destination", frame_reply[Ether].dst,
      "type", hex(frame_reply[Ether].type))
print("   Ether in the reply:", Ether in frame_reply)

# TODO 3: send echo_request with sr1, waiting at most 2 seconds, and store the
#   reply in packet_reply.
packet_reply = None
print("sr1 reply: ", packet_reply.summary())
print("   Ether in the reply:", Ether in packet_reply)
```

**Run it** on Kali, with `sudo`, which asks for your Kali password:

```bash
sudo .venv/bin/python l2_echo.py m1s3-lab 10.10.3.10 02:42:0a:0a:03:0a
```

It prints the frame it sent, then the `srp1` reply with three lines read from it, then the `sr1` reply with one line.
The `srp1` reply's Ethernet source must be the target's MAC address.
Its Ethernet destination is your bridge's own MAC, which Docker changes at every `compose up`, so it will not match a classmate's.

**Answer from your run:**

1. The `srp1` reply.
   - **1a.** What summary line did it print?
   - **1b.** What EtherType did it print, in hex?
2. The `sr1` reply.
   - **2a.** What summary line did it print?

> [!example] 📝 Submission
> Paste your completed `l2_echo.py`, its `sudo` run, and a screenshot of the run into your **Home Task Submission**, then answer the Task 3 questions.

---

## Task 4: Count the Packets a Kernel Filter Keeps From Python — REQUIRED

> **🔨 FROM SCRATCH** | Difficulty: ⭐⭐ Medium
> *Read the requirements and write the complete script yourself.*

> [!note] Concept note
> A capture can drop the packets it does not want in two places.
> A `filter` is a BPF expression: libpcap compiles it, and the kernel runs it, so a packet it drops never reaches Python.
> An `lfilter` is a Python function that `sniff()` calls on every packet after dissecting it, and the packet is kept when the function returns `True`.
> Both keep the same packets for the same test, but they differ in how much work reaches your program.
> A new Scapy process that sends to a lab address first runs its own MAC lookup, which puts packets of its own on the link before the echo request: they are not IPv4, and this task counts them without reading any of their fields.
> `sniff()` blocks until it is done, so the sender runs in a second terminal.

Create `count_filter.py`.

**Requirements:**

- Take the interface and a mode, `filter` or `lfilter`, on the command line, and print a usage line and exit for anything else.
- Define one function that counts every call made to it and returns whether the packet carries ICMP (`ICMP in packet`).
- Capture on the interface with `sniff()` and `count=2`, passing that function as `lfilter` in both modes, and in mode `filter` also `filter="icmp"`.
- Before `sniff()` starts, print a line saying the capture is waiting for the sender.
- After it returns, print how many packets reached Python (the function's call count), the list `sniff()` returned, and the summary of each packet kept.

**Run it** twice on Kali, once per mode, each time in two terminals.
In the first terminal, start the capture, and wait for its waiting line:

```bash
sudo .venv/bin/python count_filter.py m1s3-lab filter
```

Open a second terminal with **+**, and send one echo request to the target from a new Scapy process there:

```bash
sudo .venv/bin/python -c "from scapy.all import IP, ICMP, conf, sr1; conf.verb = 0; print(sr1(IP(dst='10.10.3.10') / ICMP(id=0x2468, seq=7) / b'count', timeout=2).summary())"
```

The sender prints the reply's summary line, and the capture in the first terminal returns.
Then do the same with `lfilter` in place of `filter` in the first terminal's command.

**What your tool must report:** in both modes the capture keeps the same two packets, the echo request and its reply, and the two modes report different numbers of packets that reached Python.

**Answer from your run:**

1. The capture in mode `lfilter`.
   - **1a.** How many packets reached Python?

> [!example] 📝 Submission
> Paste your `count_filter.py`, the capture's output from both runs, the sender's line, and a screenshot of both terminals from the `lfilter` run into your **Home Task Submission**, then answer the Task 4 questions.

---

> [!tip] The connection
> Task 1 read one datagram as an object, as fields after its build, and as bytes, and Task 2 found where dissection ran out of classes and left the bytes unread.
> Tasks 3 and 4 decided where a packet enters Scapy: at layer 2, where the reply keeps its Ethernet header, and behind a kernel filter, where the packets you do not want never reach Python.
> A tool that reads traffic is only as good as what it is shown, so choosing the view, the layer and the filter is part of reading a packet correctly.

---

# Hand In

When all four tasks are done, commit your worksheet and its screenshots once, then push and check that GitHub has everything:

```bash
cd ~/student-YOUR-USERNAME
git add Module1-Network-Attacks-and-Defense/Session3
git commit -m "Module 1 Session 3: home task"
git push
git status
```

**Checkpoint:** `git status` says `Your branch is up to date with 'origin/main'.`, and on GitHub your Home Task Submission shows every screenshot.
If it says **ahead**, the push did not happen: read the error `git push` printed.
Only GitHub's copy counts: until the push succeeds, your work exists only on this machine.
When you have finished with the lab, stop it from its folder with `docker compose down`.

---

# What "done" looks like

- `inspect_datagram.py` prints `None` for `plen`, `len` and `chksum` under `show()`, numbers for them under `show2()`, and a `hexdump()` whose text column ends in `=86400`
- `where_stops.py` reports, for each of the three frames, the layers it dissected, the last layer it named and the length of `Raw`
- `l2_echo.py`, run with `sudo`, prints an `srp1` reply from the target's MAC address with an Ethernet layer, and an `sr1` reply without one
- `count_filter.py` keeps the echo request and its reply in both modes, and reports how many packets reached Python in each
- Your worksheet holds all four tools' code, output, screenshots and answers, with **Anything that failed** and **AI Assistance** filled in
- On GitHub, `Module1-Network-Attacks-and-Defense/Session3` shows the worksheet with every screenshot, and `git status` says **up to date**
