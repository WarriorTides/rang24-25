import time
import board
import busio
import adafruit_bme680
import adafruit_bno055
import ms5837
import zmq
import json

# Initialize ZMQ publisher
context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:5555")  # Listen on all network interfaces at port 5555

# Initialize I2C
i2c = busio.I2C(board.SCL, board.SDA)
print("i2c initialized")

# Initialize Sensors
bme680 = None
bno055 = None
ms5837_sensor = None

try:
    bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c, address=0x77)
    bme680.sea_level_pressure = 1013.25
    print("BME GOOD!")
except Exception as e:
    print("BME failed:", e)

try:
    bno055 = adafruit_bno055.BNO055_I2C(i2c)
    print("IMU GOOD!")
except Exception as e:
    print("BNO failed:", e)

try:
    ms5837_sensor = ms5837.MS5837_02BA()
    print("DEPTH GOOD!")

    if not ms5837_sensor.init():
        print("MS failed")
        ms5837_sensor = None
except Exception as e:
    print("MS failed:", e)

print("ALL GOOD")


def get_bme_data():
    try:
        return {
            "Temperature": bme680.temperature,
            "Humidity": bme680.humidity,
            "Pressure": bme680.pressure,
        }
    except Exception:
        return {"Error": "BME680 Error"}


def get_bno_data():
    try:
        return {
            "Accelerometer": bno055.acceleration,
            "Euler": bno055.euler,
        }
    except Exception:
        return {"Error": "BNO055 Error"}


def get_ms_data():
    try:
        if not ms5837_sensor.read():
            return {"Error": "MS5837 Read Error"}
        return {
            "Depth": ms5837_sensor.depth(),
            "Pressure": ms5837_sensor.pressure(ms5837.UNITS_psi),
        }
    except Exception:
        return {"Error": "MS5837 Error"}


# ** Main Loop: Publish Sensor Data **
while True:
    sensor_data = {
        "BME": get_bme_data() if bme680 else {"Error": "BME680: Not connected"},
        "IMU": get_bno_data() if bno055 else {"Error": "BNO055: Not connected"},
        "DEPTH": get_ms_data() if ms5837_sensor else {"Error": "MS5837: Not connected"},
    }

    # Send data as JSON over ZMQ
    socket.send_string(json.dumps(sensor_data))

    # Print for debugging
    print(sensor_data)

    time.sleep(0.5)  # Adjust frequency as needed
