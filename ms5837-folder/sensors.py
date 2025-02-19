import time
import board
import busio
import adafruit_bme680
import adafruit_bno055
import ms5837

# import socketio


# sio = socketio.Client()
# isConnected = True


# @sio.event
# def connect():
#     global isConnected
#     isConnected = True
#     print("I'm connected!")


# @sio.event
# def disconnect():
#     global isConnected
#     isConnected = False
#     print("I'm disconnected!")

# print("connecting")
# sio.connect("http://10.78.19.223:5001", transports=["websocket"])
# print("connected")


bme680 = None
bno055 = None
ms5837_sensor = None

i2c = busio.I2C(board.SCL, board.SDA)
print("i2c initialised")

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


print("ALLL GOOD ")


def bme_data():
    try:

        return {
            "Tempurature": bme680.temperature,
            "Humidity": bme680.humidity,
            "Pressure": bme680.pressure,
        }

    except Exception:
        return "BME680 Error"


def bno_data():
    try:
        return {
            "Accelerometer": bno055.acceleration,
            "Euler": bno055.euler,
        }
    # (
    #         f"Accelerometer (m/s^2): {bno055.acceleration}, "
    #         f"Gyroscope (deg/s): {bno055.gyro}, "
    #         f"Magnetometer (microteslas): {bno055.magnetic}, "
    #         f"Euler angles: {bno055.euler}, "
    #         f"Temperature: {bno055.temperature}°C, "
    #         f"Quaternion: {bno055.quaternion}, "
    #         f"Linear acceleration (m/s^2): {bno055.linear_acceleration}, "
    #         f"Gravity (m/s^2): {bno055.gravity}"
    #     )
    except Exception:
        return "BNO055 Error"


def ms_data():
    try:
        if not ms5837_sensor.read():
            return "MS5837 Read Error"
        return {
            "Depth": ms5837_sensor.depth(),
            "Pressure": ms5837_sensor.pressure(ms5837.UNITS_psi),
        }

    except Exception:
        return "MS5837 Error"


while True:
    bme680_output = bme_data() if bme680 else "BME680: Not connected"
    bno055_output = bno_data() if bno055 else "BNO055: Not connected"
    ms5837_output = ms_data() if ms5837_sensor else "MS5837: Not connected"

    # print(f"{bme680_output}")
    # print(f"{bno055_output}")
    # print(f"{ms5837_output}")
    # print()
    sio.emit(
        "sensors",
        {"bme680": bme680_output, "bno055": bno055_output, "ms5837": ms5837_output},
    )

    time.sleep(0.1)
