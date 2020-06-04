#!/usr/bin/env python3

import argparse
import json
import os
import solaredge_modbus
import sys
import time
import paho.mqtt.client as mqtt
import yaml
from solaredge_modbus_mqtt import SolarData
from pymodbus.exceptions import ConnectionException

if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument('--config', type=str, default=os.environ.get('CONFIG_FILE', 'config.yaml'), help='Path to the config.yaml')
    args = argparser.parse_args()

    with open(args.config, 'r') as stream:
        try:
            config = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)    

    try:
        mqtt = mqtt.Client(client_id='', clean_session=True, userdata=None, protocol=mqtt.MQTTv311, transport='tcp')
        mqtt.username_pw_set(config['mqtt']['user'], config['mqtt']['pass'])
        mqtt.connect(config['mqtt']['host'], config['mqtt']['port'], 60)
    except OSError as err:
        print('Cannot connect to MQTT on {0}:{1}, error: {2}'.format(config['mqtt']['host'], config['mqtt']['port'], err))
        sys.exit(1)

    inverter = solaredge_modbus.Inverter(
        host=config['modbus']['host'],
        port=config['modbus']['port'],
        timeout=config['modbus']['timeout'],
        unit=config['modbus']['unit']
    )

    run = True
    publishedAutoDiscovery = False
    while run:
        try:
            solar_data = SolarData(inverter.read_all())
        except ConnectionException as err:
            print('Cannot connect to SolarEdge Modbus server on {0}:{1}, error: {2}'.format(config['modbus']['host'], config['modbus']['port'], err))
            sys.exit(2)

        mqtt.loop()

        if (publishedAutoDiscovery == False):
            for k, v in solar_data.data.items():
                message = {
                    'name': 'SolarEdge ' + k.replace('_', ' ').title(),
                    'unique_id': 'solaredge_' + k,
                    'unit_of_measurement': SolarData.fields[k]['unit'] if 'unit' in SolarData.fields[k] else '',
                    'state_topic': config['mqtt']['state_topic'] + '/' + k,
                    'force_update': 'True',
                    'device': {
                        'identifiers': ['solaredge_inverter'],
                        'name': 'SolarEdge Inverter'
                    }
                }
                mqtt.publish(
                    config['mqtt']['auto_discovery_topic'] + '/' + str(k) + '/config', 
                    json.dumps(message),
                    qos=0, 
                    retain=True
                )

            publishedAutoDiscovery = True

        for k, v in solar_data.data.items():
            mqtt.publish(config['mqtt']['state_topic'] + '/' + k, payload=str(v), qos=0, retain=False)

        time.sleep(config['poll_interval'])