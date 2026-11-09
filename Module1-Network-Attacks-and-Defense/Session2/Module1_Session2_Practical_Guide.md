# Module 1 · Session 2 — Practical Guide

## The Python Networking Stack

### Professional Training in Cybersecurity I

---

## Overview

Every network tool in this course is a program that holds a socket.
This lab opens sockets on two real machines and makes them carry bytes, then makes them fail, and then makes them survive what a real network does to them.
Your Kali machine runs the clients, and the Ubuntu server you built in Module 0 is the **peer** that runs the servers.
In this practical session, you will:

1. Check that Kali and the peer reach each other, and give the peer a folder for this session
2. Write a **TCP server and client** across the two machines, and read the live connection with `ss`
3. Put back the **message boundaries** a stream drops, with a length prefix
4. Tell a **refused** connection from a **timed-out** one, with a deadline on every attempt
5. Wrap the client in **TLS**, with both certificate checks on, and see each check fail
6. Serve several clients at once with **threads**, and protect a shared value with a **lock**
7. Build an **ICMP echo request** by hand and send it over a **raw socket**
8. Solve **CTF Challenge 1**: read a stream that arrives in pieces, record by record
9. Document everything in your Practical Guide Submission

**Primary lab environment:** Kali Linux VM and the Ubuntu server VM on the CyberLab network, VS Code, Python virtual environment.

> [!note] Two sittings
> This session is delivered over **two sittings**.
> **The first sitting** covers Exercises 1, 2 and 3, and Exercises 6 and 7 if you choose them.
> **The second sitting** covers Exercises 4, 5 and 9, Exercise 8 if you choose it, and the CTF.
> The exercise table below gives each exercise's sitting.

> [!warning] Your own lab only
> Every command in this guide points at **your own peer** on the CyberLab network, or at your own Kali machine.
> Exercise 3 adds a firewall rule to the peer and removes it again, and Exercise 9 sends packets over a raw socket.
> Never point either at a machine that is not yours.

> [!example] 📝 Submission
> Work in **Module1_Session2_Practical_Guide_Submission.md** throughout: paste your code, terminal output, and answers into its slots as you go.
> Guided exercises give you a starter with `# TODO` gaps **in this guide**.
> Copy it out, complete it in your IDE, and paste your finished code into the Submission.
> From-scratch exercises leave the slot empty for your own solution.

> [!important] You must complete
> Exercises 1 to 5 + **at least one** choice exercise (6–8) + Exercise 9 + CTF Challenge 1.

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
ls Module1-Network-Attacks-and-Defense/Session2
```

**Checkpoint:** `ls` lists `Module1_Session2_Practical_Guide.md`, `Module1_Session2_Home_Task.md`, the two `_Submission.md` worksheets and `screenshots`.
In Obsidian, open the Practical Guide worksheet, then right-click **Module1_Session2_Practical_Guide.md** and choose **Open to the right**, so this guide sits beside it.

> [!important] Fill in the worksheets only
> Never edit, move or delete the guide or the Home Task in your repository.
> Your instructor's fixes arrive in them through `git pull`, and a changed copy stops that pull.

## Step 2: A working folder for your code

> [!note] Why the code lives outside your repository
> Your repository holds what you hand in: the worksheets and their screenshots.
> The scripts you write today and this session's virtual environment live in a folder of their own, at the same path the session has in your repository, under `~/cyberlabs`.
> Your code reaches your instructor by being pasted into the worksheet.

1. **Create the folder and open it in VS Code:**

   ```bash
   mkdir -p ~/cyberlabs/Module1-Network-Attacks-and-Defense/Session2
   code ~/cyberlabs/Module1-Network-Attacks-and-Defense/Session2
   ```

2. **Trust the folder.**
   The first time VS Code opens it, a window asks *Do you trust the authors of the files in this folder?*
   You made the folder yourself, so click **Yes, I trust the authors**.
3. **Open the built-in terminal** with **Terminal**, then **New Terminal**.
   Its prompt ends in `~/cyberlabs/Module1-Network-Attacks-and-Defense/Session2`.
   **Run every Kali command in this guide in this terminal**, unless a step says otherwise.

## Step 3: This session's virtual environment

Every session gets a virtual environment of its own, inside its working folder, so what one session installs never reaches another.
Create it and activate it in the built-in terminal:

```bash
python3 -m venv .venv
source .venv/bin/activate
which python3   # should end in Session2/.venv/bin/python3
```

Your prompt now starts with `(.venv)`.
Every new terminal you open in this folder activates it by itself, because VS Code finds `.venv` and runs the same `source` line for you.

Everything this session uses is in the Python **standard library**: `socket`, `ssl`, `struct`, `threading` and `selectors`.
There is nothing to install.

Each code block in this guide begins with a **tag line**, a comment that names the file to save the block as:

- `@starter` marks a starter for a guided exercise: copy it out, complete its `# TODO`s in the editor, and keep the finished version for your Submission.
- `@generator` marks a command or program that writes the files an exercise uses: run it as given.
- `@infra` marks any other complete program you save and run as given.

The tag is a comment, so Python ignores it: copy the whole block, tag included.

## Step 4: Check the lab

This session runs on **two machines**, the two you built in Module 0: Kali, where you sit, and the Ubuntu server, the **peer**.
Start both virtual machines, then find each one's address on the CyberLab network.

1. **On Kali**, in the built-in terminal:

   ```bash
   ip -br -4 addr
   ```

   The line for `eth0` shows Kali's address, for example `10.0.2.15/24`.
   The part before the `/` is the address.

2. **Open a second terminal on the peer.**
   In VS Code, click **+** in the terminal panel, then connect with the SSH entry you made in Module 0:

   ```bash
   ssh lab
   ip -br -4 addr
   python3 --version
   ```

   The line that is not `lo` shows the peer's address, for example `10.0.2.6/24`.
   `python3 --version` prints `Python 3.12` or newer.
   This terminal stays connected to the peer for the rest of the session.

3. **Back on Kali**, check the version there too, and that the peer answers:

   ```bash
   python3 --version
   ping -c 3 PEER_ADDRESS
   ```

   Replace `PEER_ADDRESS` with the peer's address from step 2.
   `ping` reports `3 received`.

**Checkpoint:** you have written down two addresses, Kali's and the peer's, and `ping` from Kali reaches the peer.
Wherever a command in this guide says `PEER_ADDRESS`, type the peer's address.

> [!tip] How this guide shows a terminal
> The transcripts shorten Kali's prompt to `(.venv) $`, and the peer's to `peer $`.
> They were recorded on a lab where Kali is `192.168.56.107` and the peer is `192.168.56.1`, so those addresses appear in them.
> Your addresses are on CyberLab, `10.0.2.x`, and your ephemeral ports differ too.
> Everything else in a transcript is what your run prints.

## Step 5: A folder on the peer

The servers in this session run on the peer, so the peer needs a folder for them.
In the **peer terminal**:

```bash
mkdir -p ~/Session2
cd ~/Session2
```

You write every script on Kali, in VS Code.
A script that runs on the peer is copied there from the **Kali terminal** with `scp`, using the same `lab` entry:

```bash
scp tcp_server.py lab:Session2/
```

Copy a server again every time you change it on Kali.
A server keeps its terminal busy until you stop it with **Ctrl+C**.

---

# Exercises

---

| Exercise | Status | Sitting | Type | Difficulty |
|----------|--------|---------|------|------------|
| Exercise 1: A TCP Server and Client on Two Machines | **Required** | 1 | Guided (starter in guide) | ⭐ Easy |
| Exercise 2: Restoring Message Boundaries with a Length Prefix | **Required** | 1 | Guided (starter in guide) | ⭐⭐ Medium |
| Exercise 3: Refused, Timed Out or Open: One Connection Attempt | **Required** | 1 | Guided (starter in guide) | ⭐⭐ Medium |
| Exercise 4: Wrapping the Client in TLS | **Required** | 2 | Guided (starter in guide) | ⭐⭐ Medium |
| Exercise 5: One Thread per Client, and the Lock It Needs | **Required** | 2 | Guided (starter in guide) | ⭐⭐ Medium |
| Exercise 6: Datagrams Keep Their Boundaries | **Choose ≥1** | 1 | From Scratch | ⭐ Easy |
| Exercise 7: A Restart That Cannot Bind | **Choose ≥1** | 1 | From Scratch | ⭐ Easy |
| Exercise 8: One Selector Loop Serves Many Clients | **Choose ≥1** | 2 | From Scratch | ⭐⭐⭐ Hard |
| Exercise 9: An ICMP Echo Request over a Raw Socket | **Required** | 2 | Guided (starter in guide) | ⭐⭐⭐ Hard |

---

# Required Exercises

---

## Exercise 1: A TCP Server and Client on Two Machines — REQUIRED

> **🧩 GUIDED: complete the starters below** | Difficulty: ⭐ Easy
> *Save the two starters as `tcp_server.py` and `tcp_client.py`, fill their `# TODO` gaps, run the server on the peer and the client on Kali, then read the connection with `ss`.*

> [!note] Concept note
> A **socket** is an endpoint the kernel keeps for one program, and a TCP connection joins two of them.
> The two sides do not run the same calls.
> The **server** claims an address with `bind`, declares that it accepts connections with `listen`, and waits in `accept`.
> The **client** only calls `connect`.
> `accept` does not turn the listening socket into the connection: it returns **a new socket** for that one client, and the listener stays as it was, ready for the next.
> Five values identify the connection: the protocol, and the address and port at each end.
> The client's port is an **ephemeral port**, an unused one the kernel picks for it.
> `ss` lists the sockets on a machine while they are open, so you can read those five values on both machines.

Complete the three TODOs of **the server, which runs on the peer**:

```python
# @starter tcp_server.py
"""tcp_server.py: accept one TCP client, answer its message, and wait for it to close"""
import socket
import sys

PORT = 8080

if len(sys.argv) != 2:
    sys.exit("usage: python3 tcp_server.py BIND_ADDRESS")
bind_address = sys.argv[1]

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listener:
    # TODO 1: bind the listener to the address pair (bind_address, PORT).
    # TODO 2: put the listener in the listening state with listen().
    print("listening on", listener.getsockname())

    # TODO 3: wait for one client with accept(). It returns a new connected socket
    #   and the client's address: store them in conn and client_address.
    conn, client_address = None, None
    with conn:
        print("accepted", client_address)
        print("listener fd", listener.fileno(), "connection fd", conn.fileno())
        request = conn.recv(1024)
        print("server got", request)
        conn.sendall(b"OK")
        while conn.recv(1024):
            pass
        print("the client closed the connection")
```

Complete the TODO of **the client, which runs on Kali**:

```python
# @starter tcp_client.py
"""tcp_client.py: connect to the peer's server, send one message, and hold the connection open"""
import socket
import sys

PORT = 8080

if len(sys.argv) != 2:
    sys.exit("usage: python3 tcp_client.py PEER_ADDRESS")
peer_address = sys.argv[1]

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    # TODO 1: connect client_socket to the server, at (peer_address, PORT).
    print("connected from", client_socket.getsockname(), "to", client_socket.getpeername())
    client_socket.sendall(b"hello")
    print("client got", client_socket.recv(1024))
    input("connection open: read it with ss, then press Enter to close ")
```

**Run it.**

1. **On Kali**, check both addresses for your Submission, then copy the server to the peer:

   ```bash
   ip -br -4 addr
   ssh lab ip -br -4 addr
   scp tcp_server.py lab:Session2/
   ```

2. **On the peer**, start the server on the peer's own address:

   ```bash
   python3 tcp_server.py PEER_ADDRESS
   ```

3. **On Kali**, start the client:

   ```bash
   python3 tcp_client.py PEER_ADDRESS
   ```

   It prints the two endpoints of its connection, then `client got b'OK'`, and then waits with the connection open.

4. **Read the open connection.**
   Open a third terminal on Kali with **+**, and run:

   ```bash
   ss -tnp state established dst PEER_ADDRESS:8080
   ssh lab "ss -tnp state established sport = :8080"
   ```

   The first line lists the connection as Kali sees it, and the second as the peer sees it.

5. **Close it.**
   Press **Enter** in the client's terminal.
   The server prints `the client closed the connection` and exits.

6. **Bind to loopback instead.**
   On the peer, start the server again on `127.0.0.1`, and run the same client on Kali:

   ```bash
   python3 tcp_server.py 127.0.0.1
   ```

   ```bash
   python3 tcp_client.py PEER_ADDRESS
   ssh lab "ss -tln sport = :8080"
   ```

   The client fails, and the traceback's last line names the error.
   Stop the server on the peer with **Ctrl+C**.

**Answer from your run** (paste each into the Submission):

1. Your Kali `ss` line lists one connection.
   - **1a.** What is Kali's end of it, the local address and port?
   - **1b.** What is the peer's end, the address and port it reached?
2. The server printed two file descriptors.
   - **2a.** Which number does the listener hold?
   - **2b.** Which number does the connected socket that `accept` returned hold?
3. The loopback run failed.
   - **3a.** What is the last line of the client's traceback?
   - **3b.** Which local address and port does the peer's `ss -tln` line show for the listener?

> [!example] 📝 Submission
> Paste your completed `tcp_server.py` and `tcp_client.py`, both `ip` lines, the server's and client's output, both `ss` lines, the loopback run, and a screenshot of the open connection, then answer the Exercise 1 questions.

---

## Exercise 2: Restoring Message Boundaries with a Length Prefix — REQUIRED

> **🧩 GUIDED: complete the starter below** | Difficulty: ⭐⭐ Medium
> *Run the given server on the peer and the given one-`recv` client, then complete `framed_client.py` until it reads every message whole.*

> [!note] Concept note
> A stream socket carries **bytes, not messages**.
> Three `send` calls become one run of bytes, and nothing on the wire records where one ended and the next began.
> `recv(1024)` returns **whatever has arrived so far**, up to 1024 bytes, so a message can arrive in pieces, or two messages in one piece.
> The fix is to put the boundary into the bytes: a **length prefix**, a fixed-size number in front of every message that says how many bytes follow.
> Here the prefix is 4 bytes, big-endian, packed with `struct.pack("!I", n)`.
> The receiver reads in two steps, exactly 4 bytes and then exactly `n` bytes, and each step **loops**, because one `recv` can return fewer bytes than asked.
> `recv` returns empty bytes, `b''`, **only when the peer has closed** its side, so a receive loop ends on `b''`, never on a short read.
> On the sending side, `sendall` keeps sending until every byte is gone.
> The prefix counts **encoded bytes**, never characters.

**The given server, which runs on the peer.**
It sends three messages, three bytes at a time with a pause between the pieces, then reads one message back:

```python
# @infra framed_server.py
# @expect run on the peer: prints "listening on" and its address with port 8081, sends each client 'LOGIN alice', 'café' and 'QUIT' as length-prefixed messages in 3-byte pieces, and prints "client said 'BYE'" when framed_client.py runs
"""framed_server.py: send three length-prefixed messages in small pieces, then read one back"""
import socket
import struct
import sys
import time

PORT = 8081
MESSAGES = ["LOGIN alice", "café", "QUIT"]


def send_in_pieces(conn, data):
    # Three bytes at a time with a pause between them, so no single recv
    # on the other side can see a whole message.
    for start in range(0, len(data), 3):
        conn.sendall(data[start:start + 3])
        time.sleep(0.05)


def recv_exact(conn, count):
    data = b""
    while len(data) < count:
        chunk = conn.recv(count - len(data))
        if not chunk:
            raise ConnectionError("the client closed the connection")
        data += chunk
    return data


if len(sys.argv) != 2:
    sys.exit("usage: python3 framed_server.py BIND_ADDRESS")
bind_address = sys.argv[1]

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listener:
    # Lets a restart bind at once: Exercise 7 shows why.
    listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listener.bind((bind_address, PORT))
    listener.listen()
    print("listening on", listener.getsockname())
    while True:
        conn, client_address = listener.accept()
        with conn:
            print("accepted", client_address)
            try:
                for message in MESSAGES:
                    body = message.encode("utf-8")
                    send_in_pieces(conn, struct.pack("!I", len(body)) + body)
                (length,) = struct.unpack("!I", recv_exact(conn, 4))
                reply = recv_exact(conn, length).decode("utf-8")
                print("client said", repr(reply))
                body = f"{reply} received".encode("utf-8")
                conn.sendall(struct.pack("!I", len(body)) + body)
            except ConnectionError as error:
                print(error)
        print("closed", client_address)
```

**A given client that trusts one `recv`:**

```python
# @infra naive_client.py
# @expect against framed_server.py: prints how many bytes its one recv returned, and those bytes
"""naive_client.py: one recv, as if one send arrived as one message"""
import socket
import sys

PORT = 8081

if len(sys.argv) != 2:
    sys.exit("usage: python3 naive_client.py PEER_ADDRESS")
peer_address = sys.argv[1]

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect((peer_address, PORT))
    data = client_socket.recv(1024)
    print("one recv returned", len(data), "bytes:", data)
```

Complete the four TODOs of **your client**, `framed_client.py`:

```python
# @starter framed_client.py
"""framed_client.py: read and write length-prefixed messages on a stream socket"""
import socket
import struct
import sys

PORT = 8081


def recv_exact(sock, count):
    """Return exactly count bytes, calling recv as often as it takes."""
    data = b""
    # TODO 1: loop while data is shorter than count. In each pass, recv only the
    #   bytes still missing, count - len(data), and add the chunk to data.
    # TODO 2: inside the loop, an empty chunk (b"") means the peer has closed:
    #   raise ConnectionError("the peer closed the connection").
    return data


def recv_msg(sock):
    """Read one message: a 4-byte big-endian length, then that many bytes."""
    # TODO 3: read exactly 4 bytes, unpack them with "!I" into length, then read
    #   exactly length bytes and return them decoded from UTF-8.
    return ""


def send_msg(sock, text):
    """Send one message: its encoded length first, then its bytes."""
    # TODO 4: encode text to UTF-8 bytes, then send the 4-byte length of those
    #   bytes ("!I") followed by the bytes themselves, in one sendall.


if len(sys.argv) != 2:
    sys.exit("usage: python3 framed_client.py PEER_ADDRESS")
peer_address = sys.argv[1]

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect((peer_address, PORT))
    for number in range(1, 4):
        print(f"message {number}:", repr(recv_msg(client_socket)))
    send_msg(client_socket, "BYE")
    print("reply:", repr(recv_msg(client_socket)))
    try:
        recv_msg(client_socket)
    except ConnectionError as error:
        print("next read:", error)
```

**Run it.**

1. Copy the server to the peer from Kali, and start it in the peer terminal:

   ```bash
   scp framed_server.py lab:Session2/
   ```

   ```bash
   python3 framed_server.py PEER_ADDRESS
   ```

2. On Kali, run the one-`recv` client, then your completed client:

   ```bash
   python3 naive_client.py PEER_ADDRESS
   python3 framed_client.py PEER_ADDRESS
   ```

`naive_client.py` prints how many bytes its one `recv` returned, and they are not a message.
Your completed client prints exactly this:

```
(.venv) $ python3 framed_client.py 192.168.56.1
message 1: 'LOGIN alice'
message 2: 'café'
message 3: 'QUIT'
reply: 'BYE received'
next read: the peer closed the connection
```

Leave the server running while you check your answers, then stop it with **Ctrl+C**.

**Answer from your run:**

1. The one-`recv` client.
   - **1a.** How many bytes did its one `recv` return?
   - **1b.** What were those bytes?
2. The second message is `café`.
   - **2a.** Which four prefix bytes did the server send in front of it, in hex?
   - **2b.** How many characters does `café` have?
   - **2c.** How many bytes does its UTF-8 encoding have?

> [!example] 📝 Submission
> Paste your completed `framed_client.py`, the run of both clients, the server's output, and a screenshot of both clients' runs, then answer the Exercise 2 questions.

---

## Exercise 3: Refused, Timed Out or Open: One Connection Attempt — REQUIRED

> **🧩 GUIDED: complete the starter below** | Difficulty: ⭐⭐ Medium
> *Complete `probe.py`, then try one port at a time on the peer: one that listens, one that is closed, and one whose packets the peer drops.*

> [!note] Concept note
> A failed socket call raises an **exception** from the `OSError` family, and each exception describes a different event.
> A **closed** port answers a connection attempt with a reset, so `connect` raises `ConnectionRefusedError` at once, with `errno` 111.
> A port whose packets are **dropped** sends no answer at all.
> Without a deadline, `connect` waits until the kernel stops resending its connection request, about two minutes on Linux.
> `settimeout(n)` gives every blocking call on the socket a deadline of `n` seconds, and the call raises `TimeoutError` when it passes, with `errno` set to `None`.
> Both exceptions are subclasses of `OSError`, so their handlers must come **before** a general `except OSError`, or the general one catches them first.
> Silence alone cannot tell filtering from loss or from a machine that is down.
> This tool tries **one** port per run: trying many ports is scanning, which belongs to later work on the transport layer.

Complete the three TODOs in `probe.py`:

```python
# @starter probe.py
"""probe.py: classify one TCP connection attempt as open, refused or timed out"""
import socket
import sys
import time


def probe(host, port, timeout):
    """Try one connection and say how it ended, with the exception that ended it."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as probe_socket:
        # TODO 1: give every blocking call on probe_socket a deadline of timeout seconds.
        try:
            # TODO 2: connect probe_socket to (host, port).
            pass
        # TODO 3: above the OSError handler, catch ConnectionRefusedError and return
        #   "refused (...)", then TimeoutError and return "timed out (...)", each
        #   with the same name and errno details as the OSError line.
        except OSError as error:
            return f"failed ({type(error).__name__}, errno {error.errno})"
        return "open"


if len(sys.argv) not in (3, 4):
    sys.exit("usage: python3 probe.py HOST PORT [TIMEOUT_SECONDS]")
host, port = sys.argv[1], int(sys.argv[2])
timeout = float(sys.argv[3]) if len(sys.argv) == 4 else 2.0

start = time.perf_counter()
outcome = probe(host, port, timeout)
print(f"{host}:{port} {outcome} after {(time.perf_counter() - start) * 1000:.1f} ms")
```

**Run it.**

1. **On the peer**, start a listener on port 8082 with Python's built-in web server, and leave it running:

   ```bash
   python3 -m http.server 8082 --bind PEER_ADDRESS
   ```

   Port 8083 needs nothing: no program listens there, so it is closed.

2. **Make port 8084 drop its packets.**
   Open a second peer terminal with **+** and `ssh lab`, and add one firewall rule:

   > [!warning] A firewall rule on your peer
   > This rule drops every TCP packet to port 8084 on your peer, and nothing else.
   > Remove it in step 4, and check that it is gone.

   ```bash
   sudo iptables -I INPUT -p tcp --dport 8084 -j DROP
   sudo iptables -L INPUT -n
   ```

   ```
   peer $ sudo iptables -L INPUT -n
   Chain INPUT (policy ACCEPT)
   target     prot opt source               destination         
   DROP       6    --  0.0.0.0/0            0.0.0.0/0            tcp dpt:8084
   ```

3. **On Kali**, probe each port once:

   ```bash
   python3 probe.py PEER_ADDRESS 8082
   python3 probe.py PEER_ADDRESS 8083
   python3 probe.py PEER_ADDRESS 8084
   ```

   Each run prints one line: the port, how the attempt ended, and how long it took in milliseconds.

4. **Remove the rule**, check that the chain is empty again, and probe 8084 once more from Kali:

   ```bash
   sudo iptables -D INPUT -p tcp --dport 8084 -j DROP
   sudo iptables -L INPUT -n
   ```

   ```
   peer $ sudo iptables -L INPUT -n
   Chain INPUT (policy ACCEPT)
   target     prot opt source               destination         
   ```

   ```bash
   python3 probe.py PEER_ADDRESS 8084
   ```

   Stop the web server on the peer with **Ctrl+C**.

**Answer from your run:**

1. The three probes, with the rule in place.
   - **1a.** How did the attempt on 8082 end?
   - **1b.** After how many milliseconds did it end?
   - **1c.** How did the attempt on 8083 end?
   - **1d.** After how many milliseconds did it end?
   - **1e.** How did the attempt on 8084 end?
   - **1f.** After how many milliseconds did it end?
2. The probe after the rule was removed.
   - **2a.** How did the attempt on 8084 end this time?

> [!example] 📝 Submission
> Paste your completed `probe.py`, both `iptables -L` listings, the four probe lines, and a screenshot of the probes, then answer the Exercise 3 questions.

---

## Exercise 4: Wrapping the Client in TLS — REQUIRED

> **🧩 GUIDED: complete the starter below** | Difficulty: ⭐⭐ Medium
> *Make a certificate for the peer, run the given TLS server there, and complete `tls_client.py` until it connects with both checks on, then make each check fail.*

> [!note] Concept note
> Every byte a plain socket sends can be read by any machine on the path.
> **TLS** (Transport Layer Security) is a protocol that wraps the socket you already have: it encrypts the bytes, detects any change made to them on the path, and proves the server's identity.
> `wrap_socket` returns an object that still has `send` and `recv`.
> An `SSLContext` is local configuration, not a connection, and `ssl.create_default_context(cafile=...)` makes one with **two checks** turned on.
> **Trust**: the server's **certificate**, the document that binds a name to a public key, must be signed by a certificate in the trust store, here the file you pass as `cafile`.
> **Name**: the certificate's `subjectAltName` must match the `server_hostname` you pass to `wrap_socket`.
> Either failure raises `SSLCertVerificationError` before any of your data moves.
> The server holds the certificate **and its private key**.
> The client needs only the certificate of the authority that signed it, and a self-signed certificate is its own authority, so here that is `peer.crt` itself.

**Make the certificate on Kali.**
This command writes a certificate for the name `peer.lab`, valid for ten years, and its private key.
It prints a row of dots and plus signs while it makes the key:

```bash
# @generator peer.crt,peer.key
# @expect writes peer.crt (subject CN=peer.lab, subjectAltName DNS:peer.lab, valid 3650 days) and peer.key
openssl req -x509 -newkey rsa:2048 -nodes -days 3650 -subj "/CN=peer.lab" -addext "subjectAltName=DNS:peer.lab" -keyout peer.key -out peer.crt
```

Read back what it made:

```
(.venv) $ openssl x509 -in peer.crt -noout -subject -ext subjectAltName -enddate
subject=CN=peer.lab
X509v3 Subject Alternative Name: 
    DNS:peer.lab
notAfter=Oct 24 08:41:20 2036 GMT
```

Your expiry date is ten years from today.
Copy the certificate and the key to the peer, then **delete the key from Kali**, because the client never needs it:

```bash
scp peer.crt peer.key lab:Session2/
rm peer.key
```

**The given server, which runs on the peer:**

```python
# @infra tls_server.py
# @expect run on the peer beside peer.crt and peer.key: answers tls_client.py with b'OK over TLS' over TLSv1.3, and prints "handshake failed" for each client that rejects its certificate
"""tls_server.py: a TLS server for the lab that presents peer.crt and answers each client"""
import socket
import ssl
import sys

PORT = 8443

if len(sys.argv) != 2:
    sys.exit("usage: python3 tls_server.py BIND_ADDRESS")
bind_address = sys.argv[1]

server_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
server_context.load_cert_chain("peer.crt", "peer.key")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listener:
    listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listener.bind((bind_address, PORT))
    listener.listen()
    print("listening on", listener.getsockname())
    while True:
        conn, client_address = listener.accept()
        try:
            # Wrap the accepted socket, never the listener: one handshake per client.
            with server_context.wrap_socket(conn, server_side=True) as tls_conn:
                request = tls_conn.recv(1024)
                print(client_address, tls_conn.version(), "got", request)
                tls_conn.sendall(b"OK over TLS")
        except (ssl.SSLError, ConnectionError) as error:
            print(client_address, "handshake failed:", error)
            conn.close()
```

Complete the three TODOs of **your client**, `tls_client.py`:

```python
# @starter tls_client.py
"""tls_client.py: connect to the peer over TLS, checking its certificate and its name"""
import socket
import ssl
import sys

PORT = 8443

if len(sys.argv) not in (3, 4):
    sys.exit("usage: python3 tls_client.py PEER_ADDRESS SERVER_NAME [CA_FILE]")
peer_address, server_name = sys.argv[1], sys.argv[2]
ca_file = sys.argv[3] if len(sys.argv) == 4 else None

# Both checks on: the certificate must trace to ca_file, and carry server_name.
# TODO 1: make client_context with ssl.create_default_context, trusting ca_file.
client_context = None

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    # TODO 2: wrap client_socket with client_context, passing server_name as
    #   server_hostname, and call the wrapped socket tls_socket.
    with client_socket as tls_socket:
        tls_socket.connect((peer_address, PORT))
        # TODO 3: print "version:" with tls_socket.version(), and "cipher suite:"
        #   with the first item of tls_socket.cipher().
        tls_socket.sendall(b"hello")
        print("client got", tls_socket.recv(1024))
```

**Run it.**

1. Copy the server to the peer, and start it in the peer terminal:

   ```bash
   scp tls_server.py lab:Session2/
   ```

   ```bash
   python3 tls_server.py PEER_ADDRESS
   ```

2. On Kali, connect with both checks satisfied: the certificate as `cafile`, and the name it carries.
   The client connects to the address and checks the name, so no name lookup is involved:

   ```
   (.venv) $ python3 tls_client.py 192.168.56.1 peer.lab peer.crt
   version: TLSv1.3
   cipher suite: TLS_AES_256_GCM_SHA384
   client got b'OK over TLS'
   ```

3. **Break the trust check.** Leave out the CA file, so the client trusts only Kali's built-in authorities:

   ```bash
   python3 tls_client.py PEER_ADDRESS peer.lab
   ```

4. **Break the name check.** Keep the CA file, and ask for a name the certificate does not carry:

   ```bash
   python3 tls_client.py PEER_ADDRESS other.lab peer.crt
   ```

Each failing run ends in a traceback whose last line is an `ssl.SSLCertVerificationError`, and the peer prints one `handshake failed` line for each.
Stop the server with **Ctrl+C**.

**Answer from your run:**

1. The two failing runs.
   Each last line says `certificate verify failed:` and then a reason.
   - **1a.** What reason did the run without a CA file give?
   - **1b.** What reason did the run with `other.lab` give?

> [!example] 📝 Submission
> Paste your completed `tls_client.py`, the `openssl x509` check, the three client runs, the server's output, and a screenshot of the three runs, then answer the Exercise 4 questions.

---

## Exercise 5: One Thread per Client, and the Lock It Needs — REQUIRED

> **🧩 GUIDED: complete the starters below** | Difficulty: ⭐⭐ Medium
> *Time three clients against a server that serves one client at a time, move its handler into a thread, time them again, and then stop two threads from losing each other's updates.*

> [!note] Concept note
> A **blocking call** does not return until its work is finished, so a server built from blocking calls serves **one client from start to finish** before it looks at the next.
> A **thread** is an independent path of execution inside a process, with its own registers and stack, sharing the process's memory and sockets with every other thread.
> A **handler** is the function that serves one connection from start to finish.
> Give each connection a thread that runs the handler, and each thread can block on its own client without stopping the others.
> Shared memory has a price.
> `count = bump(count)` is three steps, read, compute and write, and two threads can interleave them: both read the same value, both write back one more, and one update is lost with no error.
> A `threading.Lock` makes the three steps one, because only one thread can be inside `with count_lock:` at a time.

**The given server, which serves one client at a time on the peer.**
Its handler works for one second on every request:

```python
# @infra serial_server.py
# @expect run on the peer: three_clients.py on port 8085 prints a reply time for each of the three clients
"""serial_server.py: serve each client from start to finish, one at a time"""
import socket
import sys
import time

PORT = 8085


def handle(conn, client_address):
    """Serve one connection: read the request, work for one second, reply."""
    with conn:
        try:
            request = conn.recv(1024)
            time.sleep(1.0)
            conn.sendall(b"done: " + request)
        except OSError as error:
            print(client_address, error)


if len(sys.argv) != 2:
    sys.exit("usage: python3 serial_server.py BIND_ADDRESS")
bind_address = sys.argv[1]

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listener:
    listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listener.bind((bind_address, PORT))
    listener.listen()
    print("listening on", listener.getsockname())
    while True:
        conn, client_address = listener.accept()
        handle(conn, client_address)
```

Complete the TODO of **your threaded server**, which runs the same handler in a thread:

```python
# @starter threaded_server.py
"""threaded_server.py: the same handler, run in one thread per connection"""
import socket
import sys
import threading
import time

PORT = 8086


def handle(conn, client_address):
    """Serve one connection: read the request, work for one second, reply."""
    with conn:
        try:
            request = conn.recv(1024)
            time.sleep(1.0)
            conn.sendall(b"done: " + request)
        except OSError as error:
            print(client_address, error)


if len(sys.argv) != 2:
    sys.exit("usage: python3 threaded_server.py BIND_ADDRESS")
bind_address = sys.argv[1]

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listener:
    listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listener.bind((bind_address, PORT))
    listener.listen()
    print("listening on", listener.getsockname())
    while True:
        conn, client_address = listener.accept()
        # TODO 1: replace this call. Start a threading.Thread that runs handle with
        #   the arguments (conn, client_address), with daemon=True, and do not wait for it.
        handle(conn, client_address)
```

**A given program that starts three clients at once, on Kali:**

```python
# @infra three_clients.py
# @expect against serial_server.py: prints a reply time, or "no reply within 5 s", for each of the three clients, with and without --stall
"""three_clients.py: start three clients at once and time each one's reply"""
import socket
import sys
import threading
import time


def client(peer_address, port, number, start, wait_times):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.settimeout(5.0)
        try:
            client_socket.connect((peer_address, port))
            client_socket.sendall(f"request {number}".encode())
            client_socket.recv(1024)
            wait_times.append(f"{time.perf_counter() - start:.2f} s")
        except TimeoutError:
            wait_times.append("no reply within 5 s")


if len(sys.argv) not in (3, 4) or sys.argv[3:] not in ([], ["--stall"]):
    sys.exit("usage: python3 three_clients.py PEER_ADDRESS PORT [--stall]")
peer_address, port = sys.argv[1], int(sys.argv[2])

stalled_socket = None
if "--stall" in sys.argv:
    # A client that connects and then sends nothing at all.
    stalled_socket = socket.create_connection((peer_address, port))
    print("one stalled client connected and sends nothing")
    time.sleep(0.2)

wait_times = []
start = time.perf_counter()
threads = [threading.Thread(target=client, args=(peer_address, port, number, start, wait_times))
           for number in (1, 2, 3)]
for thread in threads:
    thread.start()
for thread in threads:
    thread.join()
for place, wait_time in zip(("first", "second", "third"), wait_times):
    print(f"{place} reply: {wait_time}")
if stalled_socket:
    stalled_socket.close()
```

**Run the two servers.**

1. Copy both servers to the peer, and start the serial one:

   ```bash
   scp serial_server.py threaded_server.py lab:Session2/
   ```

   ```bash
   python3 serial_server.py PEER_ADDRESS
   ```

2. On Kali, time three clients against it, on port 8085:

   ```bash
   python3 three_clients.py PEER_ADDRESS 8085
   ```

3. Stop the serial server with **Ctrl+C**, start your threaded server in its place, and time the clients on port 8086:

   ```bash
   python3 threaded_server.py PEER_ADDRESS
   ```

   ```bash
   python3 three_clients.py PEER_ADDRESS 8086
   ```

   Stop the threaded server with **Ctrl+C**.

**Then the lost update**, in a program that runs on Kali.
Two threads each add 1 to a shared count 400,000 times, so a correct run ends at 800,000:

```python
# @starter lost_update.py
"""lost_update.py: two threads add to one shared count"""
import threading

ADDS_PER_THREAD = 400_000

count = 0
count_lock = threading.Lock()


def bump(value):
    return value + 1


def add_many():
    global count
    for _ in range(ADDS_PER_THREAD):
        # TODO 1: make the read, the bump and the write one step: hold count_lock
        #   around this line with a with statement.
        count = bump(count)


threads = [threading.Thread(target=add_many) for _ in range(2)]
for thread in threads:
    thread.start()
for thread in threads:
    thread.join()
print(f"count: {count:,} of {2 * ADDS_PER_THREAD:,}")
```

Run it **as given, three times**, before you complete its TODO.
Then complete the TODO and run it three times again:

```bash
python3 lost_update.py
python3 lost_update.py
python3 lost_update.py
```

**Answer from your run:**

1. The three clients.
   - **1a.** What was the slowest of the three reply times against the serial server?
   - **1b.** What was the slowest of the three reply times against your threaded server?
2. The shared count, before you added the lock.
   - **2a.** What count did the first run print?
   - **2b.** What count did the second run print?
   - **2c.** What count did the third run print?

> [!example] 📝 Submission
> Paste your completed `threaded_server.py` and `lost_update.py`, both `three_clients.py` runs, all six `lost_update.py` runs, and a screenshot of the two `three_clients.py` runs, then answer the Exercise 5 questions.

---

# Choice Exercises — Pick At Least 1

---

> [!tip] From scratch
> These exercises give you requirements and no starter.
> Reuse anything you wrote today: the skeletons of Exercise 1 are a good start for each.

## Exercise 6: Datagrams Keep Their Boundaries

> **🔨 FROM SCRATCH** | Difficulty: ⭐ Easy

> [!note] Concept note
> A datagram socket (`SOCK_DGRAM`, UDP) delivers **messages, not bytes**: one `sendto` becomes one `recvfrom`, and the boundary you sent is the boundary that arrives.
> It has no connection, so there is no `listen`, `accept` or `connect`, and every `sendto` names its destination.
> A read that is too small does not leave the rest of the datagram waiting.
> The rest is **discarded**.
> Nothing else is promised: a datagram can arrive out of order, twice or not at all, and the receiver is never told.

**Write two programs.**

- `udp_receiver.py` runs on the peer and takes the address to bind as its only argument.
  It binds a datagram socket to that address and port **8087**, then calls `recvfrom(1024)` five times, then `recvfrom(4)` once, then `recvfrom(1024)` once more, and prints what each call returned.
- `udp_sender.py` runs on Kali and takes the peer's address as its only argument.
  It sends seven datagrams to port 8087: `datagram 1` to `datagram 5`, then `0123456789`, then `after`.

Start the receiver on the peer first, then run the sender on Kali.

**Answer from your run:**

1. The last two reads.
   - **1a.** What did `recvfrom(4)` return?
   - **1b.** What did the `recvfrom(1024)` after it return?

> [!example] 📝 Submission
> Paste both programs, the receiver's output, the sender's output, and a screenshot of the receiver's output, then answer the Exercise 6 questions.

---

## Exercise 7: A Restart That Cannot Bind

> **🔨 FROM SCRATCH** | Difficulty: ⭐ Easy

> [!note] Concept note
> The side that **closes a connection first** keeps it in the `TIME_WAIT` state for 60 seconds on Linux, so that late packets from that connection cannot land in a new one.
> A server that closes first and then restarts inside that window cannot `bind` its port again, and fails with `OSError: [Errno 98] Address already in use`.
> A **socket option** is a per-socket setting the kernel reads.
> `setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)`, called before `bind`, lets the restart bind, but only when **every run sets it**, the first one included.

**Write one program**, `restart_server.py`, that runs on the peer.
It takes the address to bind as its first argument, and an optional second argument, `reuse`.
With `reuse`, it sets `SO_REUSEADDR` before `bind`.
It binds port **8088**, prints a line when the bind succeeds, accepts **one** client, sends it `bye` and a newline, closes that connection first, and exits.

**Run it.**

1. On the peer, start it **without** `reuse`.
   On Kali, connect once with `nc`, which prints `bye` and exits when the server closes:

   ```bash
   nc PEER_ADDRESS 8088 < /dev/null
   ```

2. On the peer, straight away, read the closed connection, then restart the server twice, first without `reuse` and then with it:

   ```bash
   ss -tano state time-wait sport = :8088
   python3 restart_server.py PEER_ADDRESS
   python3 restart_server.py PEER_ADDRESS reuse
   ```

3. Wait one minute, until the `ss` command lists nothing.
   Then repeat with `reuse` on **every** run: start the server with `reuse`, connect from Kali with `nc`, and start it with `reuse` again straight away.
   Stop the last server with **Ctrl+C**.

**Answer from your run:**

1. The first close.
   - **1a.** What did the `timer:` field of the `ss` line show?
2. The restart when every run set `reuse`.
   - **2a.** What was the first line it printed?

> [!example] 📝 Submission
> Paste `restart_server.py`, your `nc` run, the `ss` line, both restarts, the test with `reuse` on every run, and a screenshot of the restarts, then answer the Exercise 7 questions.

---

## Exercise 8: One Selector Loop Serves Many Clients

> **🔨 FROM SCRATCH** | Difficulty: ⭐⭐⭐ Hard

> [!note] Concept note
> A thread per connection parks one blocked call in every thread.
> **I/O multiplexing** is the alternative: one thread waits on many sockets at once.
> A socket is **readable** when bytes have arrived, or, for a listening socket, when a client is waiting to be accepted, so the next `recv` or `accept` returns at once.
> A **selector** is a set of sockets the kernel watches.
> `selector.select()` blocks until at least one is ready, and returns only the ready ones.
> `selectors.DefaultSelector()` picks the best mechanism the system has, which on Linux is `EpollSelector`.
> A **non-blocking** socket never waits: a call that cannot finish at once raises `BlockingIOError` instead, so one slow client can never stop the loop.

**Write one program**, `selector_server.py`, that runs on the peer and serves every client from **one thread**.

- It takes the address to bind as its only argument, binds port **8089**, and prints the class name of its selector when it starts.
- It registers the listening socket with a `selectors.DefaultSelector()`, for reading, and runs one loop over `selector.select()`.
- A ready listener means a new client: accept it, make the new socket non-blocking, and register it for reading.
- A ready client socket means bytes have arrived: `recv` them and send back `done: ` followed by the request.
  An empty `recv` means the client has closed: unregister the socket and close it.
- It never calls `time.sleep`, and it starts no threads.

**Run it**, against Exercise 5's `three_clients.py`.
Its `--stall` option first opens one connection that never sends anything.

1. Start `selector_server.py` on the peer, and time three clients against it from Kali:

   ```bash
   python3 three_clients.py PEER_ADDRESS 8089
   ```

2. Open a second peer terminal and start Exercise 5's `serial_server.py` there, beside the selector server.
   Then run the stalled test against each server:

   ```bash
   python3 three_clients.py PEER_ADDRESS 8085 --stall
   python3 three_clients.py PEER_ADDRESS 8089 --stall
   ```

   Stop both servers with **Ctrl+C**.

**Answer from your run:**

1. The stalled test.
   - **1a.** How many of the three clients got a reply from `serial_server.py`?
   - **1b.** How many of the three clients got a reply from your selector server?

> [!example] 📝 Submission
> Paste `selector_server.py`, the server's first line, the three `three_clients.py` runs, and a screenshot of the two stalled runs, then answer the Exercise 8 questions.

---

# Required Capstone

---

## Exercise 9: An ICMP Echo Request over a Raw Socket — REQUIRED

> **🧩 GUIDED: complete the starter below** | Difficulty: ⭐⭐⭐ Hard
> *Build an ICMP echo request with `struct`, send it to the peer over a raw socket, and read the reply, IPv4 header included.*

> [!note] Concept note
> Every socket so far let the kernel write all the headers, and you wrote only the payload.
> A **raw socket** moves that line: with `socket(AF_INET, SOCK_RAW, IPPROTO_ICMP)`, you write the whole **ICMP** message, header and data, and the kernel adds only the IPv4 header.
> ICMP carries Internet-layer control messages.
> An **echo request** asks the server to send its data back in an **echo reply**, with no TCP connection and no port, and the server's kernel answers it by itself.
> On receive, a raw IPv4 socket hands you the **whole packet, its IPv4 header included**.
> The header's length is not fixed: the low 4 bits of its first byte, the **IHL**, count it in 4-byte words.
> Creating a raw socket needs the Linux capability `CAP_NET_RAW`, a privilege a normal process lacks, so the program runs with `sudo`.
>
> The echo request's 8-byte header:
>
> | offset | size | field | this request |
> |---|---|---|---|
> | 0 | 1 | type | `8`, echo request (a reply is `0`) |
> | 1 | 1 | code | `0` |
> | 2 | 2 | checksum | the Internet checksum of the header and the data, computed with this field `0` |
> | 4 | 2 | identifier | `0x1234` |
> | 6 | 2 | sequence number | `1` |
>
> The checksum is the function you wrote in Module 1 Session 1, given here.

Complete the four TODOs in `icmp_echo.py`:

```python
# @starter icmp_echo.py
"""icmp_echo.py: send one ICMP echo request over a raw socket and read the reply"""
import socket
import struct
import sys

IDENTIFIER = 0x1234
SEQUENCE = 1
PAYLOAD = b"hello"


def checksum(data):
    """The Internet checksum (RFC 1071), as in Module 1 Session 1."""
    if len(data) % 2:
        data += b"\x00"
    total = sum(struct.unpack(f"!{len(data) // 2}H", data))
    while total >> 16:
        total = (total & 0xFFFF) + (total >> 16)
    return ~total & 0xFFFF


def build_request():
    # Type 8 (echo request), code 0, and checksum 0 until it is computed.
    # TODO 1: pack the 8-byte header with "!BBHHH": type 8, code 0, checksum 0,
    #   IDENTIFIER and SEQUENCE.
    header = b""
    # TODO 2: compute request_checksum over header + PAYLOAD with checksum(),
    #   then pack the header again with request_checksum in place of the 0.
    return header + PAYLOAD


if len(sys.argv) != 2:
    sys.exit("usage: sudo python3 icmp_echo.py PEER_ADDRESS")
peer_address = sys.argv[1]

request = build_request()
print("request:", request.hex(" "))

# TODO 3: create raw_socket as an IPv4 raw socket for ICMP: AF_INET, SOCK_RAW
#   and IPPROTO_ICMP.
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as raw_socket:
    raw_socket.settimeout(2.0)
    print("sent", raw_socket.sendto(request, (peer_address, 0)), "bytes")
    while True:
        reply, (source_address, _) = raw_socket.recvfrom(65535)
        # The reply starts with its IPv4 header. IHL counts 4-byte words.
        # TODO 4: set header_length from the low 4 bits of reply[0], times 4.
        header_length = 0
        icmp = reply[header_length:]
        reply_type, code, _, identifier, sequence = struct.unpack("!BBHHH", icmp[:8])
        if (source_address == peer_address and reply_type == 0
                and identifier == IDENTIFIER and sequence == SEQUENCE):
            break

print("reply from", source_address, "is", len(reply), "bytes")
print("IPv4 header:", header_length, "bytes, so ICMP starts at offset", header_length)
print("ICMP type", reply_type, "code", code, "identifier", hex(identifier), "sequence", sequence)
print("ICMP checksum verifies:", checksum(icmp) == 0)
print("data:", icmp[8:])
```

**Run it**, on Kali, twice.

1. **Without privilege** first:

   ```bash
   python3 icmp_echo.py PEER_ADDRESS
   ```

   It prints the request's bytes, and then `socket()` fails, before anything is sent.

2. **With `sudo`**, which asks for your Kali password:

   ```bash
   sudo python3 icmp_echo.py PEER_ADDRESS
   ```

   It prints the request's 13 bytes, how many it sent, and then five lines about the reply: its size, where ICMP starts in it, its type and code, whether its checksum verifies, and its data.

> [!tip] When the reply never comes
> A `TimeoutError` after 2 seconds means no matching reply arrived.
> Check the address first: `ping -c 1 PEER_ADDRESS` must work.
> A wrong checksum also gets no reply, because the peer's kernel drops the request.

**Answer from your run:**

1. The run without `sudo`.
   - **1a.** What is the last line of its traceback?
2. The run with `sudo`.
   - **2a.** How many bytes long was the reply?
   - **2b.** At which offset did ICMP start?

> [!example] 📝 Submission
> Paste your completed `icmp_echo.py`, both runs, and a screenshot of the `sudo` run, then answer the Exercise 9 questions.

---

# CTF Challenge — Solve Challenge 1

---

The CTF runs on Kali alone, on its own loopback address: a given service sends the records, and you write the solver.

| Challenge | Status | Difficulty | Skill |
|-----------|--------|------------|-------|
| Challenge 1: A Stream That Arrives in Pieces | **Required** | ⭐⭐ Medium | framing a byte stream, reading exactly *n* bytes |

> [!important] You must complete
> Challenge 1.

## Setup: start the challenge service

Save this as `ctf_service.py` in your working folder:

```python
# @infra ctf_service.py
# @expect prints "CTF service listening on ('127.0.0.1', 9000)" and sends each client five type-length-body records in pieces of 1 to 7 bytes
"""ctf_service.py: the CTF's local record service on 127.0.0.1:9000"""
import random
import socket
import struct
import time

ADDRESS = ("127.0.0.1", 9000)
NOTE, FLAG_RECORD = 0x4E, 0x46
# The flag is stored XORed, only so that it is not plain text in this file.
HIDDEN = bytes.fromhex("1c161b1d213c286e3769052e326905292e28696e3727")


def records():
    yield NOTE, b"records follow: type 1 byte, length 2 bytes, then the body"
    yield NOTE, b"FLAG{n0t_th1s_r3c0rd}"
    yield NOTE, b"." * 290 + b"FLAG{l3ngth_1s_tw0_byt3s}"
    yield FLAG_RECORD, bytes(byte ^ 0x5A for byte in HIDDEN)
    yield NOTE, b"end of records"


def send_in_pieces(conn, data, pieces):
    # Pieces of 1 to 7 bytes with a pause between them: no recv sees a whole record.
    start = 0
    while start < len(data):
        size = pieces.randint(1, 7)
        conn.sendall(data[start:start + size])
        start += size
        time.sleep(0.01)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listener:
    listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listener.bind(ADDRESS)
    listener.listen()
    print("CTF service listening on", listener.getsockname())
    while True:
        conn, client_address = listener.accept()
        print("serving", client_address)
        pieces = random.Random(2)
        with conn:
            try:
                for record_type, body in records():
                    send_in_pieces(conn, struct.pack("!BH", record_type, len(body)) + body, pieces)
            except ConnectionError:
                print(client_address, "left early")
```

Open a second Kali terminal with **+**, and start the service there.
It keeps running and serves every client that connects:

```bash
python3 ctf_service.py
```

```
(.venv) $ python3 ctf_service.py
CTF service listening on ('127.0.0.1', 9000)
```

## Challenge 1: A Stream That Arrives in Pieces — REQUIRED

> **🚩 CTF** | Difficulty: ⭐⭐ Medium

> [!note] Brief
> The service sends five **records** and then closes the connection.
> Each record is a 3-byte header, then a body: a **type** of 1 byte, then the body's **length** in 2 bytes, big-endian, then that many bytes of body.
> The flag is the body of the one record whose type is `0x46`.
> Two other records carry text shaped like a flag, and only the headers tell you which is which.
> The service sends its bytes in pieces of 1 to 7 bytes, with a pause between them, so no single `recv` sees a whole record.

**Step 1: look at what you are up against.**
One `recv` gets only the first piece:

```bash
python3 -c "import socket; s = socket.create_connection(('127.0.0.1', 9000)); print(s.recv(1024))"
```

**Step 2: solve it in Python** (write `solve1.py`, paste it into your Submission):
- Connect to `127.0.0.1` port `9000`.
- Read exactly 3 bytes, and unpack the type and the length from them.
- Read exactly that many bytes of body, and print each record's type and length.
- Repeat until the service closes the connection between two records, and print the body of the record of type `0x46`.

**Flag format:** `FLAG{...}`

> [!tip] Hint
> The `recv_exact` of Exercise 2 does the reading.
> `struct.unpack("!BH", header)` reads one unsigned byte and one big-endian 2-byte number.
> A record can be longer than 255 bytes, which is why the length takes two bytes.

> [!example] 📝 Submission
> Paste `solve1.py`, its output with every record and the flag, a screenshot of the run, and a one-line approach into your Submission.

### Rules

- **Solve the challenge by writing a Python script.**
  A flag picked out by eye, or by searching the raw bytes for `FLAG{`, earns nothing: the decoys exist to make that fail.
- **Cleanup:** stop the service with **Ctrl+C** in its terminal when you are done.
  It leaves no files behind.

---

# Hand In

When every exercise you are handing in is done, commit your worksheet and its screenshots once, then push and check that GitHub has everything:

```bash
cd ~/student-YOUR-USERNAME
git add Module1-Network-Attacks-and-Defense/Session2
git commit -m "Module 1 Session 2: practical guide"
git push
git status
```

**Checkpoint:** `git status` says `Your branch is up to date with 'origin/main'.`, and on GitHub your Practical Guide Submission shows every screenshot.
Only GitHub's copy counts: until the push succeeds, your work exists only on this machine.
Your scripts stay in `~/cyberlabs/Module1-Network-Attacks-and-Defense/Session2`, and the copies of your servers on the peer stay in `~/Session2`: the worksheet carries the code you hand in.

---

# What "done" looks like

- `ping` from Kali reaches the peer, and both machines print `Python 3.12` or newer
- `tcp_client.py` prints `client got b'OK'`, and `ss` lists the same connection on Kali and on the peer
- `framed_client.py` prints the three messages `'LOGIN alice'`, `'café'` and `'QUIT'`, the reply `'BYE received'`, and the closed connection
- `probe.py` reports port 8082 open, 8083 refused at once, and 8084 timed out after about 2,000 ms, and `iptables -L INPUT -n` lists no rule at the end
- `tls_client.py` prints `TLSv1.3` and `client got b'OK over TLS'` with both checks on, and fails each check once
- `three_clients.py` times the threaded server's three replies at about 1 second each, and `lost_update.py` prints `800,000` with the lock
- At least one of Exercises 6 to 8 prints what its exercise asks for
- `sudo python3 icmp_echo.py` reports an echo reply whose checksum verifies
- `solve1.py` prints every record's type and length, and a flag in the `FLAG{...}` format
- Your worksheet holds every completed exercise's code, output, screenshot and answers, with **Anything that failed** and **AI Assistance** filled in
- On GitHub, `Module1-Network-Attacks-and-Defense/Session2` shows the worksheet with every screenshot, and `git status` says **up to date**
