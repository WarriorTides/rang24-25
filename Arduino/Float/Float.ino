#include <ESP8266WiFi.h>
#include <espnow.h>
#include <Wire.h>
#include <ArduinoOTA.h>
#include "MS5837.h"

// Pin definitions
#define IN1_PIN D6
#define IN2_PIN D4

MS5837 sensor;

// ESP-NOW peer MAC address
uint8_t broadcastAddress[] = {0xE8, 0x06, 0x90, 0x73, 0x79, 0x1C};

// AP credentials
const char *apSSID = "ESP_Float";
const char *apPassword = "float1234";

// Control variables
const long interval = 5000;
unsigned expandtime = 18000;
long waitTime = 0;
unsigned long previousMillisFloat = 0;
bool floatIsStopped = true;
char nextCommand = 's';
int datacount = 0;
int datasendindex = 0;
unsigned long previousMillis = 0;

// Message structures
typedef struct control_message
{
    char c;
    int val;
} control_message;

typedef struct send_message
{
    int p;
    int d;
    int t;
} send_message;

control_message ControlData;
send_message sendReadings;

int preassurReadings[150];
int timeReadings[150];
int depthReadings[150];

// ESP-NOW Send Callback
void OnDataSent(uint8_t *mac_addr, uint8_t sendStatus)
{
    Serial.print("Last Packet Send Status: ");
    if (sendStatus == 0)
    {
        Serial.println("Delivery success");
        if (datacount >= datasendindex)
        {
            espNOWSend(datasendindex);
        }
        else
        {
            datacount = 0;
        }
    }
    else
    {
        Serial.println("Delivery fail");
        datasendindex = 0;
    }
}

// ESP-NOW Receive Callback
void OnDataRecv(uint8_t *mac, uint8_t *incomingData, uint8_t len)
{
    memcpy(&ControlData, incomingData, sizeof(ControlData));
    Serial.printf("Bytes received: %d\n", len);
    Serial.printf("Command: %c, Time: %d\n", ControlData.c, ControlData.val);

    if (ControlData.c == 't')
    {
        expandtime = ControlData.val;
    }
    else
    {
        waitTime = ControlData.val;
        previousMillisFloat = millis();
    }

    if (ControlData.c == 'f')
    {
        forward();
        nextCommand = 'b';
    }
    else if (ControlData.c == 'b')
    {
        back();
        nextCommand = 'f';
    }
    else if (ControlData.c == 's')
    {
        stop();
        nextCommand = 's';
    }
}

void setup()
{
    Serial.begin(115200);
    pinMode(IN1_PIN, OUTPUT);
    pinMode(IN2_PIN, OUTPUT);
    stop();
    Wire.begin();

    // Initialize sensor
    while (!sensor.init())
    {
        Serial.println("Init failed! Check SDA/SCL wiring.");
        delay(5000);
    }

    sensor.setModel(MS5837::MS5837_02BA);
    sensor.setFluidDensity(997); // freshwater

    // Setup Access Point
    WiFi.mode(WIFI_AP_STA);
    WiFi.softAP(apSSID, apPassword);
    delay(1000);
    Serial.print("Access Point IP: ");
    Serial.println(WiFi.softAPIP());

    // Init ESP-NOW
    if (esp_now_init() != 0)
    {
        Serial.println("Error initializing ESP-NOW");
        return;
    }

    esp_now_set_self_role(ESP_NOW_ROLE_COMBO);
    esp_now_register_send_cb(OnDataSent);
    esp_now_add_peer(broadcastAddress, ESP_NOW_ROLE_COMBO, 1, NULL, 0);
    esp_now_register_recv_cb(OnDataRecv);

    // OTA Setup
    ArduinoOTA.setHostname("float-module");
    ArduinoOTA.onStart([]()
                       { Serial.println("Start updating firmware..."); });
    ArduinoOTA.onEnd([]()
                     { Serial.println("\nUpdate complete."); });
    ArduinoOTA.onProgress([](unsigned int progress, unsigned int total)
                          { Serial.printf("Progress: %u%%\r", (progress / (total / 100))); });
    ArduinoOTA.onError([](ota_error_t error)
                       {
    Serial.printf("Error[%u]: ", error);
    if (error == OTA_AUTH_ERROR) Serial.println("Auth Failed");
    else if (error == OTA_BEGIN_ERROR) Serial.println("Begin Failed");
    else if (error == OTA_CONNECT_ERROR) Serial.println("Connect Failed");
    else if (error == OTA_RECEIVE_ERROR) Serial.println("Receive Failed");
    else if (error == OTA_END_ERROR) Serial.println("End Failed"); });
    ArduinoOTA.begin();
    Serial.println("OTA Ready. Connect to 'ESP_Float' and upload via network port.");
}

void loop()
{
    ArduinoOTA.handle(); // OTA loop

    unsigned long currentMillis = millis();

    if (currentMillis - previousMillisFloat >= expandtime && !floatIsStopped)
    {
        stop();
    }

    if (currentMillis - previousMillisFloat >= (waitTime + expandtime))
    {
        if (nextCommand == 'f')
        {
            forward();
            previousMillisFloat = millis();
        }
        else if (nextCommand == 'b')
        {
            back();
            previousMillisFloat = millis();
        }
        else if (nextCommand == 's')
        {
            stop();
        }
        nextCommand = 's';
    }

    if (currentMillis - previousMillis >= interval)
    {
        previousMillis = currentMillis;
        sensor.read();
        preassurReadings[datacount] = int(round(sensor.pressure() * 100));
        depthReadings[datacount] = int(round(sensor.depth() * 100));
        timeReadings[datacount] = int(round(millis() / 100));
        datacount++;

        espNOWSend(0);
    }
}

void stop()
{
    if (!floatIsStopped)
    {
        Serial.println("Stopping motor...");
        digitalWrite(IN1_PIN, LOW);
        digitalWrite(IN2_PIN, LOW);
        floatIsStopped = true;
    }
}

void back()
{
    Serial.println("Moving backward...");
    floatIsStopped = false;
    digitalWrite(IN1_PIN, LOW);
    digitalWrite(IN2_PIN, HIGH);
}

void forward()
{
    Serial.println("Moving forward...");
    floatIsStopped = false;
    digitalWrite(IN1_PIN, HIGH);
    digitalWrite(IN2_PIN, LOW);
}

void espNOWSend(int index)
{
    sendReadings.p = preassurReadings[index];
    sendReadings.d = depthReadings[index];
    sendReadings.t = timeReadings[index];
    datasendindex++;
    Serial.printf("Sending index %d of %d | Depth: %.2f\n", index, datacount, depthReadings[index] / 100.0);
    esp_now_send(broadcastAddress, (uint8_t *)&sendReadings, sizeof(sendReadings));
}
