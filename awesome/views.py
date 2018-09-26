from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    from awesome.config import myapps
    from awesome.loader import loader_memcached
    xx_cache = loader_memcached.one.get('xx')


    str = 'awesome %s ' % request.path
    str += 'config-myapps:%s ' % myapps.MY_APPS
    str += 'loader-memcache:%s ' % xx_cache
    return HttpResponse(str)