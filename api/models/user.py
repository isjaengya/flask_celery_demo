from api.models.base import BaseModel
from api.services.redis import redis_client
from extensions import db


class User(BaseModel):
    __tablename__ = 'user'

    uid = db.Column(db.String(256), index=True, comment='用户uid')
    family_id = db.Column(db.Integer, comment='家庭id')

    @classmethod
    def find_by_family_id(cls, _id):
        results = cls.query.filter(cls.family_id == _id).all()
        if not results:
            return []
        return results

    @classmethod
    def verify_join_family_num(cls, family_id):
        sql = ''' select count(*) from user where family_id = {} '''.format(family_id)
        count = db.session.execute(sql).fetchone()
        count = count[0] if count[0] else 0
        return True if count < 2 else False

    @classmethod
    def find_by_uid(cls, uid):
        result = cls.query.filter(cls.uid == uid).first()
        if not result:
            return None
        else:
            return result

    def like_photo(self, photo_id):
        photo_id = str(photo_id)
        _id = self.uid
        key = 'tebu_like_{}'.format(_id)
        # 先判断在不在这里面
        f = redis_client.sismember(key, photo_id)
        if f:
            # 点赞过返回false
            return False
        f = redis_client.exists(key)
        if f:
            redis_client.sadd(key, photo_id)
        else:
            redis_client.sadd(key, photo_id)
            redis_client.expire(key, 3600 * 24)

    def get_like_photo_ids(self):
        _id = self.uid
        key = 'tebu_like_{}'.format(_id)

        photo_ids = redis_client.smembers(key)

        return list(photo_ids)
