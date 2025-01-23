import time

import socketio


sio = socketio.Client()


@sio.event
def connect():
    sio.emit("joystick", "jsdoiafjoisj")

    print(" connected!")


@sio.event
def disconnect():
    print("disconnected!")


def runStuff():
    sio.connect("http://192.168.1.164:5001", transports=["websocket"])
    time.sleep(0.2)

    # try:
    #     while True:


    #         time.sleep(0.1)

    # except KeyboardInterrupt:
    #     print("Closing socket")
    #     sio.disconnect()

    # finally:
    #     print("Closing socket")
    #     sio.disconnect()
runStuff()