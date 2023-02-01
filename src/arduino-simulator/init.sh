#!/bin/sh
#
#   init.sh: script to start the tasks to be executed by the container that simulates the Arduino
#
export $(cat /opt/mqtt-client/.env | grep "#" -v)
echo "MQTT Server: ${MQTT_SERVER_HOST}"
echo "MQTT Port: ${MQTT_SERVER_PORT}"

sleep 10 # Wait a few seconds for the broker to be operational

/opt/mqtt-client/temperature-pub.sh & 
/opt/mqtt-client/alarm-sub.sh