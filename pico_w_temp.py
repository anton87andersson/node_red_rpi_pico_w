import network
import time
from machine import Pin
from umqtt.simple import MQTTClient
from machine import ADC

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("SSID","PASSWORD")
time.sleep(5)
print(wlan.isconnected())
print(wlan.ifconfig())

adc = machine.ADC(4) 
LED = machine.Pin("LED", machine.Pin.OUT)

#Topic in this case will be hello
topic_pub = 'hello'

# Setup for the mqqt broker
mqtt_server = 'IP-TO-BROKER'
client_id = 'PicoW'
user_t = 'YOUR-USERNAME'
password_t = 'YOUR-PASSWORD'

last_message = 0
message_interval = 5
counter = 0

# the following will set the seconds between 2 keep alive messages
keep_alive=30

#MQTT connect
def mqtt_connect():
    client = MQTTClient(client_id, mqtt_server, user=user_t, password=password_t, keepalive=60)
    client.connect()
    print('Connected to %s MQTT Broker'%(mqtt_server))
    return client

#reconnect & reset
def reconnect():
    print('Failed to connected to MQTT Broker. Reconnecting...')
    time.sleep(5)
    machine.reset()

# This code is executed once a new message is published
def new_message_callback(topic, msg):
    topic , msg=topic.decode('ascii') , msg.decode('ascii')
    print("Topic: "+topic+" | Message: "+msg)
    if msg == "off":
        LED.off()
    if msg == "on":
        LED.on()

try:
    client = mqtt_connect()
    client.set_callback(new_message_callback)
    client.subscribe(topic_pub.encode('utf-8'))

except OSError as e:
    reconnect()

last_message=time.time()

# Main loop
while True:
    try:
        client.check_msg()
        time.sleep(0.001)
        if (time.time() - last_message) > keep_alive:
            ADC_voltage = adc.read_u16() * (3.3 / (65535))
            temperature_celcius = 27 - (ADC_voltage - 0.706)/0.001721
            temp_fahrenheit=32+(1.8*temperature_celcius)
            client.publish(topic_pub, str(round(temperature_celcius,1)))
            last_message = time.time()
              

    except OSError as e:
        print(e)
        reconnect()
        pass

client.disconnect()
