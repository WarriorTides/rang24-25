
#include <UIPEthernet.h>
#include "utility/logging.h"

#include <Servo.h>

dataStorage datastore;

EthernetUDP udp;

#define THRUSTER_COUNT = 8
#define SERVO_COUNT = 4

Servo thrusters[THRUSTER_COUNT];
const byte thrusterPins[] = {6, 8, 10, 12, 2, 4, 14, 16};
const byte servoPins[] = {9, 5, 7, 3};
bool enabled = false;
int servoAngles[] = {90, 90, 90, 90}
// cosnt
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

    uint8_t mac[6] = {0x00, 0x01, 0x02, 0x03, 0x04, 0x05};
    Ethernet.begin(mac, IPAddress(192, 168, 1, 151));

    int success = udp.begin(8888);

    Serial.print("initialize: ");
    Serial.println(success ? "success" : "failed");
    Serial.println(Ethernet.localIP());
}

void loop()
{

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
            sendData = String(msg)

                if (command == 'c')
            {
                // Convert String into an Int Array that contains microseconds for all 8 thrusters and Servo Angles
                int output[THRUSTER_COUNT + SERVO_COUNT];
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