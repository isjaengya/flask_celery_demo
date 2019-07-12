from marshmallow import fields

from api.libs.schema.base import BaseSchema


class ActivitySchema(BaseSchema):
    action = fields.String(required=True)

    class Meta:
        strict = True


