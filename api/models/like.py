from api.models.base import BaseModel
from extensions import db


class Like(BaseModel):
    __tablename__ = 'like'

    uid = db.Column(db.String(256), index=True, comment='用户uid')
    child_photo_id = db.Column(db.Integer, index=True, comment='孩子照片id')
