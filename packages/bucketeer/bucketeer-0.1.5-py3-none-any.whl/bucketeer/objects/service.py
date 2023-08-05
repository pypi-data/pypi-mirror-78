
import typing

from loguru import logger

from .key import Key


class Service:
    def __init__(self, service: str, keys: typing.List[Key]):
        self._service = service
        for key in keys:
            assert isinstance(key, Key), "Please use the key object."

        self.__keys__ = keys
        self.__raw_key_list = Service._generate_raw_key_list(keys)


    @staticmethod
    def _generate_raw_key_list(key_list: typing.List[Key]):
        new_list = []

        for key in key_list:
            for weight_add in range(0, key.weight):
                logger.info(f"adding weight: {weight_add}")
                new_list.append(key.key)
        
        return new_list

    @property
    def raw_key_list(self):
        return self.__raw_key_list


    @property
    def key_list_with_weights(self):
        new_list = []
        for key in self.key_list:
            logger.info(f"Adding weight: {key.weight} for {key.key}")
            for weight_add in range(0, key.weight):
                new_list.append(key)
        
        return new_list
                
    @property
    def key_list(self) -> typing.List[Key]:
        return self.__keys__

    @property
    def name(self):
        return self._service

    def __repr__(self) -> str:
        return f"<{self.name} - {len(self.__raw_key_list)} keys>"