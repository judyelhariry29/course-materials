# Module 1 · Session 2 — Troubleshooting & FAQ

## The Python Networking Stack

### Professional Training in Cybersecurity I

---

> [!note] How to use this
> **Find the last line of the error, or the sentence you would say out loud**, not the exercise you were on.
> Errors are quoted exactly as Python, `openssl` and `nc` print them, so you can search this page for the line in front of you.
> Each entry shows the run that fails, the **cause**, then the **fix**.
> Every run was recorded on a lab with Kali at `192.168.56.107` (Python 3.13.12, OpenSSL 3.6.3, netcat-traditional 1.10-50.1) and an Ubuntu 24.04 peer at `192.168.56.1` (Python 3.12.3, OpenBSD netcat 1.226), with Kali's programs in a folder named `faq` inside the working folder.
> Your addresses are on CyberLab, `10.0.2.x`, and your paths, ports and process IDs differ.
> A line `[exit N]` after a run is that command's exit status, and `peer $` marks a command typed on the peer.
> For how a call or a tool works in full, see the **Tooling Reference**: this page is for when something breaks.
>
> If nothing here matches, note **the exact step, the exact command and everything it printed**, and ask in the Telegram group.

## Contents

- [Connections](#connections)
- [Ports already in use](#ports-already-in-use)
- [Raw sockets](#raw-sockets)
- [The TLS first flight](#the-tls-first-flight)
- [Netcat on another machine](#netcat-on-another-machine)

---

# Connections

### `ConnectionRefusedError: [Errno 111] Connection refused`

A client run against the peer, and the CTF solver run on Kali:

```
(.venv) $ python3 tcp_client.py 192.168.56.1
Traceback (most recent call last):
  File "/home/kali/cyberlabs/Module1-Network-Attacks-and-Defense/Session2/faq/tcp_client.py", line 14, in <module>
    client_socket.connect((peer_address, PORT))
    ~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^
ConnectionRefusedError: [Errno 111] Connection refused
(.venv) $ python3 solve1.py
Traceback (most recent call last):
  File "/home/kali/cyberlabs/Module1-Network-Attacks-and-Defense/Session2/faq/solve1.py", line 23, in <module>
    with socket.create_connection(("127.0.0.1", 9000)) as client_socket:
         ~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.13/socket.py", line 864, in create_connection
    raise exceptions[0]
  File "/usr/lib/python3.13/socket.py", line 849, in create_connection
    sock.connect(sa)
    ~~~~~~~~~~~~^^^^
ConnectionRefusedError: [Errno 111] Connection refused
```

On the peer, nothing listened on the client's port:

```
peer $ ss -tln 'sport = :8080'
State Recv-Q Send-Q Local Address:Port Peer Address:PortProcess
```

**Cause.**
The connection reached the machine, and no socket there listened on that address and port, so the machine answered the handshake with a reset at once.
That happens when the server was never started, was stopped with **Ctrl+C**, failed when it started (a server that was never copied to the peer with `scp` fails with `No such file or directory`), uses another port, or was started on `127.0.0.1`.
A server bound to `127.0.0.1` listens on the peer's loopback address only, so a connection from Kali to the peer's address finds nothing.
Exercise 1's last step does that on purpose.
For the CTF, `solve1.py` connects to `ctf_service.py` on Kali's own `127.0.0.1:9000`, so the service must be running in the second terminal.

**Fix.**
On the machine that runs the server, check that it listens: `ss -tln 'sport = :PORT'` must print a `LISTEN` line, and its local address must be the address the client connects to, or `0.0.0.0`.
An empty list, as above, means start the server first, in its own terminal, and leave it running.
Start a peer server with the peer's own address, `python3 tcp_server.py PEER_ADDRESS`, never `127.0.0.1`.
A connection attempt that **waits** and then fails is a different problem, a timeout, which the Tooling Reference's `iptables` example shows.

---

# Ports already in use

### `OSError: [Errno 98] Address already in use`

A second copy of a server started while the first still ran, on Kali:

```
(.venv) $ python3 ctf_service.py   [first terminal]
(.venv) $ python3 ctf_service.py
Traceback (most recent call last):
  File "/home/kali/cyberlabs/Module1-Network-Attacks-and-Defense/Session2/faq/ctf_service.py", line 35, in <module>
    listener.bind(ADDRESS)
    ~~~~~~~~~~~~~^^^^^^^^^
OSError: [Errno 98] Address already in use
(.venv) $ ss -tlnp 'sport = :9000'
State  Recv-Q Send-Q Local Address:Port Peer Address:PortProcess                           
LISTEN 0      128        127.0.0.1:9000      0.0.0.0:*    users:(("python3",pid=3703,fd=3))
```

The same for a UDP program:

```
(.venv) $ python3 trunc_detector.py   [first terminal]
(.venv) $ python3 trunc_detector.py
Traceback (most recent call last):
  File "/home/kali/cyberlabs/Module1-Network-Attacks-and-Defense/Session2/faq/trunc_detector.py", line 9, in <module>
    receiver.bind(("127.0.0.1", 8090))
    ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^
OSError: [Errno 98] Address already in use
(.venv) $ ss -ulnp 'sport = :8090'
State  Recv-Q Send-Q Local Address:Port Peer Address:PortProcess                           
UNCONN 0      0          127.0.0.1:8090      0.0.0.0:*    users:(("python3",pid=3718,fd=3))
```

And a server restarted straight after it closed a connection first, on the peer:

```
peer $ python3 restart_server.py 192.168.56.1   [peer terminal]
(.venv) $ nc 192.168.56.1 8088 < /dev/null
bye
peer $ ss -tan state time-wait 'sport = :8088'
Recv-Q Send-Q Local Address:Port   Peer Address:Port Process
0      0       192.168.56.1:8088 192.168.56.107:52596       
peer $ python3 restart_server.py 192.168.56.1
Traceback (most recent call last):
  File "/home/crc-user/Session2/restart_server.py", line 16, in <module>
    listener.bind((bind_address, PORT))
OSError: [Errno 98] Address already in use
[exit 1]
```

**Cause.**
`bind` claims an address and port, and only one socket can hold them.
There are two holders to look for:

- **A copy of the program that is still running**, in another terminal: the first two runs.
  `ctf_service.py` sets `SO_REUSEADDR` and still failed, because that option never lets a second socket in beside one that is listening.
  This is the common case: a server left running, and started again in a new terminal.
- **A connection in `TIME_WAIT`**: the third run.
  The side that closes a connection first keeps it for 60 seconds on Linux, and `ss` still lists it.
  A server that closes first and restarts inside that minute cannot bind its port, unless every run sets `SO_REUSEADDR` before `bind`, the first one included.

**Fix.**
Run `ss -tlnp 'sport = :PORT'` (`-ulnp` for UDP).
A line with a `users:` process is a running copy: stop it with **Ctrl+C** in its terminal, or `kill PID` with the `pid=` number `ss` printed, then start the program once.
No listening line, but a `time-wait` line, means wait one minute, or set `SO_REUSEADDR` on every run, as the Practical Guide's given servers do.
The peer's traceback has no `~~~^^^` line under the failing call, because its Python is 3.12, not Kali's 3.13.

---

# Raw sockets

### `TimeoutError: timed out` after `sudo`, and no echo reply arrives

Three runs that each sent a request and got nothing back.
`2>&1 | tail -1` keeps only the traceback's last line:

```
(.venv) $ sudo python3 icmp_echo.py 192.168.56.1 2>&1 | tail -1
TimeoutError: timed out
(.venv) $ sudo python3 hdrincl_echo.py 192.168.56.1 2>&1 | tail -1
TimeoutError: timed out
(.venv) $ ping -c 1 192.168.56.1 | tail -2
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 0.307/0.307/0.307/0.000 ms
(.venv) $ sudo python3 icmp_echo.py 192.168.56.99 2>&1 | tail -1
TimeoutError: timed out
(.venv) $ ping -c 1 192.168.56.99
PING 192.168.56.99 (192.168.56.99) 56(84) bytes of data.
From 192.168.56.107 icmp_seq=1 Destination Host Unreachable

--- 192.168.56.99 ping statistics ---
1 packets transmitted, 0 received, +1 errors, 100% packet loss, time 0ms
```

**Cause.**
The program waited 2 seconds for a matching echo reply, none came, and `settimeout(2.0)` ended the wait.
The peer answers an echo request in its kernel, and it answers nothing it cannot parse, so the bug is in what was sent, or the request never arrived.
Three causes produced the runs above:

- **The ICMP checksum is wrong** (the first run).
  This `icmp_echo.py` computed the checksum and then sent the header packed with `0` in its place.
  The peer's kernel checks the checksum of every ICMP message and drops one that does not verify, without a word.
- **`IP_HDRINCL` is not set** (the second run).
  This `hdrincl_echo.py` left out Task 3's TODO 2, so the kernel wrote its own IPv4 header in front of the one the program wrote.
  The peer read the program's 20-byte header as the start of the ICMP message, found no echo request there, and did not answer.
- **The address does not reach a machine** (the third run).
  `ping` fails too: `Destination Host Unreachable` means Kali asked the network for `192.168.56.99` and no machine answered.
  The first two runs reached the peer, which is why `ping` to it worked.

**Fix.**
Run `ping -c 1 PEER_ADDRESS` first.
If `ping` fails, the problem is the lab or the address, not your program: check the peer's address with `ip -br -4 addr` on the peer.
If `ping` works, the bytes are wrong:

- Check the checksum the way the receiver does: the program's own `checksum()` of a correct request, header and data together, is `0`.
  Compute it over the header with `0` in the checksum field, then pack the header again with the result in that field.
- In Task 3, set `IP_HDRINCL` to `1` on the raw socket before `sendto`.

---

# The TLS first flight

### My `openssl s_client` ends with an error. Did Task 1 fail?

With `sni_reader.py` running in the first terminal:

```
(.venv) $ python3 sni_reader.py   [first terminal]
(.venv) $ openssl s_client -connect 127.0.0.1:8444 -servername peer.lab < /dev/null 2>&1 | grep error
40478CC4E17F0000:error:0A000126:SSL routines::unexpected eof while reading:../ssl/record/rec_layer_s3.c:698:
40478CC4E17F0000:error:0A000197:SSL routines:SSL_shutdown:shutdown while in init:../ssl/ssl_lib.c:2804:
(.venv) $ openssl s_client -connect 127.0.0.1:8444 -servername peer.lab < /dev/null > /dev/null 2>&1
(.venv) $ echo $?
1
```

**Cause.**
Nothing failed on your side.
`sni_reader.py` is a plain TCP socket: it reads the ClientHello, prints what it found and closes, and it never sends a reply.
`s_client` was waiting for the server's half of the handshake, so it reports the close as `unexpected eof while reading`, then `shutdown while in init`, because it shut down a connection whose handshake never finished, and it exits with status 1.
The hexadecimal number at the start of each line and the file names and line numbers at the end come from your OpenSSL build and your process, so yours differ.

**Fix.**
None is needed: read the result from the **reader's** terminal, which prints the record and the `server_name:` line.
The client's error is only a problem when the reader printed nothing, which means it was not running, or was listening on another port.

---

# Netcat on another machine

### My `nc` prints `bye` and then hangs

A client that is not Kali, here the Ubuntu machine, connecting to Exercise 7's server running on Kali:

```
client $ nc 192.168.56.107 8088
bye
[exit 124]
client $ nc 192.168.56.107 8088 < /dev/null
bye
[exit 0]
```

The first run was recorded with a 10-second limit, which ended it with exit status 124.
At a terminal it waits until you press **Ctrl+C**.
Kali's `nc`, given the same terminal input, exits as soon as the server closes:

```
(.venv) $ nc 192.168.56.1 8088
bye
[exit 0]
```

**Cause.**
There are two different programs named `nc`.
Kali's is **netcat-traditional**, which exits once the server closes the connection.
Ubuntu's is **OpenBSD netcat**, which keeps running while its input is open, and a terminal's input stays open until you close it.
The server's `bye` arrived and the server closed, so nothing is wrong with the server.

**Fix.**
Type the Practical Guide's command as written, with `< /dev/null`: an empty input closes at once, and OpenBSD netcat then exits as soon as the server closes, as in the second run.
Run `nc -h 2>&1 | head -1` to see which program you have: netcat-traditional prints its version, `[v1.10-50.1]` on Kali, and OpenBSD netcat prints `OpenBSD netcat` and its patch level.
