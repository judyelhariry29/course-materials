# Module 1 · Session 1 — Tooling Reference

## Encapsulation, Forwarding and the Byte-Level Frame

### Professional Training in Cybersecurity I

---

> [!note] What this document is for
> The session used each tool once, on the way to building and reading a frame.
> **This is the fuller treatment**: every Python library, idiom and command-line tool the session used, each with what it is for, an example with its real output, and the mistakes it invites.
> Nothing here is required reading in order.
> Come to it when you need it.
>
> Everything is Python's standard library or a standard Kali command, with **nothing to install**.
> This session builds and reads frames as bytes in a file, so there are no sockets, no root and no network.
> Every example is a small file followed by the command that runs it and what it printed, so you can type it into your session folder and see the same.
> The examples read two sample frames of their own, which the first section writes.

> [!note] Python 3.13 on Kali
> These examples were recorded on **Python 3.13.12**, which is what `python3` is on the lab's Kali.
> A Kali upgraded to Python 3.14 prints exactly the same for every example here: each one was run on both.

---

# The Two Sample Frames

The examples below need real bytes to work on.
They do not read the session's reference frame: they read two other frames, so that every example works the same way on bytes you have not seen before.
Save this as `make_demo_frames.py` in your session folder and run it once:

```python
#!/usr/bin/env python3
# @generator make_demo_frames.py
# @expect writes demo_frame.bin (90 bytes) and demo_short.bin (60 bytes)
"""make_demo_frames.py — write the two frames this reference's examples read.

  demo_frame.bin   an HTTP request whose TCP header carries 12 bytes of options
  demo_short.bin   a one-line syslog message over UDP, padded to Ethernet's 60-byte minimum

They are not the session's reference frame: the examples read different bytes,
so every example works the same way on a frame you have not seen before.
"""

DEMO_HEX = (
    "5254 0012 3502  0800 275c 1d7e  0800"                  # Ethernet   14 B
    "4500 004c 3a1f 4000 8006 ce70 c0a8 3865 c0a8 3866"     # IPv4       20 B
    "c93a 1f90 1a2b 3c4d 5e6f 7081 8018 01f6 2acb 0000"     # TCP        20 B
    "0101 080a 0042 f1a3 00b7 1c05"                         # options    12 B
    "4745 5420 2f73 7461 7475 7320 4854 5450 2f31 2e30"     # "GET /status HTTP/1.0"
    "0d0a 0d0a"                                             # "\r\n\r\n"
)

SHORT_HEX = (
    "5254 0012 3502  0800 275c 1d7e  0800"                  # Ethernet   14 B
    "4500 0027 3a20 4000 8011 ce89 c0a8 3865 c0a8 3866"     # IPv4       20 B
    "c990 0202 0013 8460"                                   # UDP         8 B
    "3c31 333e 7265 626f 6f74 0a"                           # "<13>reboot\n"  11 B
)


def main():
    demo_frame = bytes.fromhex(DEMO_HEX)
    short_frame = bytes.fromhex(SHORT_HEX)
    short_frame += b"\x00" * (60 - len(short_frame))   # padding, as a capture shows it

    with open("demo_frame.bin", "wb") as fh:
        fh.write(demo_frame)
    with open("demo_short.bin", "wb") as fh:
        fh.write(short_frame)

    print(f"[+] demo_frame.bin  {len(demo_frame)} bytes")
    print(f"[+] demo_short.bin  {len(short_frame)} bytes (padded to the 60-byte minimum)")


if __name__ == "__main__":
    main()
```
```
(.venv) $ python3 make_demo_frames.py
[+] demo_frame.bin  90 bytes
[+] demo_short.bin  60 bytes (padded to the 60-byte minimum)
```

`demo_frame.bin` is a request from `192.168.56.101` to port 8080 on `192.168.56.102`.
Its TCP header is 32 bytes, not 20, because it carries a timestamps option, as most real TCP segments do.
`demo_short.bin` is 53 bytes of frame and 7 bytes of padding, so the frame and the file disagree about where the data ends.
Both checksums in each frame are real, and a receiver would accept them.

---

# Bytes and Text

A frame is `bytes`: a sequence of numbers from 0 to 255, with no characters and no meaning until something reads it.
Python keeps `bytes` and text (`str`) apart, and most mistakes in this section come from mixing the two.

## Bytes: indexing, slicing and joining

```python
frame = b""
frame += b"\x08\x00" + b"E\x00"
print(frame, len(frame))
print(frame[0], frame[2], frame[0:2], frame[-1:])
print(type(frame[0]), type(frame[0:1]))
```
```
(.venv) $ python3 bytesdemo.py
b'\x08\x00E\x00' 4
8 69 b'\x08\x00' b'\x00'
<class 'int'> <class 'bytes'>
```

- `b""` is an empty bytes buffer, and `+` joins bytes to bytes.
- Printed, `bytes` shows a printable byte as its character and any other byte as a `\x` code: `0x45` is `E`.
- One index, `frame[0]`, is a single byte as an **int**.
  A slice, `frame[0:2]`, is **bytes**, even when it holds one byte.

## Hex in and hex out

```python
with open("demo_frame.bin", "rb") as fh:
    demo_frame = fh.read()
print(demo_frame[:14].hex(" "))
print(bytes.fromhex("c0 a8 38 65"))
print(":".join(f"{b:02x}" for b in demo_frame[6:12]))
print(".".join(str(b) for b in demo_frame[26:30]))
protocol = demo_frame[23]
total_length = int.from_bytes(demo_frame[16:18], "big")
print(f"{protocol:x} {protocol:#x} {protocol:#04x} {total_length:04x} 0x{total_length:04x} {total_length:#06x}")
```
```
(.venv) $ python3 hexforms.py
52 54 00 12 35 02 08 00 27 5c 1d 7e 08 00
b'\xc0\xa88e'
08:00:27:5c:1d:7e
192.168.56.101
6 0x6 0x06 004c 0x004c 0x004c
```

- `.hex(" ")` shows every byte as two hex digits, separated by spaces, and `bytes.fromhex` goes back.
  `bytes.fromhex("c0 a8 38 65")` prints as `b'\xc0\xa88e'` because `0x38` and `0x65` are the characters `8` and `e`.
- A MAC address is six bytes joined with `:`, each formatted `02x`.
- An IPv4 address is four bytes joined with `.`, each as a decimal number.

After the colon inside `{}`, a **format spec** says how to show a number:

| Spec | Means | Printed above |
|---|---|---|
| `x` | hexadecimal, no padding | `6` |
| `#x` | hexadecimal, with `0x` | `0x6` |
| `#04x` | `0x` and digits together fill 4 places | `0x06` |
| `04x` | the digits alone fill 4 places | `004c` |
| `#06x` | `0x` and digits together fill 6 places | `0x004c` |

The protocol is 6 and the total length is 76, `0x4c`.

> [!tip] `04x` and `#04x` count differently
> `04x` pads the *digits* to 4, and you write the `0x` yourself: `0x{total_length:04x}` is `0x004c`.
> `#04x` counts the `0x` inside the 4, which leaves room for two digits: the right width for one byte.
> Pick the one whose width matches the field, or columns of output stop lining up.

## Printable bytes or dots

```python
with open("demo_frame.bin", "rb") as fh:
    demo_frame = fh.read()
payload = demo_frame[66:90]
print(payload)
print("".join(chr(b) if 0x20 <= b < 0x7F else "." for b in payload))
print(repr(payload.decode("ascii", errors="replace")))
```
```
(.venv) $ python3 dots.py
b'GET /status HTTP/1.0\r\n\r\n'
GET /status HTTP/1.0....
'GET /status HTTP/1.0\r\n\r\n'
```

The middle line keeps printable ASCII (`0x20` to `0x7E`) and prints a dot for every other byte, which is what `hexdump -C` does in its right-hand column.
`decode("ascii", errors="replace")` does something else: it passes control bytes such as `\r`, `\n` and `\x00` through unchanged, and replaces only bytes above `0x7F` with `�`.
A NUL byte printed to a terminal and pasted into a worksheet travels with the paste, which is why this session's tools print dots.

## Reading and writing binary files

```python
with open("demo_frame.bin", "rb") as fh:
    demo_frame = fh.read()
print(type(demo_frame), len(demo_frame))
with open("copy_frame.bin", "wb") as fh:
    written = fh.write(demo_frame)
print(written, "bytes written")
```
```
(.venv) $ python3 fileio.py
<class 'bytes'> 90
90 bytes written
```

`"rb"` reads the file as `bytes`, and `"wb"` writes `bytes`, creating the file or emptying it first.
`write` returns how many bytes it wrote.
Frames are always read and written in binary mode: text mode decodes and translates what it reads, and a frame is not text.

## Changing bytes: `bytearray`, `bytes([...])`, `ljust` and `splitlines`

A `bytes` value cannot be changed after it is made.
To edit a field in a frame, copy it into a **`bytearray`**, which can.

```python
with open("demo_frame.bin", "rb") as fh:
    demo_frame = fh.read()
changed_frame = bytearray(demo_frame)
changed_frame[22] = 64
changed_frame[26:30] = bytes([192, 168, 56, 200])
print(demo_frame[22], changed_frame[22], ".".join(str(b) for b in changed_frame[26:30]))
print(type(changed_frame), type(bytes(changed_frame)), len(changed_frame))
print(b"<13>".ljust(8, b"\x00"))
print(b"GET /status HTTP/1.0\r\nHost: lab\r\n".splitlines())
```
```
(.venv) $ python3 bytesedit.py
128 64 192.168.56.200
<class 'bytearray'> <class 'bytes'> 90
b'<13>\x00\x00\x00\x00'
[b'GET /status HTTP/1.0', b'Host: lab']
```

- `bytearray(demo_frame)` is a changeable copy: assign one byte by its index, or a run of bytes to a slice of the same length.
  The original `demo_frame` still reads TTL 128.
- `bytes([192, 168, 56, 200])` makes bytes from a list of numbers, each from 0 to 255: here, an IPv4 address.
- `bytes(changed_frame)` turns the edited copy back into `bytes`, to write or compare.
- `ljust(8, b"\x00")` pads on the right to 8 bytes, which is how the session's generators fill a fixed-size slot.
- `splitlines()` splits at each line end, `\r\n` included, and drops the line ends.

## Common mistakes

**Starting a buffer with `""` instead of `b""`:**

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

`""` is a `str`, and a `str` cannot be joined to `bytes`.
The starters hand you `b""` for this reason, so keep the `b`.

**Writing a `str` to a binary file:**

```python
with open("out.bin", "wb") as fh:
    fh.write("\x08\x00")
```
```
(.venv) $ python3 write_str.py
Traceback (most recent call last):
  File "/home/kali/cyberlabs/Module1-Network-Attacks-and-Defense/Session1/write_str.py", line 2, in <module>
    fh.write("\x08\x00")
    ~~~~~~~~^^^^^^^^^^^^
TypeError: a bytes-like object is required, not 'str'
```

The quotes have no `b` in front, so the value is text.
Write `b"\x08\x00"`, or `.encode()` a string first.

**Opening a frame without the `b`:**

```python
with open("demo_frame.bin") as fh:
    demo_frame = fh.read()
```
```
(.venv) $ python3 textmode.py
Traceback (most recent call last):
  File "/home/kali/cyberlabs/Module1-Network-Attacks-and-Defense/Session1/textmode.py", line 2, in <module>
    demo_frame = fh.read()
  File "<frozen codecs>", line 325, in decode
UnicodeDecodeError: 'utf-8' codec can't decode byte 0x80 in position 22: invalid start byte
```

`open(path)` is text mode, which decodes the file as UTF-8.
Byte 22 is the TTL, `0x80`, which is not valid UTF-8, so the read stops there.
A frame whose bytes happen to decode is worse: it reads without an error, as the wrong type.
Always pass `"rb"`.

**Assigning to `bytes`:**

```python
with open("demo_frame.bin", "rb") as fh:
    demo_frame = fh.read()
demo_frame[22] = 64
```
```
(.venv) $ python3 immutable.py
Traceback (most recent call last):
  File "/home/kali/cyberlabs/Module1-Network-Attacks-and-Defense/Session1/immutable.py", line 3, in <module>
    demo_frame[22] = 64
    ~~~~~~~~~~^^^^
TypeError: 'bytes' object does not support item assignment
```

What `read()` returns is `bytes`, which cannot be changed.
Copy it first, `changed_frame = bytearray(demo_frame)`, and edit the copy.

**A number above 255 in `bytes([...])`:**

```python
address = bytes([192, 168, 56, 256])
```
```
(.venv) $ python3 bigbyte.py
Traceback (most recent call last):
  File "/home/kali/cyberlabs/Module1-Network-Attacks-and-Defense/Session1/bigbyte.py", line 1, in <module>
    address = bytes([192, 168, 56, 256])
ValueError: bytes must be in range(0, 256)
```

One byte holds 0 to 255.
A value that needs more than one byte is packed with `struct`, below.

---

# Fixed Byte Layouts: `struct`

A header is a **fixed byte layout**: each field has a set width at a set offset.
`struct` converts between Python numbers and such a layout, so building or reading a whole header is one call.

## `pack` and `unpack`

```python
import struct
udp_header = struct.pack("!HHHH", 51514, 53, 12, 0)
print(udp_header.hex(" "), len(udp_header))
with open("demo_frame.bin", "rb") as fh:
    demo_frame = fh.read()
print(struct.unpack("!HH", demo_frame[16:20]))
total_length, identification = struct.unpack("!HH", demo_frame[16:20])
print(total_length, identification)
ttl, = struct.unpack("!B", demo_frame[22:23])
print(ttl)
for fmt in ("!6s6sH", "!BBHHHBBH4s4s", "!HHLLBBHHH", "!HHHH", "!HHBBH6s4s6s4s"):
    print(fmt, struct.calcsize(fmt))
```
```
(.venv) $ python3 structdemo.py
c9 3a 00 35 00 0c 00 00 8
(76, 14879)
76 14879
128
!6s6sH 14
!BBHHHBBH4s4s 20
!HHLLBBHHH 20
!HHHH 8
!HHBBH6s4s6s4s 28
```

- `pack(format, values...)` writes the values into bytes, in order.
- `unpack(format, data)` reads them back, and **always returns a tuple**, even for one field.
  Unpack it into names (`total_length, identification = ...`), or into one name with a trailing comma (`ttl, = ...`).
- `calcsize(format)` is the number of bytes a format describes.
  The slice you hand `unpack` must be exactly that long.

A format string is a **byte-order prefix** followed by one letter per field.
The letters this session uses:

| Letter | Reads and writes | Size with `!` | Fields it maps to here |
|---|---|---|---|
| `B` | unsigned char | 1 byte | version and IHL, TTL, protocol, TCP flags |
| `H` | unsigned short | 2 bytes | ports, total length, checksums, EtherType |
| `L` | unsigned long | **4 bytes** | TCP sequence and acknowledgment numbers |
| `4s` | raw bytes | 4 bytes | an IPv4 address |
| `6s` | raw bytes | 6 bytes | a MAC address |

The headers this session builds or reads, each as one format string, with the sizes `calcsize` printed above:

| Header | Format | Bytes |
|---|---|---|
| Ethernet | `!6s6sH` | 14 |
| IPv4, no options | `!BBHHHBBH4s4s` | 20 |
| TCP, no options | `!HHLLBBHHH` | 20 |
| UDP | `!HHHH` | 8 |
| ARP for IPv4 over Ethernet | `!HHBBH6s4s6s4s` | 28 |

## Byte order: `!` and `<`

```python
import struct
with open("demo_frame.bin", "rb") as fh:
    demo_frame = fh.read()
port_bytes = demo_frame[36:38]
print(port_bytes.hex(" "))
print(struct.unpack("!H", port_bytes)[0], struct.unpack("<H", port_bytes)[0])
print(struct.pack("!H", 8080).hex(" "), struct.pack("<H", 8080).hex(" "))
print(struct.calcsize("L"), struct.calcsize("!L"))
```
```
(.venv) $ python3 byteorder.py
1f 90
8080 36895
1f 90 90 1f
8 4
```

- `!` means **network byte order**, big-endian: the first byte of a field is its most significant.
  The wire is big-endian, so `1f 90` is `0x1f90`, port 8080.
- `<` means little-endian, the order of an x86 or ARM lab machine: the same two bytes read as `0x901f`, 36895.
  Both are plausible port numbers, which is why this bug survives testing.
- With no prefix, `struct` uses the machine's **native** order *and* native sizes.
  On 64-bit Linux, native `L` is 8 bytes, against 4 with `!`.

> [!tip] The `!` prefix does two jobs
> It fixes the byte order to the wire's, and it fixes each letter's size to the standard one.
> Every format string in this session starts with `!` for both reasons.
> You never build a frame with `<`: it is there so you can read the same bytes both ways and see the difference.

## Common mistakes

**No byte-order prefix:**

```python
import struct
with open("demo_frame.bin", "rb") as fh:
    demo_frame = fh.read()
seq = struct.unpack("L", demo_frame[38:42])[0]
```
```
(.venv) $ python3 native.py
Traceback (most recent call last):
  File "/home/kali/cyberlabs/Module1-Network-Attacks-and-Defense/Session1/native.py", line 4, in <module>
    seq = struct.unpack("L", demo_frame[38:42])[0]
          ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^
struct.error: unpack requires a buffer of 8 bytes
```

Native `L` is 8 bytes, and the slice holds the 4 the wire carries.
`"!L"` reads them.
For `H`, native and standard sizes agree, so a missing `!` raises nothing and returns the wrong number instead.

**Formatting the tuple instead of the number:**

```python
import struct
with open("demo_frame.bin", "rb") as fh:
    demo_frame = fh.read()
dst_port = struct.unpack("!H", demo_frame[36:38])
print(dst_port)
print(f"{dst_port:04x}")
```
```
(.venv) $ python3 tuplefmt.py
(8080,)
Traceback (most recent call last):
  File "/home/kali/cyberlabs/Module1-Network-Attacks-and-Defense/Session1/tuplefmt.py", line 6, in <module>
    print(f"{dst_port:04x}")
            ^^^^^^^^^^^^^^
TypeError: unsupported format string passed to tuple.__format__
```

`unpack` returned `(8080,)`, a tuple of one.
Take `[0]`, or write `dst_port, = ...`.

**A format string with a letter missing:**

```python
import struct
udp_header = struct.pack("!HHH", 51514, 53, 12, 0)
```
```
(.venv) $ python3 count.py
Traceback (most recent call last):
  File "/home/kali/cyberlabs/Module1-Network-Attacks-and-Defense/Session1/count.py", line 2, in <module>
    udp_header = struct.pack("!HHH", 51514, 53, 12, 0)
struct.error: pack expected 3 items for packing (got 4)
```

Count the letters against the fields: one letter for each value.
The error names both numbers.

**A value too large for its field:**

```python
import struct
udp_header = struct.pack("!HHHH", 51514, 65536, 12, 0)
```
```
(.venv) $ python3 toolarge.py
Traceback (most recent call last):
  File "/home/kali/cyberlabs/Module1-Network-Attacks-and-Defense/Session1/toolarge.py", line 2, in <module>
    udp_header = struct.pack("!HHHH", 51514, 65536, 12, 0)
struct.error: 'H' format requires 0 <= number <= 65535
```

A 2-byte field holds 0 to 65535.
A value outside it is a bug in the value, not in the format.

---

# Reading a Header

Reading a header is reading bytes at offsets.
Some fields are half a byte or a single bit, and the boundaries between headers are computed from length fields, never assumed.

## Nibbles and flag bits

A **nibble** is 4 bits, half a byte.
Several fields are a nibble, packed two to a byte: shift right for the high one, mask for the low one.

```python
with open("demo_frame.bin", "rb") as fh:
    demo_frame = fh.read()
print(f"{demo_frame[14]:#04x} -> version {demo_frame[14] >> 4}, IHL {demo_frame[14] & 0x0F}")
print(f"{demo_frame[46]:#04x} -> data offset {demo_frame[46] >> 4}")
print(f"{(4 << 4) | 5:#04x}")
flags = demo_frame[47]
print(f"{flags:#04x} {flags:08b} ACK {bool(flags & 0x10)} PSH {bool(flags & 0x08)} SYN {bool(flags & 0x02)}")
```
```
(.venv) $ python3 nibbles.py
0x45 -> version 4, IHL 5
0x80 -> data offset 8
0x45
0x18 00011000 ACK True PSH True SYN False
```

- `>> 4` drops the low four bits and leaves the high nibble.
  `& 0x0F` keeps only the low four bits.
- To build the byte, shift the high value up by four and OR the low one in: `(4 << 4) | 5` is `0x45`.
- IHL and the TCP data offset both count **4-byte words**: this TCP header's data offset of 8 means 32 bytes.
- A flag is one bit: `flags & 0x10` is non-zero when ACK is set.
  `08b` prints the byte as eight binary digits, so each flag can be seen in place.

## Boundaries computed from fields

Every boundary comes from a field: the transport header starts after IHL × 4 bytes of IPv4, the payload starts after the transport header, and the packet ends where IPv4's total length says.

```python
import struct
for path in ("demo_frame.bin", "demo_short.bin"):
    with open(path, "rb") as fh:
        frame = fh.read()
    ihl = frame[14] & 0x0F
    total_length = struct.unpack("!H", frame[16:18])[0]
    protocol = frame[23]
    transport = 14 + ihl * 4
    if protocol == 6:
        start = transport + (frame[transport + 12] >> 4) * 4
    else:
        start = transport + 8
    end = 14 + total_length
    print(f"{path}: {len(frame)} bytes, protocol {protocol}, payload {start}:{end} {frame[start:end]!r}")
```
```
(.venv) $ python3 bounds.py
demo_frame.bin: 90 bytes, protocol 6, payload 66:90 b'GET /status HTTP/1.0\r\n\r\n'
demo_short.bin: 60 bytes, protocol 17, payload 42:53 b'<13>reboot\n'
```

- TCP (protocol 6) states its own header length, in the high nibble of its byte 12.
  UDP (protocol 17) always has an 8-byte header.
- The end is `14 + total_length`: the Ethernet header plus every byte IPv4 says it carries.
  For `demo_short.bin` that is 53, seven bytes before the end of the file.

## Common mistakes

**A fixed payload offset:**

```python
with open("demo_frame.bin", "rb") as fh:
    demo_frame = fh.read()
print(demo_frame[54:])
```
```
(.venv) $ python3 fixed54.py
b'\x01\x01\x08\n\x00B\xf1\xa3\x00\xb7\x1c\x05GET /status HTTP/1.0\r\n\r\n'
```

54 is where a payload starts only when IPv4 and TCP both have their minimum 20-byte headers.
This TCP header carries 12 bytes of options, so the slice begins inside them: `01 01 08 0a` and the two timestamps sit in front of the request.
Compute the start from IHL and the data offset on every frame.

**Ending the payload at the end of the file:**

```python
with open("demo_short.bin", "rb") as fh:
    short_frame = fh.read()
payload = short_frame[42:]
print(payload, len(payload))
print(payload == b"<13>reboot\n")
```
```
(.venv) $ python3 lenend.py
b'<13>reboot\n\x00\x00\x00\x00\x00\x00\x00' 18
False
```

Ethernet pads a frame shorter than 60 bytes, so a capture of it carries bytes the application never sent.
The slice runs to the end of the file and takes the seven padding bytes with it, so it no longer equals what was sent.
End at `14 + total_length`.

**Swapping the two nibbles:**

```python
with open("demo_frame.bin", "rb") as fh:
    demo_frame = fh.read()
version = demo_frame[14] & 0x0F
ihl = demo_frame[14] >> 4
print("version", version, "IHL", ihl, "-> TCP at", 14 + ihl * 4)
```
```
(.venv) $ python3 swapped.py
version 5 IHL 4 -> TCP at 30
```

The **high** nibble is the version and the **low** nibble is IHL.
Swapped, IHL reads 4, which is below IPv4's minimum of 5, and every offset after it lands 4 bytes early.

---

# The Internet Checksum

The IPv4 header checksum, and the TCP and UDP checksums, are the same arithmetic: a **one's-complement sum** of the data as 16-bit words, then the complement of that sum.
It catches accidental damage such as a flipped bit, and nothing more.

## The sum, the fold and the receiver's check

```python
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


with open("demo_frame.bin", "rb") as fh:
    demo_frame = fh.read()
ihl = demo_frame[14] & 0x0F
header = demo_frame[14:14 + ihl * 4]
zeroed = header[:10] + b"\x00\x00" + header[12:]
print(f"stored    0x{header[10:12].hex()}")
print(f"computed  0x{checksum(zeroed):04x}")
print(f"receiver  0x{ones_complement_sum(header):04x} -> 0x{checksum(header):04x}")
edited = bytearray(header)
edited[8] = 64
print(f"TTL 64    0x{ones_complement_sum(bytes(edited)):04x} -> 0x{checksum(bytes(edited)):04x}")
```
```
(.venv) $ python3 cksumdemo.py
stored    0xce70
computed  0xce70
receiver  0xffff -> 0x0000
TTL 64    0xbfff -> 0x4000
```

- Each pair of bytes is one 16-bit word, high byte first: `(data[i] << 8) | data[i + 1]`.
- **The fold**: a sum can grow past 16 bits, and the bits that carry out are added back into the low end, not dropped.
  This header's words add up to more than `0xFFFF`, so the fold changes the result here.
- The sender sums the header with its checksum field **zeroed** (bytes 10 and 11 of the header), complements the sum and stores it.
- The receiver sums the header **as received**, checksum included.
  A good header sums to `0xffff`, whose complement is `0x0000`.
- After one byte changes, here the TTL lowered to 64 without recomputing, the receiver's check no longer comes to `0x0000`.
  A router that lowers the TTL recomputes the checksum, and so can anyone else who edits a header.

## Common mistakes

**Summing without zeroing the checksum field:**

```python
def ones_complement_sum(data):
    total = 0
    for i in range(0, len(data), 2):
        total += (data[i] << 8) | data[i + 1]
        total = (total & 0xFFFF) + (total >> 16)
    return total


with open("demo_frame.bin", "rb") as fh:
    demo_frame = fh.read()
ihl = demo_frame[14] & 0x0F
header = demo_frame[14:14 + ihl * 4]
print(f"stored 0x{header[10:12].hex()}, computed 0x{~ones_complement_sum(header) & 0xFFFF:04x}")
```
```
(.venv) $ python3 nozero.py
stored 0xce70, computed 0x0000
```

The stored checksum was summed into itself, so the result is the receiver's check, `0x0000`, not a checksum.
Zero bytes 10 and 11 of the header before summing.

**Dropping the carry instead of folding it:**

```python
def ones_complement_sum(data):
    total = 0
    for i in range(0, len(data), 2):
        total += (data[i] << 8) | data[i + 1]
    return total & 0xFFFF


with open("demo_frame.bin", "rb") as fh:
    demo_frame = fh.read()
ihl = demo_frame[14] & 0x0F
header = demo_frame[14:14 + ihl * 4]
zeroed = header[:10] + b"\x00\x00" + header[12:]
print(f"stored 0x{header[10:12].hex()}, computed 0x{~ones_complement_sum(zeroed) & 0xFFFF:04x}")
```
```
(.venv) $ python3 nofold.py
stored 0xce70, computed 0xce73
```

`& 0xFFFF` at the end throws away the bits that carried out of 16, and here they were worth 3.
On a header whose sum never passes `0xFFFF`, the same code gives the right answer, which is how it survives testing.
Fold inside the loop, on every word.

---

# Encoding and Hashing

Two standard-library modules appear in this session's code, each to make a point about what protects data and what does not.

## `base64`: reversible encoding, not encryption

`base64` turns any bytes into a printable ASCII alphabet and back, with `b64encode` and `b64decode`.
This session meets it in HTTP Basic authentication, where a username and password are sent base64-encoded.

```python
import base64
token = base64.b64encode(b"alice:wonderland")
print(token)
print(base64.b64decode(token))
line = b"Authorization: Basic " + token + b"\r\n"
print(base64.b64decode(line.split(b"Basic ")[1].split(b"\r\n")[0]).decode())
```
```
(.venv) $ python3 b64demo.py
b'YWxpY2U6d29uZGVybGFuZA=='
b'alice:wonderland'
alice:wonderland
```

The last line takes the token out of a header line: split after `Basic `, then cut at the line end, then decode.

> [!warning] Base64 is encoding, not a secret
> `YWxpY2U6d29uZGVybGFuZA==` looks scrambled but reverses with one call and no key.
> Anyone who reads the bytes off the wire reads the credentials.
> The fix is never to decode it better: it is TLS, so the bytes are ciphertext before they are sent.

## `hashlib`: a cryptographic hash, for contrast

You do not write `hashlib` code this session, but the Home Task's `make_lab_capture.py` calls `hashlib.sha256(...).digest()` once, to stand in for the ciphertext of a TLS record.

```python
import hashlib
digest = hashlib.sha256(b"GET /status HTTP/1.0").digest()
print(len(digest), digest.hex())
print(hashlib.sha256(b"GET /status HTTP/1.1").hexdigest())
```
```
(.venv) $ python3 hashdemo.py
32 98a6b64363e515ddddb0fabbc25283fe1d0374ddfbe7097beb98e89418bea8fb
8d3f17cc3493f1c639054253dc526c8e306727374cfe745e458c045bfb851dd4
```

`digest()` is 32 raw bytes, and `hexdigest()` is the same as hex text.
One character changed in the input, and nothing in the two outputs lines up.

> [!note] Checksum, hash and signature
> The Internet checksum is cheap arithmetic that catches accidental damage.
> Anyone can recompute it, so it proves nothing about *who* wrote the bytes.
> A cryptographic hash such as SHA-256 is one-way and collision-resistant, but anyone can compute it too.
> A **signature** or an HMAC adds a key, so only the key holder could have produced it.
> Integrity is not authenticity, and the Home Task's pair *A Checksum Is Not a Signature* makes this distinction with real bytes.

## Common mistakes

**Decoding the whole header value, `Basic ` included:**

```python
import base64
print(base64.b64decode(b"Basic YWxpY2U6d29uZGVybGFuZA=="))
```
```
(.venv) $ python3 b64whole.py
b'\x05\xab"q\x85\xb1\xa5\x8d\x94\xe9\xdd\xbd\xb9\x91\x95\xc9\xb1\x85\xb9\x90'
```

`b64decode` skips the space and decodes `Basic` as if it were part of the token, so every byte after it is shifted, and it raises no error.
Split off the scheme name first, as in the example above.

---

# Command-Line Arguments: `sys.argv`

A tool that takes its input file from the command line can be pointed at any frame without editing it.

## `sys.argv` with a default

```python
import sys
print(sys.argv)
path = sys.argv[1] if len(sys.argv) > 1 else "demo_frame.bin"
with open(path, "rb") as fh:
    print(path, len(fh.read()), "bytes")
```
```
(.venv) $ python3 argv.py
['argv.py']
demo_frame.bin 90 bytes
(.venv) $ python3 argv.py demo_short.bin
['argv.py', 'demo_short.bin']
demo_short.bin 60 bytes
```

`sys.argv` is a list of strings: `sys.argv[0]` is the script's name, and `sys.argv[1]` is the first word after it.
The `len(sys.argv) > 1` guard gives the tool a default file, so a bare run still works and a named file overrides it.

## Common mistakes

**Reading `sys.argv[1]` with no guard:**

```python
import sys
path = sys.argv[1]
print(path)
```
```
(.venv) $ python3 argv_noguard.py
Traceback (most recent call last):
  File "/home/kali/cyberlabs/Module1-Network-Attacks-and-Defense/Session1/argv_noguard.py", line 2, in <module>
    path = sys.argv[1]
           ~~~~~~~~^^^
IndexError: list index out of range
```

Run with no argument, the list holds only the script's name.
Guard with `len(sys.argv) > 1` and a default, as above.

---

# Command-Line Tools

These are the tools that let you see the bytes you built, compare them, and prove two files or two outputs are the same.

## `hexdump -C`: the canonical byte view

`hexdump -C` ("canonical") prints a file as offsets, hex bytes and printable characters, side by side.
It is the tool for every time bytes do not look right.

```
(.venv) $ hexdump -C demo_frame.bin
00000000  52 54 00 12 35 02 08 00  27 5c 1d 7e 08 00 45 00  |RT..5...'\.~..E.|
00000010  00 4c 3a 1f 40 00 80 06  ce 70 c0 a8 38 65 c0 a8  |.L:.@....p..8e..|
00000020  38 66 c9 3a 1f 90 1a 2b  3c 4d 5e 6f 70 81 80 18  |8f.:...+<M^op...|
00000030  01 f6 2a cb 00 00 01 01  08 0a 00 42 f1 a3 00 b7  |..*........B....|
00000040  1c 05 47 45 54 20 2f 73  74 61 74 75 73 20 48 54  |..GET /status HT|
00000050  54 50 2f 31 2e 30 0d 0a  0d 0a                    |TP/1.0....|
0000005a
```

A run of identical lines collapses to `*`:

```
(.venv) $ head -c 40 /dev/zero > zeros.bin
(.venv) $ hexdump -C zeros.bin
00000000  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
*
00000020  00 00 00 00 00 00 00 00                           |........|
00000028
```

| Column | Meaning |
|---|---|
| `00000000` | the offset of the line's first byte, as 8 hex digits |
| the two groups of eight | the line's 16 bytes, with one extra space between the groups |
| `\|...\|` | the same bytes as printable ASCII (`0x20` to `0x7E`), every other byte shown as `.` |
| `*` | one or more lines identical to the line above, left out |
| the last line | the file's total length, as 8 hex digits, alone |

> [!tip] The offset column is your ruler
> Each line starts 16 bytes (`0x10`) after the one above, so offset `0x16` (22) is the seventh byte of the `00000010` line: `80`, this frame's TTL of 128.
> The next byte, `06`, is the protocol, and `ce 70` after it is the header checksum.
> In `zeros.bin`, the `*` stands for the line at `00000010`, and the last line says the file is `0x28`, 40 bytes.

## `strings`: the readable runs in a binary file

`strings` prints each run of printable characters at least 4 long, in the order the runs sit in the file.
It is a first look at a capture: what text is sitting in it in the clear.

```
(.venv) $ strings demo_frame.bin
+<M^op
GET /status HTTP/1.0
(.venv) $ strings -n 3 demo_short.bin
': @
`<13>reboot
```

`-n` sets the minimum run length.
Header bytes that happen to be printable come out too: `+<M^op` is six bytes of TCP sequence and acknowledgment numbers, and the `` ` `` in front of `<13>reboot` is the last byte of the UDP checksum, `0x60`.
`strings` does not know where a header ends, so its output shows *what* text a file holds, never which bytes are payload.

## `cmp`: a byte-for-byte comparison

`cmp` compares two files byte by byte and stops at the first difference.

```
(.venv) $ cmp demo_frame.bin copy_frame.bin; echo $?
0
(.venv) $ cmp demo_frame.bin demo_short.bin; echo $?
demo_frame.bin demo_short.bin differ: byte 18, line 1
1
```

- Identical files: `cmp` prints nothing, and its exit status (`$?`) is 0.
  `cmp a b && echo IDENTICAL` therefore prints `IDENTICAL` only on an exact copy.
- Different files: it names the **first** differing byte, counting from 1, and exits with 1.
  Byte 18 is offset 17: the second byte of IPv4's total length, `4c` in one frame and `27` in the other.
  The position names the field to check.

## `diff` and `<(...)`: comparing two outputs

`diff` prints the lines that differ between two files, and nothing when they agree.
**Process substitution**, `<(command)`, hands a command's output to `diff` as if it were a file, so two commands' outputs can be compared without saving either.

```
(.venv) $ diff <(hexdump -C demo_frame.bin) <(hexdump -C copy_frame.bin) && echo IDENTICAL
IDENTICAL
(.venv) $ diff <(hexdump -C demo_frame.bin | head -2) <(hexdump -C demo_short.bin | head -2)
2c2
< 00000010  00 4c 3a 1f 40 00 80 06  ce 70 c0 a8 38 65 c0 a8  |.L:.@....p..8e..|
---
> 00000010  00 27 3a 20 40 00 80 11  ce 89 c0 a8 38 65 c0 a8  |.': @.......8e..|
```

`2c2` means line 2 of the first output must *change* into line 2 of the second.
`<` marks the first output's line and `>` the second's.
Line 1 matched, so `diff` does not show it.
The Practical Guide's hexdump exercise uses the first form to prove a hand-written dump matches `hexdump -C` to the byte.

## `head`: the first lines of a long output

`head -n N`, or `head -N`, prints only the first `N` lines.
`head -c N` prints the first `N` bytes instead, which is how `zeros.bin` was made above.

```
(.venv) $ hexdump -C demo_frame.bin | head -3
00000000  52 54 00 12 35 02 08 00  27 5c 1d 7e 08 00 45 00  |RT..5...'\.~..E.|
00000010  00 4c 3a 1f 40 00 80 06  ce 70 c0 a8 38 65 c0 a8  |.L:.@....p..8e..|
00000020  38 66 c9 3a 1f 90 1a 2b  3c 4d 5e 6f 70 81 80 18  |8f.:...+<M^op...|
```

A 1024-byte capture is 64 lines of dump, and `head` keeps the first screen readable while you get your bearings.

## `python3` and `.venv`: running the tools

Every script runs under `python3`, inside the session's virtual environment.

```
(.venv) $ which python3
/home/kali/cyberlabs/Module1-Network-Attacks-and-Defense/Session1/.venv/bin/python3
```

`which` names the file the shell runs for a command.
Inside the environment it is the environment's own `python3`.
Nothing this session uses is a third-party package, so `.venv` keeps one session's Python apart from another's rather than installing anything.

> [!note] Setup lives in the guide
> Creating the working folder and its `.venv` is in the Practical Guide's **Pre-Session Setup**, which is the single source of truth for it.
> If your prompt does not start with `(.venv)`, open a new terminal in the working folder, which activates it by itself, or run `source .venv/bin/activate`.

## Common mistakes

**`hexdump` without `-C`:**

```
(.venv) $ hexdump demo_frame.bin | head -2
0000000 5452 1200 0235 0008 5c27 7e1d 0008 0045
0000010 4c00 1f3a 0040 0680 70ce a8c0 6538 a8c0
```

Without `-C`, `hexdump` prints 2-byte words read in the machine's little-endian order, so every pair is reversed: the file starts `52 54`, shown as `5452`.
This is the byte-order bug from `struct`, made by a tool.
Always pass `-C`.

**`<(...)` under `sh`:**

```
(.venv) $ sh -c 'diff <(hexdump -C demo_frame.bin) <(hexdump -C copy_frame.bin)'
sh: 1: Syntax error: "(" unexpected
```

Process substitution belongs to bash and zsh, and Kali's `sh` is `dash`, which does not have it.
Run the line in the terminal itself, whose shell is zsh, or save each output to a file and `diff` the two files.
