from marshmallow import fields

from api.libs.schema.base import BaseSchema


class UserSchema(BaseSchema):

    child_name = fields.String(required=True)
    child_sex = fields.String(required=True)
    child_age = fields.Int(required=True)

    class Meta:
        strict = True


