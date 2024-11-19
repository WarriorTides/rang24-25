import subprocess


def get_ip():
    command = "ifconfig | grep 192 |awk '/inet/ {print $2; exit}' "
    result = subprocess.run(
        command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )
    device_ip = ""
    if result.returncode == 0:
        device_ip = result.stdout.strip()
    else:
        print(f"Command failed with error: {result.stderr}")

    return device_ip


def mapnum(
    num,
    outMin,
    outMax,
    inMin=-1,
    inMax=1,
):
    return round(
        outMin + (float(num - inMin) / float(inMax - inMin) * (outMax - outMin))
    )
