import functools
import ujson
import json
from common.json_encode import DefaultJsonEncoder


def return_json(f):
    @functools.wraps(f)
    def inner(*a, **k):
        return json.dumps(f(*a, **k), cls=DefaultJsonEncoder)

    return inner
