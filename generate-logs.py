import random

users = ["John", "Jane", "Bob"]
ips = ["198.51.100.7", "198.51.100.12", "198.51.100.23"]

for i in range(10):
    user = random.choice(users)
    ip = random.choice(ips)
    print("Oct 12 03:14:07 server sshd[1234]: Accepted password for " + user + " from " + ip + " port 40022 ssh2")