import os
import random
from webargs.flaskparser import use_args
from flask import current_app as app

from api.libs.error import error
from api.libs.interface_tips import InterfaceTips
from api.libs.output import UserVerifyInfo
from api.libs.resource import BaseResource
from api.libs.schema import family_schema, child_schema, base_family_schema, family_query_schema, family_join_schema, family_ranking_list_schema
from api.models import User, Achievement
from api.models.child import Child
from api.models.family import Family
from api.services.redis import redis_client

from flask import request

from utils.upload_to_youpaiyun import upload_to_cdn
from utils.util import req_get_uid_info, write_data_url_file, return_random_name, return_random_time
from tasks.celery_demo import celery_demo


class UserResource(BaseResource):
    # @BaseResource.get_user()
    @BaseResource.get_index_user()
    def get(self):
        user = self.user
        # 获取这个用户的成就
        result = Achievement.get_achievement_by_uid(user.uid)
        # 没有成就不提示
        if not result:
            return False

        # 如果有成就，判断是否提示过
        uid = user.uid
        redis_key = '_achievement_tips{}'.format(uid)
        f = redis_client.exists(redis_key)
        if f:
            # 存在，不提示
            return False
        else:
            redis_client.set(redis_key, 1)
            redis_client.expire(redis_key, 3600 * 24 * 30)
            return True


class TestResource(BaseResource):
    @use_args(family_query_schema)
    def post(self, args):
        # todo 这里是celery
        _id = args.get('id')
        celery_demo.apply_async(args=(_id,))
        return 1


class UserInfoResource(BaseResource):
    # @BaseResource.get_user()
    @BaseResource.get_index_user()
    @use_args(family_query_schema)
    def get(self, args):
        user = self.user
        entry = args.get('entry')
        if entry == 'user':
            nick, head = req_get_uid_info(user.uid)
            # 获取这个用户是否创建了家庭
            family = Family.find_by_id(user.family_id)
            if not family:
                return [nick, head, nick]
            if str(family.uid) == str(user.uid):
                return [nick, head, family.member_name]
            return [nick, head, nick]
