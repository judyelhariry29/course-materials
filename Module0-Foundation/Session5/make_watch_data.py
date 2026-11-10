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
