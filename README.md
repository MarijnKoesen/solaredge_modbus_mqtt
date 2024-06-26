## Usage

### Installation

The easiest way this is to run the docker container and set it to restart always. This basically makes it a system service that will always run.

To make it safe and avoid passing credentials we're using a configuration file.

```shell
mkdir /etc/solaredge_modbus_mqtt
chmod 700 /etc/solaredge_modbus_mqtt
cp config.yaml-dist /etc/solaredge_modbus_mqtt/config.yaml
docker run --detach --name=solaredge_modbus_mqtt --restart=always --volume=/etc/solaredge_modbus_mqtt/config.yaml:/app/config.yaml marijnkoesen/solaredge_modbus_mqtt:latest
```


### Uninstall

```shell
docker update --restart=no solaredge_modbus_mqtt
docker stop solaredge_modbus_mqtt
```


### Update

```shell
docker update --restart=no solaredge_modbus_mqtt
docker stop solaredge_modbus_mqtt
docker rm solaredge_modbus_mqtt
docker run --detach --name=solaredge_modbus_mqtt --restart=always --volume=/etc/solaredge_modbus_mqtt/config.yaml:/app/config.yaml marijnkoesen/solaredge_modbus_mqtt:latest
```



## For developers

### Building and running the docker image

```shell
docker build -t solaredge_modbus_mqtt:latest .
or
docker buildx build --platform linux/amd64 solaredge_modbus_mqtt:latest .

cp config.yaml-dist config.yaml
docker run --volume=$PWD/config.yaml:/app/config.yaml solaredge_modbus_mqtt:latest
```


### Running without docker

```shell
pip3 install -r requirements.txt
cp config.yaml-dist config.yaml
python3 solaredge_modbus_mqtt.py
```


### Running tests

```shell
pip3 install -r requirements.txt
python3 -m unittest
```
