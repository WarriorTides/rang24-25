import time
import board
import busio
import adafruit_bno055

# Create the I2C interface
i2c = busio.I2C(board.SCL, board.SDA)

# Initialize the BNO055 sensor
sensor = adafruit_bno055.BNO055_I2C(i2c)

# Optional: Check if a second address is needed (0x29)
# sensor = adafruit_bno055.BNO055_I2C(i2c, address=0x29)

while True:
    print("Temperature: {}°C".format(sensor.temperature))
    print("Accelerometer (m/s^2): {}".format(sensor.acceleration))
    print("Magnetometer (microteslas): {}".format(sensor.magnetic))
    print("Gyroscope (deg/s): {}".format(sensor.gyro))
    print("Euler angles: {}".format(sensor.euler))
    print("Quaternion: {}".format(sensor.quaternion))
    print("Linear acceleration (m/s^2): {}".format(sensor.linear_acceleration))
    print("Gravity (m/s^2): {}".format(sensor.gravity))
    print()

    # Wait for 1 second before the next reading
    time.sleep(1)
