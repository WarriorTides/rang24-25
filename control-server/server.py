import os
import socket
import time
import threading
import pygame
import pygame_controller
from flask import Flask
from flask_socketio import SocketIO, send, emit
from settings import *
import settings
import utils
import sensorread
import potentiometerReader

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret!"
socketio = SocketIO(app, cors_allowed_origins="*")
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

device_ip = utils.get_ip()

global pygameStarted
pygameStarted=False

def runSocket():
    print("Socket connected")
    MAX_TROTTLE = settings.MAX_TROTTLE
    socketio.run(app, port=5001, host="0.0.0.0")


def sendMsg(msg):
    socketio.emit("message", msg)
    print("Sent: " + str(msg))


@app.route("/")
def home():
    return "Server is running!"


@socketio.on("settings")
def handle_settings(data):
    print("received settings: " + str(data))
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
    print(("DATA", data[0]))
    data[0] = data[0] * settings.MAX_TROTTLE
    data[1] = int(data[1] * 300 + 100)
    data[2] = int(data[2] * 300 + 100)
    emit("pots", (data), broadcast=True)
    fdata=str(data[0])+"," +str(data[1])+","+str(data[2])
    if RUN_PYGAME and pygameStarted:
        try:
            pygame.event.post(
                pygame.event.Event(
                    pygame_controller.POWERCHANGE,
                    message=str(fdata),
                )
            )
        except Exception as e:
            # Print all error information
            print("An error occurred:")
            print(f"Type: {type(e).__name__}")
            print(f"Message: {e}")
            print(f"Args: {e.args}")


@socketio.on("sensors")
def handle_sensors(data):
    # print("received message: sensors " + str(data))

    emit("sensors", str(data), broadcast=True)

    # if RUN_PYGAME:
    #     pygame.event.post(
    #         pygame.event.Event(
    #             pygame_controller.SENSORDATA,
    #             message=str(data),
    #         )
    #     )


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
    print("UPD received message: " + str(data))
    data = str(data)
    if RUN_PYGAME:
        pygame.event.post(
            pygame.event.Event(pygame_controller.SOCKETEVENT, message=data)
        )
    # if RUN_PYGAME:
    #     pygame.event.post(
    #         pygame.event.Event(pygame_controller.SOCKETEVENT, message=data)
    #     )


@socketio.on("thrusterPower")
def handle_power(data):
    print("received new power value: " + str(data))

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

    sensors_thread = threading.Thread(target=sensorread.runSensors)
    sensors_thread.start()

    pot_thread = threading.Thread(target=potentiometerReader.main)
    pot_thread.start()

    print(mapping)
    print(os.getpid())
    time.sleep(1)
    if RUN_PYGAME:
        pygameStarted=True
        pygame_controller.runJoyStick()
    
