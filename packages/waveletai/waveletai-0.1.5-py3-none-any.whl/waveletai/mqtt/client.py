import paho.mqtt.client as paho
from waveletai import logger
import ssl
from simplejson import dumps, loads, JSONDecodeError
from waveletai.entities.mqtt_repo import MqttRepo


class MqttClient:
    def __init__(self, mqtt_repo):
        if isinstance(mqtt_repo, MqttRepo):
            self._client = paho.Client()
            self.__host = mqtt_repo.host
            self.__port = mqtt_repo.port
            self._client.username_pw_set(mqtt_repo.username, mqtt_repo.password)
            self.stopped = False
            self.__is_connected = False
            self.__connect_callback = None
            self._client.on_connect = self._on_connect
            self._client.on_log = self._on_log
            self._client.on_publish = self._on_publish
            self._client.on_message = self._on_message
            self._client.on_disconnect = self._on_disconnect
        else:
            raise TypeError("MqttClient require <MqttRepo> class type as input")

    def _on_log(self, client, user_data, level, buf):
        if isinstance(buf, Exception):
            logger.exception(buf)
        else:
            logger.debug("%s - %s - %s - %s", client, user_data, level, buf)

    def _on_publish(self, client, userdata, result):
        logger.debug("Data published to WaveletAI")
        pass

    def _on_disconnect(self, client, user_data, result_code):
        prev_level = logger.level
        logger.setLevel("DEBUG")
        logger.debug("Disconnected client: %s, user data: %s, result code: %s", str(client), str(user_data),
                     str(result_code))
        logger.setLevel(prev_level)

    def _on_connect(self, client, user_data, flags, result_code, *extra_params):
        result_codes = {
            1: "incorrect protocol version",
            2: "invalid client identifier",
            3: "server unavailable",
            4: "bad username or password",
            5: "not authorised",
        }
        if self.__connect_callback:
            self.__connect_callback(client, user_data, flags, result_code, *extra_params)
        if result_code == 0:
            self.__is_connected = True
            logger.info("connection WaveletAI MQTT SUCCESS")
            logger.debug(client)
        else:
            if result_code in result_codes:
                logger.error("connection FAIL with error %s %s", result_code, result_codes[result_code])
            else:
                logger.error("connection FAIL with unknown error")

    def _on_message(self, client, user_data, message):
        content = self.decode(message)
        logger.debug("topic{},payload{}".format(message.topic, content))

    def connect(self, callback=None, min_reconnect_delay=1, timeout=120,
                tls=False, ca_certs=None, cert_file=None, key_file=None, keepalive=60):
        if tls:
            self._client.tls_set(ca_certs=ca_certs,
                                 certfile=cert_file,
                                 keyfile=key_file,
                                 cert_reqs=ssl.CERT_REQUIRED,
                                 tls_version=ssl.PROTOCOL_TLSv1_2,
                                 ciphers=None)
            self._client.tls_insecure_set(False)
        self._client.connect(self.__host, self.__port, keepalive=keepalive)
        self.reconnect_delay_set(min_reconnect_delay, timeout)
        self._client.loop_start()
        self.__connect_callback = callback

    def is_connected(self):
        return self.__is_connected

    def disconnect(self):
        self._client.disconnect()
        logger.debug(self._client)
        logger.debug("Disconnecting from WaveletAI MQTT")
        self.__is_connected = False
        self._client.loop_stop()

    def stop(self):
        self.stopped = True

    def publish_data(self, topic, data, qos=0):
        data = dumps(data)
        if qos not in (0, 1):
            logger.exception("Quality of service (qos) value must be 0 or 1")
            raise Exception("Quality of service (qos) value must be 0 or 1")
        return self._client.publish(topic, data, qos)

    def decode(message):
        try:
            if isinstance(message.payload, bytes):
                content = loads(message.payload.decode("utf-8"))
            else:
                content = loads(message.payload)
        except JSONDecodeError:
            if isinstance(message.payload, bytes):
                content = message.payload.decode("utf-8")
            else:
                content = message.payload
        return content

    def max_inflight_messages_set(self, inflight):
        """Set the maximum number of messages with QoS>0 that can be part way through their network flow at once.
        Defaults to 20. Increasing this value will consume more memory but can increase throughput."""
        self._client.max_inflight_messages_set(inflight)

    def max_queued_messages_set(self, queue_size):
        """Set the maximum number of outgoing messages with QoS>0 that can be pending in the outgoing message queue.
        Defaults to 0. 0 means unlimited. When the queue is full, any further outgoing messages would be dropped."""
        self._client.max_queued_messages_set(queue_size)

    def reconnect_delay_set(self, min_delay=1, max_delay=120):
        """The client will automatically retry connection. Between each attempt it will wait a number of seconds
         between min_delay and max_delay. When the connection is lost, initially the reconnection attempt is delayed
         of min_delay seconds. It’s doubled between subsequent attempt up to max_delay. The delay is reset to min_delay
          when the connection complete (e.g. the CONNACK is received, not just the TCP connection is established)."""
        self._client.reconnect_delay_set(min_delay, max_delay)
