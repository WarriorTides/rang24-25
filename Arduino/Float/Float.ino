#include <ESP8266WiFi.h>
#include <espnow.h>
#include <Wire.h>
#include <ArduinoOTA.h>
#include "MS5837.h"

#define IN1_PIN D6
#define IN2_PIN D4

MS5837 sensor;

// Topside Mac Adress
uint8_t broadcastAddress[] = {0xE8, 0x06, 0x90, 0x73, 0x79, 0x1C};

// AP Mode credentials- For OTA
const char *apSSID = "ESP_Float";
const char *apPassword = "float1234";

// Profiling logic variables
const long interval = 5000;  // reading interval in milliseconds
unsigned expandtime = 18000; // time to expand the float in milliseconds
long waitTime = 0;           // time to wait before next action in milliseconds

unsigned long lastFloatAction = 0;
unsigned long lastSampleTime = 0;
bool floatIsStopped = true;
char nextCommand = 's';
int datacount = 0;
int datasendindex = 0;

// Data storage
int pressureReadings[150];
int depthReadings[150];
int timeReadings[150];

// ESP now requires a structure for sending and receiving data

struct control_message
{
    char c;
    int val;
};
struct send_message
{
    int p;
    int d;
    int t;
};

control_message ControlData;
send_message SendData;

void setup()
{
    Serial.begin(115200);
    pinMode(IN1_PIN, OUTPUT);
    pinMode(IN2_PIN, OUTPUT);
    stopMotor();
    Wire.begin();

    while (!sensor.init())
    {
        Serial.println("Sensor init failed. Check connections.");
        delay(5000);
    }
    sensor.setModel(MS5837::MS5837_02BA);
    sensor.setFluidDensity(997);

    WiFi.mode(WIFI_AP_STA);
    WiFi.softAP(apSSID, apPassword);
    Serial.print("AP IP Address: ");
    Serial.println(WiFi.softAPIP());

    setupOTA();
    setupESPNOW();
}

void loop()
{
    ArduinoOTA.handle(); // chilling here to check for OTA updates
    unsigned long now = millis();

    if (!floatIsStopped && now - lastFloatAction >= expandtime) // Check if the float has expanded for the required time
    {
        stopMotor();
    }

    if (now - lastFloatAction >= waitTime + expandtime)
    {
        handleNextCommand();
    }

    if (now - lastSampleTime >= interval)
    {
        lastSampleTime = now;
        collectData();
        sendDataESPNow();
    }
}

void setupOTA()
{
    ArduinoOTA.setHostname("float-module");
    ArduinoOTA.onStart([]()
                       { Serial.println("Starting OTA..."); });
    ArduinoOTA.onEnd([]()
                     { Serial.println("OTA Complete."); });
    ArduinoOTA.onProgress([](unsigned int p, unsigned int t)
                          { Serial.printf("OTA Progress: %u%%\r", (p * 100) / t); });
    ArduinoOTA.onError([](ota_error_t err)
                       { Serial.printf("OTA Error [%u]\n", err); });
    ArduinoOTA.begin();
    Serial.println("OTA Ready");
}

void setupESPNOW()
{
    if (esp_now_init() != 0)
    {
        Serial.println("ESP-NOW init failed");
        return;
    }
    esp_now_set_self_role(ESP_NOW_ROLE_COMBO);
    esp_now_register_send_cb(onDataSent);
    esp_now_add_peer(broadcastAddress, ESP_NOW_ROLE_COMBO, 1, NULL, 0);
    esp_now_register_recv_cb(onDataReceived);
    Serial.println("ESP-NOW ready");
}

void onDataSent(uint8_t *mac, uint8_t status)
{
    Serial.print("Send Status: ");
    Serial.println(status == 0 ? "Success" : "Fail");
    if (datacount >= datasendindex)
        espNOWSend(datasendindex);
    else
        datacount = 0;
}

void onDataReceived(uint8_t *mac, uint8_t *data, uint8_t len)
{
    memcpy(&ControlData, data, sizeof(ControlData));
    Serial.printf("Received: %c, %d\n", ControlData.c, ControlData.val);

    if (ControlData.c == 't')
        expandtime = ControlData.val;
    else
    {
        waitTime = ControlData.val;
        lastFloatAction = millis();
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
        stopMotor();
        nextCommand = 's';
    }
}

void handleNextCommand()
{
    if (nextCommand == 'f')
        forward();
    else if (nextCommand == 'b')
        back();
    else
        stopMotor();
    lastFloatAction = millis();
    nextCommand = 's';
}

void collectData()
{
    sensor.read();
    if (datacount < 150)
    {
        pressureReadings[datacount] = (int)(sensor.pressure() * 100);
        depthReadings[datacount] = (int)(sensor.depth() * 100);
        timeReadings[datacount] = millis() / 100;
        datacount++;
    }
}

void sendDataESPNow()
{
    SendData.p = pressureReadings[datasendindex];
    SendData.d = depthReadings[datasendindex];
    SendData.t = timeReadings[datasendindex];
    datasendindex++;
    esp_now_send(broadcastAddress, (uint8_t *)&SendData, sizeof(SendData));
}

void forward()
{
    Serial.println("Motor forward");
    floatIsStopped = false;
    digitalWrite(IN1_PIN, HIGH);
    digitalWrite(IN2_PIN, LOW);
}

void back()
{
    Serial.println("Motor backward");
    floatIsStopped = false;
    digitalWrite(IN1_PIN, LOW);
    digitalWrite(IN2_PIN, HIGH);
}

void stopMotor()
{
    if (!floatIsStopped)
    {
        Serial.println("Motor stopped");
        digitalWrite(IN1_PIN, LOW);
        digitalWrite(IN2_PIN, LOW);
        floatIsStopped = true;
    }
}
