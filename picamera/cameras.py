import os
import subprocess
import logging

videos = ["0", "2", "4", "6"]
resolution = [("1280", "720"), ("640", "480"), ("1280", "720"), ("640", "480")]


def startup():
    for i in range(len(videos)):

        p = subprocess.Popen(
            [
                "bash",
                "camrun.sh",
                videos[i],
                resolution[i][0],
                resolution[i][1],
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        print(p.pid)


if __name__ == "__main__":
    startup()
    print("Done")
