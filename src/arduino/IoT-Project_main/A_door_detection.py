import time,network,sys # Libraries for code
from lsm6dsox import LSM6DSOX   # Arduino library
from machine import Pin, I2C    # Arduino PIN module
from wifi_credentials import SSID, PASSWORD,HOST,PORT   # Wifi_credentials.py library
from simple import MQTTClient #MQTT simple library

# =================================================================
# Arduino configuration
# =================================================================
INT_MODE = True         # Enable interrupts
INT_FLAG = False        # At start, no pending interrupts
# I2C object initialization
i2c = I2C(0, scl=Pin(13), sda=Pin(12))

# =================================================================
# MLC configuration
# =================================================================
# The gyroscope is configured with ±2000 dps full scale and 52 Hz output data rate.
# Only one feature is computed:
# Mean on gyroscope X-axis
# Pre-trained model definition and IMU object initialization
UCF_FILE = "lsm6dsox_open_close_door.ucf"
UCF_LABELS = {0: "Closing", 4: "Opening", 8: "Still"}
lsm = LSM6DSOX(i2c, gyro_odr = 52, accel_odr = 26, gyro_scale = 2000, accel_scale = 2, ucf = UCF_FILE)
# Interrupt handler function
def imu_int_handler(pin):
    # This function defines the IMU interrupt handler function
    global INT_FLAG
    INT_FLAG = True

    # External interrupt configuration (IMU)
if (INT_MODE == True):
    int_pin = Pin(24)
    int_pin.irq(handler = imu_int_handler, trigger = Pin.IRQ_RISING)

print("\n--------------------------------")
print("- Opening/Closing door example -")
print("--------------------------------\n")
print("- MLC configured...\n")
# =================================================================
# WLAN configuration
# =================================================================

print("Trying to connect... (may take a while)...\n")
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

def connect_to_wifi():
    wlan.connect(SSID,PASSWORD) # Hotspot
    time.sleep(2)
    print('\n-Connected to hotspot:')
    print(wlan.isconnected())

def reconnect_to_wifi():
    print("Trying WLAN connection again...\n")
    time.sleep(.5)
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    connect_to_wifi()
# =================================================================
# MQTT configuration
# =================================================================
mqtt_server = '172.20.10.7' #Hotspot IPv4
client_id = 'arduino001'
topic_pub = b'/ul/4pacosaucedo2guadiaro4s40d59ov/arduino001/attrs'
topic_msg = b'door|movement'

def connect_to_mqtt(client_id, broker_ip):
    client = MQTTClient(client_id, broker_ip)
    client.connect()
    print("Connection to MQTT succesfull.\n")
    return client

def send_to_mqtt(client, topic, message):
    ##print("Sending data...")
    client.publish(topic, message)

def disconnect_from_mqtt(client):
    client.disconnect()


try:
    connect_to_wifi()
    client = connect_to_mqtt(client_id, mqtt_server)

except OSError as e:
    print("WLAN connection failed.\n'")
    reconnect_to_wifi()
    print("or")
    print('Failed to connect to the MQTT Broker. Reconnecting...\n')

while (True):
    if (INT_MODE):
        if (INT_FLAG):
            INT_FLAG = False
            buf = lsm.read_mlc_output()
            if buf is not None:
                print("-", UCF_LABELS[buf[0]])
                send_to_mqtt(client, topic_msg, topic_msg)
    else:
        buf = lsm.read_mlc_output()
        if (buf != None):
            print(UCF_LABELS[buf[0]])
            send_to_mqtt(client, topic_msg, topic_msg)

disconnect_from_mqtt(client)
