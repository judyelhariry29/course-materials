# Module 0 · Session 5 — Troubleshooting & FAQ

## Python Essentials for Cybersecurity

### Professional Training in Cybersecurity I

---

> [!note] How to use this
> **Find the last line of the traceback, or the sentence you would say out loud**, not the exercise you were on.
> Errors are quoted exactly as Python or bash prints them, so you can search this page for the line in front of you.
> Each entry shows a small file that fails, its run, the **cause**, then the **fix**.
> Every run was recorded on Kali's Python 3.14, so your paths and the numbers in some messages may differ.
>
> If nothing here matches, note **the exact step, the exact command and everything it printed**, and ask in the Telegram group.

## Contents

- [The Python environment](#the-python-environment)
- [Running a script](#running-a-script)
- [Syntax errors](#syntax-errors)
- [Values and collections](#values-and-collections)
- [Functions and modules](#functions-and-modules)
- [Files and exceptions](#files-and-exceptions)
- [Bytes and text](#bytes-and-text)
- [Command-line arguments](#command-line-arguments)
- [The Home Task's starters](#the-home-tasks-starters)

---

# The Python environment

### `error: externally-managed-environment`

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

**Cause.**
Kali's own Python runs Kali's own tools, and Kali marks it as managed by `apt`, so `pip` refuses to install into it.
A package installed over one of Kali's could break a tool that depends on it.
Nothing was installed.

**Fix.**
Install into the project's own environment, created once and activated in each new terminal:

```bash
cd ~/session5
python3 -m venv .venv
source .venv/bin/activate
pip install requests
```

For a program you want to run as a command, not import, `pipx install` gives it an environment of its own.
Never add `--break-system-packages`: it switches off the very check that protects Kali's tools.

### My prompt has no `(.venv)` in front of it

**Cause.**
Activation belongs to one terminal.
`source .venv/bin/activate` puts `.venv/bin` first on that shell's `PATH` and adds `(.venv)` to its prompt, and a terminal opened afterwards starts without either.
Without it, `python3` and `pip` are Kali's, so `pip install` stops with the error above, and a package you installed in the environment is not there.

**Fix.**
Activate from the project folder, then check which `python3` runs:

```
$ which python3
/usr/bin/python3
$ source .venv/bin/activate
(.venv) $ which python3
/home/kali/session5/.venv/bin/python3
```

**In VS Code**, every new terminal activates `.venv` by itself, typing the `source` line for you.
The terminal that was already open when you created `.venv` stays as it was, so open a new one (**Terminal → New Terminal**) or activate by hand.

### VS Code shows a warning sign on my terminal's tab

**Cause.**
On the lab's Kali, the warning sign on the first terminal's tab came from the Python Debugger extension, asking to relaunch that terminal.
It has nothing to do with `.venv` or with your code.

**Fix.**
Hover over the sign to read its message.
It does not stop your scripts, so you can carry on in that terminal or open a new one.

---

# Running a script

### `bash: ./hello.py: Permission denied`

```python
#!/usr/bin/env python3
print("This script runs on its own.")
```

```
(.venv) $ ./hello.py
bash: ./hello.py: Permission denied
```

**Cause.**
`./hello.py` asks Linux to run the file as a program, and a file you have just created does not have the **execute bit**, the permission that allows that.

**Fix.**
Set the bit once, with `chmod +x`:

```
(.venv) $ chmod +x hello.py
(.venv) $ ./hello.py
This script runs on its own.
```

`python3 hello.py` never needs the bit, because then `python3` is the program and the file is only read.

### `./name.py` says `syntax error near unexpected token`

```python
print("scan done")
```

```
(.venv) $ ./noshebang.py
./noshebang.py: line 1: syntax error near unexpected token `"scan done"'
./noshebang.py: line 1: `print("scan done")'
```

**Cause.**
The file has the execute bit but no shebang line, so bash runs it as a shell script, and `print("scan done")` is not a shell command.
The message comes from bash, not from Python, which is the clue: a Python error would start with `Traceback` or `File`.

**Fix.**
Make `#!/usr/bin/env python3` the file's **first line**, above everything else, comments included, as `hello.py` above has it.

---

# Syntax errors

Python reads the whole file before it runs any of it.
A syntax error is found in that first reading, so not one line of the file runs, not even the lines above the mistake.

### `SyntaxError: '(' was never closed`

```python
print("start")
print("end"
```

```
(.venv) $ python3 syntax.py
  File "/home/kali/session5/syntax.py", line 2
    print("end"
         ^
SyntaxError: '(' was never closed
```

**Cause.**
The `(` on line 2 has no matching `)`.
`print("start")` on line 1 printed nothing, because the error was found before anything ran.

**Fix.**
Close the bracket: `print("end")`.
The caret points at the bracket that was opened, and the missing `)` belongs somewhere after it.

### `SyntaxError: expected ':'`

```python
port = 443
if port == 443
    print("https")
```

```
(.venv) $ python3 colon.py
  File "/home/kali/session5/colon.py", line 2
    if port == 443
                  ^
SyntaxError: expected ':'
```

**Cause.**
A line that opens a block ends with a colon, as `if`, `elif`, `else`, `for`, `while`, `def`, `try`, `except` and `with` lines do.

**Fix.**
Add the colon where the caret points: `if port == 443:`.

### `IndentationError: expected an indented block after 'if' statement on line 2`

```python
port = 443
if port == 443:
print("https")
```

```
(.venv) $ python3 indent.py
  File "/home/kali/session5/indent.py", line 3
    print("https")
    ^^^^^
IndentationError: expected an indented block after 'if' statement on line 2
```

**Cause.**
The block under an `if` is the indented lines below it, and line 3 is not indented, so the `if` has no block at all.

**Fix.**
Indent the block by four spaces:

```python
port = 443
if port == 443:
    print("https")
```

### `SyntaxError: invalid syntax. Maybe you meant '==' or ':=' instead of '='?`

```python
port = 443
if port = 443:
    print("https")
```

```
(.venv) $ python3 assign.py
  File "/home/kali/session5/assign.py", line 2
    if port = 443:
       ^^^^^^^^^^
SyntaxError: invalid syntax. Maybe you meant '==' or ':=' instead of '='?
```

**Cause.**
`=` stores a value in a name, and `==` compares two values.
An `if` needs a comparison.

**Fix.**
Use `==`: `if port == 443:`.
The message also offers `:=`, a different operator this session does not use.

---

# Values and collections

### `TypeError: can only concatenate str (not "int") to str`

```python
port = input("Port: ")
next_port = port + 1
print("Next port:", next_port)
```

```
(.venv) $ python3 add.py
Port: 443
Traceback (most recent call last):
  File "/home/kali/session5/add.py", line 2, in <module>
    next_port = port + 1
                ~~~~~^~~
TypeError: can only concatenate str (not "int") to str
```

**Cause.**
`input()` always returns text, even when you type digits, so `port` is the text `'443'`.
`+` on text joins text, and Python never converts a value by itself, so text and a number cannot be added.
The same message comes from joining text and a number directly:

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

**Fix.**
Convert the text to a number before the arithmetic, with `int(port) + 1`:

```
(.venv) $ python3 add_fixed.py
Port: 443
Next port: 444
```

To build text from a number, use an f-string, `f"Port {443}"`, or convert the number with `str(443)`.

### `ValueError: invalid literal for int() with base 10: 'http'`

```python
print("start")
port = int("http")
print("end")
```

```
(.venv) $ python3 runtime.py
start
Traceback (most recent call last):
  File "/home/kali/session5/runtime.py", line 2, in <module>
    port = int("http")
ValueError: invalid literal for int() with base 10: 'http'
```

**Cause.**
`int()` converts only text that is a whole number, and the last line quotes the text it was given.
`start` printed first: unlike a syntax error, an error raised while running stops the script at the failing line, after the lines above it have run.
The same message, with `'rdp'`, comes from `int(input(...))` when you type a word at the prompt.

**Fix.**
Give `int()` digits only.
When the text comes from outside the program, typed in or read from a file, expect some of it to be bad, and catch the `ValueError`:

```python
try:
    port = int(text)
except ValueError:
    print("Not a port:", text)
```

### `ValueError: Unknown format code 'x' for object of type 'str'`

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

**Cause.**
`x` formats a **number** in hexadecimal, and `port` holds the text `"443"`.

**Fix.**
Convert first: `f"{int(port):#06x}"` prints `0x01bb`.

### `IndexError: list index out of range`

```python
ports = [22, 80, 443]
print(ports[0])
print(ports[3])
```

```
(.venv) $ python3 index.py
22
Traceback (most recent call last):
  File "/home/kali/session5/index.py", line 3, in <module>
    print(ports[3])
          ~~~~~^^^
IndexError: list index out of range
```

**Cause.**
Indexes count from 0, so a list of three items has indexes 0, 1 and 2, and `ports[3]` is past the end.
`22` printed first, from line 2.

**Fix.**
The last item is `ports[2]`, or `ports[-1]` whatever the length.
To visit every item, loop over the list itself, `for port in ports:`, and no index can go past the end.
The same error from `sys.argv[1]` has its own entry, under *Command-line arguments*.

### `KeyError: 8080`

```python
SERVICES = {22: "ssh", 80: "http", 443: "https"}
print(SERVICES[443])
print(SERVICES[8080])
```

```
(.venv) $ python3 key.py
https
Traceback (most recent call last):
  File "/home/kali/session5/key.py", line 3, in <module>
    print(SERVICES[8080])
          ~~~~~~~~^^^^^^
KeyError: 8080
```

**Cause.**
`8080` is not a key of the dictionary.
The last line of a `KeyError` is the missing key itself, not a sentence.

**Fix.**
Use `.get` with a default, `SERVICES.get(8080, "unknown")`, or test first with `if 8080 in SERVICES:`.

### My loop printed one host fewer than I wanted

```python
for i in range(1, 4):
    print(f"10.0.0.{i}")
```

```
(.venv) $ python3 short.py
10.0.0.1
10.0.0.2
10.0.0.3
```

**Cause.**
`range(1, 4)` counts from 1 up to, **but not including**, 4.
Nothing is raised, so the only sign is the count.

**Fix.**
The end is one past the last number you want: `range(1, 5)` gives 1, 2, 3 and 4.

### `AttributeError: 'dict' object has no attribute 'add'`

```python
seen = {}
print(type(seen))
seen.add("10.0.0.7")
```

```
(.venv) $ python3 emptyset.py
<class 'dict'>
Traceback (most recent call last):
  File "/home/kali/session5/emptyset.py", line 3, in <module>
    seen.add("10.0.0.7")
    ^^^^^^^^
AttributeError: 'dict' object has no attribute 'add'
```

**Cause.**
`{}` is an empty **dictionary**, not an empty set, and a dictionary has no `add`.

**Fix.**
Write an empty set as `set()`: `seen = set()`.

---

# Functions and modules

### `TypeError: parse() missing 1 required positional argument: 'line'`

```python
def parse(line):
    host, text = line.split(":")
    return host, int(text)


host, port = parse()
```

```
(.venv) $ python3 noarg.py
Traceback (most recent call last):
  File "/home/kali/session5/noarg.py", line 6, in <module>
    host, port = parse()
                 ~~~~~^^
TypeError: parse() missing 1 required positional argument: 'line'
```

**Cause.**
`parse` has one parameter, `line`, and the call passes nothing for it.

**Fix.**
Pass one argument for each parameter: `host, port = parse("10.0.0.7:443")`.

### My function's result is `None`

```python
def address(n):
    print(f"10.0.0.{n}")


host = address(7)
print("host is", host)
```

```
(.venv) $ python3 noreturn.py
10.0.0.7
host is None
```

**Cause.**
`print` shows a value on the screen, and `return` hands it back to the caller.
A function that never reaches a `return` gives back `None`, so `host` is `None`, and nothing is raised.

**Fix.**
Return the value, and print it where the function is called:

```python
def address(n):
    return f"10.0.0.{n}"
```

### I get `<function address at 0x...>` instead of a value

```python
def address(n):
    return f"10.0.0.{n}"


print(address)
```

```
(.venv) $ python3 noparens.py
<function address at 0x721b377a7530>
```

**Cause.**
A function's name without parentheses is the function itself, not a call, so `print` shows the function.
The number after `at` changes on every run.

**Fix.**
Call it, with its argument: `print(address(7))`.

### `NameError: name 'host' is not defined`

```python
def parse(line):
    host, text = line.split(":")
    return host, int(text)


parse("10.0.0.7:443")
print(host)
```

```
(.venv) $ python3 local.py
Traceback (most recent call last):
  File "/home/kali/session5/local.py", line 7, in <module>
    print(host)
          ^^^^
NameError: name 'host' is not defined
```

**Cause.**
A name given a value inside a function exists only while the function runs.
`parse` returned the host and the port, and the call threw them away.

**Fix.**
Keep what the function returns: `host, port = parse("10.0.0.7:443")`.
A `NameError` from a misspelled name ends with a suggestion instead, such as `Did you mean: 'port'?`, under *Files and exceptions*.

### `python3 -m venv` printed my own file's output, then `consider renaming`

A file in `~/session5` named `types.py`:

```python
print(type(443), type("443"), type(4.5))
print(type(True), type(None), type(b"443"))
```

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
$ echo $?
1
```

**Cause.**
`types` is also the name of a module in Python's own library, and Python looks in your folder before its library.
So it imported your file in its place: its two `print` lines ran, and then the code that needed the real module failed.
Any file named like a standard module hides that module from every import made in that folder.
On Kali's Python, `string.py` and `argparse.py` break `python3 -m venv` the same way, while `random.py` or `socket.py` breaks only a script of yours that imports that module.

**Fix.**
Rename your file, as the last line says:

```
$ mv types.py kinds.py
$ python3 -m venv .venv
$ echo $?
0
```

---

# Files and exceptions

### `io.UnsupportedOperation: not readable`, and my file is now empty

```python
with open("conns.txt", "w") as f:
    for line in f:
        print(line.strip())
```

```
(.venv) $ python3 wipe.py
Traceback (most recent call last):
  File "/home/kali/session5/wipe.py", line 2, in <module>
    for line in f:
                ^
io.UnsupportedOperation: not readable
(.venv) $ wc -c conns.txt
0 conns.txt
(.venv) $ python3 read.py
```

**Cause.**
`"w"` opens a file for **writing**, and empties it the moment it opens.
The loop then asked to read a file that was opened only for writing.
The error arrives after the damage: `conns.txt` is 0 bytes, so a correct script run afterwards prints nothing.

**Fix.**
Open a file you read with `"r"`, the default: `open("conns.txt")`.
Then put the emptied file back: for the guide's files, `python3 make_samples.py` writes them again.

### Every line is reported bad, but nothing is raised

```python
text = "443"
try:
    port = int(text)
    print("Using port", prt)
except Exception:
    print("Not a port:", text)
```

```
(.venv) $ python3 broad.py
Not a port: 443
```

**Cause.**
`except Exception` catches every kind of error, including the `NameError` from the misspelled `prt` on line 4.
The `try` hides a mistake in your own code behind the message meant for bad input, and `443` is reported as not a port.

**Fix.**
Name the exception you expect, `except ValueError:`.
The typo then stops the script with its own traceback, which points at it:

```
(.venv) $ python3 narrow.py
Traceback (most recent call last):
  File "/home/kali/session5/narrow.py", line 4, in <module>
    print("Using port", prt)
                        ^^^
NameError: name 'prt' is not defined. Did you mean: 'port'?
```

Never write a bare `except:`, which also catches Ctrl+C.

### `FileNotFoundError: [Errno 2] No such file or directory: 'conns.txt'`

```python
with open("conns.txt") as f:
    for line in f:
        print(line.strip())
```

```
(.venv) $ cd /tmp
(.venv) $ python3 ~/session5/read.py
Traceback (most recent call last):
  File "/home/kali/session5/read.py", line 1, in <module>
    with open("conns.txt") as f:
         ~~~~^^^^^^^^^^^^^
FileNotFoundError: [Errno 2] No such file or directory: 'conns.txt'
(.venv) $ echo $?
1
```

**Cause.**
A file name without a folder, such as `conns.txt`, is looked up in the folder you are **in**, not in the folder the script is in.

**Fix.**
Change to the folder that holds the file first, `cd ~/session5`, and run the script from there.
A program that catches this error and ends with its own message, such as `access.log not found`, has the same cause and the same fix.

### `TypeError: write() argument must be str, not int`

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

**Cause.**
`write` on a text file takes only text.

**Fix.**
Convert the number, and add the line ending yourself, since `write` adds none: `f.write(f"{443}\n")`.
`print(443, file=f)` converts and adds the line ending for you.

---

# Bytes and text

### `TypeError: a bytes-like object is required, not 'str'`

```python
with open("hosts.bin", "wb") as f:
    f.write("10.0.0.7")
```

```
(.venv) $ python3 wbstr.py
Traceback (most recent call last):
  File "/home/kali/session5/wbstr.py", line 2, in <module>
    f.write("10.0.0.7")
    ~~~~~~~^^^^^^^^^^^^
TypeError: a bytes-like object is required, not 'str'
(.venv) $ wc -c hosts.bin
0 hosts.bin
```

**Cause.**
A file opened `"wb"` takes only bytes, and `"10.0.0.7"` is text.
The file was created, empty, before the error.

**Fix.**
Write bytes.
For an address stored as four bytes, `f.write(bytes([10, 0, 0, 7]))`.
For text you mean to store as text, `f.write("10.0.0.7".encode())`.

### `can only concatenate str (not "bytes") to str`, or `can't concat str to bytes`

```python
print("10" + b"10")
```

```
(.venv) $ python3 strbytes.py
Traceback (most recent call last):
  File "/home/kali/session5/strbytes.py", line 1, in <module>
    print("10" + b"10")
          ~~~~~^~~~~~~
TypeError: can only concatenate str (not "bytes") to str
```

```python
print(b"ADR1" == "ADR1")
print(b"ADR1" + "2")
```

```
(.venv) $ python3 bytesstr.py
False
Traceback (most recent call last):
  File "/home/kali/session5/bytesstr.py", line 2, in <module>
    print(b"ADR1" + "2")
          ~~~~~~~~^~~~~
TypeError: can't concat str to bytes
```

**Cause.**
Text and bytes never mix, and the message depends on which comes first.
The first line of `bytesstr.py` shows the quiet side of the same rule: bytes never equal text, even with the same letters.

**Fix.**
Make both sides the same type: `decode` the bytes into text, or `encode` the text into bytes.
For example, `"10" + b"10".decode()` is the text `'1010'`.

### My comparison with bytes is always `False`

```python
with open("conns.txt", "rb") as f:
    data = f.read()
if data[0] == b"1":
    print("starts with 1")
else:
    print("no match")
```

```
(.venv) $ python3 first.py
no match
```

**Cause.**
Indexing a bytes object gives one **number**: `data[0]` is 49, the byte for the character `1`.
A number never equals a bytes object, so the test is `False`, and nothing is raised.

**Fix.**
Slice instead of indexing, since a slice of bytes is bytes: `if data[0:1] == b"1":`.

```
(.venv) $ python3 sliced.py
starts with 1
```

---

# Command-line arguments

### `IndexError: list index out of range` on `sys.argv[1]`

```python
import sys

print("Reading", sys.argv[1])
```

```
(.venv) $ python3 argone.py
Traceback (most recent call last):
  File "/home/kali/session5/argone.py", line 3, in <module>
    print("Reading", sys.argv[1])
                     ~~~~~~~~^^^
IndexError: list index out of range
```

**Cause.**
`sys.argv[0]` is the script's own name, so when you give no arguments the list has one item, and `sys.argv[1]` does not exist.

**Fix.**
Check the length first and end with a usage line:

```python
if len(sys.argv) < 2:
    raise SystemExit("usage: python3 argone.py FILE")
```

`argparse` writes this check, and its message, for you.

### My `sys.argv[1] == 443` is never true

```python
import sys

if sys.argv[1] == 443:
    print("HTTPS")
else:
    print("not 443")
```

```
(.venv) $ python3 compare.py 443
not 443
```

**Cause.**
Every command-line argument is text, so `sys.argv[1]` is `'443'`, and text never equals a number.
Nothing is raised.

**Fix.**
Convert first: `if int(sys.argv[1]) == 443:`.

```
(.venv) $ python3 fixed.py 443
HTTPS
```

With `argparse`, `type=int` converts the argument for you.

### My script printed its own source code

```python
import sys

with open(sys.argv[0]) as f:
    print(f.read())
```

```
(.venv) $ python3 zero.py conns.txt
import sys

with open(sys.argv[0]) as f:
    print(f.read())

```

**Cause.**
`sys.argv[0]` is the script's name, so the script opened and printed itself.

**Fix.**
The first argument after the script is `sys.argv[1]`: `open(sys.argv[1])`.

### `error: the following arguments are required: file`, though I gave it a default

```python
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("file", default="conns.txt")
args = parser.parse_args()
print("Reading", args.file)
```

```
(.venv) $ python3 nodefault.py
usage: nodefault.py [-h] file
nodefault.py: error: the following arguments are required: file
(.venv) $ echo $?
2
```

**Cause.**
A positional argument is required, so its `default=` is never used.
Exit status 2 is how `argparse` reports wrong usage.

**Fix.**
Add `nargs="?"`, which makes the positional argument optional, so the default applies when it is left out:

```python
parser.add_argument("file", nargs="?", default="conns.txt")
```

```
(.venv) $ python3 optional.py
Reading conns.txt
```

When the argument has no default, the message means what it says: give the argument.

### `error: argument --port: invalid int value`, or `invalid ip_address value`

```python
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("file", nargs="?",
                    default="conns.txt")
parser.add_argument("--port", type=int, default=443,
                    help="port to look for")
args = parser.parse_args()
print(args.file, args.port, type(args.port))
```

```
(.venv) $ python3 options.py --port http
usage: options.py [-h] [--port PORT] [file]
options.py: error: argument --port: invalid int value: 'http'
(.venv) $ echo $?
2
```

```python
import argparse
import ipaddress

parser = argparse.ArgumentParser()
parser.add_argument("host", type=ipaddress.ip_address)
args = parser.parse_args()
print(args.host, args.host.version)
```

```
(.venv) $ python3 check.py 10.0.0.256
usage: check.py [-h] host
check.py: error: argument host: invalid ip_address value: '10.0.0.256'
(.venv) $ echo $?
2
(.venv) $ python3 check.py 010.0.0.7
usage: check.py [-h] host
check.py: error: argument host: invalid ip_address value: '010.0.0.7'
```

**Cause.**
`argparse` converts each argument with its `type=` inside `parse_args()`, before any line after that call runs.
A value that does not convert ends the run with the usage line, one `error:` line and exit status 2.
`ip_address` rejects `10.0.0.256`, since an IPv4 address part runs from 0 to 255, and also rejects a leading zero, as in `010.0.0.7`.

**Fix.**
Nothing in the code is wrong.
Run it again with a value of the right kind, such as `--port 443` or `10.0.0.7`.

---

# The Home Task's starters

### `AttributeError: 'Namespace' object has no attribute 'watchlist'`

```
(.venv) $ python3 watchlist.py connections.log
Traceback (most recent call last):
  File "/home/kali/session5/watchlist.py", line 44, in <module>
    main()
    ~~~~^^
  File "/home/kali/session5/watchlist.py", line 17, in main
    watched = watchlib.read_watchlist(args.watchlist)
                                      ^^^^^^^^^^^^^^
AttributeError: 'Namespace' object has no attribute 'watchlist'
(.venv) $ echo $?
1
```

**Cause.**
This is `watchlist.py` as it was handed out.
`args` holds only the arguments the parser declares, and the two options are declared in TODO 4, which is not done yet.

**Fix.**
Complete TODO 4.
`./watchlist.py -h` then lists `--watchlist` and `--out`, as the Home Task shows.

### My checker says `0 watched, 0 matches, 10 skipped`

```
(.venv) $ python3 watchlist.py connections.log
0 watched, 0 matches, 10 skipped
report written to report.txt
(.venv) $ echo $?
0
(.venv) $ cat report.txt
Watchlist report for connections.log
Connections per watched host:
```

**Cause.**
`watchlist.py` is complete, and `watchlib.py` is still as it was handed out.
Until TODO 2 is done, `read_watchlist` returns an empty set, and until TODO 3 is done, `parse_line` raises a `ValueError` for every line, which `watchlist.py` counts as skipped.
Nothing failed, so the exit status is 0.

**Fix.**
Complete TODOs 1 to 3 in `watchlib.py`.
The finished tool reports `3 watched, 4 matches, 4 skipped`.
