import time
import board
import busio
import adafruit_bme680

# Create I2C interface
i2c = busio.I2C(board.SCL, board.SDA)

# Initialize the BME680 sensor
try:
    bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c, address=0x77)
except:
    print("bme failed")
    
# Set the sea-level pressure (in hPa) at your location for accurate altitude reading
bme680.sea_level_pressure = 1013.25

while True:
    print(f"Temperature: {bme680.temperature:.2f} °C")
    print(f"Gas: {bme680.gas:.2f} ohm")
    print(f"Humidity: {bme680.humidity:.2f} %")
    print(f"Pressure: {bme680.pressure:.2f} hPa")
    print(f"Altitude: {bme680.altitude:.2f} meters")

    # Wait for 2 seconds before reading again
    time.sleep(0.1)
