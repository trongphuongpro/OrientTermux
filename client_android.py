import os
import asyncio
from subprocess import PIPE, Popen
import time

rf, wf = os.pipe()

# in child process
proc = Popen(['ping', '-c 10', 'google.com'], stdout=wf)

# in parent process
os.close(wf)

with open(rf, 'r') as file:
    for line in file:
        print(f"received: {line.encode()}")

proc.wait()