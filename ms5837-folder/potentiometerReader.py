import serial
import socketio
import time

SERIAL_PORT = "/dev/cu.usbmodem2101"
BAUD_RATE = 115200

ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)

sio = socketio.Client()

def sendData():
    sio.connect("http://127.0.0.1:5001", transports=["websocket"])  
    time.sleep(0.2)

    dataPrev = [0.0] * 4 

    try:
        while True:
            line = ser.readline().decode().strip()
            if not line:
                continue 

            values = line.split('|')
            
            try:
                data = [float(val) for val in values[:4]]
            except ValueError:
                print("Invalid data received:", values)
                continue 

            send = any(abs(data[i] - dataPrev[i]) >= 5 for i in range(4))

            if send:
                print("Sending:", data)
                sio.emit("Pot Data", data)
                dataPrev = data.copy() 

    except KeyboardInterrupt:
        print("Stopping...")
    finally:
        print("Closed")
        ser.close()
        sio.disconnect()

sendData()
