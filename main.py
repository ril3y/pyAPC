import time
import argparse
from typing import Dict, Union, List
import paho.mqtt.client as mqtt

import pyHive
from pyAPC import PyAPC, OutletCommand
from pyHive import PyHive
from configparser import ConfigParser

UPDATE_CHECK_PERIOD = 300


class MqttClient:
    def __init__(self, server):
        self.client = mqtt.Client()
        self.server = server
        self.client.on_connect = self.on_connect()

    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(self):
        self.client.connect(self.server, 1883, 60)

        self.client.publish("mining_monitor", payload="CONNECTED", retain=False)

        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        self.client.subscribe("$SYS/#")

    def loop(self):
        self.client.loop(timeout=.2)

    def publish(self, topic, payload):
        self.client.publish(topic, payload)

def send_mqtt_reboot_message(workshop_oulet):
    client.publish("mining_monitor", workshop_oulet)


if __name__ == "__main__":
    # parser = argparse.ArgumentParser()
    # parser.add_argument("--apc_server", type=str)
    # parser.add_argument("--pairs", "-of", type=str)
    #
    # args=parser.parse_args()
    #
    # server = args.apc_server
    # pairs = args.pairs

    # config_object = ConfigParser()
    # with open('server1_outlet_pairs.conf', 'r') as conf:
    #     config_object = ConfigParser()
    #     config_object.read(conf)
    # workshopairs = config_object["DEFAULT"]

    # MQTT Configuration for Alerts
    client = MqttClient("mqtt.iot")

    server = 'http://192.168.1.218'
    server214 = 'http://192.168.1.214'

    # Setup or APC servers here
    apc218 = PyAPC(server, "apc", "apc")
    apc214 = PyAPC(server214, "apc", "apc")
    apc218.login()
    apc214.login()

    # Edit this to correspond to your setup.
    WORKSHOP1_OUTLET_PAIR = {"outlets": [1, 9],  "server": apc218, "device_name": "Workshop1"}
    WORKSHOP2_OUTLET_PAIR = {"outlets": [2, 10], "server": apc214, "device_name": "Workshop2"}
    WORKSHOP3_OUTLET_PAIR = {"outlets": [1, 9],  "server": apc218, "device_name": "Workshop3"}

    with open("hive_api_key.txt", "r") as f:
        api_key = f.read()
    hive = PyHive(api_key)
    workers_offline = []
    print("Starting Rig Monitor")
    _run = True

    while _run:
        client.loop()

        workers_offline = hive.check_workers_offline()
        print(f'Time: {time.ctime()}')
        hive.print_data()
        client.publish("mining_monitor", "Everything is fine")
        for w in workers_offline:
            print(f'WORKER OFFLINE: {w.name}')
            if w.name == "WORKSHOP#1":
                print(
                    f'REBOOTING OUTLETS -  {WORKSHOP1_OUTLET_PAIR["device_name"]} on {WORKSHOP1_OUTLET_PAIR["server"].get_url()}')
                apc218.apply_outlet_command(OutletCommand.REBOOT_IMMEDIATE, WORKSHOP1_OUTLET_PAIR['outlets'])
                msg = str({"time": time.ctime(), "message": "rebooting", "outlets"
                : WORKSHOP1_OUTLET_PAIR['outlets']})
                client.publish("mining_monitor", client.publish("mining_monitor", msg))
            if w.name == "WORKSHOP#2":
                print(
                    f'REBOOTING OUTLETS -  {WORKSHOP2_OUTLET_PAIR["device_name"]} on {WORKSHOP2_OUTLET_PAIR["server"].get_url()}')
                apc214.apply_outlet_command(OutletCommand.REBOOT_IMMEDIATE, WORKSHOP2_OUTLET_PAIR['outlets'])
            if w.name == "WORKSHOP#3":
                print(
                    f'REBOOTING OUTLETS -  {WORKSHOP3_OUTLET_PAIR["device_name"]} on {WORKSHOP3_OUTLET_PAIR["server"].get_url()}')
                apc218.apply_outlet_command(OutletCommand.REBOOT_IMMEDIATE, WORKSHOP3_OUTLET_PAIR['outlets'])

        time.sleep(UPDATE_CHECK_PERIOD)
