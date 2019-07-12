import random
from webargs.flaskparser import use_args

from api.libs.error import error
from api.libs.interface_tips import InterfaceTips
from api.libs.output import UserVerifyInfo
from api.libs.resource import BaseResource
from api.libs.schema import family_schema, child_schema, base_family_schema, family_query_schema, family_join_schema, \
    family_ranking_list_schema, task_schema
from api.models import User, Achievement, ChildPhoto, Address
from api.models.child import Child
from api.models.family import Family
from api.services.redis import redis_client

from flask import request


class TaskResource(BaseResource):
    @BaseResource.get_user()
    @use_args(task_schema)
    def get(self, args):
        user = self.user
        task = args.get('task')
        if task not in (1, 2, 3):
            return UserVerifyInfo.TASK_ERROR.value

        if task == 1:
            if user.family_id is None:
                return False
            family = Family.find_by_id(user.family_id)
            if family.run_total < 1:
                return False
            return True

        if task == 2:
            result = ChildPhoto.find_by_uid(user.uid)
            if result is None:
                return False
            return True

        if task == 3:
            result = Address.find_by_uid(user.uid)
            if result is None:
                return False
            return True
