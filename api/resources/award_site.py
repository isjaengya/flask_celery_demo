import random
from webargs.flaskparser import use_args

from api.libs.error import error
from api.libs.interface_tips import InterfaceTips
from api.libs.output import UserVerifyInfo
from api.libs.resource import BaseResource
from api.libs.schema import family_schema, child_schema, base_family_schema, family_query_schema, family_join_schema, \
    family_ranking_list_schema, address_schema
from api.models import User, Achievement, Address
from api.models.child import Child
from api.models.family import Family
from api.models.child_photo import ChildPhoto
from api.services.redis import redis_client


class AwardSiteResource(BaseResource):
    @use_args(address_schema)
    @BaseResource.get_user()
    def post(self, args):
        name = args.get('name')
        phone = args.get('phone')
        city = args.get('city')
        detailed_address = args.get('detailed_address')

        if not all([name, phone, city, detailed_address]):
            return UserVerifyInfo.ADDRESS_ERROR.value

        # 先判断加入家庭，家庭task_stage，
        user = self.user
        # 分析参数，前端传过来的是 city:北京，北京市，昌平
        city = args.get('city')
        if isinstance(city, str):
            if city.count(',') != 2:
                args['city'] = ''
                args['district'] = ''
            else:
                _, city, district = city.split(',')
                args['city'] = city
                args['district'] = district
        if user.family_id is None:
            return UserVerifyInfo.TASK_UNDONE.value

        family = Family.find_by_id(user.family_id)
        if family.task_stage < 1:
            return UserVerifyInfo.TASK_UNDONE.value

        child_photo = ChildPhoto.find_by_uid(user.uid)
        if not child_photo:
            return UserVerifyInfo.TASK_UNDONE_2.value

        address = Address.find_by_uid(user.uid)
        if address:
            return UserVerifyInfo.REPETITION_ADDRESS.value

        address = Address.add(uid=user.uid, **args)

        return address_schema.dump(address).data

    @BaseResource.get_user()
    def get(self):
        user = self.user
        address = Address.find_by_uid(user.uid)
        return address_schema.dump(address).data
