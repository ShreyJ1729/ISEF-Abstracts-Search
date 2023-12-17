import os
import bs4

with open("isef-abstracts.html") as f:
    data=f.readlines()

pids = []

for line in data:
    if "&amp;ProjectId=" in line:
        # grab the part of the string after ProjectId= before the next "
        pid = line.split("&amp;ProjectId=")[1].split('"')[0]
        pids.append(pid)

with open("pids.txt", "w+") as f:
    for pid in pids:
        f.write(pid + "\n")
