import socket
import time

import socketio


sio = socketio.Client()


@sio.event
def connect():
    print(" connected!")


@sio.event
def disconnect():
    print("disconnected!")


def runStuff():
    sio.connect("http://Anyas-MacBook-Pro.local:5001", transports=["websocket"])
    time.sleep(0.2)

    try:
        while True:

            sio.emit("joystick", str("jsdoiafjoisj"))

            time.sleep(0.1)

    except KeyboardInterrupt:
        print("Closing socket")
        sio.disconnect()

    finally:
        print("Closing socket")
        sio.disconnect()


runStuff()
