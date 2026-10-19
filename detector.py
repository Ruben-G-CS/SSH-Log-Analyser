from parser import parse_file
from datetime import timedelta

def group_by_ip(events):
    groups = {}
    for e in events:
        ip = e["ip"]
        if ip not in groups:
            groups[ip] = []
        groups[ip].append(e)
    return groups       

def detect_brute_force(groups, threshold=20, window_seconds=120):
    flagged = []
    for ip in groups:
        fails = []
        for e in groups[ip]:
            if e["status"] == "failed":
                fails.append(e["time"])
        fails.sort()
        for i in range(len(fails) - threshold + 1):
            span = fails[i + threshold - 1] - fails[i]
            if span <= timedelta(seconds=window_seconds):
                flagged.append(ip)
                break
    return flagged

if __name__ == "__main__":
    events, skipped = parse_file("auth.log")
    groups = group_by_ip(events)
    print("brute force:", detect_brute_force(groups))