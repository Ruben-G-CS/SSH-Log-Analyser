import random 
from datetime import datetime, timedelta

#Attacker ip address is 203.0.113.50
#Possible attack compromise 203.0.113.50

users = ["John", "Jane", "Bob"]
ips = ["198.51.100.7", "198.51.100.12", "198.51.100.23"]
start = datetime(2026,10,12,8,0,0)

lines = []

def normal_traffic():
    result = []
    for i in range(10):
        user = random.choice(users)
        ip = random.choice(ips)
        seconds = random.randint(0, 36000)
        when = start + timedelta(seconds=seconds)
        stamp = when.strftime("%b %d %H:%M:%S")
        line = stamp + " server sshd[" + str(random.randint(1000, 9999)) + "]: Accepted password for " + user + " from " + ip + " port " + str(random.randint(40000, 60000)) + " ssh2"
        result.append((when, line))
    return result 

def brute_force():
    result = []
    attacker = "203.0.113.5"
    attacker_start = start + timedelta(hours=3)
    for i in range(40):
        when = attacker_start + timedelta(seconds= i * 3)
        stamp = when.strftime("%b %d %H:%M:%S")
        line = stamp + " server sshd[" + str(random.randint(1000, 9999)) + "]: Failed password for root from " + attacker + " port " + str(random.randint(40000, 60000)) + " ssh2"
        result.append((when, line))
    return result

def compromise():
    result = []
    attacker = "203.0.113.50"
    attack_start = start + timedelta(hours=6)
    for i in range(30):
        when = attack_start + timedelta(seconds=i * 4)
        stamp = when.strftime("%b %d %H:%M:%S")
        line = stamp + " server sshd[" + str(random.randint(1000, 9999)) + "]: Failed password for bob from " + attacker + " port " + str(random.randint(40000, 60000)) + " ssh2"
        result.append((when, line))
    when = attack_start + timedelta(seconds=30 * 4 + 5)
    stamp = when.strftime("%b %d %H:%M:%S")
    line = stamp + " server sshd[" + str(random.randint(1000, 9999)) + "]: Accepted password for bob from " + attacker + " port " + str(random.randint(40000, 60000)) + " ssh2"
    result.append((when, line))
    return result


lines = normal_traffic() + brute_force() + compromise()
lines.sort()


with open("auth.log", "w") as f:
    for when, line in lines:
        f.write(line + "\n")