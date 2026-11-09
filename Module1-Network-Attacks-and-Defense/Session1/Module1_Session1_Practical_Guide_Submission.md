# Module 1 · Session 1 — Practical Guide Submission

## Encapsulation, Forwarding and the Byte-Level Frame

### Professional Training in Cybersecurity I

**Student Name:**

**Date:**

---

> [!note] How to use this submission
> This single file is your **graded artifact**.
> Work through the Practical Guide and paste your final code, terminal output, and written answers into the slots below: one block per exercise, in guide order.
> Delete any **OPTIONAL** section you did not attempt.
>
> **Paste inside each box, never over its first or last line.**
>
> **Screenshots are evidence you ran the work yourself.**
> A pasted output can be copied, but a screenshot of your own terminal cannot.
> Wherever you see a screenshot slot, replace it with a real capture.
> - Use **Flameshot** for clean, annotated captures.
> - Keep them in a `screenshots/` folder beside this file, named for the exercise (for example `ex1-build-match.png` or `ctf1-flag.png`), and embed each with `![ex1-build-match](screenshots/ex1-build-match.png)` on its own line below its evidence callout, after a blank line.
>
> **Before you submit:** delete this note, then commit and push **this markdown file together with its `screenshots/` folder** to your submission repository.
> The markdown file is what is graded, so leave it as markdown.
> Exporting a PDF copy for yourself is optional and is not what you hand in.

---

# Warm-Up: Reading the Bytes Before Parsing Them — REQUIRED

**Your `hexdump -C warmup_frame.bin` output:**

```
(paste hexdump -C warmup_frame.bin output here)
```

> [!example] Evidence — screenshot
> *(paste a screenshot of your terminal showing the hexdump here — `warmup-hexdump.png`)*

**Your answers** (warm-up questions 1a–6b in the guide, in order):

**1a —** _Answer:_

**1b —** _Answer:_

**2a —** _Answer:_

**2b —** _Answer:_

**3a —** _Answer:_

**3b —** _Answer:_

**4a —** _Answer:_

**4b —** _Answer:_

**4c —** _Answer:_

**5a —** _Answer:_

**5b —** _Answer:_

**5c —** _Answer:_

**6a —** _Answer:_

**6b —** _Answer:_

---

# Required Exercises

---

## Exercise 1: Build the Frame From the Inside Out — REQUIRED

> 🧩 **GUIDED:** paste your completed starter, with all its `# TODO`s filled in.

**Your completed code** (`build_frame.py`, all TODOs filled in):

```python

```

**Your `build_frame.py` output** (the `[*] built …` and `[+] MATCH …` lines):

```
(paste the build_frame.py run here)
```

**Your `cmp` check:**

```
(paste: cmp built_frame.bin ref_frame.bin && echo "IDENTICAL")
```

**Your `hexdump -C built_frame.bin`:**

```
(paste the hexdump of your built frame here)
```

> [!example] Evidence — screenshot
> *(one screenshot of the run showing the MATCH and IDENTICAL lines covers all three blocks above — `ex1-build-match.png`)*

**Q1. You built the frame with plain concatenation, `eth + ip + tcp + PAYLOAD`, with no offsets written anywhere.
Why does that land every field at the correct byte offset on the wire?**

```
(your answer here)
```

**Q2. IPv4's first byte is `0x45`, which you assembled as `(4 << 4) | 5` rather than packing two separate `struct` fields.
Why does that byte have to be built by hand?**

```
(your answer here)
```

**Q3. Suppose your format string `'!HHLLBBHHH'` were missing a letter.
Would the frame come out with a wrong value or a wrong length, and how would the script show it?**

```
(your answer here)
```

---

## Exercise 2: Parse the Frame From the Outside In — REQUIRED

> 🧩 **GUIDED:** paste your completed starter, with all its `# TODO`s filled in.

**Your completed code** (`parse_frame.py`, all TODOs filled in):

```python

```

**Your output for the 59-byte frame** (`python3 parse_frame.py`):

```
(paste the parse of ref_frame.bin here)
```

**Your output for the 60-byte capture** (`python3 parse_frame.py ref_frame_padded.bin`):

```
(paste the parse of ref_frame_padded.bin: it must still report b'hello', and flag the padding byte)
```

> [!example] Evidence — screenshot
> *(paste a screenshot of both parses, with the padding byte flagged in the second, here — `ex2-parse.png`)*

**Q1. Your parser reaches each layer by following a next-layer pointer.
Name the value each of the three pointers (EtherType, protocol, destination port) carried in this frame, and what each one pointed to.**

```
(your answer here)
```

**Q2. The payload's end is computed as `14 + total_length` from the IP header, not `len(frame)`.
For the padded 60-byte capture, why is `len(frame)` the wrong end?**

```
(your answer here)
```

**Q3. Your parser reads the TCP header's length from the high nibble of one byte, the same trick it used for IHL.
Which byte is that, and why can't the parser just assume the TCP header is 20 bytes long?**

```
(your answer here)
```

---

# Choice Exercises — you completed at least two of 3–7

---

## Exercise 3: Compute the IPv4 Checksum by Hand

> [!important] OPTIONAL: delete this whole section if you did not attempt it

> 🔨 **FROM SCRATCH**

**Your code** (`ip_checksum.py`):

```python

```

**Your output** (all four values: the zeroed-field sum, the computed checksum, the receiver's `0xffff → 0x0000`, and the recomputed checksum after TTL 63):

```
(paste the ip_checksum.py output here)
```

> [!example] Evidence — screenshot
> *(paste a screenshot of your run showing all four values here — `ex3-checksum.png`)*

**Q1. The receiver's check sums the whole header *including* the checksum field and expects `0x0000`.
Why does a valid header sum to `0xffff`, whose complement is `0x0000`?**

```
(your answer here)
```

**Q2. The one's-complement sum folds the carry out of bit 16 back into the low bits (`total = (total & 0xffff) + (total >> 16)`).
What goes wrong if you drop that carry instead of folding it back?**

```
(your answer here)
```

**Q3. After lowering the TTL you recomputed the checksum in three lines, and it verified perfectly.
What does a passing checksum tell you about the header, and what does it NOT tell you?**

```
(your answer here)
```

---

## Exercise 4: Find and Fix the Endianness Bugs

> [!important] OPTIONAL: delete this whole section if you did not attempt it

> 🧩 **GUIDED:** paste your completed starter, with all its `# TODO`s filled in.

**Your completed code** (`endian_fix.py`, all TODOs filled in):

```python

```

**Your output** (the field table, every row a different pair except one):

```
(paste the endian_fix.py table here)
```

> [!example] Evidence — screenshot
> *(paste a screenshot of your table here — `ex4-endian.png`)*

**Q1. Every field reads differently between the two columns except `TCP window` (`ff ff`).
Why is that one field the same whichever end you read from?**

```
(your answer here)
```

**Q2. As given, the starter crashes on the sequence-number row with `unpack requires a buffer of 8 bytes`.
Why does *no prefix at all* make `struct` expect 8 bytes for an `L`, and what two jobs does the `!` prefix therefore do?**

```
(your answer here)
```

**Q3. A port that reads `20675` instead of `50000` is still a plausible port number.
Why does producing *believable* wrong values make this bug harder to catch than one that produces obvious garbage?**

```
(your answer here)
```

---

## Exercise 5: Where the Payload Stops

> [!important] OPTIONAL: delete this whole section if you did not attempt it

> 🔨 **FROM SCRATCH**

**Your code** (`payload_bounds.py`):

```python

```

**Your output for `ref_frame.bin`** (nothing trailing):

```
(paste: python3 payload_bounds.py ref_frame.bin)
```

**Your output for `ref_frame_padded.bin`** (one byte of padding):

```
(paste: python3 payload_bounds.py ref_frame_padded.bin)
```

> [!example] Evidence — screenshot
> *(one screenshot of both runs side by side — `ex5-payload-bounds.png`)*

**Q1. Why is the payload's *start* `14 + IHL*4 + data_offset*4` rather than a fixed `54`?**

```
(your answer here)
```

**Q2. For the padded file you printed `frame[54:59] = b'hello'` against `frame[54:] = b'hello\x00'`.
Which one is the real payload, and which header field told you where it ended?**

```
(your answer here)
```

**Q3. The guide calls `frame[54:]` the most common wrong answer in this session.
Name the two independent assumptions baked into the number `54`, and give a frame where each one would be wrong.**

```
(your answer here)
```

---

## Exercise 6: Write a Hexdump From Scratch

> [!important] OPTIONAL: delete this whole section if you did not attempt it

> 🔨 **FROM SCRATCH**

**Your code** (`my_hexdump.py`):

```python

```

**Your diff for `ref_frame.bin`** (it must produce `IDENTICAL`):

```
(paste: diff <(python3 my_hexdump.py ref_frame.bin) <(hexdump -C ref_frame.bin) && echo "IDENTICAL")
```

**Your diff for `ref_frame_padded.bin`** (it must produce `IDENTICAL`):

```
(paste: diff <(python3 my_hexdump.py ref_frame_padded.bin) <(hexdump -C ref_frame_padded.bin) && echo "IDENTICAL")
```

> [!example] Evidence — screenshot
> *(paste a screenshot of your dump beside the real one, with the `IDENTICAL` result — `ex6-hexdump-diff.png`)*

**Q1. The test is a byte-for-byte `diff` against `hexdump -C`.
Name the three alignment details that most commonly break that diff.**

```
(your answer here)
```

**Q2. How does the `*` line work: when does `hexdump` collapse lines, and what does it stand in for?**

```
(your answer here)
```

**Q3. Printable is defined as `0x20` to `0x7E`.
Why must a short final line pad its hex columns with spaces, and what misaligns if it doesn't?**

```
(your answer here)
```

---

## Exercise 7: The Same Frame, With UDP

> [!important] OPTIONAL: delete this whole section if you did not attempt it

> 🔨 **FROM SCRATCH**

**Your code** (`build_udp.py`):

```python

```

**Your `build_udp.py` output** (the frame's length and hex, and its fields parsed back):

```
(paste the build_udp.py output here)
```

**Your `hexdump -C udp_frame.bin`:**

```
(paste the hexdump of udp_frame.bin here)
```

**Your parser on it** (`python3 parse_frame.py udp_frame.bin`, which stops at protocol 17):

```
(paste the parse_frame.py udp_frame.bin output here)
```

> [!example] Evidence — screenshot
> *(paste a screenshot of the build and the parser stopping at protocol 17 — `ex7-udp.png`)*

**Q1. Swapping TCP for UDP changes exactly three things in the frame.
What are they?**

```
(your answer here)
```

**Q2. The UDP checksum covers a pseudo-header of IP fields plus the UDP header and payload, yet your Exercise 3 one's-complement routine worked on it unchanged.
What does that tell you about the checksum *algorithm* versus the *data* it is fed?**

```
(your answer here)
```

**Q3. Your Exercise 2 parser stopped at "protocol 17 is not one this parser reads yet."
Why is that correct behavior and not a bug?**

```
(your answer here)
```

---

# Required Capstone

---

## Exercise 8: Reading an Unfamiliar Header — REQUIRED

> 🔨 **FROM SCRATCH** | Difficulty: ⭐⭐⭐ Hard

**Your code** (`parse_arp.py`):

```python

```

**Your output** (the full parse of `arp_frame.bin`):

```
(paste the parse_arp.py output here)
```

**One sentence naming the protocol and how you identified it:**

```
(your answer here)
```

> [!example] Evidence — screenshot
> *(paste a screenshot of your parse_arp.py run here — `ex8-arp.png`)*

**Q1. You had never parsed this protocol.
Describe the method you used to get from an unknown EtherType to reading all nine fields correctly.**

```
(your answer here)
```

**Q2. One address field was entirely zero, and that is not padding or an error.
What does that blank field mean about what the frame is asking?**

```
(your answer here)
```

**Q3. This frame was broadcast to `ff:ff:ff:ff:ff:ff` and carries no authentication of any kind: any host on the link can answer it, truthfully or not.
What attack does that enable, and why can't the protocol itself prevent it?**

```
(your answer here)
```

---

# CTF Challenges — you completed Challenge 1 and one of 2/3

> [!note] Generate the captures first
> Run `ctf_setup.py` from the guide once, to write `chal1.bin`, `chal2.bin` and `chal3.bin` into your working folder.
> That code is given, so do not paste it here.
> The solvers below are your work.

---

## Challenge 1: Read the Length — REQUIRED

> 🚩 **CTF**

**Your solver** (`solve1.py`):

```python

```

**Recovered flag:**

```
FLAG{                              }
```

> [!example] Evidence — screenshot
> *(paste a screenshot of your solver run showing the flag here — `ctf1-flag.png`)*

**One-line approach:**

```
(your answer here)
```

---

## Challenge 2: Read a Multi-Byte Value Correctly

> [!important] OPTIONAL: delete this whole section if you did not attempt it

> 🚩 **CTF**

**Your solver** (`solve2.py`):

```python

```

**Both orderings** (the wire's reading and the other one):

```
(paste both orderings your solver printed here)
```

**Recovered flag:**

```
FLAG{                              }
```

> [!example] Evidence — screenshot
> *(paste a screenshot of your solver run showing the flag here — `ctf2-flag.png`)*

**One-line approach:**

```
(your answer here)
```

---

## Challenge 3: Follow the Chain

> [!important] OPTIONAL: delete this whole section if you did not attempt it

> 🚩 **CTF**

**Your solver** (`solve3.py`):

```python

```

**Your per-slot decisions** (which slots you skipped and why, which you took):

```
(paste your solver's per-slot log here — four slots skipped, four different reasons)
```

**Recovered flag:**

```
FLAG{                              }
```

> [!example] Evidence — screenshot
> *(paste a screenshot of your solver run showing the flag here — `ctf3-flag.png`)*

**One-line approach:**

```
(your answer here)
```

---

# Anything that failed

If something did not work, describe it here: **the exact step, the exact message, and what you tried.**
It earns no points itself, but a failure described precisely keeps the marks for everything that works.
A failure you can describe is a two-minute fix.

```
(your answer here, or "nothing failed")
```

---

# AI Assistance

One line, **required either way**: `None`, or the AI assistant you used and what you used it for, for example *"to explain the `struct.error` my build script printed"*.
Using one for learning, explanation or debugging is allowed.
Not disclosing it is an integrity violation.

```
(None, or: which assistant, and what for)
```
