from api.models.base import BaseModel
from extensions import db


class Achievement(BaseModel):
    __tablename__ = 'achievement'

    uid = db.Column(db.String(256), index=True, comment='用户uid')

    @classmethod
    def get_achievement_by_uid(cls, uid):
        return cls.query.filter(cls.uid == uid).first()

    @classmethod
    def verify_add(cls, uid):
        result = cls.get_achievement_by_uid(uid)
        if not result:
            Achievement.add(uid=uid)

