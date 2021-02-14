import os
import asyncio
from subprocess import PIPE, Popen
import time

rf, wf = os.pipe()

# in child process
proc = Popen(['termux-sensor', '-d', '1000', '-s' 'Orientation Sensor'], stdout=wf)

# in parent process
os.close(wf)

with open(rf, 'r') as file:
    while proc.poll() is None:
        data = file.readline(5)
        print(f"received: {data}")

proc.wait()