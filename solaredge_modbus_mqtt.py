#!/usr/bin/env python3

import argparse
import json
import os
import solaredge_modbus
import sys
import time
import paho.mqtt.client as mqtt
from solaredge_modbus_mqtt import SolarData
from pymodbus.exceptions import ConnectionException

if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("--modbus-host", type=str, default=os.environ.get('MODBUS_HOST', '127.0.0.1'), help="ModbusTCP address")
    argparser.add_argument("--modbus-port", type=int, default=os.environ.get('MODBUS_PORT', 1502), help="ModbusTCP port")
    argparser.add_argument("--modbus-timeout", type=int, default=os.environ.get('MODBUS_TIMEOUT', 1), help="Connection timeout")
    argparser.add_argument("--modbus-unit", type=int, default=os.environ.get('MODBUS_UNIT', 1), help="Modbus unit")

    argparser.add_argument("--mqtt-host", type=str, default=os.environ.get('MQTT_HOST', '127.0.0.1'), help="MQTT Host")
    argparser.add_argument("--mqtt-port", type=int, default=os.environ.get('MQTT_PORT', 1883), help="MQTT port")
    argparser.add_argument("--mqtt-user", type=str, default=os.environ.get('MQTT_USER', None), help="MQTT Username")
    argparser.add_argument("--mqtt-pass", type=str, default=os.environ.get('MQTT_PASS', None), help="MQTT Password")

    argparser.add_argument("--poll-interval", type=int, default=os.environ.get('POLL_INTERVAL', 3), help="Waiting time between each poll")

    args = argparser.parse_args()

    try:
        mqtt = mqtt.Client(client_id="", clean_session=True, userdata=None, protocol=mqtt.MQTTv311, transport="tcp")
        mqtt.username_pw_set(args.mqtt_user, args.mqtt_pass)
        mqtt.connect(args.mqtt_host, args.mqtt_port, 60)
    except OSError as err:
        print("Cannot connect to MQTT on {0}:{1}, error: {2}".format(args.mqtt_host, args.mqtt_port, err))
        sys.exit(1)

    inverter = solaredge_modbus.Inverter(
        host=args.modbus_host,
        port=args.modbus_port,
        timeout=args.modbus_timeout,
        unit=args.modbus_unit
    )

    run = True
    publishedAutoDiscovery = False
    while run:
        try:
            solar_data = SolarData(inverter.read_all())
        except ConnectionException as err:
            print("Cannot connect to SolarEdge Modbus server on {0}:{1}, error: {2}".format(args.modbus_host, args.modbus_port, err))
            sys.exit(2)

        mqtt.loop()

        if (publishedAutoDiscovery == False):
            for k, v in solar_data.data.items():
                message = {
                    "name": "SolarEdge " + k.replace("_", " ").title(),
                    "unique_id": "solaredge_" + k,
                    "unit_of_measurement": SolarData.fields[k]['unit'] if 'unit' in SolarData.fields[k] else '',
                    "state_topic": "home/hal_beneden/sensor/solaredge_inverter/" + k,
                    "force_update": "True",
                    "device": {
                        "identifiers": ["solaredge_inverter"],
                        "name": "SolarEdge Inverter"
                    }
                }
                mqtt.publish(
                    'test/homeassistant/sensor/solaredge_inverter/' + str(k) + '/config', 
                    json.dumps(message),
                    qos=0, 
                    retain=True
                )

            publishedAutoDiscovery = True


        for k, v in solar_data.data.items():
            mqtt.publish('test/home/hal_beneden/sensor/solaredge_inverter/' + k, payload=str(v), qos=0, retain=False)

        time.sleep(args.poll_interval)