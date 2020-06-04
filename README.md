### Installation

The easiest way is to run the docker container and set it to restart always. This basically makes it a system service that will always run.

```shell
docker run --restart=always -e MODBUS_HOST=192.168.1.1 solaredge_modbus_mqtt:latest
```