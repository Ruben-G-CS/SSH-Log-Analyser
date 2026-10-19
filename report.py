import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import base64
from detector import detect_brute_force, detect_compromise, detect_enumeration


from parser import parse_file
from detector import group_by_ip
from anomaly import build_features, find_anomalies

def chart_failures_per_ip(groups, filename="failures_per_ip.png"):
    ips = list(groups.keys())
    counts = []
    for ip in ips:
        failed = 0
        for e in groups[ip]:
            if e["status"] == "failed":
                failed += 1
        counts.append(failed)

    plt.figure(figsize=(8, 4))
    plt.bar(ips, counts)
    plt.title("Failed logins per IP")
    plt.xlabel("Source IP")
    plt.ylabel("Failed logins")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()

def chart_failures_over_time(events, filename="failures_over_time.png"):
    buckets = {}
    for e in events:
        if e["status"] == "failed":
            minute = e["time"].replace(second=0)
            if minute not in buckets:
                buckets[minute] = 0
            buckets[minute] += 1

    times = sorted(buckets.keys())
    counts = [buckets[t] for t in times]

    plt.figure(figsize=(8, 4))
    plt.bar(times, counts, width=0.0007)
    plt.title("Failed logins per minute")
    plt.xlabel("Time")
    plt.ylabel("Failed logins")        
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
    plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=1))
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()

def chart_anomaly_scores(groups, filename="anomaly_scores.png"):
    rows = build_features(groups)
    results = find_anomalies(rows)
    ips = list(results.keys())
    scores = [results[ip][1] for ip in ips]
    colours = []
    for ip in ips:
        if results[ip][0] == -1:
            colours.append("tab:red")
        else:
            colours.append("tab:blue")

    plt.figure(figsize=(8, 4))
    plt.bar(ips, scores, color=colours)
    plt.axhline(0, color="black", linewidth=0.8)
    plt.title("Isolation Forest scores (red = flagged anomaly)")
    plt.xlabel("Source IP")
    plt.ylabel("Anomaly score (lower = more unusual)")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()

def embed(filename):
    with open(filename, "rb") as f:
        data = base64.b64encode(f.read()).decode()
    return '<img src="data:image/png;base64,' + data + '" style="max-width:100%">'


def write_html(groups, total_events, filename="report.html"):
    brute = detect_brute_force(groups)
    comp = detect_compromise(groups)
    enum = detect_enumeration(groups)

    html = "<html><head><title>SSH Log Report</title></head>"
    html += "<body style='font-family:sans-serif;max-width:900px;margin:auto'>"
    html += "<h1>SSH Log Analysis Report</h1>"
    html += "<p>Events parsed: " + str(total_events) + " from " + str(len(groups)) + " IPs.</p>"
    html += "<h2>Rule-based detections</h2><ul>"
    html += "<li><b>Brute force:</b> " + ", ".join(brute) + "</li>"
    html += "<li><b>Possible compromise:</b> " + ", ".join(comp) + "</li>"
    html += "<li><b>Username enumeration:</b> " + ", ".join(enum) + "</li>"
    html += "</ul>"
    html += "<h2>Failed logins per IP</h2>" + embed("failures_per_ip.png")
    html += "<h2>Failed logins over time</h2>" + embed("failures_over_time.png")
    html += "<h2>Anomaly scores</h2>" + embed("anomaly_scores.png")
    html += "</body></html>"

    with open(filename, "w") as f:
        f.write(html)

if __name__ == "__main__":
    events, skipped = parse_file("auth.log")
    groups = group_by_ip(events)
    chart_failures_per_ip(groups)
    print("saved failures_per_ip.png")
    chart_failures_over_time(events)
    print("saved failures_over_time.png")
    chart_anomaly_scores(groups)
    print("saved anomaly_scores.png")
    write_html(groups, len(events))
    print("saved report.html")