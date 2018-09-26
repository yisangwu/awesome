from django.apps import AppConfig


class ApplicationConfig(AppConfig):
    name = 'application'
    DB_APP_TABLE_PRE = 'app_'
    DB_APP_LABEL = 'application'

    # 过滤的UID
    EXPECT_ID_LIST = [2, 4, 5, 7, 8, 9, 10]
