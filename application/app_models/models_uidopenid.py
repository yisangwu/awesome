from django.db import models
from awesome.helper.helper_mysql import gen_multi_model
from application.apps import ApplicationConfig

TABLE_PRE = ApplicationConfig.DB_APP_TABLE_PRE
APP_LABEL = ApplicationConfig.DB_APP_LABEL


@gen_multi_model
class AppUidOpenid(models.Model):
    """
    uid = openid + plat
    """
    id = models.AutoField('自增id', primary_key=True)
    uid = models.PositiveIntegerField('用户ID', unique=True)
    openid = models.CharField('用户在第三方平台的ID', max_length=32, null=False, blank=False)
    plat = models.PositiveSmallIntegerField('第三方平台ID，自定义', null=False, blank=False)
    create_time = models.PositiveIntegerField('写入时间', null=False, blank=False)

    # 分表数量
    table_piece_number = 10

    class Meta:
        abstract = True  # 抽象类是不会对应数据库表
        db_table = TABLE_PRE + 'uid_openid'
        verbose_name = verbose_name_plural = '用户ID映射openid加plat'
        app_label = APP_LABEL

        unique_together = ('openid', 'plat')


# 这个方式可以创建多表， gen_multi_model 就是动态使用此方式
# class AppUidOpenid0(AppUidOpenid):
#     class Meta:
#         db_table = APP_TABLE_PRE + 'uid_openid0'
#         verbose_name = verbose_name_plural = '用户ID映射openid加plat-0'
