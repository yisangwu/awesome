"""
mysql 的配置
多库的路由基类
"""
from awesome.helper import helper_dbrouter

DB_ENGINE = 'django.db.backends.mysql'
DB_HOST = '192.168.50.163'
DB_PORT = 3306
DB_USER = 'django'
DB_PASSWORD = '123456'

MYSQL_CONF = {
    'default': {
        'ENGINE': DB_ENGINE,
        'NAME': 'awesome_django_admin',
        'USER': DB_USER,
        'PASSWORD': DB_PASSWORD,
        'HOST': DB_HOST,
        'PORT': DB_PORT,
    },
    'awesome_app': {
        'ENGINE': DB_ENGINE,
        'NAME': 'awesome_app',
        'USER': DB_USER,
        'PASSWORD': DB_PASSWORD,
        'HOST': DB_HOST,
        'PORT': DB_PORT,
    },
    'awesome_admin': {
        'ENGINE': DB_ENGINE,
        'NAME': 'awesome_admin',
        'USER': DB_USER,
        'PASSWORD': DB_PASSWORD,
        'HOST': DB_HOST,
        'PORT': DB_PORT,
    },
    'awesome_data': {
        'ENGINE': DB_ENGINE,
        'NAME': 'awesome_data',
        'USER': DB_USER,
        'PASSWORD': DB_PASSWORD,
        'HOST': DB_HOST,
        'PORT': DB_PORT,
    },
}


class DBRouterApp(helper_dbrouter.MultiMysqlRouter):
    APP_LABEL = 'application'
    DB_NAME = 'awesome_app'


# class DBRouterAdmin(helper_dbrouter.MultiMysqlRouter):
#     APP_LABEL = 'application'
#     DB_NAME = 'awesome_app'
#
#
# class DBRouterData(helper_dbrouter.MultiMysqlRouter):
#     APP_LABEL = 'application'
#     DB_NAME = 'awesome_app'
