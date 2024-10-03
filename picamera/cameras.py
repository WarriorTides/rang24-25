import os
import subprocess
import json
from kill import getProcesses, killCameras,killPID
dir_path = os.path.dirname(os.path.realpath(__file__))

statepath = str(os.path.join(dir_path, "state.json"))
camrunpath = str(os.path.join(dir_path, "camrun.sh"))

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
    port=8000
    for i in data["cameras"]:
        
        command=[
                "bash",
                str(camrunpath),
                str(i["video port"]),
                str(i["width"]),
                str(i["height"]),
                str(i["fps"]),
                str(port)
            ]
        print(command)
        p = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        print(p.pid)
        port+=1


# if __name__ == "__main__":
#     startup()
#     print("Done")
