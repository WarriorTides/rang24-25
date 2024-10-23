import os
import subprocess
import json
from kill import getProcesses, killCameras, killPID

dir_path = os.path.dirname(os.path.realpath(__file__))

statepath = str(os.path.join(dir_path, "state.json"))
# camrunpath = str(os.path.join(dir_path, "camrun.sh"))

with open(statepath) as f:
    data = json.load(f)
    # print(data)

for i in data["cameras"]:
    print(i)

# print(camrun)
# def singleCam(index):
#     processes=getProcesses()
#     for i in processes:
#         if i[1]
#     return "Done"


def startup():
    port = 8000
    with open(statepath) as f:
        data = json.load(f)
    # print(data)
    for i in data["cameras"]:
        command = [
            "ustreamer",
            "--device",
            str(i["video port"]),
            "--resolution",
            f'{str(i["width"])}x{str(i["height"])}',
            "--format",
            "MJPEG",
            "--desired-fps",
            str(i["fps"]),
            "-l",
            "--encoder",
            "HW",
            "--host",
            "::",
            "--port",
            str(i["stream port"]),
            "--brightness",
            str(i["brightness"]),
            "--contrast",
            str(i["contrast"]),
            "--saturation",
            str(i["saturation"]),
            "--hue",
            str(i["hue"]),
            "--gamma",
            str(i["gamma"]),
            "--sharpness",
            str(i["sharpness"]),
            "--backlight-compensation",
            str(i["backlight compensation"]),
            "--white-balance",
            str(i["white balance"]),
            "--gain",
            str(i["gain"]),
            "--color-effect",
            str(i["color effect"]),
            "--rotate",
            str(i["rotate"]),
            "--flip-vertical",
            str(i["flip vertical"]),
            "--flip-horizontal",
            str(i["flip horizontal"]),
        ]

        print(command)
        p = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        print(p.pid)
        port += 1


# if __name__ == "__main__":
#     startup()
#     print("Done")
