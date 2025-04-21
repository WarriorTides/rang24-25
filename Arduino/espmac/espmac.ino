#if defined(ESP8266)
#include <ESP8266WiFi.h>
#elif defined(ESP32)
#include <WiFi.h>
#endif

void setup()
{
    Serial.begin(115200);
    Serial.println();
    Serial.println();
    Serial.println();
    WiFi.mode(WIFI_STA);
    WiFi.disconnect();
    delay(100);

    uint8_t mac[6];
    WiFi.macAddress(mac);

    Serial.print("{");
    for (int i = 0; i < 6; i++)
    {
        Serial.print("0x");
        if (mac[i] < 0x10)
            Serial.print("0"); // leading zero
        Serial.print(mac[i], HEX);
        if (i < 5)
            Serial.print(", ");
    }
    Serial.println("};");
}

void loop()
{
    // no loop actions
}
