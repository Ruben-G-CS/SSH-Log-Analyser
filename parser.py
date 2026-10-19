import re
from datetime import datetime

pattern = r"^(\w{3} +\d+ \d{2}:\d{2}:\d{2}) .*?(Failed|Accepted) password for (invalid user )?(\w+) from (\S+) port (\d+)"


def parse_line(line):
    match = re.search(pattern, line)
    if match is None:
        return None
    when = datetime.strptime("2026 " + match.group(1), "%Y %b %d %H:%M:%S")
    return {
        "time": when,
        "status": match.group(2).lower(),
        "invalid": match.group(3) is not None,
        "user": match.group(4),
        "ip": match.group(5),
        "port": int(match.group(6)),
    }


def parse_file(path):
    events = []
    skipped = 0
    with open(path) as f:
        for line in f:
            event = parse_line(line.strip())
            if event is None:
                skipped += 1
            else:
                events.append(event)
    return events, skipped


if __name__ == "__main__":
    events, skipped = parse_file("auth.log")
    failed = 0
    accepted = 0
    for e in events:
        if e["status"] == "failed":
            failed += 1
        else:
            accepted += 1
    print("parsed:", len(events))
    print("skipped:", skipped)
    print("failed:", failed)
    print("accepted:", accepted)
    print(events[0])
    print(events[-1]["time"] - events[0]["time"])