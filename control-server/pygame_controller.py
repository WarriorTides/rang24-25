# Handles joystick input as well as UDP pmessaging

import socket
import sys
import time
from flask import Flask
import pygame
from pygame.locals import *
import subprocess
import os
import json
import ast

import socketio
from settings import *
import parseinput
import utils

from simple_pid import PID

pidOn = False

pid = PID(2, 0.00, 0.00, setpoint=1)
pid.output_limits = (-1, 1)


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


SOCKETEVENT = pygame.event.custom_type()
POWERCHANGE = pygame.event.custom_type()
SENSORDATA = pygame.event.custom_type()
BOUY =pygame.event.custom_type()
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
        # self.sadme="im sad"
        self.bouyone=200
        self.bouytwo=200
        self.MAX_POWER = MAX_TROTTLE
        self.depth = -1
        self.depthvalue = 0
        self.flipped=False
        self.lastflipped=0

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
                elif event.type == POWERCHANGE:
                    # print("POERRJOISJDOF")
                    # print(event.message)
                    try:
                        datarr=event.message.split(",")
                        self.MAX_POWER = float(datarr[0])
                        self.bouyone=int(datarr[1])
                        self.bouytwo=int(datarr[2])
                        self.control()
                        # print(self.bouyone)
                        # self.floatpos= 
                        # print(floatpos)
                        # self.floatpos[0]=datarr[1]
                        # self.floatpos[1]=datarr[2]
                        # self.bigbilly=int(event.message.split(",")[1])
                        # blabla=event.message
                        # self.MAX_POWER = float(event.blabla)
                        # self.depthvalue=1
                    except Exception as e:
                        print("Invalid power value")
                        print(e)
            
        
                elif event.type == SENSORDATA:
                    try:
                        json_data = ast.literal_eval(event.message)
                        # print(json_data["DEPTH"]["Depth"])
                        self.depth = json_data["DEPTH"]["Depth"]
                    except Exception as e:
                        self.depth = -1
                        # print("Invalid sensors")

            for i in range(len(self.axes)):
                if abs(self.axes[i]) < CTRL_DEADZONES[i]:
                    self.axes[i] = 0.0
                self.axes[i] = round(self.axes[i], 2)
            if ((self.axes[3] == 0.0) and (pidOn == True)):
                print("Depth: ", self.depth)
                self.depthvalue = pid(self.depth) * -1
                print("PID: ", self.depthvalue)
                self.control()
            else:
                self.depthvalue = 0
            self.depthvalue = 0

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
            print("Depth" + str(self.depth))
            print("PID" + str(self.depthvalue))
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

        heave = -self.axes[3]  # right stick up down

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
        



        if self.buttons[3] == 1 and not self.lastflipped == self.buttons[3]:
            sio.emit("flip", str(not self.flipped))
            self.flipped=not self.flipped
            
        self.lastflipped=self.buttons[3]
        controlData = {
            "surge": surge,
            "sway": sway,
            "heave": heave,
            "yaw": yaw,
            "roll": roll,
            "pitch": pitch,
            "axes": self.axes,
            "buttons": self.buttons,
            "f1":self.bouyone,
            "f2":self.bouytwo,
            "flipped": -1 if self.flipped else 1
        }
        # print(controlData)
        # if self.depthvalue != 0:
        #     controlData["heave"] = self.depthvalue

        if USE_SOCKET:
            # print(controlData)
            controlData = parseinput.parse(controlData, self.MAX_POWER)

            self.curMessage = controlData
            # print(controlData)
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
