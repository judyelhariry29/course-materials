#!/usr/bin/env python3
"""watchlist.py: report the connections whose host is on a watchlist"""
import argparse
import watchlib


def main():
    parser = argparse.ArgumentParser(
        description="Report the log lines whose host is on the watchlist.")
    parser.add_argument("log", help="the connection log to check")
    parser.add_argument("--watchlist", default="watchlist.bin", help="the binary watchlist")
    parser.add_argument("--out", default="report.txt", help="where to write the report")

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
        try:
            time_str, action, host, port = watchlib.parse_line(line)
        except ValueError:
            skipped += 1
            continue

        if host in watched:
            host_key = str(host)
            hits[host_key] = hits.get(host_key, 0) + 1
            lines.append(f"{time_str} {action:<5} {host}:{port}")

    report_content = [f"Watchlist report for {args.log}"]
    report_content.extend(lines)
    report_content.append("Connections per watched host:")
    for host_key, count in hits.items():
        report_content.append(f"  {host_key}  {count}")

    with open(args.out, "w") as f:
        f.write("\n".join(report_content) + "\n")

    print(f"{len(watched)} watched, {len(lines)} matches, {skipped} skipped")
    print(f"report written to {args.out}")


if __name__ == "__main__":
    main()
