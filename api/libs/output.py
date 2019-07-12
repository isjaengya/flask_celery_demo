from api.libs.base_enum import BaseEnum


class RoomsResourceStatus(BaseEnum):
    SUCCESS = {'msg': 'success', "code": 200}
    FAIL = {'msg': 'miss data of room_id or card_ids', "code": 422}


class UserVerifyInfo(BaseEnum):
    UID_ERROR = {'msg': 'UID IS ERROR', 'code': 400}
    OPEN_ID_ERROR = {'msg': 'OPEN ID IS ERROR', 'code': 401}
    COOKIE_ERROR = {'msg': 'COOKIE IS ERROR', 'code': 402}
    UID_NONE = {'msg': 'UID IS NONE', 'code': 403}
    TASK_UNDONE = {'msg': '任务一未完成', 'code': 404}
    REPETITION_UPLOAD = {'msg': '禁止重复上传', 'code': 405}
    TASK_UNDONE_2 = {'msg': '任务二未完成', 'code': 406}
    DATA_EXIST = {'msg': '数据不存在', 'code': 407}
    FAMILY_NAME_EXIST = {'msg': '家庭已存在', 'code': 408}
    FAMILY_ENOUGH = {'msg': '很抱歉，您要加入的家庭成员已满，请选择加入其他家庭', 'code': 409}
    JOIN_FAMILY = {'msg': '您已有家庭，不可重复加入其他家庭', 'code': 410}
    TASK_ERROR = {'msg': 'task参数错误', 'code': 411}
    CODE_REPETITION = {'msg': '验证码重复，请重试', 'code': 412}
    FAMILY_NAME_ERROR = {'msg': '家庭名字不能含有特殊字符', 'code': 413}
    FAMILY_ERROR = {'msg': '未加入家庭', 'code': 414}
    FILE_ERROR = {'msg': '文件上传失败，请重试', 'code': 415}
    PIC_ERROR = {'msg': '没有url', 'code': 416}
    REPETITION_ADDRESS = {'msg': '禁止重复提交地址', 'code': 417}
    INVITATION_CODE_DONT_EXIST = {'msg': '邀请码不正确,请重新输入', 'code': 418}
    ADDRESS_ERROR = {'msg': '地址信息不完整', 'code': 419}
    CHILD_RANKING_LIST_PHOTO_ID = {'msg': '照片id错误', 'code': 420}
    CDN_PATH_ERROR = {'msg': '当前服务器繁忙，请退出重试', 'code': 421}
