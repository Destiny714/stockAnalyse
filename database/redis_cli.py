# -*- coding: utf-8 -*-
# @Time    : 2023/2/15 11:06
# @Author  : Destiny_
# @File    : redis_cli.py
# @Software: PyCharm
import redis


class RedisCli(object):
    _pool = None
    _instance = None

    def __init__(self):
        if self._pool is None:
            self._pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True, max_connections=200)

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def instance(self) -> redis.client.Redis:
        return redis.StrictRedis(connection_pool=self._pool)
