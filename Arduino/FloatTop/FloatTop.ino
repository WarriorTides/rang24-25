#include <WiFi.h>
#include <esp_now.h>

// REPLACE WITH THE MAC Address of your receiver
uint8_t broadcastAddress[] = {0xCE, 0x50, 0xE3, 0x5A, 0xDF, 0xE7};

String input = "";

// Updates every 10 seconds (unused here, but kept for parity)
const long interval = 10000;

// Structure to send commands
typedef struct control_message {
  char c;
  int val;
} control_message;

// Structure to receive sensor data
typedef struct reciv_message {
  int p;
  int d;
  int t;
} reciv_message;

control_message ControlData;
reciv_message recivReadings;

// Callback when data is sent
void OnDataSent(const uint8_t *mac_addr, esp_now_send_status_t status) {
  Serial.println();
  Serial.print("Last Packet Send Status: ");
  Serial.println(status == ESP_NOW_SEND_SUCCESS ? "Delivery success" : "Delivery fail");
}

  // Callback when data is received
void OnDataRecv(const esp_now_recv_info_t *recvInfo, const uint8_t *incomingData, int len) {
  memcpy(&recivReadings, incomingData, sizeof(recivReadings));

  const uint8_t *mac = recvInfo->src_addr; // Extract MAC address from recvInfo

  Serial.print("Bytes received: ");
  Serial.println(len);
  Serial.print("From MAC: ");
  for (int i = 0; i < 6; i++) {
    Serial.printf("%02X", mac[i]);
    if (i < 5) Serial.print(":");
  }
  Serial.println();
  // if(recivReadings.d )
  Serial.print("DATA:  Team: RN37  Pressure: ");
  Serial.print(float(recivReadings.p) / 100.0);
  Serial.print(" KPa  Depth: ");
  Serial.print(float(recivReadings.d) / 100.0);
  Serial.print(" m  Local Time: ");
  Serial.print(float(recivReadings.t) / 10.0);
  Serial.println(" s");

}


void setup() {
  Serial.begin(115200);

  // Set device as a Wi-Fi Station
  WiFi.mode(WIFI_STA);
  WiFi.disconnect();

  // Initialize ESP-NOW
  if (esp_now_init() != ESP_OK) {
    Serial.println("Error initializing ESP-NOW");
    return;
  }

  // Register callbacks
  esp_now_register_send_cb(OnDataSent);
  esp_now_register_recv_cb(OnDataRecv);

  // Register peer
  esp_now_peer_info_t peerInfo = {};
  memcpy(peerInfo.peer_addr, broadcastAddress, 6);
  peerInfo.channel = 1;  
  peerInfo.encrypt = false;
  if (!esp_now_is_peer_exist(broadcastAddress)) {
    if (esp_now_add_peer(&peerInfo) != ESP_OK) {
      Serial.println("Failed to add peer");
      return;
    }
  }

  Serial.println("ESP32 ESP-NOW setup complete");
}

void loop() {
  if (Serial.available()) {
    input = Serial.readStringUntil('\n');
    int idx = input.indexOf('/');
    if (idx > 0) {
      ControlData.c   = input.charAt(0);
      ControlData.val = input.substring(idx + 1).toInt() * 1000;
      Serial.printf("Sending: %c, %d\n", ControlData.c, ControlData.val);
      esp_err_t result = esp_now_send(broadcastAddress, (uint8_t *)&ControlData, sizeof(ControlData));
      if (result != ESP_OK) {
        Serial.println("Error sending ESP-NOW message");
      }
    }
  }
}
