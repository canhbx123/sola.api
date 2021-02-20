import json
from bson import ObjectId
from datetime import datetime, date
from elasticsearch import serializer, compat, exceptions


class DefaultJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, bytes):
            return obj.decode("utf-8", "ignore")
        if isinstance(obj, ObjectId):
            return str(obj)
        if isinstance(obj, datetime):
            return int(datetime.timestamp(obj))
        if isinstance(obj, date):
            return obj.strftime('%Y/%m/%d')
            # return obj.strftime('%X %x')
        return json.JSONEncoder.default(self, obj)


class UpDownJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, bytes):
            return obj.decode("utf-8", "ignore")
        if isinstance(obj, ObjectId):
            return str(obj)
        if isinstance(obj, datetime):
            return int(datetime.timestamp(obj))
        return json.JSONEncoder.default(self, obj)


class JSONSerializerElastic(serializer.JSONSerializer):
    def dumps(self, data):
        if isinstance(data, compat.string_types):
            return data
        try:
            return json.dumps(data, default=self.default, ensure_ascii=True)
        except (ValueError, TypeError) as e:
            raise exceptions.SerializationError(data, e)
