#!/usr/bin/env python


from __future__ import print_function
from concurrent.futures import TimeoutError
from builtins import input
import os
import re
import sys
import errno
import binascii
import wyzesense
import paho.mqtt.client as mqtt
import time
device='/dev/hidraw0'
client = None
def register_sensor(client):
    topic = "homeassistant/binary_sensor/garageSonar/config"
    Payload = "{\"name\":\"garageSonar\", \"device_class\":\"motion\",\"off_delay\":\"1\", \"state_topic\":\"garageSonar/state\",\"unique_id\":\"garageSonar\",\"value_template\":\"{{ value_json.STATE }}\"}"
    client.publish(topic,Payload,retain=True)
def on_message(client,userdata,message):
    if "online" in str(message.payload.decode("utf-8")):
        register_sensor(client)    
def on_event(ws, e):
    global client
    s = "[%s][%s]" % (e.Timestamp.strftime("%Y-%m-%d %H:%M:%S"), e.MAC)
    if e.Type == 'state':
        s += "StateEvent: sensor_type=%s, state=%s, battery=%d, signal=%d" % e.Data
    else:
        s += "RawEvent: type=%s, data=%r" % (e.Type, e.Data)
    print(s)
    payload="{\"status\":\"on\",\"time\":\"%s\"}" % (time.time())
    if e.MAC == "778A799A":
        client.publish("hall1",payload)
    if e.MAC == "7785FED1":
        client.publish("hall2",payload)
    if e.MAC == "777C30AC":
        client.publish("sonar1",payload)
    if e.MAC == "7785FED1":
        home_assistant_payload="{\"STATE\":\"ON\", \"unique_id\":\"garageSonar\"}"
        client.publish("garageSonar/state",payload=home_assistant_payload,retain=True)
def main():
    global client
    time.sleep(1)
    USER=os.getenv('MQTT_USERNAME')
    PASS=os.getenv('MQTT_PASSWORD')
    client = mqtt.Client()
    client.username_pw_set(USER,PASS)
    client.connect("192.168.0.48",1883,60)
    register_sensor(client)
    client.subscribe("homeassistant/status",0)
    client.on_message = on_message
    client.loop_start()
    try:
        ws = wyzesense.Open(device, on_event)
        if not ws:
            print("Open wyzesense gateway failed")
            return 1
    except IOError:
        print("No device found on path %r" % device)
        return 2
    try:
        while True:
            time.sleep(.1)
    finally:
        ws.Stop()

    return 0


if __name__ == '__main__':
    main()
