# Module 0 · Session 5 — Practical Guide

## Python Essentials for Cybersecurity

### Professional Training in Cybersecurity I

---

## Overview

This guide turns the Python you have just met into programs you wrote, ran and can explain.
Every exercise works on the material a defender handles every day: log lines, ports, addresses and binary files.
By the end you will have:

1. **A virtual environment of your own**, and proof of where `pip` installs a package
2. **A firewall log line taken apart** with slices, `int()` and format specs
3. **A day of firewall decisions counted** with a dictionary and a set
4. **A module of your own**, imported by a second script
5. **A log cleaned of its bad lines**, the good ones written to a new file
6. **A binary file decoded** byte by byte
7. **Two command-line tools**, one reading `sys.argv` and one built with `argparse`

**The guide runs in two sittings: the language first, then the tool.**
Exercises 1 to 3 practice the language itself: the environment, values and text, then decisions and collections.
Exercises 4 to 7 turn it into tools: functions and modules, files and errors, bytes, and the command line.
Each exercise practices one topic, and uses the topics before it only as tools.

> [!example] Submission
> Your worksheet is **`Module0_Session5_Practical_Guide_Submission.md`**.
> Each exercise below ends with a **Record** box naming what to paste: your code, what it printed, and one screenshot, with the filename to save it under.
>
> **The Submission also asks two or three short questions per exercise.**
> Answer them as you go, while the reason you wrote a line is still in front of you.

> [!important] You must complete
> All seven exercises, in order.
> Each one uses the folder, the environment and the sample files that the steps before it set up.

> [!note] Three kinds of exercise
> - **Hands-on:** the commands are given, and you run them and read what they print.
> - **Guided:** this guide gives you a **starter**, a file with numbered `# TODO` gaps.
>   You complete the gaps and keep the rest of the file as it is.
> - **From scratch:** this guide gives you requirements and the output your finished program must print, and the code is yours.

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
ls Module0-Foundation/Session5
```

**Checkpoint:** `ls` lists `Module0_Session5_Practical_Guide.md`, `Module0_Session5_Home_Task.md`, the two `_Submission.md` worksheets and `screenshots`.
In Obsidian, open the Practical Guide worksheet, then right-click **Module0_Session5_Practical_Guide.md** and choose **Open to the right**, so this guide sits beside it.

> [!important] Fill in the worksheets only
> Never edit, move or delete the guide or the Home Task in your repository.
> Your instructor's fixes arrive in them through `git pull`, and a changed copy stops that pull.

## Step 2: A working folder for your code

> [!note] Why the code lives outside your repository
> Your repository holds what you hand in: the worksheets and their screenshots.
> The scripts you write today, the sample files they read, and the virtual environment you build in Exercise 1 live in a folder of their own, `~/session5`.
> The environment alone is thousands of files that nobody grades, and keeping it out of your repository keeps every push small.
> Your code reaches your instructor by being pasted into the worksheet.

1. **Create the folder and open it in VS Code:**

   ```bash
   mkdir ~/session5
   code ~/session5
   ```

2. **Trust the folder.**
   The first time VS Code opens it, a window asks *Do you trust the authors of the files in this folder?*
   You made the folder yourself, so click **Yes, I trust the authors**.
3. **Open the built-in terminal** with **Terminal**, then **New Terminal**.
   Its prompt ends in `~/session5`.
   **Run every command in this guide in this terminal**, unless a step says otherwise.

> [!tip] How this guide shows a terminal
> Your prompt is two lines long and names your user and folder.
> The transcripts in this guide shorten it to `$`, with `(.venv)` in front of it once your virtual environment is active.

## Step 3: Lay down the sample files

Exercises 5 and 6 read three sample files.
A short script writes them, so every student starts from exactly the same bytes.

Each code block in this guide begins with a **tag line**, a comment that names the file to save the block as.
`@generator` marks a script that writes sample files, and `@starter` marks a starter for a guided exercise.
The tag is a comment, so Python ignores it: copy the whole block, tag included.

In VS Code, create a new file in `session5` named **`make_samples.py`**, paste this block into it, and save:

```python
# @generator make_samples.py
# @expect writes access.log (6 lines), addrs.bin (17 bytes) and bad.bin (9 bytes)
"""make_samples.py: write the sample files this session's exercises read"""

LOG = """09:14:03 10.0.0.23 3389
09:14:41 10.0.0.7 443
09:15:10 10.0.0.41 ssh
09:15:52 10.0.0.7 80
09:16:00 10.0.0.12
09:16:30 10.0.0.41 22
"""

with open("access.log", "w") as f:
    f.write(LOG)
with open("addrs.bin", "wb") as f:
    f.write(b"ADR1" + bytes([3, 10, 0, 0, 5, 10, 0, 0, 7, 192, 168, 1, 10]))
with open("bad.bin", "wb") as f:
    f.write(b"ADR2" + bytes([1, 10, 0, 0, 9]))
print("wrote access.log, addrs.bin and bad.bin")
```

Run it:

```bash
python3 make_samples.py
```

**Checkpoint:** it prints one line, and the three files appear beside it in VS Code's file list:

```
wrote access.log, addrs.bin and bad.bin
```

This script needs nothing but Python itself, so it runs before your virtual environment exists.
If you ever damage a sample file, run it again: it writes all three afresh.

---

# Exercises

---

| Exercise | Status | Type | Difficulty |
|----------|--------|------|------------|
| Exercise 1: Give a Project Its Own Python | **Required** | Hands-on | ⭐ Easy |
| Exercise 2: Take One Log Line Apart | **Required** | Guided (starter in guide) | ⭐ Easy |
| Exercise 3: Tally a Firewall's Day | **Required** | From Scratch | ⭐⭐ Medium |
| Exercise 4: Split a Script Into a Module | **Required** | Guided (starter in guide) | ⭐⭐ Medium |
| Exercise 5: Read a Log That Has Bad Lines | **Required** | From Scratch | ⭐⭐ Medium |
| Exercise 6: Decode a Binary Address File | **Required** | Guided (starter in guide) | ⭐⭐⭐ Hard |
| Exercise 7: Turn a Script Into a Command-Line Tool | **Required** | From Scratch | ⭐⭐ Medium |

Exercises 1 to 3 are the first sitting, and Exercises 4 to 7 the second.

**Commit after each exercise**, in your repository, with that exercise's number in the message:

```bash
cd ~/student-YOUR-USERNAME
git add Module0-Foundation/Session5
git commit -m "Module 0 Session 5: exercise 1"
```

---

# Required Exercises

---

## Exercise 1: Give a Project Its Own Python — REQUIRED

> **🔧 HANDS-ON: run the commands given, then write one two-line script** | Difficulty: ⭐ Easy

> [!note] One Python for Kali, one for your project
> Kali's own Python runs Kali's own tools, and many of them depend on the exact packages installed beside it.
> Changing those packages with `pip` can break a tool you never touched, so Kali refuses `pip install` outside an environment.
> A **virtual environment** is a folder holding its own `python3`, its own `pip` and its own place for packages, so a project installs what it needs without touching Kali's.
> **Activating** it puts the environment's `bin` folder first on `PATH`, the list of folders the shell searches for a command, so `python3` and `pip` now find the environment's copies first.
> The second half of this exercise makes a script run on its own, as a command.

1. **Create the environment and activate it**, in the built-in terminal:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

   `python3 -m venv .venv` creates the folder `.venv`, which appears in VS Code's file list.
   After `source`, your prompt starts with `(.venv)`.

   > [!tip] Every new terminal activates the environment for you
   > From now on, each terminal you open in this folder starts by typing `source /home/kali/session5/.venv/bin/activate` by itself: VS Code finds `.venv` and runs the same command you just typed.
   > The terminal you created `.venv` in is the one exception, which is why you activated it by hand.

2. **See what activation changed:**

   ```bash
   which python3
   echo $PATH
   ```

```
(.venv) $ which python3
/home/kali/session5/.venv/bin/python3
(.venv) $ echo $PATH
/home/kali/session5/.venv/bin:/home/kali/.local/bin:/usr/local/sbin:/usr/sbin:/sbin:/usr/local/bin:/usr/bin:/bin:/usr/local/games:/usr/games:/home/kali/.dotnet/tools
```

   `which` names the file the shell would run for a command.
   The first folder on `PATH` is now `.venv/bin`, so that is where the search stops.
   The folders after it may differ on your machine: the first one is what matters.

3. **Install a package into the environment:**

   ```bash
   pip install requests
   ```

   `requests` is a widely used library for talking to web servers.
   `pip` lists each package it collects, then ends with one line naming everything it installed.
   Your version numbers will be newer than these:

   ```
   Successfully installed certifi-2026.7.22 charset_normalizer-3.5.2 idna-3.20 requests-2.34.2 urllib3-2.8.0
   ```

4. **Ask where it went:**

   ```bash
   pip show requests
   ```

   ```
   (.venv) $ pip show requests
   Name: requests
   Version: 2.34.2
   Summary: Python HTTP for Humans.
   Home-page: 
   Author: 
   Author-email: Kenneth Reitz <me@kennethreitz.org>
   License: Apache-2.0
   Location: /home/kali/session5/.venv/lib/python3.13/site-packages
   Requires: certifi, charset_normalizer, idna, urllib3
   Required-by: 
   ```

   **The `Location:` line is the evidence:** the package sits inside `.venv`.

5. **Ask Kali's own Python the same question.**
   `deactivate` switches the environment off, and `python3 -m pip` runs the `pip` that belongs to whichever `python3` runs it, now Kali's:

   ```bash
   deactivate
   python3 -m pip show requests
   ```

   ```
   (.venv) $ deactivate
   $ python3 -m pip show requests
   Name: requests
   Version: 2.32.3
   Summary: Python HTTP for Humans.
   Home-page: https://requests.readthedocs.io
   Author: Kenneth Reitz
   Author-email: me@kennethreitz.org
   License: Apache-2.0
   Location: /usr/lib/python3/dist-packages
   Requires: certifi, charset_normalizer, idna, urllib3
   Required-by: censys, certipy-ad, dropbox, faraday-agent-dispatcher, faraday-plugins, faradaysec, netexec, pooch, pyExploitDb, pypsrp, requests-file, theHarvester, tldextract, wafw00f, websockify
   ```

   Kali has its own copy, in a different place.
   Read its `Required-by:` line: those are the Kali tools that need this exact copy.

   > [!warning] Never force `pip` onto Kali's own Python
   > Outside an environment, `pip install` stops with an `externally-managed-environment` error.
   > The error is right, and the fix is an environment, never `sudo pip` or the `--break-system-packages` option, which replace the copy the tools above depend on.

6. **Switch the environment back on**, because every exercise after this one runs inside it:

   ```bash
   source .venv/bin/activate
   ```

7. **Write a script that runs on its own.**
   Create **`hello.py`** in `session5` with exactly two lines:
   - line 1, the shebang: `#!/usr/bin/env python3`
   - line 2, a `print` of the sentence `This script runs on its own.`

8. **Run it with `python3`, then as a command:**

   ```bash
   python3 hello.py
   ./hello.py
   chmod +x hello.py
   ./hello.py
   ```

   ```
   (.venv) $ python3 hello.py
   This script runs on its own.
   (.venv) $ ./hello.py
   bash: ./hello.py: Permission denied
   (.venv) $ chmod +x hello.py
   (.venv) $ ./hello.py
   This script runs on its own.
   ```

   `./hello.py` asks the system to run the file itself, and a new file is not allowed to run until `chmod +x` gives it the **execute bit**.
   The shebang then tells the system which program reads the file.

**Checkpoint:** two different `Location:` lines, and `./hello.py` printing its sentence.

> [!example] Record
> The output of `which python3`, of `pip show requests` inside the environment, and of `python3 -m pip show requests` outside it, each in its own box.
> Your `hello.py`, and the four `hello.py` commands with what they printed.
> One screenshot of the terminal from `deactivate` down to Kali's `Location:` line (`ex1-venv.png`).
> Then answer the Exercise 1 questions in the Submission.

---

## Exercise 2: Take One Log Line Apart — REQUIRED

> **🧩 GUIDED: complete the starter below** | Difficulty: ⭐ Easy
> *Save the starter as `logline.py`, fill its three `# TODO` gaps, and run it until it prints what the run below shows.*

> [!note] A log line is text at agreed positions
> A firewall writes one line per decision: when, what it did, and between which two endpoints.
> This firewall writes **fixed-width** lines: each field starts at the same column on every line, padded with spaces to its full width.
> So a **slice** cuts any field out by its positions, `.strip()` removes the padding, and `int()` turns the digits of a port into a number you can compare and format.
> A **format spec** after a colon in an f-string shows the same number another way, such as `#06x` for hex with the `0x` prefix, six characters wide.
> A comparison such as `action == "DENY"` is itself a value, `True` or `False`.

The two comment lines above `LINE` are a **ruler**: read the bottom row for the units and the top row for the tens.
The character under the `0` of `10` is at index 10.

```python
# @starter logline.py
# logline.py: take one firewall log line apart
#                 1         2         3         4         5         6
#       012345678901234567890123456789012345678901234567890123456789012345678
LINE = "2026-10-05 09:14:03 DENY  10.0.0.23       51544 10.0.0.5         3389"

date = LINE[0:10]
time = LINE[11:19]
# TODO 1: cut out the other five fields the same way, reading the ruler above.
#   The action and the two hosts are padded with spaces: .strip() removes them.
#   The two ports are text until int() converts them.
action = ""
src_host = ""
src_port = 0
dst_host = ""
dst_port = 0

print(f"{date} at {time}: {action}")
print(f"from {src_host}:{src_port} to {dst_host}:{dst_port}")
# TODO 2: print the destination port in hex (six characters, with the 0x
#   prefix) and in binary (16 digits), one format spec each.
print("denied:", action == "DENY")

# TODO 3: ask for a port with input(), convert it, then print whether it is
#   a valid port (0 to 65535) and whether it matches the destination port.
```

**Run it** and type `3389` when it asks:

```bash
python3 logline.py
```

```
(.venv) $ python3 logline.py
2026-10-05 at 09:14:03: DENY
from 10.0.0.23:51544 to 10.0.0.5:3389
destination port in hex: 0x0d3d, in binary: 0000110100111101
denied: True
Port to check: 3389
valid port: True
matches the destination: True
```

**Then run it once more and type `rdp`**, followed by:

```bash
echo $?
```

The program stops with a **traceback**, Python's report of what went wrong and where.
Read its last line first: it names the exception and the value that caused it.
`echo $?` prints the **exit status** of the command before it, `0` for success and anything else for failure.

> [!example] Record
> Your completed `logline.py`.
> The run with `3389`, and the run with `rdp` together with `echo $?`, each in its own box.
> One screenshot of the `rdp` run and its traceback (`ex2-logline.png`).
> Then answer the Exercise 2 questions in the Submission.

---

## Exercise 3: Tally a Firewall's Day — REQUIRED

> **🔨 FROM SCRATCH** | Difficulty: ⭐⭐ Medium
> *Write `tally.py` yourself from the requirements, until its output matches the run shown.*

> [!note] Counting is a dictionary, uniqueness is a set
> A day of firewall decisions is a **list** of events, each a **tuple** of source host, port and action.
> Summarizing it asks two kinds of question.
> *How many of each?* is a **dictionary** of counts, one key per kind: `counts[key] = counts.get(key, 0) + 1` adds one, starting from 0 for a key not seen before.
> *How many different?* is a **set**, which keeps each member exactly once however often it is added.
> A log also holds impossible values, and a `for` loop skips them with an `if` and `continue` before they reach any count.

Start **`tally.py`** with these two constants, copied exactly:

```python
# tally.py: summarize one day of firewall decisions
EVENTS = [
    ("10.0.0.23", 3389, "DENY"),
    ("10.0.0.7", 443, "ALLOW"),
    ("10.0.0.7", 80, "ALLOW"),
    ("10.0.0.41", 22, "DENY"),
    ("10.0.0.23", 3389, "DENY"),
    ("10.0.0.9", 70000, "DENY"),
    ("10.0.0.12", 53, "ALLOW"),
    ("10.0.0.41", 22, "DENY"),
    ("10.0.0.7", 443, "ALLOW"),
    ("10.0.0.15", -1, "ALLOW"),
    ("10.0.0.23", 445, "DENY"),
]
SERVICES = {22: "ssh", 53: "dns", 80: "http", 443: "https", 3389: "rdp"}
```

**Requirements:**
- Loop over `EVENTS` once, unpacking each tuple into its three values.
- An event whose port is not from 0 to 65535 is counted as skipped and goes no further: use `continue`.
- Count the remaining events per action in a dictionary.
- Add each remaining event's source host to a set.
- Count the remaining **denied** events per port in a second dictionary.
- After the loop, print, in this order:
  - `Skipped <n> events with an impossible port`
  - one line per action, `<action> <count>`
  - `Unique sources: <n>`
  - `Denied by port:`, then one line per denied port, indented two spaces: `<port> (<service>): <count>`, the service taken from `SERVICES` and `unknown` for a port it does not list

**Your run must print exactly this:**

```
(.venv) $ python3 tally.py
Skipped 2 events with an impossible port
DENY 5
ALLOW 4
Unique sources: 4
Denied by port:
  3389 (rdp): 2
  22 (ssh): 2
  445 (unknown): 1
```

A dictionary keeps its keys in the order they were first added, so `DENY` comes before `ALLOW` because the first event is a denial.

> [!example] Record
> Your `tally.py` and its output.
> One screenshot of the run (`ex3-tally.png`).
> Then answer the Exercise 3 questions in the Submission.

---

> [!note] The first sitting ends here
> Commit Exercise 3, then push, so your work is on GitHub before you stop: *Hand In*, at the end of this guide, has the commands.
> To start the second sitting, run `code ~/session5` and open a new terminal.
> It activates `.venv` by itself, and the sample files from Setup are still there.

---

## Exercise 4: Split a Script Into a Module — REQUIRED

> **🧩 GUIDED: complete the two starters below** | Difficulty: ⭐⭐ Medium
> *Fill the three `# TODO` gaps in `endpoint.py` and the two in `check.py`, then run both until they print what the runs below show.*

> [!note] A function does one job, and a module shares it
> A **function** is a named block that takes **parameters** and hands back one value with `return`.
> To hand back two values it returns a **tuple**, which the caller unpacks: `host, port = parse_endpoint(text)`.
> A parameter with a **default value**, such as `label="unknown"`, may be left out of the call.
> A **module** is any `.py` file, and `import endpoint` runs `endpoint.py` once and gives its functions to the importing script as `endpoint.parse_endpoint` and so on.
> The **main guard**, `if __name__ == "__main__":`, runs `main()` only when the file is run directly, so a module can test itself without that test running on every import.

Each `# TODO` sits inside a function, so read the function's name, its parameters and its docstring before you fill it: they say what it receives and what it must return.

`endpoint.py`, the module:

```python
# @starter endpoint.py
"""endpoint.py: functions for host:port text"""

SERVICES = {22: "ssh", 53: "dns", 80: "http", 443: "https", 3389: "rdp"}


def parse_endpoint(text):
    """Split "host:port" into a (host, port) tuple, the port an int."""
    # TODO 1: split text at the colon and return the host and the port,
    #   the port converted to an int.
    return "", 0


def is_valid_port(port):
    """Return True when port is a number from 0 to 65535."""
    # TODO 2: return the result of one chained comparison.
    return False


def describe(host, port, label="unknown"):
    """Return one line naming the endpoint and its service."""
    # TODO 3: look port up in SERVICES, using label when it is not there,
    #   and return a line like "10.0.0.5 port 22 (ssh)".
    return ""


def main():
    print(parse_endpoint("10.0.0.5:22"))
    print(describe("10.0.0.5", 22))
    print(describe("10.0.0.9", 8080, label="not listed"))


if __name__ == "__main__":
    main()
```

`check.py`, the script that imports it, saved in the same folder:

```python
# @starter check.py
"""check.py: describe a list of endpoints with endpoint.py"""
# TODO 4: import the endpoint module.

ENDPOINTS = ["10.0.0.5:22", "10.0.0.7:443", "10.0.0.9:8080", "10.0.0.9:70000"]


def main():
    for text in ENDPOINTS:
        # TODO 5: parse text with endpoint.parse_endpoint. For a valid port,
        #   print endpoint.describe(host, port); otherwise print
        #   "<text>: not a valid port". Replace the line below.
        print(text)


if __name__ == "__main__":
    main()
```

**Run the module on its own, then the script that imports it:**

```bash
python3 endpoint.py
python3 check.py
```

```
(.venv) $ python3 endpoint.py
('10.0.0.5', 22)
10.0.0.5 port 22 (ssh)
10.0.0.9 port 8080 (not listed)
(.venv) $ python3 check.py
10.0.0.5 port 22 (ssh)
10.0.0.7 port 443 (https)
10.0.0.9 port 8080 (unknown)
10.0.0.9:70000: not a valid port
```

Compare the two runs: `check.py` imports `endpoint.py`, yet none of `endpoint.py`'s own three test lines appear in its output.

> [!example] Record
> Your completed `endpoint.py` and `check.py`.
> The output of each run, each in its own box.
> One screenshot of both runs (`ex4-check.png`).
> Then answer the Exercise 4 questions in the Submission.

---

## Exercise 5: Read a Log That Has Bad Lines — REQUIRED

> **🔨 FROM SCRATCH** | Difficulty: ⭐⭐ Medium
> *Write `clean.py` yourself from the requirements, until its runs match the ones shown, then read one traceback.*

> [!note] Real input fails, and the program carries on
> A **file** is named data on disk that outlives the program: `with open(name) as f:` opens it and closes it again when the block ends, and `"w"` opens it for writing, creating it or emptying it first.
> Real logs hold lines a parser cannot read, and a failing line raises an **exception**, which stops the whole run unless it is handled.
> `try` and `except ValueError` handle the one kind of failure you expect: the bad line is skipped and the loop carries on.
> A failure the program cannot recover from, such as a missing input file, ends it with `raise SystemExit("message")`: one line for the user, no traceback, exit status 1.

The input is `access.log`, written in Setup.
Four of its six lines are well formed, and two are not:

```
09:14:03 10.0.0.23 3389
09:14:41 10.0.0.7 443
09:15:10 10.0.0.41 ssh
09:15:52 10.0.0.7 80
09:16:00 10.0.0.12
09:16:30 10.0.0.41 22
```

**Requirements for `clean.py`:**
- Two constants: `SOURCE = "access.log"` and `TARGET = "clean.log"`.
- The work happens in a function `main()`, called under the main guard.
- Read all of `SOURCE` inside a `try`.
  When the file does not exist, end with `raise SystemExit(f"{SOURCE} not found")`.
- Open `TARGET` for writing, and for each line of the text:
  - split it into its time, host and port, and convert the port with `int()`, both inside one `try`
  - on a `ValueError`, count the line as skipped and go on to the next one: a missing field and a port that is not a number both raise it, so one `except ValueError` handles both
  - otherwise write the line to `TARGET` as `<time> <host> <port>` with a newline, and count it as kept
- Finally print `kept <k>, skipped <s>, wrote clean.log`.

**Your runs must print exactly this.**
`cd /tmp` runs the same script from a folder that has no `access.log`:

```bash
python3 clean.py
cat clean.log
cd /tmp
python3 ~/session5/clean.py
echo $?
cd ~/session5
```

```
(.venv) $ python3 clean.py
kept 4, skipped 2, wrote clean.log
(.venv) $ cat clean.log
09:14:03 10.0.0.23 3389
09:14:41 10.0.0.7 443
09:15:52 10.0.0.7 80
09:16:30 10.0.0.41 22
(.venv) $ cd /tmp
(.venv) $ python3 ~/session5/clean.py
access.log not found
(.venv) $ echo $?
1
(.venv) $ cd ~/session5
```

`open("access.log")` looks in the folder you run the command from, not in the script's folder, which is why the same script fails from `/tmp`.

### Reading a traceback

When an exception is not handled, Python prints a traceback and stops.
Here is a short script whose function raises one, and the traceback its run printed:

```python
def check(port):
    if not 0 <= port <= 65535:
        raise ValueError(f"port out of range: {port}")
    return port


print("Using port", check(70000))
```

```
$ python3 unhandled.py
Traceback (most recent call last):
  File "/home/kali/python-essentials/unhandled.py", line 7, in <module>
    print("Using port", check(70000))
                        ~~~~~^^^^^^^
  File "/home/kali/python-essentials/unhandled.py", line 3, in check
    raise ValueError(f"port out of range: {port}")
ValueError: port out of range: 70000
$ echo $?
1
```

Read it from the bottom up, and answer in the Submission:

1. The last line names what went wrong.
   a. Which exception was raised?
   b. With what message?
2. The traceback lists the calls that led there, the most recent last.
   a. Which function raised the exception?
   b. On which line of the file?
   c. On which line was that function called?
3. The shell recorded how the run ended.
   a. What exit status did it end with?

> [!example] Record
> Your `clean.py`.
> The output of `python3 clean.py`, of `cat clean.log`, and of the run from `/tmp` with `echo $?`, each in its own box.
> One screenshot of the three (`ex5-clean.png`).
> Then answer 1a to 3a and the Exercise 5 questions in the Submission.

---

## Exercise 6: Decode a Binary Address File — REQUIRED

> **🧩 GUIDED: complete the starter below** | Difficulty: ⭐⭐⭐ Hard
> *Save the starter as `readaddrs.py`, fill its three `# TODO` gaps, and run it on all three files below.*

> [!note] A binary file is bytes at agreed offsets
> `addrs.bin` holds addresses as raw bytes, the way a program stores them compactly rather than as text, so it is opened with `"rb"` and read as **`bytes`**.
> Nothing in the bytes marks where one field ends: the layout is an agreement between the program that wrote the file and the one that reads it.
>
> | Offset | Length | Holds |
> |---|---|---|
> | 0 | 4 bytes | a **tag**, the ASCII text `ADR1`, saying what kind of file this is |
> | 4 | 1 byte | the **count**, how many addresses follow |
> | 5 | 4 bytes each | the addresses, one byte for each of the four numbers |
>
> Two operations read it, and they return different types.
> A **slice**, `data[0:4]`, returns `bytes`, which compares with `b"ADR1"`.
> An **index**, `data[4]`, returns one byte as an `int`, which is a count you can calculate with.
> A reader checks the tag and the length before it trusts anything else, because a file that is the wrong kind, or cut short, would otherwise be read as garbage without any error.

```python
# @starter readaddrs.py
"""readaddrs.py: list the addresses stored in a tagged binary file"""

TAG = b"ADR1"


def main():
    name = input("Address file: ")
    try:
        with open(name, "rb") as f:
            data = f.read()
    except FileNotFoundError:
        raise SystemExit(f"{name} not found")
    # TODO 1: compare the first four bytes, as a slice, with TAG. When they
    #   differ, raise SystemExit(f"{name}: wrong tag {data[0:4]}").
    # TODO 2: the count is the byte at index 4, and indexing gives an int.
    #   The file must then be size bytes long; when it is not,
    #   raise SystemExit(f"{name}: needs {size} bytes, has {len(data)}").
    count = 0
    size = 5 + 4 * count
    print(f"tag {data[0:4].decode('ascii')}, {count} addresses")
    # TODO 3: step through the addresses four bytes at a time, from index 5.
    #   Unpack each slice into four ints and print the dotted address, two
    #   spaces, and the same four bytes in hex: .hex(" ").


if __name__ == "__main__":
    main()
```

The program asks for the file's name with `input()`.
Exercise 7 replaces that question with a name given on the command line.

**Run it on the good file, then on the file with the wrong tag:**

```
(.venv) $ python3 readaddrs.py
Address file: addrs.bin
tag ADR1, 3 addresses
10.0.0.5  0a 00 00 05
10.0.0.7  0a 00 00 07
192.168.1.10  c0 a8 01 0a
(.venv) $ python3 readaddrs.py
Address file: bad.bin
bad.bin: wrong tag b'ADR2'
(.venv) $ echo $?
1
```

**Then cut a good file short and read that.**
`head -c 12` copies only the first 12 bytes of a file, as a download that stopped partway would leave it:

```bash
head -c 12 addrs.bin > short.bin
python3 readaddrs.py
echo $?
```

```
(.venv) $ head -c 12 addrs.bin > short.bin
(.venv) $ python3 readaddrs.py
Address file: short.bin
short.bin: needs 17 bytes, has 12
(.venv) $ echo $?
1
```

> [!example] Record
> Your completed `readaddrs.py`.
> The run on `addrs.bin`, the run on `bad.bin` with `echo $?`, and the run on `short.bin` with `echo $?`, each in its own box.
> One screenshot of the three runs (`ex6-readaddrs.png`).
> Then answer the Exercise 6 questions in the Submission.

---

## Exercise 7: Turn a Script Into a Command-Line Tool — REQUIRED

> **🔨 FROM SCRATCH** | Difficulty: ⭐⭐ Medium
> *Write `lines.py` and `addrcheck.py` yourself from the requirements, until their runs match the ones shown.*

> [!note] A tool takes its input from the command line
> A program that stops to ask questions cannot run inside a script or on a schedule, so a tool takes its input as **arguments** on the command line.
> `sys.argv` is the list of those words, the script's own name first, which a small script reads directly.
> `argparse` builds the rest from a description of the arguments: the usage line, a `-h` help page, and an error for every argument it cannot convert.
> **`type=`** names the function that converts an argument's text, so a bad value is rejected before your code runs.
> argparse ends a run it rejects with **exit status 2**, and `raise SystemExit("message")` ends one with 1, so a calling script can tell a mistyped command from a failed check.

### 7a: A script on `sys.argv`

**Requirements for `lines.py`:**
- `import sys`.
- With more than one argument after the script's name, end with `raise SystemExit("usage: python3 lines.py [file]")`.
- Take the file's name from `sys.argv[1]` when one is given, and use `access.log` otherwise, in one line with a conditional expression.
- Read the file and print `<file>: <n> lines`.

**Your runs must print exactly this:**

```
(.venv) $ python3 lines.py
access.log: 6 lines
(.venv) $ python3 lines.py clean.log
clean.log: 4 lines
(.venv) $ python3 lines.py access.log clean.log
usage: python3 lines.py [file]
(.venv) $ echo $?
1
```

### 7b: A tool built with `argparse`

**Requirements for `addrcheck.py`:**
- `import argparse` and `import ipaddress`, and the work in `main()` under the main guard.
- A parser with the description `Check an address and a port.`
- A positional argument `address`, converted with `type=ipaddress.ip_address`, with the help text `the address to check`.
- An option `--port`, converted with `type=int`, with the help text `a port to check with it`.
- Print `<address> is an IPv<version> address`, the version taken from the address's `.version`.
- Then:
  - with no `--port`, print `no port given`
  - with a port from 0 to 65535, print `port <port> is valid`
  - otherwise, end with `raise SystemExit(f"port {args.port} is out of range")`

**Your runs must print exactly this.**
Run `echo $?` after each failing run, as shown:

```
(.venv) $ python3 addrcheck.py -h
usage: addrcheck.py [-h] [--port PORT] address

Check an address and a port.

positional arguments:
  address      the address to check

options:
  -h, --help   show this help message and exit
  --port PORT  a port to check with it
(.venv) $ python3 addrcheck.py 10.0.0.5 --port 22
10.0.0.5 is an IPv4 address
port 22 is valid
(.venv) $ python3 addrcheck.py 2001:db8::1
2001:db8::1 is an IPv6 address
no port given
(.venv) $ python3 addrcheck.py 10.0.0.256
usage: addrcheck.py [-h] [--port PORT] address
addrcheck.py: error: argument address: invalid ip_address value: '10.0.0.256'
(.venv) $ echo $?
2
(.venv) $ python3 addrcheck.py 10.0.0.5 --port ssh
usage: addrcheck.py [-h] [--port PORT] address
addrcheck.py: error: argument --port: invalid int value: 'ssh'
(.venv) $ echo $?
2
(.venv) $ python3 addrcheck.py 10.0.0.5 --port 70000
10.0.0.5 is an IPv4 address
port 70000 is out of range
(.venv) $ echo $?
1
```

You wrote none of the `-h` page and none of the two `error:` lines: argparse made them from your description and help texts.

> [!example] Record
> Your `lines.py` and `addrcheck.py`.
> The three `lines.py` runs, then each `addrcheck.py` run with its `echo $?` where it has one, each command in its own box.
> One screenshot of the `10.0.0.256` and `70000` runs with their two exit statuses (`ex7-addrcheck.png`).
> Then answer the Exercise 7 questions in the Submission.

---

# Hand In

Commit Exercise 7, then push and check that GitHub has everything:

```bash
cd ~/student-YOUR-USERNAME
git add Module0-Foundation/Session5
git commit -m "Module 0 Session 5: exercise 7"
git push
git status
```

**Checkpoint:** `git status` says `Your branch is up to date with 'origin/main'.`, and on GitHub your Practical Guide Submission shows every screenshot.
Your scripts stay in `~/session5`: the worksheet carries the code you hand in.

---

# When something fails

**Read the last line of the traceback first, and copy it exactly.**
It names the exception and the value that caused it, and most of the time it is enough to find the line to fix.
Then read upwards: the line above it shows the code that failed, with its file and line number.

The Troubleshooting FAQ is organized by the symptom in front of you, with each error message exactly as Python or the shell prints it.
A message pasted in full into the Telegram group is a two-minute answer, and "it does not work" is not.

---

# What "done" looks like

- `~/session5` holds `.venv`, and a new terminal there starts with `(.venv)`
- `pip show requests` names a `Location:` inside `.venv`, and Kali's own copy names another
- `./hello.py` runs on its own
- `logline.py`, `tally.py`, `check.py`, `clean.py`, `readaddrs.py`, `lines.py` and `addrcheck.py` each print what their exercise shows
- Your worksheet holds every exercise's code, output, screenshot and answers, with **AI Assistance** filled in
- On GitHub, `Module0-Foundation/Session5` shows the worksheet with every screenshot, and `git status` says **up to date**
