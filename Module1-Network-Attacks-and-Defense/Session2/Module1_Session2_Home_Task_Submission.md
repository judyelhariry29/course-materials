# Module 1 · Session 2 — Home Task Submission

## The Python Networking Stack

### Professional Training in Cybersecurity I

**Student Name:**

**Date:**

---

> [!note] How to use this submission
> This single file is your **graded artifact** for the home task.
> Work through the Home Task and paste your final code, terminal output, values and written answers into the slots below, in task order.
> **Every section is required.**
> There are no optional tasks, and every script must run without errors.
>
> **Paste inside each box, never over its first or last line.**
>
> **Every value comes from your own run.**
> Record lengths, identification fields and addresses differ from machine to machine, and a value that your pasted output does not show earns nothing.
>
> **Screenshots are evidence you ran the work yourself.**
> A pasted output can be copied, but a screenshot of your own terminal cannot.
> Replace each screenshot slot with a real capture.
> - Use **Flameshot** for clean, annotated captures.
> - Keep them in a `screenshots/` folder beside this file, named for the task (for example `task1-sni-reader.png` or `task4-frame-echo.png`), and embed each with `![task1-sni-reader](screenshots/task1-sni-reader.png)` on its own line below its evidence callout, after a blank line.
>
> **Before you submit:** delete this note, then commit and push **this markdown file together with its `screenshots/` folder** to your submission repository.
> The markdown file is what is graded, so leave it as markdown.
> Exporting a PDF copy for yourself is optional and is not what you hand in.

---

# What Arrives on the Socket

---

## Task 1: Read the Server Name from a TLS First Flight — REQUIRED

> 🧩 **GUIDED:** paste your completed starter, with all its `# TODO`s filled in.

**Your completed code** (`sni_reader.py`, all TODOs filled in):

```python

```

**The reader's output, for the client run with `-servername peer.lab`:**

```
(paste output here)
```

**The reader's output, for the client run with `-noservername`:**

```
(paste output here)
```

> [!example] Evidence — screenshot
> *(paste a screenshot of both terminals from the `-servername peer.lab` run, the reader's output and the client's error, here — `task1-sni-reader.png`)*

**Your values** (questions 1a to 2c in the Home Task, in order, each read from your own run):

**1a —** _Answer:_

**1b —** _Answer:_

**1c —** _Answer:_

**2a —** _Answer:_

**2b —** _Answer:_

**2c —** _Answer:_

**Q1. The record version you found in 1b names an older TLS version than 1.3, although your OpenSSL client supports TLS 1.3.
Why does a TLS 1.3 client write an older version in its first record, and where in the ClientHello does it say which versions it really supports?**

```
(your answer here)
```

**Q2. Your reader read the record's body with `recv_exact(conn, record_length)` instead of one `conn.recv(record_length)`.
Why could one `recv` return less than the whole ClientHello, and what does the size you found in 1c have to do with it?**

```
(your answer here)
```

**Q3. Everything after the handshake will be encrypted, but your reader got the name without any key.
What does a party on the path learn from the first flight alone, and why can the client not simply encrypt the `server_name` extension in the ClientHello as TLS normally works?**

```
(your answer here)
```

---

## Task 2: Detect a Datagram That Was Cut Short — REQUIRED

> 🔨 **FROM SCRATCH**

**Your code** (`trunc_detector.py`):

```python

```

**Your `trunc_detector.py` output** (one line per datagram, then the count):

```
(paste output here)
```

> [!example] Evidence — screenshot
> *(paste a screenshot of both terminals, the detector's report and the sending command, here — `task2-trunc-detector.png`)*

**Q1. The 64-byte and the 65-byte datagrams both gave you exactly 64 bytes of data, and only one of them was truncated.
Why can a receiver not tell them apart from the data it got, and what does the kernel know that the buffer does not?**

```
(your answer here)
```

**Q2. A service that logs or inspects UDP messages through a small fixed buffer acts on whatever arrived.
What goes wrong without any error when a message is longer than that buffer, and what should a careful receiver do when `MSG_TRUNC` is set?**

```
(your answer here)
```

---

# Headers the Program Writes

---

## Task 3: Write the IPv4 Header with IP_HDRINCL — REQUIRED

> 🧩 **GUIDED:** paste your completed starter, with all its `# TODO`s filled in.

**Your completed code** (`hdrincl_echo.py`, all TODOs filled in):

```python

```

**Your run with `sudo`, with what it printed:**

```bash
(paste command and output here)
```

> [!example] Evidence — screenshot
> *(paste a screenshot of the `sudo` run, the written header and the reply's header visible, here — `task3-hdrincl.png`)*

**Your values** (questions 3a to 3d in the Home Task, in order, each read from your own run):

**3a —** _Answer:_

**3b —** _Answer:_

**3c —** _Answer:_

**3d —** _Answer:_

**Q1. The header your program wrote held `0` in its total length and checksum, and the server still answered.
What does the reply tell you Linux did to your header before it left, and what would the server have done with the header exactly as you wrote it?**

```
(your answer here)
```

**Q2. The reply went to the destination address you found in 3d, the source address your header named, and your tool asked the kernel for that address instead of accepting one on the command line.
Where would a reply go if a header named an address its sender does not hold, and why does that make a packet's source address weak evidence of who sent it?**

```
(your answer here)
```

---

## Task 4: Send a Complete Ethernet Frame with AF_PACKET — REQUIRED

> 🔨 **FROM SCRATCH**

**Your code** (`frame_echo.py`):

```python

```

**Your `ip neigh show` line for the peer, with its command:**

```bash
(paste command and output here)
```

**Your run without `sudo`, with what it printed:**

```bash
(paste command and output here)
```

**Your run with `sudo`, with what it printed:**

```bash
(paste command and output here)
```

> [!example] Evidence — screenshot
> *(paste a screenshot of the `sudo` run, the reply's MAC address and checksum verdict visible, here — `task4-frame-echo.png`)*

**Your values** (questions 4a and 4b in the Home Task, in order, each read from your own run):

**4a —** _Answer:_

**4b —** _Answer:_

**Q1. The reply frame (4b) was longer than the IPv4 packet inside it.
Where do the extra bytes come from, and why did your program cut the data at the IPv4 total length instead of at the end of the frame?**

```
(your answer here)
```

**Q2. In Task 3 Linux filled the total length and checksum, and in this task your program had to compute them.
What happens to a frame whose IPv4 checksum is wrong when it reaches the server, and why does a packet socket leave that work to the program?**

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

One line, **required either way**: `None`, or the AI assistant you used and what you used it for, for example *"to explain the `IndexError` my reader printed"*.
Using one for learning, explanation or debugging is allowed.
Not disclosing it is an integrity violation.

```
(None, or: which assistant, and what for)
```
