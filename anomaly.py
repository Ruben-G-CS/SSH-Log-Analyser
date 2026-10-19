from parser import parse_file
from detector import group_by_ip
from sklearn.ensemble import IsolationForest


def build_features(groups):
    rows = {}
    for ip in groups:
        events = groups[ip]
        total = len(events)
        failed = 0
        names = set()
        for e in events:
            if e["status"] == "failed":
                failed += 1
            names.add(e["user"])
        times = [e["time"] for e in events]
        minutes = (max(times) - min(times)).total_seconds() / 60
        if minutes < 1:
            minutes = 1
        rows[ip] = [total, failed / total, len(names), total / minutes]
    return rows


def find_anomalies(rows, contamination=0.5):
    ips = list(rows.keys())
    X = [rows[ip] for ip in ips]
    model = IsolationForest(contamination=contamination, random_state=42)
    labels = model.fit_predict(X)
    scores = model.decision_function(X)
    results = {}
    for i in range(len(ips)):
        results[ips[i]] = (labels[i], scores[i])
    return results


if __name__ == "__main__":
    events, skipped = parse_file("auth.log")
    groups = group_by_ip(events)
    rows = build_features(groups)
    results = find_anomalies(rows)
    for ip in results:
        label, score = results[ip]
        if label == -1:
            verdict = "ANOMALY"
        else:
            verdict = "normal"
        print(ip, verdict, round(score, 3))