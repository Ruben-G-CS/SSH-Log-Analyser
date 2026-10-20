# SSH Log Analyser and Intrusion Detector
# 1. Aim
This project creates a Python tool that parses SSH authentication logs, detects three
attack patterns using rules, and compares those rules with an unsupervised
anomaly detector (Isolation Forest). The goal was to understand what each
approach is good at and to understand the limitations that were encountered.

# 2. Data and design
I generated synthetic logs: 200 normal login events from three users and
three normal IPs (approximately 10% of them are failed logins, to mimic typos, wrong passwords etc). I also intentionally created 3 attack scenarios which are:

- `203.0.113.5`: brute force (40 failed logins in about two minutes)
- `203.0.113.50`: possible compromise (30 failures, then a successful login
  to a real account)
- `203.0.113.99`: username enumeration (16 different usernames)

I chose to create the data myself because it helps me clearly show the anomalies and  to test the detectors against the attacks, and avoids privacy issues with real IP addresses. All addresses are fake and are used for educational purposes. The generator is seeded, so results are reproducible.

# 3. Method
**Parser.** Each line is parsed with a regular expression that captures the
timestamp of the login, status (if the login has failed or been accepted), an optional "invalid user" phrase, username, IP and port. Timestamps are converted to `datetime` objects (the log has no year, so I supply it) so I can calculate time differences. As a
check, the parser read all 287 lines with none skipped, and the failed and accepted totals matched the generator.

**Rules.** Events are grouped by source IP. Three rules run on each group:
- *Brute force:* a sliding window flags an IP with 20 or more failures
  inside 120 seconds.
- *Possible compromise:* an IP flagged for brute force that then has a
  successful login after its last failure.
- *Username enumeration:* an IP that failed against 10 or more distinct
  usernames (counted with a set).

**Isolation Forest.** Each IP becomes a row of four features: total
attempts, failure rate, distinct usernames and attempts per minute. I used
scikit learns IsolationForest algorithm, which scores each IP by how easily it can be isolated from the rest. Lower scores mean more unusual.

# 4. Results
Each rule flagged exactly its intended attacker and no normal IPs. The
brute force rule also flagged `203.0.113.50`, which is correct because that specific
attacker brute-forces before getting in. Only the compromise rule separates
the two, since only one of them succeeded (hence called compromise).

The Isolation Forest results depended heavily on its `contamination`
setting. At 0.5 it flagged all three attackers and didn't flag the 3 normal IPs. At 0.1 and at `"auto"` it flagged only `203.0.113.99`. At `"auto"`, the brute force and compromise attackers scored slightly positive (0.003 and 0.017), meaning the model
treated them as normal. The ranking of IPs was similar across settings, but
the labels were not.

My conclusion is that the rules are better for deciding what to alert on,
while the model is useful for ranking how unusual an IP is. In this project
the rules caught all three attacks at every setting I tried, but the model
only did so when I told it that half the IPs were anomalous. To overcome this, perhaps using more data would've been better to train the model.

# 5. Limitations and next steps
- The data is hand made, so the attacks are obvious. Real attackers are
  often slower, spread across many IPs, or hide in normal traffic, and the
  rules would need different thresholds.
- Six IPs is very little data for machine learning. The model had too few
  normal examples to learn what normal looks like.
- I picked `contamination=0.5` knowing the answer, which a real system could
  not do.
- Thresholds (20 failures, 120 seconds, 10 usernames) were chosen by hand.
  Setting them too high missed attacks, and too low risked flagging normal
  typos.

# 6. What I learned
The Isolation Forest surprised me. At contamination setting 0.5, it flagged all three attackers, but at "auto" it flagged only one and scored two attackers as normal. That showed me its labels depend on a setting I chose, not on the model discovering the attacks, which a real system would not know.