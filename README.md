# Arduino_Project-IOT
* Welcome to my first official Arduino IOT project.
* The goal of this project is to create a smart-home implementation using my Arduino RP2040.  

![smart home plan](content/Screenshots/Smart_home_plan.drawio.png)

## Todo list
- [x] Implement all Docker images.
- [ ] Connect Arduino to the MQTT client and publish the data.
- [ ] Visualize data from Arduino on Grafana dashboard 
- [ ] Start a Telegram bot that will notify you about events.
- [ ] Enable more functionalitios for InfluxDB

## Bugs list
- [ ] https://github.com/nightguarder/Arduino_Project-IOT/issues/1 

## Orion Context Broker
> The brain of your IOT network. Orion is a C++ implementation of the NGSIv2 REST API binding developed as a part of the FIWARE platform.
* To access Orion go to: `http://localhost:1026/v2` 
## IOT Agent
> An IoT Agent is a component that lets a group of devices sends their data to and be managed from a Context Broker using their own native protocols. The API used here is NGSIv2.
* To access IOT Agent go to: `http://localhost:4041/iot/about`
* [Implementation example](https://fiware-tutorials.readthedocs.io/en/latest/iot-agent.html#22-request)

## MQTT Broker
> MQTT is a publish-subscribe-based messaging protocol used in the internet of Things
* Serves as a middleman between IOT devices (sensors) and Fiware network. 
## Telegraf
>Telegraf is a server-based agent for collecting and sending all metrics and events from databases, systems, and **IoT sensors**.
* The raw data is sent to **InfluxDB**, therefore you can visualize them in **Grafana**.
* How does it work? [Telegraf intro](https://www.influxdata.com/time-series-platform/telegraf/)
## InfluxDB
>Smart data collector for your IOT devices.
* Introduction to InfluxDB [Documentation](https://awesome.influxdata.com/docs/part-1/introduction-to-influxdb/)
## MongoDB
>Simple database image to hold temporary data.
* Used by the Orion Context Broker to hold context data information such as data entities, subscriptions and registrations
* Used by the IoT Agent to hold device information such as device URLs and Keys
## Grafana 
> Visually display the data from IOT devices (sensors).
* By default Grafana will have an InfluxDB configured with the available data.   
* To access grafana go to: `http://localhost:30001`   
## Orion Context Broker
>
## Prerequsities & References:
* Must have knowledge: [Orion Context basics](https://youtu.be/pK4GgYjlmdY)
* Fiware IOT MQTT documentation: [Fiware docs](https://fiware-tutorials.readthedocs.io/en/latest/iot-over-mqtt.html)
* Fiware IOT MQTT repository: [Github repo](https://github.com/FIWARE/tutorials.IoT-over-MQTT)

## Checklist:
[x] Installed Docker on your system. *previous experience recommended*
[x] Arduino (RP2040)
   - Arduino device or extensions that can connect to MQTT broker via Wi-fi
[x] Postman or cURL command interface
[x] Programming skills
[x] Patience & time
