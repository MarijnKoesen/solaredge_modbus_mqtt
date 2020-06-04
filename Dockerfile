FROM python:3

RUN mkdir /app && cd /app
WORKDIR /app

COPY requirements.txt /app
RUN pip install -r requirements.txt

COPY solaredge_modbus_mqtt.py /app
COPY solaredge_modbus_mqtt /app/solaredge_modbus_mqtt

#ENV MQTT_HOST 
#ENV MQTT_USER
#ENV MQTT_PASS
#ENV MQTT_PORT

CMD ./solaredge_modbus_mqtt.py