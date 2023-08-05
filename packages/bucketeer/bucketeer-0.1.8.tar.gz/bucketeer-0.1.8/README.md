
# 🌊 Bucketeer

#### Still in developement.


Bucketeer allows you to automatically use the lowest keys for your external API requests..

```python

from bucketeer.bucketeer import Bucketeer, BucketeerContext
from bucketeer.objects.service import Service
from bucketeer.objects.key import Key
from bucketeer.connections.local import LocalReferencer



current_keys = [
    Key("Main Key", properties={"client_id": "data", "client_secret": "data"}, weight=5),
    Key("Backup Key", properties={"client_id": "data", "client_secret": "data"}, weight=2),
    Key("Backup Backup Key", properties={"client_id": "data", "client_secret": "data"}, weight=3),

]
current_service = Service("testService", current_keys)

referencer = LocalReferencer([current_service], raise_exceptions=True)

bucketeer = Bucketeer(referencer)

```
