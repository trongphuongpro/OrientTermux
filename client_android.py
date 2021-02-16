import os
import signal
from subprocess import PIPE, Popen
import time
import socketio
import asyncio

sio = socketio.AsyncClient()

@sio.event
async def connect():
    print("connected to websocket server.")

@sio.event
async def disconnect():
    print("disconnect from websocket server.")

@sio.event
async def getinfo():
    return "Android-Termux"


def emitData_callback(res):
    print(res)

def sigint_callback(sig_num, stack):
    print(f"received: {sig_num}")
    proc.terminate()


async def main():
    # add callback for SIGINT signal (Ctrl+C)
    signal.signal(signal.SIGINT, sigint_callback)

    rf, wf = os.pipe()

    # in child process
    proc = Popen(['termux-sensor', '-d', '1000', '-s' 'Orientation Sensor'], stdout=wf)

    # in parent process
    os.close(wf)

    await sio.connect('http://192.168.43.191:1234')

    with open(rf, 'r') as file:
        counter = 0
        data = ""
        total_line = 9

        for line in file:
            data += line
            counter += 1
            if counter == total_line:
                data = eval(data)["Orientation Sensor"]["values"]
                print(f"yaw: {data[0]} pitch: {data[1]} roll: {data[2]}")
                await sio.emit('data', data=data, callback=emitData_callback)

                data = ""
                counter = 0
    await sio.wait()
    proc.wait()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())