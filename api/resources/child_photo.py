import os
import random
from webargs.flaskparser import use_args
from flask import request
from flask import current_app as app
from werkzeug.utils import secure_filename

from api.libs.error import error
from api.libs.interface_tips import InterfaceTips
from api.libs.output import UserVerifyInfo
from api.libs.resource import BaseResource
from api.libs.schema import family_schema, child_schema, base_family_schema, family_query_schema, family_join_schema, \
    family_ranking_list_schema, child_photo_like_schema, child_pic_schema
from api.models import User, Achievement
from api.models.child import Child
from api.models.family import Family
from api.models.child_photo import ChildPhoto
from api.models.like import Like
from api.services.redis import redis_client
from utils.upload_to_youpaiyun import upload_to_cdn
from utils.util import get_uid_info, req_get_uid_info


class ChildPhotoResource(BaseResource):
    @BaseResource.get_user()
    @use_args(child_pic_schema)
    def post(self, args):
        cdn_path = args.get('pic')
        if cdn_path is None:
            return UserVerifyInfo.PIC_ERROR.value
        if cdn_path == 'undefined':
            return UserVerifyInfo.CDN_PATH_ERROR.value
        # 先判断用户加入家庭没有，加入判断家庭状态
        user = self.user
        if user.family_id is None:
            return UserVerifyInfo.TASK_UNDONE.value

        family = Family.get_family_task_stage(user.family_id)
        if not family:
            return UserVerifyInfo.TASK_UNDONE.value

        if family.task_stage < 1:
            return UserVerifyInfo.TASK_UNDONE.value

        # f = ChildPhoto.find_by_uid(user.uid)
        # if f:
        #     return UserVerifyInfo.REPETITION_UPLOAD.value
        #
        # app.logger.debug(u'更新前端所用图片, url:{}'.format(cdn_path))
        # print(cdn_path)
        child_photo = ChildPhoto.find_by_uid(user.uid)
        if not child_photo:
            child_photo = ChildPhoto.add(uid=user.uid, child_pic_url=cdn_path)
        else:
            child_photo.update(child_pic_url=cdn_path)

        return child_photo.id

    @BaseResource.get_user()
    @use_args(child_photo_like_schema)
    def get(self, args):
        child_photo_id = args.get('child_photo_id')
        if child_photo_id is None:
            # 获取自己上传的照片
            user = self.user
            child_photo = ChildPhoto.find_by_uid(user.uid)
            if not child_photo:
                return dict(child_photo_id=0, child_pic_url='')
            return dict(child_photo_id=child_photo.id, child_pic_url=child_photo.child_pic_url)
        else:
            child_photo = ChildPhoto.find_by_id(child_photo_id)
            if not child_photo:
                return dict(child_photo_id=0, child_pic_url='')
            return dict(child_photo_id=child_photo.id, child_pic_url=child_photo.child_pic_url)


class ChildPhotoRankingListResource(BaseResource):
    @BaseResource.get_user()
    def get(self):
        user = self.user
        current_user_info = req_get_uid_info(user.uid)
        l = list()
        results = ChildPhoto.get_ranking_list_100()
        for result in results:
           # 有：点赞数 图片url
           # 没有: 上传者的头像，上传者名字，是否点赞
           # 在这里要判断一下这个用户有没有对查询出来的照片进行点赞
           # 获取当前用户全部点赞 child_photo_id
           uids = user.get_like_photo_ids()
           nick, head = req_get_uid_info(result.uid)
           is_like = str(result.id) in uids
           d = dict(nick=nick, head=head, child_pic_url=result.child_pic_url, child_pic_num=result.child_pic_num, child_photo_id=result.id, is_like=is_like)
           l.append(d)

        d = dict(current_user_info=current_user_info, ranking_info=l)

        return d


class ChildPhotoLikeResource(BaseResource):
    @use_args(child_photo_like_schema)
    @BaseResource.get_openid_user()
    def post(self, args):
        # 给照片点赞
        user = self.user
        child_photo_id = args.get('child_photo_id')
        redis_key = '{}_to_{}'.format(user.uid, child_photo_id)

        q = redis_client.get(redis_key)
        if q is None:
            # 当q是None的时候说明之前没有这个key。添加一个设置过期时间
            redis_client.set(redis_key, 0)
            redis_client.expire(redis_key, 86400)
        q = int(q) if q is not None else 1
        if q >= 5:
            return False

        # 点赞一个
        child_photo = ChildPhoto.find_by_id(child_photo_id)
        if not child_photo:
            return UserVerifyInfo.DATA_EXIST.value
        if child_photo.child_pic_num is None:
            child_photo.update(child_pic_num=1)
        else:
            child_photo.update(child_pic_num=child_photo.child_pic_num+1)

        Like.add(uid=user.uid, child_photo_id=child_photo_id)

        redis_client.incr(redis_key)
        return True

    @use_args(child_photo_like_schema)
    @BaseResource.get_user()
    def get(self, args):
        user = self.user
        child_photo_id = args.get('child_photo_id')
        redis_key = '{}_to_{}'.format(user.uid, child_photo_id)

        q = redis_client.get(redis_key)
        if q is None:
            return True

        q = int(q) if q is not None else 1
        if q < 5:
            return True
        return False


class PicResource(BaseResource):
    def post(self):
        pic_file = request.files['pic']
        pic_name = request.form['pic_name']
        file_save_path = '{}/tebu_pic/{}'.format(app.root_path, secure_filename(pic_name))
        pic_file.save(file_save_path)
        cdn_path = upload_to_cdn("/" + app.config['UPLOAD_FOLDER'] + "/" + '{}'.format(pic_name), file_save_path)
        if cdn_path is not None:
            # 删除图片
            os.remove(file_save_path)
        # app.logger.debug(u'更新前端所用图片, url:{}'.format(cdn_path))
        # print(cdn_path)
        return cdn_path


class ChildPhotoLikeVisitorResource(BaseResource):
    @use_args(child_photo_like_schema)
    def get(self, args):
        child_photo_id = args.get('child_photo_id')
        child_photo = ChildPhoto.find_by_id(child_photo_id)
        if not child_photo:
            return dict(child_photo_id=0, child_pic_url='')
        return dict(child_photo_id=child_photo.id, child_pic_url=child_photo.child_pic_url)


class ChildPhotoLikeRankingListResource(BaseResource):
    # 在照片列表点赞
    @BaseResource.get_user()
    @use_args(child_photo_like_schema)
    def get(self, args):
        child_photo_id = args.get('child_photo_id')
        if not child_photo_id:
            return UserVerifyInfo.CHILD_RANKING_LIST_PHOTO_ID.value

        # redis 存储这个人点赞的照片id
        user = self.user
        f = user.like_photo(child_photo_id)
        if f is False:
            return False

        # 点赞一个
        child_photo = ChildPhoto.find_by_id(child_photo_id)
        if not child_photo:
            return UserVerifyInfo.DATA_EXIST.value
        if child_photo.child_pic_num is None:
            child_photo.update(child_pic_num=1)
        else:
            child_photo.update(child_pic_num=child_photo.child_pic_num+1)

        Like.add(uid=user.uid, child_photo_id=child_photo_id)

        return True

