import random 
from datetime import datetime, timedelta
random.seed(42)

#Attacker ip address is 203.0.113.5
#Possible attack compromise at 203.0.113.50
#username enumerations at 203.0.113.99

users = ["John", "Jane", "Bob"]
ips = ["198.51.100.7", "198.51.100.12", "198.51.100.23"]
start = datetime(2026,10,12,8,0,0)

lines = []

def normal_traffic():
    result = []
    for i in range(200):
        user = random.choice(users)
        ip = random.choice(ips)
        when = start + timedelta(seconds=random.randint(0, 36000))
        stamp = when.strftime("%b %d %H:%M:%S")
        if random.random() > 0.1:
            outcome = "Accepted"
        else:
            outcome = "Failed"
        line = stamp + " server sshd[" + str(random.randint(1000, 9999)) + "]: " + outcome + " password for " + user + " from " + ip + " port " + str(random.randint(40000, 60000)) + " ssh2"
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


def enumeration():
    result = []
    attacker = "203.0.113.99"
    attack_start = start + timedelta(hours=8)
    names = ["admin", "test", "oracle", "ubuntu", "postgres", "guest", "git", "ftp",
             "user", "mysql", "pi", "dev", "backup", "www", "support", "demo"]
    for i in range(len(names)):
        when = attack_start + timedelta(seconds=i * 5)
        stamp = when.strftime("%b %d %H:%M:%S")
        line = stamp + " server sshd[" + str(random.randint(1000, 9999)) + "]: Failed password for invalid user " + names[i] + " from " + attacker + " port " + str(random.randint(40000, 60000)) + " ssh2"
        result.append((when, line))
    return result


lines = normal_traffic() + brute_force() + compromise() + enumeration()
lines.sort()


with open("auth.log", "w") as f:
    for when, line in lines:
        f.write(line + "\n")