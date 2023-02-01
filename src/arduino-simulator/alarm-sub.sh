#!/bin/sh
#
#    Subscribe to the alarm topics saved in Orion..
#
#   Dependencia: mosquitto-clients 
#
echo "Alarms are subscribed to ${MQTT_SUBSCRIBE_TO_TOPIC}"

mosquitto_sub -h ${MQTT_SERVER_HOST} -p ${MQTT_SERVER_PORT} -t ${MQTT_SUBSCRIBE_TO_TOPIC}