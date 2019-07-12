from enum import Enum


class InterfaceTips(Enum):
    # [10000: 10100)
    INVALID_REQUEST = (400, 10000, '不合法的请求')
    SEX_ERROR = (400, 10000, '性别不对')
    INVALID_TOKEN = (400, 10001, '无效的token')
    EXPIRED_TOKEN = (400, 10002, 'token失效，请重新登陆')
    MISSING_TOKEN = (400, 10003, 'token 缺失')
    REVOKED_TOKEN = (400, 10004, 'token 已被收回')
    INVALID_SIGNATURE = (400, 10005, '签名出错')
    WRONG_SIGN_VERSION = (400, 10006, 'sign version 错误')
    MISSING_SIGN_HEADER = (400, 10007, '缺少 ts 或 sign 或 sv')
    INVALID_PHONE = (400, 10008, '手机号码格式不正确')
    MISSING_COOKIES = (400, 10009, 'cookies 缺失')
    INVALID_COOKIES = (400, 10010, 'cookies 无效')
    VERIFYING_ERROR = (400, 10011, 'cookies验证错误')
    PERMISSION_ERROR = (400, 10012, '权限错误')
    GET_USER_INFO_ERROR = (400, 10013, '获取用户信息失败')

    FAMILY_NAME_EXIST = (200, 10014, '家庭已存在')
    DATA_EXIST = (200, 10015, '数据不存在')
    FAMILY_ENOUGH = (200, 10016, '家庭成员已满')
    TASK_UNDONE = (200, 10017, '任务一未完成')
    TASK_UNDONE_2 = (200, 10017, '任务二未完成')
    REPETITION_UPLOAD = (200, 10018, '禁止重复上传')
    REPETITION_ADDRESS = (200, 10018, '禁止重复填写信息')
    JOIN_FAMILY = (200, 10019, '已经加入家庭')

