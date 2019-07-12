from api.models.base import BaseModel
from extensions import db


class Child(BaseModel):
    __tablename__ = 'child'

    child_name = db.Column(db.String(128), nullable=True, comment='孩子名字')
    child_sex = db.Column(db.String(128), nullable=True, comment='孩子性别')
    child_age = db.Column(db.String(128), nullable=True, comment='孩子年龄')

