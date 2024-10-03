import subprocess


def killCameras():
    try:

        toKill = getProcesses()
        print(toKill)
        if len(toKill) == 0:
            print("No cameras to kill")
            return "None"
        for pid in toKill:
            # print(pid)
            subprocess.run(["kill", "-9", str(pid[0])])
            print(f"Killed process with PID: {pid[0]}")
        return "Done"

    except Exception as e:
        print(f"An error occurred: {e}")
        return "Error" + str(e)


def getProcesses():
    try:
        result = subprocess.run(["ps", "aux"], stdout=subprocess.PIPE)
        processes = result.stdout.decode().splitlines()

        toKill = []
        command=[]
        for process in processes:
            if "ustreamer" in process:
                temp = process.split()
                pid = temp[1]
                
                toKill.append((pid,[item for item in temp if "video" in item][0], temp[temp.index([item for item in temp if "port" in item][0])+1]))
            

        # toKill = toKill[:4]
        return toKill
    except Exception as e:
        print(f"An error occurred: {e}")

def killPID(pid):
    try:
    
        subprocess.run(["kill", "-9", str(pid)])
        print(f"Killed process with PID: {pid}")
        return "Done"

    except Exception as e:
        print(f"An error occurred: {e}")
        return "Error" + str(e)


if __name__ == "__main__":
    killCameras()
