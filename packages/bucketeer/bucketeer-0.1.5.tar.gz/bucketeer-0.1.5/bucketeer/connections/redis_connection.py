
import os
import typing
import uuid

import redis
from loguru import logger

from bucketeer.exceptions import (KeyLookupAdditionCountFailure,
                                  KeyLookupSubtractionCountFailure,
                                  KeyRetrievalFailure)
from bucketeer.objects.connections import Connection
from bucketeer.objects.service import Service
    


class RedisReference(Connection):
    def __init__(self, services: "typing.List[Service]", **kwargs):
        
        self._do_not_overwrite_redis_host = False
        self._do_not_overwrite_redis_port = False

        self._arg_kwargs = kwargs

        for service_unverified in services:
            assert isinstance(service_unverified, Service), f"Invalid service item ({service_unverified} {type(service_unverified)}) in service list."

        if os.getenv("BucketeerRedisHost"):
            self._provided_redis_host = os.getenv("BucketeerRedisHost")
            self._do_not_overwrite_redis_host = True

        if os.getenv("BucketeerRedisPort"):
            self._provided_redis_port = os.getenv("BucketeerRedisPort")
            self._do_not_overwrite_redis_port = True

        if kwargs.get("provided_redis_host"):
            if self._do_not_overwrite_redis_host == True:
                logger.warning("Cannot overwrite if os env is already set for host.")
            else:
                self._provided_redis_host = kwargs.get("provided_redis_host")
        else:
            logger.warning("No redis host passed, using default host (localhost)")
            self._provided_redis_host = "localhost"

        if kwargs.get("provided_redis_port"):
            if self._do_not_overwrite_redis_port == True:
                logger.warning("Cannot overwrite if os env is already set for host.")
            else:
                self._provided_redis_port = kwargs.get("provided_redis_port")   
        else:
            logger.warning("No redis port passed, using default port (6379)")
            self._provided_redis_port = 6379

        if kwargs.get("provided_database"):
            self._provided_database = kwargs.get("provided_database")
        else:
            self._provided_database = 1

        self._redis_object = RedisReference._create_redis_connection_object(
            host=self._provided_redis_host,
            port=self._provided_redis_port,
            database=self._provided_database
        )     

        self._key_reference = {"services": {}}
        for service_passed in services:
            service_passed = service_passed # type: Service
            
            self._key_reference["services"][service_passed.name] = []
            for key in service_passed.raw_key_list:
                self._key_reference["services"][service_passed.name].append(key)
                self.redis_client.set(key, 0)

                
            





    @property
    def redis_client(self) -> redis.Redis:
        if self._arg_kwargs.get("ping_redis_before_use"):
            self._redis_object.ping()
        
        return self._redis_object

    def _get_key_value(self, key):
        return self.redis_client.get(key)

    @staticmethod
    def _create_redis_connection_object(host, port, database=1) -> redis.Redis:
        try:
            current_connection = redis.Redis(
                host=host,
                port=port,
                db=database
            )
            current_connection.ping()
            return current_connection
        except Exception:
            logger.exception("Issue with contacting redis instance.")
            return False

    def _remove_counter_to_key(self, key: str, service: str) -> bool:
        grab_key = self.redis_client.get(key['_key']) # type: bytes
        if grab_key:
            if int(grab_key.decode("utf-8")) - 1 > 0:
                logger.warning("lower value would go negative.")
            self.redis_client.decr(key["_key"], 1)

    def _add_counter_to_key(self, key: str, service: str) -> bool:
        grab_key = self.redis_client.get(key)
        if grab_key:
            self.redis_client.incr(key, 1)

    def get_lowest_used_key(self, service: str) -> dict:
        keys = {}
        for key in self._key_reference["services"][service]:
            keys[key] = self._get_key_value(key)
        
        lowest_key_value = min(self._key_reference['services'][service], key=lambda x: keys[x])

        self._add_counter_to_key(key=lowest_key_value, service=None)
        return {
            "_key": lowest_key_value,
            "_amt": 0 if int(keys[lowest_key_value].decode('utf-8')) is None else int(keys[lowest_key_value].decode('utf-8')),
            "_ser": service
        }