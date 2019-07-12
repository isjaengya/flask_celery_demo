from api.libs.schema.activity import ActivitySchema
from api.libs.schema.award_site import AddressSchema
from api.libs.schema.child import ChildSchema, ChildPhotoLikeSchema, ChildPicSchema
from api.libs.schema.family import FamilySchema, BaseFamilySchema, FamilyQuerySchema, FamilyJoinSchema, FamilyRankingListSchema
from api.libs.schema.task import TaskSchema

child_schema = ChildSchema()
family_schema = FamilySchema()
base_family_schema = BaseFamilySchema()
family_query_schema = FamilyQuerySchema()
family_join_schema = FamilyJoinSchema()
family_ranking_list_schema = FamilyRankingListSchema(many=True)
child_photo_like_schema = ChildPhotoLikeSchema()
address_schema = AddressSchema()
activity_schema = ActivitySchema()
task_schema = TaskSchema()
child_pic_schema = ChildPicSchema()

__all__ = [
    'family_schema', 'child_schema', 'base_family_schema', 'family_query_schema', 'family_join_schema', 'family_ranking_list_schema',
    'child_photo_like_schema', 'address_schema', 'activity_schema', 'task_schema', 'child_pic_schema'
]
