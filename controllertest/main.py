import pygame
import time
import serial

pygame.init()

pygame.joystick.init()

while pygame.joystick.get_count() == 0:
    time.sleep(0.1)
    print("No joystick detected yet")
    pygame.joystick.quit()
    pygame.joystick.init()

print("Joystick Initialized")

joystick_count = pygame.joystick.get_count()
for x in range(joystick_count):
    joystick = pygame.joystick.Joystick(x)
    joystick.init()

ser = serial.Serial('/dev/cu.usbmodem1101', 9600, timeout=1)
ser.flush()

lastSent = 0
# tolerance = 2
while True:
    angle = int(((joystick.get_axis(1)+1)/2)*145)+21
    
    if((angle>=0 and angle<=180)):
        # print(angle)
        if((lastSent!=angle)):
        # if((abs(lastSent - angle) > tolerance)):
            print(angle)
            ser.write(bytes(str(angle)+"\n", 'UTF-8'))
            
            lastSent = angle
    pygame.event.get()
    time.sleep(0.05)