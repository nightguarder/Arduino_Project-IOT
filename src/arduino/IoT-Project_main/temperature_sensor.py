# Untitled - By: cyrils - Wed Jan 25 2023

import time,network,sys,machine # Libraries for code
from lsm6dsox import LSM6DSOX   # Arduino library
from machine import Pin, I2C    # Arduino PIN module
from wifi_credentials import SSID, PASSWORD,HOST,PORT   # Wifi_credentials.py library
from simple import MQTTClient #MQTT simple library

#MQTT SETUP
mqtt_server = '172.20.10.7'#Hotspot IP adress
client_id = 'arduino001'
topic_pub = '/ul/4pacosaucedo2guadiaro4s40d59ov/temperature001/attrs'
topic_pref = 't|'

# I2C object initialization
i2c = machine.I2C(0, scl=machine.Pin(13), sda=machine.Pin(12))

LSM6DSOX_I2C_ADDRESS = 0x6A # I2C address of the LSM6DSOX sensor
TEMP_OUT_L = 0x20
TEMP_OUT_H = 0x21
# IMU object initialization
imu = LSM6DSOX(i2c)

# Init wlan module and connect to network
print("Trying to connect... (may take a while)...")
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
# connect and wait to connect
wlan.connect(SSID,PASSWORD)
time.sleep(3)
connect_status = wlan.isconnected()
if connect_status:
    print("Is connected to: " + SSID)
else:
    print("Connection unsuccessful. " + ("True" if connect_status else "False"))
    wlan.active(False)
def mqtt_connect():
    client = MQTTClient(client_id, mqtt_server, keepalive=3600)
    client.connect()
    print('Connected to %s MQTT Broker'%(mqtt_server))
    return client

def reconnect():
    #Check if the devices run on the same network
    #Check if the mosquitto broker is running
    print('Failed to connect to the MQTT Broker. Reconnecting...')
    time.sleep(3)
    machine.reset()

def publishData(client,topic, payload):
    print("topic: " + topic)
    print("payload: " + payload)
    client.publish(topic, payload)
def read_and_publish_temperature():
    prevTemperature = None # Reset before running the function again
    while True:
        raw_temp = i2c.readfrom_mem(LSM6DSOX_I2C_ADDRESS, TEMP_OUT_L, 2)
        raw_temp = (raw_temp[1] << 8) | raw_temp[0]
        temperature = (raw_temp / 256) + 20
        if temperature != prevTemperature:
            prevTemperature = temperature
            payload = topic_pref + str(temperature)
            publishData(client,topic_pub, payload)
        # Delay for some time before reading the sensor again
        time.sleep(3)

try:
    client = mqtt_connect()
    read_and_publish_temperature()
except OSError as e:
    reconnect()


