import arrow

from sqlalchemy import func
from extensions import db


class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    created_at = db.Column(db.Integer, default=lambda: arrow.now().timestamp)
    updated_at = db.Column(db.Integer, default=lambda: arrow.now().timestamp, onupdate=lambda: arrow.now().timestamp)

    def __repr__(self):
        return '<{} {}>' .format(self.__class__.__name__, self.id)

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter(cls.id == _id).first()

    @classmethod
    def find_by_ids(cls, _ids):
        if not _ids:
            return []
        return cls.query.filter(cls.id.in_(_ids)).all()

    @classmethod
    def add(cls, **kwargs):
        auto_commit = kwargs.pop('auto_commit', True)
        obj = cls(**kwargs)
        db.session.add(obj)
        try:
            if auto_commit:
                db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise

        return obj

    @classmethod
    def add_all(cls, **kwargs):
        auto_commit = kwargs.pop('auto_commit', True)
        keys = cls(**{}).get_columns()
        obj = cls(**{k: kwargs.get(k) for k in keys})
        db.session.add(obj)
        try:
            if auto_commit:
                db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

        return obj

    @classmethod
    def add_record_by_obj(cls, obj, auto_commit=True):
        db.session.add(obj)
        try:
            if auto_commit:
                db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
        return obj

    @classmethod
    def get_count(cls, q):
        count_q = q.statement.with_only_columns(
            [func.count()]).order_by(None)
        count = q.session.execute(count_q).scalar()
        return count

    @classmethod
    def get_count_with_cache(cls, q):
        count_q = q.statement.with_only_columns(
            [func.count()]).order_by(None)
        count = q.session.execute(count_q).scalar()
        return count

    @classmethod
    def get_valid_columns(cls, **kwargs):
        columns = {}
        for key, value in kwargs.items():
            if hasattr(cls, key):
                columns[key] = value
        return columns

    @classmethod
    def get_random_data(cls, limit=10):
        return cls.query.order_by(func.random()).limit(limit).all()

    def update(self, **kwargs):
        auto_commit = kwargs.pop('auto_commit', True)
        try:
            for k, v in kwargs.items():
                if hasattr(self, k):
                    setattr(self, k, v)

            db.session.add(self)
            if auto_commit:
                db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

        return self

    @classmethod
    def pagination(cls, query, page, per_page):
        return query.offset((page - 1) * per_page).limit(per_page).all()

    @classmethod
    def get_all(cls):
        return cls.query.all()

    def delete(self, auto_commit=True):
        db.session.delete(self)
        if auto_commit:
            db.session.commit()
        self.delete_cache_func()

    @classmethod
    def fetch_one(cls, **kwargs):
        return cls.query.filter_by(**kwargs).first()

    @classmethod
    def is_existed(cls, **kwargs):
        record = cls.fetch_one(**kwargs)
        return record is not None

    @classmethod
    def fetch(cls, **kwargs):
        return cls.query.filter_by(**kwargs).all()

    def to_json(self):
        return {c.key: getattr(self, c.key, None) for c in self.__class__.__table__.columns}

    def get_columns(self):
        items = self.to_json()
        items.pop('id')
        items.pop('created_at')
        items.pop('updated_at')
        return items.keys()
