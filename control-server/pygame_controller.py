import socket
import sys
import time
from flask import Flask
import pygame
from pygame.locals import *
import subprocess
import os
import socketio
from settings import *
import parseinput
import utils

# env vars to make joystik work in background
os.environ["SDL_VIDEO_ALLOW_SCREENSAVER"] = "1"
os.environ["SDL_JOYSTICK_ALLOW_BACKGROUND_EVENTS"] = "1"
os.environ["SDL_HINT_JOYSTICK_ALLOW_BACKGROUND_EVENTS"] = "1"
os.environ["SDL_VIDEO_X11_NET_WM_BYPASS_COMPOSITOR"] = "0"


sio = socketio.Client()

isConnected = True
device_ip = utils.get_ip()


@sio.event
def connect():
    global isConnected
    isConnected = True
    print("I'm connected!")


@sio.event
def disconnect():
    global isConnected
    isConnected = False
    print("I'm disconnected!")


USE_SOCKET = True
SOCKETEVENT = pygame.event.custom_type()
CTRL_DEADZONES = [JOY_DEADZONE] * 6  # Adjust these to your liking.


class mainProgram(object):
    def init(self):
        pygame.init()

        self.lastaxes = []
        self.lastbuttons = []
        pygame.joystick.init()

        self.joycount = pygame.joystick.get_count()
        if self.joycount == 0:
            print(
                "This program only works with at least one joystick plugged in. No joysticks were detected."
            )
            self.quit(1)
        # for i in range(self.joycount):
        self.joystick = pygame.joystick.Joystick(0)
        self.joystick.init()
        self.axiscount = self.joystick.get_numaxes()
        self.buttoncount = self.joystick.get_numbuttons()
        self.axes = [0.0] * self.axiscount
        self.buttons = [0] * self.buttoncount
        self.curMessage = ""

    def run(self):
        print("Running")
        pygameRunning = True
        while pygameRunning:
            for event in [pygame.event.wait()] + pygame.event.get():
                if event.type == QUIT:
                    pygameRunning = False
                elif event.type == JOYAXISMOTION:
                    self.axes[event.axis] = event.value
                elif event.type == JOYBUTTONUP:
                    self.buttons[event.button] = 0
                elif event.type == JOYBUTTONDOWN:
                    self.buttons[event.button] = 1
                elif event.type == SOCKETEVENT:
                    print("Socket event: " + str(event.message))
                    self.curMessage = str(event.message)
                    self.sendUDP()

            for i in range(len(self.axes)):
                if abs(self.axes[i]) < CTRL_DEADZONES[i]:
                    self.axes[i] = 0.0
                self.axes[i] = round(self.axes[i], 2)
            # Check for change in vals
            if str(self.axes) != str(self.lastaxes) or str(self.buttons) != str(
                self.lastbuttons
            ):
                self.lastaxes = list(self.axes)
                self.lastbuttons = list(self.buttons)
                # print("ME SEES A CHANGE")

                if RUN_JOYSTICK:
                    self.control()
            # time.sleep(0.1)

    def sendUDP(self):
        if SEND_UDP:
            sock.sendto(self.curMessage.encode(), ARDUINO_DEVICE)
            print(f"Sent: {self.curMessage}")
            print("Waiting for response...")
            sock.settimeout(1.0)  # Set the timeout to  1 second
            try:
                data, server = sock.recvfrom(8888)
                sio.emit("joystick", str(data.decode()))
                print(f"Received: {data.decode()}")
            except socket.timeout:
                print("No response received within  1 second.")
        # else:

    def control(self):
        # print("Control")

        sway = -self.axes[2]  # right stick left right

        heave = self.axes[3]  # right stick up down

        # x button for pich and roll
        if self.buttons[0] == 0:  # x button

            surge = self.axes[1]
            yaw = -self.axes[0]
            roll = 0
            pitch = 0
        else:
            surge = 0
            yaw = 0
            roll = -self.axes[0]
            pitch = self.axes[1]

        controlData = {
            "surge": surge,
            "sway": sway,
            "heave": heave,
            "yaw": yaw,
            "roll": roll,
            "pitch": pitch,
            "axes": self.axes,
            "buttons": self.buttons,
        }
        # print(controlData)

        if USE_SOCKET:
            print(controlData)
            controlData = parseinput.parse(controlData)

            self.curMessage = controlData
            self.sendUDP()

    def quit(self, status=0):
        pygame.quit()
        sys.exit(status)


def runJoyStick():

    global sock
    if SEND_UDP:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        sock.bind((device_ip, arduino_port))

    if USE_SOCKET:
        sio.connect("http://localhost:5001", transports=["websocket"])

    try:

        program = mainProgram()

        program.init()

        program.run()

    except KeyboardInterrupt:
        pygame.quit()
        if SEND_UDP:
            sock.close()

    finally:
        pygame.quit()
        if SEND_UDP:
            sock.close()


if __name__ == "__main__":
    USE_SOCKET = False
    runJoyStick()
