import subprocess

def killCameras():
    try:
        result = subprocess.run(['ps', 'aux'], stdout=subprocess.PIPE)
        processes = result.stdout.decode().splitlines()

        toKill = []
        for process in processes:
            if "ust" in process:  
                temp = process.split()
                pid = temp[1]
                toKill.append(pid)

        toKill = toKill[:4]

        for pid in toKill:
            subprocess.run(['kill', '-9', pid])
            print(f"Killed process with PID: {pid}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    killCameras()
