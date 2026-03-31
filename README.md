# Fire-TV Proximity Control using AWS IoT & ESP8266
A real-time IoT-based automation system that pauses and resumes a TV when a person gets too close, using ultrasonic sensing, cloud-based decision making, and local device control.
### Built with AWS IoT Core, AWS Lambda, ESP8266, and ADB.
## Problem Statement
Prolonged close-distance TV viewing can harm eyesight, especially for children.
This project automatically:  
>Pauses TV when someone gets too close  
>Resumes when they move away  
## Architecture Diagram

<img width="316" height="871" alt="Screenshot 2026-03-29 233226" src="https://github.com/user-attachments/assets/6f5c8274-946d-4b8e-bf49-3896d71a3a80" />


## Circuit Diagram
<img width="1280" height="1024" alt="ChatGPT Image Mar 30, 2026, 09_48_22 PM" src="https://github.com/user-attachments/assets/7b1adaf3-7587-4489-b65d-13fed9d0b298" />
   

## Workflow  
The ESP8266 measures distance using an ultrasonic sensor and publishes the data to an AWS IoT topic (e.g., kids/distance, though the topic name can be customized). Once the data is published, an IoT Core rule processes it and triggers a Lambda function based on the configured logic. The Lambda function determines the appropriate action (Play or Pause) depending on the detected distance and publishes the result back to another IoT topic. A laptop, continuously subscribed to this topic, listens for any state changes and executes the corresponding ADB commands to control playback on the Amazon Fire TV.       
## Tech Stack
* ESP8266 (NodeMCU)  
* Ultrasonic Sensor (HC-SR04)  
* Python MQTT (Message Queuing Telemetry Transport) Clien    
* ADB (Android Debug Bridge)  
* AWS IoT Core  
* AWS Lambda    
## Hardware Setup
### Components
* ESP8266 (NodeMCU)
* HC-SR04 Ultrasonic Sensor
### Wiring
| Ultrasonic	| ESP8266                                                                             |
|:------------|------------------------------------------------------------------------------------:|
| VCC	        | 5V                                                                                  | 
| GND	        | GND                                                                                 |
| TRIG	      | D6                                                                                  |
| ECHO	      | D7 (via voltage divider ⚠️ only if you are using external voltage supply to HC-SR04)|

## AWS Setup
1. Create an IoT Thing with an appropriate access policy configured.  
   * Download the certificates, which include the Root CA, client certificate and private key.  
2. Create an IoT rule that uses AWS Lambda as the endpoint to process and forward the JSON data.   
   * Role Query: SELECT * FROM 'kids/distance'  
3. Set up a Lambda, with appropriate the policy to receive and send the data to IOT-Core thing. [**Note:** Python language is used to building lambda logic. File is app.py]    
## Laptop Setup
### Requirements
1. Python 3      
2. paho-mqtt (Connect to AWS IOT-Core)
3. ADB installed (Connect & run adb commands to control the fire-tv)    
## Network Configuration
* Set up the static IP on the Fire TV, so that you won't be greeted with a new IP when the Fire TV reboots.    
* Make certain that the laptop and Fire TV are connected to the same subnet. The laptop has an open port 5555 for connecting to the Fire TV.   
* The laptop initiates connection to AWS IoT on port 8883. AWS uses the same connection to send messages    
**Note:** This method does not necessitate port forwarding or VPN connection. A Raspberry Pi can also be used instead of a laptop.   
## Future Enhancements
* Real-time dashboard (CloudWatch / Grafana)
* Mobile notifications (SNS)
* Camera-based AI detection
* Auto-start laptop service
* Terraform deployment
