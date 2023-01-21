# Arduino_Project-IOT
* Welcome to my first official Arduino IOT project.
* The goal of this project is to create a smart-home implementation using my Arduino RP2040.  

## Todo list
- [x] Implement all Docker images.
- [ ] Connect Arduino to the MQTT client and publish the data.
- [ ] Visualize data from Arduino on Grafana dashboard 
- [ ] Start a Telegram bot that will notify you about events.

## Bugs list
- [ ] #1 

## MQTT Broker
> MQTT is a publish-subscribe-based messaging protocol used in the internet of Things
* Serves as a middleman between IOT devices (sensors) and Fiware network. 
## Grafana info
> Visually display the data from IOT devices (sensors)
* By default Grafana will have an InfluxDB configured with the available data.   
* To access grafana go to: `http://localhost:30001`   

## Prerequsities & References:
* Must have knowledge: [Orion Context basics](https://youtu.be/pK4GgYjlmdY)
* Fiware IOT MQTT documentation: [Fiware docs](https://fiware-tutorials.readthedocs.io/en/latest/iot-over-mqtt.html)
* Fiware IOT MQTT repository: [Github repo](https://github.com/FIWARE/tutorials.IoT-over-MQTT)

1. Docker
   - All docker images running (total: 8)
2. Arduino
   - Arduino device or extensions that can connect to MQTT broker via Wi-fi
3. 
