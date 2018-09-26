"""
migrate 生成创建mysql表
"""
from application.app_models.models_golbaluid import AppGlobalId
from application.app_models.models_userinfo import UserInfo
from application.app_models.models_uidopenid import AppUidOpenid

ALL = [AppGlobalId, UserInfo, AppUidOpenid]


# 创建所有的model，数据库表
for obj in ALL:
    class InitDB(obj):
        class Meta:
            abstract = True
