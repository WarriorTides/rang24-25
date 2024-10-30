import socket
import time
import subprocess
# Define the IP address and port of the Arduino
arduino_ip = "192.168.1.151"
arduino_port = 8888

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to a specific network interface and port number
command = "ifconfig | grep 192 |awk '/inet/ {print $2; exit}' "
result = subprocess.run(
    command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
)
device_ip = ""
if result.returncode == 0:
    device_ip = result.stdout.strip()
else:
    print(f"Command failed with error: {result.stderr}")
sock.bind((device_ip, arduino_port))

# The message to send


try:
    # Send data continously- used to test rate of messages
    sock.settimeout(1)
    while True:
        # message = input("Enter message: ")

        # message = "c,1500,1500,1500,1500,1500,1500,1500,1500,90,90,90"
        message = str(time.time())
        print(f"{message}")

        sent = sock.sendto(message.encode(), (arduino_ip, arduino_port))
        time.sleep(0.00001)
        print("Waiting for response...")
        try:
            data, server = sock.recvfrom(3578)
            print(f"Received: {data.decode()}")
        except socket.timeout:
            print("No response received")
            continue
        # data, server = sock.recvfrom(8888)
        # print(f"Received: {data.decode()}")
        # time.sleep(0.1)


except KeyboardInterrupt:
    print("Closing socket")
    sock.close()

finally:
    print("Closing socket")
    sock.close()
    # c, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 90, 90, 90
