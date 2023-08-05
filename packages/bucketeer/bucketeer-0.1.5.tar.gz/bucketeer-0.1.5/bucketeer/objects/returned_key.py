

class ReturnedKey(object):
    def __init__(self, key_value, key_watcher_amount=0, service="N/A"):
        self._key_value = key_value
        self._key_watcher_amount = key_watcher_amount
        self._service = service

    @property
    def service(self):
        return self._service

    @property
    def key(self):
        return self._key_value
    
    @property
    def key_watcher_amount(self):
        if self._key_watcher_amount == 0:
            return None
        return self._key_watcher_amount

    def __str__(self) -> str:
        return self._key_value

    def __repr__(self) -> str:
        return f"<Returned Key For {self.service}>"