# Module 1 · Session 3 — Troubleshooting & FAQ

## Scapy and Raw Packet Crafting

### Professional Training in Cybersecurity I

---

> [!note] How to use this
> **Find the last line of the error, or the sentence you would say out loud**, not the exercise you were on.
> Errors and warnings are quoted exactly as Python, Scapy and `tcpdump` print them, so you can search this page for the line in front of you.
> Each entry shows the run that fails, the **cause**, then the **fix**.
> Every run was recorded on the lab's Kali (Python 3.13.12, Scapy 2.8.0 in the session's `.venv`, Docker 28.5.2, tcpdump 4.99.6), in the working folder `~/cyberlabs/Module1-Network-Attacks-and-Defense/Session3`, against the Practical Guide's compose lab.
> The lab's addresses are fixed, so yours are the same, and times and the bridge's own MAC address differ.
> Where a run needs two terminals, the line marked `[first terminal]` is the program started first, and its output follows under `[first terminal output]`.
> For how a call or a tool works in full, see the **Tooling Reference**: this page is for when something breaks.
>
> If nothing here matches, note **the exact step, the exact command and everything it printed**, and ask in the Telegram group.

## Contents

- [The Python environment](#the-python-environment)
- [Building packets](#building-packets)
- [Send and receive](#send-and-receive)
- [Capturing](#capturing)
- [The lab](#the-lab)

---

# The Python environment

### `sudo python3` prints Scapy `2.6.1`, not `2.8.0`

With the session's `.venv` active:

```
(.venv) $ sudo python3 -c "import scapy; print(scapy.__version__, scapy.__file__)"
2.6.1 /usr/lib/python3/dist-packages/scapy/__init__.py
(.venv) $ sudo sh -c 'command -v python3'
/usr/bin/python3
```

**Cause.**
`sudo` runs its command with a fixed search path of its own, which never includes `.venv`, even while the environment is active.
So `sudo python3` starts Kali's own Python, `/usr/bin/python3`, and that Python imports Kali's own Scapy, version 2.6.1, from `/usr/lib/python3/dist-packages`.
Nothing fails: the session's programs run under the older Scapy too, so nothing warns you, and any version or default that differs between the two can change what your program prints.

**Fix.**
Name the environment's interpreter by its path, from the working folder, every time a program needs `sudo`:

```
(.venv) $ sudo .venv/bin/python -c "import scapy; print(scapy.__version__, scapy.__file__)"
2.8.0 /home/kali/cyberlabs/Module1-Network-Attacks-and-Defense/Session3/.venv/lib/python3.13/site-packages/scapy/__init__.py
```

It must print `2.8.0` and a path inside `.venv`.

---

# Building packets

### `WARNING: getmacbyip failed on [Errno 1] Operation not permitted`

A frame built without `sudo`, with no Ethernet destination set:

```
(.venv) $ python3 -c "from scapy.all import Ether, IP, ICMP, raw; frame = raw(Ether() / IP(dst='10.10.3.10') / ICMP()); print(frame[:6].hex(':'))"
WARNING: getmacbyip failed on [Errno 1] Operation not permitted
WARNING: MAC address to reach destination not found. Using broadcast.
ff:ff:ff:ff:ff:ff
```

**Cause.**
When `Ether`'s `dst` is left unset, the build fills it with the MAC address of the next hop toward the IPv4 destination, and Scapy finds that address by sending a request of its own on the link.
Sending needs `CAP_NET_RAW`, which a program run without `sudo` does not hold, so the lookup failed with `Operation not permitted`.
Scapy then wrote the broadcast address, `ff:ff:ff:ff:ff:ff`, into the frame and carried on: the program ran to the end, with a destination you never chose.
A frame built this way never equals one built with the destination you meant, so a byte-for-byte comparison prints `False`.

**Fix.**
Set the destination yourself whenever you build a frame you will compare or save, as the Practical Guide's tables give it.
Then no lookup runs, and no privilege is needed:

```
(.venv) $ python3 -c "from scapy.all import Ether, IP, ICMP, raw; frame = raw(Ether(dst='02:42:0a:0a:03:0a') / IP(dst='10.10.3.10') / ICMP()); print(frame[:6].hex(':'))"
02:42:0a:0a:03:0a
```

Leave `dst` unset only in a program you run under `sudo` and send from, where you want Scapy's lookup.

---

# Send and receive

### `Received 2 packets, got 1 answers, remaining 0 packets` when I sent one request

The same request sent twice from one new process:

```
(.venv) $ sudo .venv/bin/python -c "from scapy.all import IP, ICMP, sr; req = IP(dst='10.10.3.10') / ICMP(id=0x0b0b, seq=5) / b'reference'; sr(req, timeout=2); sr(req, timeout=2)"
Begin emission
.*
Finished sending 1 packets

Received 2 packets, got 1 answers, remaining 0 packets
Begin emission
*
Finished sending 1 packets

Received 1 packets, got 1 answers, remaining 0 packets
```

**Cause.**
Nothing is wrong.
Before a new process sends its first packet to the target, Scapy runs its own MAC lookup, and the answer to that lookup arrives while `sr` is listening.
`sr` counts it as received and matches it to no request, which is the `.` before the `*`.
The second `sr` in the same process found the MAC address in Scapy's cache, which keeps each answer for 120 seconds, so it received only the reply.

**Fix.**
None is needed.
Read `got 1 answers`, or the length of the answered list, never the received count.
`conf.verb = 0` turns these progress lines off.

### `WARNING: MAC address to reach destination not found. Using broadcast.`

A request to `10.10.3.11`, one digit away from the target's address:

```
(.venv) $ sudo .venv/bin/python -c "from scapy.all import IP, ICMP, conf, sr1; conf.verb = 0; print(sr1(IP(dst='10.10.3.11') / ICMP(id=0x0b0b, seq=5) / b'reference', timeout=2))"
WARNING: MAC address to reach destination not found. Using broadcast.
None
(.venv) $ ping -c 2 10.10.3.11
PING 10.10.3.11 (10.10.3.11) 56(84) bytes of data.
From 10.10.3.1 icmp_seq=1 Destination Host Unreachable
From 10.10.3.1 icmp_seq=2 Destination Host Unreachable

--- 10.10.3.11 ping statistics ---
2 packets transmitted, 0 received, +2 errors, 100% packet loss, time 1006ms
pipe 2
```

**Cause.**
Scapy's MAC lookup asked the link for the address's MAC, waited 2 s, and got no answer, because no host holds `10.10.3.11`.
So Scapy sent the request to the broadcast address instead, nothing answered it, and `sr1` returned `None` after its timeout.
`ping` agrees: `Destination Host Unreachable` means Kali asked the link for that address and nobody answered.
The same warning appears for the right address when the target is not running (*The lab* below).

**Fix.**
Check the address you passed: the target is `10.10.3.10`.
Run `ping -c 2 10.10.3.10`: when it reports `2 received`, the problem is the address in your command, and when it fails, the lab is down.
The Practical Guide's probe of `10.10.3.99` prints this warning on purpose, because no host holds that address.

---

# Capturing

### `ValueError: 'timeout' isn't supported with AsyncSniffer. Use join(timeout=1)`

```
(.venv) $ sudo .venv/bin/python -c "from scapy.all import AsyncSniffer; sniffer = AsyncSniffer(iface='m1s3-lab', filter='icmp', timeout=5)"
Traceback (most recent call last):
  File "<string>", line 1, in <module>
    from scapy.all import AsyncSniffer; sniffer = AsyncSniffer(iface='m1s3-lab', filter='icmp', timeout=5)
                                                  ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/kali/cyberlabs/Module1-Network-Attacks-and-Defense/Session3/.venv/lib/python3.13/site-packages/scapy/sendrecv.py", line 1145, in __init__
    raise ValueError(
        "'timeout' isn't supported with AsyncSniffer. Use join(timeout=1)"
    )
ValueError: 'timeout' isn't supported with AsyncSniffer. Use join(timeout=1)
```

**Cause.**
`AsyncSniffer` takes every argument of `sniff()` except `timeout`, and refuses it when the object is made, before anything is captured.
It runs in a thread of its own, so the program decides when the capture ends.

**Fix.**
Remove `timeout`, and end the capture from the program:

- `sniffer.stop()` ends a capture that is still running and returns the list of packets it kept.
- With `count=N`, the capture ends by itself, and `sniffer.join(timeout=5)` waits for it, at most 5 seconds, then `sniffer.results` holds the list.

### My `AsyncSniffer` caught nothing, though my program got its reply

A program that starts a capture and sends at once, ten times:

```python
"""race_demo.py: start a capture and send at once, ten times; with "wait", wait for its socket first"""
import sys
import threading

from scapy.all import IP, ICMP, AsyncSniffer, conf, sr1

conf.verb = 0
wait_for_socket = len(sys.argv) > 1 and sys.argv[1] == "wait"
for run in range(1, 11):
    sniffer_ready = threading.Event()
    sniffer = AsyncSniffer(iface="m1s3-lab", filter="icmp and host 10.10.3.10", started_callback=sniffer_ready.set)
    sniffer.start()
    if wait_for_socket:
        sniffer_ready.wait()
    reply = sr1(IP(dst="10.10.3.10") / ICMP(id=0x0b0b, seq=run) / b"reference", timeout=2)
    print(f"run {run}: reply {'received' if reply else 'missing'}, captured {sniffer.stop()}")
```

```
(.venv) $ sudo .venv/bin/python race_demo.py
run 1: reply received, captured <Sniffed: TCP:0 UDP:0 ICMP:2 Other:0>
run 2: reply received, captured <Sniffed: TCP:0 UDP:0 ICMP:2 Other:0>
run 3: reply received, captured <Sniffed: TCP:0 UDP:0 ICMP:0 Other:0>
run 4: reply received, captured <Sniffed: TCP:0 UDP:0 ICMP:2 Other:0>
run 5: reply received, captured <Sniffed: TCP:0 UDP:0 ICMP:2 Other:0>
run 6: reply received, captured <Sniffed: TCP:0 UDP:0 ICMP:2 Other:0>
run 7: reply received, captured <Sniffed: TCP:0 UDP:0 ICMP:0 Other:0>
run 8: reply received, captured <Sniffed: TCP:0 UDP:0 ICMP:0 Other:0>
run 9: reply received, captured <Sniffed: TCP:0 UDP:0 ICMP:2 Other:0>
run 10: reply received, captured <Sniffed: TCP:0 UDP:0 ICMP:2 Other:0>
```

**Cause.**
`start()` starts the capture in a new thread and returns at once, before that thread has opened its socket.
A program that sends straight away can send, and get its reply, in that gap, and a packet that crossed the interface before the socket was open is never seen.
Whether a run wins or loses that race changes from run to run and from machine to machine: here 3 of 10 runs caught nothing.

**Fix.**
Wait until the socket is open before sending.
`started_callback` is called once it is open, so give it a `threading.Event`'s `set`, and `wait()` for the event after `start()`, as the program does when it is given `wait`:

```
(.venv) $ sudo .venv/bin/python race_demo.py wait
run 1: reply received, captured <Sniffed: TCP:0 UDP:0 ICMP:2 Other:0>
run 2: reply received, captured <Sniffed: TCP:0 UDP:0 ICMP:2 Other:0>
run 3: reply received, captured <Sniffed: TCP:0 UDP:0 ICMP:2 Other:0>
run 4: reply received, captured <Sniffed: TCP:0 UDP:0 ICMP:2 Other:0>
run 5: reply received, captured <Sniffed: TCP:0 UDP:0 ICMP:2 Other:0>
run 6: reply received, captured <Sniffed: TCP:0 UDP:0 ICMP:2 Other:0>
run 7: reply received, captured <Sniffed: TCP:0 UDP:0 ICMP:2 Other:0>
run 8: reply received, captured <Sniffed: TCP:0 UDP:0 ICMP:2 Other:0>
run 9: reply received, captured <Sniffed: TCP:0 UDP:0 ICMP:2 Other:0>
run 10: reply received, captured <Sniffed: TCP:0 UDP:0 ICMP:2 Other:0>
```

### Every packet shows up twice when I capture on `lo`

One UDP datagram sent to `127.0.0.1` while the capture runs:

```
(.venv) $ sudo .venv/bin/python -c "from scapy.all import sniff; sniff(iface='lo', filter='udp port 9999', prn=lambda packet: packet.summary(), timeout=6)"   [first terminal]
(.venv) $ python3 -c "import socket; socket.socket(socket.AF_INET, socket.SOCK_DGRAM).sendto(b'once', ('127.0.0.1', 9999))"
[first terminal output]
Ether / IP / UDP 127.0.0.1:50906 > 127.0.0.1:9999 / Raw
Ether / IP / UDP 127.0.0.1:50906 > 127.0.0.1:9999 / Raw
```

**Cause.**
On the loopback interface, `lo`, a packet leaves and arrives on the same interface.
A capture's packet socket receives a copy of every packet the machine sends out of an interface, and of every packet that arrives on it, so on `lo` it receives each packet twice: once on the way out, and once on the way back in.
Linux's own manual (`man 7 packet`) names the first copy `PACKET_OUTGOING`, "a packet originating from the local host that is looped back to a packet socket".

**Fix.**
Capture on the lab's bridge, `m1s3-lab`, as the Practical Guide does.
There a request leaves once and its reply arrives once, so each packet is captured once.

### `tcpdump: echo3.pcap: Permission denied`

`echo3.pcap` had just been written by `capture_echo.py`, run under `sudo`:

```
(.venv) $ tcpdump -r echo3.pcap -nn
tcpdump: echo3.pcap: Permission denied
(.venv) $ ls -l echo3.pcap
-rw-r----- 1 root root 402 Nov  9 08:39 echo3.pcap
```

**Cause.**
The program that wrote the file ran as root, so root owns it, and on this Kali a file root creates under `sudo` is readable by root and its group only (`-rw-r-----`).
`tcpdump` run without `sudo` runs as your own user, which may not open it.

**Fix.**
Read the file under `sudo` too, as the Practical Guide writes it: `sudo tcpdump -r echo3.pcap -nn`.
The same applies to any file a `sudo` program writes, such as a pcap from `wrpcap`.

---

# The lab

### `AttributeError: 'NoneType' object has no attribute 'summary'`

After Kali had restarted, the Home Task's two senders:

```
(.venv) $ sudo .venv/bin/python l2_echo.py m1s3-lab 10.10.3.10 02:42:0a:0a:03:0a
frame sent: Ether / IP / ICMP 10.10.3.1 > 10.10.3.10 echo-request 0 / Raw
Traceback (most recent call last):
  File "/home/kali/cyberlabs/Module1-Network-Attacks-and-Defense/Session3/l2_echo.py", line 18, in <module>
    print("srp1 reply:", frame_reply.summary())
                         ^^^^^^^^^^^^^^^^^^^
AttributeError: 'NoneType' object has no attribute 'summary'
(.venv) $ sudo .venv/bin/python -c "from scapy.all import IP, ICMP, conf, sr1; conf.verb = 0; print(sr1(IP(dst='10.10.3.10') / ICMP(id=0x2468, seq=7) / b'count', timeout=2).summary())"
WARNING: MAC address to reach destination not found. Using broadcast.
Traceback (most recent call last):
  File "<string>", line 1, in <module>
    from scapy.all import IP, ICMP, conf, sr1; conf.verb = 0; print(sr1(IP(dst='10.10.3.10') / ICMP(id=0x2468, seq=7) / b'count', timeout=2).summary())
                                                                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AttributeError: 'NoneType' object has no attribute 'summary'
```

Then the lab, from its folder:

```
(.venv) $ cd lab
(.venv) $ docker compose ps
NAME      IMAGE     COMMAND   SERVICE   CREATED   STATUS    PORTS
(.venv) $ docker compose ps -a
NAME            IMAGE         COMMAND            SERVICE   CREATED        STATUS                        PORTS
m1s3-target-1   alpine:3.24   "sleep infinity"   target    12 hours ago   Exited (255) 13 minutes ago   
(.venv) $ ip -br addr show m1s3-lab
m1s3-lab         DOWN           10.10.3.1/24 
(.venv) $ ping -c 2 10.10.3.10
PING 10.10.3.10 (10.10.3.10) 56(84) bytes of data.
From 10.10.3.1 icmp_seq=1 Destination Host Unreachable
From 10.10.3.1 icmp_seq=2 Destination Host Unreachable

--- 10.10.3.10 ping statistics ---
2 packets transmitted, 0 received, +2 errors, 100% packet loss, time 1018ms
pipe 2
```

**Cause.**
The target was not running.
The compose file sets no restart policy, so when Kali restarts, the target container stops and stays stopped: `docker compose ps` lists only running containers, so its list is empty, and `ps -a` shows the target as `Exited`.
With no container on it, the bridge `m1s3-lab` is `DOWN`.
So nothing answered: `srp1` and `sr1` each waited their 2 seconds and returned `None`, and calling `.summary()` on `None` raised the error.
The `sr1` run also printed the MAC lookup's `WARNING`, because the target did not answer that lookup either.

**Fix.**
Start the lab again from `lab/`, and check it before you run anything:

```
(.venv) $ docker compose up -d
 Container m1s3-target-1  Starting
 Container m1s3-target-1  Started
(.venv) $ docker compose ps
NAME            IMAGE         COMMAND            SERVICE   CREATED        STATUS                  PORTS
m1s3-target-1   alpine:3.24   "sleep infinity"   target    12 hours ago   Up Less than a second   
(.venv) $ cd ..
(.venv) $ ping -c 2 10.10.3.10
PING 10.10.3.10 (10.10.3.10) 56(84) bytes of data.
64 bytes from 10.10.3.10: icmp_seq=1 ttl=64 time=0.042 ms
64 bytes from 10.10.3.10: icmp_seq=2 ttl=64 time=0.032 ms

--- 10.10.3.10 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1009ms
rtt min/avg/max/mdev = 0.032/0.037/0.042/0.005 ms
```

`docker compose ps` must list `m1s3-target-1` as `Up`, and `ping` must report `2 received`.
Do this at the start of every sitting after Kali has restarted.
In your own programs, check `if reply is None` before reading a field from a reply, and print what was not answered: the same error appears for a mistyped address (*Send and receive* above).

### My `sniff()` never returns

After Kali had restarted, a capture waiting for two packets, ended after 20 seconds with **Ctrl+C**:

```
(.venv) $ sudo .venv/bin/python -c "from scapy.all import sniff; print(sniff(iface='m1s3-lab', filter='icmp', count=2))"
Traceback (most recent call last):
  File "<string>", line 1, in <module>
    from scapy.all import sniff; print(sniff(iface='m1s3-lab', filter='icmp', count=2))
                                       ~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/kali/cyberlabs/Module1-Network-Attacks-and-Defense/Session3/.venv/lib/python3.13/site-packages/scapy/sendrecv.py", line 1416, in sniff
    sniffer._run(*args, **kwargs)
    ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/home/kali/cyberlabs/Module1-Network-Attacks-and-Defense/Session3/.venv/lib/python3.13/site-packages/scapy/sendrecv.py", line 1371, in _run
    s.close()
    ~~~~~~~^^
  File "/home/kali/cyberlabs/Module1-Network-Attacks-and-Defense/Session3/.venv/lib/python3.13/site-packages/scapy/arch/linux/__init__.py", line 282, in close
    SuperSocket.close(self)
    ~~~~~~~~~~~~~~~~~^^^^^^
  File "/home/kali/cyberlabs/Module1-Network-Attacks-and-Defense/Session3/.venv/lib/python3.13/site-packages/scapy/supersocket.py", line 249, in close
    self.ins.close()
    ~~~~~~~~~~~~~~^^
  File "/usr/lib/python3.13/socket.py", line 505, in close
    self._real_close()
    ~~~~~~~~~~~~~~~~^^
  File "/usr/lib/python3.13/socket.py", line 499, in _real_close
    _ss.close(self)
    ~~~~~~~~~^^^^^^
KeyboardInterrupt
```

**Cause.**
`sniff(count=2)` returns only when its filter has kept two packets, and with no `timeout` it waits for them for as long as it takes.
Here the lab was down, so no ICMP packet crossed the bridge.
The same wait happens with the lab up when the sender is never started, or is started in the same terminal, where it cannot run until `sniff` returns.
**Ctrl+C** ends the wait, and what it prints depends on where it lands.
Scapy catches it inside the capture loop, and then `sniff` returns what it kept so far, here the empty list `<Sniffed: TCP:0 UDP:0 ICMP:0 Other:0>`.
Here it landed while Scapy was closing its socket, after that loop, so Python printed the `KeyboardInterrupt` traceback instead.
Either way, it is how the wait was ended, not a second problem.

**Fix.**
Check the lab first, as in the entry above.
Start the capture in one terminal, then the sender in a second terminal, opened with **+**.
While you are testing, add `timeout=20` beside `count`, so a capture that sees nothing returns an empty list instead of waiting.
