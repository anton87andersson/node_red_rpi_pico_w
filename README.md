# Raspberry Pi Pico W
Use Raspberry Pi Pico W with Node-Red to send data from onboard temprature-sensor via umqtt

# Publish to mqqt broker
```python
# Topic in this case will be hello
topic_pub = 'hello'

# Setup for the mqqt broker
mqtt_server = 'IP-TO-BROKER'
client_id = 'PicoW'
user_t = 'YOUR-USERNAME'
password_t = 'YOUR-PASSWORD'
```

# Read from mqqt broker
```python
# Just an example how to read from the topic, turning the onboard LED on / off

LED = machine.Pin("LED", machine.Pin.OUT)

# When the msg in topic hello is off turn off LED
if msg == "off":
  LED.off()
# When the msg in topic hello is on turn on LED
if msg == "on":
  LED.on()
```
