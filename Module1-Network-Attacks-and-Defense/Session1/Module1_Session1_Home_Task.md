# Module 1 · Session 1 — Home Task

## Reading and Rewriting the Wire

### Professional Training in Cybersecurity I

---

> [!note] How this home task works
> This home task is about **doing something with the bytes**, not only reading them.
> You build **two offense/defense pairs**: for each idea, one tool that abuses what a packet's own headers allow, and one tool a defender uses to catch it.
> Every task opens with a **security scenario**, so you can see where the tool fits.
>
> Each task is marked **🧩 GUIDED** or **🔨 FROM SCRATCH**.
> A guided task gives you a starter with `# TODO` gaps, so the plumbing is done and you can focus on the idea.
> A from-scratch task gives you the requirements, and you write the whole script.
>
> Your worksheet is **`Module1_Session1_Home_Task_Submission.md`**, already in your repository's `Module1-Network-Attacks-and-Defense/Session1` folder since the Practical Guide's setup.
> Work in `~/cyberlabs/Module1-Network-Attacks-and-Defense/Session1`, the working folder you made for the Practical Guide, with its `.venv`.
> Everything uses the Python standard library only.
> Paste your finished code, its output, your screenshots and your answers into the worksheet, which is the graded document.

> [!important] Everything here is required
> There are no optional parts: all four tools, every run and every question.
> Every script must run without errors.

> [!warning] These are lab tools, on lab bytes
> Both offensive tools work on capture files you generate on your own machine.
> Nothing is sent anywhere, and nothing is intercepted off a live network.
> The *skills* are real, though: forging a header so it still validates, and reading someone's login off a capture, are things you may only do to traffic you own or are authorized to test.
> You build them to understand what a checksum does and does not prove, and why plaintext on a network is plaintext for everyone on the path.

---

# Before You Start

1. **Pull your repository**, because your instructor's feedback on the Practical Guide arrives there:

   ```bash
   cd ~/student-YOUR-USERNAME
   git pull
   ```

2. **Open your working folder** and a new terminal in it:

   ```bash
   code ~/cyberlabs/Module1-Network-Attacks-and-Defense/Session1
   ```

   In VS Code, open **Terminal**, then **New Terminal**.
   It activates `.venv` by itself, so its prompt starts with `(.venv)`.

---

# Pair 1: A Checksum Is Not a Signature

*Shared idea: the IPv4 header checksum proves that the header was not corrupted in transit, and nothing else.*
*The attacker edits a field and fixes the checksum, so the defender has to catch the lie some other way.*

---

## Task 1: Forge a Source Address That Still Verifies — REQUIRED

> **🗡️ Offensive · 🧩 GUIDED: complete the starter below** | Difficulty: ⭐⭐ Medium
> *Copy the starter out, fill its three `# TODO` gaps in your IDE, and run it until it prints what the run below shows.*

> [!note] Security scenario
> A checksum feels like a seal, so it is worth proving that it is not one.
> Every router on the path lowers the TTL and recomputes the checksum, and the header it forwards verifies perfectly.
> Here you go further: rewrite the **source address** so the frame claims to come from a different host, fix the checksum, and watch the header still pass every arithmetic test.
> A checksum survives editing because anyone who can edit the header can recompute it.
> **The new angle:** forge a field the sender should never be able to change, and make the header agree with the forgery.

This task edits the reference frame from the Practical Guide.
The block below is the guide's generator, unchanged, so the task does not depend on a file left over from the guide.
Save it as `make_ref_frame.py`, or keep the copy already in your folder:

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

Now create `header_forger.py` and complete its three TODOs:

```python
#!/usr/bin/env python3
# @starter header_forger.py
"""header_forger.py — edit a header, then make the checksum agree with the lie.

A checksum is arithmetic over the bytes, so anyone who can change a field can
recompute it. This writes four versions of the reference frame:

  forged_ttl.bin     time to live lowered, checksum recomputed
  forged_sloppy.bin  source address rewritten, checksum NOT recomputed
  forged_spoof.bin   source address rewritten, checksum recomputed
  forged_length.bin  payload extended, total length left as it was

Then audit all four with packet_auditor.py and see which ones a defender can
actually catch.
"""
import struct


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


def recompute(frame):
    """Zero the checksum field, sum the header, write the complement back."""
    frame = bytearray(frame)
    ihl = frame[14] & 0x0F
    header = bytes(frame[14:14 + ihl * 4])
    # TODO 1: make this header check out. Zero its two checksum bytes
    #         (header[10:12]), run checksum() over that, and write the result
    #         back with struct.pack('!H', ...) into frame[24:26] — the IPv4
    #         checksum field's real position in the frame.
    return bytes(frame)


def save(name, frame, note):
    with open(name, "wb") as fh:
        fh.write(frame)
    report(name, frame, note)


def report(name, frame, note):
    ihl = frame[14] & 0x0F
    print(f"[+] {name:<20} {len(frame):>3} bytes  ttl {frame[22]:>3}  "
          f"src {'.'.join(str(b) for b in frame[26:30])}  "
          f"len {struct.unpack('!H', frame[16:18])[0]:>3}  "
          f"cksum 0x{struct.unpack('!H', frame[24:26])[0]:04x}  "
          f"{'valid' if checksum(frame[14:14 + ihl * 4]) == 0 else 'INVALID'}  {note}")


def main():
    with open("ref_frame.bin", "rb") as fh:
        original = fh.read()
    report("ref_frame.bin", original, "the frame as captured")

    # 1. Lower the TTL, exactly as every router on the path does, and make the
    #    checksum agree. Nothing distinguishes this from legitimate forwarding.
    ttl = bytearray(original)
    ttl[22] = 63
    save("forged_ttl.bin", recompute(bytes(ttl)), "TTL rewritten, checksum fixed")

    # 2. Claim to be a different host — and forget the checksum. Careless.
    sloppy = bytearray(original)
    sloppy[26:30] = bytes([10, 0, 0, 99])
    save("forged_sloppy.bin", bytes(sloppy), "source spoofed, checksum stale")

    # TODO 2: tell the same lie properly. Take `sloppy` (source already
    #         rewritten), recompute its checksum, and save it as
    #         "forged_spoof.bin" with a note. This is the frame the defender
    #         cannot catch on arithmetic alone.

    # TODO 3: extend the payload but leave the IP header's total length alone.
    #         Copy `original`, replace frame[54:] with these 61 bytes:
    #           b"hello, plus a great many extra bytes the header never counted"
    #         and save it as "forged_length.bin" WITHOUT recomputing anything —
    #         the header still checksums; it is the frame that now disagrees
    #         with what the header claims it carries.

    print("\n[*] Three of these carry a header that verifies perfectly. Verifying is "
          "all a checksum does.")


if __name__ == "__main__":
    main()
```

**Run it:**

```bash
python3 make_ref_frame.py
python3 header_forger.py
```

Your completed starter must print exactly this:

```
(.venv) $ python3 make_ref_frame.py
[+] ref_frame.bin        59 bytes
[+] ref_frame_padded.bin 60 bytes (padded to the 60-byte minimum)
[*] Read them with:  hexdump -C ref_frame.bin
(.venv) $ python3 header_forger.py
[+] ref_frame.bin         59 bytes  ttl  64  src 10.0.0.4  len  45  cksum 0x087d  valid  the frame as captured
[+] forged_ttl.bin        59 bytes  ttl  63  src 10.0.0.4  len  45  cksum 0x097d  valid  TTL rewritten, checksum fixed
[+] forged_sloppy.bin     59 bytes  ttl  64  src 10.0.0.99  len  45  cksum 0x087d  INVALID  source spoofed, checksum stale
[+] forged_spoof.bin      59 bytes  ttl  64  src 10.0.0.99  len  45  cksum 0x081e  valid  source spoofed, checksum recomputed
[+] forged_length.bin    115 bytes  ttl  64  src 10.0.0.4  len  45  cksum 0x087d  valid  payload extended, total length stale

[*] Three of these carry a header that verifies perfectly. Verifying is all a checksum does.
```

The `forged_spoof.bin` row reads `src 10.0.0.99` and `valid`: a spoofed source with a checksum that agrees.
Anyone who can edit a header can make its checksum agree again, and that is the point of this task.

> [!example] 📝 Submission
> Paste your completed `header_forger.py`, its output with all five rows, and a screenshot into your **Home Task Submission**.

---

## Task 2: Audit a Frame Against Its Own Headers — REQUIRED

> **🛡️ Defensive · 🔨 FROM SCRATCH** | Difficulty: ⭐⭐ Medium
> *Read the requirements and write the complete script yourself.*

> [!note] Security scenario
> If the checksum cannot tell you a frame is honest, consistency can tell you some of it.
> A frame assembled by hand, or altered clumsily, usually contradicts itself somewhere: a header length below its minimum, a total length that claims more bytes than were captured, or trailing bytes that padding cannot explain.
> You build the auditor that checks a frame against its *own* headers.
> Then you run it over the four forgeries and find out exactly which lie it catches and which it does not.

Create `packet_auditor.py`.

**Requirements:**

- Take one or more frame files on the command line (`sys.argv[1:]`).
- Check the **IPv4 header checksum** with the same `ones_complement_sum` routine: over the unmodified header it must complement to `0x0000`, or the header was edited (or corrupted) without being recomputed.
- Run these consistency checks, and collect a finding for each one that fails:
  - **version** is 4, and **IHL** is at least 5.
  - **total length** is not smaller than the header it counts (`ihl * 4`).
  - The frame holds what the header claims: `14 + total_length` is not past `len(frame)`.
  - There are no unexplained trailing bytes: bytes past `14 + total_length` are acceptable only as padding, and only up to Ethernet's 60-byte minimum.
  - For TCP, the **data offset** is at least 5, and the total length leaves room for that TCP header.
- Print `PASS` (no findings) or `FAIL` with each finding, and a closing summary line.
- End with one line that states the lesson: passing means **self-consistent, not honest**.

**Run it over the forgeries:**

```bash
python3 packet_auditor.py ref_frame.bin forged_ttl.bin forged_sloppy.bin forged_spoof.bin forged_length.bin
```

**What you should see, and must explain in your answers:**

| frame | verdict | why |
|---|---|---|
| `ref_frame.bin` | PASS | the honest original |
| `forged_ttl.bin` | PASS | legitimately rewritten, checksum fixed |
| `forged_sloppy.bin` | **FAIL** | checksum was not recomputed after the edit |
| `forged_spoof.bin` | **PASS** | the spoof your own forger did *properly* |
| `forged_length.bin` | **FAIL** | more bytes than the total length admits |

> [!tip] The forgery the auditor passes
> `forged_spoof.bin` has a forged source address, and the auditor passes it.
> That is not a bug in your tool.
> It is the limit of what a single frame's own headers can tell you.
> Catching *that* needs context the frame does not carry (who is really on this link), and later sessions on Layer 2 are built on that reasoning.

> [!example] 📝 Submission
> Paste your `packet_auditor.py`, its verdicts for all five frames, and a screenshot into your **Home Task Submission**, then answer the Pair 1 questions.

---

> [!tip] The connection
> `header_forger.py` edits a field and makes the checksum agree.
> `packet_auditor.py` shows that an agreeing checksum was never the same as an honest frame.
> The attacker relies on a checksum that anyone can recompute.
> The defender answers that the frame must still be consistent with itself, and then meets the limit of what one frame can prove.

---

# Pair 2: Plaintext Travels as Plaintext

*Shared idea: reading an application's data off a capture takes nothing but the headers.*
*The attacker harvests the secrets, and the defender reports which conversations were exposed and need encrypting.*

---

## Task 3: Read the Payloads Out of a Capture — REQUIRED

> **🗡️ Offensive · 🧩 GUIDED: complete the starter below** | Difficulty: ⭐⭐⭐ Hard
> *Copy the starter out, fill its two `# TODO` gaps in your IDE, and run it until it prints what the run below shows.*

> [!note] Security scenario
> In the Practical Guide's warm-up, an SMTP greeting sat readable in a hexdump.
> Real traffic is worse: logins, tokens and commands travel in the clear on protocols that never encrypted anything.
> Here you build the tool that reads them: walk a capture, follow each frame's chain to its payload, and print what the application sent.
> No decryption is involved, because there is nothing to decrypt.
> This is what an attacker on the path sees, and it is why the rest of the module cares about TLS.
> **The new angle:** carve the payload out of every frame in a capture and surface the credentials automatically.

> [!warning] Lab only: bytes you own
> This tool reads secrets straight out of a capture.
> Run it only on the capture you generate below, or on traffic you are authorized to inspect.
> Reading anyone else's traffic is unauthorized activity.

First, generate the capture: a short slice of one workstation's afternoon, with real, checksum-correct frames.
Save this as `make_lab_capture.py` and run it:

```python
#!/usr/bin/env python3
# @generator make_lab_capture.py
# @expect writes lab_capture.bin (640 bytes = 5 slots x 128)
"""make_lab_capture.py — write a short capture off the lab segment.

Five frames from one workstation's afternoon: two FTP commands, a web request,
a DNS lookup, and one TLS record. Every checksum is computed, so these are real
frames, not sketches.

The capture is a run of fixed 128-byte slots, one frame per slot, zero-padded —
so slot n is blob[n*128:(n+1)*128] and anything after the frame is buffer slack.

Writes lab_capture.bin.
"""
import hashlib
import struct

SLOT = 128
DST_MAC = bytes.fromhex("080027abcdef")
SRC_MAC = bytes.fromhex("080027123456")
CLIENT = bytes([10, 0, 0, 4])


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


def frame(payload, *, server, proto=6, src_port=50000, dst_port=80, ident=0x1C46):
    if proto == 6:
        transport = struct.pack("!HHLLBBHHH", src_port, dst_port,
                                0x001A2B3C, 0x00E5F6A7, 5 << 4, 0x18, 0xFFFF, 0, 0)
    else:
        transport = struct.pack("!HHHH", src_port, dst_port, 8 + len(payload), 0)

    pseudo = struct.pack("!4s4sBBH", CLIENT, server, 0, proto,
                         len(transport) + len(payload))
    value = checksum(pseudo + transport + payload)
    at = 16 if proto == 6 else 6
    transport = transport[:at] + struct.pack("!H", value) + transport[at + 2:]

    total_length = 20 + len(transport) + len(payload)
    header = struct.pack("!BBHHHBBH4s4s", 0x45, 0x00, total_length,
                         ident, 0x4000, 64, proto, 0, CLIENT, server)
    header = header[:10] + struct.pack("!H", checksum(header)) + header[12:]

    eth = struct.pack("!6s6sH", DST_MAC, SRC_MAC, 0x0800)
    return eth + header + transport + payload


def slot(data):
    if len(data) > SLOT:
        raise SystemExit(f"[!] frame of {len(data)} bytes will not fit a slot")
    return data.ljust(SLOT, b"\x00")


def dns_query(name):
    """A real DNS query: 12-byte header, then the name as length-prefixed labels."""
    qname = b"".join(bytes([len(part)]) + part.encode() for part in name.split("."))
    return (struct.pack("!HHHHHH", 0x2A1F, 0x0100, 1, 0, 0, 0)
            + qname + b"\x00" + struct.pack("!HH", 1, 1))


def tls_record():
    """One TLS application-data record: the 5-byte header, then ciphertext."""
    body = hashlib.sha256(b"tls record, lab segment").digest()
    return b"\x17\x03\x03" + struct.pack("!H", len(body)) + body


def main():
    files = bytes([10, 0, 0, 9])
    resolver = bytes([10, 0, 0, 53])

    frames = [
        frame(b"USER admin\r\n", server=files, src_port=50101, dst_port=21,
              ident=0x0101),
        frame(b"PASS Sup3rS3cr3t!\r\n", server=files, src_port=50101, dst_port=21,
              ident=0x0102),
        frame(b"GET /admin HTTP/1.1\r\n"
              b"Authorization: Basic YWRtaW46czNjcjN0\r\n\r\n",
              server=files, src_port=50102, dst_port=80, ident=0x0103),
        frame(dns_query("vault.lab.local"), server=resolver, proto=17,
              src_port=50103, dst_port=53, ident=0x0104),
        frame(tls_record(), server=files, src_port=50104, dst_port=443,
              ident=0x0105),
    ]

    blob = b"".join(slot(f) for f in frames)
    with open("lab_capture.bin", "wb") as fh:
        fh.write(blob)
    print(f"[+] lab_capture.bin  {len(blob)} bytes = {len(frames)} slots x {SLOT}")
    for n, f in enumerate(frames):
        print(f"    slot {n}: {len(f)}-byte frame")


if __name__ == "__main__":
    main()
```

Now create `payload_harvester.py` and complete its two TODOs:

```python
#!/usr/bin/env python3
# @starter payload_harvester.py
"""payload_harvester.py — read every application payload out of a capture.

Walk the capture slot by slot, follow the chain each frame declares
(EtherType -> protocol -> ports), carve the payload out at the offsets the
headers give, and print whatever the application put there. No decryption, no
cleverness: plaintext travels as plaintext, and this is all it takes to read it.

Usage:  python3 payload_harvester.py [capture.bin]
"""
import base64
import struct
import sys

SLOT = 128
PROTOCOLS = {1: "ICMP", 6: "TCP", 17: "UDP"}
INTERESTING = (b"USER ", b"PASS ", b"Authorization:", b"password", b"login")


def ipv4(raw):
    return ".".join(str(b) for b in raw)


def carve(s):
    """Return (summary, payload) for one slot, or (summary, None) if not IPv4."""
    ethertype = struct.unpack("!H", s[12:14])[0]
    if ethertype != 0x0800:
        return f"EtherType 0x{ethertype:04x} — not IPv4", None

    ihl = s[14] & 0x0F
    total_length = struct.unpack("!H", s[16:18])[0]
    proto = s[23]
    src, dst = ipv4(s[26:30]), ipv4(s[30:34])
    transport = 14 + ihl * 4

    # TODO 1: read the two ports (both TCP and UDP start with src/dst port, so
    #         struct.unpack('!HH', s[transport:transport+4]) works for either),
    #         and work out where the PAYLOAD starts:
    #           - TCP (proto 6): transport + data_offset*4, where the data
    #             offset is the HIGH nibble of s[transport + 12]
    #           - UDP (proto 17): transport + 8 (its header is a fixed 8 bytes)
    #           - anything else: return f"protocol {proto} — no ports to read", None
    src_port = dst_port = 0
    start = 0

    # TODO 2: the payload ENDS at 14 + total_length, never at len(s) — the rest
    #         of the slot is buffer slack. Slice it out and return it with a
    #         summary line, e.g.  f"{src}:{src_port} -> {dst}:{dst_port}  TCP"
    return "", None


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "lab_capture.bin"
    with open(path, "rb") as fh:
        blob = fh.read()

    for n in range(len(blob) // SLOT):
        summary, payload = carve(blob[n * SLOT:(n + 1) * SLOT])
        print(f"\n[slot {n}] {summary}")
        if payload is None:
            continue
        for line in payload.splitlines() or [b""]:
            shown = "".join(chr(b) if 0x20 <= b < 0x7F else "." for b in line)
            print(f"    | {shown}")

        for marker in INTERESTING:
            if marker in payload:
                print(f"    [!] contains {marker.decode().strip()!r} — in the clear")

        # HTTP Basic authentication is not encryption; it is base64 of user:pass.
        if b"Authorization: Basic " in payload:
            token = payload.split(b"Authorization: Basic ")[1].split(b"\r\n")[0]
            print(f"    [!] decoded credentials: "
                  f"{base64.b64decode(token).decode()!r}")

    print("\n[*] Every byte above came off the wire exactly as the application sent "
          "it. Reading it took the headers, and nothing else.")


if __name__ == "__main__":
    main()
```

**Run it:**

```bash
python3 make_lab_capture.py
python3 payload_harvester.py
```

Your completed starter must print exactly this:

```
(.venv) $ python3 make_lab_capture.py
[+] lab_capture.bin  640 bytes = 5 slots x 128
    slot 0: 66-byte frame
    slot 1: 73-byte frame
    slot 2: 116-byte frame
    slot 3: 75-byte frame
    slot 4: 91-byte frame
(.venv) $ python3 payload_harvester.py

[slot 0] 10.0.0.4:50101 -> 10.0.0.9:21  TCP
    | USER admin
    [!] contains 'USER' — in the clear

[slot 1] 10.0.0.4:50101 -> 10.0.0.9:21  TCP
    | PASS Sup3rS3cr3t!
    [!] contains 'PASS' — in the clear

[slot 2] 10.0.0.4:50102 -> 10.0.0.9:80  TCP
    | GET /admin HTTP/1.1
    | Authorization: Basic YWRtaW46czNjcjN0
    | 
    [!] contains 'Authorization:' — in the clear
    [!] decoded credentials: 'admin:s3cr3t'

[slot 3] 10.0.0.4:50103 -> 10.0.0.53:53  UDP
    | *............vault.lab.local.....

[slot 4] 10.0.0.4:50104 -> 10.0.0.9:443  TCP
    | .... ...x..L.c......n..?.%.h...*..HA.

[*] Every byte above came off the wire exactly as the application sent it. Reading it took the headers, and nothing else.
```

The FTP `USER` and `PASS` lines are readable as they were sent.
Your tool decodes the HTTP `Authorization: Basic` header to `admin:s3cr3t`, because HTTP Basic authentication is base64, not encryption.
The DNS frame gives up the hostname it looked up, between the dots that stand for its binary fields.
Only the TLS record stays unreadable.

> [!example] 📝 Submission
> Paste your completed `payload_harvester.py`, its output with the recovered credentials, and a screenshot into your **Home Task Submission**.

---

## Task 4: Report the Exposed Conversations — REQUIRED

> **🛡️ Defensive · 🔨 FROM SCRATCH** | Difficulty: ⭐⭐⭐ Hard
> *Read the requirements and write the complete script yourself.*

> [!note] Security scenario
> An attacker reads what is exposed.
> A defender has to *find* what is exposed before the attacker does, and rank it.
> You build the reporting tool: walk the same capture, and for each conversation decide whether its payload is readable text, and whether it carries anything that should never have been readable.
> The output is a prioritized list of conversations to encrypt.
> It also shows that the fix is never to parse more carefully: it is to stop sending the data in the clear.

Create `exposure_report.py`.

**Requirements:**

- Walk `lab_capture.bin` (the default) or a file given as `sys.argv[1]`, slot by slot, and carve each IPv4 TCP or UDP payload with the **same boundary arithmetic** as the harvester.
- Classify each conversation's payload:
  - **CLEARTEXT**: more than 90% of the bytes are printable.
  - **PARTIAL**: mostly binary, but with a run of 4 or more printable bytes, which is what `strings -n 4` would print (a protocol name, a hostname).
  - **opaque**: no printable run that long.
  - A printable byte is `0x20` to `0x7E`, plus tab, newline and carriage return.
- Flag any payload that contains a credential marker (`USER `, `PASS `, `Authorization: Basic `, `password`).
- Print one row per conversation: source → destination:port, protocol, payload size, the printable percentage, the verdict, and the credential finding if there is one.
- Close with a summary: how many conversations gave up something readable, how many carried credentials in the clear (listed by port), and how many resisted the tool, with the reason that last number is small.

**Run it:**

```bash
python3 exposure_report.py
```

**What you should see, and must explain in your answers:**

| conversation | verdict | note |
|---|---|---|
| `:21` FTP (USER) | CLEARTEXT | account name in the clear |
| `:21` FTP (PASS) | CLEARTEXT | password in the clear |
| `:80` HTTP | CLEARTEXT | HTTP Basic credentials |
| `:53` DNS | PARTIAL | the looked-up hostname leaks |
| `:443` TLS | opaque | encrypted before it was sent |

**Cross-check with the real tool** you are reinventing:

```bash
strings -n 4 lab_capture.bin
```

Your report should account for every readable string that `strings` prints.
It also adds what `strings` cannot: *which conversation* each string belongs to, and *which port* is leaking it.

> [!tip] PARTIAL is not safe
> The DNS frame is mostly binary, so it is not cleartext.
> But the hostname `vault.lab.local` sits in it, and tells an eavesdropper exactly what this host was looking for.
> Not fully readable and not exposed are different things, and a good report says so.

> [!example] 📝 Submission
> Paste your `exposure_report.py`, its full report, the `strings -n 4` output, and a screenshot into your **Home Task Submission**, then answer the Pair 2 questions.

---

> [!tip] The connection
> `payload_harvester.py` reads the secrets off the capture, and `exposure_report.py` walks the *same* capture and ranks what needs fixing.
> The parse is the same and the intent is opposite.
> Both tools stop at the same frame: the one conversation neither can read is the one that was encrypted before it was sent.
> The defense was never better parsing: it was TLS.

---

# Hand In

When all four tasks are done, commit your worksheet and its screenshots once, then push and check that GitHub has everything:

```bash
cd ~/student-YOUR-USERNAME
git add Module1-Network-Attacks-and-Defense/Session1
git commit -m "Module 1 Session 1: home task"
git push
git status
```

**Checkpoint:** `git status` says `Your branch is up to date with 'origin/main'.`, and on GitHub your Home Task Submission shows every screenshot.
If it says **ahead**, the push did not happen: read the error `git push` printed.
Only GitHub's copy counts: until the push succeeds, your work exists only on this machine.

---

# What "done" looks like

- `header_forger.py` prints the five rows above, with `forged_spoof.bin` reading `src 10.0.0.99` and `valid`
- `packet_auditor.py` passes `ref_frame.bin`, `forged_ttl.bin` and `forged_spoof.bin`, and fails `forged_sloppy.bin` and `forged_length.bin`
- `payload_harvester.py` prints the output above, with `admin:s3cr3t` decoded
- `exposure_report.py` rates the three FTP and HTTP conversations CLEARTEXT, DNS PARTIAL and TLS opaque, and flags the three that carry credentials
- Your worksheet holds all four tools' code, output, screenshots and answers, with **Anything that failed** and **AI Assistance** filled in
- On GitHub, `Module1-Network-Attacks-and-Defense/Session1` shows the worksheet with every screenshot, and `git status` says **up to date**
