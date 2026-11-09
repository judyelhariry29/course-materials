# Module 1 · Session 2 — Practical Guide Submission

## The Python Networking Stack

### Professional Training in Cybersecurity I

**Student Name:**

**Date:**

---

> [!note] How to use this submission
> This single file is your **graded artifact**.
> Work through the Practical Guide and paste your final code, terminal output, and written answers into the slots below: one block per exercise, in guide order, then the CTF challenge.
> Delete any **OPTIONAL** section you did not attempt.
> Setup has no slots of its own: everything it builds is used, and so proven, by the exercises.
>
> **Paste inside each box, never over its first or last line.**
>
> **Screenshots are evidence you ran the work yourself.**
> A pasted output can be copied, but a screenshot of your own terminal cannot.
> Wherever you see a screenshot slot, replace it with a real capture.
> - Use **Flameshot** for clean, annotated captures.
> - Keep them in a `screenshots/` folder beside this file, named for the exercise (for example `ex1-tcp-connection.png` or `ctf1-flag.png`), and embed each with `![ex1-tcp-connection](screenshots/ex1-tcp-connection.png)` on its own line below its evidence callout, after a blank line.
>
> **Before you submit:** delete this note, then commit and push **this markdown file together with its `screenshots/` folder** to your submission repository.
> The markdown file is what is graded, so leave it as markdown.
> Exporting a PDF copy for yourself is optional and is not what you hand in.

---

# Required Exercises

---

## Exercise 1: A TCP Server and Client on Two Machines — REQUIRED

> 🧩 **GUIDED:** paste your completed starters, with all their `# TODO`s filled in.

**Your completed server** (`tcp_server.py`, all TODOs filled in):

```python

```

**Your completed client** (`tcp_client.py`, all TODOs filled in):

```python

```

**Your run of `ip -br -4 addr` on Kali, with what it printed:**

```bash
(paste command and output here)
```

**Your run of `ssh lab ip -br -4 addr`, with what it printed:**

```bash
(paste command and output here)
```

**What the server printed on the peer**, from `listening on` to `the client closed the connection`:

```
(paste output here)
```

**Your run of `python3 tcp_client.py`, with what it printed:**

```bash
(paste command and output here)
```

**Your two `ss` runs while the connection was open, with what they printed:**

```bash
(paste command and output here)
```

```bash
(paste command and output here)
```

**The loopback run: the client's run, with what it printed:**

```bash
(paste command and output here)
```

**The peer's `ss -tln`, with what it printed:**

```bash
(paste command and output here)
```

> [!example] Evidence — screenshot
> *(paste a screenshot of the open connection here: the client waiting, and both `ss` lines in the other terminal — `ex1-tcp-connection.png`)*

**Your answers** (questions 1a–3b in the guide, in order):

**1a —** _Answer:_

**1b —** _Answer:_

**2a —** _Answer:_

**2b —** _Answer:_

**3a —** _Answer:_

**3b —** _Answer:_

**Q1. `accept` returned a new socket with a descriptor of its own, while the listener kept its own descriptor.
Why does a TCP server need the two sockets, and what is the listener still for after `accept` returns?**

```
(your answer here)
```

**Q2. Bound to `127.0.0.1`, the server was running, and yet Kali's connection was refused.
Why, and what would binding the server to `0.0.0.0` make reachable instead?**

```
(your answer here)
```

---

## Exercise 2: Restoring Message Boundaries with a Length Prefix — REQUIRED

> 🧩 **GUIDED:** paste your completed starter, with all its `# TODO`s filled in.

**Your completed code** (`framed_client.py`, all TODOs filled in):

```python

```

**Your run of `python3 naive_client.py`, with what it printed:**

```bash
(paste command and output here)
```

**Your run of `python3 framed_client.py`, with what it printed:**

```bash
(paste command and output here)
```

**What the server printed on the peer:**

```
(paste output here)
```

> [!example] Evidence — screenshot
> *(paste a screenshot of both clients' runs here — `ex2-framed-client.png`)*

**Your answers** (questions 1a–2c in the guide, in order):

**1a —** _Answer:_

**1b —** _Answer:_

**2a —** _Answer:_

**2b —** _Answer:_

**2c —** _Answer:_

**Q1. One `recv(4)` can return fewer than 4 bytes on a healthy connection.
Why, and what would `recv_exact` do on a closed connection if it had no check for `b''`?**

```
(your answer here)
```

**Q2. Suppose a sender wrote the prefix as `len(text)`, the number of characters, instead of the number of encoded bytes.
What would a receiver like yours read for `café`, and what would happen to every message after it?**

```
(your answer here)
```

---

## Exercise 3: Refused, Timed Out or Open: One Connection Attempt — REQUIRED

> 🧩 **GUIDED:** paste your completed starter, with all its `# TODO`s filled in.

**Your completed code** (`probe.py`, all TODOs filled in):

```python

```

**Your run of `sudo iptables -L INPUT -n` with the rule in place, with what it printed:**

```bash
(paste command and output here)
```

**Your three probes, with what they printed:**

```bash
(paste command and output here)
```

**Your run of `sudo iptables -L INPUT -n` after removing the rule, with what it printed:**

```bash
(paste command and output here)
```

**Your probe of 8084 after removing the rule, with what it printed:**

```bash
(paste command and output here)
```

> [!example] Evidence — screenshot
> *(paste a screenshot of the three probes here — `ex3-probes.png`)*

**Your answers** (questions 1a–2a in the guide, in order):

**1a —** _Answer:_

**1b —** _Answer:_

**1c —** _Answer:_

**1d —** _Answer:_

**1e —** _Answer:_

**1f —** _Answer:_

**2a —** _Answer:_

**Q1. Compare how long the closed port and the dropped port took to fail.
What came back from each port, and what did the client wait for on 8084?**

```
(your answer here)
```

**Q2. `ConnectionRefusedError` and `TimeoutError` are both subclasses of `OSError`.
What would `probe.py` report for ports 8083 and 8084 if their two handlers were moved below `except OSError`, and why?**

```
(your answer here)
```

**Q3. A tool reports that a port timed out.
Give two different reasons the target could have sent nothing back, and explain why the tool cannot tell them apart.**

```
(your answer here)
```

---

## Exercise 4: Wrapping the Client in TLS — REQUIRED

> 🧩 **GUIDED:** paste your completed starter, with all its `# TODO`s filled in.

**Your completed code** (`tls_client.py`, all TODOs filled in):

```python

```

**Your run of `openssl x509` on `peer.crt`, with what it printed:**

```bash
(paste command and output here)
```

**Your run with `peer.lab` and `peer.crt`, with what it printed:**

```bash
(paste command and output here)
```

**Your run without a CA file, with what it printed:**

```bash
(paste command and output here)
```

**Your run with `other.lab`, with what it printed:**

```bash
(paste command and output here)
```

**What the server printed on the peer:**

```
(paste output here)
```

> [!example] Evidence — screenshot
> *(paste a screenshot of the three client runs here — `ex4-tls-client.png`)*

**Your answers** (questions 1a–1b in the guide, in order):

**1a —** _Answer:_

**1b —** _Answer:_

**Q1. The client was given `peer.crt` and never `peer.key`.
What does the client do with the certificate, and why should the private key never leave the server?**

```
(your answer here)
```

**Q2. Your first failing run broke the trust check, and your second broke the name check.
For each check, describe an attacker on the path whom that check stops.**

```
(your answer here)
```

---

## Exercise 5: One Thread per Client, and the Lock It Needs — REQUIRED

> 🧩 **GUIDED:** paste your completed starters, with all their `# TODO`s filled in.

**Your completed threaded server** (`threaded_server.py`, all TODOs filled in):

```python

```

**Your completed `lost_update.py`** (all TODOs filled in):

```python

```

**Your run of `three_clients.py` against the serial server, with what it printed:**

```bash
(paste command and output here)
```

**Your run of `three_clients.py` against your threaded server, with what it printed:**

```bash
(paste command and output here)
```

**Your three runs of `lost_update.py` before adding the lock, with what they printed:**

```bash
(paste command and output here)
```

**Your three runs of `lost_update.py` with the lock, with what they printed:**

```bash
(paste command and output here)
```

> [!example] Evidence — screenshot
> *(paste a screenshot of the two `three_clients.py` runs here — `ex5-three-clients.png`)*

**Your answers** (questions 1a–2c in the guide, in order):

**1a —** _Answer:_

**1b —** _Answer:_

**2a —** _Answer:_

**2b —** _Answer:_

**2c —** _Answer:_

**Q1. Each request needs one second of work.
Why did the serial server's slowest client wait as long as it did, and what changed in your threaded server to shorten that wait?**

```
(your answer here)
```

**Q2. Why did the count differ on every run without the lock, and why does one run that happens to reach 800,000 prove nothing about the code?**

```
(your answer here)
```

---

# Choice Exercises — you completed at least one of 6–8

---

## Exercise 6: Datagrams Keep Their Boundaries

> [!important] OPTIONAL: delete this whole section if you did not attempt it

> ✍️ **FROM SCRATCH:** paste your own code.

**Your receiver** (`udp_receiver.py`):

```python

```

**Your sender** (`udp_sender.py`):

```python

```

**What the receiver printed on the peer:**

```
(paste output here)
```

**Your run of `python3 udp_sender.py`, with what it printed:**

```bash
(paste command and output here)
```

> [!example] Evidence — screenshot
> *(paste a screenshot of the receiver's output here — `ex6-datagrams.png`)*

**Your answers** (questions 1a–1b in the guide, in order):

**1a —** _Answer:_

**1b —** _Answer:_

**Q1. Five `sendto` calls arrived as five separate `recvfrom` results.
Why does a datagram socket keep these boundaries, when Exercise 2's stream did not?**

```
(your answer here)
```

**Q2. `recvfrom(4)` returned four bytes, and the next call returned the next datagram.
What happened to the other six bytes, and what does that mean for the buffer size a UDP receiver passes to `recvfrom`?**

```
(your answer here)
```

---

## Exercise 7: A Restart That Cannot Bind

> [!important] OPTIONAL: delete this whole section if you did not attempt it

> ✍️ **FROM SCRATCH:** paste your own code.

**Your server** (`restart_server.py`):

```python

```

**Your `nc` run, with what it printed:**

```bash
(paste command and output here)
```

**The `ss` line on the peer, with what it printed:**

```bash
(paste command and output here)
```

**The restart without `reuse`, with what it printed:**

```bash
(paste command and output here)
```

**The restart with `reuse`, with what it printed:**

```bash
(paste command and output here)
```

**The test with `reuse` on every run, with what it printed:**

```bash
(paste command and output here)
```

> [!example] Evidence — screenshot
> *(paste a screenshot of the `ss` line and the two restarts here — `ex7-restart.png`)*

**Your answers** (questions 1a–2a in the guide, in order):

**1a —** _Answer:_

**2a —** _Answer:_

**Q1. The server had exited, and yet its port was still in use.
Why does the side that closes first keep the connection in `TIME_WAIT`, and which side was that here?**

```
(your answer here)
```

**Q2. Setting `reuse` on the restart alone still failed.
Why must every run of a server set `SO_REUSEADDR`, the first one included?**

```
(your answer here)
```

---

## Exercise 8: One Selector Loop Serves Many Clients

> [!important] OPTIONAL: delete this whole section if you did not attempt it

> ✍️ **FROM SCRATCH:** paste your own code.

**Your server** (`selector_server.py`):

```python

```

**What your server printed when it started:**

```
(paste output here)
```

**Your run of `three_clients.py` against your server, with what it printed:**

```bash
(paste command and output here)
```

**The `--stall` run against `serial_server.py`, with what it printed:**

```bash
(paste command and output here)
```

**The `--stall` run against your server, with what it printed:**

```bash
(paste command and output here)
```

> [!example] Evidence — screenshot
> *(paste a screenshot of the two `--stall` runs here — `ex8-selector.png`)*

**Your answers** (questions 1a–1b in the guide, in order):

**1a —** _Answer:_

**1b —** _Answer:_

**Q1. With one stalled client connected, explain what the serial server did for the other three.
Which call was it blocked in, and on which client's socket?**

```
(your answer here)
```

**Q2. Compare your server's answers to the three clients while the stalled client stayed connected.
How does `select()` let one thread serve them?**

```
(your answer here)
```

---

# Required Capstone

---

## Exercise 9: An ICMP Echo Request over a Raw Socket — REQUIRED

> 🧩 **GUIDED:** paste your completed starter, with all its `# TODO`s filled in.

**Your completed code** (`icmp_echo.py`, all TODOs filled in):

```python

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
> *(paste a screenshot of the `sudo` run here — `ex9-icmp-echo.png`)*

**Your answers** (questions 1a–2b in the guide, in order):

**1a —** _Answer:_

**2a —** _Answer:_

**2b —** _Answer:_

**Q1. The reply is longer than the request you sent.
Where do the extra bytes come from, and why does the program read IHL instead of slicing the reply at a fixed offset?**

```
(your answer here)
```

**Q2. The run without `sudo` failed at `socket()`, before anything was sent.
Why does Linux keep raw sockets behind `CAP_NET_RAW`, and why is granting that capability to the `python3` interpreter itself a poor way to avoid `sudo`?**

```
(your answer here)
```

---

# CTF Challenge — you solved Challenge 1

> [!note] Start the service first
> Run `ctf_service.py` from the guide in its own Kali terminal.
> That code is given, so do not paste it here.
> The solver below is your work.

---

## Challenge 1: A Stream That Arrives in Pieces — REQUIRED

> 🚩 **CTF**

**Your solver** (`solve1.py`):

```python

```

**Your run of `python3 solve1.py`, with what it printed:**

```bash
(paste command and output here)
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

# Anything that failed

If something did not work, describe it here: **the exact step, the exact message, and what you tried.**
It earns no points itself, but a failure described precisely keeps the marks for everything that works.
A failure you can describe is a two-minute fix.

```
(your answer here, or "nothing failed")
```

---

# AI Assistance

One line, **required either way**: `None`, or the AI assistant you used and what you used it for, for example *"to explain the `ConnectionRefusedError` my client printed"*.
Using one for learning, explanation or debugging is allowed.
Not disclosing it is an integrity violation.

```
(None, or: which assistant, and what for)
```
