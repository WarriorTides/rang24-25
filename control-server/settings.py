# For the control server
import json


arduino_ip = "192.168.1.151"
arduino_port = 8888

ARDUINO_DEVICE = (arduino_ip, arduino_port)
RUN_PYGAME = False
RUN_SOCKET = True
SEND_UDP = True


MAX_TROTTLE = 0.2
RUN_THRUSTER = True
JOY_DEADZONE = 0.1
RUN_JOYSTICK = True

# read mapping
with open("mapping.json", "r") as f:
    mapping = json.load(f)

servo_controlers = (
    [  # First two are main claw servos, second two are the second claw servos
        {
            "type": "axes",
            "index": 5,
            "used": True,
            "angles": [20, 90],
        },
        {
            "type": "buttons",
            "index": 1,
            "used": True,
            "angles": [20, 90],
        },
        {
            "type": "axes",
            "index": 5,
            "used": True,
            "angles": [20, 90],
        },
        {
            "type": "buttons",
            "index": 1,
            "used": True,
            "angles": [20, 90],
        },
    ]
)
