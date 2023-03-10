/*
  @file: fiware-iot-upo.ino
  @author: Paco Saucedo
  @brief: sketch que interactua con un broker MQTT para:
          - Publicar la temperatura leída desde un sensor.
          - Suscribirse a un tópico para recibir comandos para hacer sonar un actuador alarma.
          En el formato de payloads de publicación y suscripción se usa el protocolo Ultralight 2.0 (ul)
*/
#include <SPI.h>
#include <WiFiNINA.h>
#include <PubSubClient.h>
#include <Arduino_LSM6DSOX.h>

#define UPDATE_TIME_INTERVAL 2000
#define MQTT_BROKER_PORT     1883
#define MQTT_BUFFER_SIZE     2048

char ssid[] = "SECRET_SSID";
char pass[] = "SECRET_PASS";

const char  clientID[]   = "arduino_client";
// Cambiar por la dirección IP del equipo en el que se ejecute el broker MQTT
const char* mqttBrokerIp = "172.20.10.7";

const String temperatureTopic = "/ul/4pacosaucedo2guadiaro4s40d59ov/temperature001/attrs";

const String ulTemperatureMsgPrefix = "t|";

long lastPublishMillis   = 0;

WiFiClient client;

PubSubClient mqttClient(client);
int status = WL_IDLE_STATUS;
/**
   Configuración inicial
*/
void setup() {
  Serial.begin(9600);
  if (!IMU.begin()) {
    Serial.println("Failed to initialize IMU!");
    while (1);
  }
   if (WiFi.status() == WL_NO_MODULE) {
  Serial.println("Communication with WiFi module failed!");
   // don't continue
   while (true);
 }
  connectWifi();

  mqttClient.setServer(mqttBrokerIp, MQTT_BROKER_PORT);
  mqttClient.setCallback(mqttSubscriptionCallback);
  mqttClient.setBufferSize(MQTT_BUFFER_SIZE);
}

/**
   Bucle principal del programa
*/
void loop() {
  if (WiFi.status() != WL_CONNECTED) {
    connectWifi();
  }

  if (!mqttClient.connected()) {
    mqttConnect();

    
  }

  mqttClient.loop();

  if (abs(millis() - lastPublishMillis) > UPDATE_TIME_INTERVAL) {
    publishTemperature();

    lastPublishMillis = millis();
  }

  delay(50);
}

/**
   Método que conecta a la red WiFi
*/
void connectWifi() {
  if (WiFi.status() == WL_NO_SHIELD) {
    Serial.println("WiFi shield not present");
    while (true);
  }

  while ( status != WL_CONNECTED) {
    Serial.print("Attempting to connect to Network named: ");
    Serial.println(ssid);

    status = WiFi.begin(ssid, pass);

    delay(10000);
  }

  printWiFiStatus();
}

/**
   Método que muestra el estado de la conexión a la red WiFi
*/
void printWiFiStatus() {
  Serial.print("SSID: ");
  Serial.println(WiFi.SSID());

  IPAddress ip = WiFi.localIP();
  Serial.print("IP Address: ");
  Serial.println(ip);

  long rssi = WiFi.RSSI();
  Serial.print("Signal strength (RSSI):");
  Serial.print(rssi);
  Serial.println(" dBm");
}

/**
   Método que conecta al broker MQTT
*/
void mqttConnect() {
  while ( !mqttClient.connected() ) {
    if ( mqttClient.connect( clientID ) ) {
      Serial.print( "MQTT to " );
      Serial.print( mqttBrokerIp );
      Serial.print (" at port ");
      Serial.print( MQTT_BROKER_PORT );
      Serial.println( " successful." );
    } else {
      Serial.print( "MQTT connection failed, rc = " );
      Serial.print( mqttClient.state() );
      Serial.println( " Will try again in a few seconds" );
      delay( 10000 );
    }
  }
}

/**
   Método que gestiona la suscripción a los canales de actuadores del broker MQTT
*/
void mqttSubscriptionCallback(char* topic, byte* payload, unsigned int length) {
  String topicString = String(topic);
  String payloadString = getPayloadString(payload, length);

  Serial.print("Message arrived [");
  Serial.print(topicString);
  Serial.print("], payload: ");
  Serial.println(payloadString);
}

/**
   Método de conversión de los bytes recibidos a String
*/
String getPayloadString(byte* payload, unsigned int length) {
  char payloadCharArray[length + 1];

  memcpy(payloadCharArray, payload, length);
  payloadCharArray[length] = '\0';

  return String(payloadCharArray);
}

/**
   Método de envío de un mensaje a un tópico del broker MQTT
*/
void publishData(String topic, String payload) {
  mqttClient.publish(topic.c_str(), payload.c_str());

  Serial.print("Publishing data, Topic = ");
  Serial.print(topic);
  Serial.print(", Payload = ");
  Serial.println(payload);
}

/**
   Método que devuelve la medida del sensor de temperatura
*/
float readTemperatureSensor() {
  float tempDegrees = 0.0;
  int temperature_deg = 0;
  if (IMU.temperatureAvailable()){
    
    IMU.readTemperature(temperature_deg);
    Serial.print("LSM6DSOX Temperature = ");
    Serial.print(temperature_deg);
    Serial.println(" °C");
    temperature_deg = (float)tempDegrees;
  }
  return tempDegrees;
}

/**
   Método de envío del dato de temperatura broker MQTT
*/
void publishTemperature(void) {
  String payload = ulTemperatureMsgPrefix;
  payload.concat(String(readTemperatureSensor()));

  publishData(temperatureTopic, payload);
}