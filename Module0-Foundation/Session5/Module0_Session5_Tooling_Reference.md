# Module 0 · Session 5 — Tooling Reference

## Python Essentials for Cybersecurity

### Professional Training in Cybersecurity I

---

> [!note] What this document is for
> The session showed each part of Python once, through one example.
> **This is the fuller treatment**: every tool and idiom the session used, and the ones it named and left for later, each with what it is for, an example with its real output, and where it differs from what you might expect.
> Nothing here is required reading in order.
> Come to it when you need it.
>
> Every example is a small file followed by the command that runs it and what it printed, so you can type it into `~/session5` and see the same.
> Some examples read the sample files the Practical Guide's Setup writes, `access.log` and `addrs.bin`.

> [!note] Python 3.14 on Kali
> These examples were recorded on **Python 3.14.7**, which is what `python3` is on Kali today.
> A Kali that has not been upgraded may still run 3.13, as the session's own transcripts do.
> Nothing in this document behaves differently between the two: you will see only a different version number, and `python3.13` in place of `python3.14` in a path such as `.venv/lib/python3.14/site-packages`.

---

# The Python Environment

Kali's own Python runs Kali's own tools, so you never install into it.
Each project gets a **virtual environment**: a folder with its own `python3`, its own `pip`, and its own place for packages.

## Kali's Python refuses `pip install`

Outside an environment, `pip` stops before it changes anything:

```
$ pip install requests
error: externally-managed-environment

× This environment is externally managed
╰─> To install Python packages system-wide, try apt install
    python3-xyz, where xyz is the package you are trying to
    install.
    
    If you wish to install a non-Kali-packaged Python package,
    create a virtual environment using python3 -m venv path/to/venv.
    Then use path/to/venv/bin/python and path/to/venv/bin/pip. Make
    sure you have python3-full installed.
    
    If you wish to install a non-Kali-packaged Python application,
    it may be easiest to use pipx install xyz, which will manage a
    virtual environment for you. Make sure you have pipx installed.
    
    For more information, refer to the following:
    * https://www.kali.org/docs/general-use/python3-external-packages/
    * /usr/share/doc/python3.14/README.venv

note: If you believe this is a mistake, please contact your Python installation or OS distribution provider. You can override this, at the risk of breaking your Python installation or OS, by passing --break-system-packages.
hint: See PEP 668 for the detailed specification.
```

The message names both ways out: a virtual environment for a package your own code imports, and `pipx` for a program you want to run as a command.
`--break-system-packages` overrides the check and can replace a package that Kali's tools depend on, so it is never the answer in this course.

## Creating, activating and leaving an environment

```bash
python3 -m venv .venv          # create the folder .venv
source .venv/bin/activate      # switch it on: the prompt gains (.venv)
deactivate                     # switch it off
```

Activation puts `.venv/bin` first on `PATH`, the list of folders the shell searches for a command, so the same word now finds a different file:

```
$ which python3
/usr/bin/python3
(.venv) $ which python3
/home/kali/session5/.venv/bin/python3
```

`.venv` holds a whole Python of its own:

```
(.venv) $ ls .venv .venv/bin
.venv:
bin  include  lib  lib64  pyvenv.cfg

.venv/bin:
Activate.ps1  activate.csh   idna	 pip   pip3.14	python3     𝜋thon
activate      activate.fish  normalizer  pip3  python	python3.14
```

`activate` is the file `source` reads.
`python3` and `pip` are the environment's own copies.
The other `activate` files are for other shells, and `𝜋thon` is a joke name Python 3.14 adds, the same program as `python3`.

> [!tip] Deleting an environment is safe
> `.venv` holds nothing you wrote.
> If it breaks, `deactivate`, then `rm -rf .venv`, create it again and reinstall from `requirements.txt` (below).

> [!tip] VS Code activates it for you
> A new terminal in VS Code, in a folder that holds `.venv`, starts by typing `source .../.venv/bin/activate` by itself.
> The terminal you created `.venv` in is the exception: activate that one by hand.

## Installing and listing packages: `pip`

```bash
pip install requests           # install a package and what it needs
pip show requests              # its version, and where it is installed
pip list                       # everything installed in this environment
pip uninstall -y requests      # remove it; -y skips the question
python3 -m pip install ...     # the pip that belongs to this python3, whichever it is
```

`pip install` lists every package it collects, then ends with one line naming what it installed:

```
Successfully installed certifi-2026.7.22 charset_normalizer-3.5.2 idna-3.20 requests-2.34.2 urllib3-2.8.0
```

```
(.venv) $ pip list
Package            Version
------------------ ---------
certifi            2026.7.22
charset-normalizer 3.5.2
idna               3.20
pip                26.1.2
requests           2.34.2
urllib3            2.8.0
```

`requests` brought four packages with it.
`pip` itself is in every environment.

```
(.venv) $ pip uninstall -y requests
Found existing installation: requests 2.34.2
Uninstalling requests-2.34.2:
  Successfully uninstalled requests-2.34.2
```

## Recording what a project needs: `requirements.txt`

`pip freeze` prints every installed package with its exact version, one per line, in the form `pip install -r` reads back.
Saved to a file, it lets anyone rebuild the same environment:

```
(.venv) $ pip freeze > requirements.txt
(.venv) $ cat requirements.txt
certifi==2026.7.22
charset-normalizer==3.5.2
idna==3.20
requests==2.34.2
urllib3==2.8.0
```

`requests` was uninstalled above, so reinstalling from the file brings it back and leaves the rest alone:

```
(.venv) $ pip install -r requirements.txt
Requirement already satisfied: certifi==2026.7.22 in ./.venv/lib/python3.14/site-packages (from -r requirements.txt (line 1)) (2026.7.22)
Requirement already satisfied: charset-normalizer==3.5.2 in ./.venv/lib/python3.14/site-packages (from -r requirements.txt (line 2)) (3.5.2)
Requirement already satisfied: idna==3.20 in ./.venv/lib/python3.14/site-packages (from -r requirements.txt (line 3)) (3.20)
Collecting requests==2.34.2 (from -r requirements.txt (line 4))
  Using cached requests-2.34.2-py3-none-any.whl.metadata (4.8 kB)
Requirement already satisfied: urllib3==2.8.0 in ./.venv/lib/python3.14/site-packages (from -r requirements.txt (line 5)) (2.8.0)
Using cached requests-2.34.2-py3-none-any.whl (73 kB)
Installing collected packages: requests
Successfully installed requests-2.34.2
```

## Installing a command-line program: `pipx`

`pipx` installs a Python **program** in an environment of its own and puts its command on your `PATH`, so you can run it anywhere without activating anything.
Use it for a tool you run, and an environment for a library your code imports.
If Kali says `pipx: command not found`, install it with `sudo apt install pipx`.

```
$ pipx install hashid
WARNING: Skipping setuptools as it is not installed.
  installed package hashid 3.1.4, installed using Python 3.14.7
  These apps are now available
    - hashid
done! ✨ 🌟 ✨
$ pipx list
venvs are in /home/kali/.local/share/pipx/venvs
apps are exposed on your $PATH at /home/kali/.local/bin
manual pages are exposed at /home/kali/.local/share/man
   package hashid 3.1.4, installed using Python 3.14.7
    - hashid
```

`hashid` is a small program that guesses a hash's type.
`WARNING: Skipping setuptools` is harmless.
The new command lives in `~/.local/bin`, which is already on Kali's `PATH`.

## Running a script as a command

A script runs as `./name.py` when its first line is a **shebang** and it has the **execute bit**:

```python
#!/usr/bin/env python3
print("This script runs on its own.")
```

```
(.venv) $ ./hello.py
bash: ./hello.py: Permission denied
(.venv) $ chmod +x hello.py
(.venv) $ ./hello.py
This script runs on its own.
```

`#!/usr/bin/env python3` asks `env` to find `python3` on `PATH`, so with an environment active the script runs on the environment's Python.

## Asking Python itself: `help()` and `dir()`

`help()` prints the documentation of anything Python knows, and `dir()` lists the names something has.
In a terminal, `help()` opens a pager: scroll with the arrow keys and press `q` to leave.

```
(.venv) $ python3 -c 'help(str.strip)'
Help on method descriptor strip:

strip(self, chars=None, /) unbound builtins.str method
    Return a copy of the string with leading and trailing whitespace removed.

    If chars is given and not None, remove characters in chars instead.
(.venv) $ python3 -c 'print(dir("")[-12:])'
['rpartition', 'rsplit', 'rstrip', 'split', 'splitlines', 'startswith', 'strip', 'swapcase', 'title', 'translate', 'upper', 'zfill']
```

`dir("")` lists every method a string has, and `[-12:]` keeps the last twelve so they fit here.

---

# Values, Types and Text

A program works on **values**: the numbers, text and data it reads, compares and prints.
What it can do with each one depends on the value's type, so most mistakes in this section are a value of the wrong type.

## Types

Every value has a **type**, which decides what you can do with it.
`type()` names it:

```python
print(type(443), type("443"), type(4.5))
print(type(True), type(None), type(b"443"))
```
```
(.venv) $ python3 kinds.py
<class 'int'> <class 'str'> <class 'float'>
<class 'bool'> <class 'NoneType'> <class 'bytes'>
```

`int` and `float` are numbers, `str` is text, `bool` is `True` or `False`, `None` means *no value*, and `bytes` is raw data.

## Converting between types

```python
print(int("443"), int(" 443\n"), int("1bb", 16), int("0x1bb", 16))
print(str(443) + "/tcp", hex(443), bin(5), float("4.5"))
```
```
(.venv) $ python3 convert.py
443 443 443 443
443/tcp 0x1bb 0b101 4.5
```

`int()` ignores spaces and a newline around the digits, which is why a line read from a file converts without stripping.
`int(text, 16)` reads hexadecimal, with or without the `0x`.
`str()`, `hex()` and `bin()` go the other way, from a number to text.

## String methods

A method is called on a string with a dot, and returns a **new** string or list: the original never changes.

```python
line = "  DENY 10.0.0.23:3389\n"
print(repr(line.strip()))
print(line.split())
print(line.split()[1].split(":"))
print(" | ".join(["DENY", "10.0.0.23", "3389"]))
print(line.strip().startswith("DENY"), line.strip().endswith("3389"))
print(line.strip().replace("DENY", "ALLOW"), line.strip().lower())
print("10.0.0.23" in line, line.count("0"))
```
```
(.venv) $ python3 strings.py
'DENY 10.0.0.23:3389'
['DENY', '10.0.0.23:3389']
['10.0.0.23', '3389']
DENY | 10.0.0.23 | 3389
True True
ALLOW 10.0.0.23:3389 deny 10.0.0.23:3389
True 3
```

| Method | Returns |
|---|---|
| `strip()` | the string without spaces and newlines at either end |
| `split()` | a list of the words, split at any run of spaces |
| `split(":")` | a list of the parts between each `:` |
| `sep.join(list)` | one string, the items with `sep` between them |
| `startswith(x)`, `endswith(x)` | `True` or `False` |
| `replace(a, b)` | the string with every `a` replaced by `b` |
| `lower()`, `upper()` | the string in one case |
| `x in s` | `True` when `x` appears anywhere in `s` |
| `count(x)` | how many times `x` appears |

## Indexing and slicing

`s[i]` is one character, counted from 0, and a negative index counts from the end.
`s[a:b]` is the characters from `a` up to but not including `b`, and a missing number means *from the start* or *to the end*.

```python
host = "10.0.0.23"
print(host[0], host[-1], host[0:4], host[:4], host[3:], host[-2:])
print(len(host), host[0:100], repr(host[20:]))
```
```
(.venv) $ python3 slices.py
1 3 10.0 10.0 0.0.23 23
9 10.0.0.23 ''
```

A slice past the end returns what there is, and an empty string when there is nothing: it never raises an error.
An index past the end does raise `IndexError`.

## Format specs in f-strings

After a colon inside `{}`, a **format spec** says how to show the value:

```python
port = 443
print(f"[{port}] [{port:5}] [{port:<5}] [{port:^7}] [{port:05}]")
print(f"[{port:x}] [{port:#x}] [{port:#06x}] [{port:b}] [{port:016b}]")
action = "DENY"
print(f"[{action:5}] [{action:>6}] [{3.14159:.2f}] [{0.25:.0%}]")
print(f"{port=}")
```
```
(.venv) $ python3 formats.py
[443] [  443] [443  ] [  443  ] [00443]
[1bb] [0x1bb] [0x01bb] [110111011] [0000000110111011]
[DENY ] [  DENY] [3.14] [25%]
port=443
```

| Spec | Means | `443` shows as |
|---|---|---|
| `5` | at least 5 wide, numbers right-aligned | `  443` |
| `<5`, `>5`, `^7` | left, right, centered | `443  `, `  443`, `  443  ` |
| `05` | 5 wide, padded with zeros | `00443` |
| `x`, `#x` | hexadecimal, with `#` adding `0x` | `1bb`, `0x1bb` |
| `#06x` | hex, `0x` counted in the 6 | `0x01bb` |
| `b`, `016b` | binary, the second 16 digits | `110111011`, `0000000110111011` |
| `.2f`, `.0%` | 2 decimals, a percentage | for `3.14159`: `3.14`, for `0.25`: `25%` |

Text is left-aligned by default.
`{port=}` prints the name and its value, which is handy while debugging.

## Reading what the user types: `input()`

```python
port = input("Port: ")
print(type(port), repr(port))
```
```
(.venv) $ python3 ask.py
Port: 443
<class 'str'> '443'
```

`input()` always returns a `str`, whatever was typed.
Convert it with `int()` before comparing it with a number.

## Common mistakes

**Joining text and a number with `+`:**

```python
print("Port " + 443)
```
```
(.venv) $ python3 concat.py
Traceback (most recent call last):
  File "/home/kali/session5/concat.py", line 1, in <module>
    print("Port " + 443)
          ~~~~~~~~^~~~~
TypeError: can only concatenate str (not "int") to str
```

Convert first, `"Port " + str(443)`, or use an f-string, `f"Port {443}"`.

**A number format on text:**

```python
port = "443"
print(f"{port:#06x}")
```
```
(.venv) $ python3 formatstr.py
Traceback (most recent call last):
  File "/home/kali/session5/formatstr.py", line 2, in <module>
    print(f"{port:#06x}")
            ^^^^^^^^^^^
ValueError: Unknown format code 'x' for object of type 'str'
```

The value is the text `"443"`, so `x` has nothing to convert: `int(port)` first.

---

# Control Flow and Collections

Control flow decides which lines run and how often, and collections hold many values under one name.
Together they turn a script that handles one line of a log into one that handles all of them.

## Choosing a branch: `if`, `elif`, `else`

```python
for port in [22, 8080, 70000]:
    if port < 1024:
        print(port, "well-known")
    elif port <= 65535:
        print(port, "registered or dynamic")
    else:
        print(port, "not a port")
```
```
(.venv) $ python3 classify.py
22 well-known
8080 registered or dynamic
70000 not a port
```

Python tests each condition in order and runs the first block whose test is true, then skips the rest.
`0 <= port <= 65535` is a **chained comparison**, true only when both halves are.

## Loops

```python
for i in range(3):
    print("pass", i)
print(list(range(1, 10, 3)))
for i, host in enumerate(["10.0.0.5", "10.0.0.7"]):
    print(i, host)
for port in [22, -1, 80, 443]:
    if port < 0:
        continue
    if port == 443:
        break
    print("checked", port)
tries = 0
while tries < 2:
    tries = tries + 1
print("tries:", tries)
```
```
(.venv) $ python3 loops.py
pass 0
pass 1
pass 2
[1, 4, 7]
0 10.0.0.5
1 10.0.0.7
checked 22
checked 80
tries: 2
```

- `range(3)` counts 0, 1, 2, and `range(1, 10, 3)` counts from 1, below 10, in steps of 3.
- `enumerate(list)` gives each item with its position.
- `continue` skips to the next pass, and `break` leaves the loop at once: `443` stopped it before `checked 443`.
- `while` repeats as long as its test is true, so something in the body must make it false.

## Lists

A **list** holds items in order and can change.

```python
ports = [443, 22]
ports.append(80)
ports.extend([8080, 22])
print(ports, len(ports), 22 in ports, ports.index(80))
ports.remove(22)
last = ports.pop()
print(ports, last)
print(sorted(ports), min(ports), max(ports), sum(ports))
ports.sort(reverse=True)
print(ports)
```
```
(.venv) $ python3 lists.py
[443, 22, 80, 8080, 22] 5 True 2
[443, 80, 8080] 22
[80, 443, 8080] 80 8080 8603
[8080, 443, 80]
```

`append` adds one item, `extend` adds every item of another list, `remove` deletes the first match, and `pop` removes and returns the last.
`sorted(list)` returns a new sorted list, while `list.sort()` sorts the list itself and returns nothing.

## Tuples and unpacking

A **tuple** is a fixed group of values, written with commas.
**Unpacking** assigns its items to names in order:

```python
endpoint = ("10.0.0.5", 22)
host, port = endpoint
print(host, port, endpoint[1], len(endpoint))
a, b = 1, 2
a, b = b, a
print(a, b)
```
```
(.venv) $ python3 tuples.py
10.0.0.5 22 22 2
2 1
```

`a, b = b, a` swaps two values in one line.

## Dictionaries

A **dictionary** maps each key to a value.

```python
services = {22: "ssh", 443: "https"}
services[80] = "http"
print(services[22], services.get(8080), services.get(8080, "unknown"))
print(list(services.keys()), list(services.values()))
for port, name in services.items():
    print(port, name)
print(443 in services, len(services))
del services[80]
print(services)
```
```
(.venv) $ python3 dicts.py
ssh None unknown
[22, 443, 80] ['ssh', 'https', 'http']
22 ssh
443 https
80 http
True 3
{22: 'ssh', 443: 'https'}
```

`d[key]` raises `KeyError` for a missing key, and `d.get(key, default)` returns the default instead.
`items()` gives each key with its value, in the order they were added.

## Sets

A **set** holds each value once, in no particular order.

```python
seen = set(["10.0.0.5", "10.0.0.7", "10.0.0.5"])
seen.add("10.0.0.9")
print(len(seen), "10.0.0.7" in seen)
allowed = {"10.0.0.5", "10.0.0.6"}
print(sorted(seen & allowed), sorted(seen - allowed), sorted(seen | allowed))
```
```
(.venv) $ python3 sets.py
3 True
['10.0.0.5'] ['10.0.0.7', '10.0.0.9'] ['10.0.0.5', '10.0.0.6', '10.0.0.7', '10.0.0.9']
```

`&` is what both sets hold, `-` what the first holds and the second does not, and `|` everything in either.
A set prints in an order that can change from run to run, which is why these are passed through `sorted()`.

## List comprehensions

A **comprehension** builds a list, dictionary or set from a loop in one expression: `[expression for item in list if test]`.

```python
ports = [22, 70000, 443, -1, 80]
valid = [p for p in ports if 0 <= p <= 65535]
print(valid)
print([p * 2 for p in valid])
names = {22: "ssh", 443: "https"}
print({p: names.get(p, "unknown") for p in valid})
print({len(h) for h in ["10.0.0.5", "10.0.0.7", "192.168.1.10"]})
```
```
(.venv) $ python3 comprehensions.py
[22, 443, 80]
[44, 886, 160]
{22: 'ssh', 443: 'https', 80: 'unknown'}
{8, 12}
```

The first line is the loop-and-`if` filter written as one expression.
`{p: ... for p in ...}` builds a dictionary, and `{... for ...}` a set: three addresses have only two different lengths.

## `zip` and `sorted`

```python
hosts = ["10.0.0.7", "10.0.0.23", "10.0.0.5"]
ports = [443, 3389, 22]
for host, port in zip(hosts, ports):
    print(host, port)
print(sorted(ports), sorted(ports, reverse=True))
print(sorted(hosts), sorted(hosts, key=len))
counts = {"10.0.0.23": 3, "10.0.0.7": 5, "10.0.0.41": 1}
print(sorted(counts.items(), key=lambda pair: pair[1], reverse=True))
```
```
(.venv) $ python3 zipsort.py
10.0.0.7 443
10.0.0.23 3389
10.0.0.5 22
[22, 443, 3389] [3389, 443, 22]
['10.0.0.23', '10.0.0.5', '10.0.0.7'] ['10.0.0.7', '10.0.0.5', '10.0.0.23']
[('10.0.0.7', 5), ('10.0.0.23', 3), ('10.0.0.41', 1)]
```

- `zip(a, b)` pairs the items of two lists by position.
- `sorted` sorts text **character by character**, so `10.0.0.23` comes before `10.0.0.5`.
  Sort addresses as addresses with `ipaddress` (Command-Line Tools, below).
- `key=` names a function whose result is sorted on instead of the item: `len`, or a `lambda` (Functions and Modules, below) that picks a dictionary item's count.

## Nested loops

```python
for host in ["10.0.0.5", "10.0.0.7"]:
    for port in [22, 443]:
        print(host, port)
```
```
(.venv) $ python3 nested.py
10.0.0.5 22
10.0.0.5 443
10.0.0.7 22
10.0.0.7 443
```

The inner loop runs completely for each pass of the outer one: two hosts by two ports is four lines.

## Two names, one list

```python
a = [22, 443]
b = a
b.append(80)
print(a)
c = list(a)
c.append(8080)
print(a, c)
```
```
(.venv) $ python3 aliasing.py
[22, 443, 80]
[22, 443, 80] [22, 443, 80, 8080]
```

`b = a` does not copy the list: both names now refer to the **same** list, so a change through `b` shows through `a`.
`list(a)` makes a copy.

## Matching a value: `match`

```python
for action in ["ALLOW", "DENY", "DROP"]:
    match action:
        case "ALLOW":
            print(action, "let through")
        case "DENY" | "DROP":
            print(action, "blocked")
        case _:
            print(action, "unknown")
```
```
(.venv) $ python3 matching.py
ALLOW let through
DENY blocked
DROP blocked
```

`match` compares a value against each `case` in order.
`|` joins alternatives, and `case _` catches everything else.

## Common mistakes

```python
print(type({}), type(set()))
services = {22: "ssh"}
print(services[8080])
```
```
(.venv) $ python3 mistakes3.py
<class 'dict'> <class 'set'>
Traceback (most recent call last):
  File "/home/kali/session5/mistakes3.py", line 3, in <module>
    print(services[8080])
          ~~~~~~~~^^^^^^
KeyError: 8080
```

`{}` is an empty **dictionary**, so an empty set is written `set()`.
`services[8080]` raises `KeyError`, because the key is not there: use `services.get(8080, "unknown")`.

---

# Functions and Modules

A function gives a block of code a name, takes its input as parameters and hands back one value.
A module is a file of such functions that other scripts import, so a piece of work is written, tested and fixed in one place.

## Defining and calling functions

```python
def describe(host, port, label="unknown"):
    """Return one line naming the endpoint."""
    return f"{host}:{port} ({label})"


def split_endpoint(text):
    host, port = text.split(":")
    return host, int(port)


def no_return(port):
    print("checking", port)


print(describe("10.0.0.5", 22))
print(describe("10.0.0.5", 22, label="ssh"))
print(describe(port=443, host="10.0.0.7"))
print(split_endpoint("10.0.0.5:22"))
print(no_return(80))
help(describe)
```
```
(.venv) $ python3 funcs.py
10.0.0.5:22 (unknown)
10.0.0.5:22 (ssh)
10.0.0.7:443 (unknown)
('10.0.0.5', 22)
checking 80
None
Help on function describe in module __main__:

describe(host, port, label='unknown')
    Return one line naming the endpoint.
```

- A **default value**, `label="unknown"`, makes a parameter optional.
- A **keyword argument**, `port=443`, names the parameter, so the order no longer matters.
- `return host, int(port)` returns one tuple, which the caller can unpack.
- A function with no `return` returns `None`, which is what `print(no_return(80))` printed.
- `help(function)` shows its parameters and its **docstring**, the string on its first line.

## Modules and `import`

Any `.py` file is a **module**.
`netutil.py` holds two helpers and prints one line when it runs:

```python
"""netutil.py: two small helpers for host and port text."""

SERVICES = {22: "ssh", 443: "https"}


def service(port):
    """Return the service name for port, or "unknown"."""
    return SERVICES.get(port, "unknown")


def is_valid_port(port):
    """Return True when port is from 0 to 65535."""
    return 0 <= port <= 65535


print("netutil.py ran, __name__ is", __name__)
```
```
(.venv) $ python3 netutil.py
netutil.py ran, __name__ is __main__
```

```python
import netutil
from netutil import service
import netutil as nu
import sys

print(netutil.service(22), service(443), nu.is_valid_port(70000))
print(sys.path[0])
print([name for name in dir(netutil) if not name.startswith("_")])
```
```
(.venv) $ python3 imports.py
netutil.py ran, __name__ is netutil
ssh https False
/home/kali/session5
['SERVICES', 'is_valid_port', 'service']
```

- `import netutil` runs `netutil.py` **once**, however many times it is imported, and gives its names as `netutil.service`.
  Run directly, its `__name__` is `"__main__"`, and imported, it is `"netutil"`: the main guard, `if __name__ == "__main__":`, relies on exactly this.
- `from netutil import service` brings one name in directly.
- `import netutil as nu` gives the module a shorter name.
- `sys.path[0]` is the script's own folder, the first place Python looks for a module.

## Extra kinds of parameter, `lambda` and type hints

```python
def total(*ports):
    return len(ports), sum(ports)


def show(**fields):
    for key, value in fields.items():
        print(key, "=", value)


def is_valid_port(port: int) -> bool:
    return 0 <= port <= 65535


print(total(22, 80, 443))
show(host="10.0.0.5", port=22)
print(is_valid_port(443), is_valid_port.__annotations__)
by_length = sorted(["10.0.0.23", "10.0.0.5", "192.168.1.10"], key=lambda h: len(h))
print(by_length)
```
```
(.venv) $ python3 extras.py
(3, 545)
host = 10.0.0.5
port = 22
True {'port': <class 'int'>, 'return': <class 'bool'>}
['10.0.0.5', '10.0.0.23', '192.168.1.10']
```

- `*ports` collects any number of positional arguments into a tuple.
- `**fields` collects any number of keyword arguments into a dictionary.
- `port: int` and `-> bool` are **type hints**: they document the types and help VS Code check your code, but Python does not enforce them.
- `lambda h: len(h)` is a small function without a name, written where it is used, most often as a `key=`.

## Common mistakes

**A file named like a standard module hides that module.**
A file in your folder called `types.py` stopped `python3 -m venv` itself, and Python names the cause:

```
$ python3 -m venv .venv
<class 'int'> <class 'str'> <class 'float'>
<class 'bool'> <class 'NoneType'> <class 'bytes'>
Could not import runpy._run_module_as_main
Traceback (most recent call last):
  File "<frozen importlib._bootstrap>", line 1371, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1342, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 938, in _load_unlocked
  File "<frozen importlib._bootstrap>", line 1179, in exec_module
  File "<frozen runpy>", line 15, in <module>
  File "<frozen importlib._bootstrap>", line 1371, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1342, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 938, in _load_unlocked
  File "<frozen importlib._bootstrap>", line 1179, in exec_module
  File "<frozen importlib.util>", line 167, in <module>
AttributeError: module 'types' has no attribute 'ModuleType' (consider renaming '/home/kali/session5/types.py' since it has the same name as the standard library module named 'types' and prevents importing that standard library module)
```

The first two lines are the file's own output: `types.py` held two `print` lines, and Python ran it in place of the standard module.
The last line names the fix: rename your file.

---

# Files and Exceptions

A file is data that outlives the program, and real files contain lines a program cannot read.
An exception is how Python reports that something failed, and handling it is how a program skips the bad line instead of stopping.

## Opening a file: the modes

| Mode | Opens for | When the file exists | When it does not |
|---|---|---|---|
| `"r"` (the default) | reading text | reads it | `FileNotFoundError` |
| `"w"` | writing text | **empties it first** | creates it |
| `"a"` | appending text | adds at the end | creates it |
| `"rb"` | reading bytes | reads it | `FileNotFoundError` |
| `"wb"` | writing bytes | **empties it first** | creates it |

`with open(...) as f:` closes the file when the block ends, even after an error.
`encoding="utf-8"` names how the text is stored, and passing it makes your program read the same on every system.

## Reading

```python
with open("access.log", encoding="utf-8") as f:
    first = f.readline()
    rest = f.readlines()
print(repr(first))
print(len(rest), repr(rest[0]))
with open("access.log", encoding="utf-8") as f:
    for line in f:
        print(repr(line))
        break
with open("access.log", encoding="utf-8") as f:
    print(f.read().splitlines()[-1])
```
```
(.venv) $ python3 reading.py
'09:14:03 10.0.0.23 3389\n'
5 '09:14:41 10.0.0.7 443\n'
'09:14:03 10.0.0.23 3389\n'
09:16:30 10.0.0.41 22
```

- `readline()` reads one line, and `readlines()` the remaining lines as a list.
- `for line in f:` reads one line per pass, which works on files of any size.
- Each line keeps its `\n`, which `strip()` removes.
- `f.read().splitlines()` reads everything and splits it into lines without the `\n`.

## Writing and appending

```python
with open("notes.txt", "w", encoding="utf-8") as f:
    f.write("first\n")
    print("second", file=f)
with open("notes.txt", "a", encoding="utf-8") as f:
    print("third", file=f)
with open("notes.txt", encoding="utf-8") as f:
    print(f.read(), end="")
with open("notes.txt", "w", encoding="utf-8") as f:
    pass
with open("notes.txt", encoding="utf-8") as f:
    print(repr(f.read()))
```
```
(.venv) $ python3 writing.py
first
second
third
''
```

`write` takes text and adds no newline of its own, while `print(..., file=f)` writes a line as `print` would.
Opening with `"w"` emptied the file, even though nothing was written: `pass` is a statement that does nothing.

## Paths: `pathlib`

```python
from pathlib import Path

log = Path("access.log")
print(log.exists(), log.name, log.suffix, log.stat().st_size)
print(log.read_text(encoding="utf-8").splitlines()[0])
print(Path("missing.log").exists())
print(Path.home())
```
```
(.venv) $ python3 paths.py
True access.log .log 131
09:14:03 10.0.0.23 3389
False
/home/kali
```

A `Path` is a file's location as an object: it can say whether the file `exists()`, give its `name`, `suffix` and size, and read it in one call.

## `try`, `except`, `else` and `finally`

```python
for text in ["443", "ssh"]:
    try:
        port = int(text)
    except ValueError as err:
        print("skipped:", err)
    else:
        print("port", port)
    finally:
        print("done with", repr(text))
```
```
(.venv) $ python3 tryelse.py
port 443
done with '443'
skipped: invalid literal for int() with base 10: 'ssh'
done with 'ssh'
```

`else` runs only when the `try` block raised nothing, and `finally` runs every time, error or not.
`except ValueError as err` binds the exception, and `print(err)` shows its message.

## The exception tree

An `except` catches the class it names **and every class under it**:

```python
for kind in [FileNotFoundError, PermissionError, ValueError, KeyboardInterrupt]:
    print(kind.__name__, issubclass(kind, OSError), issubclass(kind, Exception))
```
```
(.venv) $ python3 family.py
FileNotFoundError True True
PermissionError True True
ValueError False True
KeyboardInterrupt False False
```

`except OSError` catches a missing file and a permission problem alike.
`KeyboardInterrupt`, Ctrl-C, is not under `Exception`, which is one reason a bare `except:` is never used: it would catch that too.

## Ending a program: `raise SystemExit` and `sys.exit()`

`sys.exit("message")` does exactly what `raise SystemExit("message")` does: it prints the message and ends with exit status 1.
`sys.exit(0)` ends with status 0, success.

```python
import sys

if len(sys.argv) < 2:
    sys.exit("usage: python3 exits.py <port>")
print("port", sys.argv[1])
sys.exit(0)
```
```
(.venv) $ python3 exits.py
usage: python3 exits.py <port>
(.venv) $ echo $?
1
(.venv) $ python3 exits.py 443
port 443
(.venv) $ echo $?
0
```

## Common mistakes

**Writing a number to a text file:**

```python
with open("out.txt", "w", encoding="utf-8") as f:
    f.write(443)
```
```
(.venv) $ python3 write443.py
Traceback (most recent call last):
  File "/home/kali/session5/write443.py", line 2, in <module>
    f.write(443)
    ~~~~~~~^^^^^
TypeError: write() argument must be str, not int
```

`write` takes only text: `f.write(str(443))`, or `print(443, file=f)`.

---

# Bytes and Binary Data

A `bytes` value is raw data, each item a number from 0 to 255, the form every file and every packet takes before it is read as text.
Binary files and network data are read this way, by position.

## Bytes, indexing and conversion

```python
data = b"ADR1" + bytes([3, 10, 0, 0, 5])
print(data, len(data))
print(data[4], data[0:4], data[4:5])
print(data.hex(" "), bytes.fromhex("0a 00 00 05"))
print("DENY".encode("ascii"), b"DENY".decode("ascii"))
print(repr(b"host \xc0\xa8".decode("ascii", errors="replace")))
```
```
(.venv) $ python3 bytesdemo.py
b'ADR1\x03\n\x00\x00\x05' 9
3 b'ADR1' b'\x03'
41 44 52 31 03 0a 00 00 05 b'\n\x00\x00\x05'
b'DENY' DENY
'host ��'
```

- Printed, `bytes` shows printable bytes as characters and the rest as `\x` codes: byte 10 is `\n`.
- `data[4]` is one byte as an **int**, and `data[0:4]` and `data[4:5]` are **bytes**.
- `.hex(" ")` shows every byte as two hex digits, and `bytes.fromhex` goes back.
- `encode` turns text into bytes and `decode` turns bytes into text.
  `errors="replace"` puts `�` in place of each byte that is not valid text, instead of stopping with an error.

## Joining, splitting and changing bytes

```python
parts = [b"10.0.0.5", b"10.0.0.7"]
print(b"\n".join(parts))
print(b"09:14:03 10.0.0.23 3389".split(b" "))
print(bytes(4))
buf = bytearray(b"ADR1")
buf[3] = ord("2")
buf.append(0)
print(buf, bytes(buf))
```
```
(.venv) $ python3 bytesmore.py
b'10.0.0.5\n10.0.0.7'
[b'09:14:03', b'10.0.0.23', b'3389']
b'\x00\x00\x00\x00'
bytearray(b'ADR2\x00') b'ADR2\x00'
```

- `b"".join` and `.split(b" ")` work as on text, with bytes on both sides.
- `bytes(4)` is four zero bytes.
- `bytes` cannot be changed, and a **`bytearray`** can: assign a byte by its index, or `append` one.
  `bytes(buf)` turns it back into `bytes`.

## Common mistakes

```python
print(b"ADR1" == "ADR1")
print(b"ADR1" + "2")
```
```
(.venv) $ python3 mistakes6.py
False
Traceback (most recent call last):
  File "/home/kali/session5/mistakes6.py", line 2, in <module>
    print(b"ADR1" + "2")
          ~~~~~~~~^~~~~
TypeError: can't concat str to bytes
```

`bytes` and `str` are never equal, even with the same letters, and cannot be joined.
Compare bytes with bytes, `b"ADR1"`, or `decode` first.

---

# Command-Line Tools

A tool takes its input from the command line instead of asking for it, so it can run inside a script or on a schedule.

## `sys.argv`

```python
import sys

print(sys.argv)
for name in sys.argv[1:]:
    print("would check", name)
```
```
(.venv) $ python3 argv.py 10.0.0.5 10.0.0.7
['argv.py', '10.0.0.5', '10.0.0.7']
would check 10.0.0.5
would check 10.0.0.7
```

`sys.argv` is a list of the words on the command line, the script's name first, so `sys.argv[1:]` is every argument after it.

## `argparse`

`argparse` builds the help page, the usage line and the error messages from a description of the arguments:

```python
"""scan_args.py: show what argparse builds from a description."""
import argparse


def main():
    parser = argparse.ArgumentParser(description="Show parsed arguments.")
    parser.add_argument("host", help="the host to check")
    parser.add_argument("ports", nargs="*", type=int, help="ports to check")
    parser.add_argument("--proto", choices=["tcp", "udp"], default="tcp",
                        help="the protocol (default: tcp)")
    parser.add_argument("--verbose", action="store_true", help="say more")
    parser.add_argument("--out", required=True, help="where to write")
    args = parser.parse_args()
    print(args)


if __name__ == "__main__":
    main()
```
```
(.venv) $ python3 scan_args.py -h
usage: scan_args.py [-h] [--proto {tcp,udp}] [--verbose] --out OUT
                    host [ports ...]

Show parsed arguments.

positional arguments:
  host               the host to check
  ports              ports to check

options:
  -h, --help         show this help message and exit
  --proto {tcp,udp}  the protocol (default: tcp)
  --verbose          say more
  --out OUT          where to write
```

| Argument | Means |
|---|---|
| `"host"` | a **positional** argument, required, taken by its place |
| `nargs="*"` | any number of values, perhaps none, as a list |
| `nargs="?"` | one value or none, then the `default` |
| `type=int` | the function that converts the text, rejecting values it cannot convert |
| `choices=[...]` | only these values are accepted |
| `default=` | the value when the option is not given (otherwise `None`) |
| `action="store_true"` | a flag that takes no value: `True` when given, `False` otherwise |
| `required=True` | an option that must be given |

`parse_args()` returns the values by name:

```
(.venv) $ python3 scan_args.py 10.0.0.5 22 443 --verbose --out report.txt
Namespace(host='10.0.0.5', ports=[22, 443], proto='tcp', verbose=True, out='report.txt')
(.venv) $ python3 scan_args.py 10.0.0.5 --out report.txt
Namespace(host='10.0.0.5', ports=[], proto='tcp', verbose=False, out='report.txt')
```

Every value argparse rejects ends the run with the usage line, one `error:` line and **exit status 2**:

```
(.venv) $ python3 scan_args.py 10.0.0.5 --proto icmp --out report.txt
usage: scan_args.py [-h] [--proto {tcp,udp}] [--verbose] --out OUT
                    host [ports ...]
scan_args.py: error: argument --proto: invalid choice: 'icmp' (choose from 'tcp', 'udp')
(.venv) $ echo $?
2
(.venv) $ python3 scan_args.py 10.0.0.5
usage: scan_args.py [-h] [--proto {tcp,udp}] [--verbose] --out OUT
                    host [ports ...]
scan_args.py: error: the following arguments are required: --out
(.venv) $ echo $?
2
```

## Addresses: `ipaddress`

```python
import ipaddress

a = ipaddress.ip_address("10.0.0.5")
b = ipaddress.ip_address("2001:0db8:0:0::1")
print(repr(a), a.version, str(a))
print(repr(b), b.version, str(b))
print(a == ipaddress.ip_address("10.0.0.5"), a < ipaddress.ip_address("10.0.0.23"))
print(ipaddress.ip_address("010.0.0.5"))
```
```
(.venv) $ python3 addr.py
IPv4Address('10.0.0.5') 4 10.0.0.5
IPv6Address('2001:db8::1') 6 2001:db8::1
True True
Traceback (most recent call last):
  File "/home/kali/session5/addr.py", line 8, in <module>
    print(ipaddress.ip_address("010.0.0.5"))
          ~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^
  File "/usr/lib/python3.14/ipaddress.py", line 54, in ip_address
    raise ValueError(f'{address!r} does not appear to be an IPv4 or IPv6 address')
ValueError: '010.0.0.5' does not appear to be an IPv4 or IPv6 address
```

- `ipaddress.ip_address` turns text into an `IPv4Address` or an `IPv6Address`, and `.version` says which.
- `str()` gives the address back in its standard form, so `2001:0db8:0:0::1` becomes `2001:db8::1`.
- Addresses compare as addresses, so `10.0.0.5` comes before `10.0.0.23`, unlike text.
- Text that is not an address raises `ValueError`, a leading zero included.
  Used as `type=ipaddress.ip_address` in argparse, that becomes an `error:` line and exit status 2.

---

# Shell Commands Used Here

| Command | Does |
|---|---|
| `echo $?` | prints the exit status of the command before it: `0` for success |
| `which name` | prints the file the shell runs for `name` |
| `chmod +x file` | gives a file the execute bit |
| `head -c N file` | prints the first `N` bytes of a file |
| `cat -A file` | prints a file with its invisible characters shown, `$` at each line's end |
| `diff a b` | prints the lines that differ, nothing when the files are the same |

```
(.venv) $ which python3 pip
/home/kali/session5/.venv/bin/python3
/home/kali/session5/.venv/bin/pip
(.venv) $ head -c 4 addrs.bin; echo
ADR1
(.venv) $ cat -A access.log
09:14:03 10.0.0.23 3389$
09:14:41 10.0.0.7 443$
09:15:10 10.0.0.41 ssh$
09:15:52 10.0.0.7 80$
09:16:00 10.0.0.12$
09:16:30 10.0.0.41 22$
```

`head -c 4` printed the 4-byte tag of `addrs.bin`, and `echo` added the newline the file does not have.

```
(.venv) $ cp access.log copy.log
(.venv) $ diff access.log copy.log && echo same
same
(.venv) $ echo '09:17:02 10.0.0.9 443' >> copy.log
(.venv) $ diff access.log copy.log
6a7
> 09:17:02 10.0.0.9 443
(.venv) $ echo $?
1
```

`6a7` means *after line 6 of the first file, add line 7 of the second*, and `>` marks a line only the second file has.
`diff` ends with status 0 when the files are the same and 1 when they differ, which is why `&& echo same` printed only the first time.
