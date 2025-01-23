<<<<<<< HEAD
import socket
=======
>>>>>>> 9faadee343b44c68dbafd8da5bde588ed69ce9df
import time

import socketio


sio = socketio.Client()


@sio.event
def connect():
<<<<<<< HEAD
=======
    sio.emit("joystick", "jsdoiafjoisj")

>>>>>>> 9faadee343b44c68dbafd8da5bde588ed69ce9df
    print(" connected!")


@sio.event
def disconnect():
    print("disconnected!")


def runStuff():
<<<<<<< HEAD
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
=======
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
>>>>>>> 9faadee343b44c68dbafd8da5bde588ed69ce9df
