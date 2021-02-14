import os
import asyncio
from subprocess import PIPE, Popen
import time

rf, wf = os.pipe()

# in child process
proc = Popen(['termux-sensor', '-s', 'orientation'], stdout=wf)

# in parent process
os.close(wf)

with open(rf, 'r') as file:
    data = file.read()
    data = eval(data)
    print(f"received: {data}")

proc.wait()