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
    for i in data["cameras"]:

        command = [
            "ustreamer",
            "--device",
            "-l",
            i["video port"],
            "--resolution",
            f'{i["width"]}x{i["height"]}',
            "--format",
            "MJPEG",
            "--desired-fps",
            str(i["fps"]),
            "--encoder",
            "HW",
            "--host",
            "::",
            "--port",
            str(i["stream port"]),
            "--brightness",
            i["brightness"],
            "--contrast",
            i["contrast"],
            "--saturation",
            i["saturation"],
            "--hue",
            i["hue"],
            "--gamma",
            i["gamma"],
            "--sharpness",
            i["sharpness"],
            "--backlight-compensation",
            i["backlight compensation"],
            "--white-balance",
            i["white balance"],
            "--gain",
            i["gain"],
            "--color-effect",
            i["color effect"],
            "--rotate",
            i["rotate"],
            "--flip-vertical",
            i["flip vertical"],
            "--flip-horizontal",
            i["flip horizontal"],
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
