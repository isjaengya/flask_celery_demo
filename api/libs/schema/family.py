from marshmallow import fields

from api.libs.interface_tips import InterfaceTips
from api.libs.schema.base import BaseSchema
from api.libs.error import error


class FamilySchema(BaseSchema):
    # family_name = fields.String(required=True)
    # member_name = fields.String(required=True)
    # member_sex = fields.Method(required=True)
    # member_age = fields.Int(required=True)
    # member_city = fields.String(required=True)
    # child_name = fields.String(required=True)
    # child_sex = fields.String(required=True)
    # child_age = fields.Int(required=True)

    family_name = fields.String(required=True)
    member_name = fields.String(required=True)
    member_sex = fields.Method(missing='男')
    member_age = fields.String()
    member_city = fields.String(missing='北京')
    child_name = fields.String(required=True)
    child_sex = fields.String(missing='男')
    child_age = fields.String()

    class Meta:
        strict = True


class BaseFamilySchema(BaseSchema):
    family_name = fields.String()
    member_name = fields.String()
    member_sex = fields.Method()
    member_age = fields.Int()
    member_city = fields.String()
    id = fields.Int()

    class Meta:
        strict = True


class FamilyQuerySchema(BaseSchema):
    id = fields.Int()
    entry = fields.String()

    class Meta:
        strict = True


class FamilyJoinSchema(BaseSchema):
    invitation_code = fields.String(required=True)

    class Meta:
        strict = True


class FamilyRankingListSchema(BaseSchema):
    family_name = fields.String()
    run_total = fields.String()

    class Meta:
        strict = True


class FamilyPhotoSchema(BaseSchema):
    child_pic_url = fields.String()
    child_pic_num = fields.String()
    family_name = fields.String()
