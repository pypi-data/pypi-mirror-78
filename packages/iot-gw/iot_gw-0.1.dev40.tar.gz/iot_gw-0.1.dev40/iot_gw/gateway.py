import time
import json
import logging
import io
import os
import yaml
from flask import Flask, request
from .bridge import bridge_adapter_factory
from .proxy.mqtt import MqttProxy
from .device import DeviceManager

app = Flask(__name__)
bridge = None
proxy = None
device_manager = None
configuration = None

def init(config_path=None, default_config=None):
    global bridge, proxy, device_manager, configuration
    configuration = _load_config(config_path,default_config)
    device_manager = DeviceManager(configuration['storage'])
    bridge = bridge_adapter_factory.create(device_manager,configuration['bridge'],
        on_config_handler=_on_config,
        on_commands_handler=_on_commands)
    bridge.connect()
    if 'mqtt' in configuration:
        proxy=MqttProxy(configuration['mqtt'],bridge)
        proxy.connect()
        logging.debug("MQTT proxy is enable: {}".format(proxy.is_connected()))
    else:
        logging.debug('MQTT proxy is disabled')
    return app

@app.route('/',methods = ['GET'])
def index():
    return 'OK'

@app.route('/device/<device_id>',methods = ['GET'])
def get_device(device_id):
    device = device_manager.get_device(device_id)
    return json.dumps(device.toJson())

def _load_config(config_path='/etc/iot-gw/configuration.yml',default_config=None):
    if config_path is None or not os.path.isfile(config_path):
        result = default_config
    else:
        with io.open(config_path,'r') as stream:
            result = yaml.safe_load(stream)
    return result

def _init_mqtt(config,adapter):
    global proxy
    proxy = MqttProxy(
        config['login'],
        config['password'],
        config['ca_certs_file'] if 'ca_certs_file' in config else None,
        on_attach=adapter.attach,
        on_unattach=adapter.unattach,
        on_state=adapter.publish_state,
        on_event=adapter.publish_event)    
    proxy.connect(config['hostname'],config['port'])
    


def _on_config(device_id,configuration):
    global proxy
    proxy.config(device_id,configuration)

def _on_commands(device_id,commands):
    global proxy
    proxy.commands(device_id,commands)


