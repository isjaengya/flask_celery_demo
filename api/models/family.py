from api.models.base import BaseModel
from extensions import db, testdb
from utils.util import req_user_gain_achievement, req_get_uid_info


class Family(BaseModel):
    __tablename__ = 'family'

    family_name = db.Column(db.String(128), index=True, nullable=True, comment='家庭名字')
    member_name = db.Column(db.String(128), nullable=True, comment='成员名字')
    member_sex = db.Column(db.String(128), nullable=True, comment='成员性别')
    member_age = db.Column(db.String(128), nullable=True, comment='成员命令')
    member_city = db.Column(db.String(128), nullable=True, comment='成员所在城市')
    invitation_code = db.Column(db.String(128), index=True, nullable=True, comment='家庭邀请码')
    child_id = db.Column(db.Integer, nullable=True, comment='孩子id')
    run_total = db.Column(db.Integer, default=0, comment='家庭总计跑步里程')
    task_stage = db.Column(db.Integer, default=0, comment='任务完成阶段')
    uid = db.Column(db.String(256), comment='用户uid')

    @classmethod
    def find_family_by_name(cls, name):
        exist = cls.query.filter(cls.family_name == name).first()
        return True if exist else False

    @classmethod
    def find_family_by_invitation_code(cls, code):
        family = cls.query.filter(cls.invitation_code == code).first()
        return family.id if family else None

    @classmethod
    def find_family_by_id(cls, _id, _uid):
        from api.models import User
        from api.models import Activity
        from api.models import Achievement
        # 先查询出这个家庭信息，在查询出加入这个家庭的其他用户信息
        family = cls.query.filter(cls.id == _id).first()
        if not family:
            return None
        other_members = User.find_by_family_id(family.id)

        uid_l = list()
        member_l = list()

        for member in other_members:
            uid = member.uid
            if isinstance(uid, str):
                if uid.isdigit():
                    uid = int(uid)
            elif isinstance(uid, int):
                uid = uid
            uid_l.append(uid)
            # 拿到成员id，查询名字
            nick, url = req_get_uid_info(uid)
            if str(family.uid) == str(uid):
                nick = family.member_name
            d = dict(nick=nick, head_url=url)
            member_l.append(d)

        # 孩子dict
        _d = dict(nick=family.get_child_name(), head_url=Family.get_child_head())
        member_l.append(_d)

        # 查询这个家庭累计里程，同时排名, yp_run 表user_run_0-user_run_127 按用户uid%128
        # 1560405600 2019-06-13 14:00:00 开始时间取用户参加本活动的时间
        # 1561305600 2019-06-23 24:00:00
        activity = Activity.find_by_uid(_uid)
        if activity is None:
            start_time = 1560391200
        else:
            start_time = activity.created_at

        meter_total = 0
        testdb.ping()
        cursor = testdb.cursor()
        for uid in uid_l:
            table_name = 'user_run_{}'.format(uid % 128)
            sql = '''select sum(meter) / 1000 from {} where uid = {} and status in (1, 4) and start_time > {} and end_time < 1561305600 '''.format(table_name, uid, start_time)
            # print(sql)
            cursor.execute(sql)
            meter = cursor.fetchone()
            meter = int(meter[0]) if meter[0] else 0
            meter_total += meter
        cursor.close()

        # 比较一下这个家庭薪的总里程是否和之前相等
        if family.run_total != meter_total and meter_total > 0:
            family.update(run_total=meter_total)

        if family.run_total >= 1:
            # TODO 调用java接口给这个用户增加成就
            f = req_user_gain_achievement(_uid)
            if f:
                family.update(task_stage=1)
                # 接口调用成功
                Achievement.verify_add(uid=_uid)

        current_run_total = family.run_total if family.run_total else 0
        sql = 'select count(*) from family where run_total > {}'.format(current_run_total)
        rank = db.session.execute(sql).fetchone()
        rank = rank[0] if rank[0] else 1
        # 累计爱心值 系数13
        if rank > 120:
            rank = rank * 13
        sql = 'select sum(run_total) from family'
        love_total = db.session.execute(sql).fetchone()
        love_total = int(love_total[0]) if love_total[0] else 0
        # love_total 爱心值 这里要*一个系数，暂定为13
        love_total = int(love_total * 27.1) - 639000
        # print(love_total)

        d = dict(family_name=family.family_name, member=member_l, family_meter=meter_total, rank=rank, love_total=love_total, invitation_code=family.invitation_code,
                 member_name=family.member_name, child_name=family.get_child_name())
        # print(d)
        return d

    @classmethod
    def get_ranking_list_100(cls):
        results = cls.query.order_by(cls.run_total.desc()).limit(100)
        return results

    # @classmethod
    # def get_achievement(cls, family_id):
    #     from api.models import Achievement
    #     Achievement.get_achievement_by_uid()

    @classmethod
    def get_family_photo_100(cls):
        results = cls.query.order_by(cls.child_pic_num.desc()).limit(100)
        return results

    @classmethod
    def get_family_task_stage(cls, family_id):
        result = cls.query.filter(cls.id == family_id).first()
        return result if result else None

    @classmethod
    def find_family_by_id_to_wx(cls, _id):
        from api.models import User
        # 先查询出这个家庭信息，在查询出加入这个家庭的其他用户信息
        family = cls.query.filter(cls.id == _id).first()
        if not family:
            return None
        other_members = User.find_by_family_id(family.id)

        uid_l = list()
        member_l = list()

        for member in other_members:
            uid = member.uid
            uid_l.append(uid)
            # 拿到成员id，查询名字
            nick, url = req_get_uid_info(uid)
            if str(family.uid) == str(uid):
                nick = family.member_name
            d = dict(nick=nick, head_url=url)
            member_l.append(d)

        _d = dict(nick=family.get_child_name(), head_url=Family.get_child_head())
        member_l.append(_d)

        d = dict(family_name=family.family_name, member=member_l, invitation_code=family.invitation_code, child_name=family.get_child_name())
        # print(d)
        return d

    def get_child_name(self):
        from api.models import Child
        return Child.find_by_id(self.child_id).child_name

    @classmethod
    def get_child_head(cls):
        return 'https://linked-runner.b0.upaiyun.com/avatar/avatar_default.png!/sq/200'
