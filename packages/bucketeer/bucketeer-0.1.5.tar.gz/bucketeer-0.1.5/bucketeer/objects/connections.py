import typing

if typing.TYPE_CHECKING:
   from bucketeer.objects.key import Key
   from bucketeer.exceptions import KeyRetrievalFailure

class Connection:
    """ Base object to be inherited for custom connections """
    
    def _add_counter_to_key(self, key: str, service: str) -> bool:
        raise NotImplemented

    def _remove_counter_to_key(self, key:str, service: str) -> bool:
        raise NotImplemented 

    def get_lowest_used_key(self, service: str) -> "typing.Union[Key, typing.Union[bool, KeyRetrievalFailure]]":
        raise NotImplemented