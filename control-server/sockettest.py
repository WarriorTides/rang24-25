import socket
import time

import socketio
import zmq
import json

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://sharis.local:5555")  # Replace with actual IP
socket.setsockopt_string(zmq.SUBSCRIBE, "")  # Subscribe to all messages


sio = socketio.Client()


@sio.event
def connect():
    print(" connected!")


@sio.event
def disconnect():
    print("disconnected!")


def runStuff():
    sio.connect("http://localhost:5001", transports=["websocket"])
    time.sleep(0.2)

    try:
        while True:

            message = socket.recv_string()
            data = json.loads(message)
            print("Received Sensor Data:", data)
            sio.emit("sensors", str("jsdoiafjoisj"))

            time.sleep(0.1)

    except KeyboardInterrupt:
        print("Closing socket")
        sio.disconnect()

    finally:
        print("Closing socket")
        sio.disconnect()


runStuff()
