import os
import signal
from subprocess import PIPE, Popen
import time
import socketio

sio = socketio.Client()

@sio.event
def connect():
    print("connected to websocket server.")

@sio.event
def disconnect():
    print("disconnect from websocket server.")

@sio.event
def getinfo():
    return "Android-Termux"


def emitData_callback(res):
    print(res)

def sigint_callback(sig_num, stack):
    print(f"received: {sig_num}")
    sio.disconnect()
    print(f">> disconnected with socket server")
    proc.terminate()
    print(f">> subprocess terminated")
    

signal.signal(signal.SIGINT, sigint_callback)

rf, wf = os.pipe()

# in child process
proc = Popen(['termux-sensor', '-d', '100', '-s' 'Orientation Sensor'], stdout=wf)

# in parent process
os.close(wf)

sio.connect('http://192.168.43.191:1234')

with open(rf, 'r') as file:
    counter = 0
    data = ""
    total_line = 9

    for line in file:
        data += line
        counter += 1

        # in case termux-sensor return empty dict (ex. {})
        if line == '}' and counter == 2:
            data = ""
            counter = 0

        if counter == total_line:
            try:
                data = eval(data)["Orientation Sensor"]["values"]
                sio.emit('data', data=data, callback=emitData_callback)
            except Exception as e:
                print(f"Error: {e}")

            data = ""
            counter = 0

proc.wait()
sio.wait()