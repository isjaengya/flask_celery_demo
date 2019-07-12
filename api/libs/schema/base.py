import arrow
import uuid

from marshmallow import (Schema, fields, post_dump)
from flask import current_app


class UUIDString(fields.String):
    def _validated(self, value):
        """Format the value or raise a :exc:`ValidationError` if an error occurs."""
        if value is None:
            return None
        if isinstance(value, uuid.UUID):
            return str(value)
        try:
            uuid.UUID(value)
            return value
        except (ValueError, AttributeError):
            self.fail('invalid_uuid')

    def _serialize(self, value, attr, obj):
        validated = str(self._validated(value)) if value is not None else None
        return super(fields.String, self)._serialize(validated, attr, obj)

    def _deserialize(self, value, attr, data):
        return self._validated(value)


class BSchema(Schema):
    @post_dump
    def clear_none(self, data):
        result = {}
        for k, v in data.items():
            if v is None:
                continue
            elif isinstance(v, dict):
                result[k] = self.clear_none(v)
            else:
                result[k] = v
        return result


class BaseSchema(BSchema):
    id = fields.Int(dump_only=True)
    created_at = fields.Int(dump_only=True)

    class Meta:
        strict = True


class Timestamp(fields.DateTime):
    def _serialize(self, value, attr, obj):
        if value:
            return arrow.get(value).timestamp

    def _deserialize(self, value, attr, obj):
        return arrow.get(value).datetime


class BaseQuerySchema(BaseSchema):
    page = fields.Int(missing=1)
    per_page = fields.Int(missing=10)
    q = fields.Str(location='query')

    class Meta:
        strict = True


class StatusQuerySchema(BaseQuerySchema):
    status = fields.Int(location='query')

    class Meta:
        strict = True


class Uri(fields.String):
    def _serialize(self, value, attr, obj):
        if value is None:
            return

        if value == '':
            return value

        if 'http' in value:
            return value

        return 'http://{}/{}'.format(current_app.config['QINIU_CDN_DOMAIN'], value)

    def _deserialize(self, value, attr, data):
        if value is None:
            return

        if value == '':
            return value

        if value.startswith('http://{}/'.format(current_app.config['QINIU_CDN_DOMAIN'])):
            value = value[len('http://{}/'.format(current_app.config['QINIU_CDN_DOMAIN'])):]

        return value


class CoverUri(fields.String):
    def _serialize(self, value, attr, obj):
        if value is None:
            return

        if value == '':
            return value

        if 'http' in value:
            return value

        return 'http://{}/{}{}'.format(current_app.config['QINIU_CDN_DOMAIN'], value, current_app.config['COVER_STYLE'])

    def _deserialize(self, value, attr, data):
        if value is None:
            return

        if value == '':
            return value

        if value.startswith('http://{}/'.format(current_app.config['QINIU_CDN_DOMAIN'])):
            value = value[len('http://{}/'.format(current_app.config['QINIU_CDN_DOMAIN'])):]

        if value.endswith(current_app.config['COVER_STYLE']):
            value = value[:0-len(current_app.config['COVER_STYLE'])]

        return value


class QueryString(fields.Str):
    def _deserialize(self, value, attr, data):
        if value is None:
            return None

        return value.split(',')
