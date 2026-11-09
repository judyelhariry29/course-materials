# Module 1 · Session 3 — Practical Guide Submission

## Scapy and Raw Packet Crafting

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
> - Keep them in a `screenshots/` folder beside this file, named for the exercise (for example `ex1-rebuild.png` or `ctf1-flag.png`), and embed each with `![ex1-rebuild](screenshots/ex1-rebuild.png)` on its own line below its evidence callout, after a blank line.
>
> **Before you submit:** delete this note, then commit and push **this markdown file together with its `screenshots/` folder** to your submission repository.
> The markdown file is what is graded, so leave it as markdown.
> Exporting a PDF copy for yourself is optional and is not what you hand in.

---

# Required Exercises

---

## Exercise 1: Rebuild the Reference Frame With Layer Objects — REQUIRED

> 🧩 **GUIDED:** paste your completed starter, with all its `# TODO`s filled in.

**Your completed code** (`rebuild_frame.py`, all TODOs filled in):

```python

```

**Your run of `ls -l` on your own `built_frame.bin`, with what it printed:**

```bash
(paste command and output here)
```

**Your run of `python3 rebuild_frame.py`, with what it printed:**

```bash
(paste command and output here)
```

> [!example] Evidence — screenshot
> *(paste a screenshot of the `rebuild_frame.py` run here, its five lines visible — `ex1-rebuild.png`)*

**Your answers** (questions 1a–2a in the guide, in order):

**1a —** _Answer:_

**1b —** _Answer:_

**1c —** _Answer:_

**2a —** _Answer:_

**Q1. `raw(scapy_packet)` equaled your own build byte for byte.
Explain what `built_packet == scapy_packet` printed: what does it compare between the two objects, and why is it the bytes, not the objects, that decide what a receiver gets?**

```
(your answer here)
```

**Q2. Suppose the data changes from `b"hello"` to `b"hello!"`, and nothing else does.
Which values would your hand build then get wrong, and what does Scapy's build do instead?**

```
(your answer here)
```

---

## Exercise 2: Dissect a Frame From Its Bytes — REQUIRED

> 🧩 **GUIDED:** paste your completed starter, with all its `# TODO`s filled in.

**Your completed code** (`dissect_frame.py`, all TODOs filled in):

```python

```

**Your run on `frame_a.bin`, with what it printed:**

```bash
(paste command and output here)
```

**Your run on `frame_b.bin`, with what it printed:**

```bash
(paste command and output here)
```

> [!example] Evidence — screenshot
> *(paste a screenshot of the two runs here — `ex2-dissect.png`)*

**Your answers** (questions 1a–2d in the guide, in order):

**1a —** _Answer:_

**1b —** _Answer:_

**1c —** _Answer:_

**2a —** _Answer:_

**2b —** _Answer:_

**2c —** _Answer:_

**2d —** _Answer:_

**Q1. Scapy's data for `frame_b.bin` is far shorter than everything after its UDP header.
Which field told Scapy where the IPv4 packet ends, and why would a reader that took every byte after the UDP header as data be wrong?**

```
(your answer here)
```

**Q2. Both frames carry a UDP header to port 7777.
Why did no Scapy class read the data after it, and what does a `Raw` layer in a capture tell someone analyzing it?**

```
(your answer here)
```

---

## Exercise 3: Probe the Target With `sr1` — REQUIRED

> 🧩 **GUIDED:** paste your completed starter, with all its `# TODO`s filled in.

**Your completed code** (`probe.py`, all TODOs filled in):

```python

```

**Your run without privilege, `python3 probe.py 10.10.3.10`, with what it printed:**

```bash
(paste command and output here)
```

**Your run under `sudo` against the target, with what it printed:**

```bash
(paste command and output here)
```

**Your run under `sudo` against `10.10.3.99`, with what it printed:**

```bash
(paste command and output here)
```

> [!example] Evidence — screenshot
> *(paste a screenshot of the two runs under `sudo` here — `ex3-probe.png`)*

**Your answers** (questions 1a–3a in the guide, in order):

**1a —** _Answer:_

**2a —** _Answer:_

**2b —** _Answer:_

**3a —** _Answer:_

**Q1. The probe to `10.10.3.99` set `timeout=2`, and yet it took longer than 2 seconds to return.
Where did the extra time go, and what does that cost a tool that probes many addresses no host holds?**

```
(your answer here)
```

**Q2. `answers()` tests a reply against a request.
Which fields of the reply does it compare with the request, and why can a tool not take the first ICMP packet that arrives as its answer?**

```
(your answer here)
```

---

## Exercise 4: Capture an Exchange and Save It as pcap — REQUIRED

> 🧩 **GUIDED:** paste your completed starter, with all its `# TODO`s filled in.

**Your completed code** (`capture_echo.py`, all TODOs filled in):

```python

```

**Your run of `capture_echo.py` under `sudo`, with what it printed:**

```bash
(paste command and output here)
```

**Your run of `sudo tcpdump -r echo3.pcap -nn`, with what it printed:**

```bash
(paste command and output here)
```

> [!example] Evidence — screenshot
> *(paste a screenshot of both runs here — `ex4-capture.png`)*

**Your answers** (questions 1a–2b in the guide, in order):

**1a —** _Answer:_

**1b —** _Answer:_

**1c —** _Answer:_

**2a —** _Answer:_

**2b —** _Answer:_

**Q1. Your program waits for `started_callback` before it sends.
What can go wrong without that wait, and why does it go wrong on some runs and not on others?**

```
(your answer here)
```

**Q2. `filter="icmp"` kept the echo packets and nothing else.
Where does that filter run, and why is that better than testing each packet in Python with `lfilter` on a busy link?**

```
(your answer here)
```

---

# Choice Exercises — you completed at least one of 5–7

---

## Exercise 5: `send` and `sendp`: The Same Bytes on the Wire

> [!important] OPTIONAL: delete this whole section if you did not attempt it

> 🔨 **FROM SCRATCH:** paste your own program.

**Your code** (`send_both.py`):

```python

```

**Your run of `send_both.py` under `sudo`, with what it printed:**

```bash
(paste command and output here)
```

> [!example] Evidence — screenshot
> *(paste a screenshot of the run here — `ex5-send-sendp.png`)*

**Your answers** (question 1a in the guide):

**1a —** _Answer:_

**Q1. Your program sent one packet with `send` and the same packet with `sendp`.
What did `send` do for you that your `sendp` call did by hand, and when does a tool need `sendp` instead?**

```
(your answer here)
```

---

## Exercise 6: Timeouts and Retries Against a Silent Address

> [!important] OPTIONAL: delete this whole section if you did not attempt it

> 🔨 **FROM SCRATCH:** paste your own program.

**Your code** (`retries.py`):

```python

```

**Your run of `retries.py` under `sudo`, with what it printed:**

```bash
(paste command and output here)
```

> [!example] Evidence — screenshot
> *(paste a screenshot of the run here — `ex6-retries.png`)*

**Your answers** (questions 1a–1c in the guide, in order):

**1a —** _Answer:_

**1b —** _Answer:_

**1c —** _Answer:_

**Q1. The call to `10.10.3.99` used `timeout=1` and `retry=2`.
Account for the time it took, round by round, and say why an answer list that stays empty is itself a result.**

```
(your answer here)
```

---

## Exercise 7: An Explicit Value Overrides the Binding

> [!important] OPTIONAL: delete this whole section if you did not attempt it

> 🔨 **FROM SCRATCH:** paste your own program.

**Your code** (`override.py`):

```python

```

**Your run of `python3 override.py`, with what it printed:**

```bash
(paste command and output here)
```

> [!example] Evidence — screenshot
> *(paste a screenshot of the run here — `ex7-override.png`)*

**Your answers** (questions 1a–1b in the guide, in order):

**1a —** _Answer:_

**1b —** _Answer:_

**Q1. The same TCP bytes were read back as another protocol under `nh=17`.
Why does every reader follow the next-header field, and what does that let an attacker do to a tool that trusts it?**

```
(your answer here)
```

---

# CTF Challenge — you solved Challenge 1

> [!note] The sender is given
> Run `ctf_service.py` from the guide in your second terminal while your solver captures.
> That code is given, so do not paste it here.
> The solver below is your work.

---

## Challenge 1: Rebuild the Message the Receiver Accepted — REQUIRED

> 🚩 **CTF**

**Your solver** (`solve1.py`):

```python

```

**Your run of `solve1.py` under `sudo`, with what it printed:**

```bash
(paste command and output here)
```

**Recovered flag:**

```
FLAG{                              }
```

> [!example] Evidence — screenshot
> *(paste a screenshot of the solver's run and the sender's run side by side here — `ctf1-flag.png`)*

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

One line, **required either way**: `None`, or the AI assistant you used and what you used it for, for example *"to explain the `PermissionError` my probe printed"*.
Using one for learning, explanation or debugging is allowed.
Not disclosing it is an integrity violation.

```
(None, or: which assistant, and what for)
```
