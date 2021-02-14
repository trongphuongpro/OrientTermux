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
    counter = 0
    data = ""

    for line in file:
        data += line
        counter += 1
        if counter == 9:
            print(f"received: {data}")
            data = ""
            counter = 0

proc.wait()