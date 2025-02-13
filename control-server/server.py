import os
import socket
import time
import threading
import pygame
import pygame_controller
from flask import Flask
from flask_socketio import SocketIO, send
from settings import *
import settings
import utils

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret!"
socketio = SocketIO(app, cors_allowed_origins="*")
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

device_ip = utils.get_ip()


def runSocket():
    print("Socket connected")
    socketio.run(app, port=5001, host="0.0.0.0")


def sendMsg(msg):
    socketio.emit("message", msg)
    print("Sent: " + str(msg))


@app.route("/")
def home():
    return "Server is running!"


@socketio.on("settings")
def handle_settings(data):
    print("received message: settings " + str(data))
    if data == "servo":
        send(servo_controlers, broadcast=True)
    elif data == "mapping":
        send("mapping:" + str(mapping), broadcast=True)
    # elif data


@socketio.on("setMapping")
def handle_setmapping(data):
    print("received message: setmapping " + str(data))
    # EDIT THE settings file to set the mapping
    with open("mapping.json", "w") as file:
        file.write(data)
    settings.mapping = json.loads(data)

    send("Mapping set", broadcast=True)
    # restart the server


@socketio.on("Pot Data")
def handle_potentiometer_message(data):
    print("received message: potentiometer " + str(data))
    send(str(data), broadcast=True)


@socketio.on("sensors")
def handle_sensors(data):
    print("received message: sensors " + str(data))
    send("sensors:" + str(data), broadcast=True)


@socketio.on("message")
def handle_message(data):
    if RUN_PYGAME:
        pygame.event.post(
            pygame.event.Event(pygame_controller.SOCKETEVENT, message=data)
        )
    print("received message: message  " + str(data))


# @socketio.on("sensors")
# def handle_joystick_message(data):
#     print("received message: sensors " + str(data))
#     send(str(data), broadcast=True)


@socketio.on("joystick")
def handle_joystick_message(data):
    print("received message: joystick " + str(data))
    send(str(data), broadcast=True)


@socketio.on("UDP")
def handle_udp_message(data):
    print("UPD received message: " + str(data))
    data = str(data)

    if RUN_PYGAME:
        pygame.event.post(
            pygame.event.Event(pygame_controller.SOCKETEVENT, message=data)
        )
    # if data == "connect":
    #     # try:
    #     settings.RUN_SOCKET = True
    #     sock.bind((device_ip, arduino_port))
    #     print("Socket connected")
    #     send("Socket connected", broadcast=True)
    # # except Exception as e:
    # #     print("Error connecting to socket")
    # #     print(e)
    # #     send(f"Error connecting to socket: {e}", broadcast=True)
    # elif data == "disconnect":
    #     settings.RUN_SOCKET = False
    #     sock.close()
    #     print("Socket closed")
    #     send("Socket closed", broadcast=True)
    # else:
    #     if settings.RUN_SOCKET == True:
    #         sock.sendto(data.encode(), ARDUINO_DEVICE)
    #         print(f"Sent: {data}")
    #         print("Waiting for response...")

    #         try:
    #             data, server = sock.recvfrom(8888)
    #             print(f"Received: {data.decode()}")
    #             send(f"Received: {data.decode()}", broadcast=True)
    #         except socket.timeout:
    #             print("No response received within  1 second.")
    #             send("No response received within  1 second.", broadcast=True)

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
    # sock.bind((device_ip, arduino_port))
    # sock.settimeout(1)  # Set the timeout to  1 second

    socketio_thread = threading.Thread(target=runSocket)
    # socketio_thread.setDaemon(True)
    socketio_thread.start()
    # pid_thread = threading.Thread(target=getPID.runStuff)
    # pid_thread.start()
    print(mapping)
    print(os.getpid())
    time.sleep(1)
    if RUN_PYGAME:
        pygame_controller.runJoyStick()
