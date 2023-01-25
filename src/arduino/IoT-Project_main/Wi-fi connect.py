# Untitled - By: cyrils - Wed Jan 4 2023
import network, machine, time, sys, random
from machine import Pin
from simple import MQTTClient
# Variables
# WLAN

Wifi_name='iCyril’s13'     # Network SSID
Password_name='McTrump74'      # Network key
HOST = ''   # Use first available interface
PORT = 8000 # Arbitrary non-privileged port
#MQTT
mqtt_server = '172.20.10.7'#Hotspot IP adress
client_id = 'arduino001'
topic_pub = '/ul/4pacosaucedo2guadiaro4s40d59ov/temperature001/attrs'
topic_pref = 't|'

# Init wlan module and connect to network
print("Trying to connect... (may take a while)...")
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
# connect and wait to connect
wlan.connect(Wifi_name,Password_name)
time.sleep(3)
connect_status = wlan.isconnected()
if connect_status:
    print("Is connected to: " + Wifi_name)
else:
    print("Connection unsuccessful. " + ("True" if connect_status else "False"))
    wlan.active(False)


sensor = Pin(16, Pin.IN)

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

try:
    client = mqtt_connect()
except OSError as e:
    reconnect()

def publishTemperature(client,topic_pref,topic):
    temperature = random.uniform(0, 30)
    payload = topic_pref + str(temperature)
    print("topic:")
    print(topic)
    print("payload:")
    print(payload)
    client.publish(topic,payload)

publishTemperature(client,topic_pref,topic_pub)
publishTemperature(client,topic_pref,topic_pub)
publishTemperature(client,topic_pref,topic_pub)
publishTemperature(client,topic_pref,topic_pub)
publishTemperature(client,topic_pref,topic_pub)
