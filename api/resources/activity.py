import random

from webargs.flaskparser import use_args
from flask import current_app as app

from api.config import load_config
from api.libs.error import error
from api.libs.interface_tips import InterfaceTips
from api.libs.resource import BaseResource
from api.libs.schema import family_schema, child_schema, base_family_schema, family_query_schema, family_join_schema, \
    family_ranking_list_schema, activity_schema
from api.models import User, Achievement, Activity
from api.models.child import Child
from api.models.family import Family
from api.services.redis import redis_client
from utils.util import req_user_join_activity


class ActivityResource(BaseResource):
    # @use_args(activity_schema)
    # @BaseResource.get_user()
    @BaseResource.get_activity_user()
    def get(self):
        # 给用户增加一个活动记录，接口
        user = self.user
        f = Activity.find_by_uid(user.uid)
        if f is None:
            # 调用接口成功在添加
            req = req_user_join_activity(user.uid)
            if req is None:
                return True
            d = dict(uid=user.uid, activity_id=2443)
            result = Activity.add(**d)
            return True
        return False

# tets