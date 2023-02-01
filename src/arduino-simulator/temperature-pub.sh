#!/bin/sh
#
#   script that simulates Arduino’s behavior in sending messages
# Scripts are in (Ultralight 2.0) format
#
#   Dependencia: mosquitto-clients 
#
echo "Sendind messages to topic: ${MQTT_SEND_TO_TOPIC}"

while [ 1 ]
do
    temperature=$((20 + RANDOM % 10))
    echo "Sending random... $temperature Celsius"

    mosquitto_pub -h ${MQTT_SERVER_HOST} -p ${MQTT_SERVER_PORT} -m "t|$temperature" -t ${MQTT_SEND_TO_TOPIC}

    sleep 2
done