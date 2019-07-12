from marshmallow import fields

from api.libs.interface_tips import InterfaceTips
from api.libs.schema.base import BaseSchema
from api.libs.error import error


class TaskSchema(BaseSchema):
    task = fields.Int(required=True)

    class Meta:
        strict = True
