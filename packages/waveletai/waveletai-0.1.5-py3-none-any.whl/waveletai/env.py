#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2020/6/30 10:29
@Author  : WaveletAI-Product-Team Janus
@license : (C) Copyright 2019-2022, Visionet(Tianjin)Information Technology Co.,Ltd.
@Site    : plus.xiaobodata.com
@File    : env.py
@Desc    : 
"""
from waveletai.entities.mqtt_repo import MqttRepo
from waveletai.entities.mqtt_topic import MqttTopic
from waveletai.entities.minio_repo import MinIORepo
from waveletai.entities.minio_bucket import MinioBucket

MINIO_HOST = "aiminio.xiaobodata.com:8888"

MINIO_BUCKET_TMP = {"module": "market", "bucketName": "tmp", "objectPath": "market/video/"}

MINIO_BUCKET = [MINIO_BUCKET_TMP]

MINIO_ENV = {
    "host": MINIO_HOST,
    "bucket": MINIO_BUCKET
}

MQTT_HOST = "frp.xiaobodata.com"
MQTT_PORT = 1883
MQTT_TOPIC_MARKET_VIDEO = {"module": "market", "topicFilter": "market/video",
                           "topicExpression": "market/video/{}", "timeout": 60000}
MQTT_TOPIC = [MQTT_TOPIC_MARKET_VIDEO]

MQTT_ENV = {
    "host": MQTT_HOST,
    "port": MQTT_PORT,
    "topic": MQTT_TOPIC
}

_topics = []
for topic in MQTT_ENV["topic"]:
    _topics.append(MqttTopic(topic["module"], topic["topicFilter"], topic["topicExpression"], topic["timeout"]))

_buckets = []
for bucket in MINIO_ENV["bucket"]:
    _buckets.append(MinioBucket(bucket["module"], bucket["bucketName"], bucket["objectPath"]))


def mqtt_repo(username=None, password=None):
    """
    获取系统Mqtt对象
    :param username:
    :param password:
    :return:
    """
    return MqttRepo(MQTT_ENV["host"], MQTT_ENV["port"], _topics, username, password)


def minio_repo(access_key=None, secret_key=None, secure=False):
    """
    获取系统minio对象
    :param username:
    :param password:
    :return:
    """
    return MinIORepo(MINIO_ENV["host"], _buckets, access_key, secret_key, secure)
