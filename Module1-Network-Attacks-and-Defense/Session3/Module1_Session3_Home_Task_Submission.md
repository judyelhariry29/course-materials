# Module 1 · Session 3 — Home Task Submission

## Scapy and Raw Packet Crafting

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
> A value that your pasted output does not show earns nothing.
>
> **Screenshots are evidence you ran the work yourself.**
> A pasted output can be copied, but a screenshot of your own terminal cannot.
> Replace each screenshot slot with a real capture.
> - Use **Flameshot** for clean, annotated captures.
> - Keep them in the `screenshots/` folder beside this file, named for the task (for example `task1-inspect.png` or `task4-count-filter.png`), and embed each with `![task1-inspect](screenshots/task1-inspect.png)` on its own line below its evidence callout, after a blank line.
>
> **Before you submit:** delete this note, then commit and push **this markdown file together with its `screenshots/` folder** to your submission repository.
> The markdown file is what is graded, so leave it as markdown.
> Exporting a PDF copy for yourself is optional and is not what you hand in.

---

# Reading a Packet Without Sending It

---

## Task 1: Read One Datagram Before and After Its Build — REQUIRED

> 🧩 **GUIDED:** paste your completed starter, with all its `# TODO`s filled in.

**Your completed code** (`inspect_datagram.py`, all TODOs filled in):

```python

```

**Your run of `python3 inspect_datagram.py`, with what it printed:**

```bash
(paste command and output here)
```

> [!example] Evidence — screenshot
> *(paste a screenshot of the run, the `show2()` and `hexdump()` sections visible, here — `task1-inspect.png`)*

**Your values** (questions 1a to 2b in the Home Task's Task 1, in order, each read from your own run):

**1a —** _Answer:_

**1b —** _Answer:_

**1c —** _Answer:_

**2a —** _Answer:_

**2b —** _Answer:_

**Q1. Your `show()` section and your `show2()` section printed the same datagram, and three of its fields read differently in the two.
What does `show2()` do that `show()` does not, and why can those three fields hold no value before then?**

```
(your answer here)
```

**Q2. A tool prints `show()` of a packet it is about to send, and a tester reads the packet's checksum from that printout.
Why is the tester reading the wrong view, and which view or output shows what actually leaves the machine?**

```
(your answer here)
```

---

## Task 2: Report Where Dissection Stops — REQUIRED

> 🔨 **FROM SCRATCH**

**Your code** (`where_stops.py`):

```python

```

**Your run of `where_stops.py` on the three frames, with what it printed:**

```bash
(paste command and output here)
```

> [!example] Evidence — screenshot
> *(paste a screenshot of the run, all three frames' lines visible, here — `task2-where-stops.png`)*

**Your values** (questions 1a to 2b in the Home Task's Task 2, in order, each read from your own run):

**1a —** _Answer:_

**1b —** _Answer:_

**2a —** _Answer:_

**2b —** _Answer:_

**Q1. For each of `frame_88b5.bin` and `frame_253.bin`, which field's value ended dissection?
Why did Scapy keep the bytes after that header as one `Raw` layer, instead of reading the headers those bytes still contain?**

```
(your answer here)
```

**Q2. The requirements forbid fixed offsets.
Why would a tool that always read the IPv4 protocol at byte 23 misreport `frame_88b5.bin`, and what should an analyst do next with a frame whose payload stays `Raw`?**

```
(your answer here)
```

---

# On the Lab Link

---

## Task 3: Run the Echo Exchange at Layer 2 With `srp1` — REQUIRED

> 🧩 **GUIDED:** paste your completed starter, with all its `# TODO`s filled in.

**Your completed code** (`l2_echo.py`, all TODOs filled in):

```python

```

**Your run with `sudo`, with what it printed:**

```bash
(paste command and output here)
```

> [!example] Evidence — screenshot
> *(paste a screenshot of the `sudo` run, both replies visible, here — `task3-l2-echo.png`)*

**Your values** (questions 1a to 2a in the Home Task's Task 3, in order, each read from your own run):

**1a —** _Answer:_

**1b —** _Answer:_

**2a —** _Answer:_

**Q1. `srp1` and `sr1` sent the same echo request and got a reply to it from the same target, but returned that reply in different forms.
Explain the difference from what each call takes and what it returns, and name the test that `srp1`'s match runs and `sr1`'s does not.**

```
(your answer here)
```

**Q2. Your frame named the target's MAC address itself, so Scapy ran no MAC lookup before it sent.
When does a tool need to write the Ethernet header itself, and what can a sender on the same link claim in that header that the receiver has no way to check?**

```
(your answer here)
```

---

## Task 4: Count the Packets a Kernel Filter Keeps From Python — REQUIRED

> 🔨 **FROM SCRATCH**

**Your code** (`count_filter.py`):

```python

```

**Your capture in mode `filter`, with its command and what it printed:**

```bash
(paste command and output here)
```

**Your capture in mode `lfilter`, with its command and what it printed:**

```bash
(paste command and output here)
```

**The sender in the second terminal, with its command and the line it printed:**

```bash
(paste command and output here)
```

> [!example] Evidence — screenshot
> *(paste a screenshot of both terminals from the `lfilter` run, the capture and the sender, here — `task4-count-filter.png`)*

**Your values** (question 1a in the Home Task's Task 4, read from your own run):

**1a —** _Answer:_

**Q1. Both captures kept the same two packets, yet more packets reached Python in one mode than in the other.
Which packets reached Python only in mode `lfilter`, and why did `filter="icmp"` drop them before Python saw them?**

```
(your answer here)
```

**Q2. A defender leaves a capture running for hours on a busy link, to record one kind of traffic.
Why should its test go in `filter` rather than in `lfilter`, and what can an `lfilter` test that a BPF filter cannot?**

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

One line, **required either way**: `None`, or the AI assistant you used and what you used it for, for example *"to explain why my capture never returned"*.
Using one for learning, explanation or debugging is allowed.
Not disclosing it is an integrity violation.

```
(None, or: which assistant, and what for)
```
