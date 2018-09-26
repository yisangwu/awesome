from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    from awesome.config import myapps
    from awesome.loader import loader_memcached
    xx_cache = loader_memcached.one.get('xx')
    str = 'application index xx-cache:%s, config-apps:%s' %(xx_cache, myapps.MY_APPS)
    return HttpResponse(str)


def first(request):
    return HttpResponse('application first path:%s' % request.path)


def get_one(request):
    from application.app_models.models_userinfo import UserInfo
    uinfo = list()
    for i in range(1, 20):
        uinfo.append(UserInfo.get_userinfo_byid(i))
    return HttpResponse(uinfo)


def get_all(request):
    from application.app_models.models_userinfo import UserInfo

    uinfo = UserInfo.get_one_userinfo(20)
    return HttpResponse(uinfo)



def insert_one(request):
    from application.app_models.models_golbaluid import AppGlobalId
    from application.app_models.models_userinfo import UserInfo
    uid = AppGlobalId.get_new_uid()
    if not uid:
        ret = 'AppGlobalId.get_new_uid() None'
        return HttpResponse(ret)
    
    import random
    uinfo = dict(
        nickname='人生若是如初见',
        gender=random.randint(0,2),
        usersig='还是说说呵呵',
        userarea='火星',
    )
    # ret = UserInfo.insert_userinfo_byid(uid, uinfo)
    ret = UserInfo.insert_one_userinfo(uid, uinfo)
    return HttpResponse('%s ------ %s' % (uinfo, ret))


def insert_all(request):
    pass



def detail(request, id):
    str = 'application detail %s. path:%s' % (id, request.path)
    return HttpResponse(str)


def results(request, id):
    return HttpResponse('application results %s. path:%s' % (id, request.path))


def vote(request, id):
    return HttpResponse('application vote %s. path:%s' % (id, request.path))
