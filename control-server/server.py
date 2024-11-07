import socket
import time
import subprocess
import threading
import pygame
import pygame_controller

# Setup Flask and SocketIO
from flask import Flask

from flask_socketio import SocketIO, send

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret!"
socketio = SocketIO(app, cors_allowed_origins="*")

arduino_ip = "192.168.1.151"
arduino_port = 8888
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

command = "ifconfig | grep 192 |awk '/inet/ {print $2; exit}' "
result = subprocess.run(
    command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
)
device_ip = ""


def runSocket():
    socketio.run(app, port=5001, host="0.0.0.0")


def sendMsg(msg):
    socketio.emit("message", msg)
    print("Sent: " + str(msg))


@socketio.on("message")
def handle_message(data):

    pygame.event.post(pygame.event.Event(pygame_controller.SOCKETEVENT, message=data))
    print("received message: " + str(data))


@socketio.on("joystick")
def handle_message(data):
    print("received message: " + str(data))
    send(str(data), broadcast=True)


@socketio.on("UDP")
def handle_message(data):
    print("received message: " + str(data))
    if data == "connect":
        sock.bind((device_ip, arduino_port))
    elif data == "disconnect":
        sock.close()
    else:
        sent = sock.sendto(data.encode(), (arduino_ip, arduino_port))
        time.sleep(0.00001)
        print("Waiting for response...")
        try:
            data, server = sock.recvfrom(3578)
            print(f"Received: {data.decode()}")
        except socket.timeout:
            print("No response received")

    send(str(data), broadcast=True)


@socketio.on("connect")
def handle_message():
    print("connected")
    # send("connected", broadcast=True)


@socketio.on("disconnect")
def handle_message():
    print("disconnected")
    # send("disconnected", broadcast=True)


if __name__ == "__main__":
    socketio_thread = threading.Thread(target=runSocket)
    # socketio_thread.setDaemon(True)
    socketio_thread.start()
    # pid_thread = threading.Thread(target=getPID.runStuff)
    # pid_thread.start()
    time.sleep(3)
    # pygame_controller.runJoyStick()
