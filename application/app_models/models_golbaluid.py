from django.db import models
from application.apps import ApplicationConfig
from awesome.helper import helper_datetime

# 表前缀
TABLE_PRE = ApplicationConfig.DB_APP_TABLE_PRE
# 表所属的APP
APP_LABEL = ApplicationConfig.DB_APP_LABEL


class AppGlobalId(models.Model):
    """
    全局自增ID
    """
    uid = models.AutoField('自增ID作为用户ID', primary_key=True)
    create_time = models.PositiveIntegerField('写入时间', null=False, blank=False)

    class Meta:
        managed = True  # 默认值为True，这意味着Django可以使用syncdb和reset命令来创建或移除对应的数据库
        db_table = TABLE_PRE + 'global_id'  # 自定义表名
        verbose_name = verbose_name_plural = '全局自增ID'  # 自定义的表名称, verbose_name_plural 为复数形式
        app_label = APP_LABEL  # 指定所属app

    @classmethod
    def create_uid(cls):
        """
        生成UID
        :return:
        """
        params = dict(create_time=helper_datetime.now())
        ret_obj = AppGlobalId.objects.create(**params)
        return int(ret_obj.uid)

    @classmethod
    def get_new_uid(cls):
        """
        获取UID，递归处理 过滤的UID
        :return:
        """
        from application.apps import ApplicationConfig
        expect_uid_list = ApplicationConfig.EXPECT_ID_LIST
        uid = cls.create_uid()
        if uid not in expect_uid_list:
            return uid
        return cls.get_new_uid()
