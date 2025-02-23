import serial
import serial.tools.list_ports

import socketio
import time

RUNSOCKET = True
# sends pot data to server


def get_serial_ports():  # get arduino port
    return [
        port.device
        for port in serial.tools.list_ports.comports()
        if "usb" in port.device or "acm" in port.device or "tty" in port.device
    ]


def connect():
    if RUNSOCKET:
        print("Connecting to server...")
    ports = get_serial_ports()

    while len(ports) == 0:
        # print("No serial ports found. Retrying...")
        time.sleep(5)
        ports = get_serial_ports()
    print("Serial ports found:", ports)
    SERIAL_PORT = ports[0]
    BAUD_RATE = 115200
    global ser
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)

    global sio
    sio = socketio.Client()


def sendData():
    if RUNSOCKET:
        sio.connect("http://localhost:5001", transports=["websocket"])
    time.sleep(0.2)

    dataPrev = [0.0] * 4

    try:
        while True:
            line = ser.readline().decode().strip()
            if not line:
                continue

            values = line.split("|")

            try:
                data = [float(val) for val in values[:4]]
            except ValueError:
                print("Invalid data received:", values)
                continue
            send = any(abs(data[i] - dataPrev[i]) >= 5 for i in range(4))
            # map to 0-1

            if send:
                dataPrev = data.copy()

                data = [round(val / 1023, 2) for val in data]

                data = [0 if val <= 0.01 else 1 if val >= 0.99 else val for val in data]

                if RUNSOCKET:
                    sio.emit("Pot Data", data)
                else:
                    print("Pot Data", data)

    finally:
        print("Closed")
        ser.close()
        sio.disconnect()


def main():
    while True:
        try:
            connect()
            sendData()

        except KeyboardInterrupt:
            ser.close()
            sio.disconnect()
            break
        except Exception as e:

            print("Error:", e)
            ser.close()
            sio.disconnect()


if __name__ == "__main__":
    RUNSOCKET = False
    main()
