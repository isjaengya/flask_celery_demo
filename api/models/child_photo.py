

from api.models.base import BaseModel
from extensions import db


class ChildPhoto(BaseModel):
    __tablename__ = 'child_photo'

    uid = db.Column(db.String(256), index=True, comment='用户uid')
    child_pic_url = db.Column(db.String(526), comment='孩子照片url')
    child_pic_num = db.Column(db.Integer, default=0, index=True, comment='孩子照片点赞数')
    recommend = db.Column(db.Integer, default=0, index=True, comment='是否推荐')

    @classmethod
    def get_ranking_list_100(cls):
        results = cls.query.order_by(cls.recommend.desc(), cls.child_pic_num.desc()).limit(100)
        # results = cls.query.order_by(cls.recommend.desc(), cls.child_pic_num.desc()).limit(50)
        return results

    @classmethod
    def find_by_uid(cls, uid):
        result = cls.query.filter(cls.uid == uid).first()
        if not result:
            return None
        return result
