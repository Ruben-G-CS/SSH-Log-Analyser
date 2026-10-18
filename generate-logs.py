import random 
from datetime import datetime, timedelta

users = ["John", "Jane", "Bob"]
ips = ["198.51.100.7", "198.51.100.12", "198.51.100.23"]
start = datetime(2026,10,12,8,0,0)

for i in range(10):
    user = random.choice(users)
    ip = random.choice(ips)
    seconds = random.randint(0,36000)
    when = start + timedelta(seconds=seconds)
    stamp = when.strftime("%b %d %H:%M:%S")
    print(stamp + " server sshd[1234]: Accepted password for " + user + " from " + ip + " port 40022 ssh2")