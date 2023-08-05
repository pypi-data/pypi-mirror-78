
from bucketeer.objects.key import Key
from bucketeer.objects import key
from bucketeer.objects import service
import typing
from loguru import logger

from bucketeer.objects.connections import Connection
from bucketeer.objects.returned_key import ReturnedKey



class Bucketeer(object):
    def __init__(self, initialized_connection: typing.Type[Connection]):
        assert isinstance(initialized_connection, Connection), f"Invalid object passed as initalized connection."

        self._initalized_connection = initialized_connection
        
    @property
    def passed_object(self) -> Connection:
        return self._initalized_connection


class BucketeerContext(object):
    def __init__(self, bucketeer_object: Bucketeer, service_needed: str):
        assert isinstance(bucketeer_object, Bucketeer), "A valid bucketeer object is required."
        self._object = bucketeer_object
        self._selected_service = service_needed

        self._current_key = None


    def __enter__(self) -> Key:
        try:
            get_lowest_key_from_object = self._object.passed_object.get_lowest_used_key(service=self._selected_service)
            if get_lowest_key_from_object == False:
                logger.error("Unable to retrieve latest key.")
                return None
            self._current_key = get_lowest_key_from_object
            return get_lowest_key_from_object
        except Exception:
            logger.exception("unable to grab latest key due to unhandled error.")
            return None

    def __exit__(self, type, value, traceback):
        attempt_removal = self._object.passed_object._remove_counter_to_key(key=self._current_key)
        #logger.info(f"Removal: {attempt_removal}")
        



