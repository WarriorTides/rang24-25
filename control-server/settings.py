# For the control server
arduino_ip = "192.168.1.151"
arduino_port = 8888

ARDUINO_DEVICE = (arduino_ip, arduino_port)
RUN_PYGAME = True
RUN_SOCKET = False


MAX_TROTTLE = 0.5
RUN_THRUSTER = True
JOY_DEADZONE = 0.1
RUN_JOYSTICK = True


mapping = [
    {"name": "OFL", "color": "gray", "index": 2, "posIndex": 0, "rightpad": 2},
    {"name": "OFR", "color": "cyan", "index": 0, "posIndex": 1, "rightpad": 1},
    {"name": "IFL", "color": "blue", "index": 1, "posIndex": 2, "rightpad": 0},
    {"name": "IFR", "color": "purple", "index": 5, "posIndex": 3, "rightpad": 2},
    {"name": "IBL", "color": "yellow", "index": 3, "posIndex": 4, "rightpad": 0},
    {"name": "IBR", "color": "red", "index": 4, "posIndex": 5, "rightpad": 1},
    {"name": "OBL", "color": "orange", "index": 7, "posIndex": 6, "rightpad": 2},
    {"name": "OBR", "color": "pink", "index": 6, "posIndex": 7, "rightpad": 0},
]

servo_controlers = (
    [  # First two are main claw servos, second two are the second claw servos
        {
            "type": "axes",
            "index": 5,
            "used": True,
            "angles": [20, 270],
        },
        {
            "type": "buttons",
            "index": 1,
            "used": True,
            "angles": [0, 90],
        },
        {
            "type": "axes",
            "index": 5,
            "used": False,
            "angles": [20, 270],
        },
        {
            "type": "buttons",
            "index": 1,
            "used": False,
            "angles": [0, 90],
        },
    ]
)
