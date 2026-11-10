"""watchlib.py: read a binary watchlist and parse connection log lines"""
import ipaddress


def read_watchlist(path):
    """Return the set of addresses stored in path, 4 bytes each."""
    try:
        with open(path, "rb") as f:
            data = f.read()
    except FileNotFoundError:
        raise SystemExit(f"{path} not found")

    if len(data) % 4 != 0:
        raise SystemExit(f"{path}: {len(data)} bytes, not 4 per address")

    watched = set()
    for i in range(0, len(data), 4):
        chunk = data[i:i+4]
        ip_str = f"{chunk[0]}.{chunk[1]}.{chunk[2]}.{chunk[3]}"
        watched.add(ipaddress.ip_address(ip_str))

    return watched


def parse_line(line):
    """Return (time, action, host, port) from one line, or raise ValueError."""
    parts = line.split()
    if len(parts) != 4:
        raise ValueError("invalid line format")

    time_str, action, host_str, port_str = parts
    host = ipaddress.ip_address(host_str)
    port = int(port_str)
    if not (0 <= port <= 65535):
        raise ValueError(f"port out of range: {port}")

    return (time_str, action, host, port)
