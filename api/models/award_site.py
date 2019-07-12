from api.models.base import BaseModel
from extensions import db


class Address(BaseModel):
    __tablename__ = 'address'

    uid = db.Column(db.String(256), index=True, comment='用户uid')
    name = db.Column(db.String(128), comment='用户提交快递名字')
    phone = db.Column(db.String(128), comment='手机号')
    city = db.Column(db.String(128), comment='城市')
    district = db.Column(db.String(128), comment='县/区')
    detailed_address = db.Column(db.String(128), comment='详细地址')

    @classmethod
    def find_by_uid(cls, uid):
        result = cls.query.filter(cls.uid == uid).first()
        if not result:
            return None
        return result