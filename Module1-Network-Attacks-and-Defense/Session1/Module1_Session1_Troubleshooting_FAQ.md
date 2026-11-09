# Module 1 · Session 1 — Troubleshooting & FAQ

## Encapsulation, Forwarding and the Byte-Level Frame

### Professional Training in Cybersecurity I

---

> [!note] How to use this
> **Find the last line of the traceback, or the sentence you would say out loud**, not the exercise you were on.
> Errors are quoted exactly as Python or the shell prints them, so you can search this page for the line in front of you.
> Each entry shows the run that fails, the **cause**, then the **fix**.
> Where the failing code is a small file, the entry shows it.
> Where it is your own exercise or challenge code, the entry shows only the run, and the cause names the line to look at.
> Every run was recorded on Kali's Python 3.13.12, and Python 3.14 prints the same.
> For how a tool works in full, see the **Tooling Reference**: this page is for when something breaks.
>
> If nothing here matches, note **the exact step, the exact command and everything it printed**, and ask in the Telegram group.

## Contents

- [Environment and setup](#environment-and-setup)
- [Bytes and `struct`](#bytes-and-struct)
- [Byte order](#byte-order)
- [The IPv4 checksum](#the-ipv4-checksum)
- [Boundaries and parsing](#boundaries-and-parsing)
- [Your hexdump and the real one](#your-hexdump-and-the-real-one)
- [CTF](#ctf)
- [Tools](#tools)
- [The Home Task's starters](#the-home-tasks-starters)

---

# Environment and setup

### `FileNotFoundError: [Errno 2] No such file or directory: 'ref_frame.bin'`

```python
with open("ref_frame.bin", "rb") as fh:
    frame = fh.read()
print(len(frame), "bytes")
```
```
(.venv) $ python3 read_frame.py
Traceback (most recent call last):
  File "/home/kali/cyberlabs/Module1-Network-Attacks-and-Defense/Session1/read_frame.py", line 1, in <module>
    with open("ref_frame.bin", "rb") as fh:
         ~~~~^^^^^^^^^^^^^^^^^^^^^^^
FileNotFoundError: [Errno 2] No such file or directory: 'ref_frame.bin'
```

**Cause.**
The script reads a file that is not in the folder it runs in.
Almost always the frame has not been generated yet, or the terminal is in a different folder from the one holding the `.bin` files.

**Fix.**
Run from the session's working folder, and generate the frame first:

```
(.venv) $ python3 make_ref_frame.py
[+] ref_frame.bin        59 bytes
[+] ref_frame_padded.bin 60 bytes (padded to the 60-byte minimum)
[*] Read them with:  hexdump -C ref_frame.bin
(.venv) $ python3 read_frame.py
59 bytes
```

> [!tip] Other files have their own generators
> `chal1.bin`, `chal2.bin` and `chal3.bin` come from `ctf_setup.py`, and `ctf_cleanup.sh` removes them again.
> The Home Task's `lab_capture.bin` comes from `make_lab_capture.py`.
> A missing file of either kind prints the same error with its own name.

---

# Bytes and `struct`

### `TypeError: a bytes-like object is required, not 'str'`

```python
frame = ""
frame += "hello"
with open("built_frame.bin", "wb") as fh:
    fh.write(frame)
```
```
(.venv) $ python3 build_str.py
Traceback (most recent call last):
  File "/home/kali/cyberlabs/Module1-Network-Attacks-and-Defense/Session1/build_str.py", line 4, in <module>
    fh.write(frame)
    ~~~~~~~~^^^^^^^
TypeError: a bytes-like object is required, not 'str'
```

**Cause.**
A file opened with `"wb"` takes `bytes`, and `frame` is a `str`: it started as `""`, and everything added to it was text.

**Fix.**
Start the buffer as `b""` and add only bytes to it (`b"hello"`, or a `struct.pack` result).
The starters hand you `b""` for this reason.

### `TypeError: can only concatenate str (not "bytes") to str`

```python
frame = ""
frame += b"\x08\x00"
```
```
(.venv) $ python3 concat_str.py
Traceback (most recent call last):
  File "/home/kali/cyberlabs/Module1-Network-Attacks-and-Defense/Session1/concat_str.py", line 2, in <module>
    frame += b"\x08\x00"
TypeError: can only concatenate str (not "bytes") to str
```

**Cause.**
The same mistake as the entry above, caught one step earlier: the buffer is a `str`, and the first header added to it is `bytes`.

**Fix.**
Start the buffer as `b""`.

### `struct.error: unpack requires a buffer of 8 bytes`

```python
import struct
with open("ref_frame.bin", "rb") as fh:
    frame = fh.read()
seq = struct.unpack("L", frame[38:42])[0]
```
```
(.venv) $ python3 native.py
Traceback (most recent call last):
  File "/home/kali/cyberlabs/Module1-Network-Attacks-and-Defense/Session1/native.py", line 4, in <module>
    seq = struct.unpack("L", frame[38:42])[0]
          ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^
struct.error: unpack requires a buffer of 8 bytes
```

**Cause.**
A format string with **no byte-order prefix** uses the machine's native sizes, and on 64-bit Linux native `L` is 8 bytes.
The slice holds the 4 bytes of the TCP sequence number.

**Fix.**
Start every format string with `!`.
It fixes the byte order to the wire's (big-endian) **and** the sizes to the standard ones, where `L` is exactly 4: `struct.unpack("!L", frame[38:42])[0]`.

### `struct.unpack` gives me `(50000,)`, or `unsupported format string passed to tuple.__format__`

```python
import struct
with open("ref_frame.bin", "rb") as fh:
    frame = fh.read()
port = struct.unpack("!H", frame[34:36])
print(port)
print(f"{port:04x}")
```
```
(.venv) $ python3 tuple_port.py
(50000,)
Traceback (most recent call last):
  File "/home/kali/cyberlabs/Module1-Network-Attacks-and-Defense/Session1/tuple_port.py", line 6, in <module>
    print(f"{port:04x}")
            ^^^^^^^^^^
TypeError: unsupported format string passed to tuple.__format__
```

**Cause.**
`unpack` **always returns a tuple**, even for one field, so `port` is `(50000,)`, not `50000`.
A number format such as `04x` has nothing to format in a tuple.

**Fix.**
Take the first item, `struct.unpack("!H", frame[34:36])[0]`, or unpack into a name with a trailing comma, `port, = struct.unpack("!H", frame[34:36])`.

---

# Byte order

### The bytes are right but the numbers are wrong: a port reads `20675` instead of `50000`

```python
import struct
with open("ref_frame.bin", "rb") as fh:
    frame = fh.read()
print("source port", struct.unpack("H", frame[34:36])[0])
```
```
(.venv) $ python3 noprefix.py
source port 20675
```

**Cause.**
The field was read in the wrong **byte order**.
The wire is big-endian, and without a prefix `struct` reads the machine's native order, which on a lab PC is little-endian.
For an `H`, native and standard sizes agree, so nothing raises an error: the number is simply wrong.

**Fix.**
Use `!` on every format string.
To see the two readings side by side while debugging, read the same two bytes both ways:

```python
import struct
with open("ref_frame.bin", "rb") as fh:
    frame = fh.read()
for label, field in (("source port", frame[34:36]), ("window", frame[48:50])):
    print(f"{label:12} {field.hex(' ')}  ! {struct.unpack('!H', field)[0]:5}  < {struct.unpack('<H', field)[0]:5}")
```
```
(.venv) $ python3 bothways.py
source port  c3 50  ! 50000  < 20675
window       ff ff  ! 65535  < 65535
```

`c3 50` is `0xc350`, 50000, read big-endian, and `0x50c3`, 20675, read little-endian.
Both are plausible ports, which is what lets this bug survive a quick look.

> [!tip] One field can look right by accident
> The TCP window, `ff ff`, reads the same both ways, so a parser with the wrong prefix still gets *some* fields right.
> A parser that is right about half its fields is not half right: check a field whose two bytes differ.

---

# The IPv4 checksum

### My computed checksum doesn't match the one in the packet

```python
def ones_complement_sum(data):
    total = 0
    for i in range(0, len(data), 2):
        total += (data[i] << 8) | data[i + 1]
        total = (total & 0xFFFF) + (total >> 16)
    return total


with open("ref_frame.bin", "rb") as fh:
    frame = fh.read()
ihl = frame[14] & 0x0F
header = frame[14:14 + ihl * 4]
print(f"in the frame 0x{header[10:12].hex()}, computed 0x{~ones_complement_sum(header) & 0xFFFF:04x}")
```
```
(.venv) $ python3 nozero.py
in the frame 0x087d, computed 0x0000
```

**Cause.**
The header was summed **with its checksum field still in it**.
The sender computes the checksum over a header whose checksum field is `0x0000`, so leaving the stored value in sums it into itself.
`0x0000` is the receiver's check succeeding, not a checksum.

**Fix.**
Zero the two checksum bytes (bytes 10 and 11 of the header) before summing:

```python
def ones_complement_sum(data):
    total = 0
    for i in range(0, len(data), 2):
        total += (data[i] << 8) | data[i + 1]
        total = (total & 0xFFFF) + (total >> 16)
    return total


with open("ref_frame.bin", "rb") as fh:
    frame = fh.read()
ihl = frame[14] & 0x0F
header = frame[14:14 + ihl * 4]
zeroed = header[:10] + b"\x00\x00" + header[12:]
print(f"in the frame 0x{header[10:12].hex()}, computed 0x{~ones_complement_sum(zeroed) & 0xFFFF:04x}")
print(f"receiver's check 0x{ones_complement_sum(header):04x}")
```
```
(.venv) $ python3 zeroed.py
in the frame 0x087d, computed 0x087d
receiver's check 0xffff
```

> [!tip] The receiver's check is the quick test
> Summed **unmodified**, checksum field included, a good header comes to `0xffff`.
> If yours comes to anything else, a byte is wrong or the slice is the wrong range.

### The IPv4 checksum verifies, but my UDP checksum is off by a little

This checker recomputes the UDP checksum of your `udp_frame.bin`, with the pseudo-header from the Practical Guide's UDP exercise:

```python
import struct


def ones_complement_sum(data):
    if len(data) % 2:
        data += b"\x00"
    total = 0
    for i in range(0, len(data), 2):
        total += (data[i] << 8) | data[i + 1]
        total = (total & 0xFFFF) + (total >> 16)
    return total


with open("udp_frame.bin", "rb") as fh:
    frame = fh.read()
ihl = frame[14] & 0x0F
total_length = struct.unpack("!H", frame[16:18])[0]
udp = frame[14 + ihl * 4:14 + total_length]
pseudo = struct.pack("!4s4sBBH", frame[26:30], frame[30:34], 0, 17, len(udp))
computed = ~ones_complement_sum(pseudo + udp[:6] + b"\x00\x00" + udp[8:]) & 0xFFFF
print(f"UDP checksum in the frame 0x{udp[6:8].hex()}, computed 0x{computed:04x}")
```

Run on a `udp_frame.bin` built with a sum that drops the carry:

```
(.venv) $ python3 udp_check.py
UDP checksum in the frame 0xe275, computed 0xe273
```

**Cause.**
The one's-complement sum **dropped the carry** instead of folding it back in.
The reference frame's IPv4 header sums to `0xf782` with its checksum zeroed, which never passes 16 bits, so a sum without the fold still gets that header right.
The UDP checksum covers more bytes (pseudo-header, UDP header and payload), and here they sum to `0x21d8a`.
Dropping the carry leaves `0x1d8a` and the checksum `0xe275`.
Folding it gives `0x1d8c` and the checksum `0xe273`.
The two differ by 2, which is exactly the carry that was dropped.

**Fix.**
Fold the carry back in on every step:

```python
total += (data[i] << 8) | data[i + 1]
total = (total & 0xFFFF) + (total >> 16)
```

Rebuilt with the fold, the checker agrees:

```
(.venv) $ python3 udp_check.py
UDP checksum in the frame 0xe273, computed 0xe273
```

---

# Boundaries and parsing

### My payload has a trailing `\x00`, or a recovered password won't match

```python
with open("ref_frame_padded.bin", "rb") as fh:
    frame = fh.read()
ihl = frame[14] & 0x0F
start = 14 + ihl * 4 + (frame[14 + ihl * 4 + 12] >> 4) * 4
payload = frame[start:]
print(payload, len(payload))
```
```
(.venv) $ python3 padded.py
b'hello\x00' 6
```

**Cause.**
The payload was ended at the end of the buffer, `len(frame)`, instead of where the IP header says the packet ends.
Ethernet pads any frame under 60 bytes, so a captured short frame carries padding the application never sent.

**Fix.**
Take the end from the IPv4 total length:

```python
import struct
with open("ref_frame_padded.bin", "rb") as fh:
    frame = fh.read()
ihl = frame[14] & 0x0F
start = 14 + ihl * 4 + (frame[14 + ihl * 4 + 12] >> 4) * 4
total_length = struct.unpack("!H", frame[16:18])[0]
payload = frame[start:14 + total_length]
print(payload, len(payload))
```
```
(.venv) $ python3 padded_end.py
b'hello' 5
```

> [!warning] Close enough does not exist for bytes
> One stray `\x00` glued to a credential means it no longer matches.
> A length one too long shifts every field after it.

### `frame[54:]` gives me gibberish on some frames

`trap1.bin` is written by `make_trap_demo.py`, in the [CTF](#ctf) section below.
Its frames carry 12 bytes of TCP options:

```python
with open("trap1.bin", "rb") as fh:
    blob = fh.read()
first_slot = blob[0:128]
print(first_slot[54:64])
```
```
(.venv) $ python3 fixed54.py
b'NOT-PAYLOA'
```

**Cause.**
54 is where the payload starts **only** when the IPv4 and TCP headers are both at their 20-byte minimum.
Options widen a header, and then 54 lands inside it: here, inside the TCP options.

**Fix.**
Compute the start from the two header lengths on every frame:

```python
ihl = frame[14] & 0x0F
transport = 14 + ihl * 4
data_offset = frame[transport + 12] >> 4
start = transport + data_offset * 4
```

### Version and IHL are swapped: I read version `5`, IHL `4`

```python
with open("ref_frame.bin", "rb") as fh:
    frame = fh.read()
version = frame[14] & 0x0F
ihl = frame[14] >> 4
print("version", version, "IHL", ihl)
```
```
(.venv) $ python3 swapped.py
version 5 IHL 4
```

**Cause.**
The two nibbles of byte 14 are mixed up.
The **high** nibble is the version, and the **low** nibble is IHL.

**Fix.**
High nibble is a shift, low nibble is a mask: `version = frame[14] >> 4` and `ihl = frame[14] & 0x0F`.

---

# Your hexdump and the real one

### `diff` against `hexdump -C` shows differences: my columns don't line up

```
(.venv) $ diff <(python3 my_hexdump.py ref_frame.bin) <(hexdump -C ref_frame.bin) && echo "IDENTICAL"
1,4c1,4
< 00000000  08 00 27 ab cd ef 08 00 27 12 34 56 08 00 45 00   |..'.....'.4V..E.|
< 00000010  00 2d 1c 46 40 00 40 06 08 7d 0a 00 00 04 0a 00   |.-.F@.@..}......|
< 00000020  02 05 c3 50 00 50 00 1a 2b 3c 00 e5 f6 a7 50 18   |...P.P..+<....P.|
< 00000030  ff ff 6f 69 00 00 68 65 6c 6c 6f                  |..oi..hello|
---
> 00000000  08 00 27 ab cd ef 08 00  27 12 34 56 08 00 45 00  |..'.....'.4V..E.|
> 00000010  00 2d 1c 46 40 00 40 06  08 7d 0a 00 00 04 0a 00  |.-.F@.@..}......|
> 00000020  02 05 c3 50 00 50 00 1a  2b 3c 00 e5 f6 a7 50 18  |...P.P..+<....P.|
> 00000030  ff ff 6f 69 00 00 68 65  6c 6c 6f                 |..oi..hello|
```

**Cause.**
`hexdump -C` has an exact layout, and a hand-written dump usually misses one of three spacings: the **two spaces** after the offset, the **extra space between the two groups of eight** bytes, or the **padding on a short final line**.
This dump joins its two groups with one space instead of two: the real lines (`>`) have the gap after the eighth byte, and the broken ones (`<`) do not.
Its hex column is padded to the right width, so the missing space reappears in front of the `|` gutter.
`1,4c1,4` means lines 1 to 4 of your dump must change into lines 1 to 4 of the real one.
The last line, `0000003b`, matched, so `diff` does not show it.

**Fix.**
Look at the line that joins your two groups of eight: it needs two spaces.
Building the hex column as 16 fixed slots, each a two-digit byte or three spaces, with the extra space after slot 8, lines up the gutter on its own.
The same `diff` line printing only `IDENTICAL` means byte-for-byte agreement.

---

# CTF

The entries below show each trap on a **demo capture**, so that no run prints a flag.
`make_trap_demo.py` builds the demo captures with the functions in your own `ctf_setup.py`, so each trap is laid out exactly as in the challenge files, with harmless text in place of the flag.
Save it next to `ctf_setup.py` and run it:

```python
#!/usr/bin/env python3
# @generator make_trap_demo.py
# @expect writes trap1.bin (384 B), trap2.bin (640 B) and trap3.bin (896 B)
"""make_trap_demo.py — the three CTF traps, with harmless text in place of the flags.

It builds each capture with ctf_setup.py's own functions, so every trap is laid
out exactly as in the challenge files. Save it next to ctf_setup.py.
"""
from ctf_setup import DST_IP, SRC_IP, SRC_MAC, ip_frame, other_frame, slot, write


def trap_one():
    """Text in the TCP options and in the slot slack, around the real payload."""
    options = b"NOT-PAYLOAD!"                       # 12 bytes of TCP options
    return [
        slot(ip_frame(b"READ-", ident=1, tcp_options=options)),
        slot(ip_frame(b"THE-", ident=2, tcp_options=options), b"SLACK-NOT-DATA"),
        slot(ip_frame(b"LENGTH", ident=3, tcp_options=options)),
    ]


def trap_two():
    """Shuffled slots, ordered by a two-byte identification field."""
    parts = [b"SORT-", b"BY-TH", b"E-WIR", b"E-ORD", b"ER"]
    idents = [0x0103, 0x0201, 0x0304, 0x0405, 0x0502]
    frames = [ip_frame(text, ident=ident) for text, ident in zip(parts, idents)]
    return [slot(frames[n]) for n in (2, 0, 4, 1, 3)]


def trap_three():
    """Only TCP to port 80 counts, and two of those frames carry options."""
    arp = bytes.fromhex("0001080006040001") + SRC_MAC + SRC_IP + bytes(6) + DST_IP + b"-ARP-"
    return [
        slot(ip_frame(b"FOLLOW-")),
        slot(ip_frame(b"-UDP-", proto=17, dst_port=80)),
        slot(ip_frame(b"THE-", ip_options=b"\x01\x01\x01\x00")),
        slot(other_frame(0x0806, arp)),
        slot(ip_frame(b"WHOLE-", tcp_options=b"\x02\x04\x05\xb4\x01\x01\x01\x00")),
        slot(ip_frame(b"CHAIN")),
        slot(ip_frame(b"-HTTPS-", dst_port=443)),
    ]


def main():
    write("trap1.bin", trap_one())
    write("trap2.bin", trap_two())
    write("trap3.bin", trap_three())


if __name__ == "__main__":
    main()
```
```
(.venv) $ python3 make_trap_demo.py
[+] trap1.bin  384 bytes = 3 slots x 128
[+] trap2.bin  640 bytes = 5 slots x 128
[+] trap3.bin  896 bytes = 7 slots x 128
```

The right readings are `READ-THE-LENGTH` for `trap1.bin`, `SORT-BY-THE-WIRE-ORDER` for `trap2.bin` and `FOLLOW-THE-WHOLE-CHAIN` for `trap3.bin`.
Each run below is a solver with one mistake in it.

### My flag reads as plausible words, but scrambled

```
(.venv) $ python3 solve2.py trap2.bin
BY-THERSORT-E-WIRE-ORD
```

**Cause.**
The fragments were sorted by the identification field read in the **wrong byte order**: this solver reads `slot[18:20]` with `"<H"`.
The field is two bytes, so it reads two ways, and both orders join into something that looks complete.
Only the wire's order is right.

**Fix.**
Read the ordering field big-endian, the way the wire wrote it: `struct.unpack("!H", slot[18:20])[0]`.
Print the fragments sorted by both readings, as the challenge asks, and the scrambled one is easy to tell apart.

### My recovered flag has decoy fragments in it

Two different mistakes produce this.
A solver that starts at 54 and runs to the end of the slot:

```
(.venv) $ python3 solve1.py trap1.bin
NOT-PAYLOAD!READ-NOT-PAYLOAD!THE-SLACK-NOT-DATANOT-PAYLOAD!LENGTH
```

A solver that takes every IPv4 slot without checking the rest of the chain:

```
(.venv) $ python3 solve3.py trap3.bin
FOLLOW--UDP-THE-WHOLE-CHAIN-HTTPS-
```

**Cause.**
The solver took text that sits in the file but is not payload:
- **TCP options and slot slack.**
  `NOT-PAYLOAD!` is the 12 bytes of TCP options between the header and the data, and `SLACK-NOT-DATA` is in the slot after the frame ends.
  Neither lies between the header-declared start and end.
- **Frames that are not part of the conversation.**
  `-UDP-` is protocol 17, and `-HTTPS-` goes to port 443.
  Only frames where EtherType `0x0800` **and** protocol `6` **and** destination port `80` all hold are taken.

**Fix.**
Carve strictly between the computed boundaries, `start` from IHL and the data offset and `end = 14 + total_length`, and test every link of the chain before taking a frame:

```python
if ethertype == 0x0800 and proto == 6 and dst_port == 80:
    taken.append(s[start:end])
```

### My flag has raw bytes spliced into the middle of it

```
(.venv) $ python3 solve3.py trap3.bin
b'FOLLOW-\x19\xc7\x00\x00THE-\x02\x04\x05\xb4\x01\x01\x01\x00WHOLE-CHAIN'
```

**Cause.**
This solver follows the chain correctly but slices every payload from a fixed 54.
Two of the frames it takes have wider headers:
- `THE-` comes from a frame with an IHL of 6, a 24-byte IPv4 header, so 54 is 4 bytes early and takes the end of the TCP header (`\x19\xc7\x00\x00`, its checksum and urgent pointer).
- `WHOLE-` comes from a frame with 8 bytes of TCP options, so 54 lands on them: `\x02\x04\x05\xb4` is a maximum-segment-size option.

**Fix.**
Compute the start from IHL and the data offset on **every** frame, as in [`frame[54:]` gives me gibberish on some frames](#frame54-gives-me-gibberish-on-some-frames).

---

# Tools

### `sh: 1: Syntax error: "(" unexpected` when I run a `diff <(...)` line

```
(.venv) $ sh -c 'diff <(python3 my_hexdump.py ref_frame.bin) <(hexdump -C ref_frame.bin)'
sh: 1: Syntax error: "(" unexpected
```

**Cause.**
Process substitution, `<(command)`, belongs to bash and zsh.
Kali's `sh` is `dash`, which does not have it, so the `(` is a syntax error.
The same happens when the line is pasted into a script that starts with `#!/bin/sh`.

**Fix.**
Run the line in the terminal itself, whose shell is zsh, or save each output to a file and compare the files:

```
(.venv) $ python3 my_hexdump.py ref_frame.bin > mine.txt
(.venv) $ hexdump -C ref_frame.bin > real.txt
(.venv) $ diff mine.txt real.txt && echo "IDENTICAL"
IDENTICAL
```

### `cmp` says `built_frame.bin ref_frame.bin differ: byte 15, line 1`

```
(.venv) $ cmp built_frame.bin ref_frame.bin && echo "IDENTICAL"
built_frame.bin ref_frame.bin differ: byte 15, line 1
```

**Cause.**
The built frame does not match the reference, and `cmp` names the **first** byte that differs.
It counts from 1, so byte 15 is offset 14: the version and IHL byte.

**Fix.**
The offset names the field to check: 14 is version and IHL, 22 the TTL, 24 and 25 the header checksum, and so on through the header.
A wrong *value* means one field.
A wrong *length* usually means a `struct` format string with a letter missing or extra.

---

# The Home Task's starters

### My `forged_ttl.bin` row says `INVALID`

```
(.venv) $ python3 header_forger.py
[+] ref_frame.bin         59 bytes  ttl  64  src 10.0.0.4  len  45  cksum 0x087d  valid  the frame as captured
[+] forged_ttl.bin        59 bytes  ttl  63  src 10.0.0.4  len  45  cksum 0x087d  INVALID  TTL rewritten, checksum fixed
[+] forged_sloppy.bin     59 bytes  ttl  64  src 10.0.0.99  len  45  cksum 0x087d  INVALID  source spoofed, checksum stale

[*] Three of these carry a header that verifies perfectly. Verifying is all a checksum does.
```

**Cause.**
This is the starter as shipped.
`recompute()` returns the frame unchanged until TODO 1 is done, so `forged_ttl.bin` has its new TTL and its old checksum, `0x087d`, and the header no longer verifies.
The `forged_spoof.bin` and `forged_length.bin` rows are missing because TODOs 2 and 3 have not written them yet.

**Fix.**
Complete TODO 1 as its comment describes.
When it works, the `forged_ttl.bin` row reads `valid` with a checksum different from `0x087d`.
Then complete TODOs 2 and 3, and the run prints all five rows shown in the Home Task.

### `FileNotFoundError: [Errno 2] No such file or directory: 'forged_spoof.bin'`

```
(.venv) $ python3 packet_auditor.py ref_frame.bin forged_ttl.bin forged_sloppy.bin forged_spoof.bin forged_length.bin
[PASS] ref_frame.bin  (59 bytes) — self-consistent
[FAIL] forged_ttl.bin  (59 bytes)
       - IPv4 header checksum does not verify (sum 0xfeff, expected 0xffff) — a field was edited without recomputing it
[FAIL] forged_sloppy.bin  (59 bytes)
       - IPv4 header checksum does not verify (sum 0x005f, expected 0xffff) — a field was edited without recomputing it
Traceback (most recent call last):
  File "/home/kali/cyberlabs/Module1-Network-Attacks-and-Defense/Session1/packet_auditor.py", line 123, in <module>
    main()
    ~~~~^^
  File "/home/kali/cyberlabs/Module1-Network-Attacks-and-Defense/Session1/packet_auditor.py", line 105, in main
    with open(path, "rb") as fh:
         ~~~~^^^^^^^^^^^^
FileNotFoundError: [Errno 2] No such file or directory: 'forged_spoof.bin'
```

**Cause.**
The auditor is fine: the file is missing.
`header_forger.py` writes `forged_spoof.bin` in TODO 2 and `forged_length.bin` in TODO 3, so until both are done the files do not exist.
This run also shows the forger's TODO 1 still empty: `forged_ttl.bin` fails its checksum, and it should pass.

**Fix.**
Complete all three TODOs in `header_forger.py`, run it, check that it prints five rows, then run the auditor.

### My harvester prints `[slot 0]` and nothing else

```
(.venv) $ python3 payload_harvester.py

[slot 0] 

[slot 1] 

[slot 2] 

[slot 3] 

[slot 4] 

[*] Every byte above came off the wire exactly as the application sent it. Reading it took the headers, and nothing else.
```

**Cause.**
This is the starter as shipped.
`carve()` returns an empty summary and `None` until its two TODOs are done, so each slot prints its number and is then skipped.
(`lab_capture.bin` must exist first: `python3 make_lab_capture.py`.)

**Fix.**
Complete TODO 1 (the ports and the payload's start) and TODO 2 (the payload's end, and the summary line).

### My harvester prints lines of dots after every payload

```
(.venv) $ python3 payload_harvester.py

[slot 0] 10.0.0.4:50101 -> 10.0.0.9:21  TCP
    | USER admin
    | ..............................................................
    [!] contains 'USER' — in the clear

[slot 1] 10.0.0.4:50101 -> 10.0.0.9:21  TCP
    | PASS Sup3rS3cr3t!
    | .......................................................
    [!] contains 'PASS' — in the clear

[slot 2] 10.0.0.4:50102 -> 10.0.0.9:80  TCP
    | GET /admin HTTP/1.1
    | Authorization: Basic YWRtaW46czNjcjN0
    | 
    | ............
    [!] contains 'Authorization:' — in the clear
    [!] decoded credentials: 'admin:s3cr3t'

[slot 3] 10.0.0.4:50103 -> 10.0.0.53:53  UDP
    | *............vault.lab.local..........................................................

[slot 4] 10.0.0.4:50104 -> 10.0.0.9:443  TCP
    | .... ...x..L.c......n..?.%.h...*..HA......................................

[*] Every byte above came off the wire exactly as the application sent it. Reading it took the headers, and nothing else.
```

**Cause.**
TODO 2's payload ends at `len(s)`, the end of the 128-byte slot, instead of at `14 + total_length`.
Everything after the frame inside a slot is buffer slack, zero bytes, and the harvester prints each zero byte as a dot.
The DNS and TLS lines show it most: their dots run on past the real data.

**Fix.**
End the slice at `14 + total_length`, as TODO 2's comment says.
The run then matches the Home Task's shown output line for line.
