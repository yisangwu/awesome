from django.db import models
from django.db import connection, connections
from awesome.helper.helper_mysql import gen_multi_model, dictfetchall
from awesome.helper.helper_datetime import now
from application.apps import ApplicationConfig


# connection.cursor()使用默认 connections['default'].cursor()
cursor = connections['awesome_app'].cursor()  
TABLE_PRE = ApplicationConfig.DB_APP_TABLE_PRE
APP_LABEL = ApplicationConfig.DB_APP_LABEL


@gen_multi_model
class UserInfo(models.Model):
    """
    用户信息
    """
    uid = models.PositiveIntegerField('用户ID', primary_key=True, null=False, blank=False)
    nickname = models.CharField('昵称', max_length=50, null=False, blank=False)
    gender = models.PositiveSmallIntegerField('性别', default=2, null=False, blank=False)
    usersig = models.CharField('个性签名', max_length=100, null=False, default='0', blank=False)
    userarea = models.CharField('所在区域', max_length=100, null=False, default='0', blank=False)
    regtime = models.PositiveIntegerField('注册时间', null=False, blank=False)
    entercount = models.PositiveIntegerField('登录天数', null=False, blank=False)
    entertme = models.PositiveIntegerField('最近一天第一次登录的时间', null=False, blank=False)

    # 分表数量
    table_piece_number = 10

    class Meta:
        abstract = True  # 抽象类是不会对应数据库表
        db_table = TABLE_PRE + 'userinfo'
        verbose_name = verbose_name_plural = '用户信息'
        app_label = APP_LABEL


    @classmethod
    def get_tb_byid(cls, uid=None):
        """
        根据用户ID获取分表
        """
        if not uid:
            return None
        return cls._meta.db_table + str(uid % cls.table_piece_number)


    @classmethod
    def get_userinfo_byid(cls, uid=None):
        ret_list = list()
        uid = int(uid or 0)
        if not uid:
            return ret_list

        table_name = cls.get_tb_byid(uid)
        sql = "SELECT * FROM {table} WHERE uid='{uid}' LIMIT 1"
        cursor.execute(sql.format(table=table_name, uid=uid))
        # raw = cursor.fetchall() 返回tuple
        raw = dictfetchall(cursor)

        return raw


    @classmethod
    def get_one_userinfo(cls, uid=None):
        ret_list = list()   
        uid = int(uid or 0)
        if not uid:
            return ret_list
        table_name = cls.get_tb_byid(uid)
        sql = "SELECT * FROM {table} WHERE uid='{uid}' LIMIT 1"
        one = UserInfo.objects.raw(sql.format(table=table_name, uid=uid))
        return one


    @classmethod
    def insert_userinfo_byid(cls, uid=None, uinfo=None):
        uid = int(uid or 0)
        if not uid:
            return None
        
        if not uinfo or not isinstance(uinfo, dict):
            return None

        time_now = now()
        param_dict = dict(
            uid=uid,
            nickname=uinfo.get('nickname', ''),
            gender=int(uinfo.get('gender', 0) or 0),
            usersig=uinfo.get('usersig', ''),
            userarea=uinfo.get('userarea', ''),
            regtime=int(time_now),
            entercount=1,
            entertme=int(time_now),
        )
        table_name = cls.get_tb_byid(uid)
        param_dict['table'] = table_name

        sql = '''INSERT INTO {table} SET uid={uid}, nickname='{nickname}', 
                gender={gender}, usersig='{usersig}', userarea='{userarea}',
                regtime={regtime}, entercount={entercount}, 
                entertme={entertme}'''


        sql = sql.format(
            table=table_name,
            uid=uid,
            nickname=uinfo.get('nickname', ''),
            gender=int(uinfo.get('gender', 0) or 0),
            usersig=uinfo.get('usersig', ''),
            userarea=uinfo.get('userarea', ''),
            regtime=time_now,
            entercount=1,
            entertme=time_now,
        )

        flag = cursor.execute(sql.format(param_dict))
        
        # 此方法提交当前事务。插入或删除或修改操作后,
        # 需要调用一下conn.commit()方法进行提交,数据才会真正保 存在数据库中
        connections['awesome_app'].commit()

        return flag


    @classmethod
    def insert_one_userinfo(cls, uid=None, uinfo=None):
        uid = int(uid or 0)
        if not uid:
            return None
        
        if not uinfo or not isinstance(uinfo, dict):
            return None

        time_now = now()
        table_name = cls.get_tb_byid(uid)
        
        param_dict = dict(
            table=table_name,
            uid=uid,
            nickname=uinfo.get('nickname', ''),
            gender=int(uinfo.get('gender', 0) or 0),
            usersig=uinfo.get('usersig', ''),
            userarea=uinfo.get('userarea', ''),
            regtime=int(time_now),
            entercount=1,
            entertme=int(time_now),
        )
        sql = '''INSERT INTO %s SET uid=%u, nickname='%s', 
                gender=%u, usersig='%s', userarea='%s',
                regtime=%u, entercount=%u,entertme=%u'''
        
        flag = cursor.execute(sql % tuple(param_dict.values()))
            
        # 此方法提交当前事务。插入或删除或修改操作后,
        # 需要调用一下conn.commit()方法进行提交,数据才会真正保 存在数据库中
        connections['awesome_app'].commit()

        return flag
    
        