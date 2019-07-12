from api.models.base import BaseModel
from extensions import db


class Activity(BaseModel):
    __tablename__ = 'activity'

    uid = db.Column(db.String(256), index=True, comment='用户uid')
    activity_id = db.Column(db.Integer, index=True, comment='活动id')

    @classmethod
    def find_by_uid(cls, uid):
        result = cls.query.filter(cls.uid == uid).first()
        if not result:
            return None
        return result

