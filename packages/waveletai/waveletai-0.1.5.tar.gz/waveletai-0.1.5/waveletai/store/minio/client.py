#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2020/6/29 10:29
@Author  : WaveletAI-Product-Team Janus
@license : (C) Copyright 2019-2022, Visionet(Tianjin)Information Technology Co.,Ltd.
@Site    : plus.xiaobodata.com
@File    : minio.py
@Desc    : Minio客户端操作类
"""
from waveletai import logger
from minio import Minio
from waveletai.entities.minio_repo import MinIORepo
from minio.error import ResponseError

MAX_MULTIPART_COUNT = 10000  # 10000 parts
MAX_MULTIPART_OBJECT_SIZE = 5 * 1024 * 1024 * 1024 * 1024  # 5TiB
MAX_PART_SIZE = 5 * 1024 * 1024 * 1024  # 5GiB
MAX_POOL_SIZE = 10
MIN_PART_SIZE = 5 * 1024 * 1024  # 5MiB
DEFAULT_PART_SIZE = MIN_PART_SIZE  # Currently its 5MiB


class MinioClient:
    def __init__(self, minio_repo):
        if isinstance(minio_repo, MinIORepo):
            self.uri = minio_repo.host
            self.access_key = minio_repo.access_key
            self.secret_key = minio_repo.secret_key
            self.secure = minio_repo.secure
            self.__client = Minio(self.uri, self.access_key, self.secret_key, None, self.secure)
            self.progress = None
        else:
            raise TypeError("MinioClient require <MinIORepo> class type as input")

    def stat_object(self, bucket_name, object_name):
        """
        检查对象是否存在

        :param bucket_name: Bucket of object.
        :param object_name: Name of object
        :return: Object metadata if object exists
        """
        try:
            return self.__client.stat_object(bucket_name, object_name)
        except ResponseError as err:
            logger.error(err)
            raise err

    def put_object(self, bucket_name, object_name, data, length, content_type='application/octet-stream',
                   metadata=None, progress=None, part_size=DEFAULT_PART_SIZE):
        """
        上传对象到服务器
        Add a new object to the cloud storage server.

        NOTE: Maximum object size supported by this API is 5TiB.

        Examples:
         file_stat = os.stat('hello.txt')
         with open('hello.txt', 'rb') as data:
             minio.put_object('foo', 'bar', data, file_stat.st_size, 'text/plain')

        - For length lesser than 5MB put_object automatically
          does single Put operation.
        - For length larger than 5MB put_object automatically
          does resumable multipart operation.

        :param bucket_name: Bucket of new object.
        :param object_name: Name of new object.
        :param data: Contents to upload.
        :param length: Total length of object.
        :param content_type: mime type of object as a string.
        :param metadata: Any additional metadata to be uploaded along
            with your PUT request.
        :param progress: A progress object
        :param part_size: Multipart part size
        :return: etag
        """
        try:
            return self.__client.put_object(bucket_name, object_name, data, length, content_type,
                                            metadata, None, progress, part_size)
        except ResponseError as err:
            logger.error(err)
            raise err

    def fput_object(self, bucket_name, object_name, file_path, content_type='application/octet-stream',
                    metadata=None, progress=None, part_size=DEFAULT_PART_SIZE):
        """
        上传对象文件到桶

        Examples:
            minio.fput_object('foo', 'bar', 'filepath', 'text/plain')

        :param bucket_name: Bucket to read object from.
        :param object_name: Name of the object to read.
        :param file_path: Local file path to be uploaded.
        :param content_type: Content type of the object.
        :param metadata: Any additional metadata to be uploaded along
            with your PUT request.
        :param progress: A progress object
        :param part_size: Multipart part size
        :return: etag
        """
        try:
            return self.__client.fput_object(bucket_name, object_name,
                                             file_path, content_type, metadata, None, self.progress, part_size)
        except ResponseError as err:
            logger.error(err)
            raise err

    def get_object(self, bucket_name, object_name):
        """
        获取桶中的对象

        This function returns an object that contains an open network
        connection to enable incremental consumption of the
        response. To re-use the connection (if desired) on subsequent
        requests, the user needs to call `release_conn()` on the
        returned object after processing.

        Examples:
          my_object = minio.get_partial_object('foo', 'bar')

        :param bucket_name: Bucket to read object from
        :param object_name: Name of object to read
        :param request_headers: Any additional headers to be added with GET request.
        :return: :class:`urllib3.response.HTTPResponse` object.

        """
        try:
            return self.__client.get_object(bucket_name, object_name)
        except ResponseError as err:
            logger.error(err)
            raise err

    def fget_object(self, bucket_name, object_name, file_path):
        """
        获取桶中的对象到文件

        Examples:
        client.fget_object('foo', 'bar', 'localfile')

        :param bucket_name: Bucket to read object from.
        :param object_name: Name of the object to read.
        :param file_path: Local file path to save the object.
        :return:
        """
        try:
            return self.__client.fget_object(bucket_name, object_name, file_path)
        except ResponseError as err:
            logger.error(err)
            raise err

    def remove_object(self, bucket_name, object_name):
        """
        从桶中删除对象

        :param bucket_name: Bucket of object to remove
        :param object_name: Name of object to remove
        :return: None
        """
        try:
            return self.__client.remove_object(bucket_name, object_name)
        except ResponseError as err:
            logger.error(err)
            raise err

    def list_objects(self, bucket_name, prefix=''):
        """
        从桶中删除对象

        :param bucket_name: Bucket of object to remove
        :param object_name: Name of object to remove
        :return: None
        """
        try:
            return self.__client.list_objects(bucket_name, prefix)
        except ResponseError as err:
            logger.error(err)
            raise err

    def list_buckets(self):
        """
        从桶中删除对象

        :param bucket_name: Bucket of object to remove
        :param object_name: Name of object to remove
        :return: None
        """
        try:
            return self.__client.list_buckets()
        except ResponseError as err:
            logger.error(err)
            raise err
