import subprocess


def killCameras():
    try:

        toKill = getProcesses()
        print(toKill)
        if len(toKill) == 0:
            print("No cameras to kill")
            return "None"
        for pid in toKill:
            subprocess.run(["kill", "-9", pid])
            print(f"Killed process with PID: {pid}")
        return "Done"

    except Exception as e:
        print(f"An error occurred: {e}")
        return "Error" + str(e)


def getProcesses():
    try:
        result = subprocess.run(["ps", "aux"], stdout=subprocess.PIPE)
        processes = result.stdout.decode().splitlines()

        toKill = []
        for process in processes:
            if "ustreamer" in process:
                temp = process.split()
                pid = temp[1]
                toKill.append(pid)

        toKill = toKill[:4]
        return toKill
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    killCameras()
