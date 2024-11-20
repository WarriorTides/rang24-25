
#include <UIPEthernet.h>
#include "utility/logging.h"

#include <Servo.h>

EthernetUDP udp;

const int THRUSTER_COUNT = 8;
const int SERVO_COUNT = 4;
const int ACTUATOR_COUNT = 2;

int RIGHT_RPWM = 33;
int RIGHT_LPWM = 35;
int LEFT_RPWM = 37;
int LEFT_LPWM = 39;
int sensorPin1 = A0;
int sensorPin2 = A1;

int sensorVal1, sensorVal2;
int Speed = 255;
float strokeLength = 4.0;
float extensionLength1, extensionLength2;
float targetPositionInches1 = 0;
float targetPositionInches2 = 0;
float errorTolerance = 0.05;

int maxAnalogReading = 1023;
int minAnalogReading = 0;

Servo thrusters[THRUSTER_COUNT];
const byte thrusterPins[] = {17, 15, 13, 11, 3, 5, 7, 9};
const byte servoPins[] = {14, 12, 10, 8};
bool enabled = false;
int servoAngles[] = {90, 90, 90, 90};

Servo servos[SERVO_COUNT];

String sendData = "";

IPAddress sendIP;
uint16_t sendPort;

void setup()
{
    Serial.begin(9600);

    for (int i = 0; i < THRUSTER_COUNT; i++)
    {
        thrusters[i].attach(thrusterPins[i]);
        thrusters[i].writeMicroseconds(1500);
    }
    for (int i = 0; i < SERVO_COUNT; i++)
    {
        servos[i].attach(servoPins[i]);
        servos[i].write(servoAngles[i]);
    }
    pinMode(RIGHT_RPWM, OUTPUT);
    pinMode(RIGHT_LPWM, OUTPUT);
    pinMode(LEFT_RPWM, OUTPUT);
    pinMode(LEFT_LPWM, OUTPUT);
    pinMode(sensorPin1, INPUT);
    pinMode(sensorPin2, INPUT);

    uint8_t mac[6] = {0x00, 0x01, 0x02, 0x03, 0x04, 0x05};
    Ethernet.begin(mac, IPAddress(192, 168, 1, 151));

    int success = udp.begin(8888);

    Serial.print("initialize: ");
    Serial.println(success ? "success" : "failed");
    Serial.println(Ethernet.localIP());
}

void loop()
{

    int sensorVal1 = analogRead(sensorPin1);
    int sensorVal2 = analogRead(sensorPin2);

    extensionLength1 = mapfloat(sensorVal1, minAnalogReading, maxAnalogReading, 0.0, strokeLength);
    extensionLength2 = mapfloat(sensorVal2, minAnalogReading, maxAnalogReading, 0.0, strokeLength);

    controlActuator(extensionLength1, targetPositionInches1, RIGHT_RPWM, RIGHT_LPWM);
    controlActuator(extensionLength2, targetPositionInches2, LEFT_RPWM, LEFT_LPWM);

    // check for new udp-packet:
    int size = udp.parsePacket();
    if (size > 0)
    {
        do
        {
            char *msg = (char *)malloc(size + 1);
            int len = udp.read(msg, size + 1);
            msg[len] = 0;

            char command = msg[0];
            String data = String(msg).substring(2);
            sendData = String(msg);

            if (command == 'c')
            {
                // Convert String into an Int Array that contains microseconds for all 8 thrusters and Servo Angles
                int output[THRUSTER_COUNT + SERVO_COUNT + ACTUATOR_COUNT];
                boolean done = false;
                int i = 0;
                while (!done)
                {
                    int index = data.indexOf(',');
                    if (index == -1)
                    {
                        done = true;
                        output[i] = data.toInt();
                        // Serial.println(output[i]);
                    }
                    else
                    {
                        output[i] = data.substring(0, index).toInt();
                        // Serial.println(outputx[i]);
                        data = data.substring(index + 1);
                        i++;
                    }
                }
                // write to thrusters

                for (int i = 0; i < THRUSTER_COUNT; i++)
                {
                    thrusters[i].writeMicroseconds(output[i]);
                }

                // write to servos
                for (int i = 0; i < SERVO_COUNT; i++)
                {
                    servos[i].write(output[i + THRUSTER_COUNT]);
                }

                targetPositionInches1 = output[THRUSTER_COUNT + SERVO_COUNT] / 100;
                targetPositionInches2 = output[THRUSTER_COUNT + SERVO_COUNT + 1] / 100;
            }

            else if (command == 's')
            {

                for (int i = 0; i < THRUSTER_COUNT; i++)
                {
                    thrusters[i].attach(thrusterPins[i]);
                    thrusters[i].writeMicroseconds(1500);
                }
                for (int i = 0; i < SERVO_COUNT; i++)
                {
                    servos[i].attach(servoPins[i]);
                    servos[i].write(servoAngles[i]);
                }
            }

            free(msg);
        } while ((size = udp.available()) > 0);
        // finish reading this packet:
        udp.flush();

        int success;
        do
        {

            // Serial.print(("remote ip: "));

            // Serial.println(udp.remoteIP());

            // Serial.print(("remote port: "));
            // Serial.println(udp.remotePort());

            // send new packet back to ip/port of client. This also
            // configures the current connection to ignore packets from
            // other clients!

            success = udp.beginPacket(udp.remoteIP(), udp.remotePort());
            sendIP = udp.remoteIP();
            sendPort = udp.remotePort();

        } while (!success);
        success = udp.println(sendData);

        // Serial.print(("bytes written: "));
        // Serial.println(success);

        success = udp.endPacket();

        // Serial.print(("endPacket: "));
        // Serial.println(success ? "success" : "failed");

        // udp.stop();
        // // restart with new connection to receive packets from other clients
        // success = udp.begin(5000);

        // Serial.print(("restart connection: "));
        // Serial.println(success ? "success" : "failed");
    }
}

float mapfloat(float x, float inputMin, float inputMax, float outputMin, float outputMax)
{
    return (x - inputMin) * (outputMax - outputMin) / (inputMax - inputMin) + outputMin;
}

void controlActuator(float extnsionLength, float targetPosition, int RPWM, int LPWM)
{
    e float error = abs(extensionLength - targetPosition);

    if (error <= errorTolerance)
    {
        driveActuator(0, 0, RPWM, LPWM);
        Serial.println("Stopped");
    }
    else if (extensionLength < targetPosition)
    {
        driveActuator(1, Speed, RPWM, LPWM);
        Serial.println("Extending...");
    }
    else if (extensionLength > targetPosition)
    {
        driveActuator(-1, Speed, RPWM, LPWM);
        Serial.println("Retracting...");
    }
}

void driveActuator(int Direction, int Speed, int RPWM, int LPWM)
{
    switch (Direction)
    {
    case 1:
        analogWrite(RPWM, Speed);
        analogWrite(LPWM, 0);
        break;

    case 0:
        analogWrite(RPWM, 0);
        analogWrite(LPWM, 0);
        break;

    case -1:
        analogWrite(RPWM, 0);
        analogWrite(LPWM, Speed);
        break;
    }
}
