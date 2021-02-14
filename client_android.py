import os
import signal
from subprocess import PIPE, Popen
import time

def sigterm_callback(sig_num, stack):
    print(f"received: {sig_num}")
    proc.terminate()

signal.signal(signal.SIGTERM, sigterm_callback)

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
            data = eval(data)["Orientation Sensor"]["Values"]
            print(f"yaw: {data[0]} pitch: {data[1]} roll: {data[2]}")
            data = ""
            counter = 0

proc.wait()