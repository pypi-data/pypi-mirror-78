from time import time
from functools import lru_cache
from collections.abc import Mapping
import json

from copy import deepcopy
from contextlib import contextmanager

from spintop.models.serialization import get_serializer, get_json_serializer
from spintop.utils import utcnow_aware, dict_ops

from .models import AnalyticsResponse
from . import singer
from ..logs import _logger

logger = _logger('singer')

DATETIME_TYPE = {'type': 'string', 'format': 'date-time'}

REQUEST_ID = '_spintop_request_id'

SCHEMA_ADDITIONS = {
    singer.SEQUENCE : {"type": "integer"},
    singer.BATCHED_AT: DATETIME_TYPE,
    REQUEST_ID: {"type": "string"}
}

@lru_cache()
def utcdatetime(_currenttime):
    """Computed only if current time changes."""
    return utcnow_aware()

class SingerMessagesFactory(object):
    def __init__(self, stream_name, add_null_to_fields=True):
        self.stream_name = stream_name
        self.transform_schema_kwargs = dict(
            add_null_to_fields=add_null_to_fields
        )
        self.logger = logger.getChild(stream_name)

    def begin_batch(self):
        pass

    def schema(self, schema , key_properties):
        schema = deepcopy(schema)
        schema['properties'].update(SCHEMA_ADDITIONS)
        _schema_transform(schema, **self.transform_schema_kwargs)
        schema = change_keys_deep(schema, sanitize_key)
        return {
            'type': 'SCHEMA',
            'stream': self.stream_name,
            'key_properties': key_properties,
            'schema': schema
        }

    def record(self, data):
        current_time = int(time()*1000*1000)
        data.update({
            singer.SEQUENCE: current_time,
            singer.BATCHED_AT: utcdatetime(current_time).isoformat() # serialize right away
        })

        data = change_keys_deep(data, sanitize_key, remove_none)
        return {
            'type': 'RECORD',
            'stream': self.stream_name,
            'record': data
        }

class ModelSingerMessagesFactory(SingerMessagesFactory):
    def __init__(self, stream_name, record_cls, serializer, **kwargs):
        self.record_cls = record_cls
        self.serializer = serializer
        super().__init__(stream_name, **kwargs)

    def begin_batch(self):
        jsonschema = self.record_cls.dump_json_schema()
        return super().schema(jsonschema, key_properties=[])

    def schema(self, *args, **kwargs):
        raise TypeError('Model based message factory cannot receive a schema.')

    def record(self, data):
        """Data should be of type self.record_cls"""
        serialized = self.serializer.serialize(data, self.record_cls)
        return super().record(serialized)

class _NamedEndpointAccessor(object):
    def __init__(self, name):
        self.name = name
    
    def __get__(self, obj, cls):
        return NamedEndpoint(
            name=self.name,
            analytics=obj
        )

class NamedEndpoint(object):
    def __init__(self, name, analytics):
        self.name = name
        self.analytics = analytics
    
    def update(self, data):
        return self.analytics.update_named_stream(self.name, data)

class AbstractSingerTarget(object):
    add_null_to_fields = False

    steps = _NamedEndpointAccessor('steps')
    features = _NamedEndpointAccessor('features')
    
    def __init__(self):
        self.serializer = get_serializer('tabular')
    
    def get_endpoint(self, name):
        return getattr(self, name)

    def update_named_stream(self, name, records, stream_type=None):
        with self.stream(name, stream_type) as batch:
            for record in records:
                batch.record(record)

    @property
    def functions(self):
        return None # To be overwritten

    def send_messages_dict(self, messages_dict, request_id=None, stream_name=None):
        return self.send_messages(self.json_dumps_messages(messages_dict), stream_name=stream_name)

    def send_messages(self, messages_str, request_id=None, stream_name=None):
        raise NotImplementedError()

    @contextmanager
    def stream(self, stream_name, record_cls=None):
        if record_cls:
            factory = ModelSingerMessagesFactory(
                stream_name,
                record_cls,
                serializer=self.serializer,
                add_null_to_fields=self.add_null_to_fields
            )
        else:
            factory = SingerMessagesFactory(
                stream_name,
                add_null_to_fields=self.add_null_to_fields
            )

        batch = CollectMessagesFromFactory(factory)
        batch.begin_batch()
        yield batch
        batch.result = self.send_messages_dict(batch.messages, stream_name=stream_name)

    def json_dumps_messages(self, messages):
        serialized_messages = [self.serializer.serialize(msg) for msg in messages]
        return [json.dumps(ser_msg) for ser_msg in serialized_messages]

    def complete_response(self, response, request_id, stream_name):
        if request_id and not response.request_id:
            response.request_id = request_id

        if stream_name and not response.stream_name:
            response.stream_name = stream_name
        
        return response

class CollectMessagesFromFactory(object):
    def __init__(self, factory):
        self.messages = []
        self.result = None
        self.factory = factory

    def __getattr__(self, key):
        factory_fn = getattr(self.factory, key)
        def _wrapper(*args, **kwargs):
            message = factory_fn(*args, **kwargs)
            if message:
                self.messages.append(message)
        return _wrapper

### Replace datetime by string type.
_FIELD_TRANSFORM = {
    'datetime': lambda field: DATETIME_TYPE
}

def _schema_transform(schema, add_null_to_fields=True):
    try:
        fields = schema.get('properties', {})
    except AttributeError:
        return 
    
    for key, field in fields.items():
        # Try to get type in map, else keep same.
        # Also add null allowed everywhere.
        field.pop('default', None)
        most_important_field_type = get_field_type(field['type'])

        transformer = _FIELD_TRANSFORM.get(most_important_field_type, None)
        if transformer:
            update = transformer(field)
            field.update(update)

        if add_null_to_fields:
            field['type'] = [most_important_field_type, 'null']

        # in case it contains other properties (object)
        _schema_transform(field, add_null_to_fields=add_null_to_fields)

def get_field_type(field_type):
    if isinstance(field_type, str):
        return field_type
    elif field_type:
        for possible_type in field_type:
            if possible_type.lower() != 'null':
                return possible_type
    
    # Else
    return None


class RemoveValue(Exception):
    pass

def sanitize_key(key):
    return key.replace('.', '_')

def remove_none(value):
    if value is None:
        raise RemoveValue()
    else:
        return value

def noop(value):
    return value

def change_keys_deep(dict_obj, key_op, value_op=noop):
    new_flat = {}
    flat = dict_ops.flatten_dict(dict_obj)
    for key_tuple, value in flat.items():
        new_key_tuple = tuple(key_op(key) for key in key_tuple)
        try:
            new_flat[new_key_tuple] = value_op(value)
        except RemoveValue:
            pass

    return dict_ops.deepen_dict(new_flat)
