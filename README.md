# SSH Log Analyser and Intrusion Detector

A Python tool that parses Secure shell auth logs, detects attacks with
rule-based detectors, and functions that will flag any unusual source IPs with an Isolation Forest machine learning algorithm.

This project is only for portfolio purposes.

# What the tool does
1. `generate-logs.py` creates a `auth.log` file with normal traffic and
   three known attacks (the "answer key").
2. `parser.py` turns each line in auth.log into a structured event using regular expressions.
3. `detector.py` runs three rules which detects attacks: brute force, possible compromise, username enumeration.
4. `anomaly.py` builds features per IP and runs an Isolation Forest.
5. `report.py` produces charts and a self-contained `report.html`.

# How to run
    python3 -m venv venv (Using MacOS)
    source venv/bin/activate (Activating Virtual Environment)
    pip install scikit-learn matplotlib
    python generate-logs.py
    python detector.py
    python anomaly.py
    python report.py

Then open `report.html`.

# Results

The generator injects three known attacks, so each detector can be checked
against an answer key. Every rule flagged exactly is its own attacker and no
regular IPs.

| Detector | Flagged IP (or IPs) | Expected |
----------------------------------------------
| Brute force | 203.0.113.5, 203.0.113.50 | 203.0.113.5 (40 failures), plus the compromise attacker, who also brute forces first |
| Possible compromise | 203.0.113.50 | 30 failures then a successful login |
| Username enumeration | 203.0.113.99 | 16 different usernames |

**Isolation Forest** (6 IPs (3 Normal IPs and 3 Attackers), `contamination=0.5`) ranked all three attackers as more anomalous than all three normal IPs. `203.0.113.99` scored lowest
(about -0.114).

# Tuning notes and limitations
- Brute force threshold of 45 missed the 40-failure attacker (ranked too high).
- A very low threshold risked flagging normal users typos (ranked too low).
- Isolation Forest labels depended on `contamination`: at 0.5 it flagged all
  three attackers, at 0.1 only the enumeration attacker, and at `"auto"` the only IP that got flagged was the enumeration one `203.0.113.99`.
- Margins were small (for example, `203.0.113.50` at about -0.005 versus
  `198.51.100.12` at about +0.005), which shows how little data six IPs give
  the model.

# Limitations
- The data is synthetic, so the attacks are easy to spot.
- Only 6 IPs, so the Isolation Forest has little data to learn from therefore limiting the potential of the MLA.
- The contamination setting largely decides how many IPs get labelled anomalies since its 0.5, there are 3 attackers and 3 users.
- Thresholds were tuned by hand against known attacks.