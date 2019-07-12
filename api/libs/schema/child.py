from marshmallow import fields

from api.libs.schema.base import BaseSchema


class ChildSchema(BaseSchema):
    child_name = fields.String(required=True)
    child_sex = fields.String(required=True)
    child_age = fields.Int(required=True)

    class Meta:
        strict = True


class ChildPhotoLikeSchema(BaseSchema):
    child_photo_id = fields.Integer()

    class Meta:
        strict = True


class ChildPicSchema(BaseSchema):
    pic = fields.String()

    class Meta:
        strict = True
