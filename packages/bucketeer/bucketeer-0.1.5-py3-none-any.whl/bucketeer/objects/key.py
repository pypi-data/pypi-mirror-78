
class Weights:
    DEFAULT = 1


class Key(object):
    def __init__(self, key, weight=Weights.DEFAULT, properties: dict = {}):
        self._key = key
        self._weight = weight
        self._properties = properties

        self._handle_bucketeer_properties = {}



    @property
    def _bucketeer_properties(self):
        if self._handle_bucketeer_properties == {}:
            # check if bucketeer already added unique properties..
            if self._properties.get("_bucketeer", False) != False:
                self._handle_bucketeer_properties = self._properties['_bucketeer']
                del self._properties['_bucketeer']
        return self._handle_bucketeer_properties


    @property
    def properties(self):
        if self._handle_bucketeer_properties == {}:
            # check if bucketeer already added unique properties..
            if self._properties.get("_bucketeer", False) != False:
                self._handle_bucketeer_properties = self._properties['_bucketeer']
                del self._properties['_bucketeer']
                
        return self._properties
        
    @property
    def weight(self):
        return self._weight

    @property
    def key(self):
        return self._key
    
    def __repr__(self) -> str:
        return f"<Key (weight={self._weight})"