import os
import subprocess
import json

dir_path = os.path.dirname(os.path.realpath(__file__))

statepath = str(os.path.join(dir_path, "state.json"))
camrunpath = str(os.path.join(dir_path, "camrun.sh"))

with open(statepath) as f:
    data = json.load(f)
    # print(data)

for i in data["cameras"]:
    print(i)


def startup():
    for i in data["cameras"]:

        p = subprocess.Popen(
            [
                "bash",
                str(camrunpath),
                data["cameras"][i]["video port"],
                data["cameras"][i]["width"],
                data["cameras"][i]["height"],
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        print(p.pid)


# if __name__ == "__main__":
#     startup()
#     print("Done")
