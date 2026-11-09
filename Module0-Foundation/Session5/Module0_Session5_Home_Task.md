# Module 0 · Session 5 — Home Task

## Checking Connections Against a Watchlist

### Professional Training in Cybersecurity I

---

> [!note] How this home task works
> In the Practical Guide you practiced each topic of the session on its own.
> **This home task puts all of them into one tool, and you finish it alone.**
> The tool is handed out as a starter: two files with numbered `# TODO` gaps, the rest of the code already written.
> What is assessed is that your completed tool prints exactly what the runs below show, and that you can explain why.
>
> Your worksheet is **`Module0_Session5_Home_Task_Submission.md`**, already in your repository's `Module0-Foundation/Session5` folder since the Practical Guide's Setup.
> Work in Kali, in `~/session5`, with the virtual environment you built in the Practical Guide.
> The deadline is **22:00 on the Saturday of the session's week**, and only what is on GitHub then counts.

> [!important] Everything here is required
> There are no optional parts: every `# TODO`, every run and every question.

---

# Before You Start

1. **Pull your repository**, because your instructor's feedback on the Practical Guide arrives there:

   ```bash
   cd ~/student-YOUR-USERNAME
   git pull
   ```

2. **Open your working folder** and a new terminal in it:

   ```bash
   code ~/session5
   ```

   In VS Code, open **Terminal**, then **New Terminal**.
   It activates `.venv` by itself, so its prompt starts with `(.venv)`.

---

# Task 1: Build the Watchlist Checker — REQUIRED

> **🧩 GUIDED: complete the two starters below** | Difficulty: ⭐⭐⭐ Hard
> *Fill the three `# TODO` gaps in `watchlib.py` and the three in `watchlist.py`, then run the tool until it prints what every run below shows.*

> [!note] A watchlist is what monitoring keeps an eye on
> A **watchlist** is a short list of addresses that a defender has reason to follow closely, such as hosts involved in an earlier incident.
> Monitoring checks every new log against it and reports each line that involves a watched host, so a person reads a handful of lines instead of the whole log.
> This checker reads a text **connection log** and a binary **watchlist** of 4-byte addresses, skips the log lines it cannot parse, and writes a **report** of every connection to or from a watched host, with a count per host.
> It is built the way the Practical Guide built its tools: a module of functions, `watchlib.py`, and a command-line script that uses it, `watchlist.py`.

> [!tip] Every topic of the session is in this tool
> - **The environment:** `watchlist.py` has a shebang and runs as `./watchlist.py` from your `.venv`.
> - **Values and text:** each report line is an f-string, the action padded to a width.
> - **Control flow and collections:** a set of watched addresses, a dictionary of counts, a list of report lines.
> - **Functions and modules:** two functions with docstrings in `watchlib.py`, imported by `watchlist.py`, which has a main guard.
> - **Files and exceptions:** a bad log line raises `ValueError` and is skipped, and the report is written with `"w"`.
> - **Bytes:** the watchlist is read with `"rb"`, 4 bytes per address.
> - **The command line:** `argparse` takes the log, a `--watchlist` and an `--out`, and `ipaddress.ip_address` checks every address.

## Step 1: Lay down the data

Save this block as **`make_watch_data.py`** in `~/session5`, then run it:

```python
# @generator make_watch_data.py
# @expect writes connections.log (10 lines) and watchlist.bin (12 bytes)
"""make_watch_data.py: write the Home Task's connection log and watchlist"""

LOG = """09:14:03 ALLOW 10.0.0.7 443
09:14:20 DENY 10.0.0.23 3389
09:14:41 ALLOW 10.0.0.12 53
09:15:02 DENY 10.0.0.300 22
09:15:10 ALLOW 10.0.0.7 http
09:15:33 DENY 10.0.0.23 445
09:15:52 ALLOW 192.168.1.10 22
09:16:00 ALLOW 10.0.0.12
09:16:30 DENY 10.0.0.41 99999
09:16:45 ALLOW 10.0.0.23 443
"""

with open("connections.log", "w") as f:
    f.write(LOG)
with open("watchlist.bin", "wb") as f:
    f.write(bytes([10, 0, 0, 23, 192, 168, 1, 10, 10, 0, 0, 99]))
print("wrote connections.log and watchlist.bin")
```

```
(.venv) $ python3 make_watch_data.py
wrote connections.log and watchlist.bin
```

Each line of `connections.log` holds a time, the firewall's action, a host and a port, separated by spaces.
Some lines are malformed on purpose, as lines in real logs are.
`watchlist.bin` has no tag and no count: it is nothing but addresses, 4 bytes each.

## Step 2: Complete the module

`watchlib.py` holds the two functions that read the data.
Complete its three TODOs first, because `watchlist.py` calls both functions.

```python
# @starter watchlib.py
"""watchlib.py: read a binary watchlist and parse connection log lines"""
import ipaddress


def read_watchlist(path):
    """Return the set of addresses stored in path, 4 bytes each."""
    try:
        with open(path, "rb") as f:
            data = f.read()
    except FileNotFoundError:
        raise SystemExit(f"{path} not found")
    # TODO 1: the file must hold whole 4-byte addresses. When it does not,
    #   raise SystemExit(f"{path}: {len(data)} bytes, not 4 per address").
    watched = set()
    # TODO 2: for each 4 bytes, build the dotted text, convert it with
    #   ipaddress.ip_address, and add the result to watched.
    return watched


def parse_line(line):
    """Return (time, action, host, port) from one line, or raise ValueError."""
    # TODO 3: split the line into its four fields. Convert the host with
    #   ipaddress.ip_address and the port with int(). When the port is not
    #   from 0 to 65535, raise ValueError(f"port out of range: {port}").
    #   Replace the line below with the return.
    raise ValueError("parse_line is not written yet")
```

`parse_line` signals every kind of bad line the same way, by raising `ValueError`, so its caller needs only one `except`.

## Step 3: Complete the tool

`watchlist.py` is the command-line tool.
Its first line is the shebang, so keep the tag line below it.

```python
#!/usr/bin/env python3
# @starter watchlist.py
"""watchlist.py: report the connections whose host is on a watchlist"""
import argparse

import watchlib


def main():
    parser = argparse.ArgumentParser(
        description="Report the log lines whose host is on the watchlist.")
    parser.add_argument("log", help="the connection log to check")
    # TODO 4: add two options with defaults and help text:
    #   --watchlist, default "watchlist.bin", the binary watchlist;
    #   --out, default "report.txt", where to write the report.
    args = parser.parse_args()

    watched = watchlib.read_watchlist(args.watchlist)
    try:
        with open(args.log) as f:
            text = f.read()
    except FileNotFoundError:
        raise SystemExit(f"{args.log} not found")

    hits = {}
    lines = []
    skipped = 0
    for line in text.splitlines():
        # TODO 5: parse the line with watchlib.parse_line, and count it as
        #   skipped when that raises ValueError. When the host is in watched,
        #   add 1 to its count in hits and append to lines a report line like
        #   "09:14:20 DENY  10.0.0.23:3389" (the action 5 characters wide).
        #   Replace the line below.
        skipped = skipped + 1

    # TODO 6: open args.out for writing and write the report: the line
    #   "Watchlist report for <log>", each line in lines, the line
    #   "Connections per watched host:", then each host and its count,
    #   indented two spaces and separated by two spaces.
    print(f"{len(watched)} watched, {len(lines)} matches, {skipped} skipped")
    print(f"report written to {args.out}")


if __name__ == "__main__":
    main()
```

Until TODO 4 adds the two options, `watchlist.py` stops with an `AttributeError` on `args.watchlist`: that is the starter being incomplete, not your module failing.

## Step 4: Run it as a command

**Make it executable and read its help.**
The first run fails on purpose: a new file has no execute bit.

```bash
./watchlist.py connections.log
chmod +x watchlist.py
./watchlist.py -h
```

```
(.venv) $ ./watchlist.py connections.log
bash: ./watchlist.py: Permission denied
(.venv) $ chmod +x watchlist.py
(.venv) $ ./watchlist.py -h
usage: watchlist.py [-h] [--watchlist WATCHLIST] [--out OUT] log

Report the log lines whose host is on the watchlist.

positional arguments:
  log                   the connection log to check

options:
  -h, --help            show this help message and exit
  --watchlist WATCHLIST
                        the binary watchlist (default: watchlist.bin)
  --out OUT             where to write the report (default: report.txt)
```

**Check the log, then read the report.**
Your runs must print exactly this:

```bash
./watchlist.py connections.log
cat report.txt
```

```
(.venv) $ ./watchlist.py connections.log
3 watched, 4 matches, 4 skipped
report written to report.txt
(.venv) $ cat report.txt
Watchlist report for connections.log
09:14:20 DENY  10.0.0.23:3389
09:15:33 DENY  10.0.0.23:445
09:15:52 ALLOW 192.168.1.10:22
09:16:45 ALLOW 10.0.0.23:443
Connections per watched host:
  10.0.0.23  3
  192.168.1.10  1
```

**Write the same report under another name, and compare the two.**
`diff` prints nothing when two files are the same and exits with status 0, so `&& echo same` prints `same` only then:

```bash
./watchlist.py connections.log --out hits.txt
diff report.txt hits.txt && echo same
```

```
(.venv) $ ./watchlist.py connections.log --out hits.txt
3 watched, 4 matches, 4 skipped
report written to hits.txt
(.venv) $ diff report.txt hits.txt && echo same
same
```

**Then make it fail three ways**, with `echo $?` after each.
The last one cuts the watchlist to its first 6 bytes, an address and a half:

```bash
./watchlist.py
echo $?
./watchlist.py missing.log
echo $?
head -c 6 watchlist.bin > cut.bin
./watchlist.py connections.log --watchlist cut.bin
echo $?
```

```
(.venv) $ ./watchlist.py
usage: watchlist.py [-h] [--watchlist WATCHLIST] [--out OUT] log
watchlist.py: error: the following arguments are required: log
(.venv) $ echo $?
2
(.venv) $ ./watchlist.py missing.log
missing.log not found
(.venv) $ echo $?
1
(.venv) $ head -c 6 watchlist.bin > cut.bin
(.venv) $ ./watchlist.py connections.log --watchlist cut.bin
cut.bin: 6 bytes, not 4 per address
(.venv) $ echo $?
1
```

**Checkpoint:** every run above matches yours line for line, `report.txt` included.

> [!example] Record
> Your completed `watchlib.py` and `watchlist.py`.
> The output of each command above, each in its own box: the three setup commands, the check and `cat report.txt`, the `--out` run and `diff`, and the three failing runs with their `echo $?`.
> One screenshot of the check and `cat report.txt` in the terminal (`task1-watchlist.png`).
> Then answer the Task 1 questions in the Submission.

---

# Hand In

Look at your screenshot once before pushing: it must not show a password, a key or a token.
Then commit, push and check:

```bash
cd ~/student-YOUR-USERNAME
git add Module0-Foundation/Session5
git commit -m "Module 0 Session 5: home task"
git push
git status
```

`git status` must say `Your branch is up to date with 'origin/main'.`
If it says **ahead**, the push did not happen: read the error `git push` printed.
Then open your Home Task Submission on GitHub and check that the screenshot shows.

---

# What "done" looks like

- `watchlib.py` and `watchlist.py` complete, every `# TODO` filled
- `./watchlist.py connections.log` prints `3 watched, 4 matches, 4 skipped`, and `report.txt` matches the one above
- The three failing runs end with exit statuses 2, 1 and 1
- Your worksheet holds both files, every output, `task1-watchlist.png` and your answers, with **AI Assistance** filled in
- `git status` says **up to date** after the push
