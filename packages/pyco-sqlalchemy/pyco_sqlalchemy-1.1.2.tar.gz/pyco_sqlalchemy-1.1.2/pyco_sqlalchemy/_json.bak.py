import sys
import json
import uuid
from pprint import pformat, pprint
from datetime import datetime, time
from collections import OrderedDict

pprint(sys.path, indent=2)


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        # cls = self.__class__
        print(type(obj), obj, str(obj))
        pprint(type(obj))
        if isinstance(obj, datetime):
            # '%Y-%m-%d %H:%M:%S.%f
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, time):
            return obj.strftime("%H:%M:%S")
        elif isinstance(obj, uuid.UUID):
            return str(obj)
        elif hasattr(obj, "_asdict"):
            return obj._asdict()
        elif hasattr(obj, 'to_json'):
            return obj.to_json()
        elif hasattr(obj, 'to_dict'):
            return obj.to_dict()
        elif hasattr(obj, 'json'):
            if callable(obj.json):
                return obj.json()
            else:
                return obj.json
        elif hasattr(obj, '__html__'):
            return str(obj.__html__())
        else:
            mp = pformat(obj, indent=2)
            print("JsonEncodeError", type(obj), mp)
            m = json.JSONEncoder.default(self, obj)
        return m


def json_format(data, indent=2):
    if isinstance(data, str):
        try:
            obj = json.loads(data)
            return json_format(obj, indent)
        except:
            return data
    else:
        return json.dumps(data, indent=indent, cls=CustomJSONEncoder)


def parse_json(data, default=None):
    if not data:
        return default
    elif isinstance(data, str):
        try:
            obj = json.loads(data)
            return obj
        except:
            return data
    else:
        return data


dt = datetime.utcnow()
dt2 = datetime.now()
m = dict(
    ct=dt,
    mt=dt2,
    obj=OrderedDict(c=2, b=1, d=datetime.time(dt2)),
    ob2=dict(c=2, b=1, d=datetime.time(dt2)),
    uid=uuid.uuid4(),
)

m1 = json_format(m)
pprint(m1, indent=2)

m2 = json.JSONDecoder(object_pairs_hook=OrderedDict).decode(m1)
pprint(m2)

m3 = json.JSONDecoder().decode(m1)
pprint(m3)
