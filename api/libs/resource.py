from urllib import parse
from functools import wraps
from flask import make_response

from flask import request, g
from flask_restful import Resource
from uuid import UUID

from api.libs.error import error
from api.libs.interface_tips import InterfaceTips
from api.libs.output import RoomsResourceStatus, UserVerifyInfo
from api.models import User
from utils.util import req_verify_sid, parse_cookie


class BaseResource(Resource):
    @classmethod
    def check_uuid(cls):
        def decorate(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                if len(list(kwargs.keys())) < 3:
                    record_id = list(kwargs.values())[0]
                    try:
                        UUID(record_id, version=4)
                    except ValueError:
                        return RoomsResourceStatus.FAIL.value
                return func(*args, **kwargs)

            return wrapper

        return decorate

    @classmethod
    def get_user(cls):
        def decorate(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                uid = None
                sid = None

                cookie = request.headers.get('Cookie')
                print('\n', cookie, 'cookie11111111111111111111111111111111111111111')
                if cookie is not None:
                    uid, sid = parse_cookie(cookie)
                    if not isinstance(uid, int) and uid is not None and sid is not None:
                        return UserVerifyInfo.COOKIE_ERROR.value

                if isinstance(uid, int) and sid is not None:
                    f = req_verify_sid(uid, sid)
                    if not f:
                        # 验证不通过
                        return UserVerifyInfo.UID_ERROR.value

                if uid is None:
                    return UserVerifyInfo.UID_NONE.value

                user = User.find_by_uid(uid)

                if not user:
                    user = User.add(uid=uid)

                cls.user = user
                return func(*args, **kwargs)

            return wrapper

        return decorate

    @classmethod
    def get_openid_user(cls):
        def decorate(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                uid = None
                sid = None

                uid = request.args.get('openid')
                if uid is None:
                    cookie = request.headers.get('Cookie')
                    if cookie is not None:
                        uid, sid = parse_cookie(cookie)
                        if not isinstance(uid, int) and uid is not None and sid is not None:
                            return UserVerifyInfo.COOKIE_ERROR.value

                if isinstance(uid, int) and sid is not None:
                    f = req_verify_sid(uid, sid)
                    if not f:
                        # 验证不通过
                        return UserVerifyInfo.UID_ERROR.value

                if uid is None:
                    return UserVerifyInfo.UID_NONE.value

                user = User.find_by_uid(uid)

                if not user:
                    user = User.add(uid=uid)

                cls.user = user
                return func(*args, **kwargs)

            return wrapper

        return decorate

    @property
    def current_user(self):
        try:
            uid = g.uid
            sid = g.sid
        except Exception as e:
            return error(InterfaceTips.INVALID_COOKIES)

        user = User.find_by_uid(uid)

        if uid is None:
            return error(InterfaceTips.MISSING_COOKIES)

        if not user:
            user = User.add(uid=uid)

        self._current_user = user
        return self._current_user

    @classmethod
    def get_index_user(cls):
        def decorate(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                uid = None
                sid = None

                cookie = request.headers.get('Cookie')
                print('\n', cookie, 'cookie11111111111111111111111111111111111111111')
                if cookie is not None:
                    uid, sid = parse_cookie(cookie)
                    if not isinstance(uid, int) and uid is not None and sid is not None:
                        return False

                if isinstance(uid, int) and sid is not None:
                    f = req_verify_sid(uid, sid)
                    if not f:
                        return UserVerifyInfo.UID_ERROR.value

                if uid is None:
                    return False

                user = User.find_by_uid(uid)

                if not user:
                    user = User.add(uid=uid)

                cls.user = user
                return func(*args, **kwargs)

            return wrapper

        return decorate

    @classmethod
    def get_activity_user(cls):
        def decorate(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                uid = None
                sid = None

                cookie = request.headers.get('Cookie')
                print('\n', cookie, 'cookie11111111111111111111111111111111111111111')
                if cookie is not None:
                    uid, sid = parse_cookie(cookie)
                    if not isinstance(uid, int) and uid is not None and sid is not None:
                        return True

                if isinstance(uid, int) and sid is not None:
                    f = req_verify_sid(uid, sid)
                    if not f:
                        # 验证不通过
                        return UserVerifyInfo.UID_ERROR.value

                if uid is None:
                    return True

                user = User.find_by_uid(uid)

                if not user:
                    user = User.add(uid=uid)

                cls.user = user
                return func(*args, **kwargs)

            return wrapper

        return decorate