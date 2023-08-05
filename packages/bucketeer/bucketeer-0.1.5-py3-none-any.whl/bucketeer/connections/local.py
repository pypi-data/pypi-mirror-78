import typing

from loguru import logger
import uuid

from bucketeer.exceptions import (KeyLookupAdditionCountFailure,
                                  KeyLookupSubtractionCountFailure,
                                  KeyRetrievalFailure)
from bucketeer.helpers.convert_dict_lookup_struct import \
    _convert_to_dict_lookup_structure
from bucketeer.objects.connections import Connection
from bucketeer.objects.service import Service

if typing.TYPE_CHECKING:
    from bucketeer.objects.key import Key



class LocalReferencer(Connection):
    def __init__(self, services: "typing.List[Service]", **kwargs):
        self._user_defined_kwargs = kwargs

        for service_unverified in services:
            if self._user_defined_kwargs.get("ignore_assertion_for_services", None):
                logger.warning(f"Ignoring assertion errors.")
            else:
                assert isinstance(service_unverified, Service), f"Invalid service item ({service_unverified} {type(service_unverified)}) in service list."
            
        self._referencer = {
            "services": {}
        }

        for service in services:
            self._referencer["services"][service.name] = {
                "lookup": {},
                "watcher": {}
            }
            for key in service.key_list:
                generate_unique_id_for_key = str(uuid.uuid4())
                self._referencer["services"][service.name]["lookup"][generate_unique_id_for_key] = key
                self._referencer["services"][service.name]["watcher"][generate_unique_id_for_key] = 0
                key.properties['_bucketeer'] = {
                    "service": service.name,
                    "unique": generate_unique_id_for_key
                }

        self._referencer_watcher_keys = {
            x.name: self._referencer["services"][x.name]['watcher'].keys()
            for x in services
        }
    
    def _add_counter_to_key(self, key: str, service: str) -> bool:
        try:
            self._referencer["services"][service]["watcher"][key] += 1
            return True
        except Exception:
            if self._user_defined_kwargs.get("raise_exceptions"):
                raise KeyLookupAdditionCountFailure
            return False

    def _remove_counter_to_key(self, key: "Key") -> bool:
        try:
            selected_service = key._bucketeer_properties['service']
            selected_lookup_key = key._bucketeer_properties['unique']
            if self._referencer['services'][selected_service]['watcher'][selected_lookup_key] - 1 < 0:
                logger.warning("Value would go lower then 0.")
            else:
                self._referencer['services'][selected_service]['watcher'][selected_lookup_key] - 1
        except Exception:
            if self._user_defined_kwargs.get('raise_exceptions'):
                raise KeyLookupSubtractionCountFailure
            return False

    def get_lowest_used_key(self, service: str) -> "typing.Union[Key, typing.Union[bool, KeyRetrievalFailure]]":
        try:
            lowest_value_item = min(
                self._referencer_watcher_keys[service], key=(lambda k: self._referencer["services"][service]['watcher'][k])
            )
            self._add_counter_to_key(service=service, key=lowest_value_item)
            return self._referencer["services"][service]['lookup'][lowest_value_item]
        except Exception:
            if self._user_defined_kwargs.get("raise_exceptions"):
                raise KeyRetrievalFailure
            return False         



class DictReference(Connection):
    def __init__(self, services: "typing.List[Service]", **kwargs):
        """ This connection uses a dict to reference keys """
        
        self.__user_defined_kwargs = kwargs

        for service_unverified in services:
            assert isinstance(service_unverified, Service), f"Invalid service item ({service_unverified} {type(service_unverified)}) in service list."

        self._key_referencing = {}
        self._referencer = _convert_to_dict_lookup_structure(services)

    def _add_counter_to_key(self, key: "str", service: str) -> bool:
        try:
            self._referencer['services'][service]["watch"][key] += 1
            return True
        except Exception:
            if self.__user_defined_kwargs.get("raiseExceptions"):
                raise KeyLookupAdditionCountFailure
            return False
    
    def _remove_counter_to_key(self, key: "str", service: str) -> bool:
        try:
            if self._referencer['services'][service]["watch"][key] - 1 < 0:
                logger.warning("Attempted to go below zero for key..")
            else:
                self._referencer['services'][service]["watch"][key]  -= 1
                return True
        except Exception:
            if self.__user_defined_kwargs.get("raiseExceptions"):
                raise KeyLookupSubtractionCountFailure
            logger.exception("unable to remove key..")
            return False

    def get_lowest_used_key(self, service: str) -> dict:
        try:
            lowest_value_item = min(
                self._referencer['services'][service]['watch'].keys(), key=(lambda k: self._referencer["services"][service]['watch'][k])
            )
            self._add_counter_to_key(service=service, key=lowest_value_item)

            return {
                "_key": lowest_value_item,
                "_amt": self._referencer['services'][service]["watch"][lowest_value_item],
                "_ser": service
            }
        except Exception:
            if self.__user_defined_kwargs.get("raiseExceptions"):
                raise KeyLookupSubtractionCountFailure
            return None      
