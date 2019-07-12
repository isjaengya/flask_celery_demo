import random
from webargs.flaskparser import use_args

from api.libs.error import error
from api.libs.interface_tips import InterfaceTips
from api.libs.output import UserVerifyInfo
from api.libs.resource import BaseResource
from api.libs.schema import family_schema, child_schema, base_family_schema, family_query_schema, family_join_schema, family_ranking_list_schema
from api.models import User
from api.models.child import Child
from api.models.family import Family


class FamilyResource(BaseResource):
    @use_args(family_schema)
    @BaseResource.get_user()
    def post(self, args):
        user = self.user
        if user.family_id is not None:
            return UserVerifyInfo.JOIN_FAMILY.value
        family_name = args.get('family_name')
        for _s in '!@#$%^&*()_+-=<>?":{}[],.《》':
            if _s in family_name:
                return UserVerifyInfo.FAMILY_NAME_ERROR.value
        user = self.user
        # 先判断家庭存不存在
        exist = Family.find_family_by_name(args.get('family_name'))
        if exist:
            return UserVerifyInfo.FAMILY_NAME_EXIST.value

        child = Child.add_all(**args)
        child_s = child_schema.dump(child).data

        invitation_code = ''.join(random.sample('zyxwvutsrqponmlkjihgfedcba', 5)).upper()
        # 确保code不会重复
        f = Family.find_family_by_invitation_code(invitation_code)
        if f is not None:
            return UserVerifyInfo.CODE_REPETITION.value
        args['invitation_code'] = invitation_code

        args['child_id'] = child.id
        args['uid'] = user.uid

        family = Family.add_all(**args)
        family_s = base_family_schema.dump(family).data

        family_s.update(child_s)

        user.update(family_id=family.id)

        return {'id': family.id}

    @use_args(family_query_schema)
    @BaseResource.get_user()
    def get(self, args):
        user = self.user
        uid = user.uid
        _id = args.get('id')
        entry = args.get('entry')

        if _id is not None:
            family_s = Family.find_family_by_id(_id, uid)
            if not family_s:
                return UserVerifyInfo.DATA_EXIST.value

            return family_s

        if entry == 'status':
            return user.family_id if user.family_id is not None else False

        if entry == 'wx':
            family_s = Family.find_family_by_id_to_wx(_id)
            if not family_s:
                return UserVerifyInfo.DATA_EXIST.value

            return family_s

        if _id is None:
            # 查看自己的家庭信息
            family_id = user.family_id
            if family_id is None:
                return UserVerifyInfo.FAMILY_ERROR.value
            family_s = Family.find_family_by_id(family_id, uid)
            if not family_s:
                return UserVerifyInfo.DATA_EXIST.value

            return family_s

        return ''


class FamilyJoinResource(BaseResource):
    @use_args(family_join_schema)
    @BaseResource.get_user()
    def post(self, args):
        user = self.user
        code = args.get('invitation_code')
        family_id = Family.find_family_by_invitation_code(code)
        if not family_id:
            return UserVerifyInfo.INVITATION_CODE_DONT_EXIST.value

        f = User.verify_join_family_num(family_id)
        if not f:
            return UserVerifyInfo.FAMILY_ENOUGH.value
        if user.family_id is not None:
            return UserVerifyInfo.JOIN_FAMILY.value
        user.update(family_id=family_id)
        return family_id


class FamilyRankingListResource(BaseResource):
    def get(self):
        results = Family.get_ranking_list_100()
        s = family_ranking_list_schema.dump(results).data
        return s


class FamilyPhotoResource(BaseResource):
    def get(self):
        results = Family.get_family_photo_100()

        pass

    def post(self):
        pass


class FamilyVisitorResource(BaseResource):
    @use_args(family_query_schema)
    def get(self, args):
        _id = args.get('id')
        entry = args.get('entry')

        if _id is not None:
            family_s = Family.find_family_by_id_to_wx(_id)
            if not family_s:
                return UserVerifyInfo.DATA_EXIST.value

            return family_s

        return ''