# Module 1 · Session 1 — Practical Guide

## Encapsulation, Forwarding and the Byte-Level Frame

### Professional Training in Cybersecurity I

---

## Overview

A packet is not an object.
It is a run of bytes at agreed offsets, and every tool you will ever build for a network starts by reading those bytes correctly.
This lab makes you prove you can.
You will build one real frame by hand, take it apart again, and then meet a header nobody has taught you and read it anyway.
In this practical session, you will:

1. Look at a **real frame** as raw bytes and find the layer boundaries yourself
2. **Build** the session's reference frame inside-out with `struct.pack` until your bytes match it exactly
3. **Parse** it outside-in, following the chain each header declares
4. Compute the **IPv4 checksum** by hand, hunt an **endianness bug**, find the **payload boundary**, write your own **hexdump**, and rebuild the frame with **UDP**
5. Read a header this session never taught you, from its layout table alone
6. Solve **3 CTF challenges** on the traps that bite every packet parser: **generate each capture locally**, then write a solver (1 required + 1 choice)
7. Document everything in your Practical Guide Submission

**Primary lab environment:** Kali Linux VM, VS Code, Python virtual environment.

**No second machine, no network, no root.**
Everything this session touches is bytes in a file on your own machine.
Nothing is sent, nothing is captured off a live interface, and nothing needs privileges.
That comes later, once you can read what would be on the wire.

> [!example] 📝 Submission
> Work in **Module1_Session1_Practical_Guide_Submission.md** throughout: paste your code, terminal output, and answers into its slots as you go.
> Guided exercises give you a starter with `# TODO` gaps **in this guide**.
> Copy it out, complete it in your IDE, and paste your finished code into the Submission.
> From-scratch exercises leave the slot empty for your own solution.

> [!important] You must complete
> Warm-up + Exercise 1 + Exercise 2 + **at least two** choice exercises (3–7) + Exercise 8 + CTF Challenge 1 and one of Challenge 2/3.

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
ls Module1-Network-Attacks-and-Defense/Session1
```

**Checkpoint:** `ls` lists `Module1_Session1_Practical_Guide.md`, `Module1_Session1_Home_Task.md`, the two `_Submission.md` worksheets and `screenshots`.
In Obsidian, open the Practical Guide worksheet, then right-click **Module1_Session1_Practical_Guide.md** and choose **Open to the right**, so this guide sits beside it.

> [!important] Fill in the worksheets only
> Never edit, move or delete the guide or the Home Task in your repository.
> Your instructor's fixes arrive in them through `git pull`, and a changed copy stops that pull.

## Step 2: A working folder for your code

> [!note] Why the code lives outside your repository
> Your repository holds what you hand in: the worksheets and their screenshots.
> The scripts you write today, the files they read, and this session's virtual environment live in a folder of their own, at the same path the session has in your repository, under `~/cyberlabs`.
> Your code reaches your instructor by being pasted into the worksheet.

1. **Create the folder and open it in VS Code:**

   ```bash
   mkdir -p ~/cyberlabs/Module1-Network-Attacks-and-Defense/Session1
   code ~/cyberlabs/Module1-Network-Attacks-and-Defense/Session1
   ```

2. **Trust the folder.**
   The first time VS Code opens it, a window asks *Do you trust the authors of the files in this folder?*
   You made the folder yourself, so click **Yes, I trust the authors**.
3. **Open the built-in terminal** with **Terminal**, then **New Terminal**.
   Its prompt ends in `~/cyberlabs/Module1-Network-Attacks-and-Defense/Session1`.
   **Run every command in this guide in this terminal**, unless a step says otherwise.

## Step 3: This session's virtual environment

Every session gets a virtual environment of its own, inside its working folder, so what one session installs never reaches another.
Create it and activate it in the built-in terminal:

```bash
python3 -m venv .venv
source .venv/bin/activate
which python3   # should end in Session1/.venv/bin/python3
```

Your prompt now starts with `(.venv)`.
Every new terminal you open in this folder activates it by itself, because VS Code finds `.venv` and runs the same `source` line for you.

Everything this session uses is in the Python **standard library**: `struct`, and nothing else that matters.
There is nothing to install.

As you meet a code block tagged `@generator` (writes a file you will read) or `@infra` (run it as it is), save it in this folder under the filename in its tag and run it here.
A `@starter` block is a guided exercise: copy it out, complete its `# TODO`s in the editor, and keep the finished version for your Submission.

## Step 4: Lay down the reference frame

You need real bytes before you can read them.
Save this as `make_ref_frame.py` and run it:

```python
#!/usr/bin/env python3
# @generator make_ref_frame.py
# @expect writes ref_frame.bin (59 bytes) and ref_frame_padded.bin (60 bytes)
"""make_ref_frame.py — write this session's reference frame to disk.

These are the bytes a network card hands up to software: one Ethernet frame
carrying an IPv4 packet, a TCP segment, and the five ASCII bytes "hello".
Two files are written:

  ref_frame.bin          the 59 bytes exactly as transmitted
  ref_frame_padded.bin   the same frame as a capture shows it, padded out to
                         Ethernet's 60-byte minimum

Nothing here parses or builds anything — this only lays the bytes down so you
have something real to read.
"""

# The reference frame, byte for byte. Grouped by layer for readability only;
# on the wire it is one uninterrupted run of 59 bytes.
REF_HEX = (
    "0800 27ab cdef  0800 2712 3456  0800"                  # Ethernet   14 B
    "4500 002d 1c46 4000 4006 087d 0a00 0004 0a00 0205"     # IPv4       20 B
    "c350 0050 001a 2b3c 00e5 f6a7 5018 ffff 6f69 0000"     # TCP        20 B
    "6865 6c6c 6f"                                          # "hello"     5 B
)


def main():
    frame = bytes.fromhex(REF_HEX)
    if len(frame) != 59:
        raise SystemExit(f"[!] expected 59 bytes, built {len(frame)}")

    # A card will not put a frame shorter than 60 bytes on the wire, so a real
    # capture of this frame carries one padding byte that is NOT payload.
    padded = frame + b"\x00" * (60 - len(frame))

    with open("ref_frame.bin", "wb") as fh:
        fh.write(frame)
    with open("ref_frame_padded.bin", "wb") as fh:
        fh.write(padded)

    print(f"[+] ref_frame.bin        {len(frame)} bytes")
    print(f"[+] ref_frame_padded.bin {len(padded)} bytes (padded to the 60-byte minimum)")
    print("[*] Read them with:  hexdump -C ref_frame.bin")


if __name__ == "__main__":
    main()
```

```bash
cd ~/cyberlabs/Module1-Network-Attacks-and-Defense/Session1
python3 make_ref_frame.py
```

> [!note] Why the bytes are handed to you, not built
> You will build this frame yourself in Exercise 1.
> Handing you the finished bytes first gives you something to check your build *against*, the same thing a capture gives you in real work: an authoritative answer you did not produce.

## Step 5: Lay down the warm-up frame

The warm-up reads a second frame, one you will not build or parse anywhere else.
Save this as `make_warmup_frame.py` and run it:

```python
#!/usr/bin/env python3
# @generator make_warmup_frame.py
# @expect writes warmup_frame.bin
"""make_warmup_frame.py — write the frame the warm-up asks you to read.

One Ethernet frame carrying an IPv4 packet and a TCP segment: a mail client
greeting its server with an SMTP command.

Nothing here parses or builds anything — this only lays the bytes down so you
have something real to read.
"""

# The warm-up frame, byte for byte. Its boundaries are what the warm-up asks
# you to find, so nothing here marks them.
WARMUP_HEX = (
    "0800 276d 2e19 0800 2712 3456 0800 4500"
    "0050 4d21 4000 4006 d96a 0a00 0004 0a00"
    "0019 c245 0019 6e1a 03b2 2f7c 9d41 b018"
    "faf0 f89b 0000 0101 050a 2f7c 9d81 2f7c"
    "9db1 0101 080a 0013 a8f2 0a41 c7e0 4845"
    "4c4f 206c 6162 2e6c 6f63 616c 0d0a"
)


def main():
    frame = bytes.fromhex(WARMUP_HEX)
    with open("warmup_frame.bin", "wb") as fh:
        fh.write(frame)
    print("[+] warmup_frame.bin written")
    print("[*] Read it with:  hexdump -C warmup_frame.bin")


if __name__ == "__main__":
    main()
```

```bash
python3 make_warmup_frame.py
```

---

# Warm-Up: Reading the Bytes Before Parsing Them — REQUIRED

No code.
Look at the frame:

```bash
hexdump -C warmup_frame.bin
```

```
00000000  08 00 27 6d 2e 19 08 00  27 12 34 56 08 00 45 00  |..'m....'.4V..E.|
00000010  00 50 4d 21 40 00 40 06  d9 6a 0a 00 00 04 0a 00  |.PM!@.@..j......|
00000020  00 19 c2 45 00 19 6e 1a  03 b2 2f 7c 9d 41 b0 18  |...E..n.../|.A..|
00000030  fa f0 f8 9b 00 00 01 01  05 0a 2f 7c 9d 81 2f 7c  |........../|../||
00000040  9d b1 01 01 08 0a 00 13  a8 f2 0a 41 c7 e0 48 45  |...........A..HE|
00000050  4c 4f 20 6c 61 62 2e 6c  6f 63 61 6c 0d 0a        |LO lab.local..|
0000005e
```

These bytes, and nothing in them marks where one header stops and the next begins.
There are no delimiters, no field names, no lengths written between the parts.
The structure is an **agreement**: the sender wrote each field at a fixed offset, and the receiver reads it back from the same offset.
Get the offsets right and every field falls out.
Shift by one and every value is garbage.

Work these out on the dump above with your finger, not with code.
Each answer feeds the next:

1. Ethernet's header is 14 bytes.
    a. Which offset holds its last byte?
    b. Which offset starts the next header?
    
2. A MAC address is 6 bytes, so two of Ethernet's 14 bytes are not addresses.
    a. Which two offsets are they, and what do they read?
    b. What could a field in that position be for?
    
3. The byte at offset 14 reads `45`.
   Its low hex digit is the IPv4 header's length in 4-byte words.
    a. How many bytes long is the IPv4 header?
    b. Which offset comes after it?
    
4. Offsets 16–17 hold IPv4's total length: this header plus everything it carries.
    a. What total length do those two bytes read?
    b. Added to the offset IPv4 started at, which offset does the packet end at?
    c. Does it agree with the dump's last line, `0000005e`, which is the file's total size in hex?
    
5. TCP declares its header length the same way, but in the high digit instead of the low one.
   Read the byte at offset 46, byte 12 of the TCP header.
    a. How many bytes long is the TCP header?
    b. Which offset does the payload start at?
    c. You reached that offset by adding two header lengths, so why would hard-coding it be wrong for a different frame?
    
6. Read the ASCII column at the offset you just worked out.
    a. What is sitting there?
    b. What would have to change for you not to be able to read it?

> [!tip] The ASCII column is not decoration
> `hexdump`'s right-hand gutter prints any byte that happens to be printable.
> Most header bytes are not, so they show as dots.
> The moment an application sends text, though, it appears there in plain sight.
> That is the whole reason the rest of this module cares about encryption.

> [!example] 📝 Submission
> Paste your `hexdump -C warmup_frame.bin` output, then answer 1a–6b in their slots.
> Most answers are a single offset or length.
> For each one, be able to say which header field you got it from.

---

# Exercises

---

| Exercise | Status | Type | Difficulty |
|----------|--------|------|------------|
| Exercise 1: Build the Frame From the Inside Out | **Required** | Guided (starter in guide) | ⭐⭐ Medium |
| Exercise 2: Parse the Frame From the Outside In | **Required** | Guided (starter in guide) | ⭐⭐ Medium |
| Exercise 3: Compute the IPv4 Checksum by Hand | **Choose ≥2** | From Scratch | ⭐⭐ Medium |
| Exercise 4: Find and Fix the Endianness Bugs | **Choose ≥2** | Guided (starter in guide) | ⭐ Easy |
| Exercise 5: Where the Payload Stops | **Choose ≥2** | From Scratch | ⭐ Easy |
| Exercise 6: Write a Hexdump From Scratch | **Choose ≥2** | From Scratch | ⭐⭐ Medium |
| Exercise 7: The Same Frame, With UDP | **Choose ≥2** | From Scratch | ⭐⭐ Medium |
| Exercise 8: Reading an Unfamiliar Header | **Required** | From Scratch | ⭐⭐⭐ Hard |

---

# Required Exercises

---

## Exercise 1: Build the Frame From the Inside Out — REQUIRED

> **🧩 GUIDED: complete the starter below** | Difficulty: ⭐⭐ Medium
> *Copy the starter out, fill its `# TODO` gaps in your IDE, run it until it reports MATCH, then paste your finished code into the Submission.*

> [!note] Concept note
> Wrapping data in a header is **prepending bytes**.
> You build from the inside out: pack the TCP header in front of the payload, pack an IPv4 header in front of that, then an Ethernet header in front of all of it.
> Because every wrap goes on the front, plain concatenation lands the bytes in wire order: `eth + ip + tcp + payload` *is* the frame.
>
> Each header is one `struct.pack` with that header's format string, and a format string is a **width recipe** read left to right: one letter per field, each a fixed number of bytes.
>
> | letter | width | reads as |
> |---|---|---|
> | `B` | 1 byte | an integer |
> | `H` | 2 bytes | an integer |
> | `L` | 4 bytes | an integer |
> | `Ns` | N bytes | raw bytes, not a number |
> | `!` | — | prefix: network byte order, big-endian, the wire's law |
>
> Count the letters in `'!HHLLBBHHH'` and their widths add to 20, exactly TCP's header.
> `'!6s6sH'` adds to 14, exactly Ethernet's.
>
> One field is smaller than a byte.
> IPv4's first byte packs **two** 4-bit fields, version and IHL, so you assemble it yourself by shifting one into the high nibble and OR-ing in the other: `(4 << 4) | 5` gives `0x45`.

Complete the three TODOs in `build_frame.py`:

```python
#!/usr/bin/env python3
# @starter build_frame.py
"""build_frame.py — build the reference frame inside-out with struct.pack.

Three packs and a concatenation produce the 59 bytes on the wire:

    payload  ->  + TCP  ->  + IPv4  ->  + Ethernet

Each header is one struct.pack with that header's format string. The leading
'!' on every format string means network byte order (big-endian) — the wire's
law, not your CPU's habit.
"""
import struct

# --- the values that go in each field ----------------------------------------
DST_MAC = bytes.fromhex("080027abcdef")   # 08:00:27:ab:cd:ef
SRC_MAC = bytes.fromhex("080027123456")   # 08:00:27:12:34:56
ETHERTYPE_IPV4 = 0x0800                   # "inside me: IPv4"

SRC_IP = bytes([10, 0, 0, 4])
DST_IP = bytes([10, 0, 2, 5])
PROTO_TCP = 6                             # "inside me: TCP"
IP_CHECKSUM = 0x087D                      # given here, computed in Exercise 3

SRC_PORT, DST_PORT = 50000, 80
SEQ, ACK = 0x001A2B3C, 0x00E5F6A7
FLAGS = 0x18                              # PSH + ACK
WINDOW = 0xFFFF
TCP_CHECKSUM = 0x6F69                     # covers a pseudo-header, beyond this session

PAYLOAD = b"hello"


def build():
    # --- innermost first: TCP over the payload -------------------------------
    # TODO 1: pack the TCP header with '!HHLLBBHHH' — nine fields, in this order:
    #   source port, destination port, sequence, acknowledgment,
    #   data_offset, FLAGS, WINDOW, TCP_CHECKSUM, urgent pointer 0
    # `data_offset` below is the high nibble of one byte (5 four-byte words = a
    # 20-byte header), and the low nibble is reserved and stays 0.
    # Put your packed header in `tcp` below — it starts empty as b"".
    data_offset = (5 << 4)
    tcp = b""

    # --- wrap that in IPv4 ---------------------------------------------------
    # TODO 2: build the two fields that are computed rather than given:
    #   version_ihl  — version 4 in the high nibble, IHL 5 in the low nibble
    #                  (shift the version up 4 bits and OR the IHL in)
    #   total_length — the IPv4 header plus everything it carries: 20 + the TCP
    #                  header you just built + the payload
    version_ihl = 0
    total_length = 0
    ip = struct.pack(
        "!BBHHHBBH4s4s",
        version_ihl, 0x00,                 # version/IHL, DSCP and ECN
        total_length,                      # this header + everything it carries
        0x1C46, 0x4000,                    # identification, flags (DF) + offset
        64, PROTO_TCP,                     # time to live, next-layer pointer
        IP_CHECKSUM,                       # header checksum
        SRC_IP, DST_IP,                    # '4s' = four raw bytes, not a number
    )

    # --- and Ethernet around all of it ---------------------------------------
    eth = struct.pack("!6s6sH", DST_MAC, SRC_MAC, ETHERTYPE_IPV4)

    # TODO 3: every wrap prepends, so the frame is the four pieces in wire
    #         order. Return them concatenated in place of the empty b"" below.
    return b""


def main():
    frame = build()
    print(f"[*] built {len(frame)} bytes")
    print(f"    {frame.hex(' ')}")

    with open("built_frame.bin", "wb") as fh:
        fh.write(frame)

    # The proof: byte-for-byte against the frame the card handed up.
    with open("ref_frame.bin", "rb") as fh:
        reference = fh.read()
    if frame == reference:
        print("[+] MATCH: built_frame.bin is byte-for-byte identical to ref_frame.bin")
    else:
        print("[!] MISMATCH — first differing offset:")
        for i, (a, b) in enumerate(zip(frame, reference)):
            if a != b:
                print(f"    offset {i}: built {a:#04x} != reference {b:#04x}")
                break


if __name__ == "__main__":
    main()
```

**Run it** until it reports a match, then confirm it independently:

```bash
python3 build_frame.py
cmp built_frame.bin ref_frame.bin && echo "IDENTICAL"
hexdump -C built_frame.bin
```

> [!tip] Read the mismatch, do not guess at it
> The script tells you the **first offset that differs**.
> That offset names the field you got wrong: 14 is the version/IHL byte, 16–17 the total length, 34–35 the source port.
> A wrong value is a bug in one field.
> A wrong *length* usually means a format string that does not add up.

> [!example] 📝 Submission
> Paste your completed `build_frame.py`, the MATCH line, the `cmp ... IDENTICAL` line, and a screenshot of the run, then answer the Exercise 1 questions.

---

## Exercise 2: Parse the Frame From the Outside In — REQUIRED

> **🧩 GUIDED: complete the starter below** | Difficulty: ⭐⭐ Medium
> *Complete the four TODOs in your IDE, then paste your finished code into the Submission.*

> [!note] Concept note
> Parsing is the exact mirror of building.
> You start at the outside, slice a header, and read the **next-layer pointer** it carries, the field that names what it wraps.
> That pointer tells you how to read the next slice:
>
> `EtherType 0x0800` → the next bytes are IPv4 · `protocol 6` → inside is TCP · `destination port 80` → hand the data to whatever listens there
>
> You follow that chain, and you never guess it.
> None of those numbers are secret: EtherTypes, protocol numbers and ports are public IANA registries, so an unfamiliar value is a lookup, not a dead end.
>
> Two moves do all the sub-byte work.
> To **read** a nibble: shift for the high one (`b >> 4`), mask for the low one (`b & 0x0F`).
> The same mask reads a flag bit: `flags & 0x10` is ACK, `flags & 0x08` is PSH.
>
> And every boundary is **computed from the headers**, never assumed:
> ```
> transport starts at  14 + IHL x 4
> payload   starts at  14 + IHL x 4 + data offset x 4
> payload   ends   at  14 + total length
> ```
> Twenty is a minimum, not a promise: options can widen either header, and `len(frame)` is not the end because short frames arrive padded.

Complete the four TODOs in `parse_frame.py`:

```python
#!/usr/bin/env python3
# @starter parse_frame.py
"""parse_frame.py — parse a frame outside-in, following the next-layer pointers.

Usage:  python3 parse_frame.py [frame.bin]
"""
import struct
import sys

ETHERTYPES = {0x0800: "IPv4", 0x0806: "ARP", 0x86DD: "IPv6"}
PROTOCOLS = {1: "ICMP", 6: "TCP", 17: "UDP"}
TCP_FLAGS = [(0x20, "URG"), (0x10, "ACK"), (0x08, "PSH"),
             (0x04, "RST"), (0x02, "SYN"), (0x01, "FIN")]


def mac(raw):
    """Six raw bytes -> the printed form 08:00:27:ab:cd:ef."""
    return ":".join(f"{b:02x}" for b in raw)


def ipv4(raw):
    """Four raw bytes -> dotted decimal."""
    return ".".join(str(b) for b in raw)


def parse_ethernet(frame):
    """Read frame[0:14]. Returns (ethertype, offset of the next header).

    This one is done for you — it is the pattern the other two follow.
    """
    dst, src, ethertype = struct.unpack("!6s6sH", frame[0:14])
    print("Link  [0:14]  Ethernet")
    print(f"  destination MAC : {mac(dst)}")
    print(f"  source MAC      : {mac(src)}")
    print(f"  EtherType       : 0x{ethertype:04x}  -> "
          f"{ETHERTYPES.get(ethertype, 'unknown — look it up in the IANA registry')}")
    return ethertype, 14


def parse_ipv4(frame, off):
    """Read the IPv4 header at `off`. Returns (protocol, transport offset, end)."""
    (version_ihl, tos, total_length, ident, flags_frag,
     ttl, proto, checksum, src, dst) = struct.unpack("!BBHHHBBH4s4s", frame[off:off + 20])

    # TODO 1: byte 14 packs two 4-bit fields. Split it:
    #   version    = the HIGH nibble  (shift right by 4)
    #   ihl        = the LOW nibble   (mask with 0x0F)
    #   header_len = ihl x 4, because IHL counts 32-bit words
    version = 0
    ihl = 0
    header_len = 0

    print(f"\nInternet  [{off}:{off + header_len}]  IPv4")
    print(f"  version / IHL   : {version} / {ihl}  -> header is {header_len} bytes")
    print(f"  DSCP and ECN    : 0x{tos:02x}")
    print(f"  total length    : {total_length}  -> this header + everything it carries")
    print(f"  identification  : 0x{ident:04x}")
    print(f"  flags / offset  : 0x{flags_frag:04x}"
          f"{'  (DF)' if flags_frag & 0x4000 else ''}")
    print(f"  time to live    : {ttl}")
    print(f"  protocol        : {proto}  -> "
          f"{PROTOCOLS.get(proto, 'unknown — look it up in the IANA registry')}")
    print(f"  header checksum : 0x{checksum:04x}")
    print(f"  source          : {ipv4(src)}")
    print(f"  destination     : {ipv4(dst)}")

    # TODO 2: where does the transport header start, and where does the IPv4
    #         packet end? Both come from fields you just read — not from 20,
    #         and not from len(frame).
    transport_off = 0
    end = 0
    return proto, transport_off, end


def parse_tcp(frame, off):
    """Read the TCP header at `off`. Returns the offset where the payload starts."""
    (src_port, dst_port, seq, ack, offset_reserved,
     flags, window, checksum, urgent) = struct.unpack("!HHLLBBHHH", frame[off:off + 20])

    # TODO 3: `offset_reserved` packs TCP's own header length in its HIGH
    #         nibble, counted in 32-bit words exactly like IHL. Split it out,
    #         and build `named` from TCP_FLAGS: every bit set in `flags`, joined
    #         with "+" (so 0x18 reads ACK+PSH), or "none" if no bit is set.
    data_offset = 0
    header_len = 0
    named = ""

    print(f"\nTransport  [{off}:{off + header_len}]  TCP")
    print(f"  source port     : {src_port}")
    print(f"  destination port: {dst_port}  -> hand the data to whatever listens there")
    print(f"  sequence        : 0x{seq:08x}")
    print(f"  acknowledgment  : 0x{ack:08x}")
    print(f"  data offset     : {data_offset}  -> header is {header_len} bytes")
    print(f"  flags           : 0x{flags:02x}  -> {named}")
    print(f"  window          : 0x{window:04x}")
    print(f"  checksum        : 0x{checksum:04x}")
    print(f"  urgent pointer  : 0x{urgent:04x}")
    return off + header_len


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "ref_frame.bin"
    with open(path, "rb") as fh:
        frame = fh.read()
    print(f"[*] {path}: {len(frame)} bytes captured\n")

    ethertype, off = parse_ethernet(frame)
    if ethertype != 0x0800:
        print("\n[!] not IPv4 — the chain stops here.")
        return

    proto, transport_off, end = parse_ipv4(frame, off)
    if proto == 6:
        start = parse_tcp(frame, transport_off)
    else:
        print(f"\n[!] protocol {proto} is not one this parser reads yet — "
              "the chain stops here.")
        return

    # TODO 4: slice the payload out into `payload` below, between the two
    #         boundaries you computed; then report anything after `end` as
    #         padding rather than payload.
    payload = b""
    print(f"\nApplication  [{start}:{end}]  payload")
    print(f"  {len(payload)} bytes: {payload!r}")
    if end < len(frame):
        print(f"  ({len(frame) - end} trailing byte(s) at [{end}:{len(frame)}] are "
              "padding, not payload)")


if __name__ == "__main__":
    main()
```

**Run it** against both files.
The padded one is the interesting case:

```bash
python3 parse_frame.py                        # the 59-byte frame
python3 parse_frame.py ref_frame_padded.bin   # the 60-byte capture
```

Your parser must report `b'hello'` for **both**, and flag the extra byte in the second as padding.
Every field it prints should match what `hexdump -C ref_frame.bin` shows at the same offsets.

> [!example] 📝 Submission
> Paste your completed `parse_frame.py`, the full parse of both files, and a screenshot, then answer the Exercise 2 questions.

---

# Choice Exercises — Pick At Least 2

*Choose to span the ideas: at least one of {checksum / byte order} and at least one of {boundaries / hexdump / UDP}.*

---

## Exercise 3: Compute the IPv4 Checksum by Hand

> **🔨 FROM SCRATCH** | Difficulty: ⭐⭐ Medium
> *Read the requirements and write the script yourself.*

> [!note] Concept note
> The IPv4 header carries a checksum over itself, and the scheme is **one's-complement addition**.
> The sender zeroes the checksum field, adds the header as 16-bit words, and stores the complement of that sum.
> The receiver adds every word *including* the checksum: a valid header sums to `0xFFFF`, whose complement is `0x0000`.
> One addition, and the header is either intact or it is not.
>
> One wrinkle: the sum can overflow 16 bits, and the carry out of bit 16 is added back into the low bits rather than dropped.
> That is what makes it "one's complement".

Write `ip_checksum.py` from these requirements and paste it into your Submission.

**Requirements:**
- `ones_complement_sum(data)`: add `data` as 16-bit **big-endian** words, folding each carry back in (`total = (total & 0xFFFF) + (total >> 16)`), and return the sum.
  Pad with a zero byte if the length is odd.
- `checksum(data)`: return `~ones_complement_sum(data) & 0xFFFF`.
- Read `ref_frame.bin`, take the IPv4 header (use IHL to find its length, do not hard-code 20), and print the ten 16-bit words with the checksum field zeroed.
- Print the sum, your computed checksum, and the checksum actually carried in the packet, and say whether they match.
- Then do the **receiver's** check: sum the header *unmodified*, including its checksum field, and show that the complement is `0x0000`.
- Finally, rewrite the TTL byte to 63, recompute, and print the new checksum.

**Expected values.**
Your run must reproduce these exactly:

```
sum with the checksum field zeroed : 0xf782
computed checksum                  : 0x087d      (the value in the packet)
receiver's sum over the whole header: 0xffff  ->  complement 0x0000
after lowering the TTL to 63       : 0x097d
```

> [!tip] What that last line means
> You just edited a header and made its checksum agree with the edit, in three lines.
> A checksum catches a **flipped bit on a wire**.
> It is arithmetic, not a signature, and it proves nothing about who wrote the bytes, a point the home task pushes on properly.

> [!example] 📝 Submission
> Paste your `ip_checksum.py`, its full output showing all four values, and a screenshot, then answer the Exercise 3 questions.

---

## Exercise 4: Find and Fix the Endianness Bugs

> **🧩 GUIDED: complete the starter below** | Difficulty: ⭐ Easy

> [!note] Concept note
> A two-byte field is a **pair** of bytes, and a pair reads in two orders, exactly as the digits `1 2` could mean twelve or twenty-one.
> The wire's law is **big-endian**: the first byte is the big end.
> Your x86 CPU stores numbers the other way round, and `struct` will happily read them that way if you ask it to, or if you forget to ask for anything.
>
> This is the classic first-packet bug, and what makes it vicious is that the bytes are *right*.
> Only the numbers are wrong, and they look entirely believable: a port that reads 20675 instead of 50000 is still a plausible port.

The starter below reads the frame with format strings that are missing something.
Fix them, and record what each field read before and after:

```python
#!/usr/bin/env python3
# @starter endian_fix.py
"""endian_fix.py — the same bytes read two ways, and why only one is right.

Usage:  python3 endian_fix.py [frame.bin]
"""
import struct
import sys

# (label, slice, struct letter) — every multi-byte field this frame carries.
FIELDS = [
    ("IPv4 total length", slice(16, 18), "H"),
    ("IPv4 identification", slice(18, 20), "H"),
    ("IPv4 header checksum", slice(24, 26), "H"),
    ("TCP source port", slice(34, 36), "H"),
    ("TCP destination port", slice(36, 38), "H"),
    ("TCP sequence number", slice(38, 42), "L"),
    ("TCP window", slice(48, 50), "H"),
]


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "ref_frame.bin"
    with open(path, "rb") as fh:
        frame = fh.read()

    print(f"{'field':<22} {'bytes':<12} {'right':>14} {'wrong':>16}")
    print("-" * 68)
    for label, where, letter in FIELDS:
        raw = frame[where]
        # TODO 1: `right` must read the field the way the WIRE writes it, and
        #         `wrong` the way an x86 CPU would lay it out in memory. One of
        #         these two prefixes is missing entirely below — decide which
        #         prefix each line needs, and fix them.
        right = struct.unpack(letter, raw)[0]
        wrong = struct.unpack(letter, raw)[0]
        print(f"{label:<22} {raw.hex(' '):<12} {right:>14} {wrong:>16}")

    # TODO 2: print the source port both ways with its two bytes, so the two
    #         readings sit side by side: c3 50 -> 0xc350 = 50000 (correct)
    #         and 0x50c3 = 20675 (a real port number, and wrong).


if __name__ == "__main__":
    main()
```

**Run it.**
Every row must show a different pair of numbers except one:

```bash
python3 endian_fix.py
```

> [!tip] The starter crashes before you fix it, and the crash is a clue
> Run it as given and it dies on the sequence-number row with `struct.error: unpack requires a buffer of 8 bytes`.
> With **no prefix at all**, `struct` uses your machine's *native* sizes, and on a 64-bit Linux box `L` is 8 bytes rather than 4.
> So the prefix does two jobs: it fixes the byte order *and* it pins every field to the width the wire actually uses.
> That is why every format string in this session starts with `!`.

> [!tip] One row is the same in both columns
> `TCP window` reads `ff ff`, which is the same number whichever end you start from.
> That is exactly why this bug survives testing: with the wrong prefix, *some* fields still look perfect, and a parser that is right about half its fields is not half right.

> [!example] 📝 Submission
> Paste your completed `endian_fix.py`, its output table, and a screenshot, then answer the Exercise 4 questions.

---

## Exercise 5: Where the Payload Stops

> **🔨 FROM SCRATCH** | Difficulty: ⭐ Easy

> [!note] Concept note
> `frame[54:]` is the most common wrong answer in this session.
> The payload's **start** is `14 + IHL x 4 + data offset x 4`, which is 54 only when both headers are at their 20-byte minimum, and options push it out.
> The payload's **end** is `14 + total length`, taken from the IP header, *not* `len(frame)`: Ethernet will not carry a frame under 60 bytes, so short frames arrive with padding on the end that the application never sent.

Write `payload_bounds.py` from these requirements.

**Requirements:**
- Read `ref_frame_padded.bin` (60 bytes) by default, and any file given as `sys.argv[1]`.
- Read `ihl` from the low nibble of byte 14, `total_length` from `frame[16:18]`, and `data_offset` from the high nibble of the TCP header's byte 12, located at `14 + ihl * 4 + 12`, not at a hard-coded offset.
- Print the arithmetic itself, showing the numbers substituted in: `start = 14 + 5*4 + 5*4 = 54` and `end = 14 + 45 = 59`.
- Print `frame[start:end]` and `frame[start:]` side by side with their lengths, so the difference is on screen.
- If the frame is longer than the declared end, print the trailing bytes as hex and name them padding.

**Run it against both files** and compare:

```bash
python3 payload_bounds.py ref_frame.bin          # nothing trailing
python3 payload_bounds.py ref_frame_padded.bin   # one byte of padding
```

The padded run must show `frame[54:59] = b'hello'` (5 bytes) against `frame[54:] = b'hello\x00'` (6 bytes).

> [!tip] Why one stray byte matters
> A password field with a `\x00` glued to the end does not match.
> A length that is one too long shifts every field in the record after it.
> "Close enough" is not a thing the bytes recognize.

> [!example] 📝 Submission
> Paste your `payload_bounds.py`, the output for both files, and a screenshot, then answer the Exercise 5 questions.

---

## Exercise 6: Write a Hexdump From Scratch

> **🔨 FROM SCRATCH** | Difficulty: ⭐⭐ Medium

> [!note] Concept note
> You have been reading `hexdump -C` output all session.
> Now write it.
> This is the tool you will reach for every time bytes do not look right, and building it once means you know exactly what it is and is not telling you.
> The test is unusually strict, and unusually satisfying: your output must be **byte-for-byte identical** to the real thing, so `diff` decides whether you are done.

Write `my_hexdump.py` from this format specification.

**Requirements: reproduce `hexdump -C` exactly.**
- Take a filename as `sys.argv[1]`.
- One line per 16 bytes: the offset as **8 hex digits**, two spaces, then the bytes as two groups of eight (`%02x ` each) with **one extra space between the groups**, then the printable ASCII of that line between `|` pipes.
- Printable means `0x20` to `0x7E`.
  Everything else prints as `.`.
- A short final line pads the hex columns with spaces so the `|` gutter still lines up.
- A run of identical 16-byte lines collapses to a single `*` line.
- The last line is the total length as 8 hex digits, alone.

**The test is a diff.**
This must produce no output at all:

```bash
python3 make_ref_frame.py
diff <(python3 my_hexdump.py ref_frame.bin) <(hexdump -C ref_frame.bin) && echo "IDENTICAL"
diff <(python3 my_hexdump.py ref_frame_padded.bin) <(hexdump -C ref_frame_padded.bin) && echo "IDENTICAL"
```

> [!tip] Where the alignment goes wrong
> Almost every failed diff is one of three things: the two-space gap after the offset, the extra space between the two groups of eight, or the padding on a short final line.
> Build the hex column as 16 fixed slots (a byte or three spaces), and the alignment takes care of itself.

> [!example] 📝 Submission
> Paste your `my_hexdump.py`, both `diff ... IDENTICAL` lines, and a screenshot of your dump beside the real one, then answer the Exercise 6 questions.

---

## Exercise 7: The Same Frame, With UDP

> **🔨 FROM SCRATCH** | Difficulty: ⭐⭐ Medium

> [!note] Concept note
> UDP does the same addressing job as TCP with 8 bytes of header against TCP's 20: **source port, destination port, length, checksum**, four 16-bit fields and nothing else.
> No sequence numbers, no flags, no connection state.
> Swapping TCP for UDP changes three things in the frame and nothing at all in your method, which is the point of the exercise.
>
> One field here reaches outside its own header: UDP's checksum is computed over a **pseudo-header** of IP fields (source address, destination address, protocol, UDP length) as well as the UDP header and payload.
> You are given the recipe below.
> The reason it works that way belongs to the transport layer's own session.

Write `build_udp.py` from these requirements.

**Requirements: build.**
- Same MACs, same addresses, same payload `b"hello"`, source port 50000, destination port 53.
- Pack the UDP header with `'!HHHH'`: source port, destination port, **length** (8 + payload), checksum.
- Compute the UDP checksum with the same one's-complement routine as Exercise 3, over `pseudo + udp_header_with_zero_checksum + payload`, where:
  ```python
  pseudo = struct.pack("!4s4sBBH", SRC_IP, DST_IP, 0, 17, udp_length)
  ```
  then pack the header again with the value in place.
- Build the IPv4 header with **protocol 17** and the new **total length**, and compute its checksum rather than hard-coding one.
- Write the frame to `udp_frame.bin` and print its length and hex.

**Requirements: parse it back.**
Read your own frame with the same outside-in walk and print the EtherType, the protocol, the four UDP fields, and the payload sliced at `[transport + 8 : 14 + total_length]`.

**Verify it:**

```bash
python3 build_udp.py
python3 parse_frame.py udp_frame.bin   # your Exercise 2 parser
```

Your Exercise 2 parser will stop at "protocol 17 is not one this parser reads yet".
That is correct behavior, not a bug: it followed the chain, and the chain led somewhere it does not know yet.
The frame must be **47 bytes** (14 + 20 + 8 + 5), twelve shorter than the TCP version.

> [!tip] A card would pad this one
> 47 bytes is under Ethernet's 60-byte minimum, so on a real wire this frame arrives with 13 bytes of padding.
> Your `total_length` of 33 is what tells a receiver where `hello` really ends.

> [!example] 📝 Submission
> Paste your `build_udp.py`, its output, the hexdump of `udp_frame.bin`, and a screenshot, then answer the Exercise 7 questions.

---

# Required Capstone

---

## Exercise 8: Reading an Unfamiliar Header — REQUIRED

> **🔨 FROM SCRATCH** | Difficulty: ⭐⭐⭐ Hard
> *This is the exercise the whole session is for.
> Nothing new is being taught.
> You are being handed an unfamiliar protocol and asked to read it anyway.*

> [!note] Concept note
> Everything so far used a header you had been shown.
> Real work does not go like that: you meet a protocol you have never parsed, find its layout in a specification, and read the bytes.
> The skill is not knowing Ethernet, IPv4 and TCP.
> The skill is **treating an unknown header as a new layout over the same two moves**: slice at the offset, unpack in network order.

First, lay down the frame.
Save this as `make_arp_frame.py` and run it:

```python
#!/usr/bin/env python3
# @generator make_arp_frame.py
# @expect writes arp_frame.bin (60 bytes)
"""make_arp_frame.py — lay down one frame carrying a protocol you have not met.

Writes arp_frame.bin: a single Ethernet frame, captured off the wire, padded to
the 60-byte minimum. What rides inside it is for you to work out from the bytes.
"""

FRAME_HEX = (
    "ffff ffff ffff  0800 2712 3456  0806"        # Ethernet                14 B
    "0001 0800 0604 0001"                         # the payload's first 8 bytes
    "0800 2712 3456 0a00 0004"                    # ... and its next 10
    "0000 0000 0000 0a00 0001"                    # ... and its last 10
    + "00" * 18                                   # padding to 60 bytes
)


def main():
    frame = bytes.fromhex(FRAME_HEX)
    if len(frame) != 60:
        raise SystemExit(f"[!] expected 60 bytes, built {len(frame)}")
    with open("arp_frame.bin", "wb") as fh:
        fh.write(frame)
    print(f"[+] arp_frame.bin  {len(frame)} bytes")
    print("[*] Start with:  hexdump -C arp_frame.bin")


if __name__ == "__main__":
    main()
```

**Start where you always start:**

```bash
python3 make_arp_frame.py
hexdump -C arp_frame.bin
python3 parse_frame.py arp_frame.bin    # your Exercise 2 parser
```

Your parser reads the Ethernet header and stops: the EtherType is not one it knows.
Look up that value in the public IANA registry, and you have the protocol's name.
Its layout is fixed and 28 bytes long:

| offset | size | field |
|---|---|---|
| 0 | 2 | hardware type (1 = Ethernet) |
| 2 | 2 | protocol type (`0x0800` = IPv4) |
| 4 | 1 | hardware address length |
| 5 | 1 | protocol address length |
| 6 | 2 | operation (1 = request, 2 = reply) |
| 8 | 6 | sender hardware address |
| 14 | 4 | sender protocol address |
| 18 | 6 | target hardware address |
| 24 | 4 | target protocol address |

That table is your entire brief.
Write `parse_arp.py` from it.

**Requirements:**
- Parse the Ethernet header first, and say what the destination MAC `ff:ff:ff:ff:ff:ff` means about who receives this frame.
- Confirm the EtherType before going further.
  If it is not this protocol, say so and stop.
- Unpack all nine fields in one `struct.unpack`.
  Work out the format string from the table (widths in bytes, `s` for addresses, and remember the `!`).
- Print the MACs in colon form and the addresses in dotted decimal, and translate the operation number into words.
- Say what is notable about the **target hardware address**, and what that tells you the frame is asking.
- Report the bytes after the protocol's 28 as what they are, not as data.

**Check yourself against the bytes:** the sender is `10.0.0.4` at `08:00:27:12:34:56`, the target address is `10.0.0.1`, and the frame is a **request**, sent to the broadcast MAC because the sender does not yet know who to ask.

> [!tip] What the all-zero field means
> One address field is entirely zeros.
> That is not padding and not an error: it is the blank in the question being asked.
> Working that out from the bytes alone is exactly the reasoning this exercise is testing.

> [!example] 📝 Submission
> Paste your `parse_arp.py`, its full output, a screenshot, and one sentence naming the protocol and how you identified it, then answer the Exercise 8 questions.

---

# CTF Challenges — Solve Challenge 1 and One of 2–3

---

Three challenges, three traps, and every one of them is a mistake you can make with correct-looking code.
You **generate each capture on your own machine**, work out what the headers are telling you, and **write a Python solver** to recover the flag.

> [!note] How the captures are laid out
> Each challenge file is a run of **fixed 128-byte slots**, one frame per slot, zero-padded: the shape a capture tool with a fixed buffer produces.
> So slot `n` is `blob[n*128:(n+1)*128]`, and everything after the frame inside a slot is **buffer slack, not packet**.
> Every frame carries real, verifiable checksums.

> [!warning] `strings` will lie to you here
> Running `strings` on these files finds things that look like flags.
> Some of them are sitting in option fields and buffer slack: bytes that are genuinely in the file and genuinely not payload.
> Only the headers can tell you which text is real, which is the entire point.

## CTF Structure

| Challenge | Status | Difficulty | Trap |
|-----------|--------|------------|------|
| Challenge 1: Read the Length | **Required** | ⭐ Easy | the payload is where the headers say |
| Challenge 2: Read a Multi-Byte Value Correctly | **Choose 1** | ⭐⭐ Medium | a two-byte field reads two ways |
| Challenge 3: Follow the Chain | **Choose 1** | ⭐⭐ Medium | pointers, and headers that are not 20 bytes |

> [!important] You must complete
> Challenge 1 + one of Challenge 2 or 3.

---

## Setup: generate the challenge captures

Save this as `ctf_setup.py` and run it once.
It writes all three challenge files into your working folder:

```python
#!/usr/bin/env python3
# @infra ctf_setup.py
# @expect writes chal1.bin (384 B), chal2.bin (640 B), chal3.bin (1024 B)
"""ctf_setup.py — lay down the three challenge captures on this machine.

Each capture is written as a run of fixed 128-byte slots, one frame per slot,
zero-padded: the shape a capture tool with a fixed buffer produces. So slot n is

    blob[n * 128 : (n + 1) * 128]

and everything after the frame inside a slot is buffer slack, not packet.

The flag material is base64 here purely so a casual `grep FLAG` on this file
does not spoil the challenges. That is not a security boundary — the canonical
flags live with the instructor.

Writes chal1.bin, chal2.bin, chal3.bin.
"""
import base64
import struct

SLOT = 128
DST_MAC = bytes.fromhex("080027abcdef")
SRC_MAC = bytes.fromhex("080027123456")
SRC_IP = bytes([10, 0, 0, 4])
DST_IP = bytes([10, 0, 2, 5])


def b64(text):
    return base64.b64decode(text).decode()


def ones_complement_sum(data):
    if len(data) % 2:
        data += b"\x00"
    total = 0
    for i in range(0, len(data), 2):
        total += (data[i] << 8) | data[i + 1]
        total = (total & 0xFFFF) + (total >> 16)
    return total


def checksum(data):
    return ~ones_complement_sum(data) & 0xFFFF


def ip_frame(payload, *, proto=6, ident=0x1C46, ttl=64, src_port=50000,
             dst_port=80, ip_options=b"", tcp_options=b""):
    """One Ethernet + IPv4 + (TCP|UDP) frame with real, verifiable checksums."""
    if proto == 6:
        data_offset = 5 + len(tcp_options) // 4
        transport = struct.pack("!HHLLBBHHH", src_port, dst_port,
                                0x001A2B3C, 0x00E5F6A7,
                                data_offset << 4, 0x18, 0xFFFF, 0, 0) + tcp_options
    else:
        transport = struct.pack("!HHHH", src_port, dst_port, 8 + len(payload), 0)

    # Real transport checksums, computed over the pseudo-header of IP fields
    # plus the segment itself — these captures carry no fabricated values.
    pseudo = struct.pack("!4s4sBBH", SRC_IP, DST_IP, 0, proto,
                         len(transport) + len(payload))
    value = checksum(pseudo + transport + payload)
    at = 16 if proto == 6 else 6
    transport = transport[:at] + struct.pack("!H", value) + transport[at + 2:]

    ihl = 5 + len(ip_options) // 4
    total_length = ihl * 4 + len(transport) + len(payload)
    header = struct.pack("!BBHHHBBH4s4s", (4 << 4) | ihl, 0x00, total_length,
                         ident, 0x4000, ttl, proto, 0, SRC_IP, DST_IP) + ip_options
    header = header[:10] + struct.pack("!H", checksum(header)) + header[12:]

    eth = struct.pack("!6s6sH", DST_MAC, SRC_MAC, 0x0800)
    return eth + header + transport + payload


def other_frame(ethertype, body):
    """A frame carrying something that is not IPv4 — ARP, IPv6, whatever."""
    return struct.pack("!6s6sH", DST_MAC, SRC_MAC, ethertype) + body


def slot(frame, slack=b""):
    """Drop one frame into a fixed 128-byte capture slot."""
    if len(frame) + len(slack) > SLOT:
        raise SystemExit(f"[!] {len(frame) + len(slack)} bytes will not fit a slot")
    return (frame + slack).ljust(SLOT, b"\x00")


def write(path, slots):
    blob = b"".join(slots)
    with open(path, "wb") as fh:
        fh.write(blob)
    print(f"[+] {path}  {len(blob)} bytes = {len(slots)} slots x {SLOT}")


def challenge_one():
    """The trap: a payload starts and stops where the HEADERS say, nowhere else."""
    flag = b64("RkxBR3tyMzRkX3RoM19sM25ndGh9")
    parts = [flag[:9].encode(), flag[9:14].encode(), flag[14:].encode()]
    # Twelve bytes of TCP options sit between the header and the payload, and
    # slot slack sits after it. Both look like text. Neither is payload.
    decoy_options = b64("RkxBR3swcHQxMG59").encode()
    decoy_slack = b64("RkxBR3tzbDRja18xc19uMHRfcDR5bDA0ZH0=").encode()
    return [
        slot(ip_frame(parts[0], ident=0x0001, tcp_options=decoy_options)),
        slot(ip_frame(parts[1], ident=0x0002, tcp_options=decoy_options), decoy_slack),
        slot(ip_frame(parts[2], ident=0x0003, tcp_options=decoy_options)),
    ]


def challenge_two():
    """The trap: the ordering field is two bytes, and a pair reads two ways."""
    flag = b64("RkxBR3tieXQzXzByZDNyX200dHQzcnN9")
    parts = [flag[i:i + 5] for i in range(0, 20, 5)] + [flag[20:]]
    # Identification values chosen so a little-endian reading sorts them into a
    # different order entirely — plausible, and wrong.
    idents = [0x0103, 0x0201, 0x0304, 0x0405, 0x0502]
    frames = [ip_frame(text.encode(), ident=ident)
              for text, ident in zip(parts, idents)]
    shuffled = [frames[2], frames[0], frames[4], frames[1], frames[3]]
    return [slot(f) for f in shuffled]


def challenge_three():
    """The trap: follow the pointer chain, and read every header length."""
    flag = b64("RkxBR3tmMGxsMHdfdGgzX3AwMW50M3JzfQ==")
    parts = [flag[:9].encode(), flag[9:16].encode(),
             flag[16:21].encode(), flag[21:].encode()]
    junk = [b"_n0t_th1s_", b"_0r_th1s_", b"_n0r_th1s_", b"_d3f1n1t3ly_n0t_"]

    arp = bytes.fromhex("0001080006040001") + SRC_MAC + SRC_IP + \
        bytes(6) + DST_IP + junk[1]
    ipv6 = bytes.fromhex("6000000000") + bytes(35) + junk[2]

    return [
        slot(ip_frame(parts[0])),                                   # plain, qualifies
        slot(ip_frame(junk[0], proto=17, dst_port=80)),             # UDP, not TCP
        slot(ip_frame(parts[1], ip_options=b"\x01\x01\x01\x00")),   # IHL 6: 24-byte IPv4
        slot(other_frame(0x0806, arp)),                             # not IPv4 at all
        slot(ip_frame(parts[2], tcp_options=b"\x02\x04\x05\xb4\x01\x01\x01\x00")),
        slot(other_frame(0x86DD, ipv6)),                            # not IPv4 at all
        slot(ip_frame(parts[3])),                                   # plain, qualifies
        slot(ip_frame(junk[3], dst_port=443)),                      # TCP, wrong port
    ]


def main():
    write("chal1.bin", challenge_one())
    write("chal2.bin", challenge_two())
    write("chal3.bin", challenge_three())
    print("[*] Each file is a run of 128-byte slots. Read slot n with "
          "blob[n*128:(n+1)*128].")


if __name__ == "__main__":
    main()
```

```bash
cd ~/cyberlabs/Module1-Network-Attacks-and-Defense/Session1
python3 ctf_setup.py
```

---

## Challenge 1: Read the Length — REQUIRED

> **🚩 CTF** | Difficulty: ⭐ Easy

> [!note] Brief
> Three frames, three fragments of one flag.
> The trouble is that each frame carries readable text in two places that are **not** payload: option bytes sitting between the TCP header and the data, and buffer slack after the frame ends.
> `strings` finds all of it and cannot tell you which is which.
> The headers can.

**Step 1: look at what you are up against.**

```bash
strings -n 5 chal1.bin      # three flag-shaped strings. At most one is real.
hexdump -C chal1.bin | head -20
```

**Step 2: solve it** (write `solve1.py`, paste it into your Submission).
- Walk the file 128 bytes at a time.
- For each slot compute `start = 14 + ihl*4 + data_offset*4` and `end = 14 + total_length`, reading both header lengths from the bytes rather than assuming them.
- Concatenate `slot[start:end]` across the slots in order.

**Flag format:** `FLAG{...}`

> [!tip] Hint
> The data offset is not 5 in these frames.
> If your fragments start mid-word or carry stray text, you are slicing from a hard-coded 54.

> [!example] 📝 Submission
> Paste `solve1.py`, the recovered flag, a screenshot, and a one-line approach into your Submission.

---

## Challenge 2: Read a Multi-Byte Value Correctly

> **🚩 CTF** | Difficulty: ⭐⭐ Medium

> [!note] Brief
> Five frames, each carrying one fragment, and the slots are shuffled.
> Each frame's **IPv4 identification** field says where its fragment belongs in the flag.
> It is a two-byte field, so it reads two ways, and both readings produce a complete, plausible-looking flag.
> Only one is the flag.

**Step 1: capture the shape of the problem.**

```bash
strings -n 4 chal2.bin      # the fragments, in the order they happen to sit
```

**Step 2: solve it** (write `solve2.py`).
- Walk the slots, carve each payload with the same boundary arithmetic as Challenge 1.
- Read the identification field at `slot[18:20]`, sort the fragments by it, and join them.
- Print **both** orderings (the wire's and the other one) so you can see what the wrong answer looks like.

**Flag format:** `FLAG{...}`

> [!tip] Hint
> `struct.unpack("!H", ...)` and `struct.unpack("<H", ...)` on the same two bytes.
> If your flag reads as scrambled words that are individually correct, you sorted by the wrong number.

> [!example] 📝 Submission
> Paste `solve2.py`, both orderings, the recovered flag, a screenshot, and a one-line approach into your Submission.

---

## Challenge 3: Follow the Chain

> **🚩 CTF** | Difficulty: ⭐⭐ Medium

> [!note] Brief
> Eight frames, and only some of them are talking to the web server.
> A fragment counts only if the **whole chain** says so: EtherType `0x0800` → IPv4, protocol `6` → TCP, destination port `80`.
> The rest carry decoy text.
> And two of the frames that *do* qualify carry options, so their headers are wider than the usual 20 bytes.

**Step 1: see how mixed the capture is.**

```bash
strings -n 4 chal3.bin      # fragments and decoys, indistinguishable by eye
hexdump -C chal3.bin | head -30
```

**Step 2: solve it** (write `solve3.py`).
- Walk the slots and test all three links of the chain before taking anything: EtherType, protocol, destination port.
- For the frames that qualify, compute the payload boundaries from IHL, data offset and total length.
  Two of these frames will punish a hard-coded offset.
- Concatenate the qualifying payloads in slot order.

**Flag format:** `FLAG{...}`

> [!tip] Hint
> Print a line per slot saying why you skipped it or what you took from it.
> Four slots should be skipped, and the reasons should be four different ones.

> [!example] 📝 Submission
> Paste `solve3.py`, your per-slot decisions, the recovered flag, a screenshot, and a one-line approach into your Submission.

---

### Rules

- **Generate the captures yourself** with `ctf_setup.py`.
  There is no pre-saved copy of any challenge file.
- **Solve each challenge by writing a Python script.**
  A flag pulled out by eye or by `strings` earns nothing: the decoys exist precisely to punish that.
- In your Submission, paste each solver, its recovered flag, and a one-line approach.

### Cleanup

When you have the flags (or want to reset a challenge), remove the generated captures.
Save this as `ctf_cleanup.sh` beside the captures:

```bash
#!/usr/bin/env bash
# @infra ctf_cleanup.sh
# @expect removes chal1.bin, chal2.bin and chal3.bin
# ctf_cleanup.sh — remove the generated challenge captures.
# Nothing here is precious: rerun ctf_setup.py to lay them down again.
set -eu
rm -f chal1.bin chal2.bin chal3.bin
echo "[+] Challenge captures removed. Recreate them with: python3 ctf_setup.py"
```

Run it in your working folder, like every other script in this guide.
`ctf_setup.py` recreates the captures any time:

```bash
cd ~/cyberlabs/Module1-Network-Attacks-and-Defense/Session1
bash ctf_cleanup.sh
```

---

# Hand In

When every exercise you are handing in is done, commit your worksheet and its screenshots once, then push and check that GitHub has everything:

```bash
cd ~/student-YOUR-USERNAME
git add Module1-Network-Attacks-and-Defense/Session1
git commit -m "Module 1 Session 1: practical guide"
git push
git status
```

**Checkpoint:** `git status` says `Your branch is up to date with 'origin/main'.`, and on GitHub your Practical Guide Submission shows every screenshot.
Only GitHub's copy counts: until the push succeeds, your work exists only on this machine.
Your scripts stay in `~/cyberlabs/Module1-Network-Attacks-and-Defense/Session1`: the worksheet carries the code you hand in.

---

# What "done" looks like

- `build_frame.py` prints `MATCH`, and `cmp` finds your frame identical to `ref_frame.bin`
- `parse_frame.py` reports `b'hello'` for both reference files and flags the padding byte in the second
- At least two of Exercises 3 to 7 print what their exercise shows
- `parse_arp.py` names the protocol and reads all nine fields
- Your solvers recover the flags of Challenge 1 and one of Challenges 2 and 3
- Your worksheet holds every completed exercise's code, output, screenshot and answers, with **AI Assistance** filled in
- On GitHub, `Module1-Network-Attacks-and-Defense/Session1` shows the worksheet with every screenshot, and `git status` says **up to date**
