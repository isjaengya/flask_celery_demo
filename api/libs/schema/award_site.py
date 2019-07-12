from marshmallow import fields

from api.libs.schema.base import BaseSchema


class AddressSchema(BaseSchema):
    name = fields.String(required=True)
    phone = fields.String(required=True)
    city = fields.String(required=True)
    district = fields.String()
    detailed_address = fields.String(required=True)

    class Meta:
        strict = True


