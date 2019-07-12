from flask import Blueprint
from api.libs.api import CustomApi
from api.resources.activity import ActivityResource
from api.resources.award_site import AwardSiteResource
from api.resources.child_photo import ChildPhotoResource, ChildPhotoLikeResource, PicResource, \
    ChildPhotoRankingListResource, ChildPhotoLikeVisitorResource, ChildPhotoLikeRankingListResource

from api.resources.family import FamilyResource, FamilyJoinResource, FamilyRankingListResource, FamilyVisitorResource
from api.resources.task import TaskResource
from api.resources.user import UserResource, TestResource, UserInfoResource

api_bp_v1 = Blueprint('api_v1', __name__)
api_v1 = CustomApi(api_bp_v1, prefix='/v1')

api_v1.add_resource(FamilyResource, '/family')
api_v1.add_resource(FamilyVisitorResource, '/family/visitor')
api_v1.add_resource(FamilyJoinResource, '/family/user')
api_v1.add_resource(FamilyRankingListResource, '/ranking_list/family')

api_v1.add_resource(UserResource, '/chievement/tips')

api_v1.add_resource(ChildPhotoResource, '/child_photo')
api_v1.add_resource(ChildPhotoLikeVisitorResource, '/child_photo/visitor')
api_v1.add_resource(ChildPhotoRankingListResource, '/ranking_list/child_photo')
api_v1.add_resource(ChildPhotoLikeRankingListResource, '/ranking_list/child_photo/like')
api_v1.add_resource(ChildPhotoLikeResource, '/child_photo/like')

api_v1.add_resource(PicResource, '/pic/upload')

api_v1.add_resource(AwardSiteResource, '/address')

api_v1.add_resource(ActivityResource, '/activity')

api_v1.add_resource(TestResource, '/test')

api_v1.add_resource(TaskResource, '/task')

api_v1.add_resource(UserInfoResource, '/users')

BLUEPRINTS = [
    api_bp_v1
]

__all__ = ['BLUEPRINTS']
