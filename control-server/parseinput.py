from settings import *
from power_comp import *  # powercomp is not used

# This filse converts data from the control data object- raw joystick data to thruster values mapped properly


mapping_dict = {item["name"]: item["index"] for item in mapping}
# sort
mapping = sorted(mapping, key=lambda x: x["index"])
# MappingDict is in this format: {'OFL': 2, 'OFR': 0, 'IFL': 1, 'IFR': 5, 'IBL': 3, 'IBR': 4, 'OBL': 7, 'OBR': 6}


servoangles = [0] * len(servo_controlers)
lastbuttons = [0] * len(servo_controlers)

flipped=False
for i in range(len(servo_controlers)):
    servoangles[i] = servo_controlers[i]["angles"][0]

# lastcontrol = {}


def map_thruster(value, MAX_POWER):  # from -1 to 1 to 1100 to 1900
    return int((value * MAX_POWER) * 400 + 1500)


def map_servo(value, a1, a2):  # from -1 to 1 to a1 to a2
    return int(((value + 1) * 0.5 * (a2 - a1)) + a1)


def parse(controlData, MAX_POWER):
    global lastcontrol
    controlString = "c"
    flip=controlData["flipped"]
    xythusters = {
        "OFR": (controlData["surge"] - controlData["yaw"] - controlData["sway"])*flip,
        "OFL": -1 * (controlData["surge"] + controlData["yaw"] + controlData["sway"])*flip,
        "OBR": (controlData["surge"] - controlData["yaw"] + controlData["sway"])*flip,
        "OBL": -1 * (controlData["surge"] + controlData["yaw"] - controlData["sway"])*flip,
    }

    zthrusters = {
        "IFL": (controlData["heave"] - controlData["roll"]*flip - controlData["pitch"]*flip),
        "IBL": -1 * (controlData["heave"] - controlData["roll"]*flip + controlData["pitch"]*flip),
        "IBR": controlData["heave"] + controlData["roll"]*flip + controlData["pitch"]*flip,
        "IFR": -1 * controlData["heave"] - controlData["roll"]*flip + controlData["pitch"]*flip,
    }
    maxxy = max(
        abs(value) for value in xythusters.values()
    )  # if max is greater than 1 we need to scale down
    # pri
    if maxxy > 1:
        print("Scaling down" + " " + str(maxxy))

        for key in xythusters:
            xythusters[key] /= maxxy

    maxz = max(abs(value) for value in zthrusters.values())  # same for z axis
    if maxz > 1:
        for key in zthrusters:
            zthrusters[key] /= maxz
    combinedthrust = xythusters.copy()
    combinedthrust.update(zthrusters)
    controlarray = [0] * len(mapping)
    for i in range(len(mapping)):
        controlarray[i] = combinedthrust[mapping[i]["name"]]

    for i in controlarray:
        controlString += "," + str(map_thruster(i, MAX_POWER))

    for i in range(len(servo_controlers)):
        servo = servo_controlers[i]
        if servo["used"]:
            if servo["type"] == "axes":
                servoangles[i] = map_servo(
                    controlData["axes"][servo["index"]], *servo["angles"]
                )
            elif servo["type"] == "buttons":
                curangle = servoangles[i]

                cur_angle_index = servo["angles"].index(curangle)

                # check if button state changed since last time

                cur_button = controlData["buttons"][servo["index"]]
                last_button = lastbuttons[i]
                # print(last_button, cur_button)

                if cur_button != last_button and cur_button == 1:
                    # print("Button state changed")
                    cur_angle_index += 1
                    cur_angle_index %= len(servo["angles"])
                    servoangles[i] = servo["angles"][cur_angle_index]
                lastbuttons[i] = cur_button

    # if(flip>0): 
    controlString += "," + str(servoangles[0]) + ",67,160" #+ str(servoangles[1]) +"," + str(servo_controlers[3]["angles"][0]) +"," + str(servo_controlers[2]["angles"][0] )
    # else:
    
        # controlString +="," + str(servo_controlers[0]["angles"][0]) +"," + str(servo_controlers[1]["angles"][0]) + "," + str(servoangles[3]) + "," + str(servoangles[2])
    controlString += "," + str(controlData["f1"]) + "," + str(controlData["f2"])
    print(controlString)
    return controlString
