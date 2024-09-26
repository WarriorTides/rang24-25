import os
import subprocess
import logging

videos = ["0", "2", "4", "6"]
ports = []
for x in videos:
    # v4l2-ctl --all -d /dev/video0
    command = "/dev/video" + x
    try:
        output = subprocess.check_output(
            ["v4l2-ctl", "--all", "-d", command], text=True
        )
    except subprocess.CalledProcessError as e:
        logging.error("Error: " + str(e))
        continue
    # output = subprocess.check_output(["v4l2-ctl", "--all", "-d", command], text=True)

    ports.append(x)

print(ports)

for port in ports:

    p = subprocess.Popen(
        [
            "bash",
            "camrun.sh",
            port,
            "640",
            "480",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    print(p.pid)
    print("PORTTTT")
