import socket
import time
import subprocess
import threading
import pygame
import pygame_controller
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
ARDUINO_DEVICE = (arduino_ip, arduino_port)
RUN_PYGAME = False


def runSocket():
    socketio.run(app, port=5001, host="0.0.0.0")


def sendMsg(msg):
    socketio.emit("message", msg)
    print("Sent: " + str(msg))


@app.route("/")
def home():
    return "Server is running!"


@socketio.on("message")
def handle_message(data):
    if RUN_PYGAME:
        pygame.event.post(
            pygame.event.Event(pygame_controller.SOCKETEVENT, message=data)
        )
    print("received message: message  " + str(data))


@socketio.on("joystick")
def handle_joystick_message(data):
    print("received message: joystick " + str(data))
    send(str(data), broadcast=True)


@socketio.on("UDP")
def handle_udp_message(data):
    print("received message: UDP" + str(data))
    if data == "connect":
        try:
            sock.bind(ARDUINO_DEVICE)
            print("Socket connected")
            send("Socket connected", broadcast=True)
        except Exception as e:
            print("Error connecting to socket")
            print(e)
            send(f"Error connecting to socket: {e}", broadcast=True)
    elif data == "disconnect":
        sock.close()
        print("Socket closed")
        send("Socket closed", broadcast=True)
    else:
        if sock is not None:
            sock.sendto(data.encode(), ARDUINO_DEVICE)
            print(f"Sent: {data}")
            print("Waiting for response...")
            sock.settimeout(0.5)  # Set the timeout to  1 second
            try:
                data, server = sock.recvfrom(8888)
                print(f"Received: {data.decode()}")
                send(f"Received: {data.decode()}", broadcast=True)
            except socket.timeout:
                print("No response received within  1 second.")
                send("No response received within  1 second.", broadcast=True)

    # send(str(data), broadcast=True)


@socketio.on("connect")
def handle_connect():
    print("connected")
    # send("connected", broadcast=True)


@socketio.on("disconnect")
def handle_disconnect():
    print("disconnected")
    # send("disconnected", broadcast=True)


if __name__ == "__main__":
    socketio_thread = threading.Thread(target=runSocket)
    # socketio_thread.setDaemon(True)
    socketio_thread.start()
    # pid_thread = threading.Thread(target=getPID.runStuff)
    # pid_thread.start()
    time.sleep(3)
    if RUN_PYGAME:
        pygame_controller.runJoyStick()
